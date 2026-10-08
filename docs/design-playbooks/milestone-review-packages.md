---
title: "Milestone Review PDF Packages"
page_type: playbook
page_status: draft
confidence_level: medium
domain_primary: low-voltage-lighting
ai_role: prescriptive_standard
invocation_triggers:
  systems_present: [low_voltage_lighting]
decision_axes: [milestone_review, zone_hierarchy, markup_identity, owner_review]
related_pages:
  - "https://github.com/kissolutions/lv-lighting-design/blob/main/docs/design-playbooks/milestone-review-packages.md"
---

# Milestone Review PDF Packages

## Purpose and Authority

Six printable review packages accumulate into the final package. These deliverable numbers are not replacements for the existing M1/M2/M3/M4 workflow IDs. Each contains schedule pages first, followed by applicable source-plan markup sheets. Every package records project/model revision, source revisions, deliverable/review revision and review status. Accepted owner-returned geometry supersedes provisional placement; retain the earlier review record. Never silently replace an accepted section with an unreviewed revision.

## Package Contents

| Package | Schedule/list pages first | Plan markup |
|---|---|---|
| 1. Room Boundaries | Heading **Room Boundaries**; Room ID, known source room tag/name, level, area and basis, basic notes/open items; paginate as needed | Accepted room footprints as editable fillable closed shapes, colorized by the room-map legend below; stable Room IDs and every available nonblank tag/name; do not invent missing names |
| 2. Lighting Takeoff | Fixture schedule first; all Light Point IDs grouped by fixture type and reconciled counts, continuing across pages | All light points over lightly **hatched room areas**, not borders alone; preserve visibility of source plan, undercounter lights, strips and small fixtures |
| 3. Lighting Zones and Room Devices | Lighting-zone list first, including parent/child IDs; then narrative-required device schedule | Functional zones and device-specific provisional locations under the placement rules below; owner finalizes devices and returns markup |
| 4. Micro LV Channels | Micro-channel schedule with stable ID, functional zone/subzone, assigned output, calculated connected wattage | Boxes around micro channels; `<controller tag>:CH<output>` upper left, wattage lower right. Exclude device symbols. Enveloped boxes use dashed boundaries |
| 5. Controller and Power Equipment | Device/equipment schedule and relevant assignment/feed references | QDCD, PDU, CIO, SW4/SW8 and other selected equipment at reasonable proposed positions; owner finalizes and returns |
| 6. Coordinated System | Consolidated schedules and applicable connections/routing records | Accepted room, light, zone, channel, device and cable information on separate final layers |

Use as many schedule sheets and plan pages as needed for legibility. Repeat schedule column headings; keep identifiers and associations readable rather than shrinking everything onto one page. Include plan/page reference and scale/basis information when available. Calculated labels round upward to whole numbers; source/nameplate values and engineering data retain their original precision.

## Finalized Room Map for the First Package

After the owner finalizes the room boundaries, make every accepted room footprint a fillable closed area. Retain an existing editable `/Polygon` when it already represents the accepted boundary. Convert other representations, including `/Square`, to a live `/Polygon` preserving accepted geometry; open polylines and separate edge segments alone are insufficient. Preserve the accepted geometry, Space ID, label, source/level and review history. Replace the superseded primary footprint rather than leaving duplicate room-area objects. Preserve the annotation ID when supported; otherwise explicitly reconcile the old/new annotation IDs to the same Space in the markup register.

Use a colored outline and a slightly different, lighter shade of that color for the low-opacity fill so the plan reads as a colorized room map. Keep source linework and labels legible. Include the following legend on the room-map sheets; exact RGB values/opacity are presentation choices, not newly fixed owner requirements.

| Room-map category | Color family | Interpretation |
|---|---|---|
| Enclosed rooms | Blue | Ordinary discrete enclosed rooms |
| Corridors / halls / circulation tracking spaces | Green | Includes accepted logical corridor tracking Spaces; “space tracking” describes inventory practice, not an energy-code room type |
| Open activity / common areas | Ruddy orange | Open offices, gyms, play areas, dining areas and assembly areas; these owner-named activity areas may be bounded by exterior walls and still belong in this presentation category |
| Multi-level atriums / open-to-above areas | Violet | Includes an accepted reception area open to the level above; describe the served occupied level and vertical relationship |
| Service voids / confirmed out-of-scope or no-lighting areas | Gray | Preserve the actual scope and lighting status in notes |
| Exterior areas | Wine / burgundy | Low-opacity fill |

