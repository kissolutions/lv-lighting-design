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

Current [v0.4](physical-intake-v0.4.md) stores each physical light once in root `light_objects[]`. It has exactly one primary served Space at intake and may have no zone yet. Later zones reference its ID; do not duplicate or move the authoritative physical record merely to change logical grouping. The nested location below describes legacy v0.2/v0.3 only.

In v0.3, optional `mounting` contains nullable `height_above_served_floor_ft`, `height_basis` (source_document/measured/estimated/unknown), nullable `note`, and `source_ref_ids`. Height is measured above the primary served floor. Keep the source drawing page independent of the Space's occupied level. A light over an open-to-below reception belongs to the reception floor it primarily illuminates. Qualitative high mounting leaves height null with a verification note; numerical estimates require an estimated basis and note. Mounting evidence references registered sources and does not promote unknown heights to measurements.

In [v0.3](space-context-v0.3.md), each light is also referenced by exactly one Space. Keep its internal ID stable when changing a room name, zone, or channel. Derive room fixture-type quantities from those references; a visible fixture label is optional.

When producing M2 fixture-ID markups, use [fixture display numbering](../../design-playbooks/m2-fixture-numbering.md). The existing `label` stores the readable L001-style number; `id` remains the permanent reference identity. Project-wide type blocks and room-local clockwise order are presentation rules, not source marks, zones or power-channel assignments. Keep revision crosswalks and annotation mappings when display labels change.

Location: `light_zones[].light_objects[]` in the draft v0.2 model.

Represents one selected single-input LV lighting occurrence with stable internal identity. Preserves source type, branch/zone observations, page, optional anchor and annotation ID separately from selected LV load, compatibility, channel, backup provision, and selection/assignment decision. Load can be per fixture, per foot, or per reference length. Future split-input/segmented fixtures need an explicit extension; do not duplicate physical fixtures to work around it.

The [device hierarchy contract](device-hierarchy-v0.2.md) defines fields, ownership, derived views, validation scope, and migration boundaries. The [v0.2 schema](../../../schemas/lighting-project-v0.2.schema.json) is the executable data shape. Unknown fields remain `null`; relevant source references and engineering decisions remain explicit. Owner: KIS Solutions; October 2026; draft.
