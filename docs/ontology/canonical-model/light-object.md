---
title: "Light Object"
page_type: canonical_model
page_status: draft
confidence_level: medium
domain_primary: low-voltage-lighting
ai_role: model_contract
invocation_triggers:
  systems_present: [low_voltage_lighting]
decision_axes: [device_hierarchy, source_traceability]
related_pages:
  - "device-hierarchy-v0.2.md"
---

# Light Object

The [v0.5 extension](electrical-interfaces-v0.5.md) adds selected `design.input_voltage`, `input_power_mode` and `input_current_ma` at the assigned supply-channel interface. Preserve source fixture/type voltage independently; a replacement or verified downstream interface can differ. Voltage/mode/current checks supplement watts and compatibility groups without changing physical identity or Space/zone membership.

Selected `design.driver_type`/`driver_note` describe driver/driverless/other architecture, independently of source type and dimming/CV-CC mode. Unknown selected architecture is a later-design blocker; other requires a description. Legacy zone `driver_type` retains its dimming/non-dimming meaning.

Current [v0.4](physical-intake-v0.4.md) stores each physical light once in root `light_objects[]`. It has exactly one primary served Space at intake and may have no zone yet. Later zones reference its ID; do not duplicate or move the authoritative physical record merely to change logical grouping. The nested location below describes legacy v0.2/v0.3 only.

In v0.3, optional `mounting` contains nullable `height_above_served_floor_ft`, `height_basis` (source_document/measured/estimated/unknown), nullable `note`, and `source_ref_ids`. Height is measured above the primary served floor. Keep the source drawing page independent of the Space's occupied level. A light over an open-to-below reception belongs to the reception floor it primarily illuminates. Qualitative high mounting leaves height null with a verification note; numerical estimates require an estimated basis and note. Mounting evidence references registered sources and does not promote unknown heights to measurements.

In [v0.3](space-context-v0.3.md), each light is also referenced by exactly one Space. Keep its internal ID stable when changing a room name, zone, or channel. Derive room fixture-type quantities from those references; a visible fixture label is optional.

When producing M2 fixture-ID markups, use [fixture display numbering](../../design-playbooks/m2-fixture-numbering.md). The existing `label` stores the readable L001-style number; `id` remains the permanent reference identity. Project-wide type blocks and room-local clockwise order are presentation rules, not source marks, zones or power-channel assignments. Keep revision crosswalks and annotation mappings when display labels change.

Location: `light_zones[].light_objects[]` in the draft v0.2 model.

Represents one selected single-input LV lighting occurrence with stable internal identity. Preserves source type, branch/zone observations, page, optional anchor and annotation ID separately from selected LV load, compatibility, channel, backup provision, and selection/assignment decision. Load can be per fixture, per foot, or per reference length. Future split-input/segmented fixtures need an explicit extension; do not duplicate physical fixtures to work around it.

At M2 physical intake, one Light Object may track one [source linear run](../../design-playbooks/m2-linear-fixture-extraction.md). A same-type continuous/apparently continuous path counts once even through corners or repeated type marks; separate paths count separately and ambiguity remains explicit. This run count does not establish one manufactured section or one feed/channel. Keep unconfirmed length/load/topology unknown; later single-input selection requires supported electrical structure. Do not duplicate whole runs to represent feeds or insert unsupported segment fields into the current schema.

The [device hierarchy contract](device-hierarchy-v0.2.md) defines fields, ownership, derived views, validation scope, and migration boundaries. The [v0.2 schema](../../../schemas/lighting-project-v0.2.schema.json) is the executable data shape. Unknown fields remain `null`; relevant source references and engineering decisions remain explicit. Owner: KIS Solutions; October 2026; draft.
