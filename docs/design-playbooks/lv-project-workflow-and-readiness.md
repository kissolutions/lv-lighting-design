---
title: "LV Project Workflow and Readiness"
page_type: playbook
page_status: draft
confidence_level: medium
domain_primary: low-voltage-lighting
ai_role: prescriptive_standard
invocation_triggers:
  systems_present: [low_voltage_lighting]
decision_axes: [source_intent, milestone_readiness, markup_review, implementation, release]
related_pages:
  - "lighting-design-playbook.md"
  - "architectural-space-intake.md"
  - "../ontology/canonical-model/lv-light-zone.md"
  - "../validation/space-intake-reconciliation.md"
  - "../../generators/README.md"
---

# LV Project Workflow and Readiness

## Purpose and Authority

The LV workflow extracts the MEP lighting/control scheme, checks it through the general electrical workflow in `knowledgebase_wikijs`, and translates supported intent into an LV implementation. It does not begin by designing a replacement control scheme. Architectural floor/dimension plans establish rooms and boundaries; MEP plans, legends, schedules, details, and notes establish the specified lighting/control intent. An engineering check does not overwrite a source observation.

WikiJS owns the shared electrical lighting knowledge: space vocabulary, room-by-room energy-code analysis, control-device selection/configuration, decision trees, and the application guide. This repository owns the LV project model, extraction/reconciliation workflow, electrical grouping, implementation checks, and markup/output conventions. Local application-guide/code-profile drafts are working material for alignment with WikiJS, not a competing general design authority. See the [repository boundary](../governance-and-doctrine/repository-boundary.md).

Redesign is conditional: identify a deficiency or implementation opportunity, establish authority to propose a change, document the proposal and its approval, then update the applied implementation while preserving the original scheme. A confirmed model decision alone does not establish approval by the responsible party. Unclear intent requires clarification, not an invented default.

## How to Read Readiness

This is an October 2026 audit of the local documentation and tools, not a declaration that a particular project has passed its milestones. **Method available** means there is enough documented guidance for a supervised manual/agent pass. **Checks implemented** means software checks entered data. **Development needed** means an output, rule, or round trip has not been implemented/proven. Passing synthetic checks does not prove plan extraction, source completeness, physical coverage, or an editable PDF round trip.

## Full Design and Delivery Cycle

| Step | Work and reviewable output | Enough now | Development or proof still needed |
|---|---|---|---|
| 1. Establish basis | Source register, sheet/revision matrix, scope, selected code basis, and who may authorize departures | Method and source/code-basis records available | Resolve governing discipline revisions on the actual project; explicit change-approval structure remains to be developed |
| 2. Inventory rooms | Architectural room list, neutral untagged-area entries, served levels, discrepancy list, editable boundary review | Architectural-first method and Space records available; entered membership checks implemented | Independent extraction/completeness review; boundary tracing/output and owner-edit readback not implemented |
| 3. Establish areas | Architectural area labels first; reviewed measured areas where needed, with scale/boundary evidence | Area/basis/note fields and measurement directives available | Scale-calibrated polygon calculation and saved-geometry readback; native Bluebeam Area compatibility unproven |
| 4. Extract lighting and controls | Source Lighting Schedule, Room Schedule, Lighting Fixtures takeoff, Light Points, original MEP control intent, emergency observations | Types, occurrences, source references, source groups, and normal/emergency records available | Supervised extraction and independent fixture/symbol reconciliation; v0.3 schedule/workbook exporter and complete exclusion register not implemented |
| 5. Check the MEP scheme | Reviewed room classifications, applicable WikiJS/code references, per-function findings, zone verification and implementation-review statuses | Manual check method, Space code references, decisions, and open items available | Vocabulary/profile completion in WikiJS; status fields, per-function assessments, source/applied sequence separation, and automated code matching not implemented |
| 6. Select LV implementation | Confirmed LV fixture/driver loads, compatible outputs, candidate sensors/switches/controllers reproducing MEP behavior | Load basis, compatibility, device registers, and selections available | Product evidence and coverage/layout review; detailed device configuration and approval-of-departure records incomplete |
| 7. Assign zones and equipment | Functional zones, independent controller outputs, emergency command/backup paths, physical equipment identity | Hierarchy and Space references/checks implemented | Detailed source-to-implementation mapping, locations, sensor coverage, all outage paths, and project emergency performance review |
| 8. Group supply channels | Light-to-channel assignments, limits/margins, units and aggregate capacity, reviewed one-room grouping | Arithmetic, reference, output-capacity, and declared backup checks implemented | Grouping remains manual; routing practicality/product constraints need review; no optimizer |
| 9. Produce first design markup | One-room or one-sheet LV review PDF, IDs/legend, supporting load/assignment tables, open items | Model provides IDs, point anchors, relationships, and derived values | PDF writer, crop/rotation placement proof, annotation editability, label layout, and update/readback loop not implemented |
| 10. Coordinate installer package | Locations, routes/endpoints, cable selections/length basis, controller/device schedule, connection details, quantities and sequences | Inputs partly available; v0.1 CSV exporter remains usable for v0.1 only | v0.3 schedule/BOM export, routing topology, calibrated lengths, detailed device/connection output and installation rules |
| 11. Review and issue | Approved scope/revision, resolved release blockers, coordinated package and approval record | Manual review can use existing decisions/open items | Formal release checklist, approval tracking and complete cross-deliverable reconciliation |
| 12. Installation and field changes | Substitution/field-change log, impact checks and revised affected outputs | Stable IDs and source/decision provenance support revision review | Defined change/diff workflow and reliable drawing/model round trip; authorized field changes still need documented approval |
| 13. Commission and close | Function tests, deficiency closure, accepted configuration, final schedules/markups and as-built record | Normal/emergency intent provides part of the test basis | Test protocols/results, coverage/daylight testing, installed configuration and as-built reconciliation not implemented |

