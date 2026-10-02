---
title: "Power Node"
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

# Power Node

## Purpose and Scope

One explicit physical power/control hardware unit for quantity purposes.

## Fields and Meaning

Location: `design.power_nodes[]`

`id`, `label`, `device_class`, nullable `drawing_page_id`/`drawing_anchor`, nullable `capacity_channels`/`aggregate_design_limit_watts`, `source_ref_ids`, `decision_id`.

## Relationships

Supplies assigned channels. Count physical node records by selected device class; check channel count and aggregate LV load separately.

## Constraints and Validation

Capacity evidence must be verified. Do not assume nominal per-output ratings establish aggregate capacity. A combined power/control unit is one power node; avoid adding a duplicate control node for the same unit. Locations may be pending in Phase 1.

## Sources and Stewardship

Derived from the October 2026 LV lighting handoff; field shape and validation details are draft implementation decisions. Owner: KIS Solutions. Validate against one real project before treating this contract as stable.
