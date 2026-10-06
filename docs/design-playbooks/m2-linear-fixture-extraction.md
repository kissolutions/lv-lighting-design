---
title: "M2 Linear Lighting Run Extraction"
page_type: playbook
page_status: draft
confidence_level: medium
domain_primary: low-voltage-lighting
ai_role: prescriptive_standard
invocation_triggers:
  systems_present: [low_voltage_lighting]
decision_axes: [run_continuity, source_type, physical_quantity, length_basis, electrical_topology]
related_pages:
  - "lighting-design-playbook.md"
  - "m2-fixture-numbering.md"
  - "../concepts/fixture-identity-and-summary-counts.md"
  - "../ontology/canonical-model/light-object.md"
  - "../../templates/m2-user-review-checklist.md"
---

# M2 Linear Lighting Run Extraction


## M2 Source Fixture Schedule Gate

**Extract the MEP lighting fixture schedule as referenced source design information before committing fixture counts, type identity, or linear/curved continuity interpretations.** Schedule-first applies to physical Milestone 2, not only later LV fixture selection or electrical design. Keep the original schedule separate from the proposed LV replacement schedule.

Capture every source type mark exactly (including suffixes such as L4 versus L4A), its description, manufacturer/model if given, mounting/form, lengths/dimensions/geometry, section or assembly details, wattage and its basis, voltage/driver information when stated, options/emergency variants, keyed notes and detail references. Preserve blank/unknown entries and conflicting descriptions; do not invent missing specifications. Retain schedule sheet/page/revision and row/note source locators. Reconcile source types to every affected Light Object and to the schedule front sheet.

If a schedule is referenced but not yet found or extracted, register that omission and retrieve/review it before finalizing affected counts. If no schedule exists or was supplied (including design-build work), record that fact and available evidence instead of fabricating one. Supported takeoff can proceed provisionally from RCP/plans/legends/details, with unresolved type/assembly/count/load questions identified for owner review. “Design-build” does not automatically mean the schedule is absent.

### Evidence Reconciliation for Rings, Curves and Mixed Tags

A visually continuous ring, perimeter or linear path is **not proof of one physical fixture**. Reconcile all available sources together:

- Architectural/lighting RCP: actual luminous paths, visible gaps/joints, segment boundaries, shape, dimensions and type-label associations.
- MEP fixture schedule: distinct type descriptions and variants, specified pieces/lengths, assembly/ring definitions, driver/feed information, referenced details and manufacturer configurations where supplied.
- Electrical lighting plan: symbols, circuit assignments, wiring/daisy-chain depiction, separate connection points, keyed notes and control/emergency distinctions. Wiring joins do not themselves prove physical luminous continuity; one circuit may serve several discrete fixtures.

For a circular-looking assembly tagged **L4 and L4A**, extract both schedule rows first and determine whether they describe separate luminaires/segments, variants of an assembly, an emergency/control distinction, or a source discrepancy. Preserve both tags and locators. Do not merge them into one same-type run simply because their geometry touches, and do not infer piece quantity from the number of printed tags or circuiting strokes alone.

Use the source-supported result: separate physical fixtures/independent typed sections receive separate takeoff occurrences; a documented continuous system retains its source-run/assembly identity with any supported section breakdown recorded separately. A ring assembly and its component pieces are distinct quantity views, not additive fixture counts. For mixed-type assemblies, retain an assembly/group relationship in the review register and count each established typed occurrence once; do not duplicate the whole ring under both L4 and L4A. If that relationship exceeds the current Light Object representation, retain the referenced breakdown in the review record rather than inventing a schema field or losing the distinct source types.

Record the reconciled counting decision, schedule/RCP/circuiting evidence, known versus unknown physical sections/feeds and affected IDs in the discrepancy/review register. Missing or conflicting decisive evidence keeps the affected count provisional; ask a focused owner question. The schedule can resolve continuity but is not assumed definitive when its description is incomplete or conflicts with the drawing. Complete this pass before accepting the affected M2 counts and propagating them into numbered PDFs and summaries.

## Counting Convention

**After the source fixture schedule and relevant RCP/electrical evidence are reconciled, count one explicitly or apparently continuous linear lighting path of the same Fixture Schedule Type as one source run.** This includes straight runs, connected corners, multiple turns, U-shaped paths and closed perimeter loops. Repeated fixture-type labels along the path, including labels beyond a 90-degree turn, do not alone create additional occurrences. An apparently continuous run may be recorded as one provisional run when continuity is ambiguous; retain the ambiguity for review rather than silently asserting verified physical continuity.

