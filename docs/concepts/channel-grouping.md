---
title: "Channel Grouping as a Constrained Design Problem"
page_type: concept
page_status: draft
confidence_level: medium
domain_primary: low-voltage-lighting
ai_role: explanation
invocation_triggers:
  systems_present: [low_voltage_lighting]
decision_axes: [channel_count, load_margin, geographic_grouping]
related_pages:
  - "../design-playbooks/lighting-design-playbook.md"
---

# Channel Grouping as a Constrained Design Problem

This page explains the original v0.1 baseline. The current [power-channel/LV-zone concept](power-channels-and-light-zones.md) supersedes its assumption that one power channel must have one zone. Electrical compatibility and required downstream functional boundaries remain constraints.

## Explanation

Grouping is a partition of included fixtures subject to zoning, compatibility, and load constraints. The design belongs in the model; a PDF overlay is its presentation.

For channel c, connected watts = sum of each assigned fixture's confirmed LV input watts. Under the baseline, connected watts <= design limit <=90 W. The unused margin is design limit minus connected watts.

Zone and compatibility groups split the candidate set before channel utilization is considered. Within each set, compact groups reduce difficult routing, but a small channel count cannot justify lost control boundaries.

Example: four compatible 20 W fixtures in one zone fit on one 80 W channel. Five require at least two channels under a 90 W ceiling. Four 20 W fixtures split across two required zones need at least two channels despite an 80 W combined load.

## Limits

This explains the handoff's reasoning. Prescriptive rules belong in the [playbook](../design-playbooks/lighting-design-playbook.md). The current tool checks assignments; it does not optimize them. Electrical compatibility and routing practicality still require evidence and engineering judgment.
