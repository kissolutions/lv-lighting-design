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
  - "lv-project-workflow-and-readiness.md"
  - "architectural-space-intake.md"
  - "../ontology/canonical-model/space-context-v0.3.md"
  - "../validation/README.md"
---

# Low Voltage Lighting Design Playbook

## Purpose and Authority

Extract the MEP lighting/control scheme, check it against the general electrical lighting workflow in `knowledgebase_wikijs`, and implement it with compatible LV equipment. WikiJS owns room/code analysis, vocabulary, control selection/configuration, decision trees and the application guide. This repository owns project intake, the LV canonical model, channel/equipment grouping, validation and output conventions. Follow the [full workflow and readiness map](lv-project-workflow-and-readiness.md) for milestones and implementation gaps.

The starting scheme is the MEP design. Missing or unclear instructions remain unknown and flagged. Do not replace them with a preferred control recipe. A deficiency or implementation opportunity may lead to a redesign only when authority exists and the proposed departure is approved; preserve the original intent and approval evidence.

## Current Model and Source Basis

Use [Space context v0.3](../ontology/canonical-model/space-context-v0.3.md), the [v0.3 schema](../../schemas/lighting-project-v0.3.schema.json), and its seed/checker for new room-based work. The [v0.2 hierarchy](../ontology/canonical-model/device-hierarchy-v0.2.md) supplies device ownership. The original v0.1 schema/checker/CSV exporter remain supported only for v0.1 input; their one-zone-per-channel rule does not govern v0.3 projects.

Begin with [architectural space intake](architectural-space-intake.md). Architectural floor/dimension plans establish room identities, occupied/served levels and boundaries. Reconcile architectural RCP and electrical label/revision discrepancies. MEP lighting plans, schedules, symbols, legends, keyed notes and control details establish fixture/control intent. Assign overhead fixtures to the Space they primarily illuminate while preserving their source sheet and mounting context.

## Working Steps

