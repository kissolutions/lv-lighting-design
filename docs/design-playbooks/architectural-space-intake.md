---
title: "Architectural Space Intake and Lighting Assignment"
page_type: playbook
page_status: draft
confidence_level: medium
domain_primary: low-voltage-lighting
ai_role: prescriptive_standard
invocation_triggers:
  systems_present: [low_voltage_lighting]
decision_axes: [source_reconciliation, space_inventory, fixture_membership, control_zoning]
related_pages:
  - "lighting-design-playbook.md"
  - "../ontology/canonical-model/space-context-v0.3.md"
  - "../validation/space-intake-reconciliation.md"
---

# Architectural Space Intake and Lighting Assignment

## Required Starting Point

Start room/Space extraction with the Architectural Floor Plan or Dimension Plan. Register source revisions and each sheet's role, including architectural RCP, finish/flooring plans, wall-type legend/details, sections, electrical lighting/RCP plans, schedules, and keyed notes. Reconcile discipline revisions before relying on overlaid geometry. If the required architectural starting plan is missing, record the missing source in the discrepancy list. Electrical-only extraction remains provisional and cannot establish a reconciled room inventory.

### Confirm Large Shaded or Hatched Areas

During source registration and before completing the room inventory, identify substantial gray, hatched or shaded regions and ask the owner whether they are excluded from construction/lighting scope. These markings commonly indicate out-of-scope background, but confirm their meaning from the legend, scope notes or owner. Record the region, source locator and answer in the project scope record. Once exclusion is confirmed, omit detailed room/fixture takeoff there; retain the exclusion note rather than creating full Space records for every excluded background room. If unresolved, flag the affected scope and continue other supported intake. Shading alone does not establish that an area has no installed lighting.

Use architectural floor/dimension plans as the primary source for room names, numbers, occupied levels, and boundaries. RCP and electrical room labels are comparison evidence. A mismatch in name, number, or location between an architectural floor plan, architectural RCP, and electrical RCP/lighting plan must appear in the discrepancy list with both observations and exact locators. Do not silently select or overwrite one label. A reviewer resolves the identity while preserving the original evidence and stable internal IDs.

## Inventory Before Takeoff

Catalog tagged rooms and untagged enclosed areas, circulation, stairs, service voids, and chases. An absent room tag or absent luminaire does not justify omission. For an unnumbered area, use a stable internal ID, leave `room_number` null, and describe its observed level and grid/location neutrally. Purpose remains unknown unless supported by a source or identified owner confirmation; do not infer a chase or equipment-room use from its shape alone. Inventory-only unlit service areas may have empty light/zone lists; confirm their purpose before assigning a code type. Do not invent a source room number.

