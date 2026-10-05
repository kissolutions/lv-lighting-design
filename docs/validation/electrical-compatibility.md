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

For current v0.5 design, use [electrical-interface checks](../ontology/canonical-model/electrical-interfaces-v0.5.md): selected light/channel AC/DC and CV/CC agree; fixed CV voltage matches; single-input CC current and operating/compliance ranges are supported. Unknown selected electrical inputs block design and defer at intake. Multi-input CC topology remains an explicit implementation blocker. Matching watts or compatibility keys cannot bypass these checks. Legacy conditions below remain applicable to their respective contracts.

All selected fixtures on a channel share its confirmed compatibility key, established by reviewed output/driver and control evidence.

## Block Condition

Unknown or mismatched keys, even when total wattage is below the ceiling.

## Implementation and Limits

Current v0.5 checks are implemented in `generators/model_voltage.py`, integrated into `generators/model_intake.py`, and covered by `tests/test_voltage.py`. These complement inherited checks; they do not model arbitrary series/parallel wiring, rate controller switching hardware, certify products or automatically select/count channels/controllers.

Implemented in `generators/validate_model.py` and checked with synthetic failure/boundary cases in `tests/`. Software compares keys and evidence references. Engineering review verifies that those keys correctly describe real electrical/function compatibility.

## Evidence and Stewardship

Basis: October 2026 handoff plus draft model-contract implementation choices. Owner: KIS Solutions. All rule pages remain draft pending a representative project review.
