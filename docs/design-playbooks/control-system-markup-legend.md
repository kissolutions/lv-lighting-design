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

## Connectivity and Readback

Draw and label PDnet, SDCnet, PDU power feeds and luminaire routes separately; route colors/line styles are not prescribed by the owner yet. Label route IDs, endpoints and bus/power role without inferring route color from device color. Show CIO associations, strings and PDU output/QDCD input mapping. Highlight unresolved locations, conflicts and specific owner questions. Retain editable unflattened annotations, saved coordinates and IDs; prove human edit/save/readback before promising a production markup workflow.
