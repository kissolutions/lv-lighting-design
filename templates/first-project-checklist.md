# First LV Project Workflow Checklist

Copy this template into approved project storage outside Git. Follow the [workflow/readiness map](../docs/design-playbooks/lv-project-workflow-and-readiness.md); this checklist records review gates, not schema `project.stage` values.

## Basis and authority

- [ ] Register project/model revision, source filenames/revisions, sheet/page identities, actual displayed dimensions and rotation.
- [ ] Resolve the source/revision basis used for architectural/electrical overlays; retain discrepancies and locators.
- [ ] Record scope, project energy-code basis and the responsible review/approval parties. WikiJS supplies general electrical lighting guidance.
- [ ] Preserve the MEP control scheme as the starting basis. Redesign only when authority exists and adoption of the proposed departure is approved.

## M1: Architectural room inventory

- [ ] Start with Architectural Floor Plan or Dimension Plan. If unavailable, flag the missing source and keep inventory provisional.
- [ ] Have a separate agent build an independent simple Space inventory before comparing the initial list.
- [ ] Flag omissions, unsupported entries, duplicates and label/level conflicts; owner-review corrections and omission causes, using “cause undetermined” where necessary.
- [ ] No assumptions: every fact needs source evidence or identified owner confirmation. Preserve accepted owner corrections; unsupported values and untagged uses remain unknown.
- [ ] Account for untagged rooms, circulation, stairs and unlit service areas. Describe location neutrally; do not infer purpose from shape.
- [ ] Compare architectural floor/RCP/electrical labels and retain discrepancies. Relate open-to-below footprints to their occupied/served Space.

## Boundary and area review

- [ ] Capture clear architectural area labels with high-confidence transcription/association notes, units, locator and revision; use `area_basis: source_document`.
- [ ] Trace editable closed polygons/rectangles for each scoped room/Space on the architectural floor/dimension plan, otherwise the applicable RCP; use ID-linked uncertainty callouts where a footprint cannot be resolved.
- [ ] Follow enclosing walls for physical rooms. For open logical areas, propose approximate boundaries from observed furniture, circulation, partial walls, features and supported ceiling changes; clearly label proposals for owner vertex editing.
- [ ] Preserve exact source names; identify proposed names/use explicitly without inventing room numbers or code/control classifications. Keep parent-area context and review overlaps/gaps without double counting parent and subdivision areas.
- [ ] Put the room name in Subject, Space ID/boundary basis/review notes in Comments, actual author in `/T`, and unique annotation ID in `/NM`; retain the annotation-to-Space mapping and editable labels where needed.
- [ ] Use the applicable view's printed architectural scale; verify PDF applicability against dimensions where available and resolve resizing/missing/conflicting scale before accepting measurements.
- [ ] Preserve source area and later measured evidence separately; owner-review conflicts rather than overwriting them.
- [ ] Prove annotation edit/save/readback before treating the owner-return loop as supported. Reconcile edits by ID and retain provenance.
- [ ] Test native Bluebeam Area recognition, boundary editing, correct scale/units, automatic recalculation and ID/geometry readback before promising native output.
- [ ] Describe consequential full/partial-wall/open edges narratively with evidence; discuss uncertain control consequences.

## M2: Source lighting and controls

Use the [M2 owner review checklist](m2-user-review-checklist.md) for the human review meeting and scoped acceptance. The technical checks below remain the extraction/verification basis.

