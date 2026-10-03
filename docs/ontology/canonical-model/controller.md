---
title: "Controller"
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

# Controller

Location: `controllers[]` in the draft v0.2 model.

Records physical controller identity, confirmed independent control-output capacity, optional integrated power unit, control devices, emergency inputs, and control-power backup. Connected zones are derived from their controller/output references. A typical four-output aggregated controller is a convention to verify against actual equipment; supply channels and control outputs are distinct objects.

The [device hierarchy contract](device-hierarchy-v0.2.md) defines fields, ownership, derived views, validation scope, and migration boundaries. The [v0.2 schema](../../../schemas/lighting-project-v0.2.schema.json) is the executable data shape. Unknown fields remain `null`; relevant source references and engineering decisions remain explicit. Owner: KIS Solutions; October 2026; draft.
