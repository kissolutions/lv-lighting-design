---
title: "LV Markup Deliverable Presentation Contracts"
page_type: playbook
page_status: draft
confidence_level: medium
domain_primary: low-voltage-lighting
ai_role: prescriptive_standard
invocation_triggers:
  systems_present: [low_voltage_lighting]
decision_axes: [deliverable_composition, annotation_presentation, publication_edition, owner_handoff]
related_pages:
  - "milestone-review-packages.md"
  - "control-system-markup-legend.md"
  - "lv-project-workflow-and-readiness.md"
  - "../governance-and-doctrine/october-16-consolidated-reconciliation.md"
---

# LV Markup Deliverable Presentation Contracts

Revision: 2026-11-01. Consolidates owner directions of October 29–30 and the final live FreeText form H selected November 1, 2026.
Status: owner-directed presentation definitions; owner-authorized publication to main on October 30, 2026. Reusable generator implementation and viewer verification remain separate work. Draft page status does not reopen explicit owner decisions.

## 1. Authority and purpose

Presentation inconsistency is an identified framework deficiency. A deliverable's content, composition, labels, colors, editability and dependencies are explicit contracts, not choices to reinvent during each project. This page takes precedence over conflicting older presentation wording for the deliverables defined here. Preserve source authority, engineering checks, accepted geometry, stable IDs, assignments and chain order.

These definitions refine plan markups; they do not renumber M1–M6 or review packages P1–P6, replace schedule contracts, approve construction, or silently adopt an entire external bid-package proposal.

## 2. Forms, identity and shared rules

| Form | Meaning |
|---|---|
| Full / Live | Current-step working markups stay editable. All included markup components inherited from earlier frozen steps are flattened references. Retain each earlier step's separate live master. |
| Flattened / External | Publication component retaining the full visible information defined for that component, flattened with selected properties popups enabled. |
| Abridged / Integrated | Compact publication/reference component. Omit the external text specified below and retain object identification in properties popups. Content is explicitly defined per component. |

Presentation form is distinct from engineering/source revision, review status and commercial estimate class. Record component name, form, source/model revision, placement/route revision where relevant, and output issue revision in the existing issue manifest or project issue record. Do not add unversioned fields to canonical schemas.

- All markup text/ID annotations use **4 pt at native PDF scale**, with **1.00 text margins on all sides**, including single-line labels. Preserve this setting explicitly; do not silently autosize text or use zero margins.
- **Live FreeText form H (2026-11-01):** Follow [Live FreeText Form H](live-freetext-form-h.md). Write the 1.00 margin as `margin:1pt` in `/DS`; **do not write `/RD` or generated `/RC`**. Match `/DA`, `/DS` and explicit appearance font/size/color. `/DS` uses family before size, 4.6 pt leading, and the metric-sized layout. Appearance `/BBox` equals `/Rect` in page coordinates, with no placement matrix. The shared helper/normalizer and live-plan checker implement this profile.
- The earlier margin-only causal explanation is superseded by later owner tests and annotation read-back: inconsistent styles, missing CSS margin, wrapping/color conversion and Foxit appearance rewriting contributed. The final owner-selected form H opened acceptably in Bluebeam; Foxit multi-line leading differences remain accepted. This is scoped field evidence, not universal viewer certification.
- **Bluebeam is the editing tool; Foxit is view-only.** Normalize any Foxit-saved live PDF into a new revision before more Bluebeam editing. Use `python -m tools.normalize_freetext_ap INPUT.pdf NEW_REVISION.pdf`, then the live-plan checker. Preserve IDs, contents, layer membership and current label top-left; resizing label boxes/rebuilding appearances is intentional. Normalization does not recover already-lost positions.
- Where testing is performed, inspect font, color, box dimensions and margins through two moves, save and reopen. Do not infer correctness from one unchanged-file round trip.
- Render labels above linework. Move label offsets independently of physical anchors.
- Keep editable graphic and text annotations separately identity-linked to their authoritative entity. Preserve immutable annotation IDs outside the short display metadata. Do not append machine payloads to the Light Point Subject.
- Unknown engineering values remain unknown; graphic color is not an engineering selection or acceptance.
- Compose from authoritative records and registered geometry, using the named presentation contracts. Do not use a flattened PDF as a new quantity/location database.
- Include each shared source background, graphic and physical device once in a combined view. Reused components must not produce duplicate Light Points or room shapes.
- Room boundaries are **not** a universal background. Include them only where the component definition calls for them.
- Retain live masters. External flattening does not authorize flattening the editable design source. Locked/read-only external publication copies are distinct from unlocked owner-review masters; the detailed external issue/protection policy remains under reconciliation.

