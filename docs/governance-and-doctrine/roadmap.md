---
title: "Initial Sprint and Roadmap"
page_type: governance
page_status: draft
confidence_level: medium
domain_primary: low-voltage-lighting
ai_role: authoring_rules
invocation_triggers:
  systems_present: [low_voltage_lighting]
decision_axes: [sprint_scope, phase2_readiness]
related_pages:
  - "../design-playbooks/lighting-design-playbook.md"
---

# Initial Sprint and Roadmap

## Available foundation

- Repository boundary and agent guidance linked to the parent framework.
- Draft Phase 1 playbook and minimum canonical-model pages.
- JSON schema, manual-project seed, and synthetic four-fixture reference.
- Channel-load, assignment, zone, schedule, evidence, uncertainty, and node-capacity checks.
- Five CSV review views and a machine-readable validation report.

## Next: one real-project stress test

1. Add this repository alongside `knowledgebase_wikijs` in the existing VS Code workspace. Local workspace configuration remains on the engineering workstation.
2. Select one representative MEP lighting plan and store its project model outside Git.
3. Follow [first-project-checklist.md](../../templates/first-project-checklist.md), reconcile fixtures manually, and confirm LV selection/controls with evidence.
4. Group one room, check <=90 W and exact assignment, then quantify explicit power/control nodes.
5. Export review tables; compare against the PDF and a manual quantity check. Record discrepancies in the project and improve reusable rules here.

## Then: spatial proof on one sheet

Capture page size, crop/rotation transform, fixture anchors, and reliable node positions. Prove coordinate round-trip placement before drawing production markup. Establish label collisions, legend, revision identity, and readable channel graphics. The schema reserves anchors but no PDF writer is implemented yet.

## Later: routing and optimization

Add route bundles, endpoints, branch topology, scale/calibration, installation allowances, and cable lengths after fixtures and nodes are reliable. Current `cable_routes` capture only projected points and channel membership. Do not present those points as a validated installed length.

Add constrained grouping software only after one real project tests compatibility groups, emergency exclusions, zoning, and node capacities. Prefer fewer channels and compact groups after hard constraints pass. Vendor-specific BOM generation requires selected hardware facts and procurement basis.


## Device hierarchy revision v0.2

The current [hierarchy draft](../ontology/canonical-model/device-hierarchy-v0.2.md) adds source-grounded branch/unit/channel ownership, separate LV zones/controllers, linear load bases, and emergency signal/backup provisions. Its dedicated schema/checker and synthetic examples are available. Remaining migration work includes a complete source-occurrence disposition/segmentation register, v0.2 CSV outputs, source-to-design revisions, route endpoints, and detailed class/emergency performance checks. Preserve the original v0.1 examples/tools until that migration is reviewed.
