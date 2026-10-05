---
title: "Fixture Type"
page_type: canonical_model
page_status: draft
confidence_level: medium
domain_primary: low-voltage-lighting
ai_role: model_contract
invocation_triggers:
  systems_present: [low_voltage_lighting]
decision_axes: [model_semantics, traceability]
related_pages:
  - "README.md"
  - "../../validation/README.md"
---

# Fixture Type

For the current schedule, use [v0.5 electrical interfaces](electrical-interfaces-v0.5.md). Root `fixture_types[]` retains `source_load` and now has peer `source_voltage` (nominal/range volts and AC/DC), source CV/CC mode/current, voltage-interface basis and notes. Unknown values remain null. The exporter displays source voltage beside source watts. Original source voltage does not establish the selected LV channel-interface voltage.

`source_driver_type` records driver/driverless/other/null with `source_driver_note`; other requires a description. This architecture is independent of power-regulation mode and dimming capability. Preserve original and separately selected LV driver types independently.

This page records the v0.1 baseline. For current ownership and relationships, read [Device Hierarchy v0.2](device-hierarchy-v0.2.md). The v0.1 tools retain their original contract; new hierarchy data uses the dedicated v0.2 schema/checker.

## Purpose and Scope

Original shared schedule facts for one fixture mark.

## Fields and Meaning

Location: `facts.fixture_types[]`

`id`, `type_mark`, `description`, `source_input_watts`, `source_voltage`, `driver_notes`, `source_ref_ids`.

## Relationships

Referenced by each physical occurrence and its separate LV selection.

## Constraints and Validation

Preserve original wattage and driver notes. Missing source wattage may remain null when the LV load is independently confirmed. Duplicate marks must be normalized explicitly.

## Sources and Stewardship

Derived from the October 2026 LV lighting handoff; field shape and validation details are draft implementation decisions. Owner: KIS Solutions. Validate against one real project before treating this contract as stable.
