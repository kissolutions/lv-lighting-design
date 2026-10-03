# Schema Contract

`lighting-project-v0.2.schema.json` is the current draft for the owner-provided nested device hierarchy. It is additive and uses the dedicated `generators.model_hierarchy` checker. `lighting-project.schema.json` remains the v0.1 contract consumed by the original validator/exporter; do not pass v0.2 data into those tools. Read the [v0.2 contract](../docs/ontology/canonical-model/device-hierarchy-v0.2.md) for ownership, derived fields, and migration limits.

`lighting-project.schema.json` uses JSON Schema Draft 2020-12. It enforces the v0.1.0 shape, required fields, nullable unknowns, stable ID format, positive wattage, the 100 W nominal baseline, and <=90 W design ceiling.

Use `generators.validate_model` to check references and engineering semantics in addition to schema. `null` is explicit uncertainty, not zero. Derived channel loads are intentionally not persisted. All object fields are declared; add contract fields deliberately with a schema/version/documentation/test update.
