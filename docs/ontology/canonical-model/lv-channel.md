---
title: "LV Channel"
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

# LV Channel

This page records the v0.1 baseline. For current ownership and relationships, read [Device Hierarchy v0.2](device-hierarchy-v0.2.md). The v0.1 tools retain their original contract; new hierarchy data uses the dedicated v0.2 schema/checker.

## Purpose and Scope

A design assignment to one power/control output.

## Fields and Meaning

Location: `design.lv_channels[]`

`id`, `control_zone_id`, `fixture_ids`, nullable `power_node_id`, `nominal_rating_watts` (100), `design_limit_watts` (>0 and <=90), `compatibility_group`, `decision_id`.

## Relationships

Groups occurrences in one effective zone and one confirmed compatibility group. Belongs to a physical power node for quantified design.

## Constraints and Validation

Sum selected LV watts using exact decimal comparisons. Four 20 W fixtures = 80 W. Exactly 90 W passes; any value above the chosen limit fails. Store assignments, derive connected watts. This initial baseline has no cross-zone exception.

## Sources and Stewardship

Derived from the October 2026 LV lighting handoff; field shape and validation details are draft implementation decisions. Owner: KIS Solutions. Validate against one real project before treating this contract as stable.
