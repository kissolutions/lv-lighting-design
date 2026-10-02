---
title: "Decision and Assumption"
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

# Decision and Assumption

## Purpose and Scope

Separates chosen design actions from statements that must remain true.

## Fields and Meaning

Location: `design.decisions[]` and `design.assumptions[]`

Decision: `id`, `statement`, `rationale`, `status`, `source_ref_ids`, `assumption_ids`. Assumption: `id`, `statement`, `source_ref_ids`, `invalidated_if`, `status`.

## Relationships

Selections, scope, zone corrections, channels, and nodes reference decisions. Decisions reference any assumptions on which they depend.

## Constraints and Validation

Provisional decisions and unverified/invalidated dependent assumptions block checks. A plan/driver/product change can invalidate an assumption and dependent assignments. Confirmed is an engineering assertion with evidence, not an automated approval.

## Sources and Stewardship

Derived from the October 2026 LV lighting handoff; field shape and validation details are draft implementation decisions. Owner: KIS Solutions. Validate against one real project before treating this contract as stable.
