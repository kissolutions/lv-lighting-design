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

In [v0.3](space-context-v0.3.md), Spaces reference their existing zones. A whole-room zone has a stable internal ID even when no distinct drawing label is used (`label_mode: room_default`). Named zones may display labels such as `$z109` and record their control area/basis. Space membership derives from explicit Space zone references, cross-checked against each light's primary served Space; legacy `space_labels` text is presentation context.

A reviewed named zone may span multiple rooms or levels. Preserve the specified stair-control scheme; the one-zone-per-physical-stair convention applies only when documented behavior and reviewed independent-control requirements support common operation, whether using one Space or separate level records. Describe shared operation and preserve source constraints/emergency behavior; conflicting independent-control requirements require discussion before finalizing a split or common zone. Do not duplicate a physical light across floor rows. Review room-to-zone associations before assigning channels/controllers.

Location: `light_zones[]` in the draft v0.2 model.

Owns its light objects and records their functional operation: primary controller/output, dimming capability, multiple control types, on/off strategy, normal behavior, egress role, emergency response/input, and shared source schedule groups. Total watts and power-channel membership are derived. A zone may use multiple power channels; it preserves one independent control path in this draft.

This is the LV functional grouping implementing the extracted MEP control scheme or an approved departure. MEP ZONE 1-4 remain separate source design intent and constraints, referenced through `control_group_ids`; their labels alone do not determine internal identity, controller output, or power channel. Review LV operation against those requirements and flag conflicts or proposed deviations. Preserve source intent while checking it through WikiJS; missing instructions are not filled with a preferred design.

## Agreed Review Attributes Awaiting Implementation

The owner has agreed to `control_verification_status` with values `not_reviewed`, `compliant`, `deficient`, `ambiguous_source`, `no_information`, and `implementation_review_status` with values `not_reviewed`, `typical_design`, `manual_review_required`. These are not yet fields in the v0.3/v0.2 schemas or checks. Keep findings and evidence in the project review record without inserting unsupported keys. See [review meanings and workflow](../../design-playbooks/lv-project-workflow-and-readiness.md#control-review-results).

Retain per-function occupancy/daylight/manual/scheduling findings where needed. The assessment/evidence structure, overall summary precedence, source-versus-applied sequence fields and approval/change record need a subsequent versioned model extension. A deficient zone requires manual review; a compliant one can still have an implementation proposal. Approval of a change is separate from both review statuses and from the model's confirmed decision status.

The [device hierarchy contract](device-hierarchy-v0.2.md) defines fields, ownership, derived views, validation scope, and migration boundaries. The [v0.2 schema](../../../schemas/lighting-project-v0.2.schema.json) is the executable data shape. Unknown fields remain `null`; relevant source references and engineering decisions remain explicit. Owner: KIS Solutions; October 2026; draft.
