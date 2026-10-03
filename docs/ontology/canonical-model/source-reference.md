---
title: "Source Reference"
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

# Source Reference

## Purpose and Scope

Traceable evidence linking a statement to a document, page, schedule row, note, or verified product/coordination source.

## Fields and Meaning

Location: `source_documents[]` and `source_references[]`

Document: `id`, `filename`, `revision`, nullable `storage_uri`. Reference: `id`, `source_document_id`, nullable `drawing_page_id`, `locator`, `statement`.

## Relationships

Facts and decisions cite reference IDs. External product/coordination evidence is registered as a document; its page can be null if not a drawing.

Give room identity/boundaries, fixture location/mounting, controls, and keyed/general notes their own locators rather than forcing all evidence into one ambiguous “Source sheet” value. Register a drawing note once using its sheet, note number, and faithful statement, then reference it from affected records. Reviewer descriptions and inferred use are not drawing notes. Conflicting floor/RCP/electrical labels retain both observations in references and a discrepancy/open item.

## Constraints and Validation

Use exact locators and revisions. A reference page must belong to its reference document. Credentials and private links stay in project storage; do not place real project references in synthetic examples.

## Sources and Stewardship

Derived from the October 2026 LV lighting handoff; field shape and validation details are draft implementation decisions. Owner: KIS Solutions. Validate against one real project before treating this contract as stable.
