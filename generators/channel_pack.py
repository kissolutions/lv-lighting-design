"""PROC-M4-CHANNEL-PACK v0.1 — read-only, evidence-gated micro-channel optimizer.

Electrical connection topology is always PARALLEL; downstream cable may be
daisy-chained without putting luminaires electrically in series. Groups cannot
span endpoint zones. A CC driver's total current is the sum of branch currents,
but Kirchhoff's laws do NOT prove stable sharing between bare parallel LEDs:
a documented manufacturer's supported configuration is mandatory.
"""
from __future__ import annotations

import argparse
import json
import math
from collections import defaultdict
from decimal import Decimal
from pathlib import Path

TARGET_W = Decimal("90")
MAX_W = Decimal("95")


def decimal(value, label):
    if isinstance(value, bool) or value is None:
        raise ValueError(f"{label} must be a known number")
    result = Decimal(str(value))
    if not result.is_finite():
        raise ValueError(f"{label} must be finite")
    return result


def light_watts(light):
    load = light["design"]["load"]
    if load["basis"] == "per_fixture":
        w = load["watts"]
    elif load["basis"] == "per_linear_foot":
        if load.get("watts") is None or load.get("length_ft") is None:
            raise ValueError("Linear light lacks watts/ft or confirmed length")
        w = decimal(load["watts"], "watts/ft") * decimal(load["length_ft"], "length_ft")
    else:
        raise ValueError("Unknown load basis")
    w = decimal(w, "light watts")
    if w <= 0:
        raise ValueError("Light watts must be positive")
    return w


def _exact_bins(items, ceiling, target, max_states=125000):
    """Minimize bin count (not first-feasible fill); minimize target deviation
    among equal-count candidates. Exact for small cases unless search budget
    is exhausted, in which case report heuristic rather than claim optimality.
    """
    ordered = sorted(items, key=lambda x: (-x["watts"], x["id"]))
    best = None
    best_score = None
    states = 0
    exhausted = False

    def score(bins):
        # Prefer near 90 W utilization, after minimizing the number of channels.
        totals = [sum((l["watts"] for l in b), Decimal(0)) for b in bins]
        return (len(bins), sum((abs(t - target) for t in totals), Decimal(0)),
                tuple(sorted(tuple(sorted(l["id"] for l in b)) for b in bins)))

    def consider(bins):
        nonlocal best, best_score
        key = score(bins)
        if best_score is None or key < best_score:
            best_score = key
            best = [list(b) for b in bins]

    bins = []
    def place(i):
        nonlocal states, exhausted
        if states >= max_states:
            exhausted = True
            return
        states += 1
        if i == len(ordered):
            consider(bins)
            return
        if best is not None and len(bins) > len(best):
            return
        item = ordered[i]
        seen_totals = set()
        for b in bins:
            total = sum((x["watts"] for x in b), Decimal(0))
            if total in seen_totals:
                continue
            seen_totals.add(total)
            if total + item["watts"] <= ceiling:
                b.append(item)
                place(i + 1)
                b.pop()
        if best is None or len(bins) + 1 <= len(best):
            bins.append([item])
            place(i + 1)
            bins.pop()

    # Always have a deterministic feasible first-fit-decreasing incumbent.
    first = []
    for item in ordered:
        candidate = next((b for b in first if sum((x["watts"] for x in b), Decimal(0))
                          + item["watts"] <= ceiling), None)
        if candidate is None:
            first.append([item])
        else:
            candidate.append(item)
    consider(first)
    lower_bound = math.ceil(sum((x["watts"] for x in items), Decimal(0)) / ceiling)
    if len(first) != lower_bound and len(items) <= 18:
        place(0)
    elif len(first) == lower_bound:
        # The count is proven optimal; do not claim target deviation globally minimal.
        pass
    return best, len(best) == lower_bound, exhausted


