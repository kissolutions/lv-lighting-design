# Templates

New physical-first work uses [lighting-project-v0.4.template.json](lighting-project-v0.4.template.json) under [v0.4](../docs/ontology/canonical-model/physical-intake-v0.4.md). Populate Spaces and root physical lights first; create no default zones. Historical seeds below retain their dedicated contracts.

For legacy v0.3 [Space and device modeling](../docs/ontology/canonical-model/space-context-v0.3.md), use `lighting-project-v0.3.template.json`. It is a structurally valid incomplete seed; replace source/page placeholders and build reviewed rooms and devices in project storage. `lighting-project-v0.2.template.json` and `lighting-project.template.json` remain the v0.2 and v0.1 seeds.

The legacy v0.3 seed uses draft 0.3.1. Start with [architectural space intake](../docs/design-playbooks/architectural-space-intake.md). Space `level` is the occupied/served floor; use `description` for multi-level extent and consequential boundary notes. Unlit chases can use `inventory_only: true` and empty lighting lists. Individual lights may include `mounting` with nullable `height_above_served_floor_ft`, `height_basis`, `note`, and `source_ref_ids`. Leave unknown numeric heights null. Existing 0.3.0 models remain supported.

Copy `lighting-project.template.json` into approved project storage outside Git. Replace all source/project placeholders and actual page dimensions before use. It is a structurally valid seed with no occurrences or design; Phase 1 checks intentionally fail until takeoff and assignments are populated.

Use `first-project-checklist.md` for the first representative project. Extension page templates preserve the framework metadata and give local canonical-model, validation, and governance pages a consistent structure. Other page types use the linked shared-framework templates in the page registry.
