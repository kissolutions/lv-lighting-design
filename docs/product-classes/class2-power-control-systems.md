---
title: "Power and Control System Constraint Intake"
page_type: product_class
page_status: draft
confidence_level: medium
domain_primary: low-voltage-lighting
ai_role: constraint_source
invocation_triggers:
  systems_present: [low_voltage_lighting]
decision_axes: [product_capacity, electrical_compatibility, control_architecture]
related_pages:
  - "../design-playbooks/lighting-design-playbook.md"
  - "../ontology/canonical-model/power-node.md"
---

# Power and Control System Constraint Intake

## Scope

Record how verified product constraints affect this extension. Device-level ratings and manufacturer facts belong in the shared knowledgebase and project source register. No manufacturer platform has been selected for this foundation.

## Required evidence before confirming a design

| Constraint | Design consequence |
|---|---|
| Output interface, voltage/current behavior, compatible drivers | Defines confirmed compatibility groups |
| Verified per-channel output and applicable installation limits | May lower the <=90 W design limit |
| Number of usable channels and aggregate output budget | Determines actual power-node quantity |
| Dimming/control architecture and zoning behavior | Determines control boundaries and separate control-node needs |
| Fixture input load at the channel interface | Determines channel connected watts |
| Class 2 listing/eligibility, cable and installation restrictions | Requires product/project review beyond software wattage checks |
| Emergency/egress functionality or other special loads | Triggers project-specific engineering |

## Application

Register evidence and record the selected device class, channel capacity, and aggregate design capacity on each explicit power node. A matching compatibility label is a consistency assertion based on reviewed facts. It is not evidence by itself.

If a selected system does not fit the initial 100 W nominal model, revise the model/playbook deliberately rather than overriding the schema to make it pass.
