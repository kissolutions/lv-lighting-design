---
title: "Lighting Electrical Equipment Graph v0.10 — X1/X2/X4"
page_type: canonical_model
page_status: draft
domain_primary: low-voltage-lighting
ai_role: model_contract
---

# Electrical Equipment Graph v0.10 (X1, X2, X4)

## Purpose and scope

**Version 0.10.0 is an explicit, opt-in model upgrade** from v0.9.0. The version 0.9 schema and accepted records remain available and unchanged. Engineering topology and owner acceptance remain authoritative. Do not silently migrate or rewrite a client's accepted M4 workbook/model; keep before-and-after field maps and an owner review. This contract eliminates structural misclassification of EPS PDUs as AC branch circuits and AC input phases on DC-fed QDCD drivers, and establishes one functional zone to many independently commanded output channels.

### Object model

```text
Real AC Branch Circuit (panel, circuit ID, protection)
       |
       v
Distribution Unit: EPS PDU (equipment, AC-to-Class-2 DC)
       | PDU output 1..16/32
       |     one dc_power_feed per physical output/input pair
       v
Power Unit: QDCD (DC-fed remote programmable LED driver)
       | owned independently commanded output channels 1..4
       v
Micro LV Channel -> one functional endpoint Light Zone -> Light Objects
```

The PDU is **equipment**, never an AC `branch_circuit`. The QDCD is both an independently modeled controller and a `power_unit` with `controller.integrated_power_unit_id` referencing that unit; each of its four actual LED-driver outputs is one canonical `channel` owned by the power unit. A PDU does not own fixture microchannels. QDCDs consume upstream DC **feeds** at assigned input positions, each traceable to a particular physical PDU output.

## New v0.10 fields and semantics

| Object | Contract |
|---|---|
| Root `branch_circuits[]` | **Real AC circuits only.** Own `power_unit_ids[]` for directly AC-fed converters. Real PDU AC supply is referenced by the PDU instead. No PDU-as-branch alias. |
| Root `distribution_units[]` | Physical PDU: `id`, `equipment_class`, `input_branch_circuit_id`, `input_power_type`, `input_voltage`, `output_count`, aggregate rating and provenance. |
| Root `dc_power_feeds[]` | Directed port/connection identity: `source_distribution_unit_id`, `source_output`, `target_power_unit_id`, `target_input`, `rated_watts`, `demand_watts`, evidence/decision refs. |
| Root `power_units[]` | Independent of branch circuits. Each unit has `input_power_type` (AC/DC), `input_voltage` nominal/min/max, optional `ac_input_phases` (must be null for DC), `input_feed_ids[]` (the upstream DC connections), and existing owned `channels[]` and capacities. |
| `light_zones[].channel_ids[]` | Every channel serving that endpoint zone. Channels individually declare `light_zone_id`, `controller_id` and `controller_output`. Remove the old scalar zone controller/output pair. |

**X1:** `zone.channel_ids` equals the channels whose `channel.light_zone_id` points to that zone. One zone may own several channels, including channels on multiple QDCD devices. A parent/container zone owns none. A channel never serves several independently controlled endpoint zones.

**X2:** Model physical AC circuit, PDU, PDU outputs/feeds, QDCD and QDCD outputs distinctly. The original controller-power topology companion can remain a separate placement/routing view; its `power_feeds` must reconcile to canonical `dc_power_feeds` by physical endpoints when an accepted v0.10 model is produced. Do not invent PDU hardware identity or PDU circuit numbers during migration.

**X4:** A DC-fed power unit does not require AC phases and supports a voltage *range* (e.g., min 24 V, max 57 V) and explicit upstream feed IDs. The hardware's verified range is manufacturer evidence, not a inferred requirement. Single/three phase belongs only to AC connections.

### Worked example (abbreviated, illustrative)

```json
{
  "branch_circuits": [
    {"id":"BC-1","panel_ref":"LP1","circuit_label":"12","voltage_v":120,
     "phases":1,"breaker_amps":20,"power_unit_ids":[]}
  ],
  "distribution_units": [
    {"id":"PDU-1","label":"EPS PDU 16","equipment_class":"eps_pdu",
     "input_branch_circuit_id":"BC-1","input_power_type":"ac",
     "input_voltage":{"nominal_v":120,"min_v":null,"max_v":null},
     "output_count":16,"rated_total_output_watts":1600}
  ],
  "dc_power_feeds": [
    {"id":"F-01","source_distribution_unit_id":"PDU-1","source_output":1,
     "target_power_unit_id":"QDCD-PU-01","target_input":1,
     "rated_watts":100,"demand_watts":88}
  ],
  "power_units": [
    {"id":"QDCD-PU-01","input_power_type":"dc",
     "input_voltage":{"nominal_v":48,"min_v":24,"max_v":57},
     "ac_input_phases":null,"input_feed_ids":["F-01"],
     "channels":[{"id":"CH-01","light_zone_id":"Z-A","controller_id":"QDCD-01","controller_output":1}]}
  ],
  "light_zones": [
    {"id":"Z-A","channel_ids":["CH-01","CH-02","CH-03"]}
  ]
}
```

This is a **field-focused example, not a complete schema-valid JSON model**. The full model also requires ratings, source refs, project identity, control and light records, and each referenced channel must physically exist.

## Upgrade and validator

```python
from generators.model_equipment_v10 import upgrade_v10
from generators.model_intake import check_model

new_model = upgrade_v10(accepted_v09_model)  # returns a copy
review = check_model(new_model, phase="intake")
```

CLI: `python -m generators.model_equipment_v10 accepted_v09.json --upgrade-output new_v10_draft.json`, then `python -m generators.model_intake new_v10_draft.json --phase intake`. An existing output file is never overwritten.\n\nThe upgrader moves existing nested power units into root `power_units[]` and records original branch ownership through `branch.power_unit_ids[]`. It does **not** infer a PDU from a Timmons legacy branch that used a PDU name, and cannot fabricate manufacturer ratings, actual AC circuit, voltage-range data or PDU-to-QDCD DC feeds. Those require reviewed remapping with traceable evidence. Thus upgrading a prior Timmons workaround is **not** an electrical reconciliation or release.

The v0.10 validator checks electrical graph cardinality, upstream connections, DC phase exclusion, output/input collisions, channel ownership, PDU and per-feed capacity, as well as legacy validations via an **in-memory-only** compatibility projection. The synthetic compatibility container is not serialized or an actual branch circuit. The old legacy AC power-unit and scalar-zone controller checks are excluded in favor of the v0.10 contract; unrelated findings remain. This is the first contract revision: existing topology companion, export projections and all project-local drawing generators should be checked for v0.10 compatibility before operational deployment.

## Acceptance and issue disposition

Maintain accepted M4 physical layout and owner edits until explicitly remapped. Each proposal issue X1/X2/X4 is **schema-and-core-validator implemented**; this does not mean historical missing manufacturer values or the remaining Timmons issues have been solved. Keep existing unresolved ratings and manufacturer evidence visible. For implementation on a specific project, reconcile actual PDU AC circuits and feeds, QDCD input ranges/capacity and channel-zone mapping, run the v0.10 checker, topology companion validator, packing service and dependent exports, and seek owner acceptance. No inferred replacements.
