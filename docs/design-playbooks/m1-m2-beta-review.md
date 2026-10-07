---
title: "M1/M2 Room Geometry and Physical Intake Review"
page_type: playbook
page_status: draft
confidence_level: medium
domain_primary: low-voltage-lighting
ai_role: prescriptive_standard
invocation_triggers:
  systems_present: [low_voltage_lighting]
decision_axes: [room_geometry, source_identity, physical_quantity, annotation_readback]
related_pages:
  - "architectural-space-intake.md"
  - "m2-linear-fixture-extraction.md"
  - "milestone-review-packages.md"
---

# M1/M2 Room Geometry and Physical Intake Review

## Authority and precedence

Owner-directed beta lessons, 2026-10-06. These rules apply to room-footprint and takeoff review. The room notch rule supersedes the former all-purpose swallowed-boundary advice for **Spaces only**. Functional control zones and LV micro-channel boxes retain their dashed swallowed-boundary rule and do not acquire room-notch geometry. An owner section-count decision can override the default source-run counting convention for the stated project/scope; it does not establish a universal four-foot section length.

## Room geometry: no islands and no slits

Prefer a host footprint notched from an outer edge around an otherwise enclosed same-level Space. No hairline/zero-width slit is permitted: it is unusable for vertex editing. A live PDF Polygon supplies a single Vertices ring; do not attempt a second ring/hole. Where the accepted architecture supports it, wall-adjacent stairs/elevators/chases provide the notch edge. Under the owner-directed convention, extend an open-to-below footprint to the wall instead of floating it inside the host. Do not invent wall adjacency when source geometry contradicts it.

The notch may consume the connecting wall strip because wall thickness is not occupiable floor area. Record consumed strips and slivers in the geometry/area notes. Adopt owner-returned geometry wholesale first; any subsequently authorized notch normalization becomes an explicitly recorded review revision, not a silent edit to an accepted footprint. Never retain duplicate superseded footprints in the current deliverable; keep historical geometry in prior revisions.

Rare fallback: if no usable edge is reachable, retain the enclosed island and leave the host whole. Derive `Space.nested_in` from full containment in a larger Space on the same served level and registered coordinate frame; select the smallest containing host. Set null otherwise. Equal-footprint/ambiguous overlap and unknown-frame cases require review, not automatic nesting. Draw larger footprints first, smaller last. Retained nested Spaces receive a dashed border and a deeper shade of their own category color. A factor of 0.6 times category RGB is only a beta implementation placeholder, not a fixed owner color standard. Bring all labels in front after geometry.

## Area status and mandatory front-sheet note

Package 1 uses **Area sf (check only)** and **Nested in** columns. Retain measurement/source basis in model metadata and notes, rather than presenting polygon areas as a quantity takeoff. Markup polygon areas provide a cross-check and feel for scale; the owner performs real area takeoffs in CAD. A notched host excludes carved-out Spaces and consumed connector strips. A retained whole host includes its nested Spaces: do not sum host and nested areas. Geometry-derived check areas must not silently become verified engineering area inputs.

**Both Package 1 and Package 2 must include this note (or a complete equivalent):**

> Room footprints use editable single-ring polygons. Hosts are notched from an outer edge around carved-out Spaces; no hairline/zero-width slits. Open-to-below voids extend to the wall where owner-directed; consumed wall strips are recorded. Rare retained islands leave the host whole and are shown in front, dashed, and in a deeper category shade. Area sf (check only): polygon areas are scale cross-checks, not quantity takeoffs; owner CAD governs area takeoffs. Notched host areas exclude carved-out Spaces and connector strips. Retained host areas include nested Spaces; do not sum them. Light membership uses the smallest containing Space in the accepted served-level coordinate frame; presentation never changes membership.

The schedule exporter includes this note on both front sheets and in `takeoff_notes.csv`. It preserves original source area data in the model.

## Light membership and coordinate frame

A light belongs to the smallest accepted Space containing its assigned point on its **primary served level**, in the same registered coordinate frame. Preserve the source sheet/mounting level separately: a ceiling fixture serving a lower-level reception remains associated with that occupied Space even if depicted beside an upper-floor void. Void/background scope polygons are not occupied receiving Spaces. Boundary ties, absent containment, overlapping alternatives or frame uncertainty require review.

Membership is independent of presentation: notching, nesting, drawing order and shading do not themselves move lights or reassign their Space. Resolve containment using accepted physical geometry and keep the membership record stable while styling. If a geometry revision conflicts with recorded membership, flag reconciliation; do not silently rewrite the association. Outside/unassigned fixtures remain in a separate scope/exception register until resolved.

Owner-returned footprints replace prior footprints wholesale and establish the working page frame. Replot the package onto the returned sheet frame, even when it is an electrical sheet rather than the original architectural intake sheet. Do not transform back through an unverified sheet registration. Record sheet/page revision, crop, rotation and coordinate basis; register all light anchors to that frame before containment. Preserve original source anchors and document the transformation/decision separately.

## Live annotations and register gate

