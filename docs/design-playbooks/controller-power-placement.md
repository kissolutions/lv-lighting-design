---
title: "Controller, Power and Sensor Placement"
page_type: playbook
page_status: draft
confidence_level: medium
domain_primary: low-voltage-lighting
ai_role: prescriptive_standard
invocation_triggers:
  systems_present: [low_voltage_lighting, smartdc]
decision_axes: [power_allocation, controls, equipment_placement, owner_review]
related_pages:
  - "https://github.com/kissolutions/knowledgebase_wikijs/blob/main/design-playbooks/smartdc-allocation-index.md"
---

# Controller, Power and Sensor Placement

## 1. Purpose and Use

Run after micro LV channels have already been designated under the current v0.6 electrical contract. Read the [SmartDC/EPS device index](https://github.com/kissolutions/knowledgebase_wikijs/blob/main/design-playbooks/smartdc-allocation-index.md) and each selected device mini playbook. General hardware knowledge stays upstream; project assignments and markup stay here.

## 2. Early Project Facts

During basis/room intake record AHJ explicitly alongside energy code/edition/jurisdiction/amendments. Record return-air plenum status **by area**, with served Space IDs, source/owner evidence and status true/false/unknown. Do not infer non-plenum from a suspended ceiling. Separate equipment mounting area from served lighting areas. Unknown early facts remain open and do not force invented facts to pass intake.

## 3. Design Sequence

1. Count output-based minimum QDCDs from eligible already-designated channels. Apply product capacity constraints before claiming a feasible minimum.
2. Count unique wired/Casambi sensors, separate wall controls, minimum suitable SW4/SW8 aggregators and total SDCnet peripheral devices. Count potential CIO demand without inventing locations.
3. Locate understandable geographic clusters of existing micro channels while preserving room-zone identities.
4. Assign channels to QDCD outputs and locate QDCDs. Prefer confirmed non-return-plenum above-ceiling common spaces central to served zones; co-locate related QDCDs serving one zone. Alternative corridor-wall locations require owner review and appropriate installation conditions.
5. Obtain owner CIO locations: IDF, Electrical or Storage room are usual choices. Proposed locations may support clearly provisional options.
6. Starting at furthest field devices, develop reasonable sensor strings back toward CIOs.
7. Locate SW4/SW8 near associated QDCDs, favoring the QDCD nearest CIO in the associated group.
8. Allocate PDU outputs to QDCD inputs (default four feeds, documented 1–3 exceptions) or direct lighting. Require Smart for direct network PDU on/off control; verify ratings and demand.
9. After placement, route SDCnet and PDnet separately according to manufacturer requirements, and develop power/luminaire routes with voltage-drop checks.
10. Submit first-pass equipment and route markups for owner review; incorporate returned location changes, recompute affected allocations/distances and retain IDs/decision history.

## 4. Required Review Outputs

Minimum output/port count lower bounds; feasible minima where constraints are confirmed; proposed installed counts and reasons for increases. Sensor/port/CIO ledger; QDCD output/micro-channel map; PDU output/QDCD input map; Smart policy; load/bus-power budget; locations and routes; unresolved facts/owner questions. A spare output is permitted; do not invent a spare percentage.

Use [topology companion](../ontology/canonical-model/controller-power-topology-v1.md) and [markup legend](control-system-markup-legend.md). Preserve the existing v0.6 model and channel IDs. Location/route generation and editable PDF owner round-trip still require visual work and proof; a schema/checker pass does not render a drawing.

## 5. Conflicts and Review Gates

Hardware incompatibility returns upstream with an explanation; no silent channel regrouping. Keep source facts, owner design directives, manufacturer evidence, provisional proposals and accepted owner markups distinct. Final release needs resolved applicable ratings, sensor capacity, bus power/routing, electrical compatibility and owner location decisions.

