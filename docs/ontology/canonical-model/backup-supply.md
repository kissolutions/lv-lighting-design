---
title: "Backup Supply"
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

# Backup Supply

Location: `backup_supplies[]` in the draft v0.2 model.

Records a central UPS/battery, fixture battery, or other engineered backup provision separately from the emergency command. Branch, power-unit, light, and controller references describe the provision used. The draft checks reference and declared-verification consistency; actual capacity/runtime, listing, illumination, transfer behavior, and control-path availability remain project engineering work.

The [device hierarchy contract](device-hierarchy-v0.2.md) defines fields, ownership, derived views, validation scope, and migration boundaries. The [v0.2 schema](../../../schemas/lighting-project-v0.2.schema.json) is the executable data shape. Unknown fields remain `null`; relevant source references and engineering decisions remain explicit. Owner: KIS Solutions; October 2026; draft.
