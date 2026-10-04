---
title: "Physical Intake and Logical Zoning v0.4"
page_type: canonical_model
page_status: draft
confidence_level: medium
domain_primary: low-voltage-lighting
ai_role: model_contract
invocation_triggers:
  systems_present: [low_voltage_lighting]
decision_axes: [physical_intake, served_space, later_zoning, review_readiness]
related_pages:
  - "space.md"
  - "light-object.md"
  - "lv-light-zone.md"
  - "space-context-v0.3.md"
  - "../../../schemas/lighting-project-v0.4.schema.json"
---

# Physical Intake and Logical Zoning v0.4

The current draft is `schema_version: 0.4.0`. Physical extraction precedes logical zoning. Do not create default or placeholder zones to satisfy an intake container requirement.

## Ownership and Relationships

- Root `light_objects[]` stores each physical fixture occurrence or linear run once, with its stable ID, source/type/page, mounting context and later LV design fields.
- `spaces[].light_object_ids[]` gives each light exactly one primary served Space. An orphan or duplicate served-Space assignment is a primary sanity-check failure after boundary derivation and fixture counting.
- `light_zones[].light_object_ids[]` groups those records later; it never owns another copy. Empty `light_zones[]` and empty Space zone lists are valid at intake, including Spaces that already contain lights.
- A light may have no zone during intake; it must have exactly one functional zone for full design checking. Existing duplicate zone membership fails at every phase.
- A Space can have no lights. Missing symbols do not prove the space is unlit or exempt from later review. Normal unlit corridors need no `inventory_only` workaround.
- A reviewed shared zone can serve several Spaces, including a stair Space without its own fixture. Do not impose "no lights means no possible served zone."
- Branch circuits still own power units, units own channels, and each modeled single-input light receives one channel during implementation.

These relationships support higher-level routines and derived views; there is no automatic creation of relational placeholders. Moving a boundary or changing a grouping preserves physical light identity and does not silently duplicate quantities.

## Zone Display Mode

`label_mode: room` describes an established whole-Space functional zone whose drawing label can be null. It replaces the legacy display term `room_default`; it does not create a zone automatically. `named` describes an explicitly labeled zone, including reviewed cross-room zones. Functional operation comes from source intent/reviewed decisions, not Space geometry alone.

## Phase Checks

Run `python -m generators.model_intake MODEL --phase inventory|intake|design`.

| Phase | Checks | Later requirements |
|---|---|---|
| `inventory` | Entered record structure, references/evidence links, existing memberships, Space inventory, recorded source reconciliation | Does not require any lighting records, zones, loads or code classifications |
| `intake` (default) | Above plus a populated physical lighting inventory; every light has one served Space | Unassigned zones are reported as deferred; no invented loads/controllers/areas/classifications |
| `design` | Complete zone assignment plus inherited Space/code/electrical/controller/emergency checks | Requires the selected design basis; does not certify compliance or authorize release |

These are data checks supporting M1/M2 and later design review. Software cannot discover omitted source rooms/fixtures or prove that an independent reviewer actually reconciled the takeoff. `takeoff_status: reconciled` records that separate review. The engine does not evaluate the whole WikiJS application guide or implement an M3 compliance gate.

Known invalid references, duplicate IDs, wrong Space membership, off-page anchors and contradictory entered relationships cannot be bypassed for provisional export. When lights remain unzoned, the full electrical projection is unavailable; source counts remain usable, but incomplete channel totals are not issued as complete engineering views.

An open item can specify `blocking_phases` using `inventory`, `intake`, `design`. If omitted, a blocking item conservatively blocks every phase. Explicitly classify missing load/control information as a later-design blocker when early source intake can proceed. Never infer the blocking phase from prose or automatically clear an unresolved item.

## Migration and Review Outputs

`migrate_v03` moves legacy nested physical records into the root registry and turns existing zones into ID lists. It preserves all existing zones, decisions, memberships and source facts. It cannot identify a fabricated placeholder by its name or decide whether to remove it. Remove a known placeholder only through an explicit reviewed project update.

The CLI `--migrate-output NEW_PATH` writes a new v0.4 copy and refuses to overwrite an existing file. Numeric values remain JSON numbers. Older v0.1/v0.2/v0.3 schemas, checkers and examples remain supported by their dedicated tools.

`python -m generators.export_intake MODEL --output-dir NEW_DIR [--allow-provisional]` exports Room Schedule, Fixture-Type Schedule, Lighting by Space, Light Points, Discrepancy List and an intake validation report. It accepts v0.4 or a read-only v0.3 projection. Blank fields mean unknown, not zero. A per-foot linear run count is not a discrete luminaire count.

Review tables are generated views. Preserve stable IDs when returning edits; reconcile them with source evidence/owner decisions before updating the model. No automatic spreadsheet writeback or boundary PDF generator is implemented. Human PDF edit/save/readback and native Bluebeam Area remain compatibility proofs under the architectural intake playbook.

## Sources and Stewardship

Owner-confirmed Beta 1 framework decisions, October 2026. Synthetic regression cases prove the supported data/check/export behavior; real source extraction and editor compatibility still require project review. The two agreed control-review summary attributes remain a documented future extension, with findings retained in project review records.
