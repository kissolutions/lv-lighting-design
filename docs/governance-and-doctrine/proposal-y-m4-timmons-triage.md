---
title: "Proposal Y — Timmons M4 Engineering Framework Corrections"
page_type: governance
page_status: partial
domain_primary: low-voltage-lighting
ai_role: implementation_handoff
---

# Proposal Y — Timmons M4 framework triage, 2026-10-18/19

**Project source:** Timmons M4-R4 through owner-returned M4-R14. This file records framework changes without reopening accepted physical fixture/device/output placement. Preserve original project model, drawings and owner markups.

| Proposal | Current outcome | Boundary |
|---|---|---|
| Y1 | **Implemented in shared packer.** Uses canonical `model_hierarchy.load_watts` with schema `per_fixture`, `per_foot`, `per_reference_length` and positive-length checks. | No more temporary Timmons basis renaming. |
| Y2 | **Implemented in shared packer.** Counts every known Light Object load even if unassigned, oversized or electrically blocked. Outputs full `total_input_watts` only if all loads are known, plus `known_model_watts`, `packed_watts`, `excluded_known_watts`, `missing_model_load_light_ids` and conservation status. | A partial packed sum is never called total project connected load. |
| Y3 | **Owner-oriented policy documented**, not a blanket electrical certification. Base/emergency-tag variants may share an electrical compatibility cohort when their actual interfaces and independent emergency operation are compatible, with appropriate documented reviews. | Matching catalog nominal voltage alone does not prove safe parallel CC sharing or emergency operation. |
| Y4 | **Partially implemented: manufacturer equal-mA prequalification + LV fixture-current schedule fields.** SmartDC Rev A2 expressly supports parallel static-CCT CC luminaires provided **all members have the same rated mA**, aggregate output ≤4 A and 100 W, and QDCD ≤400 W. The packer separates unequal-rated mA; the existing canonical M4 checker flags mixed/missing ratings. Fixture schedule now has optional selected LV rated/min/max CC mA and evidence refs, distinct from legacy source-current and driver-output current. | **Full Y4 still open:** additive canonical output-current/setpoint range/step checks, per-cohort evidence, actual Timmons fixture rating sources, and old 269 findings. Owner approval of same nominal voltage cannot waive the new manufacturer condition. |
| Y5 | **Implemented in packer** as a last tie-break on plan-point MST length after channel count and deviation from 90 W; bounded exact search/swap refinement and rotation-invariant tests. A `geometry_mst_span_pt` diagnostic distinguishes plan proximity from routed M5 cable length. | Geometric optimization is conditional on complete same-page anchors and is not guaranteed global optimality for large cohorts. Accepted owner chain edits are authoritative. |
| Y6 | **Playbook updated.** Editable chain Polylines and reach lines, snap/ambiguity limits, output matching and stable channel crosswalk are described in [owner chain-return playbook](../design-playbooks/m4-channel-chain-owner-return.md). | Actual Bluebeam parser/return code remains **project-side**, with its accepted return tests; the framework did not silently mutate an M4 PDF or extend the strict v0.10 schema. |
| Y7 | **Owner policy committed in knowledgebase_wikijs.** 8-output EPS PDU excluded from all KIS LV lighting projects, including QDCD/controller-only supply, because remote configuration and SNMP trap support are required. Select verified 16/32 capacities. | Suite-only separation and spare counts remain project/customer judgments unless expressly confirmed. |

## Y4 evidence gate for product-specific implementation

The existing [QDCD product knowledge page](https://github.com/kissolutions/knowledgebase_wikijs/blob/main/hardware/lighting/qdcd.md) records the 2025-06-30 manufacturer sheet's summary: 24–57 VDC input, 12–55 VDC programmable output, 1–4 A CC settings at approximately 100 mA increments with ±1% current tolerance, 100 W/channel and 400 W aggregate. The **owner-uploaded SmartDC QDCD 4CHDR1 Rev A2 parallel static-CCT CC luminaire wiring drawing** now explicitly establishes manufacturer support for parallel wiring under a hard **same luminaire rated-mA** requirement, ≤4 A and ≤100 W per channel. This does **not** automatically approve arbitrary different LED module types sharing current, output current-step mismatch, single-module loss, or base/emergency interoperability; fixture datasheets remain necessary. If an explicit owner-engineered exception is permissible, it must be labeled *owner engineering qualification*, not *manufacturer-verified*.

Remaining evidence questions:
- **Answered in part:** parallel static-CCT CC luminaires are expressly illustrated and allowed when each has the same manufacturer-rated mA. Still obtain fixture-level rated-mA evidence and investigate sharing, module pairing and failure provisions for unlike LED modules.
- What exact programmable current step applies at the chosen QDCD output, and how is the expected sum rounded? Do not treat ±1% current regulation accuracy as permission to exceed the driver's nominal voltage/watt/current envelope.
- Does the output support the three known below-1 A singleton pendants by a verified special setting or alternative driver? The 1 A minimum is a real open design gate until resolved.
- Does each emergency variant contain its own battery/driver/sensing circuit? What happens to emergency operation when it shares the controlled output with a normal variant or a branch fails?
- How should cohort evidence be versioned and tied to approved fixture interfaces across projects, with one manufacturer/owner qualification finding per actual class of uncertainty rather than one per light?

Acceptance for Y4 requires new canonical schema/companion, safe migration and side-by-side model-validation tests (especially Timmons's 79 multi-load channels, 190 fixture memberships, and 3 below-minimum-current pendants), preserving the prior M4 baseline exactly. No claim that an owner topology rule alone establishes manufacturer-supported current sharing.

### v0.10 optional electrical schedule attributes (owner requirement, 2026-10-19)

The selected LV **Fixture Type** now supports `lv_cc_rated_current_ma`, `lv_cc_min_current_ma`, `lv_cc_max_current_ma` and `lv_cc_current_source_ref_ids[]`; corresponding selected **Light Point** properties are existing `design.input_current_ma` (rated) and optional `input_current_min_ma`, `input_current_max_ma`, `input_current_source_ref_ids[]`. Existing original MEP `fixture_type.source_current_ma` is not repurposed as selected CC branch current. Selected QDCD output mA remains an aggregate current setpoint, not a fixture rating. Missing published module operating min/max values stay unknown, never filled with driver 1–4 A limits. Both `fixture_type_schedule.csv` and `light_points.csv` now show the fields; v0.10 schema additions are optional to preserve past accepted project models. Project agent must update the Timmons Paired Fixture Schedule reader/export independently, record verified LED module datasheets, and return any same-voltage-but-unequal-mA channels for owner review—never silently change accepted grouping.

## Regression and adoption

The maintained framework has regression tests for linear tape and reference-length load arithmetic, complete-load accounting under electrical blocks, MST physical grouping, rotation and fallback, and the existing v0.10 validation and topology checks. CI must be green. Re-run any newly versioned Y4 validator against the accepted Timmons model without changing physical channels. Document before/after issue sets and review any true conflicts with the owner.
