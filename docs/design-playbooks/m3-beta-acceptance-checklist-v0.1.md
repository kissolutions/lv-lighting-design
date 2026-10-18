---
title: "M3 Sequence Assignment BETA Acceptance Checklist v0.1"
page_type: playbook
page_status: draft
domain_primary: low-voltage-lighting
---

# M3 Sequence Assignment BETA Acceptance Checklist v0.1

Use the [M3 lifecycle](https://github.com/kissolutions/knowledgebase_wikijs/blob/main/design-playbooks/m3-lighting-sequence-lifecycle-v0.1.md) and [M3 companion validator](../ontology/canonical-model/m3-sequence-assignments-v0.1.md). Synthetic regression success is **not** real-project acceptance.

## Input package (real project)

- Reconciled M1 Space register, exact source room names/use, levels and accepted room geometry
- Reconciled M2 Light Points and fixture/MEP control evidence, source sheets/revisions
- Source code basis with adopted jurisdiction, edition, amendments and independently reviewed energy-code classifications
- Current canonical project JSON with existing zone hierarchy (no unapproved schema additions)
- Project M3 companion JSON recording project-owned sequences, assignments, source/requirements references, daylight determinations and per-Space direction dispositions
- Reviewed owner decisions for classification, authority to fill missing source controls, PSEQ definition adoption, zone assignments, and narrative lock

## BETA steps and pass criteria

| Step | Execution | Acceptance evidence |
|---|---|---|
| 1. Source/room reconciliation | Verify Space IDs, room/use classification and M2 Light Object membership against actual source revisions | No silent inferred classifications, missing Space or duplicated light |
| 2. Code applicability | Check project-specific provisions, exceptions, area thresholds, daylight determinations and source intent | Requirements matrix has reviewed locators and explicit unknowns |
| 3. SEQ matching | Test selected standard revision or owner-authored PSEQ definition against required functions | No draft standard falsely approved; PSEQ approval evidence |
| 4. Leaf hierarchy | Verify parent/child DAG; inspect every endpoint sequence assignment and shared aggregate dependencies | No SEQ on parent, no missing or duplicate endpoint assignment |
| 5. Overlays | Review daylight areas intersecting occupancy zones and luminaire response | Independent daylight control response documented; no duplicated physical lights |
| 6. Narrative review export | Run `python -m generators.m3_sequence_review MODEL.json M3.json NEW_OUTPUT_DIR --lock-check` | Findings absent; all named sequences render once with complete room/leaf rows |
| 7. All-Space review | Compare generated daylight and direction CSVs with real Light Points/Spaces | Every Space explicitly reviewed; unlit/missing/service exceptions resolved |
| 8. Owner M3 acceptance | Review narrative sections, owner decisions, overrides and deferred parameters | Owner accepts scope and named revisions; model narrative status locked; M4/M5 handoff tracked |

The command rejects a nonempty output folder and reports findings on failed lock check. A test failure never justifies inventing missing code facts, owner decisions or fixtures to achieve a passing output. Do not move source/project evidence into the framework repository. Retain review results in the actual project workspace.

## Readiness record

- **Synthetic BETA:** `tests/test_m3_sequence_review.py` exercises valid leaf references, shared parent, HTML/CSV export, parent misuse, missing assignment, draft standards, duplicates, custom definition decision, acceptance decision, daylight unknown and revision mismatch. Execute with CI or unittest.
- **Live real-project BETA:** Not complete until a current actual project has its M3 reviewed classification/code/MEP sources, sequence register and owner decision IDs available. A lighting/boundary M1/M2 PDF on its own cannot certify this M3 lifecycle.
- **Code verification and physical acceptance:** primary adopted-code checks and downstream M4 sensor/zone layout verification remain engineering review obligations; no automatic compliance certification claimed.

Owner: KIS Solutions; 2026-10-17; candidate test procedure.
