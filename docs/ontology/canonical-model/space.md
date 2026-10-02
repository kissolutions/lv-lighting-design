---
title: "Space"
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

# Space

## Purpose and Scope

A room or bounded area that supplies context for controls and grouping.

## Fields and Meaning

Location: `facts.spaces[]`

`id`, `name`, `drawing_page_ids`, `source_ref_ids`.

## Relationships

Owns control zones by ID; fixtures retain a `space_id`. A space can appear on multiple pages.

## Constraints and Validation

Do not infer control behavior from room shape alone. Check zone/fixture space consistency and repeated drawing coverage.

## Sources and Stewardship

Derived from the October 2026 LV lighting handoff; field shape and validation details are draft implementation decisions. Owner: KIS Solutions. Validate against one real project before treating this contract as stable.
