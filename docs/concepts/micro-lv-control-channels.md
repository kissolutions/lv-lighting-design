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

## Preferred grouping behavior

Within the hard constraints, prefer:

1. spatial adjacency and practical routing;
2. same selected fixture type;
3. simple service/commissioning identification;
4. balanced utilization without exceeding 95 W; and
5. minimal channel count only after the prior constraints are satisfied.

Same fixture type is a preferred simplifier, not automatically a universal electrical law. Mixed fixture types require explicit compatibility evidence; constant-current mixed-fixture topology remains a manual-review condition until the model supports it fully.

## Capability is not requirement

A zone requiring only on/off behavior may contain a physically dimmable fixture. That does not make the fixture non-dimming and does not change its electrical attributes. Conversely, a zone requiring dimming cannot be satisfied by a confirmed non-dimmable fixture/interface.

Owner: KIS Solutions. October 2026; draft pending YMCA M4 validation.
