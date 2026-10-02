---
title: "Low Voltage Lighting Design Playbook"
page_type: playbook
page_status: draft
confidence_level: medium
domain_primary: low-voltage-lighting
ai_role: prescriptive_standard
invocation_triggers:
  systems_present: [low_voltage_lighting]
decision_axes: [source_reconciliation, fixture_selection, control_zoning, channel_grouping, component_quantities]
related_pages:
  - "../ontology/canonical-model/README.md"
  - "../validation/README.md"
---

# Low Voltage Lighting Design Playbook

## 1. Purpose and Use

Use this playbook to turn an MEP lighting plan into a reviewable Phase 1 LV design and quantity basis. The first operator supplies source documents and performs a manual takeoff; the tools validate the model and generate schedules.

## 2. Design Intent

Preserve controls intent, obtain reliable quantities quickly, and make every design transformation traceable. Avoid missed fixtures, overloaded channels, lost micro-zones, guessed loads, and component quantities that assume unavailable device capacity.

## 3. Space / System Definition (Decision-Oriented)

The initial scope is discrete fixture instances in bounded spaces, each with a required control zone, mapped to selected compatible LV fixtures and nominal 100 W channels. A zone can use several channels; a channel belongs to one zone. Fixture type, control zone, channel, and physical power node are separate records.

## 4. Constraint Envelope

### 4.1 Hard constraints and design invariants

Each fixture has exactly one explicit scope disposition. Each included fixture belongs to exactly one channel. Every channel load is <=90 W and obeys any verified lower design limit. Required micro/control-zone boundaries are preserved. Electrical and functional compatibility, power-node channel count, and aggregate budget are confirmed with evidence.

The 90 W ceiling is KIS's initial design doctrine for the nominal 100 W baseline. Actual listing/Class 2 eligibility, wiring constraints, driver characteristics, and applicable code requirements must be verified for the selected system. A wattage check alone does not establish those facts.

### 4.2 Soft constraints

Prefer fewer unnecessary channels, compact geographic groups, useful spare capacity, simple routes, and easy-to-read schedules after the invariants pass.

### 4.3 Hidden constraints

Allow for substitutions, undocumented control notes, fixture symbols that resemble one another, repeated sheets, and node aggregate limits lower than the sum of nominal outputs. Do not let schedule pressure turn uncertainty into confirmed design data.

## 5. Baseline / Default Design Pattern

1. **Capture sources.** Register filename, revision, document ID, actual page index, sheet ID, displayed dimensions, and rotation. Set a stable model revision. Preserve the source set in project storage.
2. **Extract the schedule.** Create source fixture types with original description/wattage/voltage/driver notes and source references. Use `null` for missing information.
3. **Take off occurrences.** Create one fixture instance per physical fixture. Record type, space, source zone, drawing page, and locator. An anchor may be `null` during Phase 1; a locator remains mandatory through `source_ref_ids`.
4. **Capture control intent.** Identify each required room, area, daylight, manual, occupancy, dimming, or other micro-zone from plans and notes. Conflicts become blocking open items. Assign `unknown` intent until evidence or an engineering decision confirms the boundary.
5. **Reconcile sources.** Independently compare source types and occurrence totals by page/space/type against the PDF. Confirm exclusions and repeated drawings. Set `takeoff_status: reconciled` only after this review; software cannot detect symbols never entered into the model.
6. **Normalize the LV schedule.** Create one LV selection per included source type. Verify actual load at the channel interface, driver/output behavior, control function, and compatibility group. Preserve original source wattage. Record selection evidence and a decision.
7. **Declare scope.** Create one explicit included/excluded disposition per fixture. Exclusions require a reason and decision. Emergency/egress or special loads require project-specific review before inclusion; the baseline does not determine their architecture.
8. **Group within boundaries.** Partition by effective control zone and confirmed compatibility group. Assign fixtures to channels using confirmed LV loads, staying at or below 90 W (or lower selected design limit). Record channel decisions. Iterate until each included fixture is assigned once.
9. **Quantify nodes.** Assign channels to explicit power nodes using verified channel count and aggregate design budget. Add separate control nodes only when the selected architecture requires them; combined units are not counted twice.
10. **Validate and export.** Run the validator, resolve blocking issues, and export review CSVs. Use provisional export only for a marked draft; it preserves failing status and lists unresolved checks.
11. **Review the checkpoint.** Review tables against the PDF, source notes, selections, loads, node count, and open items. Save the reviewed model and outputs together in project storage, then set `stage: checkpoint`. Implemented checks passing do not constitute engineering approval.

