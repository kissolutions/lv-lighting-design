---
title: "Component Capacity"
page_type: validation_rule
page_status: draft
confidence_level: medium
domain_primary: low-voltage-lighting
ai_role: prescriptive_gate
invocation_triggers:
  systems_present: [low_voltage_lighting]
decision_axes: [design_validation, component_capacity]
related_pages:
  - "README.md"
  - "../design-playbooks/lighting-design-playbook.md"
---

# Component Capacity

## Purpose

Gate Phase 1 design consistency for component capacity.

## Pass Condition

Each channel has an explicit power node with confirmed usable channel capacity and aggregate design budget. Both quantities accommodate assignments.

## Block Condition

Missing node, unknown capacity, too many channels, or aggregate connected watts above the selected design budget.

## Implementation and Limits

Implemented in `generators/validate_model.py` and checked with synthetic failure/boundary cases in `tests/`. Independent per-channel checks are insufficient. Component quantities count physical node records; channel count is a distinct output. Separate control-node/network capacity checks remain future work.

## Evidence and Stewardship

Basis: October 2026 handoff plus draft model-contract implementation choices. Owner: KIS Solutions. All rule pages remain draft pending a representative project review.
