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

WikiJS owns the shared electrical lighting knowledge: space vocabulary, room-by-room energy-code analysis, control-device selection/configuration, decision trees, and the application guide. This repository owns the LV project model, extraction/reconciliation workflow, electrical grouping, implementation checks, and markup/output conventions. General application-guide/code-profile drafts now live in WikiJS; legacy local filenames are navigation-only pointers. Local directives specialize system compatibility and project execution without weakening applicable requirements. See the [repository boundary](../governance-and-doctrine/repository-boundary.md).

Redesign is conditional: identify a deficiency or implementation opportunity, establish authority to propose a change, document the proposal and its approval, then update the applied implementation while preserving the original scheme. A confirmed model decision alone does not establish approval by the responsible party. Unclear intent requires clarification, not an invented default.

## How to Read Readiness

This is an October 2026 audit of the local documentation and tools, not a declaration that a particular project has passed its milestones. **Method available** means there is enough documented guidance for a supervised manual/agent pass. **Checks implemented** means software checks entered data. **Development needed** means an output, rule, or round trip has not been implemented/proven. Passing synthetic checks does not prove plan extraction, source completeness, physical coverage, or an editable PDF round trip.

## Full Design and Delivery Cycle

| Step | Work and reviewable output | Enough now | Development or proof still needed |
|---|---|---|---|
| 1. Establish basis | Source register, sheet/revision matrix, scope, selected code basis, and who may authorize departures | Method and source/code-basis records available | Resolve governing discipline revisions on the actual project; explicit change-approval structure remains to be developed |
| 2. Inventory rooms | Architectural room list, neutral untagged-area entries, served levels, discrepancy list, editable boundary review | Architectural-first method and Space records available; entered membership checks implemented | Independent extraction/completeness review; automated boundary authoring remains unimplemented; owner-reported Bluebeam Polygon edit/readback proven in the beta workflow |
| 3. Establish areas | Architectural area labels first; reviewed measured areas where needed, with scale/boundary evidence | Area/basis/note fields and measurement directives available | Owner CAD area takeoffs; markup polygon check areas only; native Bluebeam Area measurement compatibility remains separately unproven |
| 4. Extract lighting and controls | Source Lighting Schedule, Room Schedule, Lighting Fixtures takeoff, Light Points, original MEP control intent, emergency observations | Types, occurrences, source references, source groups, and normal/emergency records available | Supervised extraction and independent fixture/symbol reconciliation; current source-review CSV exporter implemented; formatted workbook and complete exclusion register remain to develop |
| 5. Check the MEP scheme and resolve authorized gaps | Owner-confirmed room classifications, WikiJS/code references, per-function findings, scoped narrative authorization and approved interpretation/narrative where needed | Manual review/fallback handoff, Space code references, decisions, and open items available | Vocabulary/profile completion in WikiJS; status/approval fields, per-function assessments, source/applied/proposed sequence separation, automated code matching and narrative generation not implemented |
| 6. Select LV implementation | Confirmed LV fixture/driver loads, compatible outputs, candidate sensors/switches/controllers reproducing MEP behavior | Load basis, compatibility, device registers, and selections available | Product evidence and coverage/layout review; detailed device configuration and approval-of-departure records incomplete |
| 7. Assign zones and equipment | Functional zones, independent controller outputs, emergency command/backup paths, physical equipment identity | Hierarchy and Space references/checks implemented | Detailed source-to-implementation mapping, locations, sensor coverage, all outage paths, and project emergency performance review |
| 8. Group supply channels | Light-to-channel assignments, limits/margins, units and aggregate capacity, reviewed one-room grouping | Arithmetic, reference, output-capacity, and declared backup checks implemented | Grouping remains manual; routing practicality/product constraints need review; no optimizer |
| 9. Produce first design markup | One-room or one-sheet LV review PDF, IDs/legend, supporting load/assignment tables, open items | Model provides IDs, point anchors, relationships, and derived values | Full PDF writer/label layout and arbitrary frame transforms remain to develop; live-annotation gate implemented, tested Bluebeam Polygon readback owner-reported proven |
| 10. Coordinate installer package | Locations, routes/endpoints, cable selections/length basis, controller/device schedule, connection details, quantities and sequences | Inputs partly available; v0.1 CSV exporter remains usable for v0.1 only | device/channel/installer schedules and selected BOM, routing topology, calibrated lengths, detailed device/connection output and installation rules |
| 11. Review and issue | Approved scope/revision, resolved release blockers, coordinated package and approval record | Manual review can use existing decisions/open items | Formal release checklist, approval tracking and complete cross-deliverable reconciliation |
| 12. Installation and field changes | Substitution/field-change log, impact checks and revised affected outputs | Stable IDs and source/decision provenance support revision review | Defined change/diff workflow and reliable drawing/model round trip; authorized field changes still need documented approval |
| 13. Commission and close | Function tests, deficiency closure, accepted configuration, final schedules/markups and as-built record | Normal/emergency intent provides part of the test basis | Test protocols/results, coverage/daylight testing, installed configuration and as-built reconciliation not implemented |

