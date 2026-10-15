# Synthetic bundle-tree v0.9 fixture

Synthetic only; no real project, product rating, or installation allowance.
`tables/*.csv` are the authoritative routing records; `lighting-model.json` is
the derived v0.9 integration example. Other lighting facts inherit the existing
synthetic milestone example. Never edit the routing JSON instead of the tables.

The upstream tree has three depths, one terminating controller per segment and
four physical cable jackets carrying five feed circuits. Counts fall 4 → 3 → 1
for cables and 3 → 2 → 1 for controllers. One separate output drop carries one
cable. Upstream cable centerline total is 80 ft, drop total 5 ft; neither is a
purchase quantity. No electrical routing suitability is claimed.

```bash
python -m generators.model_intake docs/reference-implementations/synthetic-bundles/lighting-model.json --phase intake
python -m unittest discover -s tests -p test_model_bundles.py -v
```

Tests cover cycle rejection with edge names, unique served-set IDs, separated
flows, multi-circuit cable counting, translation and fixed owner positions,
missing/unknown IDs, topology changes, assumptions, schema/migration, flat CSV
round-trip and model reference checks. The actual PDF/Bluebeam polyline return
is not established by these synthetic tests.
