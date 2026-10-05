---
title: "M4 Electrical Attributes v0.6"
page_type: canonical_model
page_status: draft
confidence_level: medium
domain_primary: low-voltage-lighting
ai_role: model_contract
invocation_triggers:
  systems_present: [low_voltage_lighting]
decision_axes: [source_voltage, electrical_interface, fixture_capability, channel_compatibility]
related_pages:
  - "electrical-interfaces-v0.5.md"
  - "light-object.md"
  - "lv-channel.md"
  - "../../concepts/micro-lv-control-channels.md"
---

# M4 Electrical Attributes v0.6

## Purpose

M4 separates numeric voltage, AC/DC power type, CV/CC power mode, physical fixture capability, and applied zone behavior. These are independent facts and may not be rewritten to make channel grouping convenient.

## Canonical electrical attributes

At every modeled electrical interface, preserve the following as distinct attributes when applicable:

- `power_type`: `ac`, `dc`, or null.
- `power_mode`: `constant_voltage`, `constant_current`, or null.
- `nominal_v`: numeric volts or null.
- `min_v`: numeric volts or null.
- `max_v`: numeric volts or null.
- `current_ma`: numeric current setpoint/requirement where applicable, otherwise null.
- `driver_type`: physical driver/driverless/other architecture where applicable.
- `dimming_capability`: `dimmable`, `non_dimmable`, or null for the selected physical fixture/interface.

Voltage fields contain numeric values only. Do not encode `VDC`, `VAC`, `AC`, `DC`, or descriptive text in a voltage value. AC/DC belongs in the peer power-type attribute.

`min_v` and `max_v` are first-class values, not notes. They are especially important for constant-current fixtures and drivers, whose required operating range and output compliance range may determine whether an assignment is viable.

## Source, selected fixture, and output interfaces

Keep the source fixture schedule and the selected LV implementation distinct:

- Source fixture type: `source_voltage`, `source_power_type`, `source_power_mode`, `source_current_ma`, `source_driver_type`, `source_dimming_capability`.
- Selected light interface: `input_voltage`, `input_power_type`, `input_power_mode`, `input_current_ma`, `driver_type`, `dimming_capability`.
- Micro LV channel/output: `voltage`, `output_power_type`, `output_power_mode`, `output_current_ma`.

A source fixture can differ from the selected LV replacement. Preserve both rather than overwriting the source facts.

## Capability versus applied behavior

Fixture capability is physical. Zone requirements are functional.

A dimmable fixture may be installed in a zone whose reviewed narrative requires only on/off control. The unused dimming capability does not disappear and does not change the fixture's voltage, AC/DC type, CV/CC mode, current, driver architecture, or wattage.

Example: fixture C1 remains a 36 VDC constant-current dimmable fixture in an Alcove zone that does not require dimming. It does not become a 48 VDC fixture. If a physically different product is desired for that occurrence, create/select a distinct fixture type or approved variant and preserve the decision record.

The reverse condition is not acceptable without resolution: a zone that requires dimming cannot be assigned a selected fixture/interface confirmed as non-dimmable.

## M4 grouping use

The minimum electrical grouping key is:

`power_type + power_mode + applicable voltage/current requirements + fixture/interface compatibility + functional control requirement + emergency class + watt limit`

Matching watts or a shared zone does not override an electrical mismatch.

For fixed CV outputs, the selected output voltage and fixture input voltage must match unless an explicitly modeled compatible interface exists. For CC outputs, current requirements and required/compliance voltage ranges must be checked explicitly. Future mixed-fixture CC grouping may be permitted only when the modeled topology and product evidence support it.

## M4 Class 2 design profile

The current M4 baseline uses a 100 W rated Class 2 channel with a 95 W maximum design load. The legacy 90 W profile remains available for older models; M4 work should use `class2_100w_95w_design` unless project/product evidence requires another profile.

Owner: KIS Solutions. October 2026; draft pending YMCA M4 validation.
