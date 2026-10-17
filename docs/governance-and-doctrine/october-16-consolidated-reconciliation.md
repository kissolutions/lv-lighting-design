---
title: "October 16 Consolidated Framework Reconciliation"
page_type: governance
page_status: draft
confidence_level: medium
domain_primary: low-voltage-lighting
ai_role: authoring_rules
invocation_triggers:
  systems_present: [low_voltage_lighting]
decision_axes: [proposal_reconciliation, implementation_scope, shared_vocabulary]
related_pages:
  - "repository-boundary.md"
  - "roadmap.md"
  - "../design-playbooks/milestone-review-packages.md"
  - "../ontology/canonical-model/cable-route.md"
---

# Consolidated framework reconciliation — October 16, 2026

## Status and scope

This is the reconciled change specification, not an implementation-completion claim. Prepared from the October 16 handoff, the earlier pending LV discussions, current repository files, and the shared-framework review branch. No source project files, client quantities, project paths or project-specific defaults are imported here. Owner authorized publication of this reconciliation on October 17, 2026. Publication records the change specification; it does not mark the pending implementation complete.

Owner clarification controls interpretation: the named presentation views, register names, Full/Abridged Basis of Design markups, page ordering and detailed layouts are explicitly defined. Preserve them. Exploratory commentary surrounding those definitions does not reopen them. A defined deliverable can still have an unfinished reusable generator.

Verified repository baselines:

| Repository/ref | Revision | Meaning |
|---|---|---|
| LV main | `cc152a2` | A–H reconciliation and v0.9 bundle implementation already present |
| Knowledgebase main | `8bcc3f6` | Shared cable-selection guidance and vendor-neutral catalog already present |
| Knowledgebase `feature/engineering-state-peps-v0-1` | `8456a17` | Equipment/Device register, engineering acceptance, working-state versioning and package standard committed on a review branch; not merged into main |
| BAS main checked during handoff review | `c743f39` | Domain model reference; not the authority for the newly proposed shared presentation taxonomy |

The shared Canonical Vocabulary / Data / Workflow / Presentation convention layers were discussed but remain uncommitted. Do not confuse that with the already committed review-branch material. Repository versions and branch status must be refreshed before publication.

## 1. Shared conventions and named components fit together

The four shared contract layers organize the named components. They do not replace component names or prescribe identical visual styling across domains.

| Shared contract layer | Reconciled responsibility |
|---|---|
| Canonical Vocabulary | Meanings, identity, aliases and controlled terms: Equipment, Device, Internal ID, IDX, Parent ID, Location; Register, Schedule, View, Report, Set, Manifest |
| Data Contracts and Validation | Authoritative register formats, fields, requiredness, unknown handling, relationships, allowed values, structural/semantic checks and separately stated engineering checks |
| Workflow Contracts | Inputs, operations, outputs, authority, exceptions, completion and invalidation for placement/routing reviews, return reconciliation, milestone acceptance and reopening |
| Presentation Contracts | Exact named layouts, layer behavior, labels, editions, page order and generated schedules/reports |

Every addition identifies purpose, authority, validation and downstream use. Shared meanings belong in the knowledgebase; LV-specific records, rules, workflows and rendering behavior belong in this extension. No new agent-specific packaging or skills migration is required by this change.

### Component meanings

- **Register:** authoritative records with stable identity, basis and state. A spreadsheet/flat table can be authoritative; a rendered PDF is a view of that authority, not a second editable database.
- **Schedule:** a printable tabular rendering of register data. A named Schedule can be a specialized View; those labels need not be mutually exclusive.
- **View:** a named presentation over existing records. Preserve **Paired Fixture Schedule**, short form **Paired Schedule**, exactly.
- **Report:** a scoped assembly of data and derived findings. Scope entity is an input parameter (Space, zone, controller, level or route), not a new physical parent.
- **Markup layer:** a named annotation group with explicit authority/edit behavior. Some layers return owner input; derived Reach Lines do not.
- **Set:** an ordered composition of referenced components, with variant, edition, parameters and page order.
- **Manifest:** the inventory of a particular issue: component versions, files/pages/layers, source/model revisions and identity mapping. It describes an issued Set; it is not the Set definition or an engineering register.
- **Workflow:** a repeatable operation with review/state transitions and concise round records.
- **Rule:** a design/presentation constraint with basis and invalidation conditions.
- **Vocabulary:** allowed values and their definitions/version. Project fixture designations are project data, not a universal list of permitted fixture types.

