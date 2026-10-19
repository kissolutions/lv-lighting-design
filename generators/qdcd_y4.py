"""Y4 SmartDC QDCD parallel-CC engineering qualification (read only).

The Rev A2 manufacturer example proves a supported topology, not individual
Timmons fixture-combination qualification. This module never changes a model.
"""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from decimal import Decimal, InvalidOperation
from pathlib import Path

from jsonschema import Draft202012Validator

from .model_access import iter_power_units
from .model_hierarchy import load_watts
from .validate_model import read_model

SCHEMA = Path(__file__).resolve().parents[1] / "schemas/qdcd-parallel-qualification-v0.1.schema.json"
DEFAULTS = dict(min_ma=Decimal("1000"), max_ma=Decimal("4000"),
                min_v=Decimal("12"), max_v=Decimal("55"),
                rated_channel_w=Decimal("100"), design_channel_w=Decimal("95"),
                rated_unit_w=Decimal("400"))


def number(value):
    if value is None or isinstance(value, bool):
        return None
    try:
        n = Decimal(str(value))
        return n if n.is_finite() else None
    except (InvalidOperation, TypeError, ValueError):
        return None


def validate_y4(model, qualification=None):
    """Validate physical QDCD channels and separately recorded evidence.

    Missing qualification never implies that the manufacturer's general
    application drawing certifies a particular fixture combination.
    Findings are distinct from accepted design data. Electrical violations
    are channel-specific; repeated evidence gaps are grouped by fixture cohort.
    """
    if model.get("schema_version") != "0.10.0":
        raise ValueError("Y4 native validation requires a v0.10 canonical model")
    if qualification is None:
        qualification = {"schema_version": "1.0.0", "fixture_evidence": [],
                         "combination_qualifications": [], "driver_programming": None}
    errors = sorted(Draft202012Validator(json.loads(SCHEMA.read_text())).iter_errors(qualification),
                    key=lambda e: str(e.absolute_path))
    if errors:
        raise ValueError("Invalid Y4 companion: " + "; ".join(e.message for e in errors[:5]))
    findings = []
    def emit(rule, entity, message, **extra):
        findings.append(dict(rule=rule, entity_id=entity, message=message, **extra))

    fixture_types = {x["id"]: x for x in model["fixture_types"]}
    lights = {x["id"]: x for x in model["light_objects"]}
    members = defaultdict(list)
    for light in model["light_objects"]:
        cid = light["design"]["channel_id"]
        if cid is not None:
            members[cid].append(light)
    controllers = {c["integrated_power_unit_id"]: c for c in model["controllers"]
                   if c["integrated_power_unit_id"] is not None
                   and c["device_class"] and "QDCD" in c["device_class"].upper()}
    source_refs = {r["id"] for r in model["source_references"]}
    decisions = {d["id"] for d in model["decisions"]}
    evidenced = {}
    for item in qualification["fixture_evidence"]:
        fid = item["fixture_type_id"]
        if fid in evidenced:
            raise ValueError("Duplicate fixture evidence for " + fid)
        if fid not in fixture_types:
            raise ValueError("Unknown fixture type in Y4 evidence: " + fid)
        if any(ref not in source_refs for ref in item["source_ref_ids"]):
            raise ValueError("Unknown source reference in Y4 fixture evidence: " + fid)
        evidenced[fid] = item
    combinations = {}
    for item in qualification["combination_qualifications"]:
        key = tuple(sorted(item["fixture_type_ids"]))
        if key in combinations:
            raise ValueError("Duplicate fixture combination qualification: " + str(key))
        if any(fid not in fixture_types for fid in key):
            raise ValueError("Unknown fixture type in Y4 combination: " + str(key))
        if any(ref not in source_refs for ref in item["manufacturer_evidence_ref_ids"]):
            raise ValueError("Unknown source reference in Y4 combination: " + str(key))
        if item["owner_decision_id"] is not None and item["owner_decision_id"] not in decisions:
            raise ValueError("Unknown owner decision in Y4 combination: " + str(key))
        combinations[key] = item
    programming = qualification["driver_programming"]
    if programming is not None:
        if any(ref not in source_refs for ref in programming["manufacturer_evidence_ref_ids"]):
            raise ValueError("Unknown QDCD programming manufacturer source reference")
    gaps = defaultdict(list)
    ratings_without_proof = defaultdict(list)
    unit_details = []
    qdcd_channels = 0

    for unit in iter_power_units(model):
        if unit["id"] not in controllers:
            continue
        known_unit_w = Decimal("0")
        unit_unknown_w = False
        cc_in_unit = False
        for channel in unit["channels"]:
            cid = channel["id"]
            attached = members[cid]
            powers = []
            for light in attached:
                try:
                    w = number(load_watts(light["design"]["load"]))
                except (ValueError, KeyError, TypeError):
                    w = None
                powers.append(w)
            if any(w is None for w in powers):
                unit_unknown_w = True
                if attached:
                    emit("qdcd-channel-power-unknown", cid,
                         "Connected load cannot be established from the selected fixture load basis.")
            watts = sum((w for w in powers if w is not None), Decimal("0"))
            aux = number(channel.get("auxiliary_load_watts"))
            if aux is not None:
                watts += aux
            if attached:
                known_unit_w += watts
                if watts > DEFAULTS["design_channel_w"]:
                    emit("qdcd-design-power-exceeded", cid, f"Channel load {watts} W exceeds KIS 95 W design maximum.")
                if watts > DEFAULTS["rated_channel_w"]:
                    emit("qdcd-rated-power-exceeded", cid, f"Channel load {watts} W exceeds QDCD 100 W output rating.")
            if channel["output_power_mode"] != "constant_current" or not attached:
                continue
            cc_in_unit = True
            qdcd_channels += 1
            branch_ma = [number(l["design"].get("input_current_ma")) if l["design"].get("input_power_mode") == "constant_current" else None for l in attached]
            if any(i is None for i in branch_ma):
                emit("cc-parallel-rated-current-missing", cid,
                     "Every connected CC branch requires a known rated mA; CV/mixed-mode members are not valid CC branches.")
            elif len(attached) > 1 and len(set(branch_ma)) != 1:
                emit("cc-parallel-rated-current-mismatch", cid,
                     "Parallel QDCD luminaires must have identical verified rated mA; nominal voltage is not a substitute.")
            expected = sum(branch_ma) if all(i is not None for i in branch_ma) else None
            selected = number(channel.get("output_current_ma"))
            if expected is not None and expected < DEFAULTS["min_ma"]:
                emit("cc-branch-sum-below-driver-min", cid,
                     f"Required branch sum {expected} mA is below standard QDCD 1000 mA output minimum.")
            if expected is not None and expected > DEFAULTS["max_ma"]:
                emit("cc-branch-sum-above-driver-max", cid,
                     f"Required branch sum {expected} mA exceeds QDCD 4000 mA limit.")
            if selected is None:
                emit("cc-output-setpoint-missing", cid, "QDCD CC programmed total output current must be recorded.")
            else:
                if selected < DEFAULTS["min_ma"]:
                    emit("cc-output-below-driver-min", cid, f"Selected {selected} mA is below standard QDCD 1000 mA minimum.")
                if selected > DEFAULTS["max_ma"]:
                    emit("cc-output-above-driver-max", cid, f"Selected {selected} mA exceeds QDCD 4000 mA maximum.")
                if expected is not None and selected != expected:
                    emit("cc-output-sum-mismatch", cid,
                         f"Programmed {selected} mA does not equal parallel branch sum {expected} mA.")
                if programming is not None:
                    step = number(programming["current_step_ma"])
                    origin = number(programming["current_step_origin_ma"])
                    if step is not None and origin is not None and (selected - origin) % step != 0:
                        emit("cc-output-step-incompatible", cid,
                             f"QDCD {selected} mA setting is not on verified {step} mA step grid from {origin} mA.")
            volt = channel["voltage"]
            dmin, dmax = number(volt.get("min_v")), number(volt.get("max_v"))
            if dmin is None or dmax is None:
                emit("cc-channel-voltage-unverified", cid, "Selected QDCD channel voltage compliance range is unknown.")
            elif dmin < DEFAULTS["min_v"] or dmax > DEFAULTS["max_v"]:
                emit("cc-channel-voltage-limit", cid, "Configured output voltage range exceeds QDCD 12–55 V specification.")
            ranges = []
            for light in attached:
                fid = light["source"]["fixture_type_id"]
                record = evidenced.get(fid)
                rated = number(light["design"].get("input_current_ma"))
                if (record is None or record["basis"] != "manufacturer_verified"
                    or rated != number(record["rated_current_ma"])):
                    ratings_without_proof[fid].append(cid)
                v = light["design"]["input_voltage"]
                low, high = number(v.get("min_v")), number(v.get("max_v"))
                if low is None or high is None:
                    emit("cc-fixture-voltage-unverified", light["id"],
                         "Selected LED-module operating/forward-voltage range requires verification.")
                else:
                    ranges.append((low, high))
                    if low < DEFAULTS["min_v"] or high > DEFAULTS["max_v"] or (dmin is not None and low < dmin) or (dmax is not None and high > dmax):
                        emit("cc-fixture-voltage-incompatible", light["id"],
                             "Fixture verified operating voltage is not wholly within QDCD channel compliance.")
            if len(ranges) == len(attached) and ranges and max(x[0] for x in ranges) > min(x[1] for x in ranges):
                emit("cc-parallel-voltage-no-overlap", cid,
                     "Parallel fixtures do not have a common operating voltage interval.")
            if len(attached) > 1:
                key = tuple(sorted({l["source"]["fixture_type_id"] for l in attached}))
                combo = combinations.get(key)
                emergency = any(fixture_types[l["source"]["fixture_type_id"]].get("source_emergency_provision")
                                for l in attached)
                if (combo is None or combo["manufacturer_status"] != "fixture_combination_verified"
                    or not combo["manufacturer_evidence_ref_ids"]
                    or combo["project_review_status"] != "qualified"):
                    gaps[("combination", key)].append(cid)
                if emergency and (combo is None or combo["emergency_status"] != "qualified"):
                    gaps[("emergency", key)].append(cid)
        if cc_in_unit:
            if known_unit_w > DEFAULTS["rated_unit_w"]:
                emit("qdcd-unit-power-exceeded", unit["id"],
                     f"QDCD modeled connected load {known_unit_w} W exceeds 400 W maximum.")
            if unit_unknown_w:
                emit("qdcd-unit-power-unverified", unit["id"],
                     "Unknown channel load prevents complete 400 W aggregate qualification.")
            if programming is None or not programming["manufacturer_evidence_ref_ids"]:
                emit("cc-programming-step-unverified", unit["id"],
                     "Manufacturer-confirmed exact current step and origin have not been recorded; approximate 100 mA is not certification.")
            unit_details.append(dict(unit_id=unit["id"], known_watts=str(known_unit_w),
                                     complete=not unit_unknown_w))

    for fid, cids in sorted(ratings_without_proof.items()):
        emit("cc-fixture-rated-ma-unverified", fid,
             "Fixture rated branch current lacks matching manufacturer-verified evidence in the Y4 qualification register.",
             channel_ids=sorted(set(cids)))
    for (kind, key), cids in sorted(gaps.items()):
        rule = "cc-combination-qualification-pending" if kind == "combination" else "cc-emergency-qualification-pending"
        emit(rule, "|".join(key),
             ("Parallel topology is generally supported, but this particular fixture-type combination "
              "has not been manufacturer-qualified and project-reviewed." if kind == "combination"
              else "Emergency variant/transfer behavior on this shared output has not been qualified."),
             fixture_type_ids=list(key), channel_ids=sorted(set(cids)))
    return dict(schema_version="1.0.0", findings=findings,
                summary=dict(qdcd_cc_channels=qdcd_channels, qdcd_units=unit_details,
                             findings=len(findings), rule_counts={
                                 rule: sum(f["rule"] == rule for f in findings)
                                 for rule in sorted({f["rule"] for f in findings})}))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("model", type=Path)
    ap.add_argument("--qualification", type=Path)
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()
    model = read_model(args.model)
    contract = json.loads(args.qualification.read_text(), parse_float=Decimal) if args.qualification else None
    report = validate_y4(model, contract)
    payload = json.dumps(report, indent=2, default=str)
    if args.output:
        if args.output.exists():
            ap.error("Refusing to overwrite existing validation output")
        args.output.write_text(payload + "\n")
    else:
        print(payload)
    return 1 if report["findings"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