These are presentation categories, separate from building/energy-code classifications and device colors. When categories overlap, the confirmed open-to-above category takes precedence, then circulation, then the owner-named open activity/common-area category, then ordinary enclosed rooms. A tall room is not automatically an atrium. Unknown/unresolved map categories receive a neutral unclassified fill and review note rather than an invented classification. Confirmed excluded areas retain a scope note and use gray context fill. Service voids/chases use gray, preserving their actual lighting status. Exterior areas use low-opacity wine/burgundy unless confirmed gray status takes precedence.

An upper-level opening/void does not create duplicate occupied floor area, room loads or Light Objects. Preserve the accepted multi-level Space relationship and label the open-to-below context separately where shown; reception lights continue to belong to their primary served occupied level. The room-map fill is visual presentation and does not change accepted measured areas or generate controls zones.

Carry the same category colors into the second package's light-point review, using light hatching/low-opacity fills so small fixtures remain visible. Finish with the existing text-in-front pass. Verify editable fills and identity in the actual saved PDF; documentation alone does not implement a PDF renderer.

Gray also identifies service voids and confirmed out-of-scope/no-lighting areas. Exterior areas use low-opacity wine/burgundy fill. Show excluded regions as gray context with retained scope notes, without adding included takeoff records merely to color the map. Keep service-void identity, scope exclusion and confirmed no-lighting status separate; color alone establishes none of those source facts. For overlapping categories, confirmed gray status takes precedence, followed by exterior wine/burgundy, then the categories above. Retain low-opacity fills and source visibility.

## M3 Narrative Review Data

