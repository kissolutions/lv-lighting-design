---
title: LV Visual-Spatial Extraction and Light Point Markup
page_type: playbook
page_status: draft
confidence_level: medium
domain_primary: low-voltage-lighting
ai_role: prescriptive_standard
invocation_triggers:
  systems_present: [low_voltage_lighting]
  uncertainty_flags: [room_extraction, light_point_extraction, cross_drawing_transfer, spatial_discrepancy]
decision_axes: [visual_completeness, light_anchor, markup_readability, coordinate_registration, owner_review]
related_pages:
  - https://github.com/kissolutions/knowledgebase_wikijs/blob/a5616fa089d94c824551997a9fa9a14c9a4d3a58/design-playbooks/drawing-spatial-extraction-v0.1.md
  - phase-1-intake-process-map-v0.2.md
  - architectural-space-intake.md
  - m2-fixture-numbering.md
  - milestone-review-packages.md
---

# LV Visual-Spatial Extraction and Light Point Markup

## 1. Purpose and Use

Apply the parent [Drawing-Based Spatial Extraction and Verification v0.1](https://github.com/kissolutions/knowledgebase_wikijs/blob/a5616fa089d94c824551997a9fa9a14c9a4d3a58/design-playbooks/drawing-spatial-extraction-v0.1.md) to M1 Rooms/Light Points, M2 fixture reconciliation and later drawing-derived device/route handoffs. This page owns LV presentation and milestone evidence, not a new canonical schema or automated extractor. Revision: 2026-10-25. Shared method pinned to parent commit `a5616fa`; its review branch need not be merged for these links to resolve.

## 2. Design Intent

**AI performs the heavy extraction work. Human review makes it authoritative within the stated review scope.** Prepare a substantially complete first pass using rendered drawings, PDF data, geometry, legends/schedules and project records together. The owner reviews and corrects; owner-first markup remains an available chosen path. Agent-generated renders/crops are the normal visual reference. Owner screenshots are optional targeted clarification, not a standing prerequisite or substitute for agent visual inspection.

## 3. Space / System Definition (Decision-Oriented)

Architectural-first Space authority, served levels, smallest-containing membership, scope and physical-section/source-run rules remain unchanged. A Light Point's approved display label, immutable Light Object ID, source observation identity and annotation IDs are distinct. A visible light symbol/observation does not by itself establish a manufactured section, feed or channel count. Apply [M2 identity and scheduling](m2-fixture-numbering.md) and [assembly/count reconciliation](m1-m2-beta-review.md).

## 4. Constraint Envelope

### 4.1 Hard Constraints

Render and visually inspect every applicable in-scope lighting plan/RCP and architectural view. PDF extraction assists precision but cannot substitute for visual interpretation. Preserve source facts, approved M1 names, accepted owner geometry, editable annotations and persistent identities.

### 4.2 Soft Constraints

Default visible Light Point label font is **4 pt at native PDF page scale**. Inspect the saved markup at a stated intended review/print scale and useful detail zoom; if illegible or obscuring source information, document a scoped size/offset adjustment or owner direction. Do not silently change font settings. Marker size is a small legible presentation choice, not a newly fixed dimension.

### 4.3 Hidden Constraints

Label boxes, circle outlines and source fixture envelopes have different geometry. Text movement must not relocate the physical point. Source plans and returned working PDFs can have different crops/rotations and must be registered before coordinates are combined.

## 5. Baseline / Default Design Pattern

1. **Interpret and extract.** Visually establish every reasonably discernible in-scope Space and Light Point. Use PDF/vector/text discovery and source legends/schedules for precision and meaning. Do not omit a point because it is not a convenient standalone PDF object.
2. **Check Space completeness.** Compare the rendered architectural view and generated footprints for missing/extra areas, untagged pockets, circulation, gaps/overlaps and served-level relationships, using the independent architectural inventory method.
3. **Check lights by Space.** Establish apparent count, arrangement, source-symbol locations and ambiguities visually. Reconcile individual observations/points with the register/model and saved markup; check omissions, duplicates, displaced points and incorrect membership even when totals match. Before reviewed Spaces exist, perform preliminary checks by source area, then repeat by Space after association.
4. **Prepare editable output.** Use the anchor/label contract below. Render the actual saved/assembled PDF and inspect the overlay against its source; inspect source linework beneath annotations when necessary.
5. **Reconcile owner return.** Preserve returned anchor/boundary geometry, review scope and provenance. An instruction such as “take my circle locations as truth” makes those anchor locations authoritative for that scope; do not snap them back to prior fixture centers. Preserve source coordinates separately and flag new conflicts.

## 6. Typical Variants

### Light Point anchor and label

- Show a **small circular anchor marker plus only the approved Light Point ID/label**, for example `○ L-02`. Preserve existing approved formats/owner label overrides; this example does not authorize renumbering.
- **Circle center = canonical drawing anchor.** Initially place it at the depicted fixture center, or a source-defined reference/connection point where required. For a linear run, use its identified midpoint on the path unless another source-defined anchor applies; do not use an off-path bounding-box center for a bent run. Retain the full source path/envelope separately.
- Put the 4 pt label immediately adjacent, with a documented offset/leader where needed for readability. No room/type/wattage/status text is appended to the base Light Point label. Separate milestone graphics such as M4 QDCD output tags, M3 subzone suffix annotations and channel wattage callouts retain their own contracts.
- Circle and label remain editable. Prefer a live circular `/Circle` annotation and separate `/FreeText` label with a nonempty saved appearance, each with its own persistent `/NM`, both linked to the same Light Object/observation. Another representation requires demonstrated equivalent edit/readback behavior. A typed circle inside a movable text box alone does not establish an independently maintained anchor.
- **Label-only movement changes presentation, not the anchor.** Anchor movement updates canonical position only through the reviewed return/reconciliation loop. Preserve identities on moves; do not identify objects by label proximity alone. If both annotations move, reconcile their roles separately.
- Containment, naming order for a new sequence, zoning, channel-chain association and routing use the **anchor**, never text-box coordinates. Moving an already named point does not automatically renumber it or silently change its approved associations.

### Cross-drawing transfer

Use the parent's distributed architectural registration and separate post-transfer object check before bulk mapping between source and working views. Retain original source anchors, source/target page/view/frame and transformed target anchors separately, with the transformation evidence. Inspect opposite/extreme parts of the mapped area and room-by-room semantic correspondence afterward. Use controls independent of the transferred lights; the lights then help verify the result. A correct transform cannot prove that six intended lights landed in the correct Space.

## 7. Decision Gates

On any count/location/association discrepancy, inspect a focused rendered source/markup crop **before another corrective data pass**. Resolve the physical interpretation first, then edit coordinates/register records. If unclear, carry an explicit finding and request focused clarification. This replaces repeated data-only correction loops.

Before presenting an M1 Light Point package, visually compare every in-scope Space. Before accepting its Light Point inventory, reconcile the comparison or explicitly identify pending Space/object scope and the downstream effect. Recording a discrepancy does not make the affected points complete or accepted. The owner may partially accept unaffected scope; no global stop or extra approval per room is introduced. M1 room/boundary acceptance and Light Point acceptance remain separately scoped.

M2 repeats affected visual checks after schedule/assembly interpretation, split/merge, source revision or owner correction; preserve original M1 observation/approval history. M2 may explain why apparent source marks and physical fixture totals differ without silently replacing the earlier observations.

## 8. Design Zoning / Grouping Strategy

Review per primary served Space/level and check sheet/area transitions. Preserve architectural boundaries, assembly relationships and explicit exterior/scope holdouts. Visual grouping does not create a functional control zone or electrical channel.

## 9. Common Failure Modes

- Six source lights and six records that conceal one missed light and one duplicate.
- A displaced label mistaken for the point used in containment or routing.
- Correct page coordinates applied to an unregistered owner-returned crop/frame.
- Recreating an owner-rejected location or omitting readily discernible lights for manual owner digitizing.

## 10. Safe Assumptions (and Limits)

Approximate initial anchors/boundaries remain proposals where source precision is limited. Preserve unknown types, count interpretations and associations; visual presence does not establish electrical facts or compliance. An explicitly accepted owner position takes precedence over the default center placement for that scope.

## 11. Documentation Expectations

Keep additional fixture information in annotation metadata/properties/comments or a linked persistent record: source type, served Space, load, emergency classification, source/revision locator, canonical/source observation identity, review/reconciliation status and notes as available. Do not fabricate unknown values. Verify saved metadata and identity survive the actual editing/saving/reopening workflow; critical linkage must remain recoverable from annotation `/NM` and the register.

Maintain a lightweight comparison in private project review evidence, for example:

| Space ID | Source sheet/revision or crop | Apparent source points | Registered points | Arrangement/location check | Result / finding |
|---|---|---:|---:|---|---|
| SPACE-EXAMPLE | SYNTHETIC-01 / A | 6 | 6 | Each source position matched | PASS |

This row is synthetic. Include review scope/reviewer and markup revision. Use unknown/ambiguous rather than invented numeric counts, and note zero-light Spaces, holdouts and count-basis differences explicitly. Visual counts may remain verification artifacts instead of new canonical fields. Preserve registration evidence for cross-view work.

## 12. When to Go Deeper / Exit This Playbook

Unresolved source symbols, count/assembly meaning, served levels, owner/source conflicts or registration distortion need focused review. Keep unaffected work moving; affected inventory/design retains its pending status. Preserve accepted configuration and propose scoped reopening when needed.

## 13. Cross-Links to Supporting Knowledge

- [Shared drawing extraction method](https://github.com/kissolutions/knowledgebase_wikijs/blob/a5616fa089d94c824551997a9fa9a14c9a4d3a58/design-playbooks/drawing-spatial-extraction-v0.1.md)
- [Architectural intake](architectural-space-intake.md), [Phase 1 process map](phase-1-intake-process-map-v0.2.md), [M2 identity](m2-fixture-numbering.md)
- [Milestone packages](milestone-review-packages.md), [markup legend](control-system-markup-legend.md), [live annotation/register checks](m1-m2-beta-review.md#live-annotations-and-register-gate)

## 14. Status and Stewardship

- **Status:** Draft documented execution/presentation method; owner-reviewed integration of proposals 001–010.
- **Owner / review:** KIS Solutions / 2026-10-25.
- **Software limits:** No schema change is introduced. Existing markup PDF validation checks structure and IDs, not font size, marker centering, metadata completeness, visual inventory, transform accuracy or semantic correspondence. A separate marker can use existing register role `other`, linked to the same light; this checks its identity/presence, not circular shape or location. `light_label` retains its `/FreeText` rule. Do not add unsupported manifest properties or claim automatic anchor/label-return reconciliation. Retain additional role/frame/transform evidence in project records until a versioned implementation exists.
- **BETA verification still required:** On a synthetic mixed-symbol room pair, demonstrate source/target registration, omission-plus-duplicate detection, independent label/anchor edits, both annotations' ID/metadata readback and preservation of the owner-returned anchor. Check 4 pt legibility at the intended scale. Do not claim this proof from passing repository tests.

## 15. Author Notes (Institutional Context)

Consolidates owner-reviewed active proposals 001–010 without publishing real project records. The parent method owns reusable evidence/review behavior; this extension owns Light Point presentation and its M1/M2 application. It does not change approved numbering, fixture-count definitions or the later electrical design contract.

| Proposal | Integrated rule / refinement |
|---|---|
| 001 | ID-only base label; additional facts in metadata/linked persistent records; saved identity/readback required |
| 002 | 4 pt native-scale default, with recorded scoped legibility adjustment rather than an unconditional size |
| 003 | Editable circular canonical anchor distinct from label position; owner-returned geometry preserved |
| 004–006 | Rendered visual extraction, focused discrepancy review before further correction, and per-Space count plus individual correspondence evidence; pending scope remains explicit |
| 007–009 | Shared visual/geometric registration and separate object/semantic handoff checks; transferred objects may verify the result but are not the sole registration fit/check basis |
| 010 | AI-led complete first pass, human review/correction/acceptance, optional owner-first path and preservation of accepted corrections |
