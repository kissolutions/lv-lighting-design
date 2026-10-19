---
title: "Proposal Z — v0.10 Adoption Corrections"
page_type: governance
page_status: implemented
domain_primary: low-voltage-lighting
ai_role: implementation_handoff
---

# Framework Change Proposal Z — v0.10 adoption corrections (2026-10-18)

**Raised from:** Timmons M4-R12, first canonical v0.10 field adoption.
**Scope:** v0.10 validator robustness, evidence-phase behavior and backward-compatible consumers. **No changes to accepted M4 engineering design, owner markups, channel packing, PDU/QDCD assignment, or project records were made in the framework repository.**

## Implemented corrections

| Item | Implementation | Verification |
|---|---|---|
| Z1 | `python -m generators.model_equipment_v10 MODEL --phase ...` reads with the shared Decimal-safe `read_model` and prints JSON reports with Decimal serialization. Explicit migration uses `model_json` so model numbers remain numbers rather than being converted to strings. | File-loaded CLI subprocess tests |
| Z2 | DC feed demand accumulation, per-feed comparisons, QDCD input sums and PDU rating comparisons normalize to exact `Decimal` arithmetic. | Non-null Decimal input from `read_model`, multi-stage CLI test, fractional overdraw detection |
| Z3 | Canonical v0.10 open-item `affects_ids` now validate against **all real record IDs**, including distribution units and DC feeds. The in-memory v0.9 projection adapts new-only targets without changing or retargeting the actual open items. If legacy validation stops early, it emits a **blocking `legacy-projection-incomplete`** finding, sets `legacy_projection_status=halted`, leaves `derived=null`, and warns that the smaller issue list is **incomplete**. | Regression with PDU/feed open-item IDs plus unrelated, intentionally failed legacy electrical check |
| Z4 | A `decision-basis` finding belonging **only to the unsaved `X10-COMPATIBILITY-ONLY` branch** is filtered. A real branch or equipment missing its engineering decision is not exempt. | Synthetic orphan-driver regression |
| Z5 | Unknown PDU AC circuit and unknown DC feed rating, plus other missing design-only inputs, are placed into `deferred_issues` during inventory/intake and become `issues` at design. **Incorrect known equipment references and known overlimits are never deferred.** | Intake-versus-design assertions |
| Z6 | DC driver input-wattage findings do not describe their power input as AC. The requirement to establish actual input power remains. | DC-specific wording test |
| Z7 | Shared `generators.model_access.iter_power_units(model)` and `iter_channels(model)` resolve nested legacy power units or v0.10 root units. Framework consumers updated: `model_bundles.build`, `validate_topology`, `milestone_markup.schedules`, `milestone_markup.validate_manifest`, and v0.10 bundle-aware `export_intake`. `channel_pack` already reads light/zone data independently and needs no branch traversal. | v0.9/v0.10 reader parity, M4 schedule/markup, bundle, topology and intake export tests |

## M4-R13 follow-up: Z8 and Z9

Timmons M4-R13 confirmed that Z1–Z7 work with actual v0.10 data: both normal model-check CLIs agree; `legacy_projection_status=complete`; the design report has 386 findings, with the prior Z4-only artefact removed; v0.9 chain-return replay and v0.10 owner-edit regressions passed. The review markup retains 871 annotation identities and accepted geometry. These are **project-agent findings**, not a claim that this maintaining repository contains or reran the full Timmons files.

| Item | Fix | Contract/regression |
|---|---|---|
| **Z8 — Intake deferred items** | Reuse one compatibility filter for both blocking `issues` and `deferred_issues`. Inapplicable AC-only `input_voltage_v` and `input_phases` findings on DC QDCDs and the synthetic `X10-COMPATIBILITY-ONLY` decision-basis artefact are removed in both paths. Valid DC input wattage findings remain, with `DC input watts` wording. | `tests/test_proposal_z.py::test_z8_deferred_findings_use_same_x4_z4_z6_filter` checks nonmutation, preserved genuine deferred input and PDU evidence, and absence of the inapplicable items. |
| **Z9 — Mixed Decimal/float topology feed comparisons** | `validate_topology` converts companion and canonical `rated_watts`/`demand_watts` to `Decimal(str(value))` before comparing. Retains the existing strict >0.000001 difference threshold; does not round off or ignore actual mismatches. | `tests/test_proposal_z.py::test_z9_milestone_markup_cli_with_topology_and_decimal_feed` uses a Decimal-loaded canonical model and JSON-float companion, verifies the standard `milestone_markup --topology --through 5` CLI writes Package 5, verifies the input is unchanged, and asserts deliberately inconsistent demands still fail. |

