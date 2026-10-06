---
title: "Project"
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

# Project

## Purpose and Scope

Identifies a project model, its revision, and workflow state.

## Fields and Meaning

Location: `project` plus root source register

`id`, `name`, `model_revision`, `stage`, `takeoff_status`.

## Relationships

Owns the source register and all model records. `schema_version` versions the contract; model revision versions a specific design.

## Constraints and Validation

Use takeoff -> provisional -> checkpoint. Set reconciled only after independently checking the source PDF. A stage value never grants engineering approval.

## Sources and Stewardship

Derived from the October 2026 LV lighting handoff; field shape and validation details are draft implementation decisions. Owner: KIS Solutions. Validate against one real project before treating this contract as stable.


## Early authority and equipment-placement facts

Capture explicit AHJ and area-specific return-air-plenum status during basis/intake through the [topology companion](controller-power-topology-v1.md). Keep existing energy-code basis authoritative; unknown plenum status is not false.
