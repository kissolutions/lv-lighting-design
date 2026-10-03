---
title: "LV Fixture Selection"
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

# LV Fixture Selection

This page records the v0.1 baseline. For current ownership and relationships, read [Device Hierarchy v0.2](device-hierarchy-v0.2.md). The v0.1 tools retain their original contract; new hierarchy data uses the dedicated v0.2 schema/checker.

## Purpose and Scope

Selected LV interpretation of a source fixture type.

## Fields and Meaning

Location: `design.fixture_selections[]`

`id`, `fixture_type_id`, `lv_description`, nullable `lv_input_watts`, nullable `compatibility_group`, `status`, `source_ref_ids`, `decision_id`.

## Relationships

One selection per included source type. Feeds channel load and compatibility checks.

## Constraints and Validation

Verify load at the channel output/interface; source AC watts are not an automatic substitute. Compatibility groups capture confirmed output/driver, dimming/control, and other grouping restrictions. Unknown/provisional selections block checks.

## Sources and Stewardship

Derived from the October 2026 LV lighting handoff; field shape and validation details are draft implementation decisions. Owner: KIS Solutions. Validate against one real project before treating this contract as stable.
