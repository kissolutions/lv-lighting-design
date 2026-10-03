---
title: "HV-to-LV Power Unit"
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

# HV-to-LV Power Unit

Location: `branch_circuits[].power_units[]` in the draft v0.2 model.

Owns its output channels. Records input voltage/phases, LV output power type, separate input/output ratings, confirmed design input load, aggregate output design budget, channel capacity, connected controls, and backup provision. Connected output watts and served light/zone lists are derived through channels. Physical integrated controls are referenced rather than counted twice.

The [device hierarchy contract](device-hierarchy-v0.2.md) defines fields, ownership, derived views, validation scope, and migration boundaries. The [v0.2 schema](../../../schemas/lighting-project-v0.2.schema.json) is the executable data shape. Unknown fields remain `null`; relevant source references and engineering decisions remain explicit. Owner: KIS Solutions; October 2026; draft.
