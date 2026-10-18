---
title: IECC Lighting Sequence Validation Execution v0.1
page_type: playbook
page_status: draft
domain_primary: low-voltage-lighting
ai_role: prescriptive_standard
---
# IECC Sequence Validation: Mandatory Build Microprocess

The [parent process](https://github.com/kissolutions/knowledgebase_wikijs/blob/main/design-playbooks/sequence-validation-process-v0.1.md) and versioned [external 2021/2024 rule catalog](https://github.com/kissolutions/knowledgebase_wikijs/blob/main/design-playbooks/rules/iecc-lighting-sequence-validation-v0.1.json) define the governing procedures and research status. **Do not duplicate the catalog as normative SEQ definitions or alter canonical project schemas to update rules.** Use the actual parent catalog from the sibling Git checkout or download a pinned version.

**Every new/rebuilt endpoint SEQ/PSEQ assignment invokes this process.** It also runs on demand after changed permitting/code basis, controls intent, room classification, daylight or accepted source data, before M3 acceptance, and before M4 implementation. The validation results are separate work products and never silently update existing owner's decisions.

## Inputs

The wrapper reads:
- Existing canonical `MODEL.json` with `project.id`, `project.model_revision`, Space IDs and parent/leaf Zone IDs.
- Existing M3 companion `M3.json` with pinned `project_sequences` or standard SEQ revisions and per-endpoint `assignments`.
- An **external parent rule catalog** for IECC 2021 or IECC 2024. A draft rule's secondary-source status blocks a qualified result.
- Separate project `validation-context.json`, with reviewed regulatory basis and per-endpoint Space facts.

Illustrative context (NOT a statement about any real project):

```json
{
  "code_basis": {
    "standard": "IECC",
    "edition": "2024",
    "compliance_path": "prescriptive",
    "jurisdiction": "AHJ to be confirmed",
    "applicability_status": "provisional",
    "adoption_evidence": null,
    "amendments_reviewed": false,
    "exceptions_reviewed": false
  },
  "endpoint_contexts": {
    "Z-201A": {
      "space_id": "SPACE-201",
      "space_type": "conference",
      "area_sq_ft": 330,
      "special_application": false,
      "daylight_control_required": null,
      "high_end_trim_exception": null
    }
  }
}
```

Input space types are the **reviewed** normalized energy-space tokens used by the rule data. Do not map an architectural room name to a token without confirmation. `daylight_control_required` is independently established after zone-area, wattage and exception screening; a window alone is insufficient. `null` is unresolved, not false.

## Per-assignment invocation

```bash
python -m generators.sequence_validation_build MODEL.json M3.json \
  ../knowledgebase_wikijs/design-playbooks/rules/iecc-lighting-sequence-validation-v0.1.json \
  validation-context.json output/code-validation-R1.json \
  --standard-sequences approved-catalog.json
```

For an on-demand comparison, pass `--prior-result output/code-validation-R1.json` and choose a **new** output `output/code-validation-R2.json`. Optional `--require-resolved` exits nonzero if any requirements/evidence remain unresolved or incompatible. Output status is `rule_checks_passed`, `needs_review`, or `conflict`; it **never says certified compliant**.

The standalone microprocess can also be called for one endpoint:

```bash
python -m generators.sequence_code_validate RULES.json \
  single-endpoint-context.json output/SEQ-code-check.json
```

That standalone JSON contains `code_basis`, `space_context` and `sequence_assignment` (`endpoint_zone_id`, `sequence_id`, `sequence_revision`, `parameters`). The build wrapper automatically copies the selected SEQ definition's established `functions.dimming_scheme`, unless an already documented assignment override controls it, and checks contradictions against an explicit parameter. It does not resolve, invent or mutate an unknown scheme.

## Reviewer decision gate

If a missing parameter can be derived exactly, `proposed_missing_parameters` records a candidate for an **owner-reviewed new configuration revision**. Numeric min/max limits yield findings and must be explicitly selected. Conflicting prior values remain visible. Missing exceptions/applicability and all 2024 secondary-only requirements cannot be qualified by software alone.

The project must not claim a validated/certified sequence based only on an old M3 export that omitted the validation dependency. Approved 2021 and 2024 source evidence, proper ordinance/amendment review, and actual M4 fixture/controller electrical compatibility are independent of this first limited process.

**Regression tests:** `tests/test_sequence_code_validate.py` and `tests/test_sequence_validation_build.py`. Source plan, switched-zone discovery and daylight polygon generation are not part of this validator.
