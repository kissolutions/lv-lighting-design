# Synthetic v0.5 electrical-interface examples

These are synthetic framework tests; no client data or real product approval.

- `intake-model.json`: physical intake with unknown source/selected electrical values; no invented default zones.
- `design-model.json`: inherited synthetic design with source 120 V AC and selected/channel 48 V DC constant-voltage inputs. The deliberate difference illustrates separate source and selected interfaces.

Use `python -m generators.model_intake MODEL --phase intake|design`. The intake example can pass intake with deferred design findings; the fully entered design example passes implemented consistency checks. Neither is an installable product design. See [v0.5 contract](../../ontology/canonical-model/electrical-interfaces-v0.5.md).
