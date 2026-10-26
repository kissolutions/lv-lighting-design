---
title: "Phase 1 Intake — Process Map v0.2"
description: "Versioned orchestration of preliminary light-point observation, iterative M1 space markup, and M2 source takeoff"
published: true
tags: [lv-lighting, phase-1, M1, M2, process, pdf-markup]
editor: markdown
---

# Phase 1 — Intake: Process Map v0.2

**Status:** Reconstructed process orchestration for owner review/BETA. Not a declaration that generators automate all steps or that M1/M2 have passed. **Framework:** [KIS Systems Engineering Framework v1.0](https://github.com/kissolutions/knowledgebase_wikijs/blob/main/governance-and-doctrine/systems-engineering-framework-v1.md). **Domain sources:** [Architectural Space Intake](architectural-space-intake.md), [M1/M2 BETA directives](m1-m2-beta-review.md), [Workflow and Readiness](lv-project-workflow-and-readiness.md).

This document defines a **process sequence**, not new milestone names or a new canonical project schema. Existing domain-specific rules prevail for polygons, notches, source precedence, schedules, live PDF marks, and physical fixture section counting. Orchestration revision **v0.2 (2026-10-25)** integrates rendered visual extraction and anchor/label review. Changed source-register, observation, extraction and verification procedures below are v0.2; unchanged owner-return procedures retain v0.1. Separate production implementations/versioned test suites remain to be developed. Apply [visual-spatial extraction](visual-spatial-extraction.md) and its shared parent method; these are supervised requirements, not automation claims.

## Objective and milestones

- **Phase:** 1 — Intake.
- **M1:** Room Inventory and Source Verification; reviewed Space Register, editable boundary markup, independent inventory and discrepancy list.
- **M2:** Source Lighting and Controls Intake; reconciled original fixture schedule, observed lighting and controls, physical objects, human-readable IDs, source links, exceptions and review package.
- **Critical ordering:** The **preliminary Light Point Extraction** pass happens before initial room polygons solely to aid geometric coverage and presentation. This is **not** full lighting takeoff, type resolution, final fixture ID allocation, control design, or automatic transfer of M2 approval into M1.
- **Architectural precedence:** Architectural floor/dimension plans remain the primary source of Space identity and boundary evidence. Electrical/RCP light symbols may assist containment checks, not create or redefine rooms.

## Phase 1 orchestration

1. **PROC-P1-SOURCE-REGISTER v0.2 — Source Registration and Visual Reference**
   - Input: supplied drawing set, revision metadata, contract/scope notes.
   - The agent shall **render and visually inspect the applicable source views itself**, using a whole-view scan and useful detail crops. Request an owner screenshot/snippet only when it would resolve a specific ambiguous convention, unavailable view or owner interpretation; retain its provenance. Owner-provided snippets are not a routine prerequisite to extraction. Before bulk transfer between views, verify distributed architectural registration and preserve source/target frames, original coordinates and transformed coordinates separately; after transfer, check individual object meaning/association as well as alignment.
   - Register architectural floor/dimension plan, RCP, electrical lighting plan, schedule/keynotes, specialty/partition/life-safety references as available, scope candidates and code-basis candidates, with exact revisions and discrepancies. Confirm substantial hatched/shaded exclusions rather than guessing.
   - Output: source/revision matrix, scope/open questions, render/crop references, any owner-snippet provenance, observed graphical conventions and applicable registration evidence. If architectural floor/dimension plan is unavailable, M1 remains provisional.

2. **PROC-P1-LIGHT-POINT-OBSERVE v0.2 — Preliminary Light Point Extraction**
   - Input: registered lighting plans (and architectural view/coordinate frame where available).
   - Visually establish apparent light-point count, arrangement and source-symbol locations in every in-scope source area; then locate each reasonably discernible light symbol or point and record **provisional observation identity**, source tag exactly as shown, sheet/view/revision, approximate point/graphic envelope, and known coordinate frame/level. Record uncertain or non-matching symbols, source groups and obvious cross-level sources.
   - **No final Light Object ID**, fixture type grouping, verified physical section count, room association or source schedule reconciliation is required in this preliminary observation pass. Do not turn an observed symbol into a declared fixture where assembly identity is unresolved. After Space inventory provides reviewed room associations, order **rooms across each plan/served level** in a top-left-to-bottom-right grid (upper room row left-to-right, then successive rows down). **Within each room**, order its light points identically: top row left-to-right, then successive rows to bottom-right, irrespective of fixture type. Assign **one continuous project-wide Light Point name sequence** across the resulting list: start at the first room and **never restart** the counter on a new room, level or fixture type. Use an approved display format (e.g. `L001`, `L002`, etc.) and retain an immutable internal observation/object identity independently. The Light Point name is copied to the register's `label` by default; only an explicit owner override permits a different label. Ambiguous room/point row order and cross-level served-space assignment require review. A newly detected point before rooms are known remains a provisional observation without final sequence.
   - Output: source-linked provisional light-point observations available to Space Extraction; subsequently a **project-wide sequential M1 point overlay/list ordered by room grid then point grid** once Space association is reviewed. Preserve original observation IDs, coordinates, and source facts for M2 reconciliation. Use an editable circular canonical anchor and adjacent approved ID-only label, default 4 pt, with other facts in metadata/linked records. Label-only movement does not move the anchor. Before owner handoff, reconcile count, arrangement and individual source/markup correspondence per reviewed Space; matching totals alone cannot establish completeness. Keep unresolved scope explicit.

3. **PROC-P1-SPACE-EXTRACT v0.2 — AI Space Inventory and Polygon Generation**
   - Input: architectural-first evidence, scope and provisional light points.
   - Render/visually interpret the architectural views and independently identify **all reasonably discernible in-scope Spaces**: labeled rooms, untagged enclosed pockets, circulation, stairs, service voids and relevant open-use subdivisions. Retain null for unsupported name/number/use; keep primary served level.
   - Produce one live **PDF `/Polygon`** primary footprint per contiguous Space (including rectangles), with saved persistent `/NM`, `/Subj`, `/Contents`, `/T` and annotation register linking the `/NM` to stable Space ID. Read [annotation contract](architectural-space-intake.md#annotation-type-naming-and-identity).
   - Follow the interior finished-face wall perimeter **closely with a small inward visual buffer, without a fixed numerical offset**; bridge typical door openings. Contain reasonably attributable *source light points/depicted fixture positions* while preserving the actual architectural Space interpretation. If symbol graphic envelope/served level conflicts with walls, **flag** it; don't drag walls or invent room membership to capture it. The buffer is presentation-only; source-area labels and code-relevant area geometry remain separate from markup check areas.
   - Apply existing M1/M2 notch, single-ring geometry, nested-area, open-to-below, view-scale and readable legend rules. Do not create holes or zero-width notches to imitate them. Keep geometry editable/unflattened.
   - Output: provisional Space Register, live marked PDF, ID/annotation register, discrepancies. Before owner handoff, visually compare rendered source and saved footprint markup for omissions, duplicates, circulation, pockets, gaps/overlaps and served levels. Do not claim an independent verification pass merely because the extraction itself executed.

4. **PROC-P1-OWNER-REVIEW v0.1 — Owner Markup Review / Alternate Origin**
   - Owner directly **reshapes, moves, creates or removes** room polygons, modifies Subject/Comments, marks desired geometry **accepted**, or provides equivalent precise acceptance in conversation. The owner need not open or edit the canonical registry. Retain returned PDF/page/frame evidence.
   - **Owner-first path is first-class:** The owner may draw some or all Space polygons in a supplied PDF and add identifying notes/comments; skip AI-first polygon generation for those objects and proceed directly to Markup Intake. New annotations lacking the final Space ID are eligible for provisional intake, not automatically rejected.
   - Human review is one **consolidated M1 package**, not individual approvals per internal process. Early interruptions are reserved for consequential blockers/ambiguities.

5. **PROC-P1-MARKUP-INTAKE v0.1 — Editable PDF Return and Registry Reconciliation**
   - Compare annotation `/NM`, Space ID in Comments, Subject, vertices, PDF page/frame and latest stored mapping against the prior package; do **not** use a label or location alone to overwrite identity.
   - Existing edited polygon → preserve Space ID and reconcile new geometry into authoritative register; new polygon → create/link stable Space record; renamed Subject → treat as proposed label review; deletion/missing/duplicate/copy → flag before removing/merging registry records. New owner-only polygons with comments may create provisional new Spaces.
   - Preserve prior versions, owner evidence, acceptance scope and return revision. A polygon marked `accepted` or explicitly accepted in narrative has its **geometry** protected from future optimizer/redraw; a later owner edit of accepted geometry requires explicit reopening/reconciliation rather than silent replacement. Acceptance is not a compliance certification and does not freeze unrelated metadata.
   - Detect differences, update registry and generated markups consistently, retain source facts separately, and summarize changes. Where an owner-returned drawing establishes a new working page/frame, preserve/verify that frame before combining coordinates.
   - Repeat **Space Extraction/Generation → Owner Review → Markup Intake** as necessary; accepted geometry stays untouched.

6. **PROC-P1-SPACE-VERIFY v0.2 — Independent Space Inventory Reconciliation**
   - A separate agent/pass inventories Spaces independently from rendered architectural floor/dimension views with PDF data assisting precision, not merely from the AI's original list or owner annotations, applying the same known owner scope decisions. Compare missing/extra/duplicate Spaces, labels, circulation, absorbed alcoves, notches, gaps/overlaps, served level and evidence. Identify candidate light-point containment mismatches without inferring room creation from lights. Once reviewed room assignment is available, check **M1 room grid order, point grid order within each room, and uninterrupted project-wide Light Point name sequence**, independent of fixture type.
   - Compare apparent Light Point counts, arrangements and individual source/anchor correspondence per Space; check duplicates/missing points even when counts match. Retain scoped comparison evidence with zero-light Spaces, ambiguous counts and pending findings. On any spatial discrepancy, inspect a focused rendered source/markup crop before another corrective data pass. Check annotation IDs ↔ Space IDs ↔ saved PDF mapping, live annotation types/vertices, and source/revision evidence. Run available `generators.validate_markup_pdf` checks on the actual final PDF and annotation register **when those artifacts exist**; passed tool checks are not proof of room completeness.
   - Output: findings/open items with affected IDs and source references, corrections and accepted limitations. Retain the **Room Schedule**, boundary PDF, annotation register and discrepancy list together.

7. **M1 review gate** — Account for every observed Space in reviewed scope or explicit unresolved discrepancy; independently check completeness; present consolidated package to owner. Preserve outstanding boundaries and area acceptance status honestly. Before M1 Light Point acceptance, every in-scope Space has a visual comparison with reconciled points or explicit pending scope/findings and downstream effects. Unresolved discrepancies do not make affected inventory complete or accepted; unaffected scope may proceed under scoped owner review. **A checker pass alone does not approve M1.**

8. **M2 — Source Lighting and Controls Intake** invokes existing schedule-first detailed lighting processes:
   - First extract the source MEP fixture schedule with exact suffixes, notes and evidence **before accepting detailed counts or interpreting linear assemblies**.
   - Visually reconcile preliminary point observations, source patterns and individual locations per Space with fixture types and actual physical fixture occurrences/sections, keynote-only items, controls/zone observations, source provenance, cross-level primary served Space, exterior holdouts and owner overrides. Separate physical Light Object identity from readable designation.
   - **Preserve approved M1 Light Point labels.** M1 owner review establishes Light Point names in a single uninterrupted project-wide sequence: rooms in top-left-to-bottom-right grid order, then lights within each room in the same row-by-row order, regardless of fixture type. Register labels mirror the corresponding Light Point names unless the owner explicitly overrides the label. M2 **does not reassign fixture display numbers**: apply [M2 Approved Light Point Identity and Fixture Scheduling](m2-fixture-numbering.md) to enrich those same objects with source schedule and fixture facts. Preserve immutable Light Object/source observation IDs and explicit approved/provisional status. Split/merge/new observations require a traceable owner-reviewed remap, not bulk renumbering.
   - Produce and independently review M2 Room Schedule, Source Lighting Schedule, Light Objects/Points, control intent observations, exception/discrepancy report and editable PDF as required, preserving approved M1 Light Point names and default matching register labels across these outputs. Apply existing M2 gate; no automatic assumption of M3 code/controls acceptance.

## Optional parallel / repeatable process

[**PROC-PHYSICAL-BOUNDARY-INTAKE v0.1**](https://github.com/kissolutions/knowledgebase_wikijs/blob/main/design-playbooks/physical-boundary-intake-v0.1.md) is available when routing, installation, compartmentation or barrier concerns warrant a targeted construction Boundary Register. A **Space polygon does not imply a registered physical wall/barrier**. Do not make a full wall census an M1 gate.

## Acceptance and configuration

- Individual acceptance = forward-looking protection against derived reconfiguration of specified Space geometry.
- Snapshot = immutable captured state, not automatic approval.
- Configuration Baseline = explicitly designated snapshot for comparison and recovery, not blanket acceptance.
- A user directive such as “make this the M1 baseline” preserves the identified M1 registers/PDF/annotations/open issues together when the supported snapshot mechanism is available; otherwise assemble an explicitly identified manual versioned package. Do not claim automated snapshot functionality exists.

## Informative illustrations (non-normative)

- [Room polygon close to inside walls](https://github.com/kissolutions/knowledgebase_wikijs/blob/main/assets/illustrations/space-boundary-markup-example.svg)
- [Historical clockwise fixture-ID illustration (**superseded example**, not current M1/M2 practice)](https://github.com/kissolutions/knowledgebase_wikijs/blob/main/assets/illustrations/light-ids-clockwise-room-example.svg)

These are NEC Handbook-style explanatory aids. Written process/source evidence controls.

## Implementation/readiness record

| Function | Current grounded status |
|---|---|
| Architectural-first inventory rules, editable polygon field contract | Documented |
| Room notch/nested Space rules, served level/cross-level caveats | Documented |
| Owner-reported Bluebeam Polygon editing/readback, 47 returned annotations | Owner-reported proof for tested case only |
| Live PDF annotation/register checker | Implemented, requires actual PDF/CSV and correct plan pages |
| Preliminary Light Point Extraction as a standalone v0.2 procedure | **Specified here; automated extractor unproven** |
| Agent-rendered source/markup inspection; targeted optional owner snippets | **Required supervised method; automated visual completeness unproven** |
| Circular Light Point anchor / separate ID-only label and owner return | **Specified presentation; font/marker/metadata and label-vs-anchor edit/readback proof still required** |
| Cross-view architectural registration plus object correspondence | **Required method and project evidence; no automated registration certification** |
| Owner-first complete/supplemental polygon intake | **Specified here; general automated parsing/reconciliation unproven** |
| Inward visual-buffer polygon generation | **Specified here; automated geometric constraint not yet tested** |
| Acceptance via polygon comments or conversation | **Specified here; complete automated enforcement not verified** |
| Continuous project-wide M1 names; room-major/row-major ordering; labels mirror names unless overridden | **Specified here; annotation and numbering automation unproven; not grouped by fixture type** |
| M2 labels | **Must preserve owner-approved M1 Light Point labels**; type-block/clockwise renumbering superseded; split/merge reconciliation remains a supervised workflow |
| Complete independent M1 verification | Required method; dependent on actual project review |
| Full Boundary Register integration / crossing analysis | Optional future implementation |

**BETA smoke test:** Using a two/three-room source plan, render/inspect the source and record provisional fixture points; use owner snippets only for targeted ambiguity; generate markup/Space IDs; have owner reshape, accept and add a new polygon without Space ID; ingest returned comments/vertices and preserve stable IDs; verify independent room list; regenerate without changing accepted geometry; then reconcile points under known Spaces and exercise M1 uninterrupted project-wide numbering by room grid and within-room point grid irrespective of fixture type, verifying label equals name absent owner override. Use source-revision/annotation ID diffs and distinguish observed from confirmed behavior.

**v0.2 review additions:** Detect an omission paired with a duplicate despite matching totals; compare individual source/target positions. Exercise independently moved label and anchor with persistent identities/metadata. Verify a cross-view transform against distributed architectural features and then check room/object correspondence. Record actual results; no automated proof is implied.
