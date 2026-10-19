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

## Canonical fixture-current schedule attributes (optional v0.10 extension)

**Do not use the original `fixture_type.source_current_ma` as the selected remote-driver LED branch current.** That existing source attribute can describe the original MEP circuit/fixture AC input. The selected LV branch current is a distinct product interface.

| Canonical level | New selected electrical attributes | Semantics |
|---|---|---|
| `fixture_type` | `lv_cc_rated_current_ma`, `lv_cc_min_current_ma`, `lv_cc_max_current_ma`, `lv_cc_current_source_ref_ids[]` | Selected fixture-type LED-module **rated** current and optional manufacturer-permitted normal supply current range with evidence. |
| `light.design` | Existing `input_current_ma` (selected **rated branch current**), new `input_current_min_ma`, `input_current_max_ma`, `input_current_source_ref_ids[]` | Specific selected Light Point/interface values, including any reviewed per-instance substitution. |
| QDCD channel | Existing `output_current_ma` and selected capability profile | Regulated **total output** current (sum of eligible rated branch currents), not the rating of an individual fixture. |

All new fields are optional in the backward-compatible v0.10 schema; an **unknown** manufacturer min/max stays absent or null rather than taking on the QDCD's 1,000–4,000 mA output range or a dimming command window. A bare LED module need not have a published allowable mA interval. Adding an interval **does not waive exact equality of the declared rated mA** for manufacturer-approved parallel branches. The design checker detects contradictions (minimum > maximum or rated outside the manufacturer range), unknown source-reference IDs, and a selected Light Point rating inconsistent with an explicitly declared LV fixture-type rating. Missing optional data alone does not cause older accepted v0.10 files to fail.

The framework's `export_intake` now reports the selected fixture-type fields in `fixture_type_schedule.csv` and the corresponding selected-light data in `light_points.csv`. Timmons's project-local **Paired Fixture Schedule** must also be updated by the project agent; it is not maintained by this framework. **No automatic transfer of the original source schedule mA to the selected LED-interface rating, and no automated derivation of mA from W/36V**, is allowed without an evidence-backed engineering selection.

## Implemented framework qualification and remaining project evidence

- **Packer** `generators.channel_pack`: CC partitioning now includes numeric `LightObject.design.input_current_ma` (per-fixture branch mA) **in addition to zone, AC/DC, CV/CC, voltage, compatibility group and cohort**. An allowed cohort containing different mA ratings is separated into distinct channel proposals, not combined. CC proposed channels report `cc_branch_rated_current_ma` separately from summed `current_setpoint_ma`. The packer cannot independently prove that the stored mA was copied from a manufacturer-rated source rather than calculated.
- **Existing canonical electrical checker** `generators.model_m4_electrical`: emits one `cc-parallel-rated-current-mismatch` or `cc-parallel-rated-current-missing` finding per multi-fixture CC channel, **in addition to** legacy Y4 findings, without modifying accepted design records.
- **Full Y4 validation implemented for v0.10:** `generators.qdcd_y4` and the read-only `generators.model_equipment_v10` canonical integration supersede legacy `cc-topology-review` and fixture-level `current-compatibility` for QDCD CC loads. They verify summed current, 1–4 A driver output, documented setpoint grid/qualified tolerance, 12–55 V output compatibility, 95/100 W channel and 400 W unit limits, exact branch mA equality, and separate evidence for manufacturer-rated fixture current, forward voltage, combinations and emergency operation. Missing evidence remains an open qualification finding.
- **Versioned companion:** `schemas/qdcd-parallel-qualification-v0.1.schema.json` records project manufacturer/source evidence, post-freeze supplemental manufacturer documents, owner decisions, fixture qualifications and programmable current. This is a sidecar; no accepted M4 project geometry is changed or silently migrated.
- **Timmons regression (2026-10-19):** accepted M4-R13 physical model, used as M4-R14 verification baseline, remains frozen at 215 Light Points, 74 zones, 104 channels and 29 QDCDs. The final beta run replaced 269 obsolete CC findings with 129 new CC findings, preserving all 117 unrelated findings. Three singleton pendant channels (`CH-L069`, `CH-L119`, `CH-L144`) are below the published 1 A standard range on *calculated* currents and remain owner review items. All 29 fixture-type current ratings are derived, not verified manufacturer nameplate data; 0 CC channels are cleared for design release.
- **Y4 framework acceptance is distinct from fixture/design release:** the finished checker is ready for framework adoption after passing CI, but actual Timmons fixture and driver programming approvals remain outstanding.

## Acceptance and change control

Accepted Timmons M4-R14 fixtures/channels, QDCDs, PDU feeds, owner-approved chains and PDF markups **must remain unchanged** until the project agent reruns the new *read-only* checks. Produce a separate delta listing all existing multi-fixture CC channels with equal rated mA, differing rated mA or missing verified rated-mA source. Check the source of each rating rather than automatically treating `input_current_ma = fixture_watts / 36 V` as manufacturer evidence. Any proposed regrouping or equipment change requires owner review; a framework correctness rule is not unilateral authorization to alter an accepted physical design.
