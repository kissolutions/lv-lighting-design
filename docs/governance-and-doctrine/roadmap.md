---
title: "LV Workflow Development Roadmap"
page_type: governance
page_status: draft
confidence_level: medium
domain_primary: low-voltage-lighting
ai_role: authoring_rules
invocation_triggers:
  systems_present: [low_voltage_lighting]
decision_axes: [markup_readiness, source_intent, development_priority]
related_pages:
  - "../design-playbooks/lv-project-workflow-and-readiness.md"
  - "../design-playbooks/lighting-design-playbook.md"
---

# LV Workflow Development Roadmap

## Current Foundation

Use the [full workflow/readiness map](../design-playbooks/lv-project-workflow-and-readiness.md) as the current audit, with the [project checklist](../../templates/first-project-checklist.md) for execution. WikiJS owns the general electrical lighting knowledge; LV work extracts MEP intent, checks it through WikiJS, and translates it into implementation. Authorized and approved departures are tracked separately from source intent.

Available: architectural intake/reconciliation directives; current v0.3.1 Space/device schema, seed and synthetic examples; stable fixture/source IDs; area/classification/evidence records; nested branch/unit/channel ownership; zones/controllers and declared emergency/backup relationships; reference, membership, load and capacity checks with derived JSON. Legacy v0.1 has five CSV outputs but cannot export v0.3 data.

These support supervised intake, manual source/code review and LV grouping. They do not demonstrate an editable PDF output, complete code evaluation, automatic extraction/grouping or an end-to-end installer package.

## Next: First Review Markup

Prove one representative room or sheet using registered source revisions, stable IDs, traced/flagged boundaries, fixture anchors and documented MEP control groups. Include LV channel graphics only where selected load, compatibility and functional intent are supported. Label unresolved scope as provisional.

Prove displayed-page crop/rotation placement, annotation editability, save/readback and identity preservation. Use accepted scale/geometry before claiming measured area. Test native Bluebeam Area recognition/editing/recalculation separately from standard editable polygons. Do not wait for a whole-building optimizer or a complete device ontology before this small experiment.

## Small Contract and Output Extensions

1. Implement agreed zone verification and implementation-review statuses, with supporting assessment evidence and per-function findings.
2. Separate original MEP scheme, applied LV implementation and proposed/approved departures; define authorization and approval records.
3. Separate intake milestone readiness from later room/code/electrical requirements in the checker.
4. Add current-version schedule/review exports and a complete source-occurrence disposition register. Preserve occurrence identity, source facts and shared-zone relationships.

Schema/check changes require versioning, synchronized examples/docs, and meaningful tests. Merely documenting these features does not implement them.

## Refine Grouping and Equipment From the Proof

Verify actual product loads, output compatibility, unit budgets and independent controller behavior. Confirm emergency signaling and backup paths in the project. Review sensor/device configuration and coverage through WikiJS. Record real routing/grouping constraints before implementing optimization; source/control boundaries survive channel sharing.

## Later Delivery Stages

Develop route endpoints/topology, equipment locations, calibrated cable lengths and allowances; detailed connection/configuration output; selected hardware BOM; coordinated release checks; field-change/diff workflows; commissioning tests and as-built reconciliation. The v0.1 route-point object is not a current v0.3 route engine or an installed-length result.

Keep real project PDFs, schedules, takeoffs, model instances, markups, decisions and results outside Git. Turn accepted findings into reusable instructions/synthetic tests without copying client identifiers.

Owner: KIS Solutions. October 2026; draft priorities based on owner workflow and local capability audit.
