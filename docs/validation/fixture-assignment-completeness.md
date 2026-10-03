---
title: "Fixture Assignment Completeness"
page_type: validation_rule
page_status: draft
confidence_level: medium
domain_primary: low-voltage-lighting
ai_role: prescriptive_gate
invocation_triggers:
  systems_present: [low_voltage_lighting]
decision_axes: [design_validation, fixture_assignment_completeness]
related_pages:
  - "README.md"
  - "../design-playbooks/lighting-design-playbook.md"
---

# Fixture Assignment Completeness

This rule describes v0.1 input. The [v0.2 hierarchy](../ontology/canonical-model/device-hierarchy-v0.2.md) defines current nested ownership, class-specific capacity profiles, and independent power/control grouping; its dedicated checker reports the new rules.

## Purpose

Gate Phase 1 design consistency for fixture assignment completeness.

## Pass Condition

Every source occurrence has exactly one scope disposition. Every included occurrence is assigned exactly once; excluded occurrences have a reason/decision and no channel.

## Block Condition

Missing or duplicate scope rows, unassigned/double-assigned included fixtures, or assignments to excluded fixtures.

## Implementation and Limits

Implemented in `generators/validate_model.py` and checked with synthetic failure/boundary cases in `tests/`. Unique fixture IDs prevent duplicate physical records from hiding assignment errors. Human source reconciliation must also detect fixtures never entered into the model.

## Evidence and Stewardship

Basis: October 2026 handoff plus draft model-contract implementation choices. Owner: KIS Solutions. All rule pages remain draft pending a representative project review.
