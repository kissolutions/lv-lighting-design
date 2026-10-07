---
title: "Control-System Markup Legend"
page_type: playbook
page_status: draft
confidence_level: medium
domain_primary: low-voltage-lighting
ai_role: prescriptive_standard
invocation_triggers:
  systems_present: [low_voltage_lighting, smartdc]
decision_axes: [power_allocation, controls, equipment_placement, owner_review]
related_pages:
  - "https://github.com/kissolutions/knowledgebase_wikijs/blob/main/design-playbooks/smartdc-allocation-index.md"
---

# Control-System Markup Legend

## Legend

| Component | Symbol | Color | Example |
|---|---|---|---|
| PDU (current power component) | Rectangle | RED | PDU-01 |
| CIO | Rectangle | BLUE | CIO-01 |
| QDCD / driver controller | Square | BLUE | QDCD-01 |
| Sensor aggregator | Diamond | BLUE | SW8-01 / SW4-01 |
| Sensor | Diamond | PURPLE | OCC-01 / DL-01 |
| Wall controller | `$` | PURPLE | WC-01 |
| Wall dimming controller | `$D` | PURPLE | WC-02 |

Device ID labels are mandatory, particularly shared rectangle/diamond shapes. `$D` is the accepted initial glyph; no special dollar-stroked D is required. Symbols show proposed physical locations. QDCD labels/callouts reference existing micro channels and outputs; sensor/wall labels reference served functional zones. Maintain visible proposal/owner-review status and annotation IDs mapped to device IDs.

## Room-Map Colors

For the first milestone's accepted fillable room footprints, use BLUE for ordinary enclosed rooms, GREEN for corridors/halls/circulation tracking Spaces, RUDDY ORANGE for open activity/common areas (open offices, gyms, play, dining and assembly), VIOLET for multi-level atriums/open-to-above areas, GRAY for service voids and confirmed out-of-scope/no-lighting areas, and WINE/BURGUNDY for exterior areas with low-opacity fill. Fills use a slightly different lighter shade from outlines and low opacity. Follow [room-map categories and precedence](milestone-review-packages.md#finalized-room-map-for-the-first-package); retain neutral unclassified presentation for unresolved categories. Room colors are independent of component colors: violet room fill does not identify a sensor, and blue room fill does not identify equipment. Include a room-map legend and retain source visibility and frontmost labels.

## Connectivity and Readback

Draw and label PDnet, SDCnet, PDU power feeds and luminaire routes separately; route colors/line styles are not prescribed by the owner yet. Label route IDs, endpoints and bus/power role without inferring route color from device color. Show CIO associations, strings and PDU output/QDCD input mapping. Highlight unresolved locations, conflicts and specific owner questions. Retain editable unflattened annotations, saved coordinates and IDs; prove human edit/save/readback before promising a production markup workflow.

## Milestone Presentation and Device Tags

Follow [milestone review packages](milestone-review-packages.md). Display tags OS-01, DS-01, WC-01 and WD-01 distinguish room devices; persistent internal/annotation IDs remain separate. Sensors/wall controls stay PURPLE; QDCD/CIO/SW controls BLUE; PDU RED. Tag changes do not change the `$`/`$D` glyphs.

Final layers are rooms, lights, zones, lv_channels, controllers and cabling. Both device categories live on controllers. Takeoff rooms use light hatches; micro-channel maps use boxes without devices, output tag upper left and ceiling-rounded watts lower right. Finish each markup by bringing text in front of lines/shapes. Enveloped zones/channels use dashed boundaries with other styling preserved; no polyline detours. Calculated display quantities use ceiling to whole numbers while calculations stay precise.

## Fixture Power Aggregator Identification

EPS fixture power aggregators are power devices, distinct from BLUE SW4/SW8 sensor aggregators. Use the established RED power-component color and a clearly labeled internal-unit box/callout with a stable ID such as FA-01, served fixture ID, populated input count and an inside-fixture-housing note. Do not infer a sensor port, bus address or separate room-device location. Show all allocated Class 2 feed IDs and the one fixture output in equipment/connection review; keep the micro-channel review device-free. Follow [fixture power aggregation](controller-power-placement.md#eps-fixture-power-aggregation--owner-directive-2026-10-06).

## M1/M2 Beta Review Update

Follow [room geometry and physical intake review](m1-m2-beta-review.md). Room footprints use owner-reviewed edge notches with no slits; rare retained nested Spaces use frontmost dashed/deeper fills and `nested_in`. This room rule is distinct from the unchanged no-detour styling for control-zone/channel boxes. Package 1 uses **Area sf (check only)** and **Nested in**; both Package 1/2 carry the mandatory area/notch/nesting note. Owner-returned geometry establishes the working frame; presentation does not change smallest-containing served-Space membership. Deliver live Polygon/FreeText annotations and an identity register, with a zero-annotation build rejection. Apply owner section-count overrides, exact source tags, provisional schedule mappings, keynote-only types and explicit exterior holdouts under that playbook. Polygon readback is owner-reported proven for the tested Bluebeam workflow; retain scoped verification for other behaviors.
