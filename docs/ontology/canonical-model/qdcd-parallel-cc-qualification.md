---
title: "SmartDC QDCD Parallel CC Luminaire Qualification"
page_type: canonical_model
page_status: evidence_verified_limits; further_project_qualification_required
domain_primary: low-voltage-lighting
ai_role: prescriptive_standard
---

# SmartDC QDCD — Parallel Constant-Current Luminaire Qualification

## Manufacturer evidence (owner-supplied, verified 2026-10-19)

**Primary source:** SmartDC / Smart DC Lighting, **QDCD 4CHDR1 WITH STATIC COLOR TEMPERATURE CONSTANT CURRENT LUMINAIRES ON CHANNEL ONE WIRED IN PARALLEL**, drawing **Rev A2**, dated **2025-06-30**, one page, source file:

`QDCD-4CHDR1-WITH-3-STATIC-CCT-CC-LUMINAIRES-ON-CH-1-PARALLEL.pdf`

The manufacturer's actual callout states:

> Luminaires connected to the same channel must have the same mA rating.

The same callout limits **total current to 4 A per channel**, **total power to 100 W per channel** and **400 W per QDCD**. The drawing explicitly illustrates three static-CCT CC luminaires connected **electrically in parallel** to one QDCD 4CHDR1 output.

**Secondary sources:** `SMARTDC-QuadDCDrive®️-Specification-Sheet (1).pdf` pp. 1 and 6, Rev 2025-06-30: programmable **1–4 A CC output**, approximately **100 mA programming increments**, **12–55 VDC output** and 4 × 100 W nominal outputs / 400 W unit. The manufacturer also publishes **series** wiring examples, but **KIS's chosen LV design method** remains electrically parallel for every multi-fixture Class 2 output. The physical cable may be daisy-chained while the luminaire connections remain parallel.

**Scope note:** The parallel drawing proves manufacturer support for the pictured **static-color-temperature, constant-current wiring arrangement under the stated constraints**. It does **not** authorize arbitrary combinations of different LED modules, establish an acceptable *mA mismatch tolerance*, establish stable sharing under unequal I–V curves or branch disconnection, or approve emergency-transfer behavior. Do not extrapolate it to tunable white, RGB multi-channel combinations, self-contained emergency drivers or unverified interface electronics without distinct evidence.

## Required engineering checks for a multi-fixture QDCD CC output

1. **CC interface and parallel connection.** Each Light Object is truly a CC LED load at the QDCD output (typically driverless). Wiring topology is electrical **parallel** even if physically illustrated as a chain line. Distinguish any independent fixture-emergency electronics.
2. **Exact rated-mA equality (hard manufacturer condition).** Each member has a verified **luminaire/LED-module rated branch current** in mA at the connected QDCD output. **All members must share the same rated mA**. Comparing rounded watts or matching nominal voltage is **not** sufficient. No invented numerical tolerance. A single fixture may have a different wattage/forward-voltage range than another, but this does not in itself prove safe coexistence.
3. **Current setpoint is summed, not per luminaire.** Compute nominal output current by `I_output = Σ I_branch`. Verify selected programmable current/increment/tolerance against actual QDCD documentation. The manufacturer's approximate 100 mA adjustment granularity cannot establish that arbitrary sums (e.g. 2,278 mA) can be programmed exactly.
4. **Independent current and power limits.** Enforce output nominal current **between 1 A and 4 A** (product range; the three known Timmons below-1-A singleton pendants remain unresolved). Total channel load ≤ **100 W** nameplate and ≤ **95 W KIS M4 design**. Verify unit total output watts ≤ **400 W**; preserve the actual selected model's configuration/rated output.
5. **Voltage compliance.** Each verified luminaire operating/forward-voltage range must fit the output's **12–55 VDC** capability and the selected working point. All parallel branches share output voltage; equal rated mA does **not** make their I–V characteristics interchangeable. Determine whether any differing module I–V curves need a separate manufacturer application sign-off.
6. **Functional and emergency compatibility.** Do not combine independently controlled endpoint zones. A scheduled base type and its emergency variant may join a channel **only** if equal rated mA, input-interface compatibility, and the emergency transfer/monitoring/fail-operational behavior have been qualified. An owner-approved base/emergency name mapping is not a waiver of these constraints.
7. **Document qualification once per appropriate grouping.** Record drawing source ID/revision, verified fixture module/electrical source for each rated mA, owner decision, and any outstanding vendor questions. Keep separate `manufacturer_evidence`, `owner_design_decision`, and `project_engineering_review` statuses. The manufacturer's general parallel example supports the **topology and hard limits**; it does not certify every specific combination or installation.

### Worked cases

| Proposed group | Result |
|---|---|
| Two **1,139 mA**, 36 V nominal, 41 W CC troffers, same endpoint zone | Meets equal-mA and 4 A / 95 W *arithmetic*: 2,278 mA and 82 W. The exact 2,278 mA programmable setting, fixture source rating and branch behavior still require confirmation. |
| One **1,000 mA** plus one **1,139 mA** CC fixture, both nominal 36 V and combined load under 95 W | **Disallowed** on one QDCD parallel output by the manufacturer's same-rated-mA condition. Create separately rated outputs; do not reclassify them as electrically compatible because voltage matches. |
| Two same-mA CC fixtures from different manufacturers | Meets only the rated-current equality gate; requires evidence of compatible forward-voltage/current-sharing behavior before release. |
| Two equal-mA CC variants, one with emergency battery/transfer function | Needs the same current qualification **and** separate emergency behavior review; do not presume battery variant parity. |
| One CC pendant requiring less than **1 A** | Outside the documented QDCD standard CC programming range absent special product confirmation or redesign. |

## Implemented in current framework; remaining Y4 scope

- **Packer** `generators.channel_pack`: CC partitioning now includes numeric `LightObject.design.input_current_ma` (per-fixture branch mA) **in addition to zone, AC/DC, CV/CC, voltage, compatibility group and cohort**. An allowed cohort containing different mA ratings is separated into distinct channel proposals, not combined. CC proposed channels report `cc_branch_rated_current_ma` separately from summed `current_setpoint_ma`. The packer cannot independently prove that the stored mA was copied from a manufacturer-rated source rather than calculated.
- **Existing canonical electrical checker** `generators.model_m4_electrical`: emits one `cc-parallel-rated-current-mismatch` or `cc-parallel-rated-current-missing` finding per multi-fixture CC channel, **in addition to** legacy Y4 findings, without modifying accepted design records.
- **Still pending full Y4:** versioned canonical parallel group evidence and source provenance; replace legacy `cc-topology-review` and per-light `current-compatibility` with additive branch current, driver-setpoint step/range checks, manufacturer qualification and meaningful one-per-cohort review findings. Do not silently clear the existing Timmons 269 findings or claim that this limited manufacturer-condition guard completes Y4.

## Acceptance and change control

Accepted Timmons M4-R14 fixtures/channels, QDCDs, PDU feeds, owner-approved chains and PDF markups **must remain unchanged** until the project agent reruns the new *read-only* checks. Produce a separate delta listing all existing multi-fixture CC channels with equal rated mA, differing rated mA or missing verified rated-mA source. Check the source of each rating rather than automatically treating `input_current_ma = fixture_watts / 36 V` as manufacturer evidence. Any proposed regrouping or equipment change requires owner review; a framework correctness rule is not unilateral authorization to alter an accepted physical design.
