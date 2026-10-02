---
title: "Electrical Compatibility"
page_type: validation_rule
page_status: draft
confidence_level: medium
domain_primary: low-voltage-lighting
ai_role: prescriptive_gate
invocation_triggers:
  systems_present: [low_voltage_lighting]
decision_axes: [design_validation, electrical_compatibility]
related_pages:
  - "README.md"
  - "../design-playbooks/lighting-design-playbook.md"
---

# Electrical Compatibility

## Purpose

Gate Phase 1 design consistency for electrical compatibility.

## Pass Condition

All selected fixtures on a channel share its confirmed compatibility key, established by reviewed output/driver and control evidence.

## Block Condition

Unknown or mismatched keys, even when total wattage is below the ceiling.

## Implementation and Limits

Implemented in `generators/validate_model.py` and checked with synthetic failure/boundary cases in `tests/`. Software compares keys and evidence references. Engineering review verifies that those keys correctly describe real electrical/function compatibility.

## Evidence and Stewardship

Basis: October 2026 handoff plus draft model-contract implementation choices. Owner: KIS Solutions. All rule pages remain draft pending a representative project review.
