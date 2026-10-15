---
title: "Cable Routes and Bundle Trees v0.9"
page_type: canonical_model
page_status: draft
confidence_level: medium
domain_primary: low-voltage-lighting
ai_role: model_contract
invocation_triggers:
  systems_present: [low_voltage_lighting]
decision_axes: [model_semantics, routing_identity, geometry_review, conductor_identity]
related_pages:
  - "README.md"
  - "decision-and-assumption.md"
  - "milestone-markup-v1.md"
  - "../../design-playbooks/controller-power-placement.md"
  - "../../validation/README.md"
---

# Cable Routes and Bundle Trees v0.9

## Purpose and Scope

Routes are developed **during equipment placement**, through the existing
[placement/review loop](../../design-playbooks/controller-power-placement.md).
The v0.9 model/checker represents directed PDU-to-controller power bundle trees,
controller stations, physical cables and separate controller-output drops. It
checks entered routing; it does not select equipment, solve paths or certify
installation. The original independent-route shape of October change F is
superseded by this contract.

A physical cable carries *n* circuits: it is one cable, not *n* routes sharing
geometry. A bundle segment carries multiple physical cables. Conductor fields
therefore belong to cable records, not a single gauge assigned to a mixed bundle.
A circuit/feed count and a cable/jacket count are distinct. Paralleled conductors
remain inside their cable; their identity does not create alternative paths.

v0.9 extends v0.8 without changing its schema. Earlier validators and migration
paths remain supported. The old v0.1 `design.cable_routes` reserved array and the
separate topology companion's signal routes are not reinterpreted or migrated.

## Fields and Meaning

Authoritative records are the seven flat tables below, validated by
[bundle-records-v0.9.schema.json](../../../schemas/bundle-records-v0.9.schema.json).
CSV files have the exact schema property order as their headers. Null scalar
cells are empty; array cells are JSON arrays in properly quoted CSV cells.
Equivalent flat records can be passed directly to the builder. Do not maintain
an independently editable JSON copy: `lighting-project` v0.9 `bundle_routes` is
a generated export. Regeneration with `--tables` always uses the flat source.
Nested trees, calculated columns and review CSVs are read-only derived views.

| Table | Authoritative data |
|---|---|
| `frames` | Frame ID, canonical drawing page ID, served level, positive feet per displayed page unit, calibration basis |
| `bundles` | Bundle ID, single parent or null root, source ID, flow, level/frame, ordered `serves`, annotation ID, existing review metadata and dependent assumption IDs |
| `geometry` | Bundle ID, contiguous zero-based vertex sequence, x/y; no nested vertices in bundle rows |
| `attachments` | Controller ID, parent upstream bundle, station in feet from its start, signed perpendicular offset in feet, existing review metadata |
| `cables` | Physical cable ID, flow, source and endpoint, conductor count/gauge, separate nullable slack basis |
| `circuits` | Circuit ID, cable ID, source and destination port labels |
| `conductors` | Cable ID, conductor number, circuit ID, polarity, parallel group and nullable effective gauge |

Frames, geometry and physical mappings are separate to prevent duplicate editable
facts. The source directory requires one CSV for each kind.

Coordinates follow the model's displayed-page frame: upper-left origin, x right,
y down, after crop and rotation. `feet_per_unit` is explicitly calibrated; a
printed scale or a PDF coordinate alone is not calibration evidence. The PDF
adapter must transform raw `/Vertices` into this frame. Offset uses the left
normal `(-dy, dx)` in these coordinates. At a vertex, the arriving segment sets
the normal. Position and length are derived at full precision.

For upstream bundles, `serves` is the sorted set of downstream controller IDs.
Identity is `B-` plus the full SHA-256 of the UTF-8 compact JSON sorted set
(`ensure_ascii=False`). Geometry never enters the hash. A changed set produces
a new ID; repeated sets produce an error, never deduplication. A single-child
segment with no termination has the same served set and must be represented
as additional vertices of its parent segment instead. Source changes still
require review even though the mandated identity hash is served-set-only.

**Drop identity is a separate domain.** Drops terminate at output channels,
not downstream controllers. v0.9 supports one root branch per canonical channel,
with `D-` plus the same hash algorithm over its singleton channel-ID set.
`source_id` is its controller, `flow` is `drop`, and its controller count is zero.
Do not hash the source controller to identify multiple different output drops.
Upstream source IDs reference canonical power units. Drop channels must be
assigned to their source controller in the canonical model. More elaborate
fixture fan-out/drop trees require a later extension.

The builder derives `controllers_terminating`, `cables_terminating`,
`downstream_controllers`, `downstream_cables`, cable ID membership, `length_ft`,
controller x/y, and separate upstream/drop totals. Counts cannot be entered as
editable fields. Controllers normally terminate at a segment's far end;
linear stations remain valid anywhere within the segment after review edits.
Cable centerline lengths stop at each terminating controller's station and
include full ancestor segments. Lateral offsets, service loops, vertical drops,
terminations and slack are **not** included in those cable quantities. Installed
length remains unvalidated. Record a slack basis separately; no allowance is
silently invented.