### Frozen prior steps and current-step editing

**Owner direction, 2026-11-01:** In every downstream working deliverable, **all included markups from earlier frozen steps are flattened**. Only the current step's active markups remain open for editing. This supersedes the older blanket “all markup stays editable at every stage” wording for inherited content.

- Flatten derivative copies, never the frozen original or its retained live master. Retain the exact frozen source revision and component-to-page/layer mapping in the issue record.
- Include only the prior components called for by the drawing composition. This rule does not add room boundaries to PDnet/SDCnet or restore any deliberately omitted component.
- Flatten the inherited shapes, fills, symbols **and their text tags**. Use the full-information Flattened form unless the composition explicitly calls for Abridged; flattening alone does not remove labels.
- Keep the defined properties popups and independent reference-layer visibility, where applicable. Insert inherited references below current-step markup. A locked live annotation is not a substitute for a flattened reference.
- **M2 Lighting Takeoff explicitly imports M1 Room Boundaries — Flattened**, including the room graphics/text/properties required by that composition. M2 Light Point graphics, ID/type text and other active M2 annotations remain live under the current presentation/form-H rules.
- Freezing a step preserves its recorded state; it does not automatically approve provisional facts, close exceptions or grant code acceptance.
- To change inherited information, reopen the responsible earlier step, edit its live source under the existing review rules, freeze a new revision, and regenerate the dependent flattened references. Do not edit a flattened reference or silently alter the former frozen issue.
- Keep immutable object identities across steps. If a current-step component enriches/replaces a previous rendering of the same objects, use one identified current representation rather than duplicating old flattened and new live symbols. Accepted prior facts/anchors remain protected.
- The current editable-annotation register/readback scope covers the active step. Retain earlier source registers with their frozen steps and link them in the assembly record; do not require their flattened graphic annotation IDs to survive as live objects in the downstream PDF.
- Verify flattened reference appearance/popups/layers separately from current live edit/save/readback. No inherited unflattened duplicates should remain as editable shapes/text. The existing strict live-PDF checker does not automatically classify flatten-generated popup annotations; do not bypass its identity checks by ignoring unknown annotations or changing arbitrary annotations to reference status.

| Working deliverable | Earlier frozen content, if included | Editable content |
|---|---|---|
| M1 Room Boundaries | Any explicitly included earlier frozen reference | Current M1 boundary shapes and room text |
| M2 Lighting Takeoff | **M1 Room Boundaries — Flattened** | Current M2 Light Point graphics, IDs/type marks and other active M2 markup |
| Later milestone/step | Required components from every earlier frozen step, flattened (or Abridged where explicitly specified) | Only that step's active device/zone/channel/route/review markup |

This is the composition/assembly policy. It does not claim that a general PDF flattener, popup-classification adapter or frozen-reference validator is implemented. A supplied live master remains editable in its own step even though its downstream reference copy is flattened.

### Flattening and popup behavior

Bluebeam's Flatten Markups supports **Show Properties in Popup**, with selected properties, and flattening to layers. Plainly drawing graphics into page content does not automatically reproduce popups. Select Subject for Light Point identification and the defined room/device information for their popups. Preserve independent layer visibility where the composition requires it. Verify popup behavior and layer controls in the actual saved publication and intended viewer; do not promise cross-viewer equivalence.

