# Y4 native QDCD parallel constant-current validation

Status: development branch `y4/qualified-parallel-cc-validation`. This implementation is an independent, read-only engineering validator, **not authorization to redesign an accepted M4 project**.

## Manufacturer support vs fixture-specific proof

SmartDC QDCD Rev A2 supports **parallel** static-CCT constant-current luminaires under the published restrictions: same rated mA per luminaire; at most 4 A and 100 W on an output; at most 400 W on one QDCD. KIS design is stricter at 95 W/output. General support is not evidence that every Timmons fixture combination is manufacturer-qualified, that calculated W/V is a verified rated branch current, or that emergency variants share safely.

The native Y4 checker `generators.qdcd_y4.validate_y4` checks actual v0.10 QDCD-owned channels, including aggregate branch current versus programmed output, lower/upper programming limits, verified current steps (when supplied), voltage operating ranges/common overlap, 95/100 W output limits, 400 W QDCD limit, unequal ratings, and independent fixture/combination/emergency evidence. Neither it nor `check_v10` changes the model.

`generators.model_equipment_v10.check_v10` replaces the legacy `cc-topology-review` and `current-compatibility` findings **only for QDCD CC entities** with the native Y4 findings. It preserves unrelated legacy engineering findings. Y4 findings defer at intake and become design findings at design validation. The standalone Y4 tool accepts an explicit optional qualification companion.

## Evidence contract

`schemas/qdcd-parallel-qualification-v0.1.schema.json` is a separate, versioned companion; no old M4 project data is migrated or silently amended. It records:

- `fixture_evidence`: fixture type, manufacturer-verified **selected LED-interface** branch mA vs calculated/unverified, and source IDs.
- `combination_qualifications`: actual fixture type membership, manufacturer fixture-combination approval vs general-topology-only evidence, owner decision ID, project engineering review and emergency qualification.
- `driver_programming`: manufacturer-verified current step, grid origin and source IDs. The datasheet's *approximately* 100 mA increment is not sufficient to assign an exact step without manufacturer confirmation.

A valid mA sum, equal numeric ratings, or owner acceptance of the markup never upgrades an unqualified combination to manufacturer-verified status. Missing qualification is reported grouped by fixture-type combination; actual electrical violations remain channel-specific. An engineering-approved exception must never be mislabeled manufacturer-verified.

### Commands

```bash
python -m generators.qdcd_y4 ACCEPTED_V010_M4.json --qualification Y4_EVIDENCE.json --output NEW_FINDINGS.json
python -m generators.model_intake ACCEPTED_V010_M4.json --phase design
python -m unittest tests.test_qdcd_y4 -v
```

The standalone output command rejects an existing output path. The built-in `check_v10` invokes the conservative no-companion default; **a separate evidence companion does not automatically grant canonical design release**. Until a versioned project-attached qualification record is adopted by the canonical runner, a passing standalone evidence assessment and the conservative canonical finding set must be reconciled at owner review.

## Timmons read-only acceptance gate

At M4-R14, expect 215 Light Points, 74 endpoint zones, 104 microchannels, 29 QDCDs, 6 PDUs and 91 DC feeds. Capture old **79 `cc-topology-review` + 190 `current-compatibility` = 269** findings and compare to new counts, itemized channel conflicts and evidence questions. Examine `CH-L069`, `CH-L119` and `CH-L144` for branch sums below the published QDCD 1 A minimum. Determine which fixture ratings derive from original manufacturer documentation and which were estimated from watts/nominal voltage. Do **not** change M4-R14 groups, chain geometry, QDCD assignment, PDFs or owner's markup history. Obtain the accepted canonical project model and actual manufacturer fixture rating records before claiming this acceptance test complete.

## Limits before design release

Real fixture-specific source documents, exact current programming increments, branch current-sharing behavior for unlike module designs, branch failure/disconnection behavior, emergency transfer and auxiliary circuitry remain explicit manufacturer/project engineering review questions. A generic wiring diagram does not resolve them.