def pack(model, policy):
    """Return proposals only; never silently rewrite light/channel assignments.

    The approved CC cohort entries are scoped physical evidence supplied by
    the engineer, not implied from 'driverless', nominal V, or parallel wiring.
    """
    target = decimal(policy.get("target_watts", 90), "target_watts")
    limit = decimal(policy.get("design_max_watts", 95), "design_max_watts")
    rated = decimal(policy.get("rated_watts", 100), "rated_watts")
    if not 0 < target <= limit <= rated:
        raise ValueError("Require 0 < target <= design_max <= rating")
    if limit > MAX_W:
        raise ValueError("KIS Class 2 design maximum is 95 W")
    if rated != 100:
        raise ValueError("This v0.1 Class 2 profile requires a 100 W rating")
    if policy.get("topology", "parallel") != "parallel":
        raise ValueError("Only electrical parallel connection is permitted")

    profile = policy.get("output_capability", {})
    if not profile.get("manufacturer_evidence_ref_ids"):
        raise ValueError("Output current/voltage limits need manufacturer evidence references")
    min_a = decimal(profile.get("cc_min_current_a"), "cc_min_current_a")
    max_a = decimal(profile.get("cc_max_current_a"), "cc_max_current_a")
    min_v = decimal(profile.get("cc_min_voltage_v"), "cc_min_voltage_v")
    max_v = decimal(profile.get("cc_max_voltage_v"), "cc_max_voltage_v")
    if not (0 < min_a <= max_a and 0 < min_v <= max_v):
        raise ValueError("Output limits must be positive and ordered")

    zone_by_light = {}
    for zone in model["light_zones"]:
        if zone.get("parent_zone_id") is not None or zone.get("light_object_ids"):
            for lid in zone["light_object_ids"]:
                if lid in zone_by_light:
                    raise ValueError("Light belongs to multiple endpoint zones: " + lid)
                zone_by_light[lid] = zone["id"]
    cohorts = {}
    for cohort in policy.get("approved_parallel_cc_cohorts", []):
        ids = cohort.get("light_ids", [])
        if not cohort.get("approved") or len(set(ids)) != len(ids) or not cohort.get("evidence_ref_ids"):
            raise ValueError("CC parallel cohort requires explicit approval and evidence")
        for lid in ids:
            if lid in cohorts:
                raise ValueError("Light belongs to multiple CC cohorts: " + lid)
            cohorts[lid] = cohort["id"]

    findings = []
    groups = defaultdict(list)
    total_watts = Decimal(0)
    source_by_id = {l["id"]: l for l in model["light_objects"]}
    for lid in cohorts:
        if lid not in source_by_id:
            raise ValueError("Unknown CC cohort member: " + lid)
    for light in model["light_objects"]:
        lid = light["id"]
        if lid not in zone_by_light:
            findings.append(dict(light_id=lid, issue="unassigned_endpoint_zone",status="blocking"))
            continue
        d = light["design"]
        try:
            w = light_watts(light)
            total_watts += w
            if w > limit:
                findings.append(dict(light_id=lid, issue="oversized_single_fixture",status="blocking"))
                continue
            mode = d.get("input_power_mode")
            electrical = d.get("input_power_type")
            voltage = d.get("input_voltage") or {}
            nominal = decimal(voltage.get("nominal_v"), "nominal_voltage")
            if electrical not in ("ac", "dc") or mode not in ("constant_voltage", "constant_current"):
                raise ValueError("Unknown AC/DC or CV/CC mode")
            compat = d.get("compatibility_group")
            if not compat:
                raise ValueError("Missing evidence-backed compatibility group")
            # CC regulation acts at the remotely located driver, so current
            # is ADDITIVE across parallel branches, never equal per fixture.
            if mode == "constant_current":
                branch_ma = decimal(d.get("input_current_ma"), "branch_current_ma")
                if branch_ma <= 0:
                    raise ValueError("CC branch current must be positive")
                cohort = cohorts.get(lid)
                if not cohort:
                    findings.append(dict(light_id=lid, issue="cc_parallel_evidence_missing",
                                         status="needs_review",
                                         note="No approved manufacturer-supported parallel sharing cohort."))
                vmin = decimal(voltage.get("min_v"), "fixture_min_voltage")
                vmax = decimal(voltage.get("max_v"), "fixture_max_voltage")
                if not (min_v <= vmin <= nominal <= vmax <= max_v):
                    raise ValueError("Fixture voltage requirement outside supported driver compliance")
                # No inferred acceptance of different LED characteristics.
                key = (zone_by_light[lid], electrical, mode, str(nominal), compat,
                       cohort if cohort else "UNVERIFIED-" + lid)
            else:
                branch_ma = None
                key = (zone_by_light[lid], electrical, mode, str(nominal), compat, "CV")
            groups[key].append(dict(id=lid, watts=w, branch_ma=branch_ma,
                                    vmin=voltage.get("min_v"), vmax=voltage.get("max_v")))
        except (ValueError, KeyError, TypeError) as e:
            findings.append(dict(light_id=lid, issue="electrical_data_incomplete_or_invalid",
                                 status="blocking", detail=str(e)))

    proposals = []
    optimality = []
    for key, items in sorted(groups.items()):
        zone, electrical, mode, nominal, compat, cohort = key
        ceiling = limit
        if mode == "constant_current":
            # Regulated output current must remain in the evidenced range.
            # First-pass watt packing may yield current-invalid bins. Refine
            # by enumerating groupings with an additive current window.
            low_ma, high_ma = min_a * 1000, max_a * 1000
            if any(x["branch_ma"] > high_ma for x in items):
                findings.append(dict(zone_id=zone, issue="cc_branch_over_output_max",status="blocking"))
                continue
            bins, proven, exhausted = _pack_cc(items, ceiling, target, low_ma, high_ma)
            if bins is None:
                findings.append(dict(zone_id=zone, issue="cc_output_range_infeasible",
                                     status="blocking", light_ids=[x["id"] for x in items]))
                continue
        else:
            bins, proven, exhausted = _exact_bins(items, ceiling, target)
        optimality.append(proven)
        for members in bins:
            watts = sum((x["watts"] for x in members), Decimal(0))
            current_ma = sum((x["branch_ma"] for x in members), Decimal(0)) if mode == "constant_current" else None
            proposals.append(dict(proposed_id="PACK-" + "-".join(sorted(x["id"] for x in members)),
                                  light_zone_id=zone, light_ids=sorted(x["id"] for x in members),
                                  mode=mode, output_power_type=electrical,
                                  nominal_voltage_v=float(decimal(nominal, "nominal_v")),
                                  compatibility_group=compat,
                                  topology="parallel", watts=float(watts),
                                  current_setpoint_ma=float(current_ma) if current_ma is not None else None,
                                  utilization_pct=float(watts / rated * 100),
                                  unused_design_watts=float(limit - watts),
                                  target_deviation_watts=float(abs(target - watts)),
                                  cc_parallel_evidence_cohort=cohort if mode=="constant_current" and len(members)>1 else None))
        if exhausted:
            findings.append(dict(zone_id=zone, issue="search_budget_exhausted",
                                 status="needs_review",note="Feasible candidate, optimality unproved."))

    grouped_ids = [lid for item in proposals for lid in item["light_ids"]]
    missing_ids = sorted(set(source_by_id) - set(grouped_ids))
    if len(grouped_ids) != len(set(grouped_ids)):
        raise RuntimeError("Packing assigned a light more than once")
    blocked = any(f["status"] == "blocking" for f in findings) or bool(missing_ids)
    pending = any(f["status"] == "needs_review" for f in findings)
    outcome = "needs_review" if blocked or pending else ("optimized" if all(optimality) else "feasible_not_proven_optimal")
    zcounts = defaultdict(list)
    for p in proposals:
        zcounts[p["light_zone_id"]].append(p["watts"])
    return dict(process="PROC-M4-CHANNEL-PACK",version="0.1.0",
                model_revision=model["project"]["model_revision"],status=outcome,
                electrically_verified=not (blocked or pending),
                optimal_channel_count_proven=bool(optimality) and all(optimality) and not blocked,
                basis=dict(topology="parallel",rated_watts=float(rated),
                           design_max_watts=float(limit),target_watts=float(target),
                           output_manufacturer_evidence_ref_ids=profile["manufacturer_evidence_ref_ids"]),
                proposed_channels=proposals,findings=findings,unpacked_light_ids=missing_ids,
                totals=dict(input_light_count=len(source_by_id),proposed_channel_count=len(proposals),
                            total_input_watts=float(total_watts),
                            packed_watts=float(sum((Decimal(str(p["watts"])) for p in proposals), Decimal(0))),
                            zone_utilization={z:dict(channels=len(ws),watts=sum(ws),
                                mean_watts_per_channel=sum(ws)/len(ws)) for z,ws in sorted(zcounts.items())}),
                note="Read-only candidate allocation. Manufacturer qualification, canonical CC validator integration, owner acceptance and controller assignment are separate gates.")


