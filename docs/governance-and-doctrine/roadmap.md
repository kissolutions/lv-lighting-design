---
title: "LV Workflow Development Roadmap"
page_type: governance
page_status: draft
confidence_level: medium
domain_primary: low-voltage-lighting
ai_role: authoring_rules
invocation_triggers:
  systems_present: [low_voltage_lighting]
decision_axes: [markup_readiness, source_intent, development_priority]
related_pages:
  - "../design-playbooks/lv-project-workflow-and-readiness.md"
  - "../design-playbooks/lighting-design-playbook.md"
---

# LV Workflow Development Roadmap

## Current Foundation

Use the [full workflow/readiness map](../design-playbooks/lv-project-workflow-and-readiness.md) as the current audit, with the [project checklist](../../templates/first-project-checklist.md) for execution. WikiJS owns the general electrical lighting knowledge; LV work extracts MEP intent, checks it through WikiJS, and translates it into implementation. Authorized and approved departures are tracked separately from source intent.

Available: architectural intake/reconciliation directives; current v0.4 physical-first schema, seed, phase checker and synthetic examples; stable fixture/source IDs; area/classification/evidence records; nested branch/unit/channel ownership; zones/controllers and declared emergency/backup relationships; reference, membership, load and capacity checks with derived JSON. Current source-review export supports v0.4 and read-only v0.3; legacy v0.1 keeps its dedicated outputs.

These support supervised intake, manual source/code review and LV grouping. They do not demonstrate an editable PDF output, complete code evaluation, automatic extraction/grouping or an end-to-end installer package.

## Next: First Review Markup

Prove one representative room or sheet using registered source revisions, stable IDs, traced/flagged boundaries, fixture anchors and documented MEP control groups. Include LV channel graphics only where selected load, compatibility and functional intent are supported. Label unresolved scope as provisional.

Prove displayed-page crop/rotation placement, annotation editability, save/readback and identity preservation. Use accepted scale/geometry before claiming measured area. Test native Bluebeam Area recognition/editing/recalculation separately from standard editable polygons. Do not wait for a whole-building optimizer or a complete device ontology before this small experiment.

## Small Contract and Output Extensions

1. Implement agreed zone verification and implementation-review statuses, with supporting assessment evidence and per-function findings.
2. Separate original MEP scheme, applied LV implementation and proposed/approved departures; define authorization and approval records.
3. Inventory/intake/design data phases are implemented; continue developing source/owner milestone evidence and later code evaluation.
4. Five source-review CSVs are implemented. Develop later engineering schedules, spreadsheet reconciliation and a complete source-occurrence disposition register. Preserve occurrence identity, source facts and shared-zone relationships.

Schema/check changes require versioning, synchronized examples/docs, and meaningful tests. Merely documenting these features does not implement them.

## Refine Grouping and Equipment From the Proof

Verify actual product loads, output compatibility, unit budgets and independent controller behavior. Confirm emergency signaling and backup paths in the project. Review sensor/device configuration and coverage through WikiJS. Record real routing/grouping constraints before implementing optimization; source/control boundaries survive channel sharing.

## Pending Directive: Fixture Product Research Before M4

**Status: Flagged for writing before M4 equipment selection and quantified channel grouping.** Add an explicit "Resolve missing fixture specifications" step after source reconciliation. Capture missing schedule information and exact full/partial part numbers during M2; research manufacturer cut sheets, ordering guides and driver documentation before affected M4 selections/calculations proceed. Documented gaps may remain in an accepted M2 package, with affected downstream work pending.

The future directive must distinguish project-source schedule facts from manufacturer findings, preserve source/version evidence, and leave unresolved ordering options as candidates for review. A partial part number does not confirm a configuration. Keep original AC input wattage separate from verified LV channel-interface load. WikiJS owns reusable product facts; this extension owns project research records and application of verified compatibility/load limits. This entry records the writing task; it does not implement a research agent or complete the playbook step.

## Deferred Incorporation: Automatic Receptacle Control

**Status: Flagged for later incorporation.** At the beginning of project intake, ask whether Automatic Receptacle Control (ARC) is within the LV controls scope and record the answer. Do not infer scope from its presence or absence on lighting sheets. When in scope, comb electrical power drawings, notes, schedules, details and other supporting source information for the specified ARC scheme; retain source references, missing information and conflicts for review.

Provide a home for controlled receptacle points/groups, served Spaces, source circuits, specified control behavior and associated control devices. Plan an LV implementation path using the LV-controlled relay powerpack devices used by KIS, with verified device/load compatibility and controller associations. Receptacle loads must remain distinct from lighting fixture counts and LV lighting output-channel loads. The eventual abstraction may share supported control relationships without inventing default lighting zones.

