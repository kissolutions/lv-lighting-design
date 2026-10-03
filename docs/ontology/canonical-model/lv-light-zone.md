---
title: "LV Light Zone"
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

# LV Light Zone

Location: `light_zones[]` in the draft v0.2 model.

Owns its light objects and records their functional operation: primary controller/output, dimming capability, multiple control types, on/off strategy, normal behavior, egress role, emergency response/input, and shared source schedule groups. Total watts and power-channel membership are derived. A zone may use multiple power channels; it preserves one independent control path in this draft.

This is our designed LV control grouping. MEP ZONE 1-4 remain separate source design intent and constraints, referenced through `control_group_ids`; they do not determine this zone's identity, controller output, or power channel. Review the LV operation against those requirements and flag any conflicts or proposed deviations.

The [device hierarchy contract](device-hierarchy-v0.2.md) defines fields, ownership, derived views, validation scope, and migration boundaries. The [v0.2 schema](../../../schemas/lighting-project-v0.2.schema.json) is the executable data shape. Unknown fields remain `null`; relevant source references and engineering decisions remain explicit. Owner: KIS Solutions; October 2026; draft.
