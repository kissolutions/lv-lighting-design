---
title: "Drawing Page"
page_type: canonical_model
page_status: draft
confidence_level: medium
domain_primary: low-voltage-lighting
ai_role: model_contract
invocation_triggers:
  systems_present: [low_voltage_lighting]
decision_axes: [model_semantics, traceability]
related_pages:
  - "README.md"
  - "../../validation/README.md"
---

# Drawing Page

## Purpose and Scope

Identifies one source page and its displayed coordinate system.

## Fields and Meaning

Location: `drawing_pages[]`

`id`, `source_document_id`, `sheet_id`, `revision`, zero-based `page_index`, `width_pt`, `height_pt`, `pdf_rotation_deg`.

## Relationships

References a registered document. Spaces, fixture instances, anchors, and source references use this ID.

A page's displayed floor/level is source context, not the occupied level of every Space it depicts. An upper-level lighting page may show lights serving a lower-floor room through an open-to-below volume. Preserve distinct references for architectural room-label/boundary evidence and fixture/control evidence. Reconcile floor-plan, architectural RCP, and electrical room-label conflicts in the discrepancy list before affected identities are finalized.

## Constraints and Validation

Measure actual page geometry; the template dimensions are placeholders. Units are points (72/in), displayed upper-left origin after crop/rotation. Future PDF transforms and drawing-scale calibration must be explicit.

## Sources and Stewardship

Derived from the October 2026 LV lighting handoff; field shape and validation details are draft implementation decisions. Owner: KIS Solutions. Validate against one real project before treating this contract as stable.
