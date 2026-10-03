---
title: "Emergency Lighting Control Intake"
page_type: playbook
page_status: draft
confidence_level: medium
domain_primary: low-voltage-lighting
ai_role: prescriptive_standard
invocation_triggers:
  systems_present: [low_voltage_lighting]
  uncertainty_flags: [emergency_lighting_present]
decision_axes: [normal_operation, emergency_override, backup_supply, outage_signaling]
related_pages:
  - "../ontology/canonical-model/device-hierarchy-v0.2.md"
---

# Emergency Lighting Control Intake

For every source emergency/nightlight/standby indication, preserve the observed fixture type, notes, original branch label, and source control intent before deciding how the LV system will reproduce the function.

1. Determine normal behavior: controlled, always on, or normally off/standby. A battery-pack notation alone does not settle that question.
2. Identify which lights require an emergency force-on response. Place them in LV strings/zones with a controllable output that can execute that response.
3. Confirm the selected backup provision independently: fixture battery, central UPS/battery, or other engineered supply. Preserve source battery information even if the design replaces it.
4. Identify the normal supply loss being monitored. Record the monitored circuit and sensing source; do not use a generic building outage signal without confirming that it represents the required event.
5. Specify the controller receiving the event, input/interface, trigger condition, affected outputs, override action, and return-to-normal behavior. Record unknowns as blocking items.
6. Confirm controller/control-path operation during the outage. Identify any additional signal cable, input module, contact, gateway, termination, or programming that the architecture requires.
7. Review separation from normal strings. Preserve normal occupancy/timeswitch/dimming behavior while confirming how the emergency override takes priority.
8. Verify runtime, listing, illumination, transfer behavior, and failure response in the project-specific emergency design. These items are not established by a fixture suffix or the draft consistency checker.

The current draft records and checks declared relationships, emergency input confirmation, and backup provisions. Signal-route lengths, automatic failure-state evaluation, commissioning tests, and construction release remain project engineering work. Owner: KIS Solutions; October 2026; draft.
