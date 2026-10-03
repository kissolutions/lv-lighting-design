---
title: "Space Intake Reconciliation"
page_type: validation_rule
page_status: draft
confidence_level: medium
domain_primary: low-voltage-lighting
ai_role: prescriptive_gate
invocation_triggers:
  systems_present: [low_voltage_lighting]
decision_axes: [source_reconciliation, space_inventory, fixture_membership, control_zoning]
related_pages:
  - "../design-playbooks/architectural-space-intake.md"
  - "../ontology/canonical-model/space-context-v0.3.md"
---

# Space Intake Reconciliation

## Milestone 1 Gate

Verify simple room-list completeness before other source fields. A separate agent independently inventories the architectural plans, then compares the original list and flags omissions, unsupported entries, duplicates, and label/level conflicts. The owner reviews omissions and inventory corrections; establish why each omission occurred or record “cause undetermined.” Every checked source fact must have a source locator or identified owner confirmation, with no assumptions. Approximate logical-boundary geometry is separately permitted as a labeled review proposal, never an asserted source fact. Untagged purpose stays unknown until supported. Pass this gate when every observed space is accounted for and remaining factual questions are explicitly unknown/flagged; do not mistake this for later lighting/code design approval.

The review PDF must retain editable, unflattened boundaries tied to Space IDs. Follow enclosing walls for physical rooms; use flagged approximate closed polygons/rectangles for logical areas within open enclosures. Include all inventoried areas or ID-linked uncertainty callouts. Keep Subject room names, Comments Space IDs/basis, author and unique annotation IDs under the [naming/identity convention](../design-playbooks/architectural-space-intake.md#annotation-type-naming-and-identity). Proposed names and boundaries remain distinct from source facts; review parent/subdivision area overlaps and gaps without double counting. Final consequential areas/membership/zoning need owner-reviewed boundaries. Owner-returned geometry is reconciled by ID and retained for area recalculation with a verified scale. Native Bluebeam Area compatibility is a separate one-room round-trip test; passing model checks does not establish that support. See the [intake workflow](../design-playbooks/architectural-space-intake.md#editable-pdf-review-and-return).

## Pass Condition

The architectural floor/dimension plans are the starting basis for a complete Space inventory. Architectural RCP/electrical label mismatches are recorded and resolved for the scope being finalized. Untagged service areas are accounted for; open-to-below geometry is related to the occupied floor. Each physical light has one primary served Space and its fixture source remains independently traceable. Consequential mounting/boundary uncertainties retain notes and review items. Room/type counts and explicit shared-zone references reconcile without duplicate fixtures.

Explicit architectural room-area labels are captured as the preferred initial area source with `area_basis: source_document`, source locators/revisions, and high-confidence extraction notes when their value, units, and room association are clear. Unclear labels remain flagged without guessed associations. Source areas and later boundary measurements remain distinguishable, with conflicts recorded for review; high extraction confidence does not establish independent measurement verification.

Boundary-area takeoffs use the architectural floor/dimension plan when available, with the applicable RCP as a documented fallback. Accepted measurements retain editable boundary geometry, the applicable view's printed architectural scale and its locator, verification of that scale against the PDF, and review of uncertain boundaries. Missing/conflicting scales or demonstrated PDF resizing require resolution before the affected measured area is accepted.

## Block Condition

Missing architectural starting source, omitted areas, unresolved conflicting identities or consequential boundaries, duplicated lights across levels, arbitrary numerical heights, or unreviewed shared operation block finalization of the affected scope. Other verified work can continue provisionally.

## Implementation and Limits

`generators/model_spaces.py` checks unique light ownership, source-page registration, explicit zone references versus light ownership, supported additional named-zone membership, optional mounting evidence/basis, and inventory-only records with empty light/zone lists and descriptions. It derives zone-to-Space views from explicit references. Synthetic tests cover upper-sheet fixtures serving a lower-floor Space, shared zones across rooms/levels, and unlit service areas.

Independent room extraction, architectural inventory completeness, room-label mismatches, room-area label transcription/association, editable PDF generation/return, native Bluebeam compatibility, markup tracing, printed-scale verification and measurement reconciliation, physical wall interpretation, actual served level, and source plan reconciliation remain source-review or future implementation tasks. These are not automatically performed by the generator. Existing `open_items[]` records hold discrepancies; the hierarchy checker enforces open blocking items.

Owner: KIS Solutions. October 2026; owner-directed draft.
