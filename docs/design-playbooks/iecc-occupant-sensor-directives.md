---
title: "IECC Occupant Sensor Directives by Edition"
page_type: playbook
page_status: draft
confidence_level: medium
domain_primary: low-voltage-lighting
ai_role: prescriptive_standard
invocation_triggers:
  systems_present: [low_voltage_lighting]
decision_axes: [energy_code_basis, space_classification, control_zoning, sensor_coverage]
related_pages:
  - "architectural-space-intake.md"
  - "lighting-design-playbook.md"
  - "../ontology/canonical-model/space-context-v0.3.md"
---

# IECC Occupant Sensor Directives by Edition

## Purpose and Authority

Translate retrieved code provisions into reviewable room/control directives. These are paraphrased source summaries and KIS workflow instructions, not a reproduction of the code or an implemented compliance engine. They are draft supporting material for the general lighting application guide owned in WikiJS; the [local guide draft](lighting-control-application-guide.md) retains its proposed structure pending alignment upstream. In LV projects, apply supported provisions as checks on the extracted MEP control scheme. Proposed alternative quantities/sequences are developed only when redesign is authorized; they do not silently replace source intent. Keep code requirements, derived mathematical bounds, and equipment/layout decisions distinct. The profiles below cover commercial lighting under the IECC provisions; an ASHRAE compliance path needs a separate profile.

Select the project edition, jurisdiction, amendments, applicable printing/errata, and compliance path before applying a rule. A newer edition does not become the project's governing code by being available. Check the adopted scope for new work versus alterations, C405.2 control exceptions, specific-application lighting, and any selected additional-efficiency requirements. Do not carry an exemption or numbering scheme from another edition into the selected profile.

## Source Register and Verification Status

Sources reviewed October 3, 2026. ICC search retrieval supplied some section text, but direct page requests returned access errors. Government training material and original government-commissioned code-change analysis supplement the retrieved ICC text. Development proposals and another jurisdiction's amended code were not treated as final unamended model-code authority.

