---
title: "Zone Boundary Preservation"
page_type: validation_rule
page_status: draft
confidence_level: medium
domain_primary: low-voltage-lighting
ai_role: prescriptive_gate
invocation_triggers:
  systems_present: [low_voltage_lighting]
decision_axes: [design_validation, zone_boundary_preservation]
related_pages:
  - "README.md"
  - "../design-playbooks/lighting-design-playbook.md"
---

# Zone Boundary Preservation

This rule describes v0.1 input. The [v0.2 hierarchy](../ontology/canonical-model/device-hierarchy-v0.2.md) defines current nested ownership, class-specific capacity profiles, and independent power/control grouping; its dedicated checker reports the new rules.

## Purpose

Gate Phase 1 design consistency for zone boundary preservation.

## Pass Condition

Each channel contains fixtures from its one effective, confirmed zone in the same space. Source facts are preserved; design corrections cite an explicit decision.

## Block Condition

Unknown controls intent, mixed required zones, multiple overrides, or cross-space assignments.

## Implementation and Limits

Implemented in `generators/validate_model.py` and checked with synthetic failure/boundary cases in `tests/`. A zone may span several channels. This implementation offers no shared-zone/cross-space channel exception; extending that behavior requires a documented rule and schema/validator changes.

## Evidence and Stewardship

Basis: October 2026 handoff plus draft model-contract implementation choices. Owner: KIS Solutions. All rule pages remain draft pending a representative project review.
