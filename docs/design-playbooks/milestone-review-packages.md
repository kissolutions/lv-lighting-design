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
| 1. Room Boundaries | Heading **Room Boundaries**; Room ID, known source room tag/name, level, area and basis, basic notes/open items; paginate as needed | Room boundaries with stable Room IDs and every available nonblank tag/name; do not invent missing names |
| 2. Lighting Takeoff | Fixture schedule first; all Light Point IDs grouped by fixture type and reconciled counts, continuing across pages | All light points over lightly **hatched room areas**, not borders alone; preserve visibility of source plan, undercounter lights, strips and small fixtures |
| 3. Lighting Zones and Room Devices | Lighting-zone list first, including parent/child IDs; then narrative-required device schedule | Functional zones and room-device symbols initially near room centers, explicitly provisional; owner moves devices and returns markup |
| 4. Micro LV Channels | Micro-channel schedule with stable ID, functional zone/subzone, assigned output, calculated connected wattage | Boxes around micro channels; `<controller tag>:CH<output>` upper left, wattage lower right. Exclude device symbols. Enveloped boxes use dashed boundaries |
| 5. Controller and Power Equipment | Device/equipment schedule and relevant assignment/feed references | QDCD, PDU, CIO, SW4/SW8 and other selected equipment at reasonable proposed positions; owner finalizes and returns |
| 6. Coordinated System | Consolidated schedules and applicable connections/routing records | Accepted room, light, zone, channel, device and cable information on separate final layers |

Use as many schedule sheets and plan pages as needed for legibility. Repeat schedule column headings; keep identifiers and associations readable rather than shrinking everything onto one page. Include plan/page reference and scale/basis information when available. Calculated labels round upward to whole numbers; source/nameplate values and engineering data retain their original precision.

## Narrative and Device Placement Sequence

After the control narrative is locked, build the physical room-device schedule and place representations provisionally at room centers: wall controls, occupancy sensors, daylight sensors and any other narrative-required room devices. This is a relocation review, not a coverage/wall-mounting recommendation. Multiple devices may receive small display offsets/leader labels for readability while metadata keeps the proposed association/location basis explicit.

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
