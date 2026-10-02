---
title: "Fixture Schedule Consistency"
page_type: validation_rule
page_status: draft
confidence_level: medium
domain_primary: low-voltage-lighting
ai_role: prescriptive_gate
invocation_triggers:
  systems_present: [low_voltage_lighting]
decision_axes: [design_validation, fixture_schedule_consistency]
related_pages:
  - "README.md"
  - "../design-playbooks/lighting-design-playbook.md"
---

# Fixture Schedule Consistency

## Purpose

Gate Phase 1 design consistency for fixture schedule consistency.

## Pass Condition

Every occurrence references an existing normalized source type, every included type has exactly one confirmed LV selection, and load and compatibility evidence are present.

## Block Condition

Missing type/selection, duplicate source marks, conflicting selections, unknown LV load, or a provisional selection.

## Implementation and Limits

Implemented in `generators/validate_model.py` and checked with synthetic failure/boundary cases in `tests/`. Keep original source wattage separate. Missing source watts do not block an independently confirmed LV selection; unknown LV watts do. The check cannot detect a visually misidentified symbol without source review.

## Evidence and Stewardship

Basis: October 2026 handoff plus draft model-contract implementation choices. Owner: KIS Solutions. All rule pages remain draft pending a representative project review.
