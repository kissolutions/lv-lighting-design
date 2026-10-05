---
title: "M2 Fixture Display Numbering"
page_type: playbook
page_status: draft
confidence_level: medium
domain_primary: low-voltage-lighting
ai_role: prescriptive_standard
invocation_triggers:
  systems_present: [low_voltage_lighting]
decision_axes: [fixture_identity, schedule_type, room_membership, markup_readability, revision_traceability]
related_pages:
  - "lighting-design-playbook.md"
  - "../concepts/fixture-identity-and-summary-counts.md"
  - "../ontology/canonical-model/light-object.md"
  - "../../templates/m2-user-review-checklist.md"
---

# M2 Fixture Display Numbering

## Purpose and Identity

Use readable per-light display labels during M2 fixture labeling. Group each Fixture Schedule Type line item into one consecutive project-wide numeric block, with same-room/same-type fixtures numbered together in clockwise order starting at the top-left. Room quantity summaries remain useful, but do not substitute for occurrence identification when producing the fixture-ID review PDF.

Store the display number in the existing Light Object `label` field. Keep its permanent internal `id` unchanged; memberships, channels, zones and source/annotation references continue to use that ID. Retain the label-to-ID mapping in review tables and the markup register, and keep the source fixture mark such as A or B1 separately. A display-label revision does not create a new physical light or rewrite source annotations.

## Allocate Type Blocks

1. Reconcile the scoped physical lights, Fixture Schedule Type associations and primary served Spaces before assigning the initial final display sequence. Do not duplicate a light appearing on multiple sheets. Unresolved counts/type associations remain flagged; any working labels affected by those questions are provisional.
2. Use the source fixture schedule's line-item order for the type blocks. Distinct scheduled types/options remain distinct even when their printed marks look similar. If no usable schedule order exists, retain the verified type distinctions, propose a natural mark order such as A, B1, B2, C1, C2, D2, and record that fallback; do not invent a schedule association.
3. Begin at `L001` and continue across the entire agreed labeling scope. Do not restart at each room, floor, sheet or type. Use at least three digits, with a consistent larger width if the total requires it; the sequence is not limited to 999 lights. Do not preallocate unused ranges during the initial reconciled pass.
4. Finish every occurrence of the first type across the scoped Spaces before starting the next type. Within a type block, use the reviewed Room Schedule order consistently, and finish that room's occurrences of the type before moving to the next room. Record the room order if it is not already explicit in the review schedule. A room with no occurrence of that type consumes no numbers.
5. Publish a type-block register with each type's first/last label and count, plus the label-to-internal-ID and primary-room mapping. Room/type subsets should be visibly consecutive within the initial block. Sort individual-light review rows by the numeric display label, retaining type, room, internal ID and source locator.

Synthetic example:

| Source schedule type | Count | Initial display block |
|---|---|---|
| A | 64 | L001–L064 |
| B1 | 18 | L065–L082 |
| C1 | 12 | L083–L094 |

These are presentation sequences, not channel IDs, control groups, LV load groups or quantities inferred from label endpoints.

## Clockwise Within Each Room and Type

Use the accepted upright plan-view orientation: top-left means page top-left in that view, not assumed geographic northwest. Consider only the physical lights of the current type assigned to the current primary served Space. For a linear run, apply [linear extraction](m2-linear-fixture-extraction.md), use its reviewed representative anchor and count the source run once. Connected corners and repeated type labels do not add display numbers; clearly separate runs do. Record ambiguous continuity rather than treating the display path as proof of manufacturing/electrical topology.

Start with the upper-left fixture in the uppermost visible row of that room/type group. For a clear rectangular grid, follow the outer ring clockwise: across the top toward the right, down the right edge, across the bottom toward the left, and up the left edge. Then repeat on the next inward ring until all fixtures are labeled. A single row proceeds left-to-right; a single column proceeds top-to-bottom. These degenerate cases do not require an artificial circular path.

For an obvious nonrectangular perimeter arrangement, follow its visible clockwise path from the upper-left fixture, then handle remaining interior fixtures in successive reviewed groups. For irregular layouts, disconnected parts of one Space, overlapping anchors or ambiguous rows/rings, document a proposed traversal in the markup register and flag it for owner review. Do not invent fixture coordinates, move room boundaries or reorder physical identity to force a neat path. Fixture source location remains tied to its actual sheet; cross-level representations do not duplicate the light.

Top-left selection, row/ring membership and any irregular traversal are display-order decisions, not asserted source facts. Numbering within a room may be reviewed visually without requiring a new geometry object or schema field. A geometry-based automatic numbering algorithm has not been implemented.

## Revisions and Verification

Initial reconciled blocks are consecutive. Before accepting the fixture-label review, verify that each scoped light has one label, labels are unique across the scope, each label maps to one permanent ID, type-block and room-subset counts match the physical takeoff, and the visible clockwise path matches the register. Labels and records on separate PDFs/tables use the same model/review revision.

Keep accepted labels through regrouping, room renaming and unchanged backgrounds. Added/removed lights or corrected type/room associations can disrupt the original blocks. Retain the earlier issue and flag the sequence impact; either keep accepted labels and document the revised/discontinuous blocks, or issue a coordinated display-only renumbering. A renumbered revision includes old-label/new-label/permanent-ID mapping and updates all affected schedules and markups together. Never silently renumber an owner-returned PDF, recycle identity by number or conceal removed occurrences. Review the revised labeling before treating its outputs as reconciled.

The current model supports these labels. The source-review exporter emits `light_label` alongside `light_id` in Light Points and orders numbered labels numerically without altering the model. It does not assign labels, derive clockwise geometry, validate label uniqueness or generate the type-block register; those remain explicit extraction/review tasks. No new source facts, lighting zones or engineering selections are established by numbering.

Owner: KIS Solutions. October 2026; owner-directed M2 display convention.
