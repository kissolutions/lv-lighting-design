---
title: "Control Device and System"
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

# Control Device and System

Location: `control_devices[] / control_systems[]` in the draft v0.2 model.

Control devices represent individual hardware/software sources or interfaces such as occupancy sensing, timeswitches, manual inputs, power-loss signals, or gateways. Control systems represent software platforms, energy management, networks, or integration endpoints. Controllers own device-reference lists; power units record target/interface/role connections. A platform name and a communication protocol are recorded separately.

The [device hierarchy contract](device-hierarchy-v0.2.md) defines fields, ownership, derived views, validation scope, and migration boundaries. The [v0.2 schema](../../../schemas/lighting-project-v0.2.schema.json) is the executable data shape. Unknown fields remain `null`; relevant source references and engineering decisions remain explicit. Owner: KIS Solutions; October 2026; draft.


## Physical allocation extension

The [topology companion](controller-power-topology-v1.md) links existing IDs to QDCD/CIO/SW/PDU devices, sensor/port/control associations, supply feeds, locations and bus routes. Validate separately from electrical model checks.
