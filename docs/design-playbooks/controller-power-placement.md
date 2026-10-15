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

### Phase 1 — Application and Transport

Establish rooms, fixtures, functional zones, approved narrative, compatible micro channels and device-count/grouping candidates. Use room-family grouping below. These form the accepted input baseline; later incompatibility returns upstream with an explained, reviewed change, never a silent regrouping.

### Room-Family Grouping (Change A)

Group existing micro channels into QDCD candidates by room family first, then geography within the family. A controller may serve several rooms through independent outputs. Family is an equipment-service taxonomy, not an energy/building-code classification. Record each Space's family and basis in review records; no unversioned field. Fill similar rooms' boxes before mixing families, preserve electrical/product/control constraints, and flag dispersion or reach conflicts. Co-locate compatible family devices where access and installation conditions permit; owner-held devices are not free banking candidates.

### Phase 2 — Hardware and Infrastructure

Placement, pathways, routes, conductors and supports are coordinated iteratively. Field knowledge and returned changes are expected inputs.

1. Record held owner locations using existing annotation review_status: accepted and location_basis: owner_returned, with basis/evidence. Do not add a pinned state. The optimiser does not move these locations or require justification against an optimum. Source-supported fixed conditions also remain explicit constraints; do not falsely label them owner-returned.
2. Establish the proposed pathway network, access/mountable locations, risers, source/reviewer exclusions and area plenum facts. Unknown conditions remain flagged on dependent proposals; they neither justify an invented straight-line route nor block unrelated work. Above-ceiling final acceptance still requires applicable installation evidence.
3. Seed free-device locations from supported mountable candidates, then alternate routing and re-siting. Route held locations and heavy bundles first; free equipment joins mountable points on the roadway already serving its channels, within a stated project tap reach. The first pass may have no open roadway. Report off-network devices and proposed roadway extensions/spurs for deliberate review. Do not move an owner-held device to enforce an optimisation preference.
4. Use the pathway/pull/bend objective below. Retain the lowest-cost feasible configuration actually evaluated under the same inputs/objective, not merely the last pass. Detect repeated configurations, impose an explicit iteration limit, and report stable, oscillating or best-seen-at-limit as algorithm outcomes, not new review states. Re-evaluate saved candidates when inputs change.
5. Verify both drop budgets, conductor/terminal suitability and demand-based PDU feed allocation. Retain reduced_feed_decisions evidence required by topology v1/v1.1. Do not assume cable count equals feed count. Require Smart for direct network PDU on/off control and verify selected ratings/demand.
6. Coordinate sensor strings, SW4/SW8 associations and owner CIO locations using the upstream device mini playbooks. Route signal networks separately under their manufacturer rules; power bundle trees are not signal topology.
7. Submit equipment and route markups. Incorporate returned location changes, recompute affected allocations/distances and retain IDs/decision history. Use existing assumption invalidation when inputs change. Accepted geometry and associations survive a new optimisation unless explicitly reopened.

This loop defines review procedure, not a claim that a router/fixpoint solver exists in the framework. Efficient candidate scoring may use shared cost fields instead of a separate full routing solve per candidate, provided direction, weights, constraints and evaluation order are preserved.

## 4. Required Review Outputs

Minimum output/port count lower bounds; feasible minima where constraints are confirmed; proposed installed counts and reasons for increases. Sensor/port/CIO ledger; QDCD output/micro-channel map; PDU output/QDCD input map; Smart policy; load/bus-power budget; locations and routes; unresolved facts/owner questions. A spare output is permitted; do not invent a spare percentage.

Use [topology companion](../ontology/canonical-model/controller-power-topology-v1.md) and [markup legend](control-system-markup-legend.md). Preserve the existing v0.6 model and channel IDs. Location/route generation and editable PDF owner round-trip still require visual work and proof; a schema/checker pass does not render a drawing.

## 5. Conflicts and Review Gates

Hardware incompatibility returns upstream with an explanation; no silent channel regrouping. Keep source facts, owner design directives, manufacturer evidence, provisional proposals and accepted owner markups distinct. Final release needs resolved applicable ratings, sensor capacity, bus power/routing, electrical compatibility and owner location decisions.


## Earlier Room-Device Review

Immediately after narrative lock, inventory/schedule required room devices and place symbols using the device-specific provisional placement rules in the milestone packages for owner finalization. Wall switches, scene controllers, dimmers, occupancy sensors and daylight sensors start at their electrical lighting-plan or other applicable source design locations; preserve source sheet/revision/symbol references and register them into the accepted working frame. Accepted owner locations take precedence. Apply the device-specific door-swing/glazing/open-entry or sensor-center/corner/corridor/daylight-placeholder fallbacks only when no usable source location is available; record missing/conflicting evidence and the proposal basis. This stage precedes micro-channel/equipment-location review and final routing. Use [milestone packages](milestone-review-packages.md), topology v1.1 device tags/names/room links and markup identities. Hardware controller/aggregator selection and route validation still follow designated compatible channels and accepted device locations.

