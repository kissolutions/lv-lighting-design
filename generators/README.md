# Phase 1 Generators

For v0.3 draft data, use `python -m generators.model_spaces MODEL`. It checks Space references and room/zone readiness, delegates electrical hierarchy checks to the v0.2 checker, and derives fixture quantities by type, Space loads/channels, and zone display labels/control areas. It does not determine local code adoption or certify energy-code compliance. See the [Space contract](../docs/ontology/canonical-model/space-context-v0.3.md).

The overall v0.3 result includes later code/area/mounting and electrical-assignment readiness. It is not an early room-inventory gate. Keep unknowns and all findings; do not invent design data to make intake pass. Separate milestone checking and v0.3 CSV/PDF export remain development work. See the [workflow/readiness audit](../docs/design-playbooks/lv-project-workflow-and-readiness.md).

For v0.2 draft data, use `python -m generators.model_hierarchy MODEL`. It emits issues and derived zone/channel/unit/branch/controller views. The tools described below remain dedicated to v0.1. The v0.2 CSV/markup pipeline and source-occurrence exclusion register are not yet migrated.

`validate_model.py` reads the JSON schema and checks model/evidence relationships and documented design invariants. Use it as `python -m generators.validate_model MODEL [--json]` from the repository root.

`export_review.py` writes five CSVs plus a JSON validation report. It derives values from the model and never writes design state back. A nonempty output directory is rejected to avoid replacing a previous checkpoint. CSVs include model revision and review status; source labels that resemble spreadsheet formulas are escaped.

Default export requires all implemented checks to pass. `--allow-provisional` permits marked draft reviews with engineering issues, reports those issues, and exits `1`. Invalid schema, IDs/references, evidence/page-document consistency, or known geometry prevent all export.

Outputs are schedule/quantity review views, not a construction release or fully specified procurement BOM. Unknown values remain blank with issues disclosed. Counts represent explicit modeled physical nodes; channel count is separate. No extraction, optimized grouping, PDF overlay, or cable-length tool is implemented.
