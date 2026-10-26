---
title: "M2 Approved Light Point Identity and Fixture Scheduling"
page_type: playbook
page_status: draft
confidence_level: medium
domain_primary: low-voltage-lighting
ai_role: prescriptive_standard
invocation_triggers:
  systems_present: [low_voltage_lighting]
decision_axes: [fixture_identity, source_schedule, room_membership, markup_readability, revision_traceability]
related_pages:
  - "phase-1-intake-process-map-v0.2.md"
  - "lighting-design-playbook.md"
  - "../concepts/fixture-identity-and-summary-counts.md"
  - "../ontology/canonical-model/light-object.md"
  - "../../templates/m2-user-review-checklist.md"
---

# M2 — Preserve Approved Light Point Identities During Fixture Scheduling

## Governing principle

**M1 establishes room-associated Light Points and their owner-approved human-readable labels. M2 operates on those same Light Points.** M2 adds/reconciles source fixture type, physical fixture identity, schedule attributes, assembly/section interpretation, controls observations and associated evidence. **Do not renumber Light Points by type, fixture schedule order or clockwise traversal.**

The earlier M2 convention of project-wide type blocks, `L001`-style type allocation and clockwise numbering *by fixture type* is **superseded**. It must not run after approved M1 Light Point labeling. This supersedes the previous content of this page, not the existing persistent internal IDs, source facts or valid owner-approved labels.

## Input contract / authority

M2 begins with the **latest reviewed M1 Light Point Register/observation-to-Light mapping** (or an expressly identified approved subset), the associated Room/Space Register, M1 markup PDF and annotation-to-object register, acceptance record and source revisions. Verify the M1 approval/review scope and the Light Point labels it covers. If a label is not yet approved, retain it as **provisional**, and report the affected scope; do not claim approval or fill a missing label by re-running a type-sort.

M1 names Light Points by visiting **rooms in top-left-to-bottom-right grid order**, then visiting **light points within each room** top-to-bottom by row, left-to-right within each row, regardless of fixture type. The Light Point name counter is **continuous across all rooms and levels**: it never restarts at a room boundary. The register `label` equals the Light Point name by default and may differ only through an explicit owner override. The initial preliminary Light Point Extraction may find points before Spaces are established, with stable observation IDs but no approved project-wide labels. Owner markup review and reconciliation establish or revise the M1 labeling; only approved labels are protected.

**Identity layers (keep separate):**

- **Observation identity:** Stable source-detection/markup reference tying a point to what appeared on a particular drawing revision.
- **Canonical Light Object internal `id`:** Immutable identity used for links to spaces, zones, channels, routes and equipment.
- **Light Point name:** Approved human-recognizable sequential designation established at M1 across the project, with rooms/points visited in grid order; distinct from immutable internal identity.
- **Register display `label`:** By default **identical to the Light Point name**. Change only when the owner explicitly overrides it, retaining the original name and the override evidence; preserve into M2.
- **Source fixture mark/type:** Original MEP plan/schedule designation, kept distinct from the display label.
- **Annotation identity:** Saved PDF `/NM` mapped through the annotation register to the appropriate object; geometric edits do not create new identities automatically.

The existing `Light Object.label` and `id` fields remain the model fields of record where supported. Do not create duplicate canonical registers or replace immutable internal IDs with project-wide sequence numbers.

## Visual verification and anchor handoff

Carry M1's scoped [visual completeness evidence and anchor/label mapping](visual-spatial-extraction.md) into M2. Visually reconcile source marks, positions and interpreted physical occurrences per Space, including schedule/assembly-driven count differences; matching totals alone is insufficient. Recheck affected areas after split/merge, new sources or owner edits. Preserve the circular canonical anchor independently of its adjacent 4 pt default ID-only label and keep fixture facts in metadata/linked records. Label movement does not move the point or authorize renumbering. Cross-drawing transfer needs geometric registration plus object correspondence. Pending discrepancies remain pending for the affected scope rather than becoming approved through a checker pass.

## M2 procedure