## Milestone Review Points

For the M2 owner review, use the [plain-language checklist](../../templates/m2-user-review-checklist.md). Extraction/verification agents prepare the evidence and reconciliation; the owner reviews findings and records scoped acceptance. It supplements the milestone below without moving code/design approval into M2.

| Milestone | Evidence to review | Pass condition for the scoped work |
|---|---|---|
| M1. Room inventory | Independent architectural inventory, omission/identity discrepancies, boundary review | Every observed Space is accounted for; omissions reviewed and causes established or explicitly undetermined; unsupported facts remain unknown. Boundary and area acceptance can remain pending |
| M2. Source lighting/control intake | Initially completed Room Schedule, Lighting Schedule, Lighting Fixtures and Light Points; independent verification against the source set | Physical fixtures/counts and applicable control observations are reconciled; missing/conflicting information is explicitly flagged; nothing is silently filled in. Area takeoff and classifications are reviewed as their evidence becomes available |
| M3. Control check and interpretation | Owner-confirmed classifications and area/use/enclosure basis, selected code/WikiJS references, per-function findings, scoped narrative authorization and adoption decisions | Supported checks distinguish compliant, deficient, ambiguous source and no information; unavailable criteria remain not reviewed. Consequential unknowns, unapproved source-text interpretations/narratives and proposed departures block affected finalization; implementation opportunities are separately flagged |
| M4. First LV review markup | One reviewed room/sheet, source-intent mapping, confirmed loads for any quantified grouping, equipment/zone/channel assignments and editable PDF | Model/table/PDF identities and assignments agree; placement and edit/save/readback work for the tested annotation type; unresolved content is visibly provisional. This is review approval, not construction release |
| M5. Coordinated issue | Complete scoped installer package, source reconciliation, implementation/route/device details, changes and approvals | All release-critical scope, code interpretation, product, emergency, routing and coordination questions are resolved by the responsible reviewers; deliverables use the same revision |
| M6. Closeout | Installed configuration, functional test results, field changes and final documentation | Accepted field changes are reflected consistently; open deficiencies are resolved or explicitly carried in the accepted closeout record |

These are review gates, not values currently implemented in `project.stage`. That field still accepts `takeoff`, `provisional`, and `checkpoint`. Current [v0.4](../ontology/canonical-model/physical-intake-v0.4.md) offers inventory/intake/design data checks with deferred later findings. The legacy v0.3 checker mixes these concerns; its overall pass/fail is not an M1/M2 gate. Do not invent code classifications, areas, mounting heights, or channel assignments to make an intake model pass. Formal source/owner milestone acceptance remains a review task; the phase checker does not discover missing source items or implement a complete M3 code evaluator. Until then, record gate evidence and scope in the project review checklist and retain all checker findings.

## Room Classification and Controls Narrative Handoff

