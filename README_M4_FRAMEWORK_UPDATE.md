# LV Lighting M4 Framework Update — 2026-10-05

This is a repo-root overlay/update bundle for `kissolutions/lv-lighting-design`.

## What it adds

- v0.6 electrical model derived from v0.5.
- AC/DC as a peer `power_type`, not embedded in numeric voltage.
- Numeric nominal/min/max voltage retained explicitly; min/max are first-class for CC interfaces.
- Selected fixture `dimming_capability` kept separate from zone-applied dimming behavior.
- Reference rule: a dimmable 36 VDC CC C1 fixture remains physically C1 in an on/off-only Alcove zone.
- Micro LV Control Channel contract: one functional zone per channel; one zone may have many channels; one physical controller/output claim per micro channel when assigned.
- New M4 Class 2 profile: 100 W rated / 95 W maximum design load. Legacy 90 W profile remains intact.
- New design checks for power type, CV/CC, voltage/current/range, fixture capability, channel-zone ownership, and duplicate physical output claims.
- Exporter peer columns: `source_power_type` and `lv_input_power_type` while legacy v0.5 aliases remain available during transition.

## Apply

1. Extract/copy this ZIP into the root of the existing `lv-lighting-design` checkout, preserving paths. Do not replace `.git`.
2. Run:

   `python tools/apply_m4_framework_update.py`

3. Run the repository test suite:

   `python -m unittest discover -s tests`

4. Review the resulting diff and Git Sync/commit in the normal workflow.

The update creates `schemas/lighting-project-v0.6.schema.json` and `templates/lighting-project-v0.6.template.json`; it does not delete v0.5.

## Important migration behavior

`upgrade_v06()` converts v0.5 embedded `voltage.current_type` values into peer `source_power_type`, `input_power_type`, and `output_power_type` fields without changing numeric voltage. Newly introduced dimming-capability and micro-channel ownership/output fields remain unknown until reviewed rather than being guessed.

## Review targets

Before accepting the update on the YMCA project, confirm the active agent populates C1 as its actual selected 36 VDC CC interface and treats the Alcove's lack of a dimming requirement only as an applied-control decision. The grouping pass must not mutate C1 into 48 VDC or another physical fixture definition to simplify channel assignment.
