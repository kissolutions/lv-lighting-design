---
title: "M3 Sequence Assignments Companion v0.1"
page_type: canonical_model
page_status: draft
domain_primary: low-voltage-lighting
ai_role: model_contract
---

# M3 Sequence Assignment Companion v0.1

**Parent authority:** [KIS shared sequence assignment contract](https://github.com/kissolutions/knowledgebase_wikijs/blob/main/ontology/lighting-sequence-assignment-contract-v0.1.md) and [M3 lifecycle](https://github.com/kissolutions/knowledgebase_wikijs/blob/main/design-playbooks/m3-lighting-sequence-lifecycle-v0.1.md). **Library:** [SEQ Registry](https://github.com/kissolutions/knowledgebase_wikijs/blob/main/design-playbooks/lighting-control-standard-sequences.md).

## Implementation

The companion [JSON Schema](../../../schemas/m3-sequence-assignments-v0.1.schema.json) and [Python checker and review exporter](../../../generators/m3_sequence_review.py) are deliberately **outside** the existing lighting-project-v0.7/v0.8/v0.9 schemas. They reference the current model using `project_id`, `model_revision` and existing persistent `endpoint_zone_id` values. Do **not** add unregistered properties to old schemas or migrate real projects until a versioned canonical schema migration is approved.

Companion top-level arrays:
- `project_sequences[]`: self-contained project-scoped `PSEQ-###` definitions and full narrative/function descriptions; approved local records require owner evidence in the project
- `assignments[]`: one per endpoint leaf, sequence ID/revision, status, owner decision, requirement and source-intent references, parameters, overrides
- `daylight_determinations[]`: one per reviewed Space, yes/no/unresolved and evidence
- `space_direction_reviews[]`: per-Space lit/unlit/served or unresolved disposition, associated leaf zones, physically inventoried Light Object IDs and evidence
- `deferred_items[]`: explicitly recorded M4/M5 handoff with scope

Approved **standard** sequences are not copied into project-authored definitions. Supply a separately vetted `--standard-catalog` JSON array of full `SEQ-###` definition records (`id`, `revision`, `status: approved`, `title`, `narrative`, `functions`). **The seven standard SEQ slots are all still reserved/draft; do not mark them approved merely to silence the checker.** Until standards are approved, use reviewed project `PSEQ-` definitions.

Parent zones carry no sequence reference and cannot appear in `assignments[]`. A leaf has at most one current assignment; on locked review all leaves must have one accepted assignment. Existing v0.7 parent aggregation and leaf member ownership are unchanged; daylight boundaries may cut across leaves and are recorded as evidence/constraints, not a conflicting second sequence. Owner-approved project sequences can still require further code verification.

## Validator and output

```bash
python -m generators.m3_sequence_review project-model.json m3-sequences.json output/m3 --lock-check
# only after actual standard approval:
python -m generators.m3_sequence_review project-model.json m3-sequences.json output/m3 --standard-catalog approved-sequences.json
python -m unittest tests.test_m3_sequence_review -v
```

Choose a new empty output folder on each revision. Output consists of:
- `m3_sequence_narratives.html`: one full narrative **per referenced sequence ID/revision**, then all assigned endpoint/room rows and per-function data
- `m3_endpoint_assignments.csv`: sequence, room/leaf, parameters, manual, occupancy, Light Reduction, daylight, scheduling, emergency, statuses and decisions
- `m3_daylight_review.csv`: per-Space determination
- `m3_space_direction_review.csv`: every Space's lighting/sequence disposition
- `m3_review_report.json`: findings, model identity and disclaimer

The checker catches parent assignments, unknown/mismatched sequence references, draft standard selections, duplicate or missing leaf assignments, unconfirmed accepted decisions, missing Space/daylight review, and project/model revision mismatch. `--lock-check` also requires the base model's separate owner narrative lock. Review printouts are **HTML and CSV**, not an editable PDF overlay; no automatic source-code compliance certification or physical sensor coverage is claimed.

The adjacent [synthetic regressions](../../../tests/test_m3_sequence_review.py) exercise the contract. Passing these tests shows internally consistent registration/output; it does not verify any project code interpretation, physical zone division, MEP source intake, daylight geometry, or owner acceptance. A real M3 test requires actual vetted source drawings/room classifications and signed-off control direction.

## M3 / M4 boundary

M3 records functional leaf/parent requirements and exact accepted SEQ/PSEQ references. M4 works out physical polygons, overlap/reduction groups, independent switching/outputs, actual devices, channel assignments and layout verification. Changes discovered at M4 reopen affected M3 assumptions/sequence assignments rather than silently substituting behaviors.

Owner: KIS Solutions; 2026-10-17; companion v0.1.
