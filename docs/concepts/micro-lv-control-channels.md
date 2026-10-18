---
title: "Micro LV Control Channels"
page_type: concept
page_status: draft
confidence_level: medium
domain_primary: low-voltage-lighting
ai_role: explanation
invocation_triggers:
  systems_present: [low_voltage_lighting]
decision_axes: [channel_grouping, control_zoning, controller_outputs]
related_pages:
  - "channel-grouping.md"
  - "../ontology/canonical-model/m4-electrical-attributes-v0.6.md"
  - "../ontology/canonical-model/lv-light-zone.md"
---

# Micro LV Control Channels

## Definition

A Micro LV Control Channel is the smallest independently commanded physical LV lighting output group used by the M4 design.

Relationship:

`Functional Room/Control Zone -> one or more Micro LV Control Channels -> one physical output each`

A simple zone may be 1:1 with one micro channel. A zone may require several micro channels because of wattage, voltage, AC/DC type, CV/CC mode, driver/interface, fixture type, emergency classification, daylight subdivision, routing, or other physical constraints.

A micro channel may not span multiple functional zones in the M4 baseline. One zone may own many micro channels.

## Physical output relationship

Each micro channel maps 1:1 to the independently commanded physical output serving it. In the YMCA implementation this includes SmartControls QDCD output channels for driver-controller applications and the applicable EPS Edge Class 2 output arrangement for non-dimming constant-voltage applications.

Do not group fixtures by first choosing an available controller box and filling outputs. Define the required micro channels from fixture and functional constraints first, then assign eligible physical equipment/outputs.

## Hard grouping boundaries

Fixtures on one micro channel must have compatible:

- functional zone membership;
- AC/DC power type;
- CV/CC power mode;
- applicable nominal/min/max voltage requirements;
- CC current requirement where applicable;
- driver/interface requirements;
- emergency classification/behavior;
- required independent control behavior;
- product/output capability; and
- connected load within the selected design limit.

The M4 Class 2 baseline is 95 W maximum on a 100 W rated channel.

## Channel allocation objective — owner correction, October 18, 2026

**Call [PROC-M4-CHANNEL-PACK](../design-playbooks/m4-channel-packing-v0.1.md) for every M4 channel derivation, before assigning physical controller outputs.** This is a real, read-only executable service in `generators/channel_pack.py`, not merely a directive to stop after an allocation satisfies the 95 W limit.

Within hard electrical/functional boundaries, **minimize channel count first**; among equal-count feasible candidates, prefer utilization near **90 W per channel** (soft target). **95 W** is the nonnegotiable design maximum on the **100 W** rated Class 2 output, not the target. Report actual utilization per leaf zone and project, and whether optimality has been proved. Never force a 90 W target if practical routing/service or product requirements preclude it; capture those constraints in the input compatibility qualification/review.

Remote driver topology is **parallel only**. A two-wire daisy-chain run is not series-connected LEDs. Constant-current programmable remote driver output current is the sum of LED branch currents *when manufacturer-supported parallel operation is proven*. Do not mistake KCL for proof that the remote current regulator and the bare LED branches will share current stably. A verified approval/evidence cohort is required for multiple CC branches; no automatic series topology fallback.

Same selected fixture type and proximity are preferences, not electrical compatibility tests. Known routing/practical placement constraints may force a reviewed deviation from numerical minimum; record that reason. Unknown voltage, current, load or CC parallel sharing evidence is not permission to pass one fixture per channel as optimized.

## Orientation-independent adjacency

Do not implement adjacency as row/column clustering on a coordinate or as mandatory straight-run detection. Horizontal, vertical, diagonal, curved and grid arrangements must all be evaluated without favouring a drawing axis. Compare feasible compact partitions under the hard boundaries and the preference order above; a minimum channel count never overrides practical routing or service legibility. A fixture-count capacity formula applies only where compatible equal-load fixtures justify it; heterogeneous loads require actual load checks. Unknown loads remain unresolved, not repacked by assumed capacity.

Before accepting a building-wide packing result, check layouts against the dominant plan axis, curves and grids. Verify every included light is assigned exactly once, total load is unchanged and all channel limits/control boundaries are preserved. The dedicated packer now creates and evaluates channel proposals; existing canonical model validators still govern actual instantiated outputs. Multi-load CC output validation remains a separate evidence-contract integration gap, so packer reports are not themselves final design acceptance.

## Capability is not requirement

A zone requiring only on/off behavior may contain a physically dimmable fixture. That does not make the fixture non-dimming and does not change its electrical attributes. Conversely, a zone requiring dimming cannot be satisfied by a confirmed non-dimmable fixture/interface.

Owner: KIS Solutions. October 2026; draft pending YMCA M4 validation.