## Milestone Review Points

| Milestone | Evidence to review | Pass condition for the scoped work |
|---|---|---|
| M1. Room inventory | Independent architectural inventory, omission/identity discrepancies, boundary review | Every observed Space is accounted for; omissions reviewed and causes established or explicitly undetermined; unsupported facts remain unknown. Boundary and area acceptance can remain pending |
| M2. Source lighting/control intake | Initially completed Room Schedule, Lighting Schedule, Lighting Fixtures and Light Points; independent verification against the source set | Physical fixtures/counts and applicable control observations are reconciled; missing/conflicting information is explicitly flagged; nothing is silently filled in. Area takeoff and classifications are reviewed as their evidence becomes available |
| M3. Control check and interpretation | Area/use/enclosure basis, adopted code and WikiJS references, occupancy/daylight/manual/scheduling findings | Findings distinguish compliant, deficient, ambiguous source and no information; implementation opportunities are separately flagged. Consequential unknowns and proposed departures block finalization of the affected scope |
| M4. First LV review markup | One reviewed room/sheet, source-intent mapping, confirmed loads for any quantified grouping, equipment/zone/channel assignments and editable PDF | Model/table/PDF identities and assignments agree; placement and edit/save/readback work for the tested annotation type; unresolved content is visibly provisional. This is review approval, not construction release |
| M5. Coordinated issue | Complete scoped installer package, source reconciliation, implementation/route/device details, changes and approvals | All release-critical scope, code interpretation, product, emergency, routing and coordination questions are resolved by the responsible reviewers; deliverables use the same revision |
| M6. Closeout | Installed configuration, functional test results, field changes and final documentation | Accepted field changes are reflected consistently; open deficiencies are resolved or explicitly carried in the accepted closeout record |

These are review gates, not values currently implemented in `project.stage`. That field still accepts `takeoff`, `provisional`, and `checkpoint`. The current v0.3 checker mixes later room/code and electrical-assignment readiness with structural checks; its overall pass/fail result is not an M1/M2 gate. Do not invent code classifications, areas, mounting heights, or channel assignments to make an intake model pass. A separate milestone evaluator is future work. Until then, record gate evidence and scope in the project review checklist and retain all checker findings.

## Control Review Results

The owner has agreed to these two zone attributes, but they have not yet been added to the schema/generators:

| Attribute | Values | Meaning |
|---|---|---|
| `control_verification_status` | `not_reviewed`, `compliant`, `deficient`, `ambiguous_source`, `no_information` | Result of checking the extracted source scheme against the reviewed interpretation of applicable code for the functions assessed |
| `implementation_review_status` | `not_reviewed`, `typical_design`, `manual_review_required` | Whether implementation fits the typical approach or warrants discussion about a departure, limitation, or simpler arrangement |

