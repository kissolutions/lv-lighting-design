---
title: "LV Lighting Control Application Guide"
page_type: playbook
page_status: draft
confidence_level: medium
domain_primary: low-voltage-lighting
ai_role: prescriptive_standard
invocation_triggers:
  systems_present: [low_voltage_lighting]
decision_axes: [room_design, energy_code_basis, sensor_coverage, control_sequences, channel_grouping]
related_pages:
  - "iecc-occupant-sensor-directives.md"
  - "architectural-space-intake.md"
  - "lighting-design-playbook.md"
  - "../ontology/canonical-model/space-context-v0.3.md"
---

# LV Lighting Control Application Guide

## Authority and Role in the LV Workflow

WikiJS is KIS's main electrical engineering knowledgebase and owns the general lighting application guide, room/code analysis, sensor/switch/controller selection/configuration and decision trees. This local draft preserves proposed guide content for alignment with WikiJS and records its LV use; it is not a competing design authority. Verified existing entry points are [Interior Space Types](https://github.com/kissolutions/knowledgebase_wikijs/blob/main/ontology/reg-and-class/interior-space-types.md), [Open Office Controls](https://github.com/kissolutions/knowledgebase_wikijs/blob/main/design-playbooks/open-office-lighting-controls-playbook.md), and [Enclosed Office Controls](https://github.com/kissolutions/knowledgebase_wikijs/blob/main/design-playbooks/enclosed-office-lighting-controls-playbook.md). A completed shared application-guide page has not yet been established here.

LV projects start by extracting the MEP control scheme. Use the supported general guidance as a check on that scheme, preserving source observations and review findings. Do not automatically create or replace sequences or sensor quantities from a room recipe. An alternative design is conditional on authority and approval. Follow the [LV workflow](lv-project-workflow-and-readiness.md).

The local [edition-specific IECC directives](iecc-occupant-sensor-directives.md) are draft code-support material for shared-guide development and cited checks. The intended WikiJS guide supplies the general engineering implementation layer through approved room examples. Manufacturer facts and coverage limits remain in the shared knowledge repository and are referenced here; do not replace them with generic area-per-sensor assumptions. ASHRAE-based examples require a separately verified code profile rather than mixing its requirements into IECC examples.

An approved, applicable example can supply verification criteria. For explicitly authorized redesign, it may also support a proposed alternative; adoption of that alternative requires approval. Automated replacement of extracted MEP design is not the LV workflow. Draft examples remain review proposals. Unknown room facts, unverified equipment coverage, missing code text, and unmatched conditions are flagged for discussion. Preserve owner-confirmed classifications and decisions.

## Required Contents of a Room Example

| Part | Required information |
|---|---|
| Identity and status | Stable example ID, revision, owner approval, and draft/approved status |
| Applicability | Energy-code room type, code edition/profile, area range, enclosure, geometry, occupied activity, mounting-height range, and exclusions |
| Code basis | Requirement/exception references with verified inputs; distinguish code minimum from KIS design choices |
| Control areas | Room boundary, independent occupancy zones, daylight/manual subdivisions, maximum applicable zone area, and boundary-review notes |
| Sensor design | Referenced sensor model/technology, coverage evidence, placement pattern, physical quantity or conditional quantity rule, obstructions, and expansion triggers |
| Activation | Manual-on, partial-on percentage, or permitted full-on; manual-off arrangement and override behavior |
| Vacancy | Delay, full-off or reduced-power setpoint, affected area, and return-to-occupancy behavior |
| Time-switch operation | When required, scheduling basis, holidays, override area/duration, interaction with occupant sensors, and handling of unknown schedules |
| Dimming/daylight | Applicable independent requirements and coordinated actions; do not equate partial-on permission with a universal dimming mandate |
| Emergency/egress | Normal sequence, emergency override, power-loss/backup behavior, and explicit applicability review |
| LV implementation | Functional zones, downstream controller inputs/outputs, channel-grouping constraints, and verified load limits |
| Verification | Source/code review, coverage/layout review, expected sequence checks, and required functional testing |

## Sensor Quantity Rules

Separate three outputs: the code-required independent control areas, the physical sensing devices, and the controller/channel arrangement. The application guide ties them together without treating them as interchangeable counts.

For an open-office example, first derive the code-driven lower bound on independent zones from the selected profile, then design and verify the actual zone polygons. A KIS example may specify one sensor per independently sensed zone when the referenced device and placement pattern cover that zone under the example's approved conditions. Add sensors when geometry, partitions, mounting height, activity, or other coverage limits require them. The guide must state those triggers and how sensor inputs combine within a zone.

That one-per-zone pattern is a conditional KIS design rule, not a universal statement that the code requires one physical sensor per a fixed number of square feet. Approve it only with verified equipment and layout evidence. Alternative arrangements, including multiple sensing devices per zone or independently resolved sensing areas within one device, require their own verified example.

When an approved example matches, produce a proposed physical sensor count and identify the example revision, matching conditions, and coverage basis. Verify the applied layout before finalizing the count. When no approved example matches, leave the count unresolved and flag the condition. A preliminary owner-selected allowance remains explicitly preliminary.

## Initial Example Catalog

These are example families to develop, not approved sensor-count or control recipes. Edition-specific numeric control requirements come from the cited code profile; do not populate missing rules by analogy.

| Family | Design questions the example must resolve |
|---|---|
| Single enclosed office | Wall versus ceiling sensing, coverage, manual/partial-on, vacancy shutoff, daylight subdivision |
| Open office | Independent occupancy-zone layout, physical sensors per zone, partitions/activity, local versus whole-space vacancy, scheduling interaction |
| Meeting/classroom/multipurpose room | Occupied activities, sensing coverage, manual/partial-on, dimming/presentation actions, daylight and overrides |
| Restroom/locker room | Compartments and blind spots, full-on permission, manual controls, vacancy behavior |
| Storage/janitorial room | Confirmed use, racks/obstructions, sensing and activation, distinction from warehouse aisle controls |
| Warehouse storage | Independent aisles/open areas, sensor placement, vacancy reduction and scheduled shutoff |
| Corridor | Geometry/coverage, applicable reduction rule, illumination exception evidence, egress and adjacent-area triggering |
| Lobby/reception/open circulation | Confirmed use and architectural boundaries, high-mounted fixtures, sensing height, daylight and scheduling |
| Physical stair | Shared multi-level zone, sensing at occupied access points, required illumination, normal/emergency sequence |
| Other or specialized space | Named/catch-all rule applicability or manual discussion; no unsupported classification |

## Applying and Approving Examples

Complete room/source verification and reviewed area takeoff first. Confirm actual use separately from building-code classification and select the project code profile. Compare the extracted MEP scheme with applicable supported criteria, recording findings without overwriting the scheme. Only for authorized redesign, match an approved example and emit a proposed alternative with evidence, exceptions and approval status. Review deviations and unknowns before final implementation.

To approve a new example, verify the relevant final code text/errata and project-independent applicability, the referenced equipment facts, the boundary/coverage pattern, and the control sequence. Record owner approval and revise affected examples when their sources change. An adopted project amendment or a different sensor model may invalidate the match and require a new variant.

The current schema and generators validate entered model data. They do not yet select examples, calculate sensor coverage/counts, evaluate all code requirements, or generate these designs automatically. This draft defines material for the shared guide and its future verification/authorized-redesign application; implementation needs a subsequent versioned change with tests for applicability boundaries, unknowns, and conflicting requirements.

Owner: KIS Solutions. October 2026; owner-directed application-guide structure, draft pending example development.
