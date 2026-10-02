---
title: "Repository Boundary"
page_type: governance
page_status: draft
confidence_level: medium
domain_primary: low-voltage-lighting
ai_role: authoring_rules
invocation_triggers:
  systems_present: [low_voltage_lighting]
decision_axes: [knowledge_ownership, project_data_storage]
related_pages:
  - "../../CLAUDE.md"
  - "page-type-registry.md"
---

# Repository Boundary

## Authority and ownership

| Repository or storage | Owns |
|---|---|
| `knowledgebase_wikijs` | Shared taxonomy, templates, reasoning vocabulary, and physical product facts |
| `lv-lighting-design` | Lighting-specific method, canonical project contract, channel/grouping doctrine, spatial conventions, validation, generators |
| Approved project storage | Real client PDFs, source schedules, fixture takeoffs, model instances, decisions, markups, and generated deliverables |

The hierarchy is inherited from the [Framework Extension Doctrine](https://github.com/kissolutions/knowledgebase_wikijs/blob/main/governance-and-doctrine/framework-extension-doctrine.md). Folder names represent knowledge roles, not process steps.

## Design information boundaries

Source facts record what is shown. `design` records selections, scope, channel assignments, node choices, assumptions, and decisions. CSVs and future PDF overlays are derived views. Change the authoritative model and regenerate views.

Product facts stay upstream. This repository records the engineering use of a verified limit, along with the project evidence reference, rather than creating competing manufacturer specifications.

## Publication checks

Before committing, inspect all added/changed paths and contents. Synthetic examples must say they are synthetic. Real model JSON and CSV files are excluded by policy even if their extension is not globally ignored. Add approved anonymized precedents only after checking that both content and metadata are safe for this public repository.

## Basis and limits

Initial architectural source: user-supplied *Low Voltage Lighting Design Knowledge Model Handoff*, October 2026, especially sections 1-7. The uploaded PDF stays outside the repository. Engineering conventions beyond the handoff are draft implementation choices, including JSON collections, page coordinates, and node capacity gates.