Every milestone plan markup must remain live, editable PDF annotations. Source plans and schedule pages may remain ordinary page content; newly delivered footprint/fill/symbol/label markup must not be baked into page content. Room footprints use `/Polygon` with `/Vertices`, `/IC`, `/CA` and stable `/NM`, including rectangular rooms. Light display labels use `/FreeText` with a nonempty `/AP` appearance stream and stable `/NM`. This supersedes earlier permission to retain `/Square` as the final room footprint subtype. No flattening or editing locks.

Ship an annotation register CSV mapping every delivered annotation `/NM` to its object ID and final PDF page, including **Nested in** (`nested_in`), exact `source_tag` and `assembly_id` where applicable. A schedule page offset must be reflected in the final 1-based plan page numbers. One object can have multiple annotations, each with its own stable ID.

Run `python -m generators.validate_markup_pdf package.pdf annotation_register.csv --plan-pages 3 4` using the actual plan-page numbers. It rejects a plan page with zero annotations, missing/duplicate identities, register/PDF mismatches, wrong footprint/label subtypes, invalid polygons, missing fills/opacity and missing FreeText appearances. A dummy annotation cannot make missing registered labels pass. This structural check complements rendered visual review and human edit/save/readback; it cannot detect markup painted into page content if that markup was also omitted from the register. Reconcile expected model coverage independently before acceptance.

**Compatibility evidence status:** owner-reported beta success: all 47 returned Polygon annotations retained `/NM` and readable edited vertices after Bluebeam edit/save/readback. This closes the previously unproven polygon identity/geometry contract for that tested workflow. It is not a claim that this framework independently inspected the project PDF, nor proof for all viewers, FreeText appearance behavior or final optional-content layers. Preserve the evidence in the private project registers and continue per-deliverable checks. Automated notch authoring and full PDF plan generation are not supplied by the new validator.

## Owner section-count override and assembly identity

When the owner directs physical-section counting, each supported straight or curved physical section is a separate Light Object, even when joined into a continuous-looking assembly. Curved corners are first-class lights with their own source-defined type. Visible joints, exact plan tags and schedule evidence establish the breakdown. An approximately four-foot section is an interpretation awaiting a verified length basis, not a dimension to populate as fact. Keep length and section wattage null while their basis is unverified.

Record the dated owner decision, affected scope/IDs and superseded source-run interpretation. Set `count_basis=physical_section` and `count_decision_id` to a confirmed decision; preserve stable identities and label history through the split. Each section carries the same `assembly_id` where appropriate. The assembly is addressable as a system but is not an extra physical light or additive wattage/count. Keep the default same-type source-run convention for scopes without this override.

## Exact plan tags, schedule mappings and keynote-only types

Each Light Object retains exact `source.source_tag` and existing `source.source_annotation_id`, separately from its referenced Fixture Type's `source_mark`. An unexplained suffix is not a safe normalization: preserve it and mark `schedule_match_status=provisional` until owner/design-team resolution. Keep affected counts provisional; a project can continue supported unaffected intake. Mixed-tag rings retain assembly relationships and separate typed sections.

A luminaire defined only by a keynote receives its own fixture type with `schedule_presence=keynote_only`; its light mapping uses `not_on_schedule`. Preserve the keyed description/model and source locator; wattage and voltage remain null unless separately evidenced. Do not invent specs from a product name or fold the type into a similar scheduled fixture. Source references, type records and notes retain the full evidence without manufacturing a schedule row.

## Exterior holdouts

Exterior fixtures lacking a served Space are held out of the active takeoff with exact observed mark, quantity, source location, reason and unresolved disposition in the scope/exception register. Do not delete their observation, force-assign an interior Space or count them as accepted takeoff. Reconcile accepted counts plus explicit holdouts against observed source totals. Wine/burgundy exterior map color establishes no scope/control/equipment decision. See the unresolved exterior item in the workflow map.

## Anonymized owner-reported beta precedent

A returned upper-level host rectangle enclosed a stair, elevator and open-to-below region. A notch from the accepted east edge changed 4 vertices to 14 and the check area from 4,019.8 to 3,554.1 sf. Removed regions were reported as 149.8, 110.2 and 168.1 sf, plus approximately 31 sf of connector wall strip and 6 sf of edge slivers. These component figures are approximate and do not exactly reconcile the 465.7 sf difference; retain the recorded geometry as the check basis rather than adjusting numbers to force agreement. No light moved. This is an anonymized owner-reported example, not a reusable geometry template or independently verified CAD quantity.

## Implemented metadata and limits

`lighting-project-v0.8` adds Space nesting, exact plan tag/mapping status, assembly ID, count basis/decision and fixture schedule presence. Upgrade preserves existing data and sets new unknown values without inference. Existing versions remain supported. Geometry helpers derive full containment and smallest-Space proposals in explicit frames without mutating model membership; invalid single rings/zero-width slits fail, while practical finite notch widths still need owner visual review. These additions do not implement the separate pending EPS fixture-aggregator topology.
