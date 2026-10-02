---
title: "Control Node"
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

# Control Node

## Purpose and Scope

A separately counted physical controls unit when required by the selected architecture.

## Fields and Meaning

Location: `design.control_nodes[]`

`id`, `label`, `device_class`, nullable `drawing_page_id`/`drawing_anchor`, `source_ref_ids`, `decision_id`.

## Relationships

Complements power nodes. This version counts explicit records but does not model controls-network capacities or topology.

## Constraints and Validation

Create only known separate units; an empty collection is legitimate for combined hardware. Product functions and capacity need project engineering review.

## Sources and Stewardship

Derived from the October 2026 LV lighting handoff; field shape and validation details are draft implementation decisions. Owner: KIS Solutions. Validate against one real project before treating this contract as stable.