| ID | Primary source and locator | Supports | Remaining verification |
|---|---|---|---|
| S15 | [DOE 2015 lighting training](https://www.energycodes.gov/sites/default/files/2019-09/2015_IECC_commercial_requirements_lighting.pdf), PDF pages 20–23 | Listed-space examples, general function, warehouse outline | Complete final C405.2.1 list and exceptions; exact catch-all area operator; printing/errata |
| S18 | [DOE 2018 lighting training](https://www.energycodes.gov/sites/default/files/2019-09/2018_IECC_commercial_requirements_lighting.pdf), PDF pages 18–21 | Listed spaces, general function, open-office zoning/actions | Exact catch-all area operator and complete final exception text; printing/errata |
| S18O | [ICC 2018 C405.2.1.3](https://codes.iccsafe.org/s/IECC2018P5/chapter-4-ce-commercial-energy-efficiency/IECC2018P5-CE-Ch04-SecC405.2.1.3) | Open-office threshold and maximum zone area | Full final section/exception comparison with S18 |
| S21 | [ICC 2021 Chapter 4](https://codes.iccsafe.org/content/IECC2021V3.0/chapter-4-ce-commercial-energy-efficiency), C405.2.1, .1.1, .1.3 | Listed spaces, general function, open-office threshold/zone size | Full open-office sequence and exceptions; project adoption/amendments |
| S21E | [ICC 2021 errata](https://www.iccsafe.org/wp-content/uploads/errata_central/2021-International-Energy-Conservation-Code-Errata-Complete.pdf), PDF pages 17–19 | Corrected warehouse, corridor, time-switch text | Confirm application to the project's printing and adopted text |
| S21A | [DOE/PNNL 2021 commercial analysis](https://www.energycodes.gov/sites/default/files/2022-09/2021_IECC_Commercial_Analysis_Final_2022_09_02.pdf), PDF page 33, section 3.4.2 | Corridor requirement added relative to 2018 | Does not replace final code/exception review |
| S24A | [Florida Building Commission comparison report](https://www.floridabuilding.org/fbc/publications/Research_2023_2024/2023-FBCEC-vs-2024-IECC-and-2022-ASHRAE-901_FinalReport.pdf), PDF pages 76–77, C405.2 and C405.2.1 rows | Final-edition change summary, including four added categories | Complete final 2024 space list, control exceptions, printing/errata |
| S24G | [ICC 2024 C405.2.1.1](https://codes.iccsafe.org/s/IECC2024V1.1/chapter-ce-4-commercial-energy-efficiency/IECC2024V1.1-CE-Ch04-SecC405.2.1.1) | Retrieved general-control function | Complete final exception text and project amendment review |
| S24O | [ICC 2024 C405.2.1.3](https://codes.iccsafe.org/s/IECC2024V1.0/chapter-ce-4-commercial-energy-efficiency/IECC2024V1.0-CE-Ch04-SecC405.2.1.3), also [first-printing locator](https://codes.iccsafe.org/s/IECC2024P1/chapter-4-ce-commercial-energy-efficiency/IECC2024P1-CE-Ch04-SecC405.2.1.3) | Retrieved open-office threshold and zone-area ceiling | Complete final sequence/exception text and consistency across printings |

These are draft profiles with explicit verification gaps, not approved automatic-compliance profiles. A supported rule may produce a cited candidate result for review. An unresolved provision cannot produce a final requirement or exemption. Completing one rule's verification does not verify the entire edition.

## Edition Summaries

### 2015

S15 identifies educational instruction spaces, meeting/multipurpose rooms, lounges, employee eating/break rooms, private offices, toilets, storage, janitorial closets, lockers, small fully enclosed spaces, and warehouses. Its general sequence is vacancy shutoff within 30 minutes, manual activation or automatic activation limited to half power, and manual shutoff. It describes full-on permissions for certain public/safety spaces and separate warehouse aisle control. This is a supported subset, not a complete final-code transcription. Copy/print applicability and the exact small-space boundary must be checked against final C405.2.1 before automatic matching; the training slide uses a shortened inequality.

Do not import the later open-office 600-square-foot rule into 2015 without separate authority. Room types not matched by a verified 2015 rule remain for review.

### 2018

S18 identifies instruction rooms; meeting/multipurpose rooms; copying/printing spaces; lounges/break rooms; enclosed and open offices; toilets; storage; lockers; small fully enclosed spaces; and warehouse storage. General controls shut off within 20 minutes and provide manual-on or at most half-power auto-on, plus manual-off, subject to exceptions.

S18/S18O distinguish open offices below 300 square feet from larger cases. The latter need independent zones no larger than 600 square feet, whole-office vacancy shutoff within 20 minutes, and at least 80% zone power reduction within 20 minutes of zone vacancy; complete zone shutoff satisfies that reduction. The training also addresses occupancy-dependent daylight operation. Keep this edition's sequence separate from later editions.

The training shorthand does not settle the catch-all's exact 300-square-foot equality. Leave that edge case pending final text verification. Special-space controls and full-on exceptions need the final section review before finalizing actions.

### 2021

S21 lists instruction rooms, meeting/multipurpose rooms, copying/printing spaces, lounges/break rooms, enclosed offices, open offices, toilets, storage, lockers, corridors, warehouse storage, and other rooms no larger than 300 square feet enclosed by floor-to-ceiling partitions. The 300-square-foot condition qualifies the other-room category; it is not a size exemption for an explicitly listed office.

General controls require shutoff within 20 minutes, manual-on or automatic-on limited to half power, and manual-off, subject to the section's full-on/manual-control exception. Route warehouse, open-office, and corridor cases to their dedicated subsections. Open offices below 300 square feet use the general function; other open offices require independently controlled zones no larger than 600 square feet. Finalize their complete operating sequence only after the remaining section/exception verification in the source register.

S21E corrects warehouse control: separate aisleways, vacancy reduction to at most half power within 20 minutes, time-switch shutoff for lights not shut off by sensors, and manual-off. It corrects corridor control to uniform vacancy reduction to at most half power within 20 minutes. The corridor exception concerns less than two footcandles at the darkest floor point with all lights on; it needs illumination evidence, not a guess from fixture count. The errata also identifies time-switch exceptions; verify them independently rather than transferring them to the sensor requirement.

### 2024

S24A reports four added categories relative to 2021: computer rooms/data centers, healthcare medical-supply rooms, laundry/washing spaces, and healthcare telemedicine rooms. It also reports changed C405.2 exceptions involving exit access and fire-alarm conditions. Therefore, copying the 2021 applicability/exceptions wholesale is not a verified 2024 profile.

Retrieved S24G retains a 20-minute general vacancy shutoff, manual-on or half-power-limited auto-on, and manual-off. S24O retains the below-300-square-foot open-office branch and the 600-square-foot independent-zone ceiling in the other branch. Treat these as supported candidate rules; the complete final space list, sequence, and exceptions still require verification before automatic use.

## Room Matching Directives

1. Confirm the room inventory and source facts under Milestone 1. Preserve `source_room_type`, `energy_code_space_type`, and building-code classifications separately. Architectural room names alone do not prove an ambiguous use.
2. Select the verified project code profile. Match only supported, clearly identified uses. An exact named category can produce a candidate requirement without an area guess; an area-dependent category requires the verified area/enclosure inputs.
3. Check applicability and exception evidence for the affected lighting. An exception permitting full-on is not an exemption from sensors. A time-switch exception is not automatically an occupant-sensor exception. Emergency/egress behavior remains separately reviewed.
4. Record the matched rule ID, year, section, source locator, inputs, requirement/action, and review status. Preserve existing manual classifications/decisions. Present a conflict for review instead of overwriting them.
5. If the use, governing profile, needed area/enclosure, or exception is unknown, return `needs_review` with the missing input. No match means further analysis, not “no sensor required.” Consider other automatic-control requirements under the selected edition.
6. Assign the applicable sequence family before channels/controllers: general room, open office, warehouse aisle/open area, or corridor. Preserve their independent control requirements through LV grouping. Source MEP zones remain observed design intent and constraints, not automatic proof of final compliance.

Room-use aliases and interpretation decisions need owner review. For example, an untagged equipment enclosure must not become storage, a room named Recovery must not become patient-care space, and a large open reception must not become an open office solely to trigger a convenient rule.

## Control Zones Versus Physical Sensor Quantity

For an applicable, verified open-office rule with maximum zone area 600 square feet, KIS derives the area-only lower bound:

`minimum_control_zones = ceil(verified_open_office_area_sq_ft / 600)`

Use this only in the edition's applicable open-office branch. It is a mathematical consequence of the zone-area ceiling, not a quoted hardware-count requirement. At exactly 300 square feet, the retrieved 2018/2021/2024 open-office branch is the other-space branch because the small branch uses a strict less-than comparison. Do not confuse this with the separate catch-all room applicability threshold.

Verify the actual polygon partition: each control zone must satisfy the area ceiling and required independent operation. An adequate number of zones alone does not prove their layout complies. Other manual/daylight/operation constraints can require further subdivisions. The room polygon, occupancy-control zones, and LV power channels are distinct geometry/relationships.

Do not equate installed sensor count with room area or the number of control zones. Use an approved application-guide example to determine a proposed physical sensor quantity when its verified coverage, technology, mounting height, occupied activity, geometry, and input/controller conditions match the room. Verify the applied coverage layout before finalizing the count. Several devices may serve one zone. A device with multiple independently resolved sensing areas may support several zones only with verified capabilities and an appropriate layout. When no approved example matches, retain the quantity as unresolved for design review; an owner-selected preliminary allowance remains an allowance, not a code-derived count.

| Synthetic case | Candidate code result | KIS derived/design result |
|---|---|---|
| Confirmed 2021 enclosed office, 450 square feet | Named category under C405.2.1; area alone does not remove sensor applicability | General-function review; physical sensor quantity unknown pending coverage |
| Confirmed 2021 open office, 1,450 square feet | C405.2.1.3 independent-zone area ceiling applies, subject to applicability/exception review | At least 3 control zones by area; actual polygons and physical sensor quantities need design |
| Untagged 180-square-foot enclosure, enclosure/use evidence missing | Insufficient facts to assign a final energy-code type or catch-all result | Preserve inventory; obtain source/owner confirmation |
| Corridor being evaluated under 2015 versus 2021 | S21A confirms the later explicit corridor addition | Select the year-specific rule; do not transfer the newer mandate to the older profile |

## Review Output and Implementation Boundary

In a code-review schedule, distinguish these outputs: governing profile; matched section/rule; applicability status; sensing required; sequence family; maximum vacancy delay; activation mode; vacancy power action; manual-control requirement; exception evidence; control-zone ceiling/derived lower bound; physical sensor quantity/coverage status; source evidence; and owner decision. These are proposed review outputs, not new fields implemented in the current schema.

Use existing Space area/classification/provision evidence and zone control-area fields where applicable. Record unresolved questions in `open_items[]` and reviewed interpretation in decisions. Do not populate unsupported canonical fields or claim that the existing generator evaluates these profiles. Implementing an automated matcher requires a later versioned contract/code change and meaningful boundary tests, including area equality, listed-use versus catch-all conditions, edition isolation, exception scope, and unknown inputs.

Owner: KIS Solutions. October 2026; source-grounded draft for engineering review.
