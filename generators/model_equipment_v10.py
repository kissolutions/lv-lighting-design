"""v0.10 electrical equipment graph (X1/X2/X4).

A branch circuit is an actual AC circuit, a distribution unit is a physical
PDU, a DC feed is a physical PDU output to QDCD input connection, and a
DC-fed power unit is the remote programmable LED driver. No invented AC
phases or synthetic branch circuits are persisted.
"""
from __future__ import annotations

import copy
import json
from collections import Counter, defaultdict
from decimal import Decimal
from pathlib import Path

from jsonschema import Draft202012Validator

SCHEMA = Path(__file__).resolve().parents[1] / "schemas/lighting-project-v0.10.schema.json"


def upgrade_v10(model):
    """Explicit copy migration. Do not infer PDU identity from legacy branch IDs."""
    from .model_bundles import upgrade_v09
    if model.get("schema_version") == "0.10.0":
        return copy.deepcopy(model)
    old = upgrade_v09(model)
    result = copy.deepcopy(old)
    result["schema_version"] = "0.10.0"
    result["power_units"] = []
    result["distribution_units"] = []
    result["dc_power_feeds"] = []
    for branch in result["branch_circuits"]:
        units = branch.pop("power_units")
        branch["power_unit_ids"] = [unit["id"] for unit in units]
        for unit in units:
            nominal = unit.pop("input_voltage_v")
            phases = unit.pop("input_phases")
            unit["input_power_type"] = "ac" if nominal is not None or phases is not None else None
            unit["input_voltage"] = dict(nominal_v=nominal,min_v=None,max_v=None)
            unit["ac_input_phases"] = phases
            unit["input_feed_ids"] = []
            result["power_units"].append(unit)
    channels = {c["id"]:c for u in result["power_units"] for c in u["channels"]}
    for zone in result["light_zones"]:
        zone.pop("controller_id")
        zone.pop("controller_output")
        zone["channel_ids"] = sorted(cid for cid,c in channels.items() if c["light_zone_id"]==zone["id"])
    return result



def _canonical_record_ids(model):
    """All real, referable v0.10 records, including PDUs and DC feeds.

    The legacy checker predates two physical equipment collections. Their
    identities remain first-class in the canonical model; compatibility
    projections must not force the owner to relabel an open item.
    """
    ids = []
    def walk(value):
        if isinstance(value, dict):
            if isinstance(value.get("id"), str):
                ids.append(value["id"])
            for item in value.values():
                walk(item)
        elif isinstance(value, list):
            for item in value:
                walk(item)
    walk(model)
    return ids

