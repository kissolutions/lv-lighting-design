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

Type-and-quantity intake is useful before individual grouping, but cannot identify which light moved to another channel, which subset is in a daylight zone, or which emergency fixture requires a distinct response. Coarse counts remain preliminary evidence until reconciled with physical occurrences. There is no bulk-count object in the current design schema.

Keep drawings readable with room/zone/channel labels and grouped counts. Add per-fixture labels where commissioning, troubleshooting, special selection, or ambiguity makes them useful. Preserve a source locator or reviewed geometry even when the identifier is hidden; automated fixture-center detection and overlays remain future work.

IDs stay stable through regrouping, equipment reassignment, room renaming, and unchanged source revisions. A background revision requires reconciliation: retain matched occurrences, issue new IDs for new lights, and record removals in the future source-disposition workflow. Changed/ambiguous geometry requires review. Identity is persistent, not a promise that an early takeoff is permanently correct.

Linear/segmented fixtures, multiple feeds, and several control inputs require deliberate topology extensions. Owner: KIS Solutions; October 2026; draft.