def _pack_cc(items, ceiling, target, min_ma, max_ma):
    """Exact search up to 18 items; larger cohorts use greedy and disclose
    unproved optimality. Unlike watt-only packing, every CC bin must satisfy
    both current bounds; no below-minimum singleton is silently accepted.
    """
    ordered = sorted(items, key=lambda x: (-x["watts"], x["id"]))
    if len(ordered) > 18:
        bins = []
        for x in ordered:
            b = next((b for b in bins if sum((y["watts"] for y in b), Decimal(0))+x["watts"]<=ceiling and
                      sum((y["branch_ma"] for y in b), Decimal(0))+x["branch_ma"]<=max_ma),None)
            if b is None:bins.append([x])
            else:b.append(x)
        if any(sum((x["branch_ma"] for x in b), Decimal(0))<min_ma for b in bins):
            return None, False, False
        return bins, False, False
    best = None
    best_score = None
    bins = []
    def recurse(i):
        nonlocal best,best_score
        if best is not None and len(bins)>len(best):return
        if i == len(ordered):
            if any(not min_ma<=sum((x["branch_ma"] for x in b),Decimal(0))<=max_ma for b in bins):
                return
            totals=[sum((x["watts"] for x in b),Decimal(0)) for b in bins]
            score=(len(bins),sum((abs(x-target) for x in totals),Decimal(0)),
                   tuple(sorted(tuple(sorted(x["id"] for x in b)) for b in bins)))
            if best_score is None or score<best_score:
                best_score=score;best=[list(b) for b in bins]
            return
        x=ordered[i]
        seen=set()
        for b in bins:
            watts=sum((y["watts"] for y in b),Decimal(0))
            amps=sum((y["branch_ma"] for y in b),Decimal(0))
            if (watts,amps) in seen:continue
            seen.add((watts,amps))
            if watts+x["watts"]<=ceiling and amps+x["branch_ma"]<=max_ma:
                b.append(x);recurse(i+1);b.pop()
        if best is None or len(bins)+1<=len(best):
            bins.append([x]);recurse(i+1);bins.pop()
    recurse(0)
    return best, best is not None, False


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("model",type=Path)
    parser.add_argument("policy",type=Path)
    parser.add_argument("output",type=Path)
    args=parser.parse_args()
    if args.output.exists():parser.error("Output exists; preserve previous review revision")
    output=pack(json.loads(args.model.read_text()),json.loads(args.policy.read_text()))
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(output,indent=2)+"\n")
    print(json.dumps(dict(status=output["status"],channels=output["totals"]["proposed_channel_count"],
                          findings=len(output["findings"]))))
    if output["status"]=="needs_review":raise SystemExit(1)


if __name__=="__main__":
    main()
