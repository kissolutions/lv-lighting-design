---
title: "Open Item"
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

# Open Item

## Purpose and Scope

A missing/conflicting fact or unresolved design question with stated consequences.

## Fields and Meaning

Location: `open_items[]`

`id`, `description`, `affects_ids`, `source_ref_ids`, `blocking`, `status`, nullable `resolution`/`decision_id`.

## Relationships

`affects_ids` identifies affected records or stable engineering rule IDs; source references explain the gap. Resolution can cite a decision.

## Constraints and Validation

Open blocking items fail Phase 1 checks. Closing an item does not bypass a missing load, zone, or capacity check. A resolved item requires an actual resolution. Send an RFI when an external party must supply the answer.

## Sources and Stewardship

Derived from the October 2026 LV lighting handoff; field shape and validation details are draft implementation decisions. Owner: KIS Solutions. Validate against one real project before treating this contract as stable.