An unlabeled area is accounted for either as its own Space or within an adjacent Space under [the untagged-area rules](#when-an-untagged-area-is-its-own-space). Being inside another Space's footprint is not an omission. A corridor with no light depicted is still inventoried: flag whether lighting is existing, excluded or omitted. Do not automatically set `inventory_only` to suppress its eventual lighting/code review. The physical-intake checker permits empty lighting lists on ordinary Spaces without requiring that flag.

An open-to-below footprint above an occupied room is part of that room unless architectural designation, distinct use, or a reviewed design decision establishes a separate Space. Preserve the opening and its location in the room description. Do not create a second room merely because its lights appear on an upper-level plan.

## Milestone 1: Room Inventory and Source Verification

First establish a simple, complete room/Space list. The initial extraction agent supplies exact source names/numbers, occupied levels, stable Space IDs, and source locators, together with the editable boundary review PDF described below. Missing room tags receive neutral location descriptions, not invented room names or uses. Boundary uncertainty does not justify dropping an observed area from the list.

A separate verification agent builds an independent inventory from the architectural floor/dimension plans before comparing it with the original list. Apply the same source revisions and identified owner decisions, but do not use the original list as the checklist for finding spaces. Compare the two lists for missing spaces, unsupported entries, duplicates, and name/number/level conflicts. Flag every omission with evidence; review it with the owner to determine why it was missed and whether the extraction instructions need correction. If the cause is not established, record “cause undetermined” rather than inventing an explanation. Report discrepancies before changing the working inventory; incorporate accepted resolutions while preserving evidence and stable IDs.

Only after room-list completeness is reviewed, verify the other captured source information against the drawings and identified owner confirmations. Explicit architectural area labels may be captured during the initial extraction; accepting calculated boundary areas follows boundary/scale review. Energy-code interpretation and final zoning are later steps, not reasons to guess missing facts at this gate.

**Verification instruction: No assumptions are permitted in asserted source facts.** Every asserted fact must have a drawing reference or identified owner confirmation. The separately labeled logical-boundary proposals described below may use observed spatial clues for an approximate initial geometry; that limited permission does not convert inferred names, uses, boundaries or code classifications into source facts. Do not invent room numbers, infer the purpose of an untagged space, fill unsupported fields, or treat absent symbols as proof of absent installed equipment. Leave unknown values null/Unknown and flag the question. Keep owner decisions distinct from drawing facts. Existing owner-confirmed corrections must survive a new pass; a conflict with new evidence is a discrepancy for review, not a silent reversal.

The milestone deliverables are the reconciled simple room list, boundary review PDF, and discrepancy list with omission causes/resolutions where established. Pass when every observed space is accounted for, the owner has reviewed omissions and proposed inventory corrections, and each checked fact is supported or explicitly unknown/flagged. Open factual questions remain visible; the affected downstream design cannot be finalized until consequential questions are resolved.

### Circulation Reconciliation Before Completing M1

**Before completing M1, reconcile circulation separately from labeled rooms.** Explicitly account for untagged passages connecting rooms or primary Spaces. A distinct architectural corridor receives a proposed Space even without a room tag or depicted lighting. Use a neutral proposed name, preserve boundary evidence, and leave unsupported room numbers and code classifications null. Record unresolved identity, extent or association in the discrepancy list. Circulation included within another Space must lie within that Space's boundary and be described there.

Run this pass after drawing the initial room boundaries. The independent verification agent also performs it against the architectural plan, rather than relying on the extracted room list:

1. Trace circulation connecting rooms and primary open areas, including bends and connections into larger Spaces.
2. Identify distinct traffic passages bounded by walls or partitions. Apply [the untagged-area rules](#when-an-untagged-area-is-its-own-space); do not absorb a distinct corridor merely because its ends open into named Spaces.
3. Account for each passage as a proposed corridor Space or an explicitly documented part of a surrounding Space. Workstation aisles may remain within an open-office Space, and door alcoves may remain within the surrounding Space. Preserve the architectural evidence for the chosen treatment.
4. Flag uncertain endpoints, boundaries, finish transitions or Space associations for owner review. Use neutral proposal labels such as “Corridor – North/East”; do not convert a proposal into a source room designation or code classification.
5. Check the boundary review PDF for unexplained gaps and overlaps, including circulation between otherwise complete room outlines. A passage described as included in another Space must actually be inside its marked boundary; unassigned floor area remains an explicit discrepancy rather than being described as absorbed.

For each corridor endpoint and internal tracking split, record its boundary basis in the existing description or annotation Comments: wall/partition, finish transition, source-named use transition, or proposed open-area division. Retain the source locator and identify any approximate dividing line where the passage opens into a larger Space. A well-supported corridor does not make its open endpoints exact. Owner acceptance resolves the tracking choice; retain that decision and the original basis without turning the proposed line into a source wall or requiring separate lighting controls.

Record the result in the existing room descriptions, boundary review PDF and discrepancy list. Before M1 is complete, every observed circulation area must have an explicit Space association or a visible unresolved item. The owner may accept, split or merge proposed tracking Spaces while preserving their evidence and stable-ID history. These decisions do not create lighting zones; logical control zoning comes later.

## Architectural Room Areas

A width-by-depth label such as `10' X 15'` is dimension evidence, not an explicit square-footage label. Preserve it verbatim with its source in `area_note`; leave `area_sq_ft` null at initial extraction unless a separate supported area is available. A reviewed calculation or boundary takeoff may establish area later with its own basis. Do not silently turn nominal room labels into accepted measured areas.

During initial room extraction, look for square footage in architectural room tags and floor/dimension-plan annotations. When the printed value, units, and association with the room are clear, bring that area into the Room Schedule with high confidence. Use it as the preferred initial room-area source; do not defer an explicit architectural area until a separate measurement pass.

Record the value in `area_sq_ft` with `area_basis: source_document`, and retain the sheet/revision and exact label locator through the Space's source references. Use `area_note` to identify the architectural area label and its high-confidence extraction; preserve any stated net/gross or other area convention. High confidence describes the source transcription and room association, not independent confirmation of the architect's calculation. Do not infer an unstated area convention or assign a nearby number to a room without clear evidence.

An absent, illegible, ambiguously associated, or conflicting area remains unknown or explicitly flagged for review; no assumptions are permitted. Where no usable source area exists, leave the value null until a boundary takeoff with a verified view scale or an identified owner-confirmed estimate is available, with its own basis. The verification agent does not invent an estimate to fill the field. Later boundary measurements are comparison evidence: retain both observations and flag discrepancies rather than silently overwriting the architectural value. Do not treat an upper-level open-to-below footprint as additional occupied floor area.

## Boundary Markups and Drawing Scale

### When an Untagged Area Is Its Own Space

Spaces are architectural/use tracking units; lighting zones are later logical control units. Use architectural evidence to establish boundaries: walls/partitions, doors, finish or material transitions, documented ceiling changes and source room naming. Register and inspect finish plans when floor/RCP evidence is insufficient. Fixture layout never creates, splits or moves a Space boundary. A fixture straddling a boundary creates a membership question, not permission to move the boundary.

As an initial tracking heuristic, consider whether the area has a distinct architectural name/use rather than creating a Space for every leftover patch of floor. Preserve an actual source-designated vestibule or other room; the door-alcove rule below concerns untagged recesses, not every room called a vestibule.

| Observed condition | Initial Space treatment |
|---|---|
| Untagged three-sided door alcove opening onto a larger Space | Include in that Space; describe the recess and doors served |
| Distinct bounded pocket beyond an alcove's closing wall | Inventory separately even without a tag, door or luminaire; leave purpose unknown until supported |
| Traffic passage between opposing walls connecting larger Spaces | Propose its own corridor Space, lit or unlit |
| Finish/material transition within a corridor | Propose separate tracking Spaces at the transition; preserve the finish-plan locator |
| Unlabeled floor with no architectural evidence of separation | Include with the adjacent labeled Space sharing its finish/ceiling; flag unclear association |
| Short opposing wall segments that could be a cased opening | Flag interpretation; no arbitrary minimum length or aspect-ratio rule is established |

Untagged corridor names/extents remain logical-boundary proposals until owner review. Use neutral proposal labels; unsupported source room number/type remain null. A tracking split does not impose independent lighting control. Lights in an alcove belong to its served Space, with no automatic zone assignment.

### Check Behind Absorbed Alcoves

Before including an untagged door alcove in its surrounding Space, trace each wall closing the recess and inspect the area on the other side. The accessible recess and a distinct bounded pocket beyond its wall must not be combined merely because both lack tags. Limit the absorbed alcove footprint to the supported recess boundary; do not extend it through a separating wall.

Within the confirmed project scope, inventory a distinct pocket even when no room tag, door or luminaire is depicted. Use a stable Space ID and neutral location description; leave its purpose, room number and code classifications unknown until supported by drawings or identified owner confirmation. Do not call it a chase solely from shape or lack of access. Distinguish a depicted pocket from wall thickness, a symbol or uncertain linework by consulting architectural plans, wall details and applicable RCP/finish evidence. If that distinction or boundary cannot be resolved, retain a visible candidate outline/question in the boundary PDF and discrepancy list rather than silently absorbing or omitting it.

The independent verification pass repeats this check for absorbed alcoves. When a missed pocket is accepted as a separate Space, correct the surrounding footprint, check for gaps/overlaps and revisit any affected area or light membership. Preserve the earlier geometry and correction basis in the review history; retain unaffected IDs. Owner-confirmed purpose may then be recorded with its confirmation provenance. This physical-inventory correction does not create a default lighting zone.

### Enclosed Rooms and Logical Open Areas

The initial extraction pass must create an editable review boundary for every inventoried room/Space in the scoped plan views. Where a boundary cannot be resolved, provide a visibly provisional outline or uncertainty callout tied to its stable ID rather than omitting the area. Include untagged areas and inventory-only service spaces. Multi-level/disconnected representations may need several annotations for one Space; keep unique annotation IDs and the same Space association without duplicating the physical area or fixtures.

**Fully enclosed room:** Follow the architectural walls forming the enclosed area, using a closed polygon or a rectangle where appropriate. Prefer the interior finished-face footprint for the takeoff and record the convention; if wall-face evidence or an existing source-area convention differs, flag it rather than claiming an exact reconciliation. Bridge ordinary door openings along the enclosing wall line so the room outline closes. Keep true open connections, alcoves and uncertain partitions visible for review rather than manufacturing a full-height wall. Vector linework can assist tracing but must be checked against the rendered plan; a detected closed region is not automatically a room. For raster/scanned plans, trace from the rendered image and retain the precision limitations.

**Logical areas within a larger enclosure:** Distinct architecturally named uses such as reception, atrium, entry, seating, bar or elevator lobby may lack physical walls between them. Produce reasonable, approximate closed polygons or rectangles from architectural use/traffic evidence, counters, partial-height walls, finish/material transitions, architectural features and documented ceiling changes. Consult finish plans, RCPs and sections as needed. Furniture may clarify a source-designated use, but does not establish an unsupported source room designation. Fixture layout is not a boundary clue. A perfect dividing line is not expected; get close enough for owner review and vertex editing. Do not infer a mandatory lighting-control split from a tracking subdivision.

Keep an architectural label exactly as observed. If an agent proposes a logical area name/use or subdivision absent from the source, label it as a proposal, leave the source room number/type unknown where unsupported, and retain the source parent-area context. Do not invent a source designation or code classification. Proposals can be associated with stable candidate Space IDs, but only owner-reviewed accepted subdivisions become the finalized Space/membership basis. Preserve original names, accepted owner corrections and IDs during revision reconciliation.

Distinguish wall-following boundaries from logical-boundary proposals in annotation comments and the PDF legend; record the observed clues and any uncertain edges. All initial boundaries are for review, including apparently clear enclosed rooms. Approximate logical boundaries are permitted at this stage without requiring a discussion before drawing them; owner review is required before finalizing consequential area, membership or zoning conclusions. Maintain separate room/Space boundaries and lighting-control boundaries.

Account for parent/child open-area outlines explicitly. If a parent footprint is shown for context alongside logical subdivisions, do not sum its area again with the child areas. Flag overlaps, gaps or intentionally unallocated circulation for review; do not hide them to force an area total. Proposed-boundary areas remain provisional even with a valid scale. After geometry and measurement convention are accepted, retain their logical-boundary basis/limitations when recording a measured area; review uncertainty near any consequential threshold.

Place room-boundary markups on the Architectural Floor Plan or Dimension Plan when available and calculate takeoff square footages from those markups. Use the applicable RCP view as the fallback when the architectural floor/dimension plan is unavailable for the takeoff. Record that fallback and preserve any unresolved architectural-inventory limitation; an RCP measurement does not by itself reconcile missing room identities or unclear boundaries. Explicit architectural room-area labels retain their preferred initial-source status above.

Use the standard architectural scale printed with the applicable plan view, usually below the view, as the preferred source for converting markup geometry to real dimensions. Record the exact scale, its label locator, sheet/revision, and applicable view. Do not assume a customary scale from the room's appearance, reuse another view's scale, or treat one scale as applying to every view on a sheet.

Verify that the printed scale applies to the actual PDF geometry before accepting measured areas. Compare against labeled architectural dimensions when available, but do not assume that dimension text is correct when it conflicts with corroborating geometry. Resized/scanned PDFs, missing or illegible scales, not-to-scale views, or disagreement with dimension labels require a flag and verified calibration or reviewer resolution; do not silently replace the printed scale or invent one. A clear, applicable printed scale remains the preferred starting basis, with calibration used to resolve demonstrated scaling issues.

Keep closed, editable room polygons or rectangles tied to stable Space IDs and source room labels, with their coordinates and scale basis retained for later recalculation. Flag uncertain boundary segments for visual review before accepting the area's measurement. Use `area_basis: measured` for accepted markup takeoffs, and retain the source view, scale, measurement convention, and review status in the evidence/area note. A lighting-zone boundary remains distinct from the room's floor-area boundary.

### Scale Verification Using Repeated Architectural Features

**Verify questionable drawing scale using repeated architectural features.** When printed dimensions, room-area labels or the stated view scale conflict with drawn geometry, retain the conflicting observations and investigate the measurement basis before accepting calculated areas. PDF page properties establish the digital sheet size; they do not prove that a plan view retained its intended architectural scale.

Use clearly depicted suspended-ceiling grid modules as a scale check. First identify the ceiling region and its project-specific type from the RCP tags, legend or schedule, then establish the module dimensions applicable to that region. Source- or owner-confirmed sizes take precedence over typical-size hypotheses, including larger modules such as 4-foot by 4-foot where supported. Type letters such as B or C have no universal size meaning; never transfer one project's type mapping or an adjacent region's module size to another region.

Where size is not established, initially test nominal 2-foot by 2-foot or 2-foot by 4-foot modules only where the depicted ceiling system supports that interpretation. Measure several full modules between suspension-grid centerlines in both axes and at multiple locations within the applicable view. Distinguish actual suspension-grid lines from decorative panel scoring and partial perimeter tiles. Do not force an unidentified or nonstandard ceiling system to fit those nominal sizes. Record the ceiling type/region, module dimensions, their evidence and whether the size is source-confirmed, owner-confirmed or a provisional interpretation. Repeated agreement strengthens the evidence but does not turn an assumed module size into a source fact; do not assign an unsupported statistical probability such as 99 percent.

Use doors as a secondary plausibility check, preferring scheduled or explicitly dimensioned leaf widths. A nominal 36-inch leaf may be tested as an initial hypothesis for an ordinary commercial office door; it is not an asserted width for every small enclosed room. Keep leaf width, frame/opening width and clear passage width distinct. An assumed typical door width must not independently establish measurement scale.

Compare these checks with the printed view scale and available dimensions. Record the measured spans, module counts or door identifiers, tested real dimensions, resulting scale and source locators. Determine whether disagreement is consistent throughout the view, confined to particular text labels, or different between drawing axes. A consistent factor can suggest a scale mismatch; isolated or unrelated disagreements can suggest incorrect dimension text. Neither pattern alone proves the cause. As a diagnostic example, confusing 1/4-inch and 3/16-inch architectural scales produces reciprocal linear factors of 4/3 and 3/4, and area factors of 16/9 and 9/16. Do not require errors to follow a standard-scale ratio or be an order of magnitude apart.

An RCP grid check applies to that RCP view. Before using it to calibrate architectural floor-plan boundaries, verify registration and relative scale between the views using matching architectural geometry; do not copy one sheet's scale to another without that check. Different horizontal and vertical factors require a distortion discrepancy and separate resolution before accepting areas.

Preserve original dimension/area text alongside the measurement result. Document the selected calibration, supporting evidence and source locators, alternatives rejected with their reasons, reviewer decision and affected Spaces in the existing area notes, markup register and discrepancy list. Unsupported calibration and its calculated areas remain provisional; do not silently replace source values. Once calibration is supported by source evidence or identified owner confirmation and reviewed, recalculate the affected boundary areas while retaining the original observations and review history. No new default lighting zones or code classifications follow from a scale decision.

Reference basis: Armstrong's [ceiling layout calculator](https://www.armstrong.com/drop-ceiling-calculator/en-us) uses nominal 24-inch by 24-inch and 24-inch by 48-inch layouts; its [SAHARA product information](https://www.armstrongceilings.com/residential/en-us/project-ideas-and-installation/sahara.html) describes scored panels that can create smaller visual subdivisions. The U.S. Access Board's [door guidance](https://www.access-board.gov/ada/guides/chapter-4-entrances-doors-and-gates/) distinguishes clear opening measurements from door-leaf dimensions. These references support the checks, not a project's actual module size, door width or scale. The procedure is owner-directed KIS intake guidance, not a statistical or code-derived calibration rule.

## Editable PDF Review and Return

### Annotation Type, Naming and Identity

Use live PDF `/Polygon` annotations with `/Vertices` for every final room footprint, including rectangles. The owner beta directive supersedes `/Square` as a final room-footprint representation. Open `/PolyLine` annotations may mark uncertain edges or support notes but are not the primary closed room-area object. After boundary acceptance, redraw any footprint that is not already an editable fillable closed shape as a closed polygon, preserving accepted geometry and Space identity and reconciling replacement annotation IDs. Keep one primary area object; do not leave duplicate superseded footprints. Apply the [finalized room-map colors and fills](milestone-review-packages.md#finalized-room-map-for-the-first-package): blue enclosed rooms, green circulation, ruddy orange open activity/common areas, violet multi-level open-to-above areas, gray service voids/confirmed out-of-scope or no-lighting areas, and low-opacity wine/burgundy exterior areas, with lighter low-opacity fills than outlines. Do not flatten the review annotations or lock out boundary editing. Generate one clearly distinguishable primary footprint per contiguous area; additional context/labels do not become extra area-count objects.

Use this default naming convention without asking for a choice on every project:

| PDF field | Project convention |
|---|---|
| `/Subj` (Subject) | Exact source room name/number, or clearly prefixed proposed logical-area name |
| `/Contents` (Comments) | Room name; stable Space ID; boundary kind (wall-following or logical proposal); source sheet/view/revision; observed basis; review status/uncertainties; scale/area basis where applicable |
| `/T` | Actual author/organization responsible for creating the markup; do not claim owner review/approval here |
| `/NM` | Persistent unique annotation ID, maintained separately from the display room name and mapped to the Space ID |

For logical proposals, record a short observed-basis checklist in Comments, for example `walls: 2 sides / doors: 2 served / finish transition: yes / ceiling transition: unknown`, followed by the source locators. Unknown observations stay unknown. Verify the saved raw `/NM`, `/T`, `/Subj` and `/Contents` values, not merely similarly named properties in an annotation library. `/Name` is not a substitute for `/NM`. The annotation register records the actual saved ID-to-Space mapping. Include visible labels for untagged proposals and IDs where repeated room names prevent quick identification, plus a legend explaining boundary colors.

These are standard annotation fields, not a dedicated PDF room-name property. Subject/comments do not by themselves draw a label on the page. Add a legible room label with an editable text annotation where the background label is absent, obscured or insufficient for identification; tie its unique annotation ID to the same Space and do not count the text box as area geometry. Keep labels and low-opacity fills clear of source text, dimensions and symbols. Include a small legend distinguishing physical boundary evidence, approximate logical proposals and uncertainty.

Preserve annotation-to-Space mapping in the project markup register, with source/view, geometry and revision evidence. Keep the Space ID redundantly in comments, so a viewer changing `/NM` or the display name does not silently reassign the room. On return, match retained annotation IDs and cross-check Space IDs; if IDs were changed, copied or lost, reconcile the mapping explicitly rather than guessing from the Subject alone. Different annotations for one multi-level Space need distinct annotation IDs. Renaming a room does not renumber its stable Space ID.

Source: Adobe *PDF Reference*, version 1.6, section 8.4, common annotation entries and markup annotation entries ([reference](https://opensource.adobe.com/dc-acrobat-sdk-docs/pdfstandards/pdfreference1.6.pdf)); Adobe [Acrobat Annotation API](https://opensource.adobe.com/dc-acrobat-sdk-docs/library/jsapiref/JS_API_AcroJS.html?highlight=response). Retrieved reference excerpts establish the field meanings and annotation types; owner-reported Bluebeam Polygon identity/vertex readback now supplies workflow-specific proof; other viewer/annotation behavior needs separate verification. These are output conventions, not new v0.3 schema attributes.

Deliver actual editable PDF Polygon annotations (including rectangular footprints), with a legible outline and light transparent fill, rather than a flattened image or page-content lines. Preserve the unflattened working PDF. Each boundary carries a stable Space ID as well as its source room label, so the owner can adjust corners/edges in a compatible editor and return the saved PDF without losing room association.

On return, read the revised annotation geometry and reconcile it through the annotation-to-Space mapping above, including the Space ID recorded in comments. A moved label alone does not change the boundary geometry. Preserve the prior markup revision and owner-edit provenance; flag missing, duplicated, or unidentifiable boundaries for reconciliation. Use the revised geometry and verified view scale to recalculate polygon check areas and update the Room Schedule after review; actual area takeoffs remain owner CAD work. Preserve explicit source-area labels separately and flag disagreement rather than replacing them silently. Retain accepted owner corrections when regenerating the next markup.

The readback test must include a saved boundary edit by the owner, not just saving and reopening an unchanged generated file. Compare geometry with the actual boundary path: a rectangle annotation's outer `/Rect` may include padding described by `/RD`. Do not measure a bounding box containing border padding as though it were the room footprint. Retain the calculation convention in the markup register; ordinary polygons/rectangles are not native Area measurements.

Treat native Bluebeam Area measurements as a compatibility test, not established generator support. Before requiring them for production output, generate one representative room and have the owner test in Bluebeam that it is recognized as an Area measurement, its boundary is editable, its scale/units are correct, its area updates when edited, and its saved geometry/Space ID can be read back. Record the tested version and result. Until that round trip passes, editable standard polygons plus agent recalculation are the supported workflow target; do not promise automatic area updates inside Bluebeam for an ordinary polygon.

## Served Space, Level, and Mounting Height

Assign each physical light to exactly one primary Space according to the floor or working area it primarily illuminates. That Space's level is the level of useful lighting and occupancy, not the fixture's source sheet or ceiling elevation. Incidental spill into another area does not duplicate the light. If a fixture genuinely serves several levels or spaces, document the primary assignment and shared service in a description and request review rather than guessing ownership.

For example, high-mounted lights above a two-story reception remain assigned to the Level 1 reception when they illuminate its floor. Keep the upper-level electrical sheet as the fixture source. Mounting height belongs to the individual Light Object, measured above the served floor. A qualitative high-mounting observation may be recorded with a verification note while numeric height stays null. A numerical estimate needs an explicit estimated basis and note; never insert an arbitrary large value as though measured. Use architectural RCPs/sections or verified dimensions to resolve height.

A ceiling AFF tag is an observation about its ceiling region, not automatically a fixture mounting height. Establish the tagged region and the fixture's mounting relationship before assigning a numeric height; room membership or a single tag within a Space is insufficient. Do not extend one tag across ceiling transitions, outside its drawn region, or to pendants/cove/undercabinet lights without evidence. Otherwise retain the candidate ceiling height in a source note and leave fixture height null pending review.

## Boundaries and Review

Inspect walls, partitions, counters, open edges, alcoves, and soffits before assigning lights and controls. Use wall legends and referenced details to distinguish full-height from partial-height construction where it affects zoning. Plan hatch or line weight alone may not establish height. Do not assign a fixture solely to its nearest text tag.

Keep consequential boundaries in concise room/zone descriptions, such as “zone boundary ends at the west half-wall,” with a source locator. A wall-by-wall object catalog or new spreadsheet wall columns are not required. Unclear boundary extent, height, or control consequences require a discrepancy/open item and discussion before the affected zone is finalized. A half-wall does not itself prove that controls must be shared or separate.

## Stairs and Shared Lighting Zones

A physical stair may be recorded as one Space spanning levels, with its extent in the description, or as architectural level-specific Space records. Preserve architectural names/numbers in either view. Preserve the MEP-specified stair control scheme. KIS's one-zone-per-physical-stair convention is used only when documented behavior and reviewed independent-control constraints support shared operation. Level-specific Space records may reference that same zone; one Light Object is counted once in its primary served Space. Do not manufacture separate control zones merely to match floor rows or merge source-independent zones merely to follow the convention.

A named lighting zone may serve multiple Spaces when their operation is compatible and reviewed. Capture the common zone identity, control area/basis, source controls, and decision. Preserve any demonstrated independent operation, emergency behavior, daylight requirement, or other conflicting constraint as a discrepancy for review before departing from the stair default or finalizing shared control. A shared zone does not predetermine its channels or controller outputs.

## Electrical Overlay and Reconciliation

After the architectural inventory, extract fixture types, physical occurrences, control symbols and text, home runs, and relevant notes. Use power-plan equipment/keynotes to inform apparent room use without silently selecting a code classification. Distinguish lighting controls from plug-load controls and resolve legend conflicts in context. Register actual drawing notes once and reference them from affected Spaces; reviewer comments are separate from source notes.

Maintain separate locators for room-label/boundary evidence and fixture/control evidence. Check upper-level lighting against the floor below and inspect symbol-only items. Reconcile room/type summaries to individual assignments and the source plans. Then review the lighting zones associated with each Space. Extract the specified MEP control scheme first and check it through WikiJS against reviewed room conditions and the project code basis. Preserve unclear, absent and conflicting intent as findings, not invented control actions. Resolve consequential interpretation/implementation questions before finalizing affected channel/controller assignments; redesign needs authority and approval. See the [full workflow and readiness map](lv-project-workflow-and-readiness.md).

## Discrepancy List and Handoff

Use existing `open_items[]` and the review workbook's discrepancy list rather than a second database. Each item identifies conflicting or missing observations, affected IDs, source locators, consequence/action, review status, and resolution/decision. Preserve resolved discrepancies as history. Block finalization of the affected scope while a consequential issue remains open; do not stop unrelated verified work.

Human review resolves ambiguous use, boundaries, shared service, and design consequences. A second extraction pass can independently check labels, complete area coverage, assignments, cross-level alignment, references, and counts. Accepted owner corrections are evidence for reconciliation and must survive refreshes. Source reconciliation is an engineering workflow; the current generators validate entered data and do not extract drawings.

Owner: KIS Solutions. October 2026; owner-directed draft clarification to v0.3.

## Room Review Print Package

For each boundary review deliverable, front-load a Room Boundaries schedule with Room ID, available source room tag/name, level, area/basis and basic notes, spanning as many legible pages as necessary. Plan labels retain every nonblank known name/tag without inventing missing names. Later light-point review overlays all fixtures on lightly hatched room areas. Follow [milestone packages](milestone-review-packages.md).

## M1/M2 Beta Review Update

Follow [room geometry and physical intake review](m1-m2-beta-review.md). Room footprints use owner-reviewed edge notches with no slits; rare retained nested Spaces use frontmost dashed/deeper fills and `nested_in`. This room rule is distinct from the unchanged no-detour styling for control-zone/channel boxes. Package 1 uses **Area sf (check only)** and **Nested in**; both Package 1/2 carry the mandatory area/notch/nesting note. Owner-returned geometry establishes the working frame; presentation does not change smallest-containing served-Space membership. Deliver live Polygon/FreeText annotations and an identity register, with a zero-annotation build rejection. Apply owner section-count overrides, exact source tags, provisional schedule mappings, keynote-only types and explicit exterior holdouts under that playbook. Polygon readback is owner-reported proven for the tested Bluebeam workflow; retain scoped verification for other behaviors.
