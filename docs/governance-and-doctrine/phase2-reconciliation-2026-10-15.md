---
title: "Phase 2 Proposal Reconciliation — 2026-10-15"
page_type: governance
page_status: draft
confidence_level: medium
domain_primary: low-voltage-lighting
ai_role: authoring_rules
decision_axes: [migration, review_identity, implementation_readiness]
---
# Phase 2 Proposal Reconciliation

Owner-directed integration order: reconciliation; separate A, B, C, E, G, H documentation commits; D after A; bundle-tree v0.9 as separate implementation work. Changes spanning repositories have one corresponding commit per repository. The original independent-route shape of F is superseded by the October 14 bundle model and October 15 maintainer instruction; never implement both shapes.

## Preserve current decisions

The October 3/5 lists are historical gap registers, not replacement instructions. Architectural boundaries and finish evidence, independent classifications, source schedule extraction, physical-first ownership, v0.5/v0.6 electrical attributes, M3 review sections and scope deferrals, and editable markup rules already exist wholly or partly. Do not restore default zones during intake, automatically classify unlit corridors as inventory-only, impose one-zone-per-Space ownership, or replace dashed enveloped channel boxes with stepped outlines. Source/selected electrical data remain separate; fixture capability does not change with the narrative. Unfinished room examples, CC arrangements, per-type selected schedules and other older gaps require their own current-state review.

## Reuse review vocabulary

Use manifest annotations' review_status (proposed, accepted, change_requested) and location_basis. An owner-held location uses accepted plus owner_returned; no new pinned state. Legacy project pinned rows require explicit migration with retained evidence, not unsupported new schema properties. A change request is not acceptance. Invalidation follows the existing assumption/decision records; recomputation follows the placement review loop. as_built remains an unimplemented local extension, not a permitted manifest enum.

All delivered markups remain unflattened, including final and closeout. Unknown or missing returned annotation IDs require reconciliation, never proximity matching. Proven room-Polygon readback does not prove bundle-polyline readback.

## Documentation versus implementation

A/B/C define grouping doctrine; E/G define allocation review; H defines exclusions and cost terms; D coordinates these in Phase 2. They do not claim an implemented optimiser or modify existing schema/checker behavior. The existing topology checker still requires reduced-feed records for one to three QDCD feeds until a versioned migration changes that interface.

Bundle work is a separate v0.9 contract/checker/test migration. Source records remain flat; nested JSON is a derived view. Preserve conductor and circuit identity from F while replacing its independent-route topology. Reconcile cable jackets versus feeds, source/root identity, upstream versus drop counts, unique served-set decomposition, coordinate frames/scale, and accepted-device geometry before release. Cycle detection must check actual reachability/cycles; an edge-count equality alone is insufficient. Do not silently repair cycles or deduplicate ID collisions.

## Outstanding engineering and proof

Upstream/downstream budget values, terminal and paralleling suitability, selected-device conversion/loading limits, bundle/ambient conditions, area plenum status and calibrated labour costs remain open as applicable. The suggested 6%/3% values are not adopted defaults. Reach tables require verified calculation inputs before publication as design guidance. Unknowns block dependent final conclusions, not unrelated provisional work. Project-side tooling and its reported results are not framework validation; synthetic tests and an actual editable polyline return remain required.