## 6. Typical Variants

**Lower verified limit:** Reduce `design_limit_watts` below 90 W where equipment/installation constraints require it. Preserve exact assignment and zoning rules.

**Documented source-zone correction:** Add a `zone_assignment` and a confirmed, traceable engineering decision when source intent changes or is clarified. Retain `source_control_zone_id` as the observed fact. Cross-space/zone-sharing systems require an explicit future rule and model extension; they are blocked by this baseline.

**Special or excluded fixtures:** Retain the source occurrence, explicitly exclude it with a reason, and coordinate its separate design. Do not silently drop it from the count.

## 7. Decision Gates

| Gate | Yes | No |
|---|---|---|
| Source set/revisions and takeoff reconciled? | Continue | Resolve discrepancies |
| LV load and compatibility confirmed? | Group fixtures | Open a blocking item; keep provisional |
| Required control intent confirmed? | Preserve boundaries | Obtain clarification |
| Fixture exceeds design limit by itself? | Review alternate fixture/architecture | Group normally |
| Selected node has sufficient channel and aggregate capacity? | Quantify explicit nodes | Revise hardware/nodes and regroup |
| Validation and source review complete? | Save the Phase 1 checkpoint | Revise and recheck |

## 8. Design Zoning / Grouping Strategy

Within each confirmed zone and compatibility group, use a manual load ledger and compact fixture groups. A 20 W fixture group of four is 80 W; adding a fifth is 100 W and fails the 90 W ceiling. Two channels may serve one zone while maintaining coordinated control. Do not merge required zones to improve channel utilization.

## 9. Common Failure Modes

Design-time: replacing unknown loads with zero; using AC source wattage for an unverified LV conversion; equating watts with driver compatibility; ignoring node aggregate capacity.

Documentation: missing occurrences, duplicate IDs, broken source links, silently edited source zones, stale calculated totals, and unlabeled provisional exports.

Construction/operation: incompatible output/driver combinations, controls that no longer preserve intent, and installer-facing cable lengths inferred without calibrated geometry.

## 10. Safe Assumptions (and Limits)

The initial 100/90 W baseline applies only while the chosen product and installation support it. Record assumptions with an `invalidated_if` condition. Substitution, driver change, reduced device output, revised zoning, or updated plan invalidates dependent decisions and triggers review.

## 11. Documentation Expectations

Phase 1: original and LV fixture schedules, every fixture's disposition/assignment, effective zone, channel load/margin, node counts/capacity basis, source references, and open items. Exported views carry model revision and review status.

Phase 2: source PDF revision, stable page transforms, identifiers, node locations, channel graphics, projected bundle paths, legend, and coordinated installer notes. The PDF remains a rendering of the model.

## 12. When to Go Deeper / Exit This Playbook

Exit for emergency/egress architecture, unsupported shared control boundaries, fixtures needing split power interfaces, unverified electrical behavior, systems outside the 100 W baseline, or cable/routing constraints that invalidate Phase 1 grouping. Resolve with project-specific engineering before extending reusable rules.

## 13. Cross-Links to Supporting Knowledge

- [Model overview](../ontology/canonical-model/README.md)
- [Channel grouping concept](../concepts/channel-grouping.md)
- [Product constraint intake](../product-classes/class2-power-control-systems.md)
- [Validation rules](../validation/README.md)
- [Parent framework](https://github.com/kissolutions/knowledgebase_wikijs/blob/main/AI/AGENT-FRAMEWORK-GUIDE.md)

## 14. Status and Stewardship

Draft; owner KIS Solutions; last review October 2026. Software behavior is tested on synthetic data. Real-project takeoff and engineering review are the next validation step.

## 15. Author Notes (Institutional Context)

The initial handoff prioritizes usable quantities before polished markup. Keep the first implementation narrow and improve it from one representative project rather than adding unused lighting conditions.
