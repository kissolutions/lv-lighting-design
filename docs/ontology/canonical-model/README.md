# Canonical Lighting Model v0.1.0

The current contract is [Physical Intake v0.4](physical-intake-v0.4.md). Root light records have served Spaces before zones exist. Use its phase checker and current review exporter; the v0.1/v0.2/v0.3 descriptions below preserve their historical executable contracts.

Current Space intake follows the [architectural-first workflow](../../design-playbooks/architectural-space-intake.md). Draft 0.3.1 distinguishes occupied level from fixture mounting height, accounts for unlit service areas, and supports reviewed named zones spanning Spaces/levels. Shared stair zoning preserves specified MEP behavior and applicable independent-control constraints. Consequential boundary details remain narrative evidence and review items.

Follow the [full LV workflow and readiness map](../../design-playbooks/lv-project-workflow-and-readiness.md): extract MEP intent, check through WikiJS, preserve it in LV implementation, and adopt departures only with authority/approval. The current [v0.5 electrical-interface extension](electrical-interfaces-v0.5.md) adds source voltage beside source load and selected light/channel compatibility checks while retaining v0.4 physical-first ownership. The agreed zone review statuses are documented but not yet schema fields.

The preserved Space extension is [Space Context v0.3](space-context-v0.3.md), extending [Device Hierarchy v0.2](device-hierarchy-v0.2.md). Read [Space](space.md) for room conditions and independent code classifications, and [fixture identity](../../concepts/fixture-identity-and-summary-counts.md) for occurrence IDs and derived quantities. This page otherwise documents the preserved v0.1 baseline. Its flat collections and one-zone-per-channel restriction are superseded for new work; the v0.1 executable tools still enforce them on v0.1 input.

The [JSON schema](../../../schemas/lighting-project.schema.json) is the machine-readable structure. These pages define its meaning. [Phase 1 validation](../../validation/README.md) checks relationships and engineering invariants beyond JSON Schema.

## Separation and relationships

| Section | Role | Collections |
|---|---|---|
| Root/project | Identity, source register, drawing context | `project`, `source_documents`, `drawing_pages`, `source_references` |
| `facts` | Observed plan/schedule facts | `spaces`, `control_zones`, `fixture_types`, `fixture_instances` |
| `design` | Engineering transformation | `fixture_selections`, `fixture_scope`, `zone_assignments`, `lv_channels`, `power_nodes`, `control_nodes`, `decisions`, `assumptions` |
| `design.cable_routes` | Future projected geometry | Route points and channel membership |
| `open_items` | Unresolved/closed uncertainty | Gaps, consequences, blocking state, resolutions |

One type has many physical occurrences. Each included occurrence has one LV selection through its type and one channel. A control zone can span several channels, all inside its space. Each channel is assigned to one power node for quantified design. Decisions cite source evidence and any assumptions they depend on.

Record arrays are normalized and connected by globally unique stable IDs. The logical source page -> space -> zone -> fixture relationship is represented by IDs rather than duplicated nested objects. A space can occur on multiple drawing pages without creating duplicate fixtures.

## Contract rules

- Required unknown nullable fields use `null`. Missing fields are structural errors. Empty collections are allowed in the seed but incomplete takeoffs fail Phase 1 checks.
- `source_input_watts` preserves the original schedule; `lv_input_watts` is the confirmed design load. Connected channel watts and margins are calculated, never stored as editable authority.
- `compatibility_group` is an engineering-confirmed key based on verified electrical and control behavior. A matching key allows a software consistency check; it does not itself prove compatibility.
- `project.stage` describes workflow, not approval. `takeoff_status: reconciled` records a human source audit that software cannot independently verify.
- Unknown spatial anchors are allowed in Phase 1. Known anchors must fall within their page bounds.
- Display coordinates use points, origin at the displayed page's upper-left, +x right and +y down, after crop/rotation. Preserve `pdf_rotation_deg`. A future renderer must explicitly map between displayed and raw PDF coordinates; engineering scale is separate and unmodeled.
- Scope and zone corrections are decisions; keep their source occurrences and source zones unchanged.
- Schema changes require versioning and synchronized documentation/examples/validators. v0.1.0 is draft and has no migration guarantee until the first project review.

## Element pages

[Project](project.md), [drawing page](drawing-page.md), [space](space.md), [control zone](control-zone.md), [fixture type](fixture-type.md), [fixture instance](fixture-instance.md), [LV fixture selection](fixture-selection.md), [LV channel](lv-channel.md), [power node](power-node.md), [control node](control-node.md), [cable route](cable-route.md), [open item](open-item.md), [source reference](source-reference.md), [decision and assumption](decision-and-assumption.md).


## Current v0.2 element pages

[HV branch circuit](branch-circuit.md), [power unit](power-unit.md), [LV light zone](lv-light-zone.md), [light object](light-object.md), [controller](controller.md), [control device/system](control-device.md), [shared control group](control-group.md), [backup supply](backup-supply.md). Power-channel fields and many-to-many derived membership are defined in [the hierarchy contract](device-hierarchy-v0.2.md).


## Controller/power topology companion

[Companion v1](controller-power-topology-v1.md) pairs with v0.6 and adds AHJ/plenum, equipment placement, PDU-to-QDCD feeds, sensor port/control associations, bus strings and routes. Validate both contracts separately.
