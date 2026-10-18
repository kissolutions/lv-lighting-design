---
title: "Fixture Dimming Interface and Schedule v0.1"
page_type: canonical_model
page_status: draft
domain_primary: low-voltage-lighting
ai_role: model_contract
---

# Fixture Dimming Interface and Schedule v0.1

**Authority:** [KIS Lighting Dimming Vocabulary](https://github.com/kissolutions/knowledgebase_wikijs/blob/main/ontology/lighting-dimming-vocabulary-v0.1.md). This domain companion applies the shared vocabulary to actual fixture schedule records; unlike a sequence's `dimming_scheme`, fixture `dimming_interfaces[]` identifies the electrical/physical control method accepted by its driver or luminaire.

## Source vs selected record

The [JSON Schema](../../../schemas/fixture-dimming-interface-v0.1.schema.json) defines a fixture record identified by `fixture_type_id` and `interface_basis` (`source` or `selected`). Preserve the original MEP source lighting schedule independently of the LV fixture/driver selected during design. The same source fixture type may have one source record and one selected record; do not mix them.

- `dimming_interfaces[]`: one or more manufacturer-documented choices from `triac_forward_phase`, `elv_reverse_phase`, `phase_cut_universal`, `zero_to_ten_v`, `one_to_ten_v`, `dali`, `dmx512`, `pwm`, `ccr`, `proprietary_digital`, `integrated_wireless`, `none`, `other`, or `unknown`.
- `supported_dimming_schemes[]`: `continuous`, `stepped`, `none` or `unknown`. A continuous-capable source does not require the selected zone to dim.
- `minimum_dim_percent`: manufacturer-supported minimum controlled light/output level, or null when unknown/none; use `dim_to_off` as a separate boolean/null fact.
- `signal_mode`: analog control sink/source capability where known, otherwise `not_applicable` or `unknown`.
- `driver_location`: integral, remote, driverless or unknown; preserve separate existing driver architecture and CV/CC electrical inputs.
- `source_ref_ids[]`, `notes`: exact datasheet/schedule evidence, optional dimming driver variants, applicability, fixture/driver product limitations.

`none` and `unknown` are mutually exclusive with documented positive choices. Schema rejects unrecognized interface names; validator rejects contradictory none/schemes, duplicate records, missing source references and conflicts with existing `source_dimming_capability` when established. No fake default interfaces.

## Source schedule export

```bash
python -m generators.export_intake lighting-project.json \
  --output-dir NEW_REVIEW_DIR --allow-provisional \
  --dimming-register fixture-dimming.json

# Standalone source and selected interface table + validation:
python -m generators.dimming_interfaces lighting-project.json \
  fixture-dimming.json NEW_OUTPUT_DIR --require-complete
```

The existing `fixture_type_schedule.csv` now has source capability, interface, supported scheme, minimum dimming %, dim-to-off, signal sink/source, driver location and source notes columns. If the companion isn't provided, leave new fields unasserted/blank. Standalone output is `fixture_dimming_schedule.csv` plus validation report; `--require-complete` demands a source interface record for every fixture type, but `unknown` remains an honest valid observation.

## Controller/dimmer compatibility handoff

M3 defines **required behavior** `dimming_scheme`, not electrical signaling. M4 verifies that each selected fixture/driver truly supports the needed behavior and that the selected controller/dimmer output supports the actual electrical interface and its engineering parameters. In particular, validate phase-cut edge and load range, analog sink/source and current capacity, bus/addressing, PWM signal frequency, and low-end/minimum dimming and off behavior.

A controlled enum is not a compatibility certification. This first companion supports documented intake and validation; automated final controller-to-fixture matching and manufacturer-specific electrical limits still need a versioned M4 contract. Preserve sources/decisions rather than claiming electrical compatibility from an interface name alone.

Owner: KIS Solutions; October 2026.