## Relationships

A bundle has one parent except a source segment. Multiple roots are allowed as
a forest; every component reaches its explicit source. Each controller has one
upstream attachment; two-PDU redundancy is out of scope. A child and parent
share source, flow, frame and level and meet geometrically. A drop starting at
a controller represented in the same record set must meet its derived position.
Port labels and conductor mappings preserve circuit identity, but do not prove
manufacturer terminal suitability or reconcile the topology companion's feed
ledger automatically. Continue validating that companion separately.

Signals (SDCnet, PDnet, sensor chains/rings) are not power trees. Pathways can
contain loops; if they become shared infrastructure they need a separate graph
with bundle trees laid over it. This extension does not build that pathway
model. Cross-level or cross-frame edges fail closed: an explicit calibrated
riser/root-link extension is still needed. Separate level-local roots must not
be presented as a measured whole-building route.

## Constraints and Validation

`generators.model_bundles.build` rejects cycles, including disconnected cycles,
and names their edges. It never selects a spanning tree or discards edges.
Edges = nodes − 1 alone cannot prove a tree. It checks parent references,
canonical served-set identity, disjoint children/terminations, physical cable
mapping, conductor/polarity/port uniqueness, station limits, geometry continuity
and canonical model references when a model is supplied.

For each upstream node:

- Downstream cable count equals child cable counts plus physical cables terminating locally.
- Downstream controller count equals child counts plus controllers terminating locally.
- Its served set equals the disjoint union of child served sets and local controllers.
- Upstream and drop quantities are never added into one reported scalar.

Conductor records may leave unused conductors unassigned. Every recorded circuit
needs both polarities. Parallel groups cannot cross circuits or polarities;
effective gauge remains entered evidence, not a verified ampacity calculation.

### Geometry return and existing review states

All markup remains live and unflattened, including final packages. Export stable
bundle annotation IDs as `/NM` and retain the annotation register. The existing
manifest accepts bundle IDs as route entities on `cabling`; annotation ID, page
and review metadata must agree with the flat records.

`apply_geometry_return(records, returned)` consumes a full issued-set extraction
with `annotation_id`, `bundle_id`, `parent_bundle_id`, `serves`, `source_id`,
`flow`, `frame_id`, and ordered `vertices` pairs. The PDF extraction layer must
supply retained topology metadata as well as the returned coordinates. This
function is an adapter/checker, **not an implemented PDF extractor**.

Unknown, missing or duplicate annotation IDs stop reconciliation; never match
by proximity. Changed parent/served set/source/frame/flow stops the geometry
return. After validation, new vertices become authoritative in a **new flat-table
revision**. Counts, lengths and controller positions are regenerated without
rerouting. A shortened path cannot swallow an out-of-bounds station. Disconnected
branches or drops require a coherent reviewed edit, not an invented connector.

Use existing `review_status` (proposed/accepted/change_requested) and
`location_basis`. Accepted plus owner_returned holds a controller position:
a route edit that would move it stops for station/offset reconciliation.
Readback itself does not grant acceptance or change review states.

`apply_model_geometry_return` marks referenced existing assumptions `invalidated`
when their route geometry changes; see [decision/assumption rules](decision-and-assumption.md).
The result also lists voltage drop, conductor selection, labour and drop distances
as requiring recomputation. Those electrical/cost engines are **not implemented
here**: `electrical_routing_validated` and `installed_length_validated` remain
false. Do not carry a previous electrical routing approval through a geometry
edit. The existing placement step 10 governs recomputation and retained history;
there is no new stale/pinned state. Missing approved budgets and product evidence
continue to block dependent engineering conclusions.

### Commands and migration

```bash
# v0.3–v0.8 copy upgrade: preserves facts/IDs; adds empty routing tables only.
python -m generators.model_bundles old-model.json --output model-v09.json

# Regenerate a v0.9 model export from authoritative flat CSVs.
python -m generators.model_bundles model-v09.json --tables route-tables --output revised-model.json
python -m generators.model_intake revised-model.json --phase intake
python -m generators.export_intake revised-model.json --output-dir review-v09
```

Nonempty routing exports require `--tables` for regeneration. The exporter adds
`bundle_review_derived.csv` and `controller_positions_derived.csv`; these are
review outputs, not source tables. `nested_view` generates a read-only tree.
`write_tables` requires an empty destination and writes a new source revision.
The caller retains model revision history and reconciles the manifest alongside
accepted changes. An empty migrated route set means not yet routed, not routing
complete. Intake/design data checks do not certify routing readiness.

## Sources and Stewardship

Owner-directed October 14–15 bundle-tree handoff and revised maintainer
instructions; the maintainer instruction supersedes the earlier proximity-match
text and the independent-route version of F. Hash encoding, separate drop ID
domain, calibrated frames and normalized physical cable tables are implementation
choices making that direction explicit. Owner: KIS Solutions.

The [synthetic fixture](../../reference-implementations/synthetic-bundles/README.md)
proves schema/checker behavior, not manufacturer suitability or an actual Bluebeam
polyline edit/save/readback. That viewer round-trip remains a separate proof gate.
