---
title: "Cable Route"
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

# Cable Route

## Purpose and Scope

Reserved Phase 2 projected route geometry and channel membership.

## Fields and Meaning

Location: `design.cable_routes[]`

`id`, `drawing_page_id`, `points` (at least two), `channel_ids`, `decision_id`.

## Relationships

References channels and a displayed drawing page. It is subordinate to reliable fixture/node placement.

## Constraints and Validation

Leave empty in the initial Phase 1 project. Only references and point bounds are checked. No cable type, endpoint topology, bundle quantities, drawing-scale calibration, or installed length is validated or exported yet.

## Sources and Stewardship

Derived from the October 2026 LV lighting handoff; field shape and validation details are draft implementation decisions. Owner: KIS Solutions. Validate against one real project before treating this contract as stable.


## Physical allocation extension

The [topology companion](controller-power-topology-v1.md) links existing IDs to QDCD/CIO/SW/PDU devices, sensor/port/control associations, supply feeds, locations and bus routes. Validate separately from electrical model checks.
