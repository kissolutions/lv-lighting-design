"""Generate review CSVs from the model; never write back design state."""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from decimal import Decimal
from pathlib import Path

from .validate_model import read_model, validate


def safe_cell(value):
    # Protect spreadsheet users when a source label begins with a formula character.
    if isinstance(value, str) and value.lstrip().startswith(("=", "+", "-", "@")):
        return "'" + value
    return value


def write_csv(path, fields, rows):
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: safe_cell(row.get(key, "")) for key in fields})


def export_review(model: dict, output_dir: Path, allow_provisional=False) -> dict:
    issues = validate(model)
    structural_rules = {"schema", "unique-ids", "reference-integrity", "source-traceability", "spatial-context"}
    if issues and (not allow_provisional or any(i["rule"] in structural_rules for i in issues)):
        raise ValueError("Model is blocked; run generators.validate_model for details. "
                         "--allow-provisional permits only structurally valid review drafts.")
    output_dir = Path(output_dir)
    if output_dir.exists() and any(output_dir.iterdir()):
        raise ValueError("Output directory must be empty; choose a new revision directory.")
    status = "PROVISIONAL - BLOCKED" if issues else "CHECKS PASSED - ENGINEERING REVIEW REQUIRED"
    facts, design = model["facts"], model["design"]
    fixtures = {r["id"]: r for r in facts["fixture_instances"]}
    types = {r["id"]: r for r in facts["fixture_types"]}
    selections = defaultdict(list)
    for row in design["fixture_selections"]:
        selections[row["fixture_type_id"]].append(row)
    scopes = defaultdict(list)
    for row in design["fixture_scope"]:
        scopes[row["fixture_id"]].append(row["disposition"])
    overrides = defaultdict(list)
    for row in design["zone_assignments"]:
        overrides[row["fixture_id"]].append(row["control_zone_id"])
    assignments = defaultdict(list)
    for channel in design["lv_channels"]:
        for fixture_id in channel["fixture_ids"]:
            assignments[fixture_id].append(channel["id"])

    def selection_for(type_id):
        rows = selections[type_id]
        return rows[0] if len(rows) == 1 else None

    def load_for(fixture_id):
        selection = selection_for(fixtures[fixture_id]["fixture_type_id"])
        return None if not selection or selection["lv_input_watts"] is None else Decimal(str(selection["lv_input_watts"]))

    common = {"model_revision": model["project"]["model_revision"], "review_status": status}
    output_dir.mkdir(parents=True, exist_ok=True)
    type_rows = []
    for type_id, fixture_type in types.items():
        occurrence_ids = [f["id"] for f in fixtures.values() if f["fixture_type_id"] == type_id]
        selected = selection_for(type_id)
        type_rows.append({**common, "fixture_type_id": type_id, "source_mark": fixture_type["type_mark"],
                          "source_description": fixture_type["description"], "source_input_watts": fixture_type["source_input_watts"],
                          "lv_description": selected["lv_description"] if selected else "UNKNOWN / CONFLICT",
                          "lv_input_watts": selected["lv_input_watts"] if selected else None,
                          "compatibility_group": selected["compatibility_group"] if selected else None,
                          "source_count": len(occurrence_ids),
                          "included_count": sum(scopes[fid] == ["included"] for fid in occurrence_ids),
                          "source_ref_ids": ";".join(fixture_type["source_ref_ids"])})
    write_csv(output_dir / "lv_fixture_schedule.csv", list(common) + ["fixture_type_id", "source_mark", "source_description",
              "source_input_watts", "lv_description", "lv_input_watts", "compatibility_group", "source_count", "included_count", "source_ref_ids"], type_rows)

    fixture_rows = []
    for fid, fixture in fixtures.items():
        effective_zone = overrides[fid][0] if len(overrides[fid]) == 1 else fixture["source_control_zone_id"]
        fixture_rows.append({**common, "fixture_id": fid, "fixture_type_id": fixture["fixture_type_id"],
            "space_id": fixture["space_id"], "source_control_zone_id": fixture["source_control_zone_id"],
            "effective_control_zone_id": ";".join(overrides[fid]) if len(overrides[fid]) > 1 else effective_zone,
            "scope": ";".join(scopes[fid]) or "UNKNOWN", "channel_ids": ";".join(assignments[fid]),
            "lv_input_watts": load_for(fid), "drawing_page_id": fixture["drawing_page_id"],
            "source_ref_ids": ";".join(fixture["source_ref_ids"])})
    write_csv(output_dir / "fixture_channel_assignments.csv", list(common) + ["fixture_id", "fixture_type_id", "space_id",
        "source_control_zone_id", "effective_control_zone_id", "scope", "channel_ids", "lv_input_watts", "drawing_page_id", "source_ref_ids"], fixture_rows)

    channel_rows = []
    for channel in design["lv_channels"]:
        loads = [load_for(fid) for fid in channel["fixture_ids"]]
        total = None if any(w is None for w in loads) else sum(loads, Decimal(0))
        limit = Decimal(str(channel["design_limit_watts"]))
        channel_rows.append({**common, "channel_id": channel["id"], "control_zone_id": channel["control_zone_id"],
            "power_node_id": channel["power_node_id"], "fixture_ids": ";".join(channel["fixture_ids"]),
            "connected_watts": total, "design_limit_watts": limit,
            "unused_watts": None if total is None else limit - total,
            "compatibility_group": channel["compatibility_group"], "decision_id": channel["decision_id"]})
    write_csv(output_dir / "channel_schedule.csv", list(common) + ["channel_id", "control_zone_id", "power_node_id",
        "fixture_ids", "connected_watts", "design_limit_watts", "unused_watts", "compatibility_group", "decision_id"], channel_rows)

    component_rows = []
    for category in ("power_nodes", "control_nodes"):
        counts = Counter(r["device_class"] for r in design[category])
        for device_class, quantity in sorted(counts.items()):
            component_rows.append({**common, "component_category": category, "device_class": device_class,
                                   "quantity": quantity, "quantity_basis": "Explicit modeled nodes"})
    component_rows.append({**common, "component_category": "assigned_channels", "device_class": "100 W nominal / <=90 W design",
                           "quantity": len(design["lv_channels"]), "quantity_basis": "Explicit modeled channels; not purchased device count"})
    write_csv(output_dir / "component_quantities.csv", list(common) + ["component_category", "device_class", "quantity", "quantity_basis"], component_rows)
    write_csv(output_dir / "open_items.csv", list(common) + ["open_item_id", "description", "blocking", "status", "resolution", "source_ref_ids"],
              [{**common, "open_item_id": r["id"], **{k: r[k] for k in ("description", "blocking", "status", "resolution")},
                "source_ref_ids": ";".join(r["source_ref_ids"])} for r in model["open_items"]])
    report = {"project_id": model["project"]["id"], **common, "phase1_checks_pass": not issues, "issues": issues,
              "limitations": ["No construction release or engineering approval implied.",
                              "No automatic PDF takeoff, channel optimization, or cable-length estimate.",
                              "Quantities count modeled nodes; product selection and source reconciliation require review."]}
    (output_dir / "validation_report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("model", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--allow-provisional", action="store_true")
    args = parser.parse_args()
    try:
        report = export_review(read_model(args.model), args.output_dir, args.allow_provisional)
    except (OSError, ValueError) as error:
        parser.exit(2, f"Cannot export review: {error}\n")
    print(f"{report['review_status']}: review written to {args.output_dir}")
    return 1 if report["issues"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
