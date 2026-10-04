# Synthetic Physical-First Intake

These contain no client data. The current [v0.4 contract](../../ontology/canonical-model/physical-intake-v0.4.md) keeps physical light identity separate from later zones.

- `lighting-model.json`: reviewed synthetic physical intake with three lights, two served Spaces, zero zones and unknown load/code/mounting inputs. Intake checks pass; design checks flag missing zoning. No placeholder zone is needed.
- `design-model.json`: the existing synthetic v0.3 design migrated with real zone memberships and unchanged physical IDs. Full design checks pass.
- `emergency-model.json`: the existing synthetic emergency example migrated; inherited backup/override checks still apply.

```bash
python -m generators.model_intake docs/reference-implementations/synthetic-intake/lighting-model.json --phase intake
python -m generators.model_intake docs/reference-implementations/synthetic-intake/design-model.json --phase design
python -m generators.model_intake docs/reference-implementations/synthetic-intake/emergency-model.json --phase design
python -m generators.export_intake docs/reference-implementations/synthetic-intake/lighting-model.json --output-dir outputs/synthetic-intake-review
```

A check pass is entered-data consistency, not proof of source completeness, energy-code compliance, human PDF editing or approval for construction.