## EPS Fixture Power Aggregation — Owner Directive, 2026-10-06

A fixture above 95 W is a permitted design candidate via an EPS **fixture power aggregator**, distinct from SW4/SW8 sensor aggregators. Owner-described topology: **1–4 separate Class 2 inputs, one combined output up to 400 W, inside the fixture housing**. Reserve its use for **on/off-only nominal 48 VDC constant-voltage fixtures switched through the EPS outputs**; no dimming or constant-current application. QDCD similarity concerns input aggregation only, not four independently controlled outputs.

Follow the upstream [EPS allocation directive](https://github.com/kissolutions/knowledgebase_wikijs/blob/main/design-playbooks/eps-pdu-allocation.md#eps-fixture-power-aggregation--owner-directive-2026-10-06) for sizing, feed counting, common switching, evidence and installation constraints. Use the smallest supported 1–4 input count that meets full fixture demand within verified limits and project margins. Do not silently waive the current 95 W feed target, assume equal feed sharing, or claim an ordinary Class 2 channel can deliver 400 W. Every allocated input consumes a distinct EPS output and remains in the same functional on/off group.

Maintain one physical Light Object, the actual LV nameplate load, stable aggregator tag such as FA-01, Room/zone association, each supply output/input mapping, and one output-to-fixture link. Count all feeds in PDU capacity/demand and routing records. Locate the internal power unit at its served fixture with an inside-housing note. The gym/high-bay use is a candidate, not an established requirement.

**Model-support gate:** current canonical single-channel light ownership and topology v1/v1.1 PDU-to-QDCD-only feed checks cannot express or validate this path. Retain a candidate/feed ledger in project review records pending a versioned contract and checks. Do not duplicate lights, invent QDCD devices, repurpose sensor-aggregator fields, raise ordinary channel limits or claim the existing checks validated an aggregator. Record the limitation separately from fixture suitability. Manufacturer confirmation for the exact selected EPS aggregator remains outstanding.

### Oversized Fixture Branch and Dedicated Micro Zone

Run the oversized-fixture branch whenever one fixture exceeds **95 W**, before ordinary channel packing. An approved dimming application is **hard-incompatible with the typical EPS aggregator solution** and requires a different solution; do not revise the narrative to fit the hardware. If on/off nominal 48 VDC CV is compatible, install the fixture aggregator and route its necessary 1–4 power-channel feeds. Represent the fixture as its **own combined-power LV micro zone**, with one full-load label, one aggregator output and explicit upstream feed IDs; retain its functional-zone association. The owner describes the larger-fixture band as **100 W < load < 400 W**; resolve the 95–100 W interval explicitly through this same branch and review the nominal 400 W boundary against usable capacity. Do not fold another fixture into the dedicated micro zone or duplicate the fixture's load across feeds. Follow the [decision tree and concrete implementation gap](https://github.com/kissolutions/knowledgebase_wikijs/blob/main/design-playbooks/eps-pdu-allocation.md#oversized-single-fixture-decision-tree-and-micro-zone).

## Two-Sided Voltage-Drop Review

Use the upstream [separate-budget doctrine](https://github.com/kissolutions/knowledgebase_wikijs/blob/main/design-playbooks/smartdc-allocation-index.md#separate-upstream-and-downstream-voltage-drop-budgets). Record source-to-controller and controller-to-fixture budgets independently with selected-device and conductor evidence. Keep derived reach tables here, scoped to the actual voltage/current/output profiles, temperature/resistance basis, one-way versus loop length and installed wiring arrangement. The proposal's reach table is pending verification; do not publish its rounded values as verified limits or adopt 6%/3% by default.

Record route centreline length separately from vertical portions, service loops, terminations and purchase allowances. Spare conductors are not an approved paralleling scheme until terminal, equipment and applicable installation requirements are confirmed.

## Routing Objective and Review Outputs

Charge pathway opening/support work once per used segment, plus marginal pulling cost per physical cable, and charge changes of direction. Respect pathway quality and exclusion weights in the same objective; do not compute a labour score that ignores them. A direction-sensitive search must retain arrival direction (or an equivalent state) to price turns. Distinguish route feasibility from cost preference: a cheap route is not permission to violate a no-go or crossing-only rule.

Report pathway length, physical cable length, support count and spacing basis, heavy-run definition/count, corner count, assumed cost coefficients and unresolved installation conditions. Labour coefficients and support spacing are project inputs requiring installer calibration, not universal defaults. A bend penalty is a costing assumption, not a universal support prescription. Follow the [reviewer exclusion legend](control-system-markup-legend.md#reviewer-routing-exclusions). These are required design/review methods; no routing optimiser is implemented by this documentation change.