Keep established names; aliases preserve discoverability if a name changes. Canonical IDs and schema field names must not be changed solely to match a display label. Existing `review_status` and `location_basis` vocabulary remains; do not introduce a competing `pinned` enum.

**Controls Narrative Register** remains the named deliverable. It presents the authoritative sequence records and zone/room assignments in the established **Controls Narrative Review** layout. Specify the register's data contract and its rendering separately; do not rename or duplicate the owner's deliverable to resolve a terminology preference. The existing review name remains a discoverable reference to the workflow/layout.

**BOM** remains a distinct orderable-line-item dataset under the shared review-branch model. **Quantity Schedule** is the defined provisional, not-for-procurement rendering of known engineering quantities. It does not silently become a selected procurement BOM. Purchasing complete assemblies and their included components must not be double-counted.

The BAS **Controls Scope Navigator** and **Controls Scope Infographic** remain named derived views over authoritative registers. Their names and purposes are compatible with this structure; LV does not need to copy BAS I/O ontology.

## 2. Routing architecture: merge the background proposals with the handoff

| Pending item | Reconciled disposition |
|---|---|
| Independent equipment locations | Required before pathway discovery. Record equipment/device ID, working frame, coordinates, location basis and review state independently of a bundle station. Preserve accepted owner placement. |
| Pathways distinct from cables | Required. Physical route segments/nodes carry geometry, constraints and installation costs before cable occupancy exists. A pathway is not electrically owned by a single PDU. |
| Cable-to-pathway assignments | Required. Record ordered traversals/attachments and derive pathway cable occupancy. Keep cable, circuit, conductor and source identities distinct. |
| Equipment assemblies | Reuse shared Equipment/Device and actual physical Parent Internal ID semantics. A rack/enclosure/panel can contain devices; proximity, electrical supply, served rooms and communications are separate relationships. |
| Co-located power sources | Multiple separately identified PDUs can occupy an assembly and share pathways/support infrastructure. Never combine their electrical identities because they are co-located. |
| Nullable conductor gauge | Permit unknown selection in the next versioned design contract; routing can proceed provisionally. Gauge-dependent voltage-drop/electrical checks remain unresolved until selection is known. Do not silently weaken v0.9. |
| Nominal design target | Add a separate optional target below/equal to the applicable design limit. The existing 95 W design cap and 100 W rating are distinct; 90 W is a project target when selected, not a new universal ceiling. |
| Highway versus drops (L) | Separate editable geometry, review state and workflows. Coordinate controller locations, electrical drop budgets and deliberately shared supports. Reusable drop reader/scoring/state remain unfinished. |
| Wall-to-deck markings (K) | Track runs-to-deck / stops-at-ceiling / unclassified, with wall type/rating evidence separately. Space boundary crossings are not penetration counts. Unclassified crossings remain separately reported. |

Pathways may contain alternate routes or geometric cycles. That does not authorize cycles in electrical distribution trees. Preserve the v0.9 bundle tree and served-set identities as its versioned contract; its electrical/tree checks must not be imposed on the new physical pathway graph. Do not resurrect superseded F's independent `cable_routes[]` shape as a competing authority.

### Reconciled iteration

1. Begin with established channel/light/control associations and independent provisional/held equipment positions.
2. Generate alternative pathway sketches using ceiling/access conditions, owner-confirmed exclusion/crossing zones, support and bend costs.
3. Review endpoint locations and pathway geometry; a reviewer may change either. Preserve held positions unless explicitly reopened.
4. Assign cables to pathways and derive occupancy, electrical lengths, conductor requirements and installation costs.
5. Develop and review fixture drops separately. Recheck the coupled electrical path and controller position when either system changes.
6. Repeat until the scoped review is accepted, carrying unresolved selections explicitly.

