# Schema Contract

`lighting-project.schema.json` uses JSON Schema Draft 2020-12. It enforces the v0.1.0 shape, required fields, nullable unknowns, stable ID format, positive wattage, the 100 W nominal baseline, and <=90 W design ceiling.

Use `generators.validate_model` to check references and engineering semantics in addition to schema. `null` is explicit uncertainty, not zero. Derived channel loads are intentionally not persisted. All object fields are declared; add contract fields deliberately with a schema/version/documentation/test update.
