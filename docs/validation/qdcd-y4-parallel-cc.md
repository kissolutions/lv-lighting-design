# Y4 native QDCD parallel constant-current validation

Status: v0.10 native Y4 electrical qualifier, regression accepted 2026-10-19. This implementation is an independent, read-only engineering validator, **not authorization to redesign an accepted M4 project**.

## Manufacturer support vs fixture-specific proof

SmartDC QDCD Rev A2 supports **parallel** static-CCT constant-current luminaires under the published restrictions: same rated mA per luminaire; at most 4 A and 100 W on an output; at most 400 W on one QDCD. KIS design is stricter at 95 W/output. General support is not evidence that every Timmons fixture combination is manufacturer-qualified, that calculated W/V is a verified rated branch current, or that emergency variants share safely.

The native Y4 checker `generators.qdcd_y4.validate_y4` checks actual v0.10 QDCD-owned channels, including aggregate branch current versus programmed output, lower/upper programming limits, verified current steps (when supplied), voltage operating ranges/common overlap, 95/100 W output limits, 400 W QDCD limit, unequal ratings, and independent fixture/combination/emergency evidence. Neither it nor `check_v10` changes the model.

`generators.model_equipment_v10.check_v10` replaces the legacy `cc-topology-review` and `current-compatibility` findings **only for QDCD CC entities** with the native Y4 findings. It preserves unrelated legacy engineering findings. Y4 findings defer at intake and become design findings at design validation. The standalone Y4 tool accepts an explicit optional qualification companion.

## Evidence contract

`schemas/qdcd-parallel-qualification-v0.1.schema.json` is a separate, versioned companion; no old M4 project data is migrated or silently amended. It records:

- `fixture_evidence`: fixture type, manufacturer-verified **selected LED-interface** branch mA vs calculated/unverified, optional manufacturer-confirmed branch operating mA band and voltage-range evidence, and source IDs.
- `combination_qualifications`: actual fixture type membership, manufacturer fixture-combination approval vs general-topology-only evidence, owner decision ID, project engineering review and emergency qualification.
- `driver_programming`: manufacturer-verified current step, grid origin, optional separately documented current-sum deviation and source IDs. A nonzero deviation can only pass with manufacturer-verified fixture ratings and allowed branch-current bands, current-sharing combination qualification where multi-fixture, and valid programmed grid. The datasheet's *approximately* 100 mA increment is not sufficient to assign an exact step without manufacturer confirmation.
- `supplemental_sources`: reviewed manufacturer documents obtained after the frozen project model was accepted, without modifying that model. General parallel examples do not count as particular combination qualification.

A valid mA sum, equal numeric ratings, or owner acceptance of the markup never upgrades an unqualified combination to manufacturer-verified status. Missing qualification is reported grouped by fixture-type combination; actual electrical violations remain channel-specific. An engineering-approved exception must never be mislabeled manufacturer-verified.

### Commands

```bash
python -m generators.qdcd_y4 ACCEPTED_V010_M4.json --qualification Y4_EVIDENCE.json --output NEW_FINDINGS.json
python -m generators.model_equipment_v10 ACCEPTED_V010_M4.json --phase design --y4-qualification Y4_EVIDENCE.json
python -m unittest tests.test_qdcd_y4 -v
```

The standalone output command rejects an existing output path. The canonical v0.10 checker accepts an explicit evidence companion using `--y4-qualification`; without it the conservative unqualified default is used. A passing result does not override unresolved project engineering review or constitute construction release.

## Timmons read-only acceptance gate

At M4-R14, expect 215 Light Points, 74 endpoint zones, 104 microchannels, 29 QDCDs, 6 PDUs and 91 DC feeds. Capture old **79 `cc-topology-review` + 190 `current-compatibility` = 269** findings and compare to new counts, itemized channel conflicts and evidence questions. Examine `CH-L069`, `CH-L119` and `CH-L144` for branch sums below the published QDCD 1 A minimum. Determine which fixture ratings derive from original manufacturer documentation and which were estimated from watts/nominal voltage. Do **not** change M4-R14 groups, chain geometry, QDCD assignment, PDFs or owner's markup history. Obtain the accepted canonical project model and actual manufacturer fixture rating records before claiming this acceptance test complete.

## Timmons Y4 beta acceptance (2026-10-19)

The accepted M4-R13 physical model used for M4-R14 testing was unchanged before and after validation. The original 79 topology and 190 per-light current false positives (269 total) were superseded by **129 Y4 CC findings** after beta corrections, while 117 unrelated findings remained identical. The corrected count includes 29 manufacturer-mA provenance gaps, 29 unverified forward-voltage cohorts, 29 unknown driver step settings, 26 fixture-combination qualifications, 13 emergency qualifications, and 3 below-1 A singleton pendant channels. The remaining potential electrical conflicts are CH-L069, CH-L119 and CH-L144; these mA values are based on W/36 V assumptions, not product datasheets.

**Framework accepted for main branch:** no automatic project design approval follows. The three pendant conditions remain unresolved owner review items, and all fixture-specific evidence questions remain open.

## Limits before design release

Real fixture-specific source documents, exact current programming increments, branch current-sharing behavior for unlike module designs, branch failure/disconnection behavior, emergency transfer and auxiliary circuitry remain explicit manufacturer/project engineering review questions. A generic wiring diagram does not resolve them.