A deficient finding needs clear source evidence plus the interpretation/reference it violates. Ambiguous source means information exists but cannot be resolved; no information means the relevant plan/legend/schedule/note/detail review found no applicable instruction. Compliant describes the reviewed functions and basis, not an unqualified certification of the whole project. A deficient zone always requires manual review; a compliant zone may also need implementation review. Unknown/ambiguous findings cannot be treated as compliant by default.

Retain separate occupancy, daylight, manual-control, and scheduling findings when necessary. The per-function structure and zone-summary precedence need a later contract decision; do not collapse an unresolved daylight sequence into an occupancy pass. Retain source locators, code/guide edition and revision, reasoning, review scope, reviewer/date, and any proposal/approval in the project review record. Use existing `open_items[]`, decisions and references where appropriate; do not insert unsupported new fields into v0.3 instances. Record deviations and their actual approval separately from both status attributes.

## Progressive Markup Readiness

Early markups can precede complete controls analysis. Follow the [enclosed/logical boundary instructions](architectural-space-intake.md#enclosed-rooms-and-logical-open-areas) and [annotation naming/identity convention](architectural-space-intake.md#annotation-type-naming-and-identity). Enclosed rooms follow architectural walls; logical open-area subdivisions may be approximate proposals for owner editing, with their observed basis and uncertainty retained. That permission applies to draft geometry, not invented source names/use, code classification or control behavior. Room-boundary markups need registered architectural sheets, stable Space IDs, traceable boundaries, and visible uncertainty notes. They do not need final channels, controllers, sensor quantities, or final code conclusions. Measured areas additionally require accepted scale/boundary evidence.

Fixture/source-control review markups need reconciled occurrences and evidence for the symbols, groups, and behaviors being shown. Distinguish source observations from proposed LV assignments through the legend. A provisional outline may identify an unresolved group; it must not present an invented sequence as MEP intent.

A quantified LV channel markup additionally needs confirmed channel-interface loads and product limits, preserved functional behavior, and reviewed controller/backup relationships for the scope being quantified. Unresolved rooms can remain visibly provisional while unrelated verified rooms proceed. No connected-load number is obtained by treating unknown watts as zero.

First prove one representative room or sheet. Use stable IDs on editable annotations; verify displayed-page crop/rotation placement, open/save behavior, and readback of changed geometry/IDs. Standard editable polygon annotations and native Bluebeam Area measurements are separate output capabilities. Promise native Area behavior only after the owner's editor recognizes it, permits boundary edits, recalculates area with the correct scale/units, and retains readable identity/geometry after saving. Do not require the full installer-package pipeline before attempting this small proof.

## Development Priorities

1. **Next experiment: one-sheet editable PDF proof.** Show room boundaries, fixture anchors/IDs and documented source control groups. Add provisional LV channel graphics only for load-confirmed scope. Record what can be edited and read back; keep native Bluebeam Area as a separate compatibility test.
2. **Small model extension: control review and change provenance.** Implement the agreed statuses with evidence, per-function findings and distinct source/applied/proposed states. Define who approved departures. Version the contract, update examples and run meaningful tests when this work is undertaken.
3. **Milestone-specific checking and current-version schedules.** Separate intake from final assignment readiness and export v0.3 Room/Lighting/Light Points/Zone/Channel/Controller review views without using the incompatible v0.1 exporter.
4. **Refine grouping from the real proof.** Capture routing, capacity, emergency and compatibility constraints discovered in one room before building an optimizer.
5. **Develop later delivery support.** Routes/lengths, connections/configuration, BOM, release, field-change control, commissioning and as-built output follow the verified markup/model round trip.

Do not expand the model solely to describe every future stage before the first proof. Existing narratives, references and the discrepancy record are enough to document early findings while the missing structured functions are developed.

## Audit Basis and Limits

Reviewed the current architectural intake, lighting playbook, canonical v0.3/v0.2 pages, reconciliation rule, checklist, roadmap, and `model_spaces.py`, `model_hierarchy.py`, `export_review.py`. The first two check entered model data and emit derived JSON; the exporter consumes v0.1 only. The v0.3 schema contains no PDF boundary geometry, daylight polygons, route topology, detailed device configuration, control-review statuses, approval register, or commissioning results. Supporting method exists for several of these activities, but an end-to-end production pipeline has not been demonstrated.

Owner: KIS Solutions. October 2026; owner-directed workflow and local capability audit. Draft pending project proof.