1. **Ingest approved M1 package.** Read the Room Register, approved/provisional Light Points, saved annotation register and source/revision manifest. Reconcile mappings using persistent IDs, not text placement alone.
2. **Preserve names, labels and identities.** Retain the approved M1 Light Point names, project-wide sequence, and canonical identities. Preserve `label = Light Point name` unless a documented owner override authorizes another label. Do not allocate new fixture-type-based display sequences. Provisional names/labels remain provisional.
3. **Extract original MEP fixture schedule before detailed counting.** Preserve schedule lines, exact type suffixes, keynotes, descriptions, manufacturer/model facts when evidenced, wattage/voltage, driver characteristics, and source/revision locators.
4. **Associate fixture schedule types with already-registered Light Points.** Assign exact source marks/types and reconcile symbol evidence without regrouping their approved Light Point labels. Maintain unknown or ambiguous associations as findings.
5. **Reconcile physical occurrences.** Apply linear-run/physical-section/assembly rules and source group evidence; a point/symbol may not map one-to-one to a final physical fixture. When one observation resolves into multiple physical Light Objects, or multiple observations into one, **retain the original M1 observation identities and approval evidence**, propose a documented remap and any required new labels for owner review. Do not silently duplicate, delete, merge or renumber approved Light Points.
6. **Reconcile rooms and served levels.** Compare source level, primary served Space, accepted polygons and cross-level luminaires without forcing membership or creating duplicates. Any changed approved association is a finding/change proposal.
7. **Review and deliver.** Publish a label-to-internal-ID-to-observation-to-source-type mapping and room/type counts, M2 source schedule and physical fixture records, control observations, open items and review markup as required. All derived views retain the same M1-approved display labels where applicable.

## M1 labeling order — reference only

For a new initial M1 sequence, use the accepted upright drawing/view coordinate frame: order **rooms** in rows from upper-left to lower-right across the scoped building plan, then **light points inside each room** in rows from upper-left to lower-right. Continue the **same numbering counter across every room** and do not restart at changes of room, level, or fixture type. The `label` mirrors the Light Point name unless the owner overrides it. Mixed fixture types do not change order. Row breaks or ordering in diagonal, irregular, disconnected or overlapping arrangements are review decisions rather than asserted drawing facts. Keep accepted existing labels through later point movements unless the owner explicitly authorizes coordinated renumbering. This is *not* a clockwise or type-specific rule.

## Verification and exceptions

Before M2 review, verify that:

- every approved M1 Light Point is accounted for in M2, or has an explicit, traceable split/merge/exclusion/holdout finding;
- approved M1 Light Point names are unchanged; labels equal those names except for documented owner overrides; any provisional/unlabeled items are clearly marked as such;
- each present canonical physical Light Object has a stable internal identity and unambiguous references to observed source items, primary served Space and fixture type or an explicit unresolved type;
- duplicates, missing points, room-membership conflicts, schedule-count mismatches, external fixture holdouts and source revisions are surfaced, not hidden by relabeling;
- annotation and register representations agree and approved geometric/label acceptance remains protected;
- any approved-label change has explicit owner authority plus old/new label, permanent ID, affected deliverables and revision mapping.

**New/missing/split points:** Do not assume all M1 annotations equal one physical fixture. If a reconciliation adds a genuinely new physical object, assign a new **internal** ID immediately; propose a Light Point name and matching default register label consistent with the continuous M1 sequence without reusing an accepted name or silently shifting approved names. If a display sequence cannot remain perfectly consecutive, document the exception; approval and traceability take precedence over aesthetic continuity.

**Changed approved labels:** Only owner-authorized changes may replace them. Preserve previous issued mappings and reconcile all affected workbook and PDF references together. Snapshot/baseline does not itself imply per-record acceptance.

## Software status

The current model supports separate `Light Object.id` and `label`. The source-review exporter can include `light_label` and `light_id`, but **does not** independently certify M1 approval, guarantee cross-room and within-room grid ordering, reconcile owner markup edits, or complete physical split/merge handling. These are supervised engineering tasks until specifically implemented/tested. Existing numbering-related software that sorts type blocks is **not authorized** to overwrite M1-approved labels under this contract.

Owner: KIS Solutions. 2026-10-17. Supersedes prior M2 fixture-type-block / clockwise display-numbering guidance.
