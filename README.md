# LV Lighting Design

KIS Solutions' low-voltage lighting design domain extension. It owns the reusable design method, canonical lighting model, grouping rules, validation, and generated-review conventions.

The current device-model discussion is captured in the [v0.2 hierarchy draft](docs/ontology/canonical-model/device-hierarchy-v0.2.md). It separates power channels from LV light zones, nests power units under HV branches, and adds explicit emergency operation/signaling. Use its [schema](schemas/lighting-project-v0.2.schema.json), [seed](templates/lighting-project-v0.2.template.json), and [synthetic examples](docs/reference-implementations/synthetic-hierarchy/README.md). The original v0.1 tools below remain a runnable legacy baseline; they cannot express the new many-to-many hierarchy.

The Phase 1 path is **source intake -> fixture takeoff -> canonical model -> LV selection and grouping -> validation -> review schedules and component quantities**. Phase 2 adds professional PDF markup and routing after the model is tested on real work.

## Start here

1. Read [repository guidance](CLAUDE.md) and the [repository boundary](docs/governance-and-doctrine/repository-boundary.md).
2. Follow the [Lighting Design Playbook](docs/design-playbooks/lighting-design-playbook.md).
3. Use the [model overview](docs/ontology/canonical-model/README.md), [schema](schemas/lighting-project.schema.json), and [project template](templates/lighting-project.template.json).
4. Review the [synthetic example](docs/reference-implementations/synthetic-room/README.md). It contains no client data.
5. Use the [first-project checklist](templates/first-project-checklist.md) to stress-test the foundation.

## Legacy v0.1 working rules

- Preserve source facts independently from LV design decisions and generated views.
- Use a 90 W design ceiling for this baseline's nominal 100 W channels; a verified lower product limit governs when applicable.
- Include each fixture exactly once, or explicitly exclude it with a documented reason.
- Preserve required room/control micro-zones. Check compatibility before combining loads.
- Unknown LV wattage, unclear controls, unresolved blocking items, and unknown node capacity block quantified design checks.
- Keep real plans, client takeoffs, markups, and project models in approved project storage outside Git. A public repository is not a project archive.

## Run the Phase 1 tools

Requires Python 3.10+ and the dependency in `requirements.txt`. From this repository root:

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python -m generators.validate_model docs/reference-implementations/synthetic-room/lighting-model.json
python -m generators.export_review docs/reference-implementations/synthetic-room/lighting-model.json --output-dir outputs/demo-01
```

For real work, substitute a model path in approved project storage and put output there too. The export contains five CSVs and a validation report. `--allow-provisional` writes clearly labeled draft reviews and returns a failing status when engineering issues remain; structural/reference failures always prevent export.

Validation returns `0` when implemented checks pass, `1` for model issues, and `2` for unreadable input or a failed export. Passing checks is a data/design consistency result; engineering review is required before a project checkpoint or construction issue.

## Repository map

| Area | Owns |
|---|---|
| `docs/governance-and-doctrine/` | Boundary, page registry, framework relationships |
| `docs/ontology/canonical-model/` | Entity definitions and model contract |
| `docs/concepts/` | Grouping and load reasoning |
| `docs/design-playbooks/` | Reusable workflow and decision gates |
| `docs/product-classes/` | How product constraints enter the design |
| `docs/validation/` | Check definitions and checkpoint gates |
| `docs/reference-implementations/` | Synthetic worked references |
| `docs/historical-examples/` | Approved anonymized precedent policy |
| `templates/`, `schemas/` | Project seed and machine-readable contract |
| `generators/`, `tests/` | Validator, review exporter, regression cases |

Automatic PDF extraction, optimized grouping, PDF markup, cable lengths, and product-specific BOM selection are future work. See the [roadmap](docs/governance-and-doctrine/roadmap.md).
