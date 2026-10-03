# Synthetic Space Examples

Draft 0.3.1 regression tests additionally cover upper-sheet lights serving a lower-floor Space, optional mounting height/evidence, two Spaces sharing one named zone, an unlit stair level referencing overhead lighting without duplicate lights, and an unnumbered inventory-only service enclosure. These are synthetic engineering-data cases, not project or code precedent. Existing example JSON remains 0.3.0 to exercise backward compatibility.

These invented v0.3 examples extend the synthetic v0.2 topology; they contain no client data or real code approval. Two Spaces reference three existing lights. One Space spans two channels, and a channel supplies both Spaces. Counts and wattages are derived without duplicating lights.

The room-default zones have stable IDs and null visible labels. Tests cover named labels such as `$z109`, code-classification separation, daylight geometry versus control applicability, and room/reference consistency.

Run `python -m generators.model_spaces docs/reference-implementations/synthetic-spaces/lighting-model.json` and the analogous `emergency-model.json` command. The latter retains the separate outage signal and backup supply from the synthetic hierarchy example.
