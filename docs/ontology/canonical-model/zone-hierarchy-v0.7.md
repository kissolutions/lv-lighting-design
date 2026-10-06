---
title: "Zone Hierarchy and Narrative Review v0.7"
page_type: canonical_model
page_status: draft
confidence_level: medium
domain_primary: low-voltage-lighting
ai_role: model_contract
invocation_triggers:
  systems_present: [low_voltage_lighting]
decision_axes: [milestone_review, zone_hierarchy, markup_identity, owner_review]
related_pages:
  - "https://github.com/kissolutions/lv-lighting-design/blob/main/docs/design-playbooks/milestone-review-packages.md"
---

# Zone Hierarchy and Narrative Review v0.7

## Contract

[Schema](../../../schemas/lighting-project-v0.7.schema.json) · [Seed](../../../templates/lighting-project-v0.7.template.json). v0.6 fixture electrical data and physical light ownership remain unchanged. `generators.model_zone_hierarchy.upgrade_v07` copies older supported models, preserves IDs and inserts null parent IDs plus unreviewed narrative status; it does not guess hierarchy or lock a narrative.

Every zone has nullable `parent_zone_id`. A zone referenced as a parent is a named container, has no editable `light_object_ids`, and derives descendant light membership. Children retain their independent lights/output behavior. Reject unknown parents, cycles, parent/child duplicate ownership and physical channel/output assignments to parent containers. Space zone lists may include parent IDs for navigation, but leaf membership remains authoritative.

Optional `control_narrative` records approved behavior; `occupancy_aggregation` captures any-child, all-children or other approved logic. Do not default to a mode merely from an open-office label. Shared wall controls and sensor/zone associations remain in topology `control_connections`, including parent associations. Do not duplicate physical sensor records across children.

Project `controls_narrative_review` has status unreviewed/draft/locked and a decision ID. Locked requires a confirmed owner-review decision and recorded narrative for every existing zone; this explicit review status records the owner's adoption and is not inferred from validator success. Hierarchy can be recorded before locking.

## Validation and Derived Views

`generators.model_intake` accepts v0.7. It checks hierarchy, then projects leaf records into the v0.6 electrical checks, preserving original input. Parent views derive membership without adding load to branch/channel totals. A parent is a logical container, not an additional lighting load or driver. Existing v0.6 schemas/templates/checks remain available.

The milestone exporter reports zone/child/room associations and requires narrative lock before the device review stage. Use [review packages](../../design-playbooks/milestone-review-packages.md).
