# Phase 1 Validation

These rules and `validate_model` apply to v0.1 input. The [v0.2 draft](../ontology/canonical-model/device-hierarchy-v0.2.md) uses `python -m generators.model_hierarchy MODEL` to verify nested ownership, derived many-to-many loads, controller outputs, and declared outage signal/backup relationships. It retains the 100/90 W constraint only for the selected Class 2 baseline profile. Its checks do not certify electrical/code or emergency performance.

The schema checks data shape. The validator checks IDs/references, traceability, geometry bounds, source reconciliation, engineering assignments, loads, confirmed decisions/assumptions, blocking open items, and node capacity. It returns every issue found at the current safe validation layer; fix structure/reference failures before downstream engineering checks run.

- [Channel wattage](channel-wattage.md)
- [Assignment completeness](fixture-assignment-completeness.md)
- [Zone boundaries](zone-boundary-preservation.md)
- [Schedule consistency](fixture-schedule-consistency.md)
- [Compatibility](electrical-compatibility.md)
- [Component capacity](component-capacity.md)
- [Checkpoint readiness](checkpoint-readiness.md)

Unknown spatial anchors are acceptable for Phase 1. Known anchors must fit their page. Cable-route references and point bounds are checked, but route design/topology/length and controls-network capacities are outside the implemented checks.

Passing results mean that the recorded model satisfies these implemented checks. Confirm source completeness, loads, product evidence, and control intent through engineering review. Run from the repository root with `python -m generators.validate_model PATH_TO_MODEL --json` for a machine-readable report.
