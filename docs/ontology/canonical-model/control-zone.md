---
title: "Control Zone"
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

# Control Zone

## Purpose and Scope

A source-defined or confirmed required room/area micro-zone.

## Fields and Meaning

Location: `facts.control_zones[]`

`id`, `label`, `space_id`, `intent_status`, `source_ref_ids`.

## Relationships

Fixtures preserve `source_control_zone_id`. Design zone corrections are separate records. Several channels may serve one zone.

## Constraints and Validation

Unknown intent blocks included fixtures. Daylight/manual/occupancy/dimming distinctions remain separate whenever the source requires them. This version cannot authorize cross-space shared channels.

## Sources and Stewardship

Derived from the October 2026 LV lighting handoff; field shape and validation details are draft implementation decisions. Owner: KIS Solutions. Validate against one real project before treating this contract as stable.
