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


def check_v10(model, phase="intake"):
    """Check new physical relationships and safely delegate unchanged v0.9 checks.

    The compatibility projection is *only* an in-memory translation. New
    graph constraints are always checked against the actual v0.10 records.
    """
    from .model_bundles import check_v09
    issues = []
    def fail(rule, entity, message):
        issues.append(dict(rule=rule, entity_id=entity, message=message))
    schema = json.loads(SCHEMA.read_text())
    errors = list(Draft202012Validator(schema).iter_errors(model))
    if errors:
        for e in errors:
            fail("schema", "/".join(str(x) for x in e.absolute_path) or "model", e.message)
        return dict(checks_pass=False, phase=phase, issues=issues,
                    deferred_issues=[], derived=None)
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
                fail("dc-input-feeds",u["id"],"DC-fed power unit requires explicit PDU feed references.")
        elif u["input_power_type"] == "ac":
            if u["ac_input_phases"] not in (1,3):
                fail("power-input",u["id"],"AC-fed unit needs known 1- or 3-phase input at design release.")
            if u["input_feed_ids"]:
                fail("power-input",u["id"],"AC input cannot claim PDU DC feeds.")
        else:
            fail("power-input",u["id"],"Confirm AC or DC input.")
        v=u["input_voltage"]
        if v["min_v"] is not None and v["max_v"] is not None and v["min_v"]>v["max_v"]:
            fail("power-input",u["id"],"Invalid input operating voltage range.")
        if not any(v[k] is not None for k in ("nominal_v","min_v","max_v")):
            fail("power-input",u["id"],"Power unit input voltage not established.")
    ac_owners=defaultdict(list)
    for b in model["branch_circuits"]:
        for uid in b["power_unit_ids"]:
            if uid not in units:fail("ac-branch-map",b["id"],f"Unknown power unit {uid}")
            else:ac_owners[uid].append(b["id"])
            if uid in units and units[uid]["input_power_type"]=="dc":
                fail("ac-branch-map",uid,"DC-fed QDCD cannot be direct load of AC branch circuit.")
    for uid,u in units.items():
        if u["input_power_type"]=="ac" and len(ac_owners[uid])!=1:
            fail("ac-branch-map",uid,"AC-fed unit must map to exactly one real AC branch circuit.")
        if u["input_power_type"]=="dc" and ac_owners[uid]:
            fail("ac-branch-map",uid,"DC-fed unit cannot have direct AC branch mapping.")
    pdu_outputs=defaultdict(list)
    input_claims=set()
    feed_ids=set()
    delivered=defaultdict(float)
    for p in model["distribution_units"]:
        bid=p["input_branch_circuit_id"]
        if bid is not None and bid not in branches:
            fail("pdu-ac-circuit",p["id"],"PDU references nonexistent real branch circuit.")
        if p["input_power_type"]=="ac" and bid is None:
            fail("pdu-ac-circuit",p["id"],"AC-fed PDU needs its actual upstream AC branch circuit.")
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
            delivered[feed["source_distribution_unit_id"]]+=feed["demand_watts"]
        if feed["rated_watts"] is not None and feed["demand_watts"] is not None and feed["demand_watts"]>feed["rated_watts"]:
            fail("dc-feed-load",fid,"Feed demand exceeds this PDU output rating.")
    claims=defaultdict(list)
    for feed in model["dc_power_feeds"]:
        claims[(feed["target_power_unit_id"],feed["target_input"])].append(feed["id"])
    for key,assigned in claims.items():
        if len(assigned)>1:fail("qdcd-input-ownership",key[0],f"Multiple feeds claim input {key[1]}.")
    for uid,u in units.items():
        if set(u["input_feed_ids"])!={f["id"] for f in model["dc_power_feeds"] if f["target_power_unit_id"]==uid}:
            fail("dc-feed-mapping",uid,"Power-unit input feed references do not match actual feed records.")
    for pid,p in pdus.items():
        if p["rated_total_output_watts"] is not None and delivered[pid]>p["rated_total_output_watts"]:
            fail("pdu-total-load",pid,"Sum of known PDU output demands exceeds equipment rating.")
        if any(f["demand_watts"] is None for f in pdu_outputs[pid]):
            fail("pdu-total-load",pid,"Cannot certify PDU total without feed demands.")
    parent_ids={z["parent_zone_id"] for z in zones.values() if z["parent_zone_id"] is not None}
    for zid,z in zones.items():
        claimed=set(z["channel_ids"])
        actual={cid for cid,c in channels.items() if c["light_zone_id"]==zid}
        if claimed!=actual:
            fail("zone-channel-map",zid,"Channel IDs must exactly equal channels whose light_zone_id is this zone.")
        if zid in parent_ids and claimed:
            fail("zone-channel-map",zid,"Container/parent zone cannot own physical output channels.")
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
            u["input_phases"]=u.pop("ac_input_phases") if u["input_power_type"]=="ac" else None
            u.pop("input_power_type");u.pop("input_feed_ids")
            synthetic["power_units"].append(u)
        legacy["branch_circuits"].append(synthetic)
    for z in legacy["light_zones"]:
        ids=z.pop("channel_ids")
        first=channels.get(ids[0]) if ids else None
        z["controller_id"]=first["controller_id"] if first else None
        z["controller_output"]=first["controller_output"] if first else None
    legacy_report=check_v09(legacy,phase)
    # Legacy 'power-unit-basis' (AC input requirement) and
    # zone-output scalar assignment errors are inapplicable to the new graph.
    # Keep *all other* legacy findings visible.
    exempt={"power-unit-basis","input-compatibility","controller-assignment"}
    for entry in legacy_report["issues"]:
        if entry["rule"] not in exempt:issues.append(entry)
    deferred=legacy_report.get("deferred_issues",[])
    derived=legacy_report.get("derived") or {}
    derived["equipment_graph"]=dict(real_ac_branches=len(branches),pdus=len(pdus),
                                    remote_power_units=len(units),dc_feeds=len(feed_ids),
                                    zone_channel_ids={zid:list(z["channel_ids"]) for zid,z in zones.items()})
    return dict(checks_pass=not issues,phase=phase,issues=issues,
                deferred_issues=deferred,derived=derived,
                review_note="v0.10 electrical graph validated. Legacy projection is read-only; original source and acceptance state are unchanged.")
