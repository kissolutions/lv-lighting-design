# Synthetic Device Hierarchy v0.2

These are synthetic software test examples. No real client, manufacturer, or source plan is represented.

- [lighting-model.json](lighting-model.json): two power channels, two LV zones, one four-output controller. Zone A spans both channels; Channel 1 supplies both zones. Derived total light load is 75 W without double-counting.
- [emergency-model.json](emergency-model.json): the same topology, with Zone B off during normal operation and forced on by a confirmed normal-power-loss input during outage. Separate backup declarations keep the lighting and controller supplied.

From the repository root:

```bash
python -m generators.model_hierarchy docs/reference-implementations/synthetic-hierarchy/lighting-model.json
python -m generators.model_hierarchy docs/reference-implementations/synthetic-hierarchy/emergency-model.json
python -m unittest discover -s tests -v
```

The CLI emits a JSON issue report and derived load/reference views. Unknown loads remain `null`; Decimal load results are serialized as exact strings. It does not invoke the v0.1 CSV exporter or a PDF writer. Passing synthetic checks is not a project engineering approval.
