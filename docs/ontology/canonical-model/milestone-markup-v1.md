---
title: "Milestone Markup and Review Manifest v1"
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

# Milestone Markup and Review Manifest v1

## Contract

[Schema](../../../schemas/milestone-markup-v1.schema.json) · [Seed](../../../templates/milestone-markup-v1.template.json). The manifest pairs project/model revision with deliverable PDF revisions and stable annotations; it is separate from physical lighting ownership and topology assignments.

`packages[]` identifies the six deliverable kinds, printable schedule page count, plan page IDs, filename, annotation IDs, review status and actual edit/save/readback verification. Accepted packages require a concrete PDF filename and verified readback. Record page counts after actual PDF assembly; do not invent them from HTML tables.

`annotations[]` stores immutable annotation ID, linked entity kind/ID, visible tag, exact final layer, drawing page, location/review basis, room/zone associations, position and enveloped boundary style. Coordinates use the displayed page after crop/rotation, matching existing project conventions. Boundary geometry remains in the editable PDF; x/y is an anchor, not a complete polygon. Parent/child zone identity comes from the lighting model.

Prefer PDF `/NM` as stable annotation identity, a readable Subject identifying tag/device type and structured Comments containing manifest version, entity ID, project/revision and room/zone associations. Preserve these through owner moves. Layer membership requires actual PDF optional-content support; annotation properties alone do not establish layers. If an editor strips IDs/metadata, reconcile explicitly using the retained manifest and owner review; never silently rematch by proximity.

Owner-returned location revisions update topology and annotation review basis together after owner corrections are read. Multiple symbol/text annotations can reference one Device ID with distinct annotation IDs; they do not create extra devices. Keep labels linked to the same device when a symbol moves. `room_center_provisional` and `reasonable_equipment_proposal` must not remain the location basis of an accepted device.

## Check and Export Scope

`generators.milestone_markup.validate_manifest` checks IDs, references, layer/category agreement, narrative dependency, envelope styling and acceptance/readback flags. `render_order` and `calculated_label` are formatting helpers, not PDF editing operations. `export_schedules` emits schedule CSVs and printable HTML front sheets; it does not generate PDF plan annotations. Do not claim a layered PDF or successful human readback from manifest validation alone.
