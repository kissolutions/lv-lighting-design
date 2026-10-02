---
title: "Lighting Page-Type Registry"
page_type: governance
page_status: draft
confidence_level: medium
domain_primary: low-voltage-lighting
ai_role: authoring_rules
invocation_triggers:
  systems_present: [low_voltage_lighting]
decision_axes: [page_authority, metadata]
related_pages:
  - "repository-boundary.md"
---

# Lighting Page-Type Registry

## Inherited and extension page roles

Preserve the framework meanings of `page_type`, `page_status`, `confidence_level`, `ai_role`, `invocation_triggers`, `decision_axes`, and `related_pages`. Draft pages do not become validated because software tests pass.

| Local page type | Parent framework type | Template | AI role |
|---|---|---|---|
| `governance` | Governance / template | [Governance](../../templates/governance-page.template.md) | Authoring and boundary rules |
| `canonical_model` | Ontology | [Model element](../../templates/canonical-model-page.template.md) | Model semantics, entity relationships, implementation contract |
| `validation_rule` | Playbook | [Validation rule](../../templates/validation-rule-page.template.md) | Prescriptive pass/block conditions |
| `playbook` | Playbook | [Parent playbook template](https://github.com/kissolutions/knowledgebase_wikijs/blob/main/templates/playbook-template.md) | Prescriptive workflow and branching |
| `concept` | Concept | [Parent concept template](https://github.com/kissolutions/knowledgebase_wikijs/blob/main/templates/concept-template.md) | Explanation, subordinate to doctrine |
| `product_class` | Product type / class | [Parent product class template](https://github.com/kissolutions/knowledgebase_wikijs/blob/main/templates/product-class-template.md) | Product constraint inputs |
| `reference` | Reference / deep-dive | [Parent reference template](https://github.com/kissolutions/knowledgebase_wikijs/blob/main/templates/reference-template.md) | Supporting example, never a standard |

`canonical_model` is an ontology specialization describing records, not physical fixture ratings. `validation_rule` specializes prescriptive decision gates. Generic opportunities should be proposed to the shared framework after practical evidence exists.

Each knowledge page carries metadata and related-page links. README indexes, agent instructions, code, checklists, and JSON contracts are navigation or implementation files rather than typed knowledge pages.
