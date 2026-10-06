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

After the owner finalizes the room boundaries, make every accepted room footprint a fillable closed area. Retain an existing editable `/Polygon` or fillable `/Square` when it already represents the accepted boundary. Otherwise redraw the accepted footprint as a closed polygon; open polylines and separate edge segments alone are insufficient. Preserve the accepted geometry, Space ID, label, source/level and review history. Replace the superseded primary footprint rather than leaving duplicate room-area objects. Preserve the annotation ID when supported; otherwise explicitly reconcile the old/new annotation IDs to the same Space in the markup register.

Use a colored outline and a slightly different, lighter shade of that color for the low-opacity fill so the plan reads as a colorized room map. Keep source linework and labels legible. Include the following legend on the room-map sheets; exact RGB values/opacity are presentation choices, not newly fixed owner requirements.

| Room-map category | Color family | Interpretation |
|---|---|---|
| Enclosed rooms | Blue | Ordinary discrete enclosed rooms |
| Corridors / halls / circulation tracking spaces | Green | Includes accepted logical corridor tracking Spaces; “space tracking” describes inventory practice, not an energy-code room type |
| Open activity / common areas | Ruddy orange | Open offices, gyms, play areas, dining areas and assembly areas; these owner-named activity areas may be bounded by exterior walls and still belong in this presentation category |
| Multi-level atriums / open-to-above areas | Violet | Includes an accepted reception area open to the level above; describe the served occupied level and vertical relationship |

These are presentation categories, separate from building/energy-code classifications and device colors. When categories overlap, the confirmed open-to-above category takes precedence, then circulation, then the owner-named open activity/common-area category, then ordinary enclosed rooms. A tall room is not automatically an atrium. Unknown/unresolved map categories receive a neutral unclassified fill and review note rather than an invented classification. Confirmed excluded areas retain a scope note and are not colored as included rooms. Outdoor areas, chases and service voids do not receive a new category by assumption; record their known nature and request category review if included.

An upper-level opening/void does not create duplicate occupied floor area, room loads or Light Objects. Preserve the accepted multi-level Space relationship and label the open-to-below context separately where shown; reception lights continue to belong to their primary served occupied level. The room-map fill is visual presentation and does not change accepted measured areas or generate controls zones.

Carry the same category colors into the second package's light-point review, using light hatching/low-opacity fills so small fixtures remain visible. Finish with the existing text-in-front pass. Verify editable fills and identity in the actual saved PDF; documentation alone does not implement a PDF renderer.

## Narrative and Device Placement Sequence

After the control narrative is locked, build the physical room-device schedule and place representations using the provisional rules below. Owner review establishes final positions. Apply the rules to the actual served room/zone and retain each device's stable identity and parent/child associations. Multiple devices may receive label offsets/leaders for readability without moving the intended physical position.

### Provisional Room-Device Placement

| Device/context | Initial location for owner review |
|---|---|
| Wall switch, dimmer or scene controller in an enclosed room with a door | On the room side of the wall, on the door knob/latch side, a few inches beyond the door frame. Use a solid wall segment clear of the frame and door swing. |
| The latch-side wall is glazing/window | Use the adjacent solid wall, a few inches beyond where the open door/swing reaches that wall. Keep the proposed control clear of the swing. |
| Manual control for a parent zone or a larger common open area, particularly open offices and lobbies | On a suitable wall near the entryway/corridor opening along the reasonable pedestrian approach. Associate the shared control with the parent and all served zones; do not duplicate a switch for each child zone unless the narrative calls for it. |
| Ceiling occupancy sensor in a simple enclosed room | Near the room center, centered within a ceiling tile when a visible tile grid permits it. |
| Ceiling occupancy sensor in a complex zone or open-office cluster | Near the middle of its served zone/child zone, on a tile center when visible. Apply narrative-required quantities and positions to the occupancy-controlled child zones rather than adding a sensor solely for the parent container. |
| Wall occupancy sensor | Use the top-left corner of the room as shown on the displayed plan, on a solid wall near that corner, as the current review placeholder. Note an intended view into the occupied area; owner review resolves orientation, obstructions and final position. |
| Hallway/corridor occupancy sensor | Near the middle of the served hallway/corridor zone. For multiple narrative-required sensors, propose positions within their served portions and flag review rather than stacking symbols at one midpoint. |
| Daylight sensor or another room device without a defined placement rule | Retain a room/served-zone-center review placeholder and flag device-specific placement for owner review. |

These are owner-directed initial markup locations. “A few inches” is qualitative guidance, not an invented exact offset, mounting height or installation detail. Do not infer final sensor coverage or add/remove devices from symbol placement alone; quantities and functions come from the locked narrative. If the door, latch side, swing, solid wall, entry route or tile grid cannot be determined from the available source, record the missing basis and use a clearly provisional room/zone-center fallback instead of inventing geometry. Tile alignment is conditional on a visible grid. Preserve any already accepted owner location.

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

The v0.7 zone hierarchy, topology v1.1 device identity, markup manifest checks, upward-rounding/render-order helpers and CSV/printable HTML schedule exporter are implemented. Schedule HTML can be printed to PDF and used as front sheets. Automatic PDF plan overlay, label promotion in an existing PDF, PDF layer authoring, sensor coverage and human-edit readback are not implemented/proven by this update. An agent can produce scoped markups through a suitable external PDF workflow, following these directives and recording verification.