Pathway construction costs and cable installation/electrical costs remain separate terms even when jointly optimized. Count shared supports once through explicit sharing records, not by adding independent route totals. Alternative route quantities are comparisons, not additive project quantities. A route's acceptance is geometric/engineering scope-specific; it does not make unresolved electrical selections valid.

## 3. Complete A–T disposition

| Item | Baseline / disposition | Work remaining |
|---|---|---|
| A Room-family grouping | Already in main, LV and shared taxonomy | Reuse; family is independent of energy/building code classification. |
| B Axis-independent packing | Already in main | Reuse; no regression to row/column-only packing. |
| C 95 W correction | Already in main | Keep rating, maximum design and optional target distinct. |
| D Iterative placement/routing | Workflow doctrine in main | Implement independent locations/pathways and coupled recalculation; retain held-state semantics. |
| E Two voltage-drop budgets | Doctrine in main | Project-select budgets and calculate at actual interfaces. Do not universalize example percentages or add percentages at unlike voltages without a justified electrical model. |
| F Cable/conductor identity | Superseded by implemented v0.9 bundle contract | Extend versionedly for pathways; preserve cables/circuits/conductors and migration evidence. |
| G Feeds by demand | Doctrine in main | Reuse. Keep current checker evidence compatibility; no automatic four-feed default. |
| H Exclusions/bend costs | Doctrine in main | Implement owner review and route scoring. Open volumes are not automatically no-go. |
| I Reach Lines | Defined pending addition | Derived per controller/channel, separate visible layer, stable pair identity, return classification and reference metrics. |
| J Route PDF plus picture | Defined pending workflow | Request screenshot per level; PDF geometry remains authority; missing picture is reported, not a stop. |
| K Wall-to-deck | Explicit pending feature | Capture wall evidence; separate boundary crossings from penetrations; do not claim penetration costing complete. |
| L Independent drops | Direction fixed; mechanics expressly unfinished | Separate reader, state, scoring and optional support-sharing; resolve intra-channel wiring scope later. |
| M Architectural RCP base | Defined pending rule | Use RCP from initial issue; preserve existing owner frame and register background alignment for legacy projects. |
| N Paired Fixture Schedule | Exact presentation contract fixed | Generalize generator and connect selected type data; preserve all columns and row offsets. |
| O Room label layers / appearances | Defined pending requirements | Three label layers and full polygon metadata; appearance streams for every issued live annotation; viewer/editability verification. |
| P BoD publication edition | Owner-directed publication exception | Keep live authority and derived publication edition; provenance, layer preservation and no-readback gates. |
| Q Layer steps | Exact behavior fixed | Explicit milestone-only layer states, Everything, layer-panel use, bookmark convenience; optional step-page fallback. |
| R Full/Abridged sets | Definitions fixed | Reusable set assembler, generated contents and resource deduplication; no reopening of named layouts. |
| S Controls Narrative Register | Definition fixed, reuses M3 review | Generalize sequence-section rendering from authoritative records and room-device counts. |
| T Cable summary / Quantity Schedule | Definitions fixed | Generalize report and schedule; preserve unknowns, scoped alternatives, exclusions and not-for-procurement status. |

## 4. Preserve the exact presentation contracts

### Paired Fixture Schedule

One block per exact fixture designation: designation/context header, ORIGINAL row, then shaded LV row. Only the header uses column 1, for the designation. Every other row starts in column 2. Context names control requirements and served rooms. The columns are: Designation; Row; Description/part; Qty; Input V; Watts each; Driver; Dimming; Dim method; Compat. group; Channels; Status.

