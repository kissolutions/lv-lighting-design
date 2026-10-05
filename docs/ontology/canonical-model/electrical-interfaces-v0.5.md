---
title: "Source Voltage and Selected Electrical Interfaces v0.5"
page_type: canonical_model
page_status: draft
confidence_level: medium
domain_primary: low-voltage-lighting
ai_role: model_contract
invocation_triggers:
  systems_present: [low_voltage_lighting]
decision_axes: [source_voltage, electrical_interface, power_mode, channel_compatibility]
related_pages:
  - "physical-intake-v0.4.md"
  - "fixture-type.md"
  - "light-object.md"
  - "../../../schemas/lighting-project-v0.5.schema.json"
---

# Source Voltage and Selected Electrical Interfaces v0.5

## Purpose and Scope

The current draft is `schema_version: 0.5.0`. It retains v0.4 physical-first ownership, served Spaces, later zones and stable IDs, while restoring source voltage to the fixture schedule and explicitly checking the selected light/channel electrical interface. Voltage and drive mode constrain grouping independently of watts. No default zones or automatic equipment counts are created.

## Fields and Meaning

| Record | Added fields | Meaning |
|---|---|---|
| `fixture_types[]` | `source_voltage` | Peer of `source_load`: original voltage evidence, with `current_type` (`ac`/`dc`/null), `nominal_v`, `min_v`, `max_v`. All numbers are volts. Unknowns are null. |
| `fixture_types[]` | `source_power_mode`, `source_current_ma` | Observed `constant_voltage`/`constant_current`/null and CC drive-current setpoint in mA where supported. Unknown mode/current stay null; do not infer from watts. |
| `fixture_types[]` | `source_voltage_basis`, `source_voltage_note` | Identify `fixture_input`, `led_module_input`, `driver_output`, or `unknown`; preserve original wording/options and ambiguities in the note and source references. |
| `fixture_types[]` | `source_driver_type`, `source_driver_note` | Source architecture: `driver`, `driverless`, `other`, or null. Preserve unfamiliar descriptions and integral/remote arrangement where supported in the note; `other` requires a description. |
| `light_objects[].design` | `input_voltage`, `input_power_mode`, `input_current_ma` | Selected electrical input at the interface powered by the assigned supply channel, with the same voltage shape, selected CV/CC mode and CC setpoint. A downstream module's CC drive is not automatically the channel's mode. |
| `light_objects[].design` | `driver_type`, `driver_note` | Independently selected driver/driverless/other architecture, with a description required for `other`. This does not replace the legacy zone `driver_type`, which describes dimming/non-dimming behavior. |
| Power-unit `channels[]` | `output_power_mode`, `output_current_ma` | Selected output CV/CC mode and CC setpoint; existing `voltage` records the actual output setting or CC compliance range. |

All added fields are required in v0.5 but their unknown values are permitted during intake. Retain original electrical facts even when the selected LV replacement differs. Source fixture AC input, source driver output and selected LV channel input are distinct interfaces. Never substitute one for another or change a source fact to make a group pass. Preserve type/options separately when voltage variants are distinct schedule items; resolve per-occurrence deviations explicitly rather than assigning one unsupported voltage to every light of that type.

Driver architecture, CV/CC regulation mode and dimming capability are separate facts. Do not infer voltage, current, dimming, driver location or electrical compatibility solely from `driver`/`driverless`. Use `other` plus source wording for unfamiliar architectures, leaving an unsupported classification null. Selected source and replacement driver types can differ with supported selection evidence; retaining a source driver does not establish its LV compatibility. Driver quantity/location/interface breakdown remains selection evidence and later modeling work, not an automatic BOM count.

Example: a source fixture may be scheduled at 120 V AC while its selected LV replacement/interface operates at 48 V DC. The source schedule still shows 120 V AC; grouping uses the verified selected 48 V DC input. A compatible DC/DC or other interface can change the downstream LED voltage, but its verified input/output, losses/load and limits must support the selection; the checker does not invent an adapter.

## Relationships and Review Schedule

