---
title: "Channel Wattage"
page_type: validation_rule
page_status: draft
confidence_level: medium
domain_primary: low-voltage-lighting
ai_role: prescriptive_gate
invocation_triggers:
  systems_present: [low_voltage_lighting]
decision_axes: [design_validation, channel_wattage]
related_pages:
  - "README.md"
  - "../design-playbooks/lighting-design-playbook.md"
---

# Channel Wattage

This rule describes v0.1 input. The [v0.2 hierarchy](../ontology/canonical-model/device-hierarchy-v0.2.md) defines current nested ownership, class-specific capacity profiles, and independent power/control grouping; its dedicated checker reports the new rules.

## Purpose

Gate Phase 1 design consistency for channel wattage.

## Pass Condition

The selected LV load of every assigned fixture is known and the exact decimal sum is <= the channel design limit, itself >0 and <=90 W for the nominal 100 W baseline.

## Block Condition

Unknown LV wattage, a single fixture too large, a sum over the selected limit, or an attempt to raise the limit above 90 W.

## Implementation and Limits

Implemented in `generators/validate_model.py` and checked with synthetic failure/boundary cases in `tests/`. Exactly 90 W passes; 90.0001 W fails. A verified 80 W design limit must also be honored. Original AC fixture watts are retained but not used automatically.

## Evidence and Stewardship

Basis: October 2026 handoff plus draft model-contract implementation choices. Owner: KIS Solutions. All rule pages remain draft pending a representative project review.
