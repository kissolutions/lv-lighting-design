---
title: "Fixture Identity and Room Quantity Summaries"
page_type: concept
page_status: draft
confidence_level: medium
domain_primary: low-voltage-lighting
ai_role: explanation
invocation_triggers:
  systems_present: [low_voltage_lighting]
decision_axes: [takeoff_granularity, assignment_traceability, drawing_legibility]
related_pages:
  - "../ontology/canonical-model/space-context-v0.3.md"
  - "../ontology/canonical-model/light-object.md"
---

# Fixture Identity and Room Quantity Summaries

Maintain one stable internal occurrence ID per physical light once grouping begins. Display room quantities by fixture type, e.g. a synthetic room with Type A x3 and Type AE x1. An occurrence establishes assignment/revision identity; a summary communicates quantity. Visible per-fixture labels are optional.

When labeling fixtures for M2, apply the [display-numbering playbook](../design-playbooks/m2-fixture-numbering.md): one global consecutive block per source Fixture Schedule Type, room subsets together, clockwise from top-left within each room/type. The Light Object's `label` is the display number; its permanent `id` remains the relationship/revision identity. Readable ordering complements room/type summaries without silently reassigning identities.

Type-and-quantity intake is useful before individual grouping, but cannot identify which light moved to another channel, which subset is in a daylight zone, or which emergency fixture requires a distinct response. Coarse counts remain preliminary evidence until reconciled with physical occurrences. There is no bulk-count object in the current design schema.

Keep drawings readable with room/zone/channel labels and grouped counts. Add per-fixture labels where commissioning, troubleshooting, special selection, or ambiguity makes them useful. Preserve a source locator or reviewed geometry even when the identifier is hidden; automated fixture-center detection and overlays remain future work.

IDs stay stable through regrouping, equipment reassignment, room renaming, and unchanged source revisions. A background revision requires reconciliation: retain matched occurrences, issue new IDs for new lights, and record removals in the future source-disposition workflow. Changed/ambiguous geometry requires review. Identity is persistent, not a promise that an early takeoff is permanently correct.

For linear lighting, follow [M2 source-run extraction](../design-playbooks/m2-linear-fixture-extraction.md): count one continuous/apparently continuous same-type path once, including turns and repeated marks; clearly separated paths are distinct runs. Describe linear quantities as runs, retain full-path length evidence and flag continuity ambiguity. A source run is not necessarily one manufactured section or one feed/channel. Linear/segmented fixtures, multiple feeds, and several control inputs still require deliberate topology extensions for electrical implementation. Owner: KIS Solutions; October 2026; draft.