def check_v10(model, phase="intake"):
    """Check new physical relationships and safely delegate unchanged v0.9 checks.

    The compatibility projection is *only* an in-memory translation. New
    graph constraints are always checked against the actual v0.10 records.
    """
    from .model_bundles import check_v09
    issues, deferred = [], []
    def fail(rule, entity, message, *, design_only=False):
        finding=dict(rule=rule, entity_id=entity, message=message)
        (deferred if design_only and phase != 'design' else issues).append(finding)
    schema = json.loads(SCHEMA.read_text())
    errors = list(Draft202012Validator(schema).iter_errors(model))
    if errors:
        for e in errors:
            fail("schema", "/".join(str(x) for x in e.absolute_path) or "model", e.message)
        return dict(checks_pass=False, phase=phase, issues=issues,
                    deferred_issues=[], derived=None)
    all_record_ids = _canonical_record_ids(model)
    for identifier, count in Counter(all_record_ids).items():
        if count > 1:
            fail("unique-ids", identifier, "Multiple canonical records reuse this identifier.")
    valid_ids = set(all_record_ids)
    source_reference_ids = {ref["id"] for ref in model["source_references"]}

    def current_range_issues(owner, rated, minimum, maximum, label):
        """Check optional verified fixture operating range, not QDCD supply range."""
        values=[v for v in (rated, minimum, maximum) if v is not None]
        if values and any(Decimal(str(v)) <= 0 for v in values):
            fail("cc-rated-current-range",owner,f"{label}: specified branch current must be positive.")
        if minimum is not None and maximum is not None and Decimal(str(minimum)) > Decimal(str(maximum)):
            fail("cc-rated-current-range",owner,f"{label}: allowable minimum mA exceeds maximum mA.")
        if rated is not None and minimum is not None and Decimal(str(rated)) < Decimal(str(minimum)):
            fail("cc-rated-current-range",owner,f"{label}: rated mA below manufacturer's permitted minimum.")
        if rated is not None and maximum is not None and Decimal(str(rated)) > Decimal(str(maximum)):
            fail("cc-rated-current-range",owner,f"{label}: rated mA exceeds manufacturer's permitted maximum.")

    fixture_types={fixture["id"]:fixture for fixture in model["fixture_types"]}
    for fixture in model["fixture_types"]:
        current_range_issues(fixture["id"],
            fixture.get("lv_cc_rated_current_ma"),
            fixture.get("lv_cc_min_current_ma"),
            fixture.get("lv_cc_max_current_ma"),"LV Fixture Type")
        for rid in fixture.get("lv_cc_current_source_ref_ids",[]):
            if rid not in source_reference_ids:
                fail("cc-current-source-reference",fixture["id"],f"Unknown rated-current manufacturer source reference: {rid}")
    for light in model["light_objects"]:
        d=light["design"]
        current_range_issues(light["id"],d.get("input_current_ma"),
            d.get("input_current_min_ma"),d.get("input_current_max_ma"),"Selected Light Point")
        for rid in d.get("input_current_source_ref_ids",[]):
            if rid not in source_reference_ids:
                fail("cc-current-source-reference",light["id"],f"Unknown selected current-rating source reference: {rid}")
        f=fixture_types.get(light["source"]["fixture_type_id"])
        if (f and d["input_power_mode"]=="constant_current" and
            f.get("lv_cc_rated_current_ma") is not None and d["input_current_ma"] is not None
            and Decimal(str(f["lv_cc_rated_current_ma"])) != Decimal(str(d["input_current_ma"]))):
            fail("cc-selected-current-vs-fixture-type",light["id"],
                 "Selected Light Point CC rated mA conflicts with the verified LV fixture-type rated mA.")
    for item in model["open_items"]:
        for identifier in item["affects_ids"]:
            if identifier not in valid_ids:
                fail("reference-integrity", item["id"],
                     f"Missing v0.10 affected object: {identifier}")
    units = {}
    channels = {}
    controllers = {c["id"]:c for c in model["controllers"]}
    branches = {b["id"]:b for b in model["branch_circuits"]}
    pdus = {p["id"]:p for p in model["distribution_units"]}
    zones = {z["id"]:z for z in model["light_zones"]}
    ids = [obj["id"] for group in ("power_units","distribution_units","dc_power_feeds")
           for obj in model[group]]
    ids += [b["id"] for b in model["branch_circuits"]]
    ids += [z["id"] for z in model["light_zones"]]
    ids += [c["id"] for c in model["controllers"]]
    if len(ids) != len(set(ids)):
        fail("electrical-ids", model["project"]["id"], "Duplicated electrical equipment, feed or zone ID.")
    for u in model["power_units"]:
        if u["id"] in units:
            fail("electrical-ids",u["id"],"Duplicate power unit ID.")
        units[u["id"]]=u
        for c in u["channels"]:
            if c["id"] in channels:
                fail("electrical-ids",c["id"],"Duplicate microchannel ID.")
            channels[c["id"]]=c
        if u["number_of_channels"] is not None and len(u["channels"]) > u["number_of_channels"]:
            fail("power-unit-capacity",u["id"],"More physical outputs than rated.")
        if u["input_power_type"] == "dc":
            if u["ac_input_phases"] is not None:
                fail("power-input",u["id"],"DC input has no AC phases.")
            if not u["input_feed_ids"]:
                fail("dc-input-feeds",u["id"],"DC-fed power unit requires explicit PDU feed references.",design_only=True)
        elif u["input_power_type"] == "ac":
            if u["ac_input_phases"] not in (1,3):
                fail("power-input",u["id"],"AC-fed unit needs known 1- or 3-phase input at design release.",design_only=True)
            if u["input_feed_ids"]:
                fail("power-input",u["id"],"AC input cannot claim PDU DC feeds.")
        else:
            fail("power-input",u["id"],"Confirm AC or DC input.",design_only=True)
        v=u["input_voltage"]
        if v["min_v"] is not None and v["max_v"] is not None and v["min_v"]>v["max_v"]:
            fail("power-input",u["id"],"Invalid input operating voltage range.")
        if not any(v[k] is not None for k in ("nominal_v","min_v","max_v")):
            fail("power-input",u["id"],"Power unit input voltage not established.",design_only=True)
    # Equipment/controller and output ownership remain separate from functional
    # zones: each programmable driver's outputs are physical channel objects.
    qdcd_units=set()
    for c in controllers.values():
        uid=c["integrated_power_unit_id"]
        if uid is not None and uid not in units:
            fail("controller-power-unit",c["id"],"Controller references an unknown integrated power unit.")
        if c["device_class"] and "QDCD" in c["device_class"].upper():
            if uid is None or uid not in units:
                fail("qdcd-power-unit",c["id"],"QDCD must reference its physical programmable-driver power unit.")
                continue
            qdcd_units.add(uid)
            u=units[uid]
            if len(u["channels"])>4 or u["number_of_channels"] not in (4,None):
                fail("qdcd-channel-capacity",c["id"],"QDCD contains four physical driver outputs; model capacity cannot exceed four.")
            if len(u["input_feed_ids"])>4:
                fail("qdcd-input-capacity",c["id"],"QDCD has at most four distinct DC input feed ports.")
            for channel in u["channels"]:
                if channel["controller_id"] not in (None,c["id"]):
                    fail("qdcd-channel-map",channel["id"],"QDCD-owned output is mapped to another controller.")
    for uid,u in units.items():
        for channel in u["channels"]:
            controller=controllers.get(channel["controller_id"])
            if controller is not None and controller["integrated_power_unit_id"] not in (None,uid):
                fail("controller-power-unit",channel["id"],"Controller's integrated driver does not own this channel.")
    ac_owners=defaultdict(list)
    for b in model["branch_circuits"]:
        for uid in b["power_unit_ids"]:
            if uid not in units:fail("ac-branch-map",b["id"],f"Unknown power unit {uid}")
            else:ac_owners[uid].append(b["id"])
            if uid in units and units[uid]["input_power_type"]=="dc":
                fail("ac-branch-map",uid,"DC-fed QDCD cannot be direct load of AC branch circuit.")
    for uid,u in units.items():
        if u["input_power_type"]=="ac" and len(ac_owners[uid])!=1:
            fail("ac-branch-map",uid,"AC-fed unit must map to exactly one real AC branch circuit.",design_only=len(ac_owners[uid])==0)
        if u["input_power_type"]=="ac" and len(ac_owners[uid])==1:
            b=branches[ac_owners[uid][0]]
            if b["voltage_v"] is not None and u["input_voltage"]["nominal_v"] is not None and b["voltage_v"]!=u["input_voltage"]["nominal_v"]:
                fail("input-compatibility",uid,"Actual AC circuit voltage and converter AC input nominal disagree.")
            if b["phases"] is not None and u["ac_input_phases"] is not None and b["phases"]!=u["ac_input_phases"]:
                fail("input-compatibility",uid,"Actual AC circuit phases and converter AC input phases disagree.")
        if u["input_power_type"]=="dc" and ac_owners[uid]:
            fail("ac-branch-map",uid,"DC-fed unit cannot have direct AC branch mapping.")
    pdu_outputs=defaultdict(list)
    input_claims=set()
    feed_ids=set()
    delivered=defaultdict(Decimal)
    for p in model["distribution_units"]:
        bid=p["input_branch_circuit_id"]
        if bid is not None and bid not in branches:
            fail("pdu-ac-circuit",p["id"],"PDU references nonexistent real branch circuit.")
        if p["input_power_type"]=="ac" and bid is None:
            fail("pdu-ac-circuit",p["id"],"AC-fed PDU needs its actual upstream AC branch circuit.",design_only=True)
        if p["input_power_type"]=="dc" and bid is not None:
            fail("pdu-ac-circuit",p["id"],"DC-fed PDU cannot attach directly to an AC branch.")
    for feed in model["dc_power_feeds"]:
        fid=feed["id"];feed_ids.add(fid)
        p=pdus.get(feed["source_distribution_unit_id"])
        u=units.get(feed["target_power_unit_id"])
        if p is None:
            fail("dc-feed-source",fid,"Unknown PDU.")
        elif feed["source_output"]>p["output_count"]:
            fail("pdu-output-capacity",fid,"PDU physical output number out of range.")
        if u is None:
            fail("dc-feed-target",fid,"Unknown destination power unit.")
        elif u["input_power_type"]!="dc":
            fail("dc-feed-target",fid,"Destination must have DC input.")
        elif fid not in u["input_feed_ids"]:
            fail("dc-feed-mapping",fid,"Feed must be listed on destination input_feed_ids.")
        pin=(feed["source_distribution_unit_id"],feed["source_output"])
        if pin in input_claims:
            fail("pdu-output-ownership",fid,"One PDU output cannot be claimed by two distinct feeds.")
        input_claims.add(pin)
        if u is not None:
            if feed["target_input"]>4 and any(
                c["device_class"] and "QDCD" in c["device_class"].upper()
                and c["integrated_power_unit_id"]==u["id"] for c in controllers.values()
            ):
                fail("qdcd-input-capacity",fid,"QDCD supports only four input positions.")
        pdu_outputs[feed["source_distribution_unit_id"]].append(feed)
        if feed["demand_watts"] is not None:
            delivered[feed["source_distribution_unit_id"]]+=Decimal(str(feed["demand_watts"]))
        if feed["rated_watts"] is not None and feed["demand_watts"] is not None and Decimal(str(feed["demand_watts"]))>Decimal(str(feed["rated_watts"])):
            fail("dc-feed-load",fid,"Feed demand exceeds this PDU output rating.")
    claims=defaultdict(list)
    for feed in model["dc_power_feeds"]:
        claims[(feed["target_power_unit_id"],feed["target_input"])].append(feed["id"])
    for key,assigned in claims.items():
        if len(assigned)>1:fail("qdcd-input-ownership",key[0],f"Multiple feeds claim input {key[1]}.")
    for uid,u in units.items():
        if set(u["input_feed_ids"])!={f["id"] for f in model["dc_power_feeds"] if f["target_power_unit_id"]==uid}:
            fail("dc-feed-mapping",uid,"Power-unit input feed references do not match actual feed records.")
    for uid,u in units.items():
        if u["input_power_type"]!="dc":
            continue
        inbound=[f for f in model["dc_power_feeds"] if f["target_power_unit_id"]==uid]
        if len(inbound)>4 and uid in qdcd_units:
            fail("qdcd-input-capacity",uid,"QDCD exceeds four distinct DC input feeds.")
        confirmed=[f["demand_watts"] for f in inbound]
        if any(x is None for x in confirmed):
            fail("dc-feed-load",uid,"Input demand cannot be fully checked with unknown feed demands.",design_only=True)
        else:
            total=sum((Decimal(str(value)) for value in confirmed), Decimal(0))
            if u["design_input_watts"] is not None and total<Decimal(str(u["design_input_watts"])):
                fail("dc-feed-load",uid,"Summed DC feed demand is below recorded power-unit design input load.")
        known_rated=[f["rated_watts"] for f in inbound]
        if any(x is None for x in known_rated):
            fail("dc-feed-rating",uid,"Confirm each upstream Class 2 feed rating.",design_only=True)
        elif u["design_input_watts"] is not None and sum((Decimal(str(v)) for v in known_rated), Decimal(0))<Decimal(str(u["design_input_watts"])):
            fail("dc-feed-rating",uid,"Summed available DC feed ratings cannot support power-unit design input.")
    for pid,p in pdus.items():
        if p["rated_total_output_watts"] is not None and delivered[pid]>Decimal(str(p["rated_total_output_watts"])):
            fail("pdu-total-load",pid,"Sum of known PDU output demands exceeds equipment rating.")
        if any(f["demand_watts"] is None for f in pdu_outputs[pid]):
            fail("pdu-total-load",pid,"Cannot certify PDU total without feed demands.",design_only=True)
    parent_ids={z["parent_zone_id"] for z in zones.values() if z["parent_zone_id"] is not None}
    for zid,z in zones.items():
        claimed=set(z["channel_ids"])
        actual={cid for cid,c in channels.items() if c["light_zone_id"]==zid}
        if claimed!=actual:
            fail("zone-channel-map",zid,"Channel IDs must exactly equal channels whose light_zone_id is this zone.")
        if zid in parent_ids and claimed:
            fail("zone-channel-map",zid,"Container/parent zone cannot own physical output channels.")
        if phase=="design" and zid not in parent_ids and z["light_object_ids"] and not claimed:
            fail("zone-channel-map",zid,"A populated designed endpoint zone requires at least one assigned microchannel.")
        for cid in claimed:
            c=channels.get(cid)
            if c is None:fail("zone-channel-map",zid,f"Unknown channel {cid}")
            elif c["controller_id"] is not None:
                controller=controllers.get(c["controller_id"])
                if controller is None:
                    fail("channel-controller",cid,"Unknown output controller.")
                elif c["controller_output"] is None or (controller["number_of_control_outputs"] is not None
                      and c["controller_output"]>controller["number_of_control_outputs"]):
                    fail("channel-controller",cid,"Output number missing or exceeds controller capacity.")
        for lid in z["light_object_ids"]:
            light=next((x for x in model["light_objects"] if x["id"]==lid),None)
            if light and light["design"]["channel_id"] is not None and light["design"]["channel_id"] not in claimed:
                fail("zone-channel-map",lid,"Light's selected channel is not mapped to its endpoint zone.")
    physical_outputs=defaultdict(list)
    for cid,c in channels.items():
        if (c["controller_id"] is None)!=(c["controller_output"] is None):
            fail("channel-controller",cid,"Controller ID and output must be populated together.")
        if c["controller_id"] is not None:
            physical_outputs[(c["controller_id"],c["controller_output"])].append(cid)
    for out,cids in physical_outputs.items():
        if len(cids)>1:fail("channel-controller",out[0],"Physical output shared by multiple channels.")

    # v0.9 adapter preserves established checks without writing fictitious
    # branch-circuit or AC-input records into canonical v0.10 project data.
    legacy = copy.deepcopy(model)
    legacy["schema_version"]="0.9.0"
    # Optional v0.10 fixture-current provenance/range attributes do not exist
    # in strict v0.9. These are checked natively above and then stripped ONLY
    # from the in-memory backward-validation projection; keep the real model
    # intact so unrelated current, emergency and CC findings remain visible.
    for fixture in legacy["fixture_types"]:
        for key in ("lv_cc_rated_current_ma","lv_cc_min_current_ma",
                    "lv_cc_max_current_ma","lv_cc_current_source_ref_ids"):
            fixture.pop(key,None)
    for light in legacy["light_objects"]:
        for key in ("input_current_min_ma","input_current_max_ma",
                    "input_current_source_ref_ids"):
            light["design"].pop(key,None)
    legacy.pop("distribution_units");legacy.pop("dc_power_feeds")
    raw_units=legacy.pop("power_units")
    by_id={u["id"]:u for u in raw_units}
    attached=set()
    for b in legacy["branch_circuits"]:
        owners=b.pop("power_unit_ids")
        b["power_units"]=[]
        for uid in owners:
            if uid not in by_id:continue
            attached.add(uid)
            unit=copy.deepcopy(by_id[uid])
            unit["input_voltage_v"]=unit.pop("input_voltage")["nominal_v"]
            unit["input_phases"]=unit.pop("ac_input_phases")
            unit.pop("input_power_type");unit.pop("input_feed_ids")
            b["power_units"].append(unit)
    # v0.9 does not model intermediate DC distribution. A validation-only
    # synthetic container lets old light/channel checks run; its AC fields
    # are explicitly null rather than inventing phase or voltage.
    orphan=[u for u in raw_units if u["id"] not in attached]
    if orphan:
        base=legacy["branch_circuits"][0] if legacy["branch_circuits"] else None
        synthetic=dict(id="X10-COMPATIBILITY-ONLY",panel_ref=None,
                       circuit_label="INTERNAL PROJECTION ONLY",voltage_v=None,
                       phases=None,breaker_amps=None,backup_supply_id=None,
                       source_ref_ids=base["source_ref_ids"] if base else model["project"]["energy_code_basis"]["source_ref_ids"],
                       decision_id=None,power_units=[])
        for unit in orphan:
            u=copy.deepcopy(unit)
            u["input_voltage_v"]=u.pop("input_voltage")["nominal_v"]
            recorded_phases=u.pop("ac_input_phases")
            u["input_phases"]=recorded_phases if u["input_power_type"]=="ac" else None
            u.pop("input_power_type");u.pop("input_feed_ids")
            synthetic["power_units"].append(u)
        legacy["branch_circuits"].append(synthetic)
    for z in legacy["light_zones"]:
        ids=z.pop("channel_ids")
        first=channels.get(ids[0]) if ids else None
        z["controller_id"]=first["controller_id"] if first else None
        z["controller_output"]=first["controller_output"] if first else None

    # A v0.9 schema cannot express distribution_units or dc_power_feeds.
    # Independently validate the original v0.10 open-item targets above,
    # then adapt only the in-memory reference list for legacy checks.
    # The true affects_ids are never modified or replaced in the model.
    new_equipment_ids = {item["id"] for key in ("distribution_units", "dc_power_feeds")
                         for item in model[key]}
    for item in legacy["open_items"]:
        retained = [identifier for identifier in item["affects_ids"]
                    if identifier not in new_equipment_ids]
        if len(retained) != len(item["affects_ids"]):
            # v0.9 requires a nonempty affects_ids list; this placeholder
            # identifies the review container, not a fabricated PDU/feeder.
            item["affects_ids"] = retained or [model["project"]["id"]]
    legacy_report=check_v09(legacy,phase)
    legacy_incomplete = legacy_report.get("derived") is None
    if legacy_incomplete:
        fail("legacy-projection-incomplete",model["project"]["id"],
             "The v0.9 compatibility checker stopped before downstream electrical "
             "checks; its reduced finding count is incomplete and cannot be "
             "treated as a passing design review.")
    # Y4 supersedes only the two legacy CC warnings; keep all other validation.
    # The manufacturer authorizes parallel topology subject to specific fixture
    # qualification, which is assessed independently against canonical equipment.
    from .qdcd_y4 import validate_y4
    y4_report = validate_y4(model)
    # Legacy 'power-unit-basis' (AC input requirement) and
    # zone-output scalar assignment errors are inapplicable to the new graph.
    # Keep *all other* legacy findings visible.
    dc_unit_ids={uid for uid,u in units.items() if u["input_power_type"]=="dc"}

    # Legacy compatibility findings for QDCD CC channels/fixtures only.
    # Unrelated legacy fixture current mismatches must not be suppressed.
    qdcd_cc_ids = {channel["id"] for unit in units.values() if unit["id"] in qdcd_units
                   for channel in unit["channels"] if channel["output_power_mode"] == "constant_current"}
    y4_legacy_cc_entities = set(qdcd_cc_ids)
    y4_legacy_cc_entities.update(light["id"] for light in model["light_objects"]
                                 if light["design"]["channel_id"] in qdcd_cc_ids)

    def applicable_legacy_findings(findings):
        """Filter the same obsolete v0.9 rules from issues AND deferred issues.

        Return fresh records; never mutate the legacy report or original model.
        Keep valid DC input power-basis findings with neutral DC wording.
        """
        applicable=[]
        for finding in findings:
            entry=finding
            rule=entry["rule"];owner=entry["entity_id"];message=entry["message"]
            if rule=="decision-basis" and owner=="X10-COMPATIBILITY-ONLY" and orphan:
                # Only the synthetic, unsaved v0.9 projection container lacks
                # an owner decision. Never exempt real branches or equipment.
                continue
            if rule in ("cc-topology-review", "current-compatibility") and owner in y4_legacy_cc_entities:
                continue
            if rule=="controller-assignment":
                # v0.10 zone.channel_ids replaces the legacy scalar assignment.
                continue
            if rule=="power-unit-basis" and owner in dc_unit_ids:
                if "input_phases" in message or "input_voltage_v" in message:
                    continue
                if "AC input watts" in message:
                    entry={**entry,"message":message.replace("AC input watts","DC input watts")}
            if rule=="input-compatibility" and owner in dc_unit_ids:
                continue
            applicable.append(entry)
        return applicable

    issues.extend(applicable_legacy_findings(legacy_report["issues"]))
    deferred.extend(applicable_legacy_findings(legacy_report.get("deferred_issues",[])))
    (issues if phase == "design" else deferred).extend(y4_report["findings"])
    derived=legacy_report.get("derived")
    if derived is not None:
        derived["equipment_graph"]=dict(real_ac_branches=len(branches),pdus=len(pdus),
                                        remote_power_units=len(units),dc_feeds=len(feed_ids),
                                        zone_channel_ids={zid:list(z["channel_ids"]) for zid,z in zones.items()})
    return dict(checks_pass=not issues,phase=phase,issues=issues,
                y4_validation_summary=y4_report["summary"],
                deferred_issues=deferred,derived=derived,
                legacy_projection_status="halted" if legacy_incomplete else "complete",
                review_note=("Legacy downstream validation halted: the displayed issue count is incomplete."
                             if legacy_incomplete else
                             "v0.10 electrical graph validated; legacy projection is read-only."))


