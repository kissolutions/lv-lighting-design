---
title: "Fixture Instance"
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

# Fixture Instance

This page records the v0.1 baseline. For current ownership and relationships, read [Device Hierarchy v0.2](device-hierarchy-v0.2.md). The v0.1 tools retain their original contract; new hierarchy data uses the dedicated v0.2 schema/checker.

## Purpose and Scope

One physical fixture occurrence observed on a plan.

## Fields and Meaning

Location: `facts.fixture_instances[]`

`id`, `fixture_type_id`, `space_id`, nullable `source_control_zone_id`, `drawing_page_id`, nullable `drawing_anchor`, `source_ref_ids`.

## Relationships

Has one explicit design scope disposition and, if included, exactly one channel assignment. Uses LV load through its type selection.

## Constraints and Validation

Retain excluded fixtures for reconciliation. IDs identify occurrences, not schedule types. Null anchor is acceptable for Phase 1; source locator/evidence is still required.

## Sources and Stewardship

Derived from the October 2026 LV lighting handoff; field shape and validation details are draft implementation decisions. Owner: KIS Solutions. Validate against one real project before treating this contract as stable.
