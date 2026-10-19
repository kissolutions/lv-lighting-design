---
title: "M4 Microchannel Chain-Line Markup and Owner Return"
page_type: playbook
page_status: draft
domain_primary: low-voltage-lighting
ai_role: prescriptive_standard
---

# M4 Microchannel Chain-Line Markup and Owner Return — Y6

**Owner directive, 2026-10-18:** Show editable **chain lines** through Light Points, not overlapping boxes. This is a physical *markup and review* convention; an electrical Class 2 channel with multiple fixtures is **always parallel**, even when its physical two-wire distribution is daisy-chained. Chain lines illustrate connection order, not a surveyed cable route, final conductor length, or a series LED string.

## Package 4: markup contract

1. Each channel with two or more assigned Light Points has exactly one editable `/PolyLine` passing through the member Light Point anchors, in intended chain order, on the `lv_channels` layer. Single-light channels do not need a chain line. Do not use bounding boxes as the primary representation.
2. Show the microchannel's persistent ID in review registers. Label each Light Point with its assigned `<QDCD tag>:CH<output>` when the physical assignment is known. Keep its label editable, and do not invent an assignment if unknown.
3. Show a separate editable **reach line** on the `controllers` layer from the assigned QDCD/output toward its assigned chain, indicating the intended feed-entry Light Point. The reach line is an assignment and entry-location indicator, not a claim of surveyed cabling.
4. Keep zone boundaries, wiring and output ownership separately validated. An owner may move a reach line between two **unchanged** chains to swap their QDCD outputs.
5. Preserve original annot IDs, source page identity, layers and owner-returned locations. Capture accepted PDF/save/readback verification before changing the canonical model.

## Owner chain-return algorithm (required behaviors)

Use the *accepted baseline* register to match every returned chain/reach annotation to its stable identity. A changed shape alone never proves an engineering assignment without its registered IDs.

- **Snap** every chain vertex to its nearest Light Point anchor, using a tolerance calibrated to the actual symbol size, page scale and minimum fixture separation. The Timmons field test accepted **≤8 pt**, provided the second-closest Light Point was **≥15 pt away**; its minimum Light Point spacing was **17.1 pt**. These are *project-tested values, not universal constants*. Ambiguous snaps must block automatic acceptance. Verify no impossible duplicate vertices.
- **Membership and ordering:** the snapped vertex sequence defines membership and intended physical daisy-chain order. A light belonging to two returned chains is rejected. A light omitted from all returned chains becomes a proposed one-light channel, then receives the same zone/electrical/assignment validation as any other output; do not silently lose it.
- **Reach-line interpretation:** independently evaluate every changed reach line, including those attached to otherwise unchanged chains. It identifies the physical QDCD output and the feed-entry Light Point. Changing a reach line may trigger output reassignment and DC feed changes.
- **Candidate output allocation:** when no explicit owner moved reach line resolves the output, assign changed chains via **minimum-cost matching**, prioritizing retaining the same output, then the same QDCD, then a QDCD serving the same room. A first-fit or greedy overlap selection may create unnecessary cross-device feeds. Do not silently reassign already accepted unedited channels.
- **Diff tolerance:** Bluebeam can rewrite unedited floating-point coordinates when re-saving. Use a meaningful geometric change tolerance **at least 0.5 pt**, and require exact stable ID/page/layer matching. Treat minor round-trip coordinate noise differently from an intentional moved vertex or line.
- **Electrical revalidation:** before accepting changed membership/outputs, rerun independent-zone ownership, fixture-to-channel voltage/mode/compatibility, **95 W** maximum, CC aggregate branch current and hardware operating limits, unique controller output ownership, PDU-to-QDCD feed capacity and relevant safety/emergency controls. Manufacturer evidence remains a separate approval gate; owner-drawn geometry does not establish electrical qualification.
- **Physical identity:** maintain immutable Light Point IDs and an explicit old-channel-to-new-channel **crosswalk**. Timmons derives the revised channel ID from the lowest carried Light Point; it must detect collisions, preserve accepted history and never overwrite another existing channel silently. A future project may specify another documented deterministic policy.
- **Handoff to M5:** carry ordered members and `feed_entry_light_id` as first-class information in a **versioned project markup/routing companion** until the canonical model has dedicated fields. Do not write undocumented properties into the strict v0.9/v0.10 channel schema or claim the framework PDF tooling implements the project-specific Bluebeam parser.

## Review output

Report before/after per-channel member IDs, physical chain order, assigned output, feed-entry point, renamed/crosswalk IDs, electrical checks, manual ambiguity exceptions, and whether accepted PDF annotation IDs and owner approvals were preserved.

**Evidence:** Timmons M4-R5/R6 owner returned polylines and reach lines were reconciled and tested by the project agent. The actual project-specific `chain_return.py` and Bluebeam operations are **not** implemented by this framework repository; they establish a validated handoff pattern to promote into a reusable generator later. Do not alter the accepted project solely because this doctrine is recorded.