def main():
    """Explicit, non-overwriting version upgrade or read-only validation."""
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input",type=Path)
    parser.add_argument("--upgrade-output",type=Path,
                        help="Write a new v0.10 JSON copy; never overwrite existing records.")
    parser.add_argument("--phase",choices=("inventory","intake","design"),default="intake")
    args=parser.parse_args()
    from .validate_model import read_model
    from .model_intake import model_json
    source=read_model(args.input)
    if args.upgrade_output is None:
        if source.get("schema_version")!="0.10.0":
            parser.error("Input is not v0.10; use --upgrade-output for an explicit migration copy.")
        result=check_v10(source,args.phase)
        print(json.dumps(result,indent=2,default=str))
        return 0 if result["checks_pass"] else 1
    if args.upgrade_output.exists():
        parser.error("Refusing to overwrite an existing review/model file.")
    result=upgrade_v10(source)
    Draft202012Validator(json.loads(SCHEMA.read_text())).validate(result)
    args.upgrade_output.parent.mkdir(parents=True,exist_ok=True)
    args.upgrade_output.write_text(model_json(result)+"\n")
    print(json.dumps({"written":str(args.upgrade_output),"schema_version":"0.10.0",
                      "warning":"Legacy PDU-as-branch and DC-fed QDCD records require explicit reviewed electrical remapping; no inferred feeds."}))
    return 0


if __name__=="__main__":
    raise SystemExit(main())