ORIGINAL and LV use identical columns for vertical comparison. Unknown LV selections read TBD; never populate them from source AC specifications. Quantity agrees unless a recorded type split explains a difference. A trailing machine key may repeat designation outside the visible format. Meaning is carried by labels as well as shading. This is a View over source and selected records, not a third set of fixture facts.

### Basis of Design Set

**Full** is the default. One cover with generated contents and legend; per level: untouched reference electrical plan, combined **BoD Plan / Basis of Design Plan**, then individual **Milestone Plan** pages in milestone order. Omit a milestone page where that level has no work. Append schedules once after all levels: Paired Fixture Schedule, Controls Narrative Register, Cable and Routing Summary, Quantity Schedule. Room List remains a defined schedule to add; its reusable rendering and final insertion position are pending.

**Abridged** is cover/legend plus the combined BoD Plan for each applicable level, without appended schedules. The established baseline omits electrical reference pages; the handoff's optional inclusion question is an enhancement, not a reason to withhold Abridged. Do not repeat a cover per level or hardcode the BoD Plan as absolute page 3 for every level. Generate an actual component-to-page map.

**Cover Sheet** retains project name/address/job number, title, variant, issue date, status, source/base-sheet identifiers, contents and legend from project/set records. **Milestone Plan** and combined **BoD Plan** reuse the same annotation sources with different layer subsets. Keep established names; the older “name awaiting confirmation” note does not undo the owner's subsequent clarification about explicit named deliverables.

Issue **Live** as editable authority. Offer the defined **Flattened** publication edition derived from the live issue, with layer visibility retained and clear edition/live-revision identification. The handoff describes both a BoD-Plan-only carve-out and a flattened Full set: reconcile these as publication-only copies of the set's plan views, never permission to flatten or replace any working/review deliverable. Schedules and source backgrounds may remain ordinary page content. A returned flattened edition is identified and not ingested as authoritative geometry.

Layer steps isolate their own milestone; no inherited room/context layers unless explicitly listed. Include RCP-only and Everything. Layer panel is primary, bookmark actions a convenience, optional static step pages the fallback. Viewer compatibility is tested, not inferred from one viewer's success. Deduplicate identical shared resources without losing annotation identity, layers, bookmarks or page associations.

### Controls Narrative Register

One section per sequence: number/ID, revision, title, full narrative, basis, required-functions table, then all assigned zones and their rooms in identical columns. Required functions include manual, occupancy/vacancy, dimming, light reduction, daylight, time switch and return after shutoff. Room/zone rows show actual implementation: level, control area, lights/types, control/on-off/driver types, sensor and wall-control counts, reduction and status. Preserve known absence as None and missing values as TBD. Counts come from device records and retain provisional status; grouping into sections does not duplicate physical devices.

### Cable and Routing Summary / Quantity Schedule

Summary compares alternatives per level: pathway footage, supports, bends, junctions, classified/unclassified crossings, actual penetration findings where supported, jacket and conductor footage, worst home run, budget findings and labor. Include per-controller feeds, load, length basis, gauge, drop result and state for each alternative. State selected cable basis, voltage interfaces, project budgets, plenum evidence and exclusions such as vertical travel, slack, terminations and waste. Missing levels/routes read TBD. Straight display lines, Manhattan estimates and calibrated polyline lengths are different bases; report which was used.

Quantity Schedule groups: power/distribution and used/spare outputs; source/LV fixture quantities and channels; control devices by kind/level; cable/pathway quantities by alternative. Parts remain TBD until supported by source/selection evidence, with source-specified distinguished from selected replacement. Mark **not for procurement**. Derive missing device level through its Space, flag disagreement rather than overwrite it, and retain unresolved level if neither is known. Report known load totals and unknown-load counts together; unknown is not zero.

### Room labels, reach lines and returned route sketches

