---
title: "Controller/Power Topology Companion v1.0"
page_type: canonical_model
page_status: draft
confidence_level: medium
domain_primary: low-voltage-lighting
ai_role: model_contract
invocation_triggers:
  systems_present: [low_voltage_lighting, smartdc]
decision_axes: [power_allocation, controls, equipment_placement, owner_review]
related_pages:
  - "https://github.com/kissolutions/knowledgebase_wikijs/blob/main/design-playbooks/smartdc-allocation-index.md"
---

# Controller/Power Topology Companion v1.0

## Purpose and Compatibility

Versioned companion JSON pairs with an accepted v0.6 project. It supplies first-class AHJ and area plenum facts early, then device/port/feed/sensor/bus/spatial records without modifying fixture or channel identities. Energy-code basis remains authoritative in the v0.6 project. This companion must be validated separately; existing electrical validators do not check it.

[Schema](../../../schemas/controller-power-topology-v1.schema.json) · [Seed](../../../templates/controller-power-topology-v1.template.json) · [Workflow](../../design-playbooks/controller-power-placement.md).

## Records and Ownership

`project_id` matches the canonical project; `model_revision` identifies the companion revision. `ahj` and `ahj_source_ref_ids` capture authority, independently of jurisdiction wording. `areas[]` references served/mounting Spaces and tri-state return-air-plenum status. Areas can split a Space if ceiling conditions differ; never collapse mixed conditions to a building-wide boolean.

`devices[]` describes proposed equipment/field devices; link `canonical_entity_id` where a corresponding controller/control-device/power-unit already exists. It does not duplicate their lighting objects. Device kind determines legend symbol/color. `location` references mounting area and drawing page/displayed point; unknown values remain null and owner review remains explicit. Rated power, connected input demand, verified available input watts and bus current are distinct.

`channel_assignments[]` references existing canonical micro-channel IDs and their functional zone IDs; one micro channel per controller/PDU output, no changes to upstream electrical membership. `power_feeds[]` maps PDU output to QDCD input, independently of lighting assignments; separate feed and input identities prevent double counting. `reduced_feed_decisions[]` records 1–3 feed rationale, owner decision and hardware verification. Total input demand must include losses/auxiliaries before comparing supply budgets.

`control_connections[]` counts unique physical sensors/wall devices and binds one wired port (or Casambi wireless association) to served zones/channels/QDCDs. A physical device can serve multiple zones without duplicating it. `bus_assignments[]` records CIO/network membership and verified peripheral bus-unit count; unknown SW counting remains null. `routes[]` stores ordered device strings, displayed page points and route/network identity. Measured physical length differs from displayed coordinate distance; `distance_from_cio_ft` requires manufacturer-consistent interpretation. `spec_verified` never follows merely from length under 250 ft.

`count_review` stores feasible minima only after constraints are reviewed; the checker derives output/port lower bounds and installed counts. Open items preserve uncertainty and dependent blocking. References to real owner decisions and source evidence remain in the canonical ledger; project PDFs and JSON stay outside Git.

## Implemented and Manual Checks

The companion checker verifies structure/IDs, links to canonical channels/zones/Spaces/pages/evidence, output/input/port collisions, family count capacities, Smart direct service, feed exceptions, aggregate recorded wattage, bus counts/current/distance, plenum placement, coordinates and device associations. Unknown capacities, CIO location and unverified routes remain review gaps. It does not prove fixture electrical compatibility, sensor coverage, reduced-feed routing, control precedence, physical installation suitability or editable PDF delivery; apply existing v0.6 checks and manufacturer/owner review too.

Run `python -m generators.validate_topology topology.json --model lighting-model.json` for review, adding `--final` for dependent completeness gates. No build is required to copy these framework files into the repository.


## Device-review extension v1.1

[Topology v1.1 device review](topology-device-review-v1.1.md) adds display tag, name, associated Room ID and room-device/equipment review category. Existing topology v1 remains supported; use v1.1 for new milestone device schedules.
