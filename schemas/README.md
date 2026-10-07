# Schema Contract

`lighting-project-v0.4.schema.json` is current for new projects. Root `light_objects[]` separates physical intake from later `light_zones[].light_object_ids[]`. Use `generators.model_intake` with inventory/intake/design phases and `generators.export_intake` for review CSVs. Empty zones are valid at intake; served-Space membership is required for every entered light. Older version schemas/checkers remain unchanged and supported. See [v0.4](../docs/ontology/canonical-model/physical-intake-v0.4.md).

`lighting-project-v0.3.schema.json` is the preserved v0.3 [Space extension](../docs/ontology/canonical-model/space-context-v0.3.md), checked by `generators.model_spaces`. It adds room conditions, code classifications/basis, light/zone reference lists, and zone label/area context to the nested hierarchy.

Draft revision 0.3.1 adds optional `Space.level`, `Space.inventory_only`, and `LightObject.mounting` with height above the served floor, basis, note, and evidence. The same v0.3 schema accepts existing `schema_version: 0.3.0` models without these optional fields. The seed uses 0.3.1. Shared zone references are checked against light ownership and reviewed additional served Spaces. Inventory-only service areas require descriptions and empty lighting lists.

`lighting-project-v0.2.schema.json` remains supported by `generators.model_hierarchy`. `lighting-project.schema.json` remains the v0.1 contract consumed by the original validator/exporter; use each version's dedicated tools. Read the [v0.2 contract](../docs/ontology/canonical-model/device-hierarchy-v0.2.md) for device ownership and migration limits.

`lighting-project.schema.json` uses JSON Schema Draft 2020-12. It enforces the v0.1.0 shape, required fields, nullable unknowns, stable ID format, positive wattage, the 100 W nominal baseline, and <=90 W design ceiling.

Use `generators.validate_model` to check references and engineering semantics in addition to schema. `null` is explicit uncertainty, not zero. Derived channel loads are intentionally not persisted. All object fields are declared; add contract fields deliberately with a schema/version/documentation/test update.


Controller/power placement uses the independently versioned `controller-power-topology-v1.schema.json` companion paired with v0.6. It does not upgrade or replace the existing lighting project.

Versioned additions: lighting-project-v0.7.schema.json (zone hierarchy/narrative review), controller-power-topology-v1.1.schema.json (device identity), milestone-markup-v1.schema.json (deliverable/annotation review). Older schemas remain supported.

## Physical Intake Review v0.8

The v0.8 schema/template adds `Space.nested_in`, light `assembly_id`, `count_basis`, `count_decision_id`, source `source_tag`/`schedule_match_status`, and fixture `schedule_presence`. `model_intake_review.upgrade_v08` preserves existing values and leaves new facts unknown. `model_intake` checks v0.8 through prior electrical/hierarchy validators. `room_geometry_review` derives same-frame containment without changing membership; `validate_markup_pdf` checks the saved live annotations/register. Schedule exports include required M1/M2 notes and review metadata. The EPS aggregator contract is not implemented by this version.