- Room layers: name/number (fallback Space ID without invented names); area with basis/check-only qualification; building and energy code types with provisional marker and legend. Full Space data and basis remain in annotation contents. These belong to M1 and carry into subsequent sets. Detailed classification rendering does not create an approved classification.
- All live annotation classes need valid appearances and editable native geometry, stable `/NM`, identity register and scope-aware build checks. Merely adding `/AP` does not prove editability; verify actual save/edit/readback and representative rendering. The nonzero-annotation gate applies to expected live plan pages, not schedule/reference pages or labeled publication editions.
- Reach Lines run from controller to each served channel's light centroid, thin/dashed on their own default-visible layer. Identity is `REF-REACH-<controller_id>-<channel_id>`, not a sequence index. Store assignment revision. Missing anchors are reported rather than invented. Owner-location styling remains distinguishable while device-category colors are retained.
- Reach Lines are reference-only: never cable/drop length or quantity. Report served Spaces, placement inside any served Space, and maximum/mean reference reach. Outside placement is a review prompt, not an error. Report edits/deletions and regenerate them. Exempt only recognized reference-class annotations from authoritative return matching; an arbitrary unknown `REF-` ID is not a blanket bypass.
- Route sketches start as one-line alternatives on `ROUTE <letter> - <name>` layers. Segment at junctions and controller stubs. Connectivity uses calibrated geometry and a declared tolerance, not names or color. New sketch lines are explicitly classified in the route-intake workflow; layer/subject/color can suggest route ownership but cannot silently assign an existing canonical identity. Unassigned/ambiguous lines are reported. Keep strict identity rules for already-issued device and cable/bundle returns.
- Request live PDF and per-level picture. Picture explains intent; it never supplies or silently corrects coordinates. Process PDF-only returns with the missing-reference note. Report discrepancies for resolution.

## 5. Earlier beta material: retain useful findings, reject regressions

### October 3 Beta 1

| Items | Reconciled disposition |
|---|---|
| A1–A4, A8–A9 architectural boundaries, inventory, finish evidence, agent guidance and evidence comments | Present in current intake/playbook guidance; reuse. |
| A5 automatic inventory-only for unlit corridors; A10 test of that behavior | Superseded. Record the corridor and unresolved lighting scope; empty light lists are permitted without inventing an exemption flag. Do not add a test enforcing the rejected behavior. |
| A6 default zones; zone portion of A7 | Superseded by physical-first v0.4+. Each light has one primary served Space; no placeholder zones at intake. Functional zones follow supported narrative/control direction. |
| B1/B3/B4 circulation definitions, duplicate heading, room vocabulary | Current shared vocabulary covers circulation and needed room names; vocabulary does not complete room-specific control playbooks. |
| B2 corridor sensing | Keep in edition-specific guidance backlog; do not promote a project expectation to a universal rule. |
| C1/C3 absent schedule/controls and source search | Covered by current source/intake and narrative-authority guidance. Missing data does not authorize fabricated controls. |
| C2 dimensions versus area | Keep source dimensions distinct from measured/calculated area; current scale/area evidence guidance applies. |
| C4 review exporter | Implemented; do not recreate the old v0.3-only gap. |
| D withdrawn claims; E project corrections | Do not implement withdrawn proposals or publish project-instance corrections. |

Later room notching/nested-Space rules remain distinct from control-zone/channel presentation. Keep accepted notches, no hairline slits, rare nested dashed/deeper footprints and area disclaimers. Keep primary served-Space membership independent of presentation. Older “stepped channel outlines / no outline overlaps” recommendations cannot override the owner's later simple box/dashed swallowed-outline rule. A box containing an unrelated light is a presentation issue to explain, not an instruction to change electrical membership.

### October 5 F-1–F-33 backlog

These IDs remain traceable. “Recorded in main” is not equivalent to completed guidance or executable validation.