- [ ] Initially complete Room Schedule, Lighting Schedule, Lighting Fixtures and Light Points; independently verify them against the registered source set.
- [ ] Preserve all fixture schedule marks, description/load/driver notes and manufacturer options; flag missing/conflicting facts.
- [ ] Record source driver architecture (driver/driverless/other/unknown), with descriptions for other and source notes for supported integral/remote arrangements. Preserve the selected LV driver architecture separately; do not substitute CV/CC or dimming labels for this classification.
- [ ] Capture [source voltage beside source wattage](../docs/ontology/canonical-model/electrical-interfaces-v0.5.md), with AC/DC, nominal/range, CV/CC mode and drive current where supported. Identify fixture-input versus module-input/driver-output evidence; retain ambiguous wording and unknowns rather than inferring from watts.
- [ ] Give each physical occurrence a stable internal ID; count by sheet/Space/type and reconcile repeated/duplicate coverage and exclusions.
- [ ] Apply [linear run extraction](../docs/design-playbooks/m2-linear-fixture-extraction.md): connected/apparently continuous same-type paths count once through corners/repeated marks; clearly disconnected paths count separately. Check source linework beneath overlays, describe quantities as runs, and flag uncertain continuity, full-path length/load and feed/section topology.
- [ ] Apply [M2 fixture display numbering](../docs/design-playbooks/m2-fixture-numbering.md): consecutive type blocks across the project, room subsets together, clockwise from top-left within room/type; retain unique labels, a type-block register and label-to-permanent-ID mapping. Review ambiguous traversal and coordinate any display-label revision across tables/PDFs.
- [ ] Assign lights to the occupied/served Space, retaining their independent source sheet. Keep numeric mounting height unknown where only qualitative high mounting or an unassociated ceiling tag is supported. Create no default zones; run the served-Space sanity check after boundary derivation/counting.
- [ ] Extract source control symbols, legends, schedules, keyed notes, details and sequences; distinguish lighting from receptacle controls.
- [ ] Confirm substantial gray/hatched scope exclusions; inspect finish plans and review alcove/corridor/finish-transition boundary proposals.
- [ ] Preserve MEP group labels and source intent; inspect relevant notes/details before declaring no information. Do not fill gaps with a preferred room design.
- [ ] Preserve normal and emergency observations; a fixture suffix/battery note alone does not establish a complete operating sequence.
- [ ] Set `takeoff_status: reconciled` only after scoped source review. Software cannot detect fixtures/symbols that were never entered.

## M3: Check the extracted scheme

- [ ] Retrieve proposed room-type/synonym matches from WikiJS; preserve source names and independently propose building/energy classifications with supporting use evidence and alternatives.
- [ ] Record owner-confirmed classifications, owner/date/basis and remaining unknowns before final classification-dependent conclusions.
- [ ] Identify source gaps by dimming, manual control, on/off behavior, occupancy/vacancy sensing and time switches, plus relevant daylight/emergency interaction; preserve known functions and supported not-applicable findings.
- [ ] For affected rooms/functions, retain scoped owner authorization for narrative development, a supplied owner narrative, or deferral; confirmation of room type alone is insufficient. Reuse authorization already covering the scope.
- [ ] Assess WikiJS guidance readiness. For missing/unfinished/ambiguous guidance, use the selected-code primary-source fallback; retain exact sections, conditions, options, exception evidence and unavailable text as unresolved.
- [ ] Flag source-text interpretations and the proposed narrative for owner approval before adoption. Permission to draft and approval to adopt are separate; preserve source, applied and proposed behavior.
- [ ] Confirm LV-system compatibility preserves reviewed requirements and operation; record system conflicts without weakening the requirement.


- [ ] Review actual use, area/basis, enclosure, independent building/energy classifications and the selected code/edition/amendment basis.
- [ ] Check occupancy, daylight, manual-control and scheduling functions through applicable WikiJS guidance. Retain source/code/guide references, reasoning and review scope.
- [ ] Record zone verification as not reviewed, compliant, deficient, ambiguous source or no information. These agreed status fields are not yet in the schema; retain them in project review records meanwhile.
- [ ] Separately record implementation review as not reviewed, typical design or manual review required. Deficient findings always require manual review; compliant schemes can still have simpler implementation proposals.
- [ ] Retain per-function findings where mixed; unknown source information does not receive an automatic compliant result.
- [ ] Preserve proposals separately. Establish authority and approval before adopting a departure; confirmed model decision status alone is not external approval.

## M4: LV implementation and first markup

