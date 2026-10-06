---
title: "Topology Device Review v1.1"
page_type: canonical_model
page_status: draft
confidence_level: medium
domain_primary: low-voltage-lighting
ai_role: model_contract
invocation_triggers:
  systems_present: [low_voltage_lighting]
decision_axes: [milestone_review, zone_hierarchy, markup_identity, owner_review]
related_pages:
  - "https://github.com/kissolutions/lv-lighting-design/blob/main/docs/design-playbooks/milestone-review-packages.md"
---

# Topology Device Review v1.1

[Schema](../../../schemas/controller-power-topology-v1.1.schema.json) · [Seed](../../../templates/controller-power-topology-v1.1.template.json).

Preserves the v1.0 power-feed, bus, sensor and location contract. Each device additionally requires `display_tag`, descriptive `name`, nullable `room_id`, and `review_category` (room_device/equipment). Use room_device for every narrative-required field device, including unfamiliar devices represented as kind other; room_id links the associated served Room, while location.area_id describes mounting location. Do not infer function from a tag alone. `rationale` records narrative function for room devices and allocation rationale for equipment.

Typical display tags: OS-01, DS-01, WC-01, WD-01; equipment QDCD-01, PDU-01, CIO-01, SW4-01/SW8-01. Keep existing device IDs stable and display tags unique. Schedule Room names derive from the linked Room ID. Functional zone/subzone IDs derive from control_connections, preserving many-to-one physical devices. The devices' location remains explicitly proposed until owner-returned markup is reconciled.

`validate_topology` supports both versions and checks room-reference validity/tag uniqueness in v1.1. A version change does not manufacture names or device/zone assignments. Populate them from the approved narrative and current inventory. This update requires no build to install and does not automatically migrate project-instance JSON.
