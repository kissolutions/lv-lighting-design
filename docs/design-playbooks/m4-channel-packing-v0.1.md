---
title: "PROC-M4-CHANNEL-PACK v0.1 — Parallel Remote-Driver Channel Packing"
page_type: playbook
page_status: draft
domain_primary: low-voltage-lighting
ai_role: prescriptive_standard
---

# PROC-M4-CHANNEL-PACK v0.1

## Mandatory M4 ordering

Run this **after M3 leaf/endpoint zoning and before QDCD output/equipment assignment**. Source of truth remains the accepted model and reviewed electrical/product evidence. The packing output is a read-only candidate; it does **not** edit the model, change an accepted Light Point ID, change its served Space, or alter the M3 control grouping.

1. Determine the remote programmable LED driver output and **parallel electrical topology**. A two-wire daisy-chain/bus-like physical cable run is *parallel*, never a series-connected LED string. Kirchhoff: parallel branches share voltage; total output current = sum of branch currents; watts are additive. **Do not** add nominal LED voltages across branches.
2. Split by independently commanded leaf zone, electrical AC/DC type, CV/CC mode, compatible voltage and fixture/interface requirements, and recorded compatibility group. Never pack across independent zones even if a physical controller can command them together. A selected dimming-capable fixture may be in an on/off-only zone; required control behavior still governs.
3. For CC parallel LED assemblies, require **explicit manufacturer-qualified current-sharing evidence** and an owner-accepted configuration/cohort. A remote driver being programmable, an electrical parallel topology, nominal matching voltage, and KCL **do not independently establish acceptable branch current balance, startup/reliability, or driver support**. Without evidence, return `needs_review`; do not pass singletons as an optimized design. Different fixture types remain separated until compatibility is substantiated.
4. Optimize **channel count first**, toward **90 W per channel** among solutions with equal channel count. **95 W/channel is a design maximum** on the 100 W rated Class 2 output, *not* the goal or a blanket approval. 92 W is valid if compatible. Verify CC **sum of branch currents** against the evidenced programmable-driver minimum and maximum (e.g. the manufacturer's actual supported 1–4 A range, if verified), as well as the driver voltage compliance envelope. Never force a below-minimum CC setpoint into an output.
5. Expose per-zone and overall proposed channel count, watts, utilization, remaining design capacity, unassigned lights, current settings and unresolved evidence. Keep physical fixture spacing, geometry, cable routes and selected equipment placement separate. Channel-packing candidates precede M4 routing/placement, which can return constraints to this process for targeted reevaluation.
6. Do not publish as accepted/validated while an electrical compatibility blocker remains. The existing v0.9 canonical `cc-topology-review` still blocks multi-load CC outputs and still compares per-fixture current to the channel setpoint. This initial generator does **not** bypass that checker or assert that the canonical design model is valid; a separate versioned CC-parallel evidence/validation contract is required before it can build accepted multi-load CC channels. Maintain this as a visible downstream integration gap.

## Proposal Y: physical load accounting, emergency variants and proximity

**Y1 / Y2 — canonical load accounting.** Calculate fixture watts through `model_hierarchy.load_watts`: `per_fixture`, `per_foot` and `per_reference_length` use the exact schema meanings. Do not translate a valid tape basis into an invented `per_linear_foot` value. Evaluate every Light Object's known wattage **before** checking zone assignment or electrical compatibility: the `total_input_watts` field is the complete modeled load if all loads are known, while `known_model_watts`, `missing_model_load_light_ids`, `packed_watts`, `excluded_known_watts` and `load_balance_verified` explicitly disclose unresolved/blocked items. Never call a partial packed sum the project load.

**Y3 — base and emergency variants.** The owner may approve a base fixture and its emergency-tagged schedule variant in the **same electrical compatibility cohort** if their actual LED power interfaces are compatible and the accepted sequence does not require separately commanded outputs. Identical scheduled nominal voltage is an owner grouping basis, **not by itself proof** of equal LED forward-voltage behavior, safe constant-current sharing, battery transfer compatibility, emergency egress response, or manufacturer approval. A self-contained battery/emergency variant may participate in the normal-power group only when its normal/emergency feed, test/monitoring and failover arrangements remain compliant with the selected design and hardware. Where that is unclear, retain one separately identified electrical/emergency review issue and do not silently share the output or alter the emergency control sequence. Manufacturer approval is an independent qualification gate.

**Y5 — geometry is the *last* packing tie-break.** After channel count and watt-target deviation, prefer lower total **minimum spanning-tree (MST) length in plan points** among each channel's Light Point anchors; this is orientation-independent and not a substitute for M5 routed length. Only use coordinates when all candidates in a group have known anchors on the same drawing page; otherwise fall back to stable ID ordering. Bounded exact search on smaller cohorts and deterministic spatial pair-swaps on feasible larger candidates improve compactness, but no claim of globally shortest route or distance is made. Re-run on real approved drawing geometry and preserve owner-returned chain orders.

**Y4 — not resolved by the above.** Every multi-fixture Class 2 output is wired electrically **parallel**, irrespective of physical daisy-chain routing. The canonical CC checker still needs a versioned product/compatibility qualification contract and additive-branch-current validation. Owner topology approval removes any need for a *series-versus-parallel question*; it does not by itself verify manufacturer-supported stable current sharing or emergency behavior. Do not relabel unknown manufacturer evidence as confirmed.

## Execution

`python -m generators.channel_pack M4_MODEL.json channel_packing_policy.json new_channel_proposal.json`

The nonoverwriting output carries evidence, candidate IDs, zone summaries and blockers; the command exits nonzero when `needs_review`. Policy includes:

```json
{
  "topology": "parallel",
  "target_watts": 90,
  "design_max_watts": 95,
  "rated_watts": 100,
  "output_capability": {
    "cc_min_current_a": 1,
    "cc_max_current_a": 4,
    "cc_min_voltage_v": 12,
    "cc_max_voltage_v": 55,
    "manufacturer_evidence_ref_ids": ["ACTUAL-VERIFIED-DATASHEET-REF"]
  },
  "approved_parallel_cc_cohorts": [
    {
      "id": "ACTUAL-VERIFIED-COHORT",
      "approved": true,
      "evidence_ref_ids": ["MANUFACTURER-PARALLEL-CC-APPLICATION-APPROVAL"],
      "light_ids": ["EXAMPLE-LIGHT-1", "EXAMPLE-LIGHT-2"]
    }
  ]
}
```

The numeric capability values above are **examples only** and must be verified for the *selected actual device*. A cohort is a reviewed permitted *set*; the packer may split that cohort into multiple rated outputs. CC light branch current comes from the accepted model; do not derive an unknown current automatically from nominal watts. The `compatibility_group` must reflect verified electrical compatibility; no automatic approval of unequal nominal loads is implied. If CC sharing is unsupported, use an alternative manufacturer-approved output topology or redesign with documented authority—not arbitrary override of the requirement.

### Beta Timmons replay

Preserve the 215 Light Point identities, accepted 74 M3 endpoints and original M4-R3 derivation. Rerun this process at the channel grouping step with a policy tied to independently verified QDCD hardware evidence and reviewed CC parallel-support cohorts. Compare resulting channel count and utilization with 215 single-light channels. Do not invent/approve parallel CC load behavior, silently move zones, or release 215 channels as optimized merely because each is below 95 W. Do not assign QDCD boxes until compatibility, channel allocation and downstream validation are reconciled.
