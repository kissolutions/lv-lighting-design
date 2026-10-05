"""M4 v0.6 electrical-interface, capability, and micro-channel checks."""
from __future__ import annotations

from collections import defaultdict


def voltage_shape_issues_v06(model):
    issues = []
    profiles = [(t["id"], t["source_voltage"]) for t in model["fixture_types"]]
    profiles += [(l["id"], l["design"]["input_voltage"]) for l in model["light_objects"]]
    profiles += [(c["id"], c["voltage"]) for b in model["branch_circuits"] for u in b["power_units"] for c in u["channels"]]
    for owner, voltage in profiles:
        low, high, nominal = (voltage[k] for k in ("min_v", "max_v", "nominal_v"))
        invalid = low is not None and high is not None and low > high
        invalid |= nominal is not None and low is not None and nominal < low
        invalid |= nominal is not None and high is not None and nominal > high
        if invalid:
            issues.append(dict(rule="voltage-shape", entity_id=owner,
                               message="Voltage range/nominal values contradict one another."))
    return issues


def m4_interface_issues(model):
    issues, members = [], defaultdict(list)
    channels = {c["id"]: c for b in model["branch_circuits"] for u in b["power_units"] for c in u["channels"]}
    zones = {z["id"]: z for z in model["light_zones"]}
    light_zone = {}
    for zone in model["light_zones"]:
        for lid in zone["light_object_ids"]:
            light_zone[lid] = zone["id"]

    def fail(rule, owner, message):
        issues.append(dict(rule=rule, entity_id=owner, message=message))

    def confirmed_profile(voltage, power_type, mode, current):
        if power_type is None or mode is None:
            return False
        if mode == "constant_voltage":
            return voltage["nominal_v"] is not None and current is None
        return voltage["min_v"] is not None and voltage["max_v"] is not None and current is not None

    for light in model["light_objects"]:
        owner, design = light["id"], light["design"]
        voltage, ptype, mode, current = (design[k] for k in ("input_voltage", "input_power_type", "input_power_mode", "input_current_ma"))
        if design["driver_type"] is None:
            fail("light-driver-basis", owner, "Confirm selected driver architecture independently of dimming and CV/CC mode.")
        if design["dimming_capability"] is None:
            fail("light-dimming-capability", owner, "Confirm whether the selected physical fixture/interface is dimmable or non-dimmable.")
        if not confirmed_profile(voltage, ptype, mode, current):
            fail("light-electrical-basis", owner,
                 "Confirm selected AC/DC power type, CV/CC mode, and numeric nominal/range voltage/current at the channel interface.")
        cid = design["channel_id"]
        if cid is not None:
            members[cid].append(light)

    output_claims = {}
    for cid, lights in members.items():
        channel = channels[cid]
        voltage, ptype, mode, current = (channel[k] for k in ("voltage", "output_power_type", "output_power_mode", "output_current_ma"))
        if not confirmed_profile(voltage, ptype, mode, current):
            fail("channel-electrical-basis", cid,
                 "Confirm selected output AC/DC power type, CV/CC mode, and numeric fixed voltage or CC setpoint/compliance range.")
        if channel["validation_profile"] == "class2_100w_95w_design" and channel["design_limit_watts"] not in (None, 95):
            fail("channel-design-profile", cid, "The M4 Class 2 profile uses a 95 W maximum design limit on a 100 W rated channel.")
        if mode == "constant_current" and len(lights) > 1:
            fail("cc-topology-review", cid,
                 "Multiple physical fixtures on one CC output require explicit supported topology evidence before mixed-fixture grouping is accepted.")

        actual_zones = {light_zone.get(l["id"]) for l in lights}
        if None in actual_zones:
            fail("micro-channel-zone", cid, "Every fixture on a used micro LV channel must belong to a reviewed functional zone.")
            actual_zones.discard(None)
        if len(actual_zones) > 1:
            fail("micro-channel-zone", cid, "A micro LV control channel cannot span multiple functional zones.")
        elif actual_zones and channel["light_zone_id"] != next(iter(actual_zones)):
            fail("micro-channel-zone", cid, "Channel light_zone_id must match the single functional zone of all assigned fixtures.")

        ctl, out = channel.get("controller_id"), channel.get("controller_output")
        if (ctl is None) != (out is None):
            fail("micro-channel-output", cid, "controller_id and controller_output must be populated together.")
        if ctl is not None:
            key = (ctl, out)
            if key in output_claims:
                fail("micro-channel-output", cid,
                     f"Controller output {ctl}/{out} is already assigned 1:1 to micro channel {output_claims[key]}.")
            else:
                output_claims[key] = cid

        for light in lights:
            owner, design = light["id"], light["design"]
            needed, needed_type, needed_mode = design["input_voltage"], design["input_power_type"], design["input_power_mode"]
            if ptype is not None and needed_type is not None and ptype != needed_type:
                fail("power-type-compatibility", owner, "Selected fixture and channel AC/DC power types disagree.")
            if mode is not None and needed_mode is not None and mode != needed_mode:
                fail("power-mode-compatibility", owner, "Selected fixture and channel CV/CC modes disagree.")
            if mode == needed_mode == "constant_voltage":
                if voltage["nominal_v"] is not None and needed["nominal_v"] is not None and voltage["nominal_v"] != needed["nominal_v"]:
                    fail("voltage-compatibility", owner, "Fixed-voltage fixture input must match the selected channel setting.")
            elif mode == needed_mode == "constant_current":
                if current is not None and design["input_current_ma"] is not None and current != design["input_current_ma"]:
                    fail("current-compatibility", owner, "Selected CC fixture current and channel current setpoint disagree.")
                if len(lights) == 1 and all(v is not None for v in (voltage["min_v"], voltage["max_v"], needed["min_v"], needed["max_v"])):
                    if needed["min_v"] < voltage["min_v"] or needed["max_v"] > voltage["max_v"]:
                        fail("voltage-compatibility", owner, "Required CC fixture voltage range is outside the channel compliance range.")

            zid = light_zone.get(owner)
            if zid is not None:
                zone = zones[zid]
                # Existing zone driver_type is functional/applied behavior, not physical fixture architecture.
                if zone.get("driver_type") == "dimming" and design["dimming_capability"] == "non_dimmable":
                    fail("fixture-control-capability", owner,
                         "Zone requires dimming but the selected physical fixture/interface is non-dimmable.")
                # Deliberately no failure for dimmable fixture in a non-dimming zone. Unused capability does not mutate the fixture.

    return issues
