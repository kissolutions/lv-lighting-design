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
  - "phase-1-intake-process-map-v0.1.md"
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

M1 labeling is **within each room, top row to bottom row, left-to-right across each row, regardless of fixture type**, after reviewed Space association. The initial preliminary Light Point Extraction may find points before Spaces are established, with stable observation IDs but no approved room-local labels. Owner markup review and reconciliation establish or revise the M1 labeling; only approved labels are protected.

**Identity layers (keep separate):**

- **Observation identity:** Stable source-detection/markup reference tying a point to what appeared on a particular drawing revision.
- **Canonical Light Object internal `id`:** Immutable identity used for links to spaces, zones, channels, routes and equipment.
- **Light Point display `label`:** Human-recognizable room-local designation established at M1 and preserved into M2. Keep the approved spelling/format, which may be project-specific; no new mandatory naming schema is imposed here.
- **Source fixture mark/type:** Original MEP plan/schedule designation, kept distinct from the display label.
- **Annotation identity:** Saved PDF `/NM` mapped through the annotation register to the appropriate object; geometric edits do not create new identities automatically.

The existing `Light Object.label` and `id` fields remain the model fields of record where supported. Do not create duplicate canonical registers or replace immutable internal IDs with room-local sequence numbers.

## M2 procedure

1. **Ingest approved M1 package.** Read the Room Register, approved/provisional Light Points, saved annotation register and source/revision manifest. Reconcile mappings using persistent IDs, not text placement alone.
2. **Preserve labels and identities.** Copy/retain the M1 approved room-local labels and canonical identities without numbering by source fixture type or making a new display-label pass. Provisional labels remain provisional.
3. **Extract original MEP fixture schedule before detailed counting.** Preserve schedule lines, exact type suffixes, keynotes, descriptions, manufacturer/model facts when evidenced, wattage/voltage, driver characteristics, and source/revision locators.
4. **Associate fixture schedule types with already-registered Light Points.** Assign exact source marks/types and reconcile symbol evidence without regrouping their approved Light Point labels. Maintain unknown or ambiguous associations as findings.
5. **Reconcile physical occurrences.** Apply linear-run/physical-section/assembly rules and source group evidence; a point/symbol may not map one-to-one to a final physical fixture. When one observation resolves into multiple physical Light Objects, or multiple observations into one, **retain the original M1 observation identities and approval evidence**, propose a documented remap and any required new labels for owner review. Do not silently duplicate, delete, merge or renumber approved Light Points.
6. **Reconcile rooms and served levels.** Compare source level, primary served Space, accepted polygons and cross-level luminaires without forcing membership or creating duplicates. Any changed approved association is a finding/change proposal.
7. **Review and deliver.** Publish a label-to-internal-ID-to-observation-to-source-type mapping and room/type counts, M2 source schedule and physical fixture records, control observations, open items and review markup as required. All derived views retain the same M1-approved display labels where applicable.

## M1 labeling order — reference only

A new/revised M1 label proposal uses the accepted upright drawing/view coordinate frame, **starting at the room's upper-left**, scanning the uppermost row **left-to-right** and proceeding downward **row-by-row** to the lower-right. Mixed fixture types do **not** restart the count. Row breaks or ordering in diagonal, irregular, disconnected or overlapping arrangements are review decisions rather than asserted drawing facts. Keep accepted existing labels through later point movements unless the owner explicitly authorizes coordinated renumbering. This is *not* a clockwise or type-specific rule.

## Verification and exceptions

Before M2 review, verify that:

- every approved M1 Light Point is accounted for in M2, or has an explicit, traceable split/merge/exclusion/holdout finding;
- approved M1 labels are unchanged; any provisional/unlabeled items are clearly marked as such;
- each present canonical physical Light Object has a stable internal identity and unambiguous references to observed source items, primary served Space and fixture type or an explicit unresolved type;
- duplicates, missing points, room-membership conflicts, schedule-count mismatches, external fixture holdouts and source revisions are surfaced, not hidden by relabeling;
- annotation and register representations agree and approved geometric/label acceptance remains protected;
- any approved-label change has explicit owner authority plus old/new label, permanent ID, affected deliverables and revision mapping.

**New/missing/split points:** Do not assume all M1 annotations equal one physical fixture. If a reconciliation adds a genuinely new physical object, assign a new **internal** ID immediately; propose a human-readable label consistent with M1 conventions without reusing an accepted label or shifting all approved labels. If a display sequence cannot remain perfectly consecutive, document the exception; approval and traceability take precedence over aesthetic continuity.

**Changed approved labels:** Only owner-authorized changes may replace them. Preserve previous issued mappings and reconcile all affected workbook and PDF references together. Snapshot/baseline does not itself imply per-record acceptance.

## Software status

The current model supports separate `Light Object.id` and `label`. The source-review exporter can include `light_label` and `light_id`, but **does not** independently certify M1 approval, guarantee row-major ordering, reconcile owner markup edits, or complete physical split/merge handling. These are supervised engineering tasks until specifically implemented/tested. Existing numbering-related software that sorts type blocks is **not authorized** to overwrite M1-approved labels under this contract.

Owner: KIS Solutions. 2026-10-17. Supersedes prior M2 fixture-type-block / clockwise display-numbering guidance.