Organize the M3 review into **one section per sequence**: sequence number/stable ID and revision, full narrative, required functions/components, then a table of every assigned room/zone. Preserve the one-to-many narrative relationship. Follow the [shared sequence-section layout](https://github.com/kissolutions/knowledgebase_wikijs/blob/main/design-playbooks/room-classification-and-controls-review-playbook.md#m3-review-layout--one-section-per-sequence).

Sequence requirements cover manual/automatic operation, switching, occupancy/vacancy, dimming, **Light Reduction**, daylight, scheduling and other applicable functions. Room rows show what is actually documented or proposed: wall-switch/dimmer quantities, sensor quantities and operating modes, controlled groups and settings, shared control references, and implementation gaps. Do not simply repeat “required” or the generic sequence in every row. Keep source/proposed/adopted status explicit; these are not installed-equipment assertions.

Use consistent columns and identical wording for matching entries so differences can be scanned vertically. Flag differing cells and unresolved entries with text as well as optional shading. Distinguish legitimate device-count variations from behavior conflicting with the sequence. Known absence is None; missing information is Unknown/TBD. Preserve stable Room/zone/device identities and references, and avoid duplicate counts for shared devices.

Retain **Light Reduction** as a dedicated header: sequence summaries state partial on/off, 50% on/off, none or another supported behavior; room rows state the actual implementation, percentage basis and known equipment/group quantities. See the [shared Light Reduction definition](https://github.com/kissolutions/knowledgebase_wikijs/blob/main/design-playbooks/room-classification-and-controls-review-playbook.md#m3-control-narrative-data--light-reduction). Unknown device counts remain pending; do not bypass narrative lock or coverage review to populate this table. Physical scheduling and placement continue after narrative lock.

Repeat sequence IDs and column headers across continuation pages. Project-authored narrative tables implement this review format; the current generic zone CSV/HTML exporter and narrative-text model do not yet structure or render these per-function sequence sections. Do not add unsupported JSON properties.

## Narrative and Device Placement Sequence

After the control narrative is locked, build the physical room-device schedule and place representations using the provisional rules below. Owner review establishes final positions. Apply the rules to the actual served room/zone and retain each device's stable identity and parent/child associations. Multiple devices may receive label offsets/leaders for readability without moving the intended physical position.

### Wall-Control and Sensor Location Priority

For wall switches, scene controllers, dimmers, occupancy sensors and daylight sensors, start with the locations already established on the electrical lighting plans or other applicable source design drawings. Capture source control symbols/locations during source intake and carry them into post-narrative device selection/placement. Match each location to its source tag, room and intended control function; selecting an LV device does not itself relocate the shown control.

Preserve an already accepted owner location first. Otherwise use the applicable electrical-plan location as the initial proposal, recording sheet/page/revision and symbol/anchor evidence with location basis `source`. Register source positions into the accepted working page frame before placing symbols; retain the original source locator. If sources conflict or a symbol's association/location is unclear, flag that uncertainty for review rather than silently treating the location as absent or overriding it with a generic placement rule. Preserve the source designer's established sensor layout as the starting point; investigate any supported coverage or narrative conflict explicitly instead of automatically recentering sensors.

Only when no usable source location is available for the required device, apply the corresponding fallback below: door-latch/glazing/open-entry rules for wall controls; room/child-zone/tile centers, wall-corner or corridor-midpoint proposals for occupancy sensors; and the existing flagged daylight-sensor placeholder. Record the source search and fallback basis; fallback positions remain provisional for owner finalization. Location evidence does not independently establish control quantities/functions or approve a departure from the narrative.

### Provisional Room-Device Placement

| Device/context | Initial location for owner review |
|---|---|
| Wall switch, dimmer, scene controller, occupancy sensor or daylight sensor with a source design location | Use that location first, subject to accepted owner changes and source/working-frame reconciliation. |
| Wall switch, dimmer or scene controller in an enclosed room with a door, without a usable source location | On the room side of the wall, on the door knob/latch side, a few inches beyond the door frame. Use a solid wall segment clear of the frame and door swing. |
| No usable source location, and the latch-side wall is glazing/window | Use the adjacent solid wall, a few inches beyond where the open door/swing reaches that wall. Keep the proposed control clear of the swing. |
| Manual control for a parent zone or larger common open area without a usable source location, particularly open offices and lobbies | On a suitable wall near the entryway/corridor opening along the reasonable pedestrian approach. Associate the shared control with the parent and all served zones; do not duplicate a switch for each child zone unless the narrative calls for it. |
| Ceiling occupancy sensor in a simple enclosed room, without a usable source location | Near the room center, centered within a ceiling tile when a visible tile grid permits it. |
| Ceiling occupancy sensor in a complex zone or open-office cluster, without a usable source location | Near the middle of its served zone/child zone, on a tile center when visible. Apply narrative-required quantities and positions to the occupancy-controlled child zones rather than adding a sensor solely for the parent container. |
| Wall occupancy sensor, without a usable source location | Use the top-left corner of the room as shown on the displayed plan, on a solid wall near that corner, as the current review placeholder. Note an intended view into the occupied area; owner review resolves orientation, obstructions and final position. |
| Hallway/corridor occupancy sensor, without a usable source location | Near the middle of the served hallway/corridor zone. For multiple narrative-required sensors, propose positions within their served portions and flag review rather than stacking symbols at one midpoint. |
| Daylight sensor without a usable source location, or another room device without a defined placement rule | Retain a room/served-zone-center review placeholder and flag device-specific placement for owner review. |

These are owner-directed initial markup locations. “A few inches” is qualitative guidance, not an invented exact offset, mounting height or installation detail. Do not infer final sensor coverage or add/remove devices from symbol placement alone; quantities and functions come from the locked narrative. If the applicable fallback geometry (door, latch side, swing, solid wall or entry route) or sensor tile grid cannot be determined from the available source, record the missing basis and use a clearly provisional room/zone-center fallback instead of inventing geometry. Tile alignment is conditional on a visible grid. Preserve any already accepted owner location.

Record the rule/context and source basis, uncertainties and provisional status in annotation comments or the linked review record. Separate intended device location from text/leader offsets. Sensor quantities and coverage, mounting heights and manufacturer-specific installation details remain subject to the applicable design/owner review.

Owner-returned device locations are reconciled before dependent aggregator placement and cable routing. Controllers receive their own later reasonable-location review. Controller/output assignments may precede equipment location acceptance so channel-map tags can be shown; use stable micro-channel IDs while assignments remain unknown. Do not invent assignments just to make labels look complete.

## Device Schedule and Simple Tags

| Device | Tag example | Symbol/color |
|---|---|---|
| Occupancy sensor | OS-01 | Diamond / PURPLE |
| Daylight sensor | DS-01 | Diamond / PURPLE |
| Wall controller/switch | WC-01 | `$` / PURPLE |
| Wall dimming controller | WD-01 | `$D` / PURPLE |

Rows require persistent Device ID, visible tag, descriptive name, associated Room ID/name, all served functional zone/subzone IDs, narrative function and placement review status. Tags are simple KIS identifiers inspired by instrument-tag clarity; no claim of ISA compliance. Keep stable internal IDs independently of display tags. Equipment retains QDCD-01, PDU-01, CIO-01, SW8-01/SW4-01 tags. Record additional device kinds explicitly. Count one physical device once even when it serves multiple child/parent zones.

## Functional Parent and Child Zones

Each occupancy-controlled open-office cluster is a first-class zone. The same zone object optionally references a parent zone; the parent represents shared whole-office operation/manual control and aggregate child occupancy. A child zone is never only a drawn grouping or annotation. Parent lighting membership/load is derived from descendants; do not duplicate physical lights or assign a separate power output to the parent container. Exact aggregate logic and manual/occupancy precedence come from the approved narrative, not a default invented by the renderer. Micro LV channels continue to reference leaf functional zones and remain separate electrical objects.

## Final Layers and Presentation Pass

Final layer names: **rooms, lights, zones, lv_channels, controllers, cabling**. The controllers layer includes both room devices and controller/power equipment. The micro-channel review excludes devices even though the coordinated package includes them. Layers must be independently controllable in the actual PDF, subject to compatibility verification; named drawing groups alone do not prove PDF layers.

After all geometry/markup operations for each deliverable, promote every text label in front of lines/shapes, including existing source-identifying labels added by this workflow. Preserve the effective front-to-back order during save/readback. Keep calculated wattage/footage and other calculated labels at zero decimals using mathematical ceiling (42.1 W → 43 W; 18.01 ft → 19 ft). Never round before summing or checking electrical capacity.

When another zone visually envelops a zone/channel, draw the more enveloped boundary dashed while preserving color, label, width and other styling. Do not spend time weaving polylines around surrounding geometry. Hatch opacity/density must preserve fixture/source visibility; no geometric clipping optimization is required merely to avoid visual overlap.

## Annotation Identity and Owner Return

Use the [markup manifest contract](../ontology/canonical-model/milestone-markup-v1.md). Device symbols carry immutable annotation identity and linked Device ID; moving a symbol preserves its schedule and zone associations. Retain geometry/location in displayed-page coordinates, revision and review state. Verify the actual human edit/save/readback path before marking a package accepted. Preserve editable unflattened markups until review is complete.

## Implemented Scope and Remaining Proof

The v0.7 zone hierarchy, topology v1.1 device identity, markup manifest checks, upward-rounding/render-order helpers and CSV/printable HTML schedule exporter are implemented. Schedule HTML can be printed to PDF and used as front sheets. Automatic PDF plan overlay, label promotion in an existing PDF, PDF layer authoring and sensor coverage remain outside this exporter. Owner-reported Bluebeam Polygon edit/save/readback is proven for the tested beta workflow; see the scoped evidence and live-annotation gate in the M1/M2 beta review playbook. An agent can produce scoped markups through a suitable external PDF workflow, following these directives and recording verification.

## M2 Fixture-Schedule Evidence Prerequisite

The Lighting Takeoff package's first-sheet fixture schedule is the extracted **original MEP source schedule**, with source locators and exact type marks; selected LV substitutions remain separately identified. Extract/review it before accepting light counts and apparent run/assembly continuity. Reconcile schedule descriptions with RCP geometry and electrical circuiting/daisy-chain evidence, especially curved/circular mixed-tag assemblies such as L4/L4A. Follow the [M2 source schedule gate](m2-linear-fixture-extraction.md#m2-source-fixture-schedule-gate). If the source schedule is absent, record that absence and do not substitute invented source data; unresolved affected quantities remain provisional.

## M1/M2 Beta Review Update

Follow [room geometry and physical intake review](m1-m2-beta-review.md). Room footprints use owner-reviewed edge notches with no slits; rare retained nested Spaces use frontmost dashed/deeper fills and `nested_in`. This room rule is distinct from the unchanged no-detour styling for control-zone/channel boxes. Package 1 uses **Area sf (check only)** and **Nested in**; both Package 1/2 carry the mandatory area/notch/nesting note. Owner-returned geometry establishes the working frame; presentation does not change smallest-containing served-Space membership. Deliver live Polygon/FreeText annotations and an identity register, with a zero-annotation build rejection. Apply owner section-count overrides, exact source tags, provisional schedule mappings, keynote-only types and explicit exterior holdouts under that playbook. Polygon readback is owner-reported proven for the tested Bluebeam workflow; retain scoped verification for other behaviors.