1. **Register sources and scope.** Record document/sheet revisions, displayed dimensions/rotation, governing revision questions and the project model revision. Preserve all project inputs outside Git.
2. **Inventory Spaces.** Include tagged and untagged areas, unlit service areas and cross-level conditions. Perform [Milestone 1](architectural-space-intake.md#milestone-1-room-inventory-and-source-verification) independent room-list verification and owner review of omissions. No assumptions in source verification.
3. **Capture area evidence.** Prefer clear architectural area labels with a high-confidence transcription note. Review editable boundaries and the applicable printed view scale before accepting measured areas; retain source-versus-measured conflicts.
4. **Extract lighting.** Preserve schedule types and source loads/options. Give physical occurrences stable internal IDs, served Space membership and source locators. Reconcile sheet/room/type quantities, repeated coverage and exclusions independently.
5. **Extract controls.** Preserve original MEP group labels, devices and sequences, including daylight/manual/occupancy/scheduling and normal/emergency distinctions. Check all relevant source notes/details before declaring no information. No prescribed sequence is inferred merely from a room type.
6. **Review source intake.** Independently verify the initial Room Schedule, Lighting Schedule, Lighting Fixtures and Light Points. Preserve accepted owner corrections and unresolved source discrepancies. Set `takeoff_status: reconciled` only when the scoped takeoff has been reviewed, not because references pass software checks.
7. **Check through WikiJS.** Confirm reviewed room/use/area/enclosure/code basis, evaluate the extracted scheme, and record compliant/deficient/ambiguous/no-information findings plus separate implementation-review opportunities. The [status contract discussion](lv-project-workflow-and-readiness.md#control-review-results) is agreed but not yet implemented in v0.3. Approved general design examples supply check criteria; they do not automatically replace MEP intent.
8. **Select compatible LV components.** Confirm fixture/driver load at the supply-channel interface, output/driver compatibility, actual equipment limits and independent control capabilities. Preserve source AC watts separately. Reproduce documented sensor/switch/controller behavior, escalating system limitations and proposed departures.
9. **Establish functional zones.** Preserve specified independent operation and approved corrections, including emergency override/backup behavior. Room-default zones have stable IDs. Shared stair/cross-room zones are used only when source behavior and reviewed constraints support common operation; physical stair identity alone does not override the MEP scheme.
10. **Assign equipment and group channels.** Give each modeled single-input light one channel. Verify controller-output independence, compatibility, per-channel watts, auxiliary loads, unit channel count and aggregate budget. For the selected nominal Class 2 baseline, use the 100 W / <=90 W design profile; other equipment uses its verified profile. A shared supply is permitted only when valid downstream controls preserve the functional zones.
11. **Produce scoped review markups.** Start with one room/sheet: boundaries, lights, source control intent, LV assignments where confirmed, labels/legend and unresolved items. Prove placement/edit/save/readback. Room-review markups may precede final electrical assignments. Follow [progressive markup readiness](lv-project-workflow-and-readiness.md#progressive-markup-readiness).
12. **Coordinate and release later outputs.** Develop equipment locations, routes, connection/configuration details, quantities, sequences, installation coordination and approval evidence. Resolve release-critical questions before issuing. Record field changes, commissioning and as-built reconciliation under the full-cycle milestones.

## Design and Verification Gates

| Question | Supported scope can proceed when | Otherwise |
|---|---|---|
| Is room/source identity supported? | Architectural inventory and applicable revisions are reviewed | Flag identity/revision ambiguity; retain provisional inventory |
| Is MEP behavior documented? | Relevant symbols, legends, schedules, notes and details establish the behavior | Record ambiguous source or no information; seek clarification |
| Is a change proposed? | Authority and approval are documented before adopting the departure | Keep it a proposal; preserve the specified basis |
| Are LV load and compatibility known? | Selected interface load and product evidence are confirmed | Keep assignments provisional; do not issue quantified grouping |
| Are functional controls preserved? | Source/approved behavior, output capacity and applicable emergency paths are reviewed | Flag conflict and revise the affected scope |
| Can the markup be reviewed and returned? | IDs, page placement and annotation edit/readback have been proved for the output type | Perform the small proof before production use |
| Is the package ready for issue? | Coordinated deliverables and release-critical evidence/approvals are complete | Continue review; a validator pass alone is insufficient |

## Electrical Grouping

Functional zones and power channels have separate identities. A zone may use several channels; a channel may serve several zones only when confirmed downstream architecture preserves independent operation. The Light Objects establish the many-to-many relationship without duplicate wattage. Sharing a controller output is a separate decision and cannot collapse independent zones.

Use confirmed LV input load and any required linear length/reference-length basis. Channel load includes confirmed auxiliary load. Compare against the selected design and rated limits; check power-unit aggregate and channel capacities separately. Original AC fixture wattage, nameplate input wattage and connected LV output wattage are distinct quantities. Grouping remains manual in the current tools.

## Review Records and Outputs

Keep source observations, code-check findings, LV implementation, proposals and approved changes distinguishable. Record consequential uncertainties in `open_items[]` with affected IDs and source evidence. A confirmed `decision` means the recorded engineering basis has been confirmed; it does not establish external change/release approval by itself.

The current v0.3 checker emits derived JSON for counts, loads, membership and labels. A v0.3 schedule/markup generator is not implemented; do not send v0.3 data to the v0.1 exporter or hand-restructure it into v0.1 in a way that loses source intent or shared zones. Source occurrence dispositions/exclusions need a reviewed project ledger until their current-version register is developed.

Every review output identifies source/model revision, scope, legend, unresolved items and review status. Keep editable annotations and stable IDs. Native Bluebeam Area behavior requires a successful one-room compatibility test. Owner-returned edits are reconciled to the authoritative model, with evidence/review before regeneration; the round trip is not yet implemented.

## Limits and Stewardship

Entered relationships and arithmetic are checkable today. Architectural/fixture extraction, complete code interpretation, equipment coverage, electrical/emergency suitability, routes, release, commissioning and as-built acceptance remain source/engineering review or development work. Unknown values stay unknown. Passing later engineering checks is not required merely to inventory rooms or prepare an explicitly provisional review markup.

Owner: KIS Solutions. October 2026; draft current workflow. Legacy v0.1 tools/examples remain available for their original contracts.
