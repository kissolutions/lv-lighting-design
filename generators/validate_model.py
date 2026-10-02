"""Validate structure, traceability, and Phase 1 lighting assignments."""
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from decimal import Decimal
from pathlib import Path

from jsonschema import Draft202012Validator

SCHEMA_PATH = Path(__file__).resolve().parents[1] / "schemas/lighting-project.schema.json"


def read_model(path: str | Path) -> dict:
    def reject_constant(value):
        raise ValueError(f"Non-finite JSON number: {value}")

    def unique_keys(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"Duplicate JSON key: {key}")
            result[key] = value
        return result

    return json.loads(Path(path).read_text(encoding="utf-8"),
                      parse_constant=reject_constant, parse_float=Decimal,
                      object_pairs_hook=unique_keys)


def validate(model: dict) -> list[dict]:
    issues = []

    def fail(rule, entity_id, message):
        issues.append({"rule": rule, "entity_id": entity_id, "message": message})

    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    errors = sorted(Draft202012Validator(schema).iter_errors(model),
                    key=lambda e: str(list(e.absolute_path)))
    for error in errors:
        fail("schema", "/".join(map(str, error.absolute_path)) or "model", error.message)
    if errors:
        return issues

    collections = {"source_documents": model["source_documents"],
                   "drawing_pages": model["drawing_pages"],
                   "source_references": model["source_references"],
                   **model["facts"], **model["design"],
                   "open_items": model["open_items"]}
    all_ids = [model["project"]["id"]] + [r["id"] for rows in collections.values() for r in rows]
    for entity_id, count in Counter(all_ids).items():
        if count > 1:
            fail("unique-ids", entity_id, "IDs must be unique across the model.")
    if issues:
        return issues
    index = {name: {r["id"]: r for r in rows} for name, rows in collections.items()}

    def ref(row, field, collection, nullable=False):
        value = row[field]
        if nullable and value is None:
            return
        if value not in index[collection]:
            fail("reference-integrity", row["id"], f"{field} references missing {collection}: {value}")

    def refs(row, field, collection):
        for value in row[field]:
            if value not in index[collection]:
                fail("reference-integrity", row["id"], f"{field} references missing {collection}: {value}")

    for rows in collections.values():
        for row in rows:
            if "source_ref_ids" in row:
                refs(row, "source_ref_ids", "source_references")
            if "decision_id" in row:
                ref(row, "decision_id", "decisions", nullable=True)
    for row in model["drawing_pages"]:
        ref(row, "source_document_id", "source_documents")
    for row in model["source_references"]:
        ref(row, "source_document_id", "source_documents")
        ref(row, "drawing_page_id", "drawing_pages", nullable=True)
        page = index["drawing_pages"].get(row["drawing_page_id"])
        if page and page["source_document_id"] != row["source_document_id"]:
            fail("source-traceability", row["id"], "Reference document and page document disagree.")
    for row in model["facts"]["spaces"]:
        refs(row, "drawing_page_ids", "drawing_pages")
    for row in model["facts"]["control_zones"]:
        ref(row, "space_id", "spaces")
    for row in model["facts"]["fixture_instances"]:
        for field, collection in [("fixture_type_id", "fixture_types"), ("space_id", "spaces"),
                                  ("drawing_page_id", "drawing_pages")]:
            ref(row, field, collection)
        ref(row, "source_control_zone_id", "control_zones", nullable=True)
        space = index["spaces"].get(row["space_id"])
        zone = index["control_zones"].get(row["source_control_zone_id"])
        if space and row["drawing_page_id"] not in space["drawing_page_ids"]:
            fail("spatial-context", row["id"], "Fixture page is not listed for its space.")
        if zone and zone["space_id"] != row["space_id"]:
            fail("zone-boundary-preservation", row["id"], "Source zone belongs to a different space.")
    for row in model["design"]["fixture_selections"]:
        ref(row, "fixture_type_id", "fixture_types")
    for row in model["design"]["fixture_scope"]:
        ref(row, "fixture_id", "fixture_instances")
        if row["disposition"] == "excluded" and not (row["reason"] or "").strip():
            fail("fixture-assignment-completeness", row["id"], "Exclusion requires a reason.")
    for row in model["design"]["zone_assignments"]:
        ref(row, "fixture_id", "fixture_instances")
        ref(row, "control_zone_id", "control_zones")
    for row in model["design"]["lv_channels"]:
        ref(row, "control_zone_id", "control_zones")
        ref(row, "power_node_id", "power_nodes", nullable=True)
        refs(row, "fixture_ids", "fixture_instances")
    for name in ("power_nodes", "control_nodes"):
        for row in model["design"][name]:
            ref(row, "drawing_page_id", "drawing_pages", nullable=True)
            if row["drawing_anchor"] is not None and row["drawing_page_id"] is None:
                fail("spatial-context", row["id"], "An anchor requires a drawing page.")
    for row in model["design"]["decisions"]:
        refs(row, "assumption_ids", "assumptions")
    for row in model["design"]["cable_routes"]:
        ref(row, "drawing_page_id", "drawing_pages")
        refs(row, "channel_ids", "lv_channels")
    for row in model["open_items"]:
        if row["status"] == "resolved" and not (row["resolution"] or "").strip():
            fail("open-items", row["id"], "Resolved items require a resolution.")

    # Stop before dereferencing invalid links. Structural failures cannot be bypassed by export.
    if issues:
        return issues

    for name in ("fixture_instances", "power_nodes", "control_nodes", "cable_routes"):
        for row in collections[name]:
            page = index["drawing_pages"].get(row["drawing_page_id"])
            points = row["points"] if name == "cable_routes" else [row["drawing_anchor"]]
            for point in points:
                if point and page and not (0 <= point["x_pt"] <= page["width_pt"] and
                                           0 <= point["y_pt"] <= page["height_pt"]):
                    fail("spatial-context", row["id"], "Point lies outside the displayed page bounds.")

    if model["project"]["takeoff_status"] != "reconciled":
        fail("source-reconciliation", model["project"]["id"], "Source takeoff has not been reconciled.")
    if not model["facts"]["fixture_instances"]:
        fail("source-reconciliation", model["project"]["id"], "Takeoff contains no fixture instances.")
    marks = Counter(r["type_mark"] for r in model["facts"]["fixture_types"])
    for mark, count in marks.items():
        if count > 1:
            fail("fixture-schedule-consistency", mark, "Duplicate source schedule mark; normalize explicitly.")

    def grouped(name, key):
        result = defaultdict(list)
        for row in collections[name]:
            result[row[key]].append(row)
        return result

    scopes = grouped("fixture_scope", "fixture_id")
    overrides = grouped("zone_assignments", "fixture_id")
    selections = grouped("fixture_selections", "fixture_type_id")
    assignments = defaultdict(list)
    for channel in model["design"]["lv_channels"]:
        for fixture_id in channel["fixture_ids"]:
            assignments[fixture_id].append(channel["id"])
    effective_zones = {}
    included = set()
    for fixture in model["facts"]["fixture_instances"]:
        fid = fixture["id"]
        if len(scopes[fid]) != 1:
            fail("fixture-assignment-completeness", fid, "Exactly one explicit scope disposition is required.")
            continue
        if len(overrides[fid]) > 1:
            fail("zone-boundary-preservation", fid, "More than one design zone assignment.")
        if scopes[fid][0]["disposition"] == "excluded":
            if assignments[fid]:
                fail("fixture-assignment-completeness", fid, "Excluded fixture is assigned to a channel.")
            continue
        included.add(fid)
        if len(assignments[fid]) != 1:
            fail("fixture-assignment-completeness", fid, "Included fixture must be assigned exactly once.")
        selected = selections[fixture["fixture_type_id"]]
        if len(selected) != 1:
            fail("fixture-schedule-consistency", fid, "Included type requires exactly one LV selection.")
        effective_zones[fid] = (overrides[fid][0]["control_zone_id"] if overrides[fid]
                                else fixture["source_control_zone_id"])
        zone = index["control_zones"].get(effective_zones[fid])
        if not zone or zone["intent_status"] != "confirmed":
            fail("zone-boundary-preservation", fid, "Control intent is unknown or provisional.")
        if zone and zone["space_id"] != fixture["space_id"]:
            fail("zone-boundary-preservation", fid, "Design zone belongs to a different space.")

    for type_id, selected in selections.items():
        if len(selected) > 1:
            fail("fixture-schedule-consistency", type_id, "Multiple LV selections for one source type.")
        for row in selected:
            if row["lv_input_watts"] is None or row["compatibility_group"] is None or row["status"] != "confirmed":
                fail("fixture-schedule-consistency", row["id"], "LV load and compatibility must be confirmed.")

    for row in model["design"]["decisions"]:
        if row["status"] != "confirmed":
            fail("decision-confirmation", row["id"], "Decision remains provisional.")
        for assumption_id in row["assumption_ids"]:
            if index["assumptions"][assumption_id]["status"] != "confirmed":
                fail("assumptions", row["id"], f"Assumption is unverified or invalidated: {assumption_id}")
    for row in model["open_items"]:
        if row["blocking"] and row["status"] == "open":
            fail("open-items", row["id"], row["description"])

    node_channels = defaultdict(list)
    node_watts = defaultdict(Decimal)
    for channel in model["design"]["lv_channels"]:
        cid = channel["id"]
        watts = Decimal(0)
        unknown_load = False
        for fid in channel["fixture_ids"]:
            fixture = index["fixture_instances"][fid]
            if fid not in included:
                continue
            if effective_zones.get(fid) != channel["control_zone_id"]:
                fail("zone-boundary-preservation", cid, f"Fixture {fid} crosses the channel's zone boundary.")
            selected = selections[fixture["fixture_type_id"]]
            if len(selected) != 1 or selected[0]["lv_input_watts"] is None:
                unknown_load = True
                continue
            selection = selected[0]
            watts += Decimal(str(selection["lv_input_watts"]))
            if (channel["compatibility_group"] is None or
                    selection["compatibility_group"] != channel["compatibility_group"]):
                fail("electrical-compatibility", cid, f"Fixture {fid} has no matching confirmed compatibility group.")
        if unknown_load:
            fail("channel-wattage", cid, "Load cannot be calculated with unknown LV wattage.")
        if watts > Decimal(str(channel["design_limit_watts"])):
            fail("channel-wattage", cid, f"{watts} W exceeds {channel['design_limit_watts']} W design limit.")
        if channel["power_node_id"] is None:
            fail("component-capacity", cid, "Power-node assignment is required for quantified design.")
        else:
            node_channels[channel["power_node_id"]].append(cid)
            node_watts[channel["power_node_id"]] += watts
    for node_id, channel_ids in node_channels.items():
        node = index["power_nodes"][node_id]
        if node["capacity_channels"] is None or node["aggregate_design_limit_watts"] is None:
            fail("component-capacity", node_id, "Node channel count and aggregate design capacity are unknown.")
            continue
        if len(channel_ids) > node["capacity_channels"]:
            fail("component-capacity", node_id, "Assigned channels exceed device channel capacity.")
        if node_watts[node_id] > Decimal(str(node["aggregate_design_limit_watts"])):
            fail("component-capacity", node_id, "Connected load exceeds aggregate design capacity.")
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("model", type=Path)
    parser.add_argument("--json", action="store_true", help="Emit a machine-readable validation report")
    args = parser.parse_args()
    try:
        issues = validate(read_model(args.model))
    except (OSError, ValueError) as error:
        parser.exit(2, f"Cannot read model: {error}\n")
    report = {"phase1_checks_pass": not issues, "issues": issues}
    if args.json:
        print(json.dumps(report, indent=2))
    elif issues:
        for issue in issues:
            print(f"{issue['rule']} | {issue['entity_id']} | {issue['message']}")
        print(f"Phase 1 checks blocked: {len(issues)} issue(s).")
    else:
        print("Phase 1 checks passed. Engineering review is still required.")
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
