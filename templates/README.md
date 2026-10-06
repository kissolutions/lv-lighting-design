# Templates

New physical-first work uses [lighting-project-v0.5.template.json](lighting-project-v0.5.template.json) under [v0.5 electrical interfaces](../docs/ontology/canonical-model/electrical-interfaces-v0.5.md), retaining v0.4 ownership. Capture source voltage beside source load; populate selected electrical inputs/outputs from supported product evidence before grouping. Populate Spaces and root physical lights first; create no default zones. The v0.4 and historical seeds below retain their dedicated contracts.

For legacy v0.3 [Space and device modeling](../docs/ontology/canonical-model/space-context-v0.3.md), use `lighting-project-v0.3.template.json`. It is a structurally valid incomplete seed; replace source/page placeholders and build reviewed rooms and devices in project storage. `lighting-project-v0.2.template.json` and `lighting-project.template.json` remain the v0.2 and v0.1 seeds.

The legacy v0.3 seed uses draft 0.3.1. Start with [architectural space intake](../docs/design-playbooks/architectural-space-intake.md). Space `level` is the occupied/served floor; use `description` for multi-level extent and consequential boundary notes. Unlit chases can use `inventory_only: true` and empty lighting lists. Individual lights may include `mounting` with nullable `height_above_served_floor_ft`, `height_basis`, `note`, and `source_ref_ids`. Leave unknown numeric heights null. Existing 0.3.0 models remain supported.

Copy `lighting-project.template.json` into approved project storage outside Git. Replace all source/project placeholders and actual page dimensions before use. It is a structurally valid seed with no occurrences or design; Phase 1 checks intentionally fail until takeoff and assignments are populated.

Use `first-project-checklist.md` for the first representative project. Extension page templates preserve the framework metadata and give local canonical-model, validation, and governance pages a consistent structure. Other page types use the linked shared-framework templates in the page registry.

Use [M2 — Lighting and Source Controls: Owner Review](m2-user-review-checklist.md) as the plain-language companion to the technical checklist. It identifies the review materials, fixture/count/type/room checks, source-controls observations, open-item treatment and scoped owner acceptance. Copy the completed project review outside Git.


Use `controller-power-topology-v1.template.json` for early AHJ/plenum facts and later controller/PDU/sensor/route assignments paired with the lighting project.
