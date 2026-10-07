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
| `knowledgebase_wikijs` | General electrical engineering workflow; shared taxonomy/templates/vocabulary/product facts; room-by-room lighting energy-code analysis; sensor/switch/controller selection and configuration; decision trees and lighting application guide |
| `lv-lighting-design` | MEP/architectural extraction and reconciliation for LV projects; canonical project contract; LV implementation/grouping, spatial and markup conventions; validation and generators |
| Approved project storage | Real client PDFs, source schedules, fixture takeoffs, model instances, decisions, markups, and generated deliverables |

The hierarchy is inherited from the [Framework Extension Doctrine](https://github.com/kissolutions/knowledgebase_wikijs/blob/main/governance-and-doctrine/framework-extension-doctrine.md). Folder names represent knowledge roles, not process steps.

## Design information boundaries

Source facts record what is shown. LV implementation records selections, channel/output assignments and decisions needed to reproduce the MEP scheme. WikiJS provides the engineering check. Preserve source intent, verification findings, implementation proposals and approved departures separately. Redesign only under established authority with approval evidence; a confirmed model decision does not by itself authorize a departure. General application-guide/code drafts are maintained in WikiJS; old LV filenames are navigation-only pointers. Local directives define project execution and LV-system compatibility, implementation constraints and documented KIS preferences. They narrow available selections while preserving applicable requirements and source/approved operation. Where no compatible implementation satisfies those requirements, record the conflict for review rather than weakening a requirement or silently changing the scheme. Owner confirmation of a room classification, authorization to draft missing controls, and approval of a source-text interpretation/narrative remain separate gates; follow the linked workflow map and WikiJS review playbook.

Review tables and PDF overlays are derived views. Editable owner-returned annotations are reconciled by stable ID, with accepted changes incorporated into the authoritative model before regeneration. Owner-reported Bluebeam Polygon identity/edited-vertex round-trip has been demonstrated in the beta workflow; other annotation types/viewers and automated full plan generation retain separate verification requirements. The current schema does not yet structure all source/applied/proposed control sequences or the agreed review-status attributes. See the [workflow/readiness map](../design-playbooks/lv-project-workflow-and-readiness.md).

Product facts stay upstream. This repository records the engineering use of a verified limit, along with the project evidence reference, rather than creating competing manufacturer specifications.

## Publication checks

Before committing, inspect all added/changed paths and contents. Synthetic examples must say they are synthetic. Real model JSON and CSV files are excluded by policy even if their extension is not globally ignored. Add approved anonymized precedents only after checking that both content and metadata are safe for this public repository.

## Basis and limits

Initial architectural source: user-supplied *Low Voltage Lighting Design Knowledge Model Handoff*, October 2026, especially sections 1-7. The uploaded PDF stays outside the repository. Engineering conventions beyond the handoff are draft implementation choices, including JSON collections, page coordinates, and node capacity gates.
