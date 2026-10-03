# Schema Contract

`lighting-project-v0.3.schema.json` is the current [Space extension](../docs/ontology/canonical-model/space-context-v0.3.md), checked by `generators.model_spaces`. It adds room conditions, code classifications/basis, light/zone reference lists, and zone label/area context to the nested hierarchy.

Draft revision 0.3.1 adds optional `Space.level`, `Space.inventory_only`, and `LightObject.mounting` with height above the served floor, basis, note, and evidence. The same v0.3 schema accepts existing `schema_version: 0.3.0` models without these optional fields. The seed uses 0.3.1. Shared zone references are checked against light ownership and reviewed additional served Spaces. Inventory-only service areas require descriptions and empty lighting lists.

`lighting-project-v0.2.schema.json` remains supported by `generators.model_hierarchy`. `lighting-project.schema.json` remains the v0.1 contract consumed by the original validator/exporter; use each version's dedicated tools. Read the [v0.2 contract](../docs/ontology/canonical-model/device-hierarchy-v0.2.md) for device ownership and migration limits.

`lighting-project.schema.json` uses JSON Schema Draft 2020-12. It enforces the v0.1.0 shape, required fields, nullable unknowns, stable ID format, positive wattage, the 100 W nominal baseline, and <=90 W design ceiling.

Use `generators.validate_model` to check references and engineering semantics in addition to schema. `null` is explicit uncertainty, not zero. Derived channel loads are intentionally not persisted. All object fields are declared; add contract fields deliberately with a schema/version/documentation/test update.