Reference: [Bluebeam Flatten Markups](https://support.bluebeam.com/user-manual/menus/document/flatten-markups.html). This reference supports the application method, not proof of a framework generator.

## 3. Light Points

Three independently controllable layers: **fixture representations**, **Light Point IDs**, **fixture type marks**.

Use a simple representation at the accepted anchor: dot, triangle, square or suitable fixture graphic. Put the Light Point ID inside the graphic where practical, but keep it a separate text annotation/layer. The exact source fixture type designation is separate visible text. The agent selects distinct colors per scheduled fixture type/name, applies them consistently across levels, and includes a type-to-color legend. Do not replace approved labels or renumber.

The graphic's **Subject is exactly** `<Light Point ID> <fixture type mark>`, one space, e.g. `L042 A2`. No extra descriptive text. Keep only necessary technical identity linkage separately; no superfluous repeated descriptive properties.

| Form | Content |
|---|---|
| Full / Live | Editable type-colored graphic, separate approved ID text and exact fixture-type text. |
| Flattened / External | Full visible graphic/ID/type content; flatten the graphic with Subject popup enabled. Retain separate text-layer visibility. Flattening publication text must preserve its defined appearance. |
| Abridged / Integrated | Type-colored graphic only; omit both external text layers; flattened graphic with Subject popup enabled. |

## 4. Room Boundaries

Distinct from the Energy Code Set.

Full / Live uses editable closed polygons or simple closed shapes representing the accepted room boundary. Do not convert an accepted shape merely for stylistic uniformity; retain identity/geometry and document any necessary reconciliation. Open disconnected boundary segments alone are not the full shape.

Visible room text: **room name, Room ID and energy-code space type**, in room text boxes. Unsupported classification is TBD; do not invent it.

Retain the established room-map categories and color families:

| Category | Color |
|---|---|
| Enclosed rooms | Blue |
| Corridors / halls / circulation | Green |
| Open activity / common areas | Ruddy orange |
| Atriums / open-to-above | Violet |
| Service voids / confirmed excluded or no-lighting areas | Gray |
| Exterior | Wine / burgundy |

Existing category precedence, low-opacity source visibility, source-area/check-area distinctions and geometric review rules remain. These colors are independent of code types and device colors.

Room shape properties/popup contain Room ID, room name, source room number where known, source room type, building-code space type, building-code occupancy group, energy-code space type and functional description. Preserve unknowns. Current fields are `id`, `name`, `room_number`, `source_room_type`, `building_code_space_type`, `building_code_occupancy_group`, `energy_code_space_type`, `description`; level and enclosure remain available in the database. The four type/classification fields are independent.

| Form | Content |
|---|---|
| Full / Live | Editable shapes and room text for handoff. |
| Flattened / External | Same visible shapes/text, flattened with room properties popups enabled. |
| Abridged / Integrated | Full room shapes flattened with room properties popups; omit external room text. |

## 5. Room Devices

Reusable markup component and standalone view of the Energy Code Set. Includes room switches/controls, occupancy sensors, ALS/daylight sensors and applicable controlled-system relays/other room devices. QDCD, PDU, CIO and SW equipment belong to the separate equipment component.

| Device type | Color |
|---|---|
| Wall switches / wall controls | Blue |
| Occupancy sensors | Red |
| ALS / daylight sensors | Green |
| Combined ALS / occupancy sensors | Purple |
| Other device types | Agent selects consistent distinct colors and documents the legend. |

These owner colors supersede older all-purple room-device rules. Existing device symbol shapes remain unless explicitly revised; no new equipment symbol/color scheme is implied.

| Form | Content |
|---|---|
| Full / Live | Editable device symbols, separate device-ID text and device properties. |
| Flattened | Same colors and ID labels; flattened with properties popups. |
| Abridged / Integrated | Device symbols with properties popups; omit separate ID text. |

Properties preserve device identification and available role/association information. Exact minimal device popup field order has not yet been defined; do not claim it was settled.

## 6. Energy Code Set

A separate controls-design set equivalent in purpose to an MEP lighting-control plan **without circuiting**. Does not imply code-compliance certification.

**Full composition:**

1. Room Boundaries — Abridged / Integrated, inserted first at the bottom of the stack, with low-opacity reference fills and useful room popups.
2. Room Devices — Full / Live, showing applicable controls, occupancy/daylight sensors, relays and future receptacle/fan/shade controls.
3. Separate sequence-ID text inside each room.
4. Append applicable sequence ID(s) to room-shape metadata; assign a distinct color per determined sequence type/line item, recoloring room shapes and including a legend.

Sequence/device facts come from current authoritative assignments, not stale narrative exports. Before sequences exist, allow a **provisional device-layout view**: retain room reference colors and omit all sequence-ID/recoloring steps. A complete sequence-based issue needs devices and sequences.

Multiple-sequence room color treatment and whole-set Flattened/Abridged composition are not yet defined. Do not choose a single sequence silently or invent a new approval gate.

## 7. Micro LV Channels

| Form | Content |
|---|---|
| Full / Live | Light Points — Abridged underneath; editable fixture-to-fixture channel lines connecting assigned Light Points in accepted order; editable channel-ID text at the first fixture reached. |
| Flattened | Same channel lines and channel-ID text, flattened with properties enabled, using the same underlying Light Point reference when standalone. |
| Abridged | Channel lines only; no channel-ID text. Underlying Light Points are a separately selected component when composing a larger set. |

Channel line colors: **green CV, orange CC, black unknown/unselected**. Use the selected channel-interface CV/CC basis, not a generic dimming label or assumed source driver. Preserve unknown state.

Channel-ID labels follow 4 pt / 1.00 margins. Preserve accepted membership and chain order. A single-light channel needs its ID but no fabricated fixture-to-fixture line. Lines show connection/order, not series electrical wiring or surveyed cable routes.

The owner has not specified microchannel line width/dash here. **Do not inherit the 2.0 dashed reach-line style below.** No automatic room boundaries or equipment symbols are included.

## 8. QDCD-to-Fixture Connections

**Full composition:** Light Points — Abridged; Micro LV Channels — **Flattened**, not Abridged; current QDCD graphics/locations; editable straight association/reach lines from each QDCD output to the first fixture of its assigned channel.

Reach lines: **2.0 width, dashed**, **green CV / orange CC / black unknown or unselected**. Respect the accepted first fixture/chain entry point. The underlying microchannel component supplies fixture-to-fixture connections; avoid duplicating its Light Points when assembling.

These straight reach lines express association and location efficiency, not surveyed route length. Full/Flattened/Abridged forms for QDCD equipment itself and additional connection-set variants remain to define.

## 9. PDnet Set

Show CIOs, QDCDs, their current PDnet daisy-chain routing polylines and straight QDCD-output-to-first-fixture association lines whenever assignments/entry points exist. Pull **Light Points — Abridged**.

**Do not include room boundaries or fixture-to-fixture chains by default.** In particular, do not import the whole QDCD-to-Fixture Full set, because it includes flattened microchannel chains. Reuse only its reach-line presentation.

Keep PDnet routes and fixture association lines on separate layers. Preserve current equipment identities, accepted hop geometry/order and explicit proposed status. Incomplete associations stay incomplete rather than invented. These lines support routing/location-efficiency review.

PDnet route labels/properties and all publication variants remain partly undefined.

### PDnet Bundles — Abridged / Reference

Owner-confirmed reference view of the current PDnet bundle/path polylines: significantly widened strokes, **light grayscale / low opacity**, no external labels, identification in properties popups. Draw below active network routes, devices and association lines. Width is a presentation choice, not physical bundle size or cable count. Exact width/opacity and which sets include this by default remain open. The name does not authorize substituting PDU power-bundle geometry for PDnet records.

## 10. SDCnet Set

Show current CIO and SDCnet module (SW4/SW8 and other applicable module) graphics/locations, SDCnet routing polylines, and **Room Devices — Abridged / Integrated**. This last selection is explicit: no imported room-device ID text.

Show room-device-to-assigned-SW association lines separately from SDCnet bus routes. Omit room boundaries, sequence labels and Light Points by default. Retrieve room-device records through the reusable component rather than importing the Energy Code Set as a whole.

CIO/module ID presentation follows existing equipment guidance until redefined. Room-device actual cable routes versus straight association presentation, network label/property details and publication variants still need a defining pass.

## 11. Composition dependency register

| Deliverable | Explicit dependencies |
|---|---|
| Light Points | Current Light Point anchors, approved IDs, exact scheduled type marks |
| Room Boundaries | Current accepted Space geometry, room records and classifications |
| M2 Lighting Takeoff — Full / Live | M1 Room Boundaries — **Flattened** from the identified frozen M1 issue; current M2 Light Points — **Full / Live** |
| Room Devices | Current physical room-device records and locations |
| Energy Code — Full | Room Boundaries — Abridged; Room Devices — Full; current sequences |
| Micro LV Channels — Full | Light Points — Abridged; accepted channel membership/order; channel-ID labels |
| QDCD-to-Fixture — Full | Light Points — Abridged; Micro LV Channels — Flattened; QDCD locations; reach lines |
| PDnet | Light Points — Abridged; CIO/QDCD locations; PDnet routes; reach lines only |
| SDCnet | Room Devices — Abridged; CIO/SW locations; SDCnet routes; device associations |
| PDnet Bundles — Abridged / Reference | Current identified PDnet path geometry; set inclusion not yet fixed |

Assembly may filter component content, but must explicitly record the chosen subset, flatten all included components from earlier frozen steps, and deduplicate common objects. Source/model and component revisions remain recoverable. Regeneration changes a working issue, never an already frozen issue.

## 12. Remaining defining passes

- Controller and Power Equipment: Full/Flattened/Abridged content, symbols, colors, IDs and popup details. No standalone all-devices set has been adopted; Room Devices is the defined reusable subset.
- PDU Feed / Power Bundle Routing: widths, junctions, labels, properties and integration forms.
- Room-device cable routing: actual routes, association-line roles, port/length presentation.
- Energy Code: multiple-sequence colors and whole-set publication variants.
- PDnet/SDCnet: network label/property contracts and publication forms.
- Combined/Coordinated plan: component versions, layer order/default visibility and duplicate suppression.
- Exact microchannel stroke style; exact gray-reference width/opacity.
- Automated renderer implementation and tested popup/OCG/edit-save-readback behavior.

Do not invent these definitions during packaging. Use established older guidance where compatible and identify any necessary scoped project choice.

## 13. External bid-package proposal boundary

The separate external package proposal identifies BID-FX (fixture supplier), BID-CTL (controls vendor) and BID-LV (installer). Preserve their audience-specific intent alongside P1–P6 and the existing Full/Abridged Basis of Design sets; do not silently replace those families.

Recorded package direction:

- BID-FX: fixture schedule, typed Light Point plan sheets, individual Light Point table; workbook companion.
- BID-CTL: orderable device schedule, layered per-level room/sequence/device/connection/network views, physical device list; workbook companion.
- BID-LV: scope/directives, cable schedule, installation quantities/support specification, separate printed device/power/control sheets, detailed segments/support tables, alternates/open items and spreadsheet bid form.

These are **proposal-level package definitions**, not proof of reusable generators or wholesale adoption of their project examples. No real project counts, client files or product-specific defaults are imported here.

The DD1–DD17 source proposals were not available in this reconciliation. External entry criteria, confidence vocabulary, allowances, naming/freeze rules and bid-form details cannot be claimed fully reconciled without them. Outstanding conflicts include schedule-first versus installer scope-first order; accepted-only source language versus explicitly proposed routes; frozen-draft replacement; equipment legends; and publication protection policy.

Support-spacing, cable separation, truss attachment, hard-ceiling treatment, voltages, network power/length limits, termination methods and scope allocations require project/evidence basis. Unverified technical citations in the external proposal are not adopted standards. Estimate class, presentation form and commercial price commitment remain distinct.

## 14. Delivery verification and implementation limits

Before handoff, verify the saved artifact against the selected composition: correct input revisions, required/absent layers, colors and labels, 4 pt text / 1.00 margins, accepted locations/chain order, exact Light Point Subject, room/device properties, layer visibility and popup retention after flattening. Check that reference lines are not reported as measured routes.

A flattened Abridged reference in a Full composite is intentionally not editable; its retained live source is the place to make authoritative changes. New working annotations remain editable. A Full file name alone does not prove all embedded references are live.

The original October 30 contract was documentation only. The November 1 form-H implementation adds a live FreeText style/layout helper, updates the subzone writer, extends the saved-PDF checker, and provides a new-revision normalizer. Checks cover style/appearance agreement, CSS margins, width/height and Bluebeam-workflow BBox/matrix conventions; they do not certify native viewer behavior, visual completeness or popup survival. No engineering schema/validator or existing project PDF is changed by this framework update. No construction acceptance or maintaining-agent native-viewer proof is implied.