Retrieve and link the owner's existing WikiJS ARC pages when writing the directive. WikiJS owns general ARC/code/design guidance; this extension owns scope intake, source extraction and LV-system compatibility/implementation. Preserve the MEP scheme first and apply the existing authorization/review process to gaps or proposed departures. Scope-check placement, model/review outputs, powerpack selection and verification remain development tasks; no ARC extraction or schema support is implemented by this entry.

## Deferred Feature: Drawing North-Arrow Recognition

**Status: Future feature.** Recognize North arrows during source registration so cardinal-direction references in room descriptions, boundary notes and review markups remain consistent. Associate evidence with the applicable plan view, source sheet and revision; distinguish explicitly identified true/geographic North from project/plan North rather than assuming they are equivalent.

Account for page/view rotation and differently oriented plan views before transferring a directional reference. Retain an explicit source-based orientation mapping; flag missing, ambiguous or conflicting arrows for review instead of treating page-up as North. Keep page-relative instructions such as M2 fixture numbering's "top-left" and clockwise traversal distinct from geographic directions. Recognition, orientation mapping and consistency checks remain unimplemented.

## Pending M3 LV Workflow Gaps

**Status: Flagged for later development.** The owner-supplied first-M3 guidance-gap report identifies four LV tasks below; the other fourteen are tracked in the [WikiJS guidance backlog](https://github.com/kissolutions/knowledgebase_wikijs/blob/main/design-playbooks/lighting-controls-guidance-index.md#pending-m3-guidance-backlog). Preserve report IDs/priorities for follow-up; they are the testing agent's suggestions, not verified rule statements.

| ID | Reported priority | Pending LV work |
|---|---|---|
| F-14 | High | Strengthen Step 1/code-basis intake: identify the actual authority having jurisdiction using supporting evidence, rather than treating the mailing city as jurisdiction; reconcile and populate existing code-basis records before dependent M3 conclusions. |
| F-15 | Medium | Define the M3 evidence/output home for gate scope/status, owner directions/interpretations, adopted narrative and per-room checks; implement the agreed verification/implementation status attributes through a versioned contract. Existing project records remain usable. |
| F-16 | Medium | Make the minimal-source-controls/design-build branch explicit in Step 7. Preserve known source functions and document gaps, then use existing scoped authority or owner narrative through the classification/interpretation/adoption gates. Missing controls alone do not authorize redesign. |
| F-17 | Low | Develop a verified selected-LV-system capability/constraint page: available sensor/switch combinations, software-reconfigurable sequences and daylight-capable hardware, with actual equipment/configuration limits and evidence. Beta properties are not universal LV facts. |

For F-15 and later reporting, follow [on-demand owner decision review](../design-playbooks/lv-project-workflow-and-readiness.md#on-demand-owner-decision-review). The owner has chosen a sweep/report of existing project records rather than a separate primary owner-decision register. Preserve record provenance and decisions during any later refactoring. This section flags development; it does not implement M3 fields, a report generator or the other workflow extensions.

## Later Delivery Stages

Develop route endpoints/topology, equipment locations, calibrated cable lengths and allowances; detailed connection/configuration output; selected hardware BOM; coordinated release checks; field-change/diff workflows; commissioning tests and as-built reconciliation. The v0.1 route-point object is not a current v0.3 route engine or an installed-length result.

Keep real project PDFs, schedules, takeoffs, model instances, markups, decisions and results outside Git. Turn accepted findings into reusable instructions/synthetic tests without copying client identifiers.

## Deferred Feature: Layered Master Review PDF

**Status: Future feature; not part of the current workflow.** Keep room-boundary, fixture/source-control, device/design and cabling markup documents separate for now, as their information becomes available. Identify source/model revision and review scope on each document, retain stable object/annotation IDs, and preserve accepted milestone copies. Do not consolidate current deliverables or require PDF layers to complete a milestone.

The future concept is one editable master PDF per source-background revision with separately visible Rooms, Fixtures, Source Controls, Lighting Zones, Devices, Cabling and Review layers. Preserve architectural and RCP page identities and their independent scale/registration evidence. Source intent remains distinct from proposed/adopted implementation, and functional zones still come later from supported operation; a layer does not establish an object identity or approval status.

Before adopting the feature, prove visibility controls, boundary/device editing, saved layer membership, stable IDs and geometry readback in Bluebeam and any other supported editors. Keep the working master unflattened and retain milestone snapshots. Record tested editor/version behavior and delivery visibility settings. This roadmap entry neither implements layer generation/readback nor establishes compatibility; schedule it after the separate-document workflow is working reliably.

Owner: KIS Solutions. October 2026; draft priorities based on owner workflow and local capability audit.
