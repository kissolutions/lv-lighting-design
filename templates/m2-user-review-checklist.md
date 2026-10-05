# M2 — Lighting and Source Controls: Owner Review

**Goal:** Confirm that we captured the lights and control information shown in the source drawings accurately, with gaps and conflicts clearly identified.

Copy this checklist into project storage. The extraction/verification agents prepare the review package and perform the detailed reconciliation; the owner reviews the results and resolves questions. This is the human-readable companion to [M2 in the project checklist](first-project-checklist.md#m2-source-lighting-and-controls), not a separate milestone or a new design approval.

Project: __________  Review date: __________  Reviewer: __________

Drawing revision(s): __________  Review-package revision: __________

Rooms/sheets included in this review: __________

## Have These Open

- Source lighting/RCP plans, fixture schedule/legend, notes and available control details.
- Room Schedule, Fixture-Type/Lighting Schedule, Lighting by Space and Light Points.
- Fixture-ID review PDF and source-control observations, where provided.
- Discrepancy list and the independent verification summary.

Use matching revisions. Keep the markup documents separate for now. Missing review material should be identified before accepting the affected portion.

## 1. Did We Capture the Right Lights?

- [ ] The fixture-ID markup identifies the visible lights clearly; I can match each ID to its record.
- [ ] Display numbers follow the [numbering rule](../docs/design-playbooks/m2-fixture-numbering.md): one consecutive block per schedule type, each room's same-type lights together, clockwise from top-left. The type-block register matches the counts; unclear paths or revisions are flagged. Permanent internal IDs are preserved.
- [ ] Room/type counts agree with the marked plan and review tables. The verification summary identifies its checked sheets and remaining count questions.
- [ ] Lights are not counted twice because they appear on multiple plans. Existing, excluded and out-of-scope items have an explicit treatment.
- [ ] Linear lighting is described consistently as fixtures or runs. Uncertain lengths, label-to-fixture matches and counting conventions are flagged.

Questions / discrepancy IDs: __________

## 2. Are the Fixture Types Captured Correctly?

- [ ] Fixture marks match the source schedule/legend. Similar marks, suffixes and unresolved matches are preserved rather than silently combined.
- [ ] Available descriptions, wattages, driver/dimming information, options and notes were copied with their source references.
- [ ] Missing schedules or conflicting values are flagged. Unknown values stay blank/unknown, and original source wattages are not presented as confirmed LV loads.

Questions / discrepancy IDs: __________

## 3. Is Each Light in the Correct Room?

- [ ] Every light has one primary served room/Space. No lights are left unassigned or duplicated between rooms.
- [ ] Lights above a lower occupied floor belong to the room they illuminate; their actual source sheet is still recorded.
- [ ] Accepted M1 boundary corrections are preserved. Any new boundary or membership question is identified for review.
- [ ] Mounting heights have a stated basis. A ceiling tag was not automatically assigned to every fixture in a room, and unsupported heights remain unknown.

Questions / discrepancy IDs: __________

## 4. What Controls Did the Source Actually Specify?

Review these functions by room. The agent should show the source evidence or identify the gap; the owner does not need to reconstruct the entire scheme from scratch.

| Function | What to look for in the review |
|---|---|
| Dimming | Whether dimming is specified and any documented level/sequence |
| Manual controls | Switches, dimmers, overrides and the lights they operate |
| On/off behavior | Manual-on, automatic-on, partial-on and vacancy response, where specified |
| Occupancy/vacancy sensing | Depicted sensors, source groups and documented operation |
| Time switches | Schedules, time-control notes and documented overrides |
| Daylight / emergency | Applicable source notes, groups and interactions; unresolved behavior flagged |

- [ ] Source symbols and MEP group labels are preserved. Lighting controls are distinguished from receptacle controls.
- [ ] Each relevant function is identified as documented, ambiguous, missing or supported not applicable. Missing symbols alone were not treated as proof that a function is unnecessary.
- [ ] The agent checked available legends, notes, schedules, details and specifications before reporting no information; missing referenced documents are listed.
- [ ] Proposed controls or owner-directed additions are distinguished from source observations. Room type alone did not produce an invented control scheme or default zone.
- [ ] Emergency suffixes, battery notes and normal-operation observations are captured without claiming a complete emergency sequence where none is documented.

Questions / discrepancy IDs: __________

## 5. Are the Open Items Clear Enough to Move Forward?

- [ ] Every remaining question identifies the affected rooms/lights, source location, missing/conflicting information and next action.
- [ ] My corrections are recorded, with their basis, and the affected tables/markups have been reconciled before acceptance.
- [ ] The independent verification summary is available. A software pass alone has not been treated as proof that nothing was missed on the plan.

| Remaining issue | Effect on M2 |
|---|---|
| Missed/doubled fixtures, unreconciled counts or unresolved primary room assignments | Keep the affected intake scope pending correction/review |
| Source genuinely omits a wattage, mounting height or controls instruction | Can carry forward as a clearly recorded source gap; affected later design stays pending |
| Conflicting source documents | Preserve both observations; accept only reconciled observations or clearly identified unknowns for the stated scope |
| Code interpretation, final controls narrative, LV equipment choice or channel grouping | Reviewed in later steps; do not invent these merely to complete M2 |

M2 acceptance confirms source capture for the stated scope. It does not confirm code compliance, authorize filling missing controls or approve a construction design. Owner-confirmed room classifications, permission to develop a controls narrative and approval of the finished narrative are separate review decisions in [the M3 handoff](../docs/design-playbooks/lv-project-workflow-and-readiness.md#room-classification-and-controls-narrative-handoff).

## Review Decision

- [ ] **Accepted for the scope listed above**, with recorded source gaps/open items carried into the next review.
- [ ] **Partially accepted:** accepted rooms/sheets __________; pending scope __________.
- [ ] **Return for correction:** required changes __________.

Choose one decision. Record the accepted package revision, remaining discrepancy IDs and reviewer/date in the project review record. Subsequent source changes reopen the affected review; preserve the earlier acceptance history.

Remaining discrepancy IDs / next actions: __________

Reviewer and date: __________  Accepted package revision: __________
