---
title: "Space"
page_type: canonical_model
page_status: draft
confidence_level: medium
domain_primary: low-voltage-lighting
ai_role: model_contract
invocation_triggers:
  systems_present: [low_voltage_lighting]
decision_axes: [room_conditions, code_classification, fixture_membership, traceability]
related_pages:
  - "space-context-v0.3.md"
  - "../../../schemas/lighting-project-v0.3.schema.json"
---

# Space

## Purpose and Scope

A room or bounded area supplying the conditions for energy-code analysis, controls, zoning, and channel grouping. Location: `spaces[]` in v0.3. Use Space as the general entity for enclosed rooms and source-designated or owner-reviewed logical areas within larger enclosures. Initial open-area subdivisions may have approximate review boundaries; distinguish those proposals and proposed names from architectural source facts until accepted under the [boundary workflow](../../design-playbooks/architectural-space-intake.md#enclosed-rooms-and-logical-open-areas). A logical Space is not automatically an independent lighting-control zone.

## Fields and Meaning

| Fields | Meaning |
|---|---|
| `id`, `name`, `room_number`, `description` | Stable identity, plan-facing name/number, and custom location/use description |
| Optional `level` | Occupied/served level, independent of fixture mounting elevation or source sheet. Null for a multi-level Space whose extent is described in `description` |
| Optional `inventory_only` | Explicit unlit service-void/chase inventory record. Requires location/purpose/uncertainty in `description` and empty light/zone lists; not a lighting design or code exemption |
| `area_sq_ft`, `area_basis`, `area_note` | Known area or null; source/measured/estimated/unknown basis and limitations |
| `source_room_type` | Plan label or ordinary use, preserved as source information |
| `building_code_space_type` | Independently selected space function for building-code analysis |
| `building_code_occupancy_group` | Separate building-code occupancy group; unknown remains null |
| `energy_code_space_type` | Selected energy-code function, e.g. enclosed office or open office |
| `energy_classification_basis`, `energy_classification_note`, `energy_classification_decision_id` | Explanation and decision for the selected/inferred energy type |
| `enclosure` | Enclosed, open, another bounded area, or unknown |
| `has_windows` | Window presence; not an automatic control requirement |
| `has_daylight_zone` | Geometric daylight-zone presence; not an exemption flag |
| `daylight_control_required`, `daylight_assessment_note` | Control applicability and its basis; unknown remains null |
| `code_references[]` | Standard, edition, section, reason, URL, applicability status, and decision |
| `drawing_page_ids`, `source_ref_ids` | Source evidence and pages where the Space appears |
| `light_object_ids`, `light_zone_ids` | References only; no duplicate objects or editable quantity totals |
| `decision_id` | Engineering basis for conditions and membership |

The selected project code, edition, jurisdiction, amendments review, evidence, and decision live in `project.energy_code_basis`. Room references do not establish local adoption or combine alternative compliance paths.

## Relationships

Zones continue to own light objects; channels remain inside power units. Spaces reference those existing objects. Every modeled physical light has exactly one primary served Space membership, selected by the occupied floor/working area primarily illuminated. Lights above an open-to-below portion of a room remain in that room unless a separate Space is established by source designation or reviewed use. Fixture mounting height and source sheet do not change the occupied level. Preserve shared-service uncertainty in descriptions and open items without duplicating lights.

A Space may reference several zones; a named shared zone may serve several Spaces after review of independent operation. Every zone containing a Space's lights must be referenced. An additional named zone may serve a Space without a directly assigned light, such as another stair level, when a description and confirmed membership decision document that relationship. Room-default zones still serve one Space. Zone membership derives from explicit Space references and is cross-checked against light ownership.

Either represent a physical stair as one multi-level Space with described extent, or retain architectural level-specific records. Preserve the specified MEP stair scheme; use one shared zone per physical stair only when documented operation and reviewed independent-control constraints support it. Describe and resolve source conflicts before either sharing or splitting. Untagged chases/service voids remain in the inventory with `room_number: null`; absence of lights is not absence of a Space. Use narrative boundary evidence and a discrepancy for uncertain consequential partial walls/open edges; a wall object catalog is not required. Follow [architectural space intake](../../design-playbooks/architectural-space-intake.md).

Fixture-type quantities, connected light watts, and channel IDs are derived. Stable type IDs are the count-grouping keys; visible marks alone need not be unique across schedules/revisions.

## Constraints and Validation

The checker verifies references, membership, zone-list agreement, source pages, condition/evidence readiness, and inherited hierarchy checks. It does not infer building-code classification from energy classification, calculate daylight geometry, resolve code exceptions, or certify compliance. Passing checks does not promote estimated area to a measurement; revisit estimates when proximity to a threshold could change the outcome.

## Sources and Stewardship

Owner-defined extension; KIS Solutions; October 2026; draft. The preserved v0.1 `facts.spaces[]` stores only ID/name/page/source context and remains consumed by the v0.1 tools. Read the [v0.3 contract](space-context-v0.3.md) for this extension and the identity/display policy.
