# Phase 1 Validation

The current [v0.5 electrical-interface extension](../ontology/canonical-model/electrical-interfaces-v0.5.md) uses `generators.model_intake`. It adds source-voltage shape and selected AC/DC, CV/CC, fixed-voltage and single-input CC current/range checks. Incompatible/unknown selected interfaces defer at intake and block design; contradictory numbers block every phase. Matching watts/group labels cannot bypass these checks. Multiple CC inputs on one output remain topology-review blockers. Older contracts remain unchanged and do not perform the new interface checks.

The [v0.3 Space extension](../ontology/canonical-model/space-context-v0.3.md) uses `python -m generators.model_spaces MODEL`. It adds unique Space ownership of each light, consistent light/zone references, classification/evidence readiness, estimated-area notes, daylight assessment, and room-default versus named-zone checks. Counts derive from referenced lights. Energy-code thresholds, daylight geometry, sensor coverage, and building-code classification are engineering inputs, not automatically certified results.

Use the [milestone/readiness map](../design-playbooks/lv-project-workflow-and-readiness.md) for early intake and first-markup review. The v0.3 checker is not a separate M1/M2 evaluator: it also requires later engineering inputs. The zone verification/implementation-review statuses and a complete code-check engine remain unimplemented.

These rules and `validate_model` apply to v0.1 input. The [v0.2 draft](../ontology/canonical-model/device-hierarchy-v0.2.md) uses `python -m generators.model_hierarchy MODEL` to verify nested ownership, derived many-to-many loads, controller outputs, and declared outage signal/backup relationships. It retains the 100/90 W constraint only for the selected Class 2 baseline profile. Its checks do not certify electrical/code or emergency performance.

The schema checks data shape. The validator checks IDs/references, traceability, geometry bounds, source reconciliation, engineering assignments, loads, confirmed decisions/assumptions, blocking open items, and node capacity. It returns every issue found at the current safe validation layer; fix structure/reference failures before downstream engineering checks run.

- [Channel wattage](channel-wattage.md)
- [Assignment completeness](fixture-assignment-completeness.md)
- [Architectural space intake reconciliation](space-intake-reconciliation.md)
- [Zone boundaries](zone-boundary-preservation.md)
- [Schedule consistency](fixture-schedule-consistency.md)
- [Compatibility](electrical-compatibility.md)
- [Component capacity](component-capacity.md)
- [Checkpoint readiness](checkpoint-readiness.md)

Unknown spatial anchors are acceptable for Phase 1. Known anchors must fit their page. Cable-route references and point bounds are checked, but route design/topology/length and controls-network capacities are outside the implemented checks.

Passing results mean that the recorded model satisfies these implemented checks. Confirm source completeness, loads, product evidence, and control intent through engineering review. Run from the repository root with `python -m generators.validate_model PATH_TO_MODEL --json` for a machine-readable report.