Follow the [WikiJS classification and controls review playbook](https://github.com/kissolutions/knowledgebase_wikijs/blob/main/design-playbooks/room-classification-and-controls-review-playbook.md); it owns the general procedure and selected-code source-text fallback. The LV project applies these gates to the existing review records:

1. After architectural inventory, retrieve candidate matches from WikiJS space-type entries, including synonyms. Preserve source labels; propose Building Code Space Type and Energy Code Space Type independently with use evidence, alternatives and unknowns. Do not derive either solely from the other or create lighting zones from a classification.
2. Obtain owner confirmation of the room classifications and the inputs needed for dependent analysis. Record owner/date/basis and affected Space IDs. Source extraction may proceed concurrently, but classification-dependent conclusions remain provisional. A confirmed room type is not permission to assign missing controls.
3. Extract the source scheme by function: dimming, manual controls, on/off behavior, occupancy/vacancy sensing and time switches; assess daylight/emergency interactions as relevant. Check all available source roles before declaring a gap. Preserve known functions and identify ambiguous, missing or supported not-applicable functions separately. For incomplete rooms, seek scoped owner authorization to propose controls using WikiJS, a specific owner narrative, or deferral. Reuse authorization that already covers those rooms/functions.
4. For authorized narrative buildout, use applicable supported WikiJS space-type controls guidance. If it is absent, unfinished, ambiguous or insufficient, follow WikiJS's primary-source fallback for the selected project standard/edition and amendments. IECC 2024 is an example only when it is the selected basis. Record source-text derivations, options, exception evidence and questions as proposals for owner approval; do not force a complete scheme from incomplete code guidance. Permission to draft does not approve the interpretation, options or final narrative.
5. Adopt only the reviewed, scoped approved narrative within established project authority. Preserve original source intent, owner direction, source/guide revisions and approval history. Narrow compatible LV sensors, switches, controllers, drivers, interfaces and configurations while preserving the required/approved operation. System incompatibility is a review conflict, not permission to weaken the requirement. Establish functional zones and channel/controller assignments only from supported operation.

Retain classification confirmation, narrative-development authorization and narrative/interpretation adoption as separate review evidence. Use existing Space descriptions, references, decisions, project narratives and `open_items[]`; no new unversioned schema fields are introduced. Missing source controls, incomplete WikiJS guidance and unresolved code interpretation remain distinct findings. M2 may finish source intake with documented gaps; M3 cannot finalize affected controls until consequential classification, authorization, interpretation and narrative questions are resolved. Manual/agent source-text review is documented method, not an implemented code matcher or narrative generator.

## On-Demand Owner Decision Review

Owner decisions remain recorded where they belong in the project: model decisions and references, discrepancy resolutions, room/fixture notes, review checklists, controls narratives and other retained review evidence. An owner-decision record/report is an on-demand analysis of that project information, not a separate primary document or mandatory duplicate register.

At any stage, the owner may request a sweep of the available project records for confirmations, corrections, subjective judgments, explicit overrides and directions. Identify the reviewed files/revisions and milestone scope. For each finding, show the affected stable IDs, original interpretation where available, adopted owner instruction, rationale, owner/date when recorded, current status and an exact source-record locator. Distinguish current decisions from superseded decisions, unanswered proposals and conflicts; leave missing metadata unknown rather than inferring approval from an agent statement. Link repeated mentions to the same underlying decision and flag inconsistent records for review. State retrieval gaps so an incomplete sweep is not presented as a complete project inventory.

The report may filter to explicit overrides or group the wider decision set by milestone, Space, fixture, controls topic or follow-up. Closing a discrepancy does not remove its decision history. Refactor accepted findings into clearer project records or propose reusable guidance when requested, preserving the original evidence and supersession links. A generated report does not change decisions or promote project-specific field judgment into framework doctrine. No new schema fields, automatic sweep or report exporter are implemented by this directive.

## Control Review Results

The owner has agreed to these two zone attributes, but they have not yet been added to the schema/generators:

| Attribute | Values | Meaning |
|---|---|---|
| `control_verification_status` | `not_reviewed`, `compliant`, `deficient`, `ambiguous_source`, `no_information` | Result of checking the extracted source scheme against the reviewed interpretation of applicable code for the functions assessed |
| `implementation_review_status` | `not_reviewed`, `typical_design`, `manual_review_required` | Whether implementation fits the typical approach or warrants discussion about a departure, limitation, or simpler arrangement |

A deficient finding needs clear source evidence plus the interpretation/reference it violates. Ambiguous source means information exists but cannot be resolved; no information means the relevant plan/legend/schedule/note/detail review found no applicable instruction. Compliant describes the reviewed functions and basis, not an unqualified certification of the whole project. A deficient zone always requires manual review; a compliant zone may also need implementation review. Unknown/ambiguous findings cannot be treated as compliant by default. Missing or unverified guidance leaves the affected check not reviewed; it is neither proof of source deficiency nor source no-information. An approved proposed narrative does not retroactively make the originally incomplete source scheme compliant.

Retain separate occupancy, daylight, manual-control, and scheduling findings when necessary. The per-function structure and zone-summary precedence need a later contract decision; do not collapse an unresolved daylight sequence into an occupancy pass. Retain source locators, code/guide edition and revision, reasoning, review scope, reviewer/date, and any proposal/approval in the project review record. Use existing `open_items[]`, decisions and references where appropriate; do not insert unsupported new fields into v0.3 instances. Record deviations and their actual approval separately from both status attributes.

## Progressive Markup Readiness

M2 source schedules capture voltage beside source wattage with electrical-interface evidence. M4 uses separately confirmed selected channel-interface voltage, AC/DC, CV/CC and CC current/range; incompatible inputs can increase required channel/controller-output capacity even below the watt ceiling. Follow [v0.5 electrical interfaces](../ontology/canonical-model/electrical-interfaces-v0.5.md), preserving existing owner/source decisions. Older model passes do not prove the new checks; explicit upgrades leave new values unknown for review.

Early markups can precede complete controls analysis. Follow the [enclosed/logical boundary instructions](architectural-space-intake.md#enclosed-rooms-and-logical-open-areas) and [annotation naming/identity convention](architectural-space-intake.md#annotation-type-naming-and-identity). Enclosed rooms follow architectural walls; logical open-area subdivisions may be approximate proposals for owner editing, with their observed basis and uncertainty retained. That permission applies to draft geometry, not invented source names/use, code classification or control behavior. Room-boundary markups need registered architectural sheets, stable Space IDs, traceable boundaries, and visible uncertainty notes. They do not need final channels, controllers, sensor quantities, or final code conclusions. Measured areas additionally require accepted scale/boundary evidence.

Fixture/source-control review markups need reconciled occurrences and evidence for the symbols, groups, and behaviors being shown. Distinguish source observations from proposed LV assignments through the legend. A provisional outline may identify an unresolved group; it must not present an invented sequence as MEP intent.

A quantified LV channel markup additionally needs confirmed channel-interface loads and product limits, preserved functional behavior, and reviewed controller/backup relationships for the scope being quantified. Unresolved rooms can remain visibly provisional while unrelated verified rooms proceed. No connected-load number is obtained by treating unknown watts as zero.

First prove one representative room or sheet. Use stable IDs on editable annotations; verify displayed-page crop/rotation placement, open/save behavior, and readback of changed geometry/IDs. Standard editable polygon annotations and native Bluebeam Area measurements are separate output capabilities. Promise native Area behavior only after the owner's editor recognizes it, permits boundary edits, recalculates area with the correct scale/units, and retains readable identity/geometry after saving. Do not require the full installer-package pipeline before attempting this small proof.

## Development Priorities

1. **Next experiment: one-sheet editable PDF proof.** Show room boundaries, fixture anchors/IDs and documented source control groups. Add provisional LV channel graphics only for load-confirmed scope. Record what can be edited and read back; keep native Bluebeam Area as a separate compatibility test.
2. **Small model extension: control review and change provenance.** Implement the agreed statuses with evidence, per-function findings and distinct source/applied/proposed states. Define who approved departures. Version the contract, update examples and run meaningful tests when this work is undertaken.
3. **Milestone-specific checking and current-version schedules.** Inventory/intake/design data phases and five source-review CSVs are implemented in v0.4. Develop later Zone/Channel/Controller/installer output views and reviewed spreadsheet writeback without using the incompatible v0.1 exporter.
4. **Refine grouping from the real proof.** Capture routing, capacity, emergency and compatibility constraints discovered in one room before building an optimizer.
5. **Develop later delivery support.** Routes/lengths, connections/configuration, BOM, release, field-change control, commissioning and as-built output follow the verified markup/model round trip.

Do not expand the model solely to describe every future stage before the first proof. Existing narratives, references and the discrepancy record are enough to document early findings while the missing structured functions are developed.

## Audit Basis and Limits

Reviewed the current architectural intake, lighting playbook, canonical v0.3/v0.2 pages, reconciliation rule, checklist, roadmap, and `model_spaces.py`, `model_hierarchy.py`, `export_review.py`. Legacy Space/hierarchy tools check entered data and emit derived JSON; their original exporter consumes v0.1 only. Beta 1 updates add the v0.4 physical registry, phase checks and v0.4/v0.3 source-review CSV export. The v0.3 schema contains no PDF boundary geometry, daylight polygons, route topology, detailed device configuration, control-review statuses, approval register, or commissioning results. Supporting method exists for several of these activities, but an end-to-end production pipeline has not been demonstrated.

Owner: KIS Solutions. October 2026; owner-directed workflow and local capability audit. Draft pending project proof.


## Controller/power topology readiness

Capture AHJ and area return-plenum status during basis/intake. After channel designation use [controller/power placement](controller-power-placement.md), [legend](control-system-markup-legend.md), and [companion contract](../ontology/canonical-model/controller-power-topology-v1.md). Supervised allocation method and companion checks are available; automatic location/routing optimization, manufacturer missing-data resolution and editable PDF output/readback remain to prove.

## Milestone Print and Markup Sequence

[Milestone review packages](milestone-review-packages.md) defines six printable packages without renumbering existing milestones: room boundaries; hatched-room light takeoff; zones/room devices after narrative lock; device-free micro channels; equipment location review; coordinated layers/cabling. Owner-returned room-device locations precede dependent routing. Parent/child zones and narrative status use v0.7; topology v1.1 supplies descriptive device/room identity. Markup manifest and schedule checks are implemented; automatic PDF overlay/layer/readback remains to prove.

## Open Framework Item: Exterior Lighting

**Status: unresolved. Owner flag: 2026-10-06.**

Define the exterior-lighting workflow before treating exterior designs as covered by the framework. Resolve exterior area/fixture ownership and takeoff, functional zoning and controls narrative, applicable code-review routing, power/driver/channel selection (including larger-fixture aggregation when compatible), outdoor equipment/enclosure and routing evidence, and review deliverables. Record decisions through the existing owner-review process; no default exterior sequence or hardware selection is established by this flag.

The accepted low-opacity wine/burgundy exterior room-map color is presentation guidance only. It does not resolve exterior lighting scope, controls, electrical compatibility or equipment suitability. Preserve known source intent and mark unsupported exterior design decisions as open. Shared exterior design/controls knowledge belongs in WikiJS; project/model/channel/markup implementation belongs in this LV extension.

## M1/M2 Beta Review Update

Follow [room geometry and physical intake review](m1-m2-beta-review.md). Room footprints use owner-reviewed edge notches with no slits; rare retained nested Spaces use frontmost dashed/deeper fills and `nested_in`. This room rule is distinct from the unchanged no-detour styling for control-zone/channel boxes. Package 1 uses **Area sf (check only)** and **Nested in**; both Package 1/2 carry the mandatory area/notch/nesting note. Owner-returned geometry establishes the working frame; presentation does not change smallest-containing served-Space membership. Deliver live Polygon/FreeText annotations and an identity register, with a zero-annotation build rejection. Apply owner section-count overrides, exact source tags, provisional schedule mappings, keynote-only types and explicit exterior holdouts under that playbook. Polygon readback is owner-reported proven for the tested Bluebeam workflow; retain scoped verification for other behaviors.
