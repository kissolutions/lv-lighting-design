---
title: "Source Control Intent and Constraints"
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

# Source Control Intent and Constraints

Location: `control_groups[]` in the draft v0.2 model.

The existing `control_groups[]` name denotes source control intent and constraints, not KIS-designed LV control groups. MEP labels such as ZONE 1-4 belong here as preserved source requirements. Their labels, schedule/override intent, and source references remain separate from our LV light-zone IDs and controller-output assignments.

Local LV zones reference the applicable source intent through `control_group_ids`. Several independently controlled LV zones may implement the same MEP requirement. Source membership never creates an LV zone, selects a controller output, or assigns a power channel by itself.

During design review, verify that each applicable MEP requirement is satisfied by the proposed LV operation. Record any conflict, proposed deviation, or missing interpretation as an engineering decision and, where clarification is needed, an open item/RFI. Preserve the original source requirement rather than rewriting it to match our design. The current checker validates references; interpreting and verifying the source constraints remains a human review step.

The [device hierarchy contract](device-hierarchy-v0.2.md) defines fields, ownership, derived views, validation scope, and migration boundaries. The [v0.2 schema](../../../schemas/lighting-project-v0.2.schema.json) is the executable data shape. Unknown fields remain `null`; relevant source references and engineering decisions remain explicit. Owner: KIS Solutions; October 2026; draft.
