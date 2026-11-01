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

## Beta Delivery Gate

In an active room-boundary step, room footprints use live Polygon annotations; active light labels use FreeText with nonempty appearance streams. Included earlier frozen-step components are flattened references, not missing live annotations. Every active annotation ID maps through the current step's delivered CSV register. Use `generators.validate_markup_pdf` against the saved PDF. The v1 manifest remains unchanged; its anchors do not substitute for actual Vertices or page-frame evidence. See [beta workflow and scoped Bluebeam proof](../../design-playbooks/m1-m2-beta-review.md).

## Current-step editability and frozen references

Current-step working markup remains live, editable and unlocked, with stable identity and linked records. All included markup from earlier frozen steps is flattened in the downstream copy, retaining defined properties/layer behavior and the separate frozen source/live master. Review completion does not authorize destroying that source. Verify inherited reference appearance/popups and current-step annotation editability separately; layers alone prove neither. Do not use rasterization or print-to-PDF that loses required metadata. See the [current presentation contract](../../design-playbooks/markup-deliverable-presentation-contracts.md#frozen-prior-steps-and-current-step-editing) for composition, source reopening and scoped annotation-register rules.

The saved-PDF annotation/register checks apply to final assembled packages as well as intermediate reviews. Existing validation covers its documented scope; do not infer editability of every annotation type solely from a nonzero annotation count.

The unchanged v1 manifest and strict live-PDF checker do not automatically distinguish flattened reference graphics or viewer-created popup annotations. Keep frozen component source/revision mappings in the assembly record, and scope live annotations to the active step. Do not add unsupported schema fields or ignore unexplained live annotations merely to obtain a pass. Inherited popup/layer verification is separate from the current live edit/readback gate.
