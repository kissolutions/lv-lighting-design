---
title: "Synthetic Four-Fixture Room"
page_type: reference
page_status: draft
confidence_level: medium
domain_primary: low-voltage-lighting
ai_role: supporting_detail
invocation_triggers:
  systems_present: [low_voltage_lighting]
decision_axes: [minimum_model, tool_usage]
related_pages:
  - "../../design-playbooks/lighting-design-playbook.md"
---

# Synthetic Four-Fixture Room

## 0. Parent Page and Purpose

Deepens the [playbook](../../design-playbooks/lighting-design-playbook.md). Demonstrates the minimum manually populated model and review tools without client data.

## 1. Summary

Room 204 contains A1-A4, source Type L3, each selected at 20 W LV input. One confirmed zone Z-204 and one synthetic compatibility group permit channel LPC-3:CH-07 at 80 W. One modeled synthetic power/control node has one usable channel and a 90 W aggregate design budget.

## 2. Detail

[lighting-model.json](lighting-model.json) includes sources, facts, selections, scope, assignments, node capacity, and documented decisions. Synthetic evidence is asserted solely for demonstrating software behavior. It is not a product specification.

Run validation and export using the commands in the repository README. Outputs: `lv_fixture_schedule.csv`, `fixture_channel_assignments.csv`, `channel_schedule.csv`, `component_quantities.csv`, `open_items.csv`, and `validation_report.json`.

## 3. Edge Cases

Tests alter this seed to cover exact/over-limit loads, missing and duplicate assignments, source zone changes, incompatible loads, unknown selections, explicit exclusions, bad references, open items, and node capacities.

## 4. Applicability Limits

No real PDF, product, project, or installation is represented. No cable estimate or PDF markup is generated. Use this as a structural example, never as a universal engineering standard.

## 5. Sources and Validation

Architectural source: October 2026 LV lighting handoff's A1-A4 example. Verified by automated synthetic tests; a real-project source review is still required.

## 6. Status and Stewardship

Draft; owner KIS Solutions; October 2026.
