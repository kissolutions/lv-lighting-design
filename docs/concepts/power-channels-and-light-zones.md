---
title: "Power Channels and LV Light Zones"
page_type: concept
page_status: draft
confidence_level: medium
domain_primary: low-voltage-lighting
ai_role: explanation
invocation_triggers:
  systems_present: [low_voltage_lighting]
decision_axes: [power_grouping, functional_zoning, many_to_many_loads]
related_pages:
  - "../ontology/canonical-model/device-hierarchy-v0.2.md"
---

# Power Channels and LV Light Zones

A power channel describes a supply output. An LV light zone describes lights operated as a functional group. Supply topology and control topology therefore need separate identities.

Zone A can contain a 20 W light on Channel 1 and a 25 W light on Channel 2. Zone B can contain a 30 W light on Channel 1. Zone A totals 45 W; Zone B totals 30 W; Channel 1 totals 50 W; Channel 2 totals 25 W. Overall light load is 75 W when viewed through either grouping.

The light objects establish the relationship. Each is stored once, inside its zone, and references its power channel. Channel-zone lists and zone-channel lists are derived. This avoids duplicating fixtures or charging all of a zone's watts to every associated channel.

Sharing a supply output still requires compatible electrical behavior and valid downstream control paths. Controller capacity is measured in independent control outputs; power-unit capacity is measured in power outputs and aggregate watts. The two output counts need not match.

MEP source zones belong in the source-intent records currently named `control_groups`. They supply design intent and constraints; they are not our LV zones. Local LV zones reference the applicable source requirements and must satisfy them while retaining separate occupancy, dimming, emergency, or other functional behavior. Source zone numbering alone does not select a controller output or power channel. Preserve and flag conflicts for review instead of changing the source intent to fit the LV design.

This concept explains the owner-provided hierarchy. The [draft contract](../ontology/canonical-model/device-hierarchy-v0.2.md) defines data ownership and checks.
