---
title: "HV Branch Circuit"
page_type: canonical_model
page_status: draft
confidence_level: medium
domain_primary: low-voltage-lighting
ai_role: model_contract
invocation_triggers:
  systems_present: [low_voltage_lighting]
decision_axes: [device_hierarchy, source_traceability]
related_pages:
  - "device-hierarchy-v0.2.md"
---

# HV Branch Circuit

Location: `branch_circuits[]` in the draft v0.2 model.

Owns selected HV-to-LV power units. Records source/selected panel and circuit identity, operating voltage/phases, breaker rating when known, and optional backup provision. Derived lighting input watts sum the confirmed input-load basis of those units. Original circuit labels on fixtures remain preserved source observations. Branch sizing, PF, inrush, diversity, and other non-lighting loads require separate project checks.

The [device hierarchy contract](device-hierarchy-v0.2.md) defines fields, ownership, derived views, validation scope, and migration boundaries. The [v0.2 schema](../../../schemas/lighting-project-v0.2.schema.json) is the executable data shape. Unknown fields remain `null`; relevant source references and engineering decisions remain explicit. Owner: KIS Solutions; October 2026; draft.
