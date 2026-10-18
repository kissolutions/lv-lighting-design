---
title: M3-B Lighting Subzone Detection, CSV Review and Markup v0.1
page_type: playbook
page_status: draft
domain_primary: low-voltage-lighting
ai_role: prescriptive_standard
published: true
tags: [lighting, subzone, M3, CSV, PDF, daylight]
---

**Framework proposal U (2026-10-18):** The M1/M2 `source.drawing_anchor` is defined here as **top-left PDF-page coordinates in points** (PyMuPDF-style), and the derived subzone manifest explicitly declares `anchor_origin: top_left`. The PDF overlay converts Y to native bottom-left PDF user space using the **actual page height** (`pdf_y = page_height - y_top`). Only manifests explicitly marked `bottom_left` bypass the conversion. Verify original source document page dimensions/rotation/crop alignment as part of PDF reconciliation. Owner CSV `full_room_name` displays the full `name` first followed by `(room_number)`, e.g., `1100 Conference (11.002)`; grouping/sorting is by immutable `space_id` to prevent repeated room numbers from interleaving suites. No M1/M2 model-schema migration is required.

# M3-B Lighting Subzone Detection, CSV Review and Markup v0.1

**Parent rules:** [Subzone Detection and Extraction v0.1](https://github.com/kissolutions/knowledgebase_wikijs/blob/main/design-playbooks/lighting-subzone-detection-extraction-v0.1.md), [M3 Lifecycle](https://github.com/kissolutions/knowledgebase_wikijs/blob/main/design-playbooks/m3-lighting-sequence-lifecycle-v0.1.md). **Illustration:** [Reusable editable SVG](../../assets/lighting-subzones-example.svg), also available under `knowledgebase_wikijs/assets/diagrams/` for the lighting application guide.

## Inputs and readiness

Load the accepted M1 Space registry and M2 immutable Light Point IDs/anchors/source revisions. Check for the MEP electrical lighting plan (when missing, request owner upload); review original circuit/home-run paths, adjacent dimmer/switch symbols, multi-location switching, lowercase switch-to-fixture tags, keyed notes and control legends. Keep physical circuits distinct from switched zones. Do not invent flags from fixture spacing alone. Run reviewed code and daylight screening even if the source indicates no subzones. A **true no-flags/no-independent-control** room uses `single_zone_candidate` and never enters detailed per-Light Point subzone CSV. The presence of only an electrical lighting plan satisfies the availability gate; unrelated architectural sheets are requested only for a specific missing need.

Detection records `SZ-01` through `SZ-07` carry LOW/MEDIUM/HIGH/VERIFIED confidence and status. The owner-discussion CSV contains active below-HIGH or unresolved findings, appropriate for agent-facilitated Teams review. PDF symbol/circuit recognition itself is a supervised agent/manual source-evidence extraction step, **not an implemented OCR/automated plan parser**.

## Companion contract

Use [versioned JSON Schema](../../schemas/subzone-review-v0.1.schema.json) and [validator/exporter](../../generators/subzone_review.py) with arrays `spaces[]`, `detection_findings[]`, `daylight_areas[]`, `assignments[]` and `acceptance`. This companion does **not** silently insert fields in older canonical lighting-project schemas. Its `daylight_areas[]` documents independent areas and affected lights, not nested lighting-tree children. New daylight data can be supplied in a later review; recompute only affected Space memberships and endpoint sequence dependencies.

For each flagged room, produce exactly one row for each accepted Light Point. The owner-facing CSV includes immutable `space_id`, full room name, immutable `light_id`, light display label, fixture type, editable `subzone_label`, derived stable `zone_id`, basis, confidence, original source group/evidence and owner comment. Labels are **sequential lowercase a,b,c...** per room and are not copied blindly from the MEP's source switch letters. Owner should change **only** `subzone_label` and `owner_comment`. `Unzoned` is a temporary scratch value encoded as null label and zone ID in JSON, never a real zone or approved SEQ endpoint. Single-zone rooms have no new subzone annotation.

## Run a review

```bash
python -m generators.subzone_review lighting-model.json subzone-register.json outputs/m3b-r1
```

The new empty output directory contains:
- `subzone_owner_review.csv` — editable per-Light Point room-sorted owner register
- `subzone_detection.csv` — detection flags, status, confidence, source evidence
- `subzone_owner_discussion.csv` — active uncertain findings for a focused Teams call
- `subzone_label_annotations.json` — deterministic, independent label annotations and `Subzone: a` comment upsert instructions
- `subzone_report.json` — acceptance readiness, unresolved scratch count, model/revision identity

## CSV-only correction cycle

Owner edits `subzone_owner_review.csv`, changing only the selected lowercase label and comment. Re-import from the original revisioned JSON, never from a previous generated overlay:

```bash
python -m generators.subzone_review lighting-model.json subzone-register.json outputs/m3b-r2 \
    --owner-csv outputs/m3b-r1/subzone_owner_review.csv
```

This enforces unchanged immutable Light Point ID, Space, fixture mark and row cardinality, looks up stable Zone IDs, resets review acceptance, exports `updated_subzone_register.json`, `sequence_reverification_impact.json` and rebuilt derived annotations. Review, repeat, then explicitly obtain an owner acceptance decision and update the register to `accepted` at the current review revision. Daylight additions may enter at any stage and trigger this exact same cycle. No spreadsheet/PDF side-editing ambiguity.

## Accepted hierarchy rebuild

```bash
python -m generators.subzone_review lighting-model.json accepted-subzone-register.json \
    outputs/m3b-accepted --lock-check --build-accepted-model
```

Requires all affected lights assigned, source/code/daylight screening resolved, owner decision confirmed and below-HIGH findings dispositioned. Emits `proposed_accepted_zone_tree.json` and `accepted_zone_model_copy.json` without modifying the original M2/lighting model. Only flagged/reprocessed rooms receive derived parent/leaf zones; fast-path rooms retain their existing whole-room direction. Existing zone IDs outside affected Spaces are preserved. The rebuild **refuses to rewrite** existing controller/output or electrical-channel allocations and leaves zone narratives unapproved, to be verified/locked in M3-C and physically implemented in M4.

If an existing topology uses impacted zones, stop and explicitly reconcile it rather than bypass safeguards. Stable internal zone IDs survive display-label edits where possible. A reprocess must invalidate only affected sequence decisions; the impact report identifies affected Spaces for that action.

## Add labels to existing accepted Light Point PDF

```bash
python -m generators.subzone_pdf ACCEPTED_M2_LIGHTPOINTS.pdf \
    outputs/m3b-accepted/subzone_label_annotations.json pdf_page_map.json \
    outputs/m3b-accepted/accepted_m2_with_subzones.pdf
```

`pdf_page_map.json` explicitly maps stable drawing-page IDs to **zero-based page indices** (example: `{"PG1":0}`). The tool adds separate editable PDF FreeText annotations next to existing Light Point anchors, preserving original Light Point identity/position. Where the original PDF annotation's `/NM` matches the extracted `source_annotation_id`, it **upserts** `Subzone: a` into its comments without destroying unrelated comments. Missing original IDs are returned as an error/reconciliation list; do not silently report all comments updated. Always regenerate from the **original accepted PDF** on every CSV revision rather than cumulatively annotating a prior output. Do not expect the reusable SVG to replace actual plan drawings.

The code produces native PDF annotations, but Bluebeam appearance/editor and PDF save/readback must still be checked on an actual source drawing before treating a print markup as owner-accepted.

## M3-C dependency

`python -m generators.m3_sequence_review ... --lock-check --subzone-register accepted-subzone-register.json` refuses acceptance if scratch Light Points remain or the subzone register has not passed owner acceptance. One active sequence per endpoint; parent nodes have no sequence. Late daylight/source changes force affected endpoint SEQ/PSEQ reverification rather than an unchecked continuation.

**Tests:** `python -m unittest discover -s tests -v` includes `test_subzone_review.py` for fast path, uncertainty report, Unzoned gate, CSV edits, reprocessing and end-to-end pypdf annotation generation. Automated fixture/switch symbol detection and true daylight geometry are still separate development work; no automatic code compliance claim.

Owner: KIS Solutions, October 2026.
