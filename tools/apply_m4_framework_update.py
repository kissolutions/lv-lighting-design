#!/usr/bin/env python3
"""Apply the October 2026 M4 LV-lighting electrical/channel framework update.

Run from the repository root:
    python tools/apply_m4_framework_update.py

The script is intentionally idempotent. It creates v0.6 alongside v0.5, preserves
legacy v0.5 behavior, and patches current generators only where required to route
v0.6 models through the new contract.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"
TEMPLATES = ROOT / "templates"
GENERATORS = ROOT / "generators"
DOCS = ROOT / "docs"
TESTS = ROOT / "tests"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data):
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def insert_after(seq, existing, new_item):
    if new_item in seq:
        return
    seq.insert(seq.index(existing) + 1, new_item)


def patch_once(text: str, old: str, new: str, label: str) -> str:
    if new in text:
        return text
    if old not in text:
        raise RuntimeError(f"Cannot patch {label}: expected source text not found")
    return text.replace(old, new, 1)


def build_v06_schema():
    src = SCHEMAS / "lighting-project-v0.5.schema.json"
    dst = SCHEMAS / "lighting-project-v0.6.schema.json"
    schema = load_json(src)
    schema["title"] = "KIS LV Lighting Project Model v0.6.0"
    schema["description"] = (
        "M4 electrical/channel contract. AC/DC power type is independent of numeric voltage; "
        "fixture capability remains physical while zone requirements remain functional."
    )
    schema["properties"]["schema_version"]["const"] = "0.6.0"
    defs = schema["$defs"]

    # Voltage is numeric only. AC/DC is a peer interface attribute.
    voltage = defs["voltage"]
    voltage["required"] = [k for k in voltage["required"] if k != "current_type"]
    voltage["properties"].pop("current_type", None)
    voltage["description"] = (
        "Numeric voltage attributes only. nominal_v, min_v and max_v are volts; "
        "AC/DC is stored separately as the applicable peer power-type field."
    )

    # Physical output (the micro LV control channel / supply output).
    channel = defs["channel"]
    for peer in ("output_power_type", "light_zone_id", "controller_id", "controller_output"):
        if peer not in channel["required"]:
            insert_after(channel["required"], "voltage" if peer == "output_power_type" else "output_current_ma", peer)
    channel["properties"]["output_power_type"] = {"enum": ["ac", "dc", None]}
    channel["properties"]["light_zone_id"] = {
        "anyOf": [
            {"type": "string", "pattern": "^[A-Za-z0-9][A-Za-z0-9_.:-]*$"},
            {"type": "null"},
        ],
        "description": "Functional room/control zone served by this micro LV channel. One channel serves one zone; one zone may use many channels.",
    }
    channel["properties"]["controller_id"] = {
        "anyOf": [
            {"type": "string", "pattern": "^[A-Za-z0-9][A-Za-z0-9_.:-]*$"},
            {"type": "null"},
        ],
        "description": "Controller providing this channel's independently commanded output, when applicable.",
    }
    channel["properties"]["controller_output"] = {
        "type": ["integer", "null"],
        "minimum": 1,
        "description": "Physical controller output number. A populated controller/output pair is unique to one micro LV channel.",
    }
    profiles = channel["properties"]["validation_profile"]["enum"]
    if "class2_100w_95w_design" not in profiles:
        profiles.insert(profiles.index("product_specific"), "class2_100w_95w_design")
    existing = next(
        (x for x in channel.get("allOf", [])
         if x.get("if", {}).get("properties", {}).get("validation_profile", {}).get("const") == "class2_100w_90w_design"),
        None,
    )
    if existing and not any(
        x.get("if", {}).get("properties", {}).get("validation_profile", {}).get("const") == "class2_100w_95w_design"
        for x in channel.get("allOf", [])
    ):
        rule95 = copy.deepcopy(existing)
        rule95["if"]["properties"]["validation_profile"]["const"] = "class2_100w_95w_design"
        rule95["then"]["properties"]["design_limit_watts"]["maximum"] = 95
        channel["allOf"].append(rule95)

    # Source fixture facts: electrical interface and inherent capability.
    fixture = defs["fixture_type_v02"]
    insert_after(fixture["required"], "source_voltage", "source_power_type")
    if "source_dimming_capability" not in fixture["required"]:
        fixture["required"].append("source_dimming_capability")
    fixture["properties"]["source_power_type"] = {"enum": ["ac", "dc", None]}
    fixture["properties"]["source_dimming_capability"] = {
        "enum": ["dimmable", "non_dimmable", None],
        "description": "Physical/source fixture capability. This is not the zone's applied dimming requirement.",
    }

    # Selected fixture interface/capability at the channel interface.
    design = defs["light_object"]["properties"]["design"]
    insert_after(design["required"], "input_voltage", "input_power_type")
    if "dimming_capability" not in design["required"]:
        design["required"].append("dimming_capability")
    design["properties"]["input_power_type"] = {"enum": ["ac", "dc", None]}
    design["properties"]["dimming_capability"] = {
        "enum": ["dimmable", "non_dimmable", None],
        "description": (
            "Inherent capability of the selected physical fixture/interface. A non-dimming zone may use a dimmable fixture; "
            "the unused capability does not alter voltage, AC/DC, CV/CC, current, driver architecture or wattage."
        ),
    }

    write_json(dst, schema)


def build_v06_template():
    src = TEMPLATES / "lighting-project-v0.5.template.json"
    dst = TEMPLATES / "lighting-project-v0.6.template.json"
    data = load_json(src)
    data["schema_version"] = "0.6.0"
    write_json(dst, data)


def write_m4_module():
    path = GENERATORS / "model_m4_electrical.py"
    path.write_text('''"""M4 v0.6 electrical-interface, capability, and micro-channel checks."""\nfrom __future__ import annotations\n\nfrom collections import defaultdict\n\n\ndef voltage_shape_issues_v06(model):\n    issues = []\n    profiles = [(t["id"], t["source_voltage"]) for t in model["fixture_types"]]\n    profiles += [(l["id"], l["design"]["input_voltage"]) for l in model["light_objects"]]\n    profiles += [(c["id"], c["voltage"]) for b in model["branch_circuits"] for u in b["power_units"] for c in u["channels"]]\n    for owner, voltage in profiles:\n        low, high, nominal = (voltage[k] for k in ("min_v", "max_v", "nominal_v"))\n        invalid = low is not None and high is not None and low > high\n        invalid |= nominal is not None and low is not None and nominal < low\n        invalid |= nominal is not None and high is not None and nominal > high\n        if invalid:\n            issues.append(dict(rule="voltage-shape", entity_id=owner,\n                               message="Voltage range/nominal values contradict one another."))\n    return issues\n\n\ndef m4_interface_issues(model):\n    issues, members = [], defaultdict(list)\n    channels = {c["id"]: c for b in model["branch_circuits"] for u in b["power_units"] for c in u["channels"]}\n    zones = {z["id"]: z for z in model["light_zones"]}\n    light_zone = {}\n    for zone in model["light_zones"]:\n        for lid in zone["light_object_ids"]:\n            light_zone[lid] = zone["id"]\n\n    def fail(rule, owner, message):\n        issues.append(dict(rule=rule, entity_id=owner, message=message))\n\n    def confirmed_profile(voltage, power_type, mode, current):\n        if power_type is None or mode is None:\n            return False\n        if mode == "constant_voltage":\n            return voltage["nominal_v"] is not None and current is None\n        return voltage["min_v"] is not None and voltage["max_v"] is not None and current is not None\n\n    for light in model["light_objects"]:\n        owner, design = light["id"], light["design"]\n        voltage, ptype, mode, current = (design[k] for k in ("input_voltage", "input_power_type", "input_power_mode", "input_current_ma"))\n        if design["driver_type"] is None:\n            fail("light-driver-basis", owner, "Confirm selected driver architecture independently of dimming and CV/CC mode.")\n        if design["dimming_capability"] is None:\n            fail("light-dimming-capability", owner, "Confirm whether the selected physical fixture/interface is dimmable or non-dimmable.")\n        if not confirmed_profile(voltage, ptype, mode, current):\n            fail("light-electrical-basis", owner,\n                 "Confirm selected AC/DC power type, CV/CC mode, and numeric nominal/range voltage/current at the channel interface.")\n        cid = design["channel_id"]\n        if cid is not None:\n            members[cid].append(light)\n\n    output_claims = {}\n    for cid, lights in members.items():\n        channel = channels[cid]\n        voltage, ptype, mode, current = (channel[k] for k in ("voltage", "output_power_type", "output_power_mode", "output_current_ma"))\n        if not confirmed_profile(voltage, ptype, mode, current):\n            fail("channel-electrical-basis", cid,\n                 "Confirm selected output AC/DC power type, CV/CC mode, and numeric fixed voltage or CC setpoint/compliance range.")\n        if channel["validation_profile"] == "class2_100w_95w_design" and channel["design_limit_watts"] not in (None, 95):\n            fail("channel-design-profile", cid, "The M4 Class 2 profile uses a 95 W maximum design limit on a 100 W rated channel.")\n        if mode == "constant_current" and len(lights) > 1:\n            fail("cc-topology-review", cid,\n                 "Multiple physical fixtures on one CC output require explicit supported topology evidence before mixed-fixture grouping is accepted.")\n\n        actual_zones = {light_zone.get(l["id"]) for l in lights}\n        if None in actual_zones:\n            fail("micro-channel-zone", cid, "Every fixture on a used micro LV channel must belong to a reviewed functional zone.")\n            actual_zones.discard(None)\n        if len(actual_zones) > 1:\n            fail("micro-channel-zone", cid, "A micro LV control channel cannot span multiple functional zones.")\n        elif actual_zones and channel["light_zone_id"] != next(iter(actual_zones)):\n            fail("micro-channel-zone", cid, "Channel light_zone_id must match the single functional zone of all assigned fixtures.")\n\n        ctl, out = channel.get("controller_id"), channel.get("controller_output")\n        if (ctl is None) != (out is None):\n            fail("micro-channel-output", cid, "controller_id and controller_output must be populated together.")\n        if ctl is not None:\n            key = (ctl, out)\n            if key in output_claims:\n                fail("micro-channel-output", cid,\n                     f"Controller output {ctl}/{out} is already assigned 1:1 to micro channel {output_claims[key]}.")\n            else:\n                output_claims[key] = cid\n\n        for light in lights:\n            owner, design = light["id"], light["design"]\n            needed, needed_type, needed_mode = design["input_voltage"], design["input_power_type"], design["input_power_mode"]\n            if ptype is not None and needed_type is not None and ptype != needed_type:\n                fail("power-type-compatibility", owner, "Selected fixture and channel AC/DC power types disagree.")\n            if mode is not None and needed_mode is not None and mode != needed_mode:\n                fail("power-mode-compatibility", owner, "Selected fixture and channel CV/CC modes disagree.")\n            if mode == needed_mode == "constant_voltage":\n                if voltage["nominal_v"] is not None and needed["nominal_v"] is not None and voltage["nominal_v"] != needed["nominal_v"]:\n                    fail("voltage-compatibility", owner, "Fixed-voltage fixture input must match the selected channel setting.")\n            elif mode == needed_mode == "constant_current":\n                if current is not None and design["input_current_ma"] is not None and current != design["input_current_ma"]:\n                    fail("current-compatibility", owner, "Selected CC fixture current and channel current setpoint disagree.")\n                if len(lights) == 1 and all(v is not None for v in (voltage["min_v"], voltage["max_v"], needed["min_v"], needed["max_v"])):\n                    if needed["min_v"] < voltage["min_v"] or needed["max_v"] > voltage["max_v"]:\n                        fail("voltage-compatibility", owner, "Required CC fixture voltage range is outside the channel compliance range.")\n\n            zid = light_zone.get(owner)\n            if zid is not None:\n                zone = zones[zid]\n                # Existing zone driver_type is functional/applied behavior, not physical fixture architecture.\n                if zone.get("driver_type") == "dimming" and design["dimming_capability"] == "non_dimmable":\n                    fail("fixture-control-capability", owner,\n                         "Zone requires dimming but the selected physical fixture/interface is non-dimmable.")\n                # Deliberately no failure for dimmable fixture in a non-dimming zone. Unused capability does not mutate the fixture.\n\n    return issues\n''', encoding="utf-8")


def patch_model_intake():
    path = GENERATORS / "model_intake.py"
    text = path.read_text(encoding="utf-8")
    text = patch_once(
        text,
        "from .model_voltage import interface_issues, voltage_shape_issues\n",
        "from .model_voltage import interface_issues, voltage_shape_issues\nfrom .model_m4_electrical import m4_interface_issues, voltage_shape_issues_v06\n",
        "model_intake import",
    )
    text = patch_once(
        text,
        "SCHEMA_V05 = SCHEMA.with_name('lighting-project-v0.5.schema.json')\n",
        "SCHEMA_V05 = SCHEMA.with_name('lighting-project-v0.5.schema.json')\nSCHEMA_V06 = SCHEMA.with_name('lighting-project-v0.6.schema.json')\n",
        "v0.6 schema path",
    )
    marker = "\ndef check_model(model, phase='intake'):\n"
    if "def upgrade_v06(" not in text:
        fn = '''\n\ndef upgrade_v06(model):\n    """Upgrade v0.3-v0.5 electrical data without changing physical fixture identity."""\n    if model.get('schema_version') in ('0.3.0', '0.3.1', '0.4.0'):\n        model = upgrade_v05(model)\n    if model.get('schema_version') != '0.5.0':\n        raise ValueError('M4 electrical upgrade requires a v0.3-v0.5 model.')\n    upgraded = copy.deepcopy(model)\n    upgraded['schema_version'] = '0.6.0'\n    for fixture in upgraded['fixture_types']:\n        voltage = fixture['source_voltage']\n        fixture['source_power_type'] = voltage.pop('current_type', None)\n        fixture['source_dimming_capability'] = None\n    for light in upgraded['light_objects']:\n        design = light['design']\n        design['input_power_type'] = design['input_voltage'].pop('current_type', None)\n        design['dimming_capability'] = None\n    for branch in upgraded['branch_circuits']:\n        for unit in branch['power_units']:\n            for channel in unit['channels']:\n                channel['output_power_type'] = channel['voltage'].pop('current_type', None)\n                channel['light_zone_id'] = None\n                channel['controller_id'] = None\n                channel['controller_output'] = None\n    return upgraded\n'''
        text = text.replace(marker, fn + marker, 1)
    text = patch_once(
        text,
        "    electrical_version = model.get('schema_version') == '0.5.0'\n    schema = json.loads((SCHEMA_V05 if electrical_version else SCHEMA).read_text())\n",
        "    version = model.get('schema_version')\n    electrical_version = version in ('0.5.0', '0.6.0')\n    m4_version = version == '0.6.0'\n    schema_path = SCHEMA_V06 if m4_version else (SCHEMA_V05 if electrical_version else SCHEMA)\n    schema = json.loads(schema_path.read_text())\n",
        "schema routing",
    )
    text = patch_once(
        text,
        "    if electrical_version:\n        issues.extend(voltage_shape_issues(model))\n        if issues:\n            return result()\n",
        "    if electrical_version:\n        issues.extend(voltage_shape_issues_v06(model) if m4_version else voltage_shape_issues(model))\n        if issues:\n            return result()\n",
        "voltage shape routing",
    )
    text = patch_once(
        text,
        "    if electrical_version:\n        (issues if phase == 'design' else deferred).extend(interface_issues(model))\n",
        "    if electrical_version:\n        electrical_issues = m4_interface_issues(model) if m4_version else interface_issues(model)\n        (issues if phase == 'design' else deferred).extend(electrical_issues)\n",
        "electrical issue routing",
    )
    # Strip v0.6-only fields from temporary legacy projection used by inherited checks.
    old_fixture_tuple = "('source_voltage', 'source_power_mode', 'source_current_ma',\n                            'source_voltage_basis', 'source_voltage_note', 'source_driver_type', 'source_driver_note')"
    new_fixture_tuple = "('source_voltage', 'source_power_type', 'source_power_mode', 'source_current_ma',\n                            'source_voltage_basis', 'source_voltage_note', 'source_driver_type', 'source_driver_note',\n                            'source_dimming_capability')"
    if old_fixture_tuple in text:
        text = text.replace(old_fixture_tuple, new_fixture_tuple, 1)
    old_light_tuple = "('input_voltage', 'input_power_mode', 'input_current_ma', 'driver_type', 'driver_note')"
    new_light_tuple = "('input_voltage', 'input_power_type', 'input_power_mode', 'input_current_ma', 'driver_type', 'driver_note',\n                                'dimming_capability')"
    if old_light_tuple in text:
        text = text.replace(old_light_tuple, new_light_tuple, 1)
    old_channel = "                        channel.pop('output_power_mode')\n                        channel.pop('output_current_ma')\n"
    new_channel = "                        channel.pop('output_power_mode')\n                        channel.pop('output_current_ma')\n                        channel.pop('output_power_type', None)\n                        channel.pop('light_zone_id', None)\n                        channel.pop('controller_id', None)\n                        channel.pop('controller_output', None)\n"
    if old_channel in text and new_channel not in text:
        text = text.replace(old_channel, new_channel, 1)
    path.write_text(text, encoding="utf-8")


def patch_exporter():
    path = GENERATORS / "export_intake.py"
    text = path.read_text(encoding="utf-8")
    text = text.replace(
        "source_voltage_current_type=voltage.get('current_type'),",
        "source_power_type=t.get('source_power_type', voltage.get('current_type')), source_voltage_current_type=voltage.get('current_type'),",
    )
    text = text.replace(
        "'source_voltage_current_type', 'source_power_mode'",
        "'source_power_type', 'source_voltage_current_type', 'source_power_mode'",
    )
    text = text.replace(
        "lv_input_current_type=voltage.get('current_type'),",
        "lv_input_power_type=l['design'].get('input_power_type', voltage.get('current_type')), lv_input_current_type=voltage.get('current_type'),",
    )
    text = text.replace(
        "'lv_input_voltage', 'lv_input_voltage_min_v', 'lv_input_voltage_max_v', 'lv_input_current_type',",
        "'lv_input_voltage', 'lv_input_voltage_min_v', 'lv_input_voltage_max_v', 'lv_input_power_type', 'lv_input_current_type',",
    )
    path.write_text(text, encoding="utf-8")


def patch_playbook():
    path = DOCS / "design-playbooks" / "lighting-design-playbook.md"
    text = path.read_text(encoding="utf-8")
    text = text.replace("100 W / <=90 W design profile", "100 W / <=95 W M4 design profile")
    block = '''\n\n### M4 Micro LV Control Channel and Fixture-Capability Rules\n\nUse [Micro LV Control Channels](../concepts/micro-lv-control-channels.md) and the [v0.6 electrical attributes](../ontology/canonical-model/m4-electrical-attributes-v0.6.md) for M4 grouping. One functional room/control zone may require many micro LV channels, but each micro LV channel serves one functional zone and corresponds to one independently commanded physical output. Grouping must preserve physical fixture interface facts before considering the zone narrative.\n\nA control narrative can use less capability than a selected physical fixture provides. A dimmable fixture in an on/off-only zone remains the same dimmable fixture with the same AC/DC type, CV/CC mode, numeric nominal/min/max voltage, current requirement, driver architecture and load. Do not mutate fixture C1 (for example, a 36 VDC CC dimmable fixture) into a 48 VDC fixture merely because its zone does not require dimming. If a physically different implementation is desired, create/select a distinct fixture type or approved variant and preserve the decision trail.\n\nThe converse is a design failure: when the functional zone requires dimming and the selected fixture/interface is non-dimmable, resolve the fixture or the reviewed control requirement before channel assignment.\n'''
    if "### M4 Micro LV Control Channel and Fixture-Capability Rules" not in text:
        text += block
    path.write_text(text, encoding="utf-8")


def patch_docs_links():
    # Keep this deliberately minimal; the new pages are authoritative additions.
    path = DOCS / "ontology" / "canonical-model" / "light-object.md"
    text = path.read_text(encoding="utf-8")
    note = "\nFor M4, see [v0.6 electrical attributes](m4-electrical-attributes-v0.6.md): AC/DC power type is a peer of numeric voltage, min/max voltage remain explicit, and selected fixture dimming capability is physical rather than inferred from zone behavior.\n"
    if "v0.6 electrical attributes" not in text:
        text = text.replace("# Light Object\n", "# Light Object\n" + note, 1)
        path.write_text(text, encoding="utf-8")


def main():
    required = [SCHEMAS / "lighting-project-v0.5.schema.json", GENERATORS / "model_intake.py", GENERATORS / "export_intake.py"]
    missing = [str(p.relative_to(ROOT)) for p in required if not p.exists()]
    if missing:
        raise SystemExit("Run from an lv-lighting-design checkout. Missing: " + ", ".join(missing))
    build_v06_schema()
    build_v06_template()
    write_m4_module()
    patch_model_intake()
    patch_exporter()
    patch_playbook()
    patch_docs_links()
    print("M4 framework update applied: v0.6 schema/template, electrical/channel checks, exporter fields, and guidance.")


if __name__ == "__main__":
    main()