| IDs | Reconciled status / disposition |
|---|---|
| F-1–F-7 | Room/application playbooks and sensor-system selection remain shared backlog. Some edition-specific requirements exist, but the new handoff does not complete these playbooks. Beta sequences are scoped precedents, not universal code requirements. |
| F-8 | Still open: current enclosed-office page retains the reported 10/20-minute inconsistency and legacy citation tokens. Requires source-backed correction separately. |
| F-9 | Shared interior-space vocabulary now rejects a universal 250 SF definition; edition-specific playbook cleanup remains open. |
| F-10 | Full 2018 profile completion remains open; the later 2021 additions do not close it. |
| F-11–F-13 | Defaults, classification examples and reviewed application examples remain shared development/review work. |
| F-14 | AHJ/code-basis fields and intake directives exist; completeness/evidence still require project review. Do not derive jurisdiction from mailing city. |
| F-15 | M3 review layout and zone hierarchy are documented. Full review-state/evidence model remains incomplete; join the Controls Narrative Register and shared acceptance work without creating a new primary owner-decision register. |
| F-16 | Existing workflow permits scoped owner narrative/gap-filling authority. Preserve that path; no automatic redesign permission. |
| F-17 | Verified product facts/constraints remain device-specific; no blanket assertion that every LV system lacks a combination sensor. |
| F-18 | Emergency/exit guidance remains open. Routing/presentation changes do not resolve it. |
| F-19 | Source/selected voltage, AC/DC, CV/CC and driver/interface work substantially implemented in v0.5/v0.6. Type-level selections, complete schedules and reviewed multi-light CC topology remain distinct gaps. |
| F-20 | Type-level selected input/application and consistency validation remain pending; prerequisite for reliable Paired Fixture Schedule aggregation. |
| F-21 | Source-type and per-light exports exist; selected LV-by-type schedule gap is addressed by the defined Paired Fixture Schedule, whose reusable generator remains to build. |
| F-22 | Multi-light CC series/parallel topology remains unsupported. Matching nominal voltage/watts alone must not bypass `cc-topology-review`. |
| F-23 | Ordering-code evidence rule/product research remains pending. Preserve unresolved options and source versus manufacturer basis. |
| F-24 | Physical dimming capability exists; selected dimming method still needs its own data/export contract. Do not substitute legacy zone driver labels. |
| F-25 | Physical capability independent of narrative is existing doctrine. Type-wide selected-input consistency and approved splits still need implementation. |
| F-26 | Per-room/type dimming requirement and fixed commissioning trim interpretation need explicit traceable fields; include in narrative-to-fixture cross-reference. AC/DC remains a physical interface fact, not invented from narrative. |
| F-27 | CC current/compliance checks exist; nominal-only evidence handling and precise missing-value feedback need completion. |
| F-28 | Existing provisional-export banner is useful but not equivalent to per-value placeholder provenance. Explicit dry-run/electrical evidence status remains pending. |
| F-29 | v0.8 section-count/assembly identity partly addresses modular runs. A true continuous multi-fed light still needs a supported fed-section model; do not duplicate full load or count both assembly and pieces. |
| F-30 | Zone/narrative review and parent/child records exist. Explicit selected light/type membership and automated narrative-to-zone checking remain to complete; never infer authoritative membership from rendered boxes. |
| F-31 | Compatibility and independent-control doctrine exists. Mixed-type CC grouping depends on the still-unimplemented reviewed topology. |
| F-32 | Per-zone watts-only lower bound versus actual channel count remains an unimplemented comparison view. Label lower bound as theoretical, not feasible packing. |
| F-33 | Milestone/markup conventions now cover substantial scope. Reconcile remaining renderer/detail/readback work with I–T; supersede trial detours/nonoverlap assertions with later owner rules. True-scale return and enlarged reading-copy roles remain explicit. |

## 6. Other pending discussion items not lost in A–T

