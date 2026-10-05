---
title: "Fixture Capability vs Zone Requirement"
page_type: validation_rule
page_status: draft
confidence_level: medium
domain_primary: low-voltage-lighting
ai_role: prescriptive_gate
invocation_triggers:
  systems_present: [low_voltage_lighting]
decision_axes: [fixture_selection, controls, channel_grouping]
related_pages:
  - "electrical-compatibility.md"
  - "../ontology/canonical-model/m4-electrical-attributes-v0.6.md"
  - "../concepts/micro-lv-control-channels.md"
---

# Fixture Capability vs Zone Requirement

## Pass conditions

- A dimmable selected fixture/interface may serve a zone that does not require dimming.
- The fixture retains its physical voltage, AC/DC type, CV/CC mode, current/range, driver architecture and wattage even when a capability is unused.
- Channel assignment continues to use those physical requirements.

## Block conditions

- A zone requiring dimming is assigned a selected fixture/interface confirmed as non-dimmable.
- The model changes a fixture's physical electrical attributes merely to conform to a simpler zone narrative.
- An occurrence is given materially different physical characteristics without a distinct selected fixture type/variant and traceable decision.

## Required iterative check

After control narratives are established and before final micro-channel grouping:

1. Read the zone's required behavior.
2. Read each selected fixture's physical capability and interface.
3. Verify the fixture can meet the required behavior.
4. Preserve all physical electrical attributes regardless of unused capability.
5. Group only after electrical and functional compatibility are both satisfied.

The C1 Alcove case is the reference example: 36 VDC CC dimmable C1 remains C1 when the zone uses on/off behavior only.

Owner: KIS Solutions. October 2026; draft pending YMCA M4 validation.