The Fixture-Type CSV puts `source_voltage` immediately after existing `source_watts` (the schedule's source-wattage value). This column is nominal volts, with separate minimum/maximum, AC/DC, mode/current, basis and note columns, plus `source_driver_type` and its note. A range-only voltage has a blank nominal column, not an invented midpoint. Unknown fields export blank, never zero. Light Points separately exports selected `lv_input_voltage`, range, AC/DC, mode, drive current and `lv_driver_type`/note beside LV watts. Capture source evidence during M2 and resolve selected interfaces/product limits before affected M4 grouping. Existing type/light/channel source references and confirmed engineering decisions retain provenance.

## Constraints and Validation

- Contradictory entered voltage ranges/nominal values fail all phases. Positive nominal/max voltage and drive current are schema constraints; null is the unknown value.
- Unknown selected driver architecture defers at intake and blocks the design phase. `other` without an explanatory note is structurally incomplete at every phase. Unknown original source architecture can remain unknown when the selected replacement is independently verified.
- Selected CV inputs need confirmed AC/DC and fixed nominal voltage. Used CV channels need a selected fixed output setting; an adjustable product range alone is not a confirmed setting. `input_current_ma`/`output_current_ma` are CC setpoints, so they remain null for CV. Output current capacity is separate product evidence, not this setpoint field.
- Direct selected CV input and channel voltage/mode/AC-DC must match. A 12 V CV light and a 24 V CV light cannot share the same direct output merely because their combined watts are below its limit. Matching compatibility-group text does not bypass these numeric checks.
- Selected CC inputs need drive current and their supported operating voltage range. A used CC channel needs a current setpoint and compliance range. For one modeled input, current/mode/AC-DC must match and the entire required voltage range must fit within the channel range. A nominal voltage or watt value alone is insufficient.
- More than one modeled light on a CC output raises `cc-topology-review` and blocks the v0.5 design phase: series/parallel/current-sharing or downstream-interface topology is not modeled by this extension. This is an implementation limit, not a claim that all such arrangements are prohibited. Do not split/duplicate physical runs to bypass it. Retain the proposed arrangement for engineering review and a future explicit contract if needed.
- Unknown selected interfaces and incompatible proposed assignments are deferred at inventory/intake and block affected full design checks. Unknown original source voltage does not automatically block a separately verified LV replacement interface. No selected voltage/current is inferred from source watts or channel settings.
- Voltage compatibility supplements existing load, class/profile, dimming/control, controller-output, aggregate-capacity, source/approval and emergency checks. Matching electrical fields does not certify a product or prove coverage, wiring topology, input-current capacity, dimming compatibility or controller switching ratings.

Separate compatible load groups first, then apply watt budgets and independent functional-control requirements. Channel count can increase when compatible voltage/mode groups differ, even below the watt ceiling. Controller count depends on actual compatible output capacity and required independent operation; it is not automatically equal to supply-channel or voltage-group count. The current tools check entered assignments and do not optimize grouping or select hardware.

## Migration and Compatibility

`python -m generators.model_intake OLD_MODEL --upgrade-output NEW_MODEL --phase intake` explicitly copies v0.3/v0.4 to v0.5, preserves IDs, source facts, zones and numeric precision, and fills new fields as unknown. It refuses to overwrite an existing output and does not copy channel voltage into selected-light voltage. Populate supported fields through project review. Source-review export accepts v0.5, v0.4 and read-only v0.3; older inputs receive blank new columns.

Older schemas/checks/examples remain unchanged. Their reports identify `electrical_interface_checks_available: false`; a legacy pass does not prove the added voltage/current checks. The v0.5 checker evaluates the new electrical fields, then uses a temporary legacy projection for inherited engineering checks without mutating the original model or discarding its evidence. The previously agreed M3 review-status attributes are still not implemented by this voltage extension.

## Sources and Stewardship

Owner-directed source-voltage restoration and channel-compatibility requirement, October 2026; synthetic v0.5 tests exercise matching/mismatching fixed voltages, AC/DC, modes, CC setpoints/ranges, unknowns, upgrade precision and retained legacy checks. [MEAN WELL LED application guidance](https://led.meanwell.com/qa.aspx?c=9) supports distinguishing CV input/driver arrangements from CC current and combined forward-voltage ranges; use verified selected-product documents for project limits. Reusable manufacturer/device facts remain owned by WikiJS. This page defines entered-data rules, not a product certification or code interpretation. Owner: KIS Solutions; draft pending project review.