**Count clearly separated or unconnected lighting paths as distinct runs**, even when they share the same type mark or occur in the same room. An explicit source designation of independent fixture runs also takes precedence over an apparent continuous line. A manufacturer section joint or connector within a continuous run does not alone increase the source-run count; retain its hardware breakdown separately. Preserve supported distinct schedule types rather than combining them into one typed occurrence. A change of direction alone is not a break.

This is an M2 source-takeoff convention. One run count does not establish one manufactured luminaire, one purchasable section, one feed, one driver, one power channel or a verified electrically continuous assembly. Clearly identify the linear quantities as runs in review descriptions/registers so they are not mistaken for a hardware piece count. Use the same convention across the fixture-ID PDF, Room/Lighting by Space summaries, Fixture-Type Schedule and Light Points.

## Follow the Source Path

1. Complete the source fixture schedule gate above, then identify the lighting symbol/line convention and actual schedule type from the source legend/schedule. Distinguish lighting type marks from architectural ceiling-type annotations, detail references, dimensions and other text. Multiple matching marks are evidence of type association, not a count by themselves.
2. Trace the original lighting path, including corners, returns and any closing segment. Inspect the source background with colored fixture-ID overlays hidden or removed from a review copy where needed; an annotation must not bridge or conceal a source break. Consult details/elevations where plan linework is unclear.
3. Separate clearly independent paths. Conversely, a dashed depiction or interruption by a label, symbol or overlaid annotation does not automatically prove a physical break. Establish the source convention or flag continuity. Do not invent a universal gap-distance threshold or connect visibly separate runs merely because they are close.
4. Give each resulting run one permanent Light Object ID and one display label under [M2 numbering](m2-fixture-numbering.md). Preserve every relevant type-label/segment locator as evidence for that occurrence. A corner or repeated mark does not receive a second ID. A room boundary alone does not duplicate a run; retain one primary served Space and flag genuinely shared/uncertain service for review.
5. Record the observed continuity basis, counting basis and any unresolved source ambiguity in supported source references, markup comments/registers and project review notes. The initial source-run interpretation remains distinguishable from a later confirmed manufacturing or electrical breakdown.

## Length and Load

Measure the full lighting path with a verified scale and source geometry. Add each unique straight segment once; include supported curved or closing portions. Do not use a run's bounding-box width, perimeter-room dimensions or a count of printed labels as its length. Shared corner vertices do not add extra segment length. Unknown or obscured geometry/scale leaves length unknown or explicitly provisional.

Use the supported load basis: per foot, per reference length or per fixture/section as established by the schedule/product evidence. Do not assume watts per foot merely because the symbol is linear. For a verified per-foot basis, total run load is verified length multiplied by verified watts per foot; include supported product-specific allowances/auxiliary loads separately where applicable. Original source AC watts and selected LV channel-interface loads remain separate. Do not calculate a final load from an unverified length or inferred product rate.

## Later Electrical and Hardware Resolution

Retain source run identity when resolving product section lengths, connectors, drivers, feeds, emergency portions and independent control requirements. Multiple feeds or a load exceeding a selected output limit require supported segmentation/topology and engineering review; the single source-run count does not grant permission to assign the entire path to one channel.

The present canonical Light Object models a single-input selected occurrence. A source run with unresolved feed/segment topology can remain at physical intake with unconfirmed electrical selections. Do not duplicate the full run and load to work around that contract. Supported split-input/segment modeling and its physical-run-to-section relationship require an explicit versioned extension or a separately reviewed implementation record until supported. Source takeoff counts and later hardware section/feed counts remain reconciled, distinct views.

## M2 Review and Corrections

Review the run path, type associations, separation/continuity interpretation, primary served Space and display-label mapping. Confirm whether each quantity is a discrete fixture or a linear run. Record uncertain continuity, source-directed sectional divisions and missing length/load/topology information in the discrepancy list with the affected ID and next action.

A documented apparently continuous candidate can carry forward as a provisional source-run interpretation; it is not a verified hardware quantity or final electrical design. A clearly missed separate run, duplicated path or unresolved counting disagreement keeps the affected intake scope pending correction/review. Do not hide ambiguity solely to make type-block totals or a milestone pass.

If later evidence changes one run into several, or several into one, preserve the earlier geometry/count basis and label history. Reconcile permanent-ID dispositions and any new occurrences; update every affected count, label map and markup in one review revision. Do not silently replace accepted owner corrections. No default lighting zone follows from this counting decision.

Owner: KIS Solutions. October 2026; owner-directed source-run counting convention. Automated continuity tracing, section/feed derivation and PDF generation remain unimplemented.