**M4-R13 adoption step:** Pull the latest framework SHA; retire no further project tools. Re-run both intake/design model commands and the `milestone_markup MODEL NEW_OUTPUT_DIR --topology TOPOLOGY --through 5` command. Confirm intake no longer includes the obsolete Z8 deferred items, all legitimate design findings remain present, the 871 accepted markup annotation IDs and 104 microchannels are preserved, and the Package 5 equipment schedule is produced without any re-design. The new test set cannot establish the exact post-change intake finding count for the private Timmons model, so report actual counts and rule/entity deltas; do not assert a fixed number in advance.

## Readiness gate

The repaired v0.10 checker must **never** interpret a low issue count as success if `legacy_projection_status` is `halted`; review and resolve its blocking reason. Read the entire `issues` and `deferred_issues` arrays and keep distinct the phase in which a missing requirement becomes blocking. Running a model through `python -m generators.model_equipment_v10 ...` or `python -m generators.model_intake ...` is equivalent; **no private plain-float loader is required**.

These changes do **not** waive the separate Y4 parallel-CC canonical-validation gap, missing selected electrical ratings, manufacturer evidence, actual panel circuits, pending emergency sequences, or other owner-deferred design requirements. The accepted Timmons M4-R12 invariant baseline is 215 lights, 74 endpoint zones, 104 microchannels, 29 QDCDs, six EPS PDUs and 91 canonical DC feeds. The maintaining agent has **not** rerun the proprietary project model here; these are the project's previously reported accepted quantities.

## Handoff: Timmons project agent

1. Pull the latest `kissolutions/lv-lighting-design` commit and pin its SHA. Preserve M4-R12 and its rollback model, accepted PDF markups, device/chain mapping, M3 and topology companion.
2. Run `python -m generators.model_equipment_v10 MODEL_v10.json --phase intake > intake_v10.json`, then `--phase design > design_v10.json` (a nonzero exit means unresolved blocking findings, not necessarily an execution crash). The normal `python -m generators.model_intake ... --phase ...` path should work with the same input.
3. Assert `legacy_projection_status=complete` and non-null `derived` on the known structurally sound project. Restore real PDU/feed IDs to affected open items as appropriate; do not use project-ID substitutions to hide the legacy projection problem. Confirm the previous electrical findings remain visible. Separate new `deferred_issues` from design `issues`.
4. Replace per-project `branch_circuits[].power_units[]` traversals with `from generators.model_access import iter_power_units, iter_channels`. **Project-owned** tools such as `tools/chain_return.py`, the paired fixture schedule, and other Timmons-only markup builders are outside this framework repository and must be updated/tested by the project agent. Do not claim framework Z7 makes unmodified project scripts version-aware.
5. Reconcile v0.10 companion PDU/feed/output maps, rerun M4 schedule/markup exports in a **new output directory**, compare counts and accepted IDs/routes/locations with M4-R12, and provide a findings delta grouped by root cause.
6. Do **not** regenerate accepted design geometry or change owner markups merely because the data representation changed. Raise any genuine discrepancies to the owner. Do not mark Y4/manufacturer/electrical/equipment release questions resolved by these Z fixes.

## Commands

```bash
python -m generators.model_equipment_v10 MODEL_v10.json --phase intake
python -m generators.model_equipment_v10 MODEL_v10.json --phase design
python -m generators.model_intake MODEL_v10.json --phase design
python -m generators.validate_topology TOPOLOGY_v1_1.json --model MODEL_v10.json
python -m generators.export_intake MODEL_v10.json --output-dir NEW_REVIEW_DIR --allow-provisional
python -m generators.milestone_markup MODEL_v10.json NEW_MILESTONE_DIR --topology TOPOLOGY_v1_1.json --through 5
```

**Review reminder:** `export_review` is the older v0.1-style design/facts exporter, not a v0.10 M4 exporter. Use `export_intake` and `milestone_markup` for the v0.10 canonical model. The old v0.9 schema and original project files remain supported and untouched.