| Item | Treatment |
|---|---|
| General Class 2 cable selection and multi-vendor catalog | Already committed to knowledgebase main. Catalog remains vendor-neutral and extensible; individual manufacturer candidates/installation approvals keep their own evidence state. |
| EPS fixture power aggregator | Existing owner directive, still pending first-class multi-input/one-output topology and electrical validation. Keep distinct from sensor aggregator and ordinary QDCD. New assembly/pathway records do not themselves implement it. |
| Exterior lighting | Still unresolved scope/control/equipment policy. Map color is presentation only; retain excluded/unserved fixture reasons. |
| M3 scope, daylight and narrative/fixture cross-check | Existing directives remain: owner-level sequence specificity; deferred commissioning/photometry; explicit daylight yes/no/unresolved with edition/evidence; separately recorded bidirectional cross-check. No new duplicate review. |
| Area precision | Check-only areas generally; accurate second pass near applicable code thresholds. Labels retain basis and rounding does not affect threshold calculations. |
| Switch/sensor placement | Source electrical-plan positions first, accepted owner returns prevail, existing fallbacks only when usable source positions are absent. RCP background choice does not change this evidence priority. |
| Display rounding and draw order | Calculated display quantities round upward to zero decimals; model/check precision remains. Text stays in front. Rich label layers do not repeal these rules. |
| Lighting-selection-team deliverable | Paired Fixture Schedule supplies the explicit source-versus-LV comparison. It can be issued early with LV TBD; avoid presenting channel counts or selected input as known before design establishes them. |
| Owner decision review | Keep the on-demand sweep/report of existing project decisions. No unsolicited second authoritative decision register. |
| Engineering state / PEPS / working-state versioning | Already on shared review branch, not main. Align route iterations with current/previous working states and immutable accepted baselines; retain concise round findings, not unlimited full working snapshots. Do not silently merge the branch as part of LV reconciliation. |

## 7. Genuine unfinished choices and implementation boundaries

Do not turn these into blockers for the already defined presentation contracts:

- Drop geometry initialization, its scoring method, explicit shared-support ownership, and fixture-to-fixture wiring scope.
- Exact schema/migration shape for pathway graph, independent placements, equipment membership, cable traversals, nullable gauge and target wattage.
- Complete selected-input/type data model, dimming-method fields and evidence statuses needed by schedules.
- Room List insertion position, optional electrical reference in Abridged, optional static step-page generator.
- Tested generalized native annotations, PDF appearance/OCG construction, publication conversion and edit/readback across required viewers.
- Wall evidence/penetration costing and hard-ceiling access policy.
- Project choices of cable product, shielding, plenum rating, conductor gauge, budgets and unresolved over-budget runs. These stay with the project, not in framework defaults.

The supplied scripts demonstrate approaches, but contain hardcoded project files, IDs, placements and selected assumptions. Extract algorithms and replace project dependencies with explicit inputs and synthetic tests. A script in the handoff is not proof that the framework CLI supports the same operation. No claims of general PDF render parity or route validation follow from the project-reported results alone.

## 8. Coordinated implementation and publication sequence

1. Reconcile shared convention definitions with the existing Equipment/Device and acceptance review branch; keep branch work identified rather than relabeling it uncommitted.
2. Incorporate explicit LV workflow/presentation contracts and links. Retain established component names and exact formats; mark generator readiness separately.
3. Introduce the next versioned physical-location/pathway/cable contract with migrations preserving stable identities and historical v0.9 support. Do not infer unknown geometry, gauge, electrical selection or owner approval.
4. Implement independent return/review workflows and invalidation. Device relocation invalidates connected route/drop calculations; geometry return invalidates dependent lengths, electrical results and labor, not accepted light membership.
5. Generalize named schedule/view/set generators, live annotations and publication copies; connect actual source registers rather than project constants.
6. Verify meaningful failure cases: identity loss, ambiguous route assignment, held-location movement, unknown gauge/load, mixed voltage/current topology, alternate-route double counting, manifest/page drift, missing appearances, accidental review flattening and lost OCG/editability. Run repository gates for any schema/engineering implementation.
7. Inspect the public diff for project data and publish the coordinated changes after the applicable review. Shared and LV repositories require separate commits linked as one change package; they cannot be one atomic Git commit.

This reconciliation does not merge the shared branch, change executable schemas, run a design optimization, or claim those pending generators are implemented. It consolidates the work so the next implementation uses one coherent specification without losing older open items or re-asking settled presentation decisions.