- [ ] Confirm selected LV load, driver/output compatibility and actual product limits; preserve original source AC watts separately.
- [ ] Confirm selected supply-channel input/output voltage, AC/DC and CV/CC mode independently of source voltage. Separate incompatible fixed-voltage groups before watt grouping; verify CC current/range and flag unmodeled multi-input CC topology. Review actual controller output capabilities rather than deriving controller count from watts alone.
- [ ] Reproduce specified/approved operation in LV functional zones and controller outputs. Preserve MEP stair behavior; use shared zones only when supported.
- [ ] Confirm relevant emergency signal source, monitored circuit, controller path, backup supply and outage operation independently.
- [ ] Group one representative room manually with confirmed loads, auxiliary load and selected limits; preserve independent operation and one channel per modeled single-input light.
- [ ] Check physical unit/channel/output capacities and aggregate budgets; distinguish integrated hardware from separate components.
- [ ] Inspect checker findings without inventing later-stage data to force an early intake pass. Maintain separate scoped milestone evidence.
- [ ] Produce one-room/one-sheet review markup with stable IDs, source/model revision, legend, source-versus-LV distinction and visible unresolved items.
- [ ] Prove page placement, editable annotations and save/readback; reconcile model/table/PDF assignments. This is review approval, not construction release.
- [ ] Use current-version review views; do not feed v0.3 input to the v0.1 CSV exporter. Use `generators.export_intake` for v0.4/v0.3 source-review tables. PDF generation remains to be developed.

## M5: Coordinated package and issue

- [ ] Coordinate equipment/device locations, routes/endpoints, cable selection/length basis, output/device schedule, connections/configuration, quantities and sequences.
- [ ] Resolve release-critical source, code-interpretation, product, emergency, routing and installation issues with the responsible reviewers.
- [ ] Retain approval evidence and issue all scoped deliverables at the same reviewed revision.

## M6: Field changes, commissioning and closeout

- [ ] Record substitutions and field changes, authorization/approval and their affected loads, controls, routes and deliverables.
- [ ] Reconcile accepted changes to the authoritative model and drawings without renumbering stable IDs.
- [ ] Verify installed control functions, coverage/daylight response and normal/emergency operation under the applicable test basis; retain results and deficiency closure.
- [ ] Save accepted configuration, final schedules/markups and as-built reconciliation with any accepted outstanding items.
- [ ] Capture reusable lessons as framework instructions/synthetic tests without copying client material into Git.

## Printable Review Package Checks

- [ ] Room boundary schedule before plans; known room tags/names shown; readable pagination.
- [ ] Fixture schedule and every Light Point ID grouped by type; lightly hatched room membership; undercounter/strip reconciliation.
- [ ] Narrative locked with owner decision; first-class open-office clusters and parent common control recorded.
- [ ] Room-device schedule includes ID/tag/name/Room ID/name/zone/subzone/function; wall switch/scene/dimmer positions start with electrical-plan evidence (accepted owner positions prevail), with door/entry/glazing fallbacks only where source locations are unavailable; occupancy/daylight sensors also start with source design locations; use tile/zone, wall/corridor or daylight-placeholder fallbacks only without usable source locations; placement basis and missing geometry recorded; returned locations reconciled.
- [ ] Micro-channel map boxes show assigned output at upper left and calculated watts at lower right; no devices; no invented output tags.
- [ ] Equipment schedule/proposed positions reviewed and returned with stable annotation/device IDs.
- [ ] Text brought to front; calculated values ceiling-rounded to zero decimals; enveloped boundaries dashed with other style retained.
- [ ] Final six PDF layers independently verified; editable annotation identity and human edit/save/readback checked before acceptance.


## M2 Source Schedule and Assembly Reconciliation

- [ ] Original MEP fixture schedule extracted with exact type suffixes, descriptions, available electrical/geometry/section facts and row/note locators; referenced-but-missing schedule retrieved or flagged.
- [ ] Original source schedule remains distinct from selected LV replacements; absence of a schedule is documented rather than inferred from design-build delivery.
- [ ] Curved/ring and mixed-tag paths reconciled against schedule, RCP and electrical circuiting/daisy-chain evidence; L4/L4A not merged from visual continuity alone.
- [ ] Physical fixture, source run, assembly and hardware-piece quantities distinguished; unresolved counts provisional and source-supported changes reconciled across IDs/PDFs/summaries.

## M1/M2 Beta Review Gates

- [ ] Owner-returned geometry and working page frame adopted without duplicate footprints; notches documented, no slits.
- [ ] Nesting derived in the same served-level frame; rare islands styled and Nested in exported.
- [ ] Both front sheets include the mandatory notch/nesting/area-check note; no summed overlapping areas.
- [ ] Live annotations and register reconcile on every plan page; zero annotations rejects build.
- [ ] Owner section-count decisions, assembly IDs, exact plan tags and unresolved suffix mappings recorded.
- [ ] Keynote-only types retain unknown electrical values; exterior holdouts retained with quantities and reasons.
