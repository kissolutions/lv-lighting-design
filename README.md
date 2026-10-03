# LV Lighting Design

KIS Solutions' LV lighting implementation workspace. WikiJS owns the general electrical lighting workflow and design knowledge. This repository extracts/reconciles the MEP scheme, checks it through that knowledgebase, and records the LV model, grouping, validation and markup/output conventions.

The current draft is [Space context v0.3](docs/ontology/canonical-model/space-context-v0.3.md), extending the [v0.2 device hierarchy](docs/ontology/canonical-model/device-hierarchy-v0.2.md). It adds room conditions, independent building-code and energy-code classifications, code-basis evidence, and references to existing lights and zones. Use the [v0.3 schema](schemas/lighting-project-v0.3.schema.json), [seed](templates/lighting-project-v0.3.template.json), and [synthetic examples](docs/reference-implementations/synthetic-spaces/README.md). Fixture quantities are derived from stable internal light IDs; drawing labels are optional. The v0.2 checker and original v0.1 tools remain available for their respective contracts.

The current path is **architectural inventory -> lighting/control source intake -> check MEP intent through WikiJS -> compatible LV implementation -> zones/controllers/channels -> review markups -> coordinated issue -> field changes, commissioning and as-built reconciliation**. Follow the [workflow and readiness map](docs/design-playbooks/lv-project-workflow-and-readiness.md) for outputs, six review milestones, implemented capabilities and remaining development. Redesign is conditional on authority and approval; source ambiguity is not resolved by inventing controls.

The model and documented method are sufficient to attempt a supervised one-room/one-sheet review markup. PDF generation/edit/readback and native Bluebeam Area behavior still need a practical proof. Room/boundary markups can precede final electrical assignments; the current checker includes later engineering requirements and is not an early room-inventory gate. Follow [architectural intake](docs/design-playbooks/architectural-space-intake.md) for independent no-assumptions room verification, source areas/scales, owner corrections, served levels and source discrepancies. The two agreed zone-review status attributes are documented but have not been added to the schemas/generators.

## Start here

WikiJS owns room definitions, code analysis, controls selection/configuration, decision trees and the application guide. Local [application-guide](docs/design-playbooks/lighting-control-application-guide.md) and [IECC profile](docs/design-playbooks/iecc-occupant-sensor-directives.md) drafts are support material for alignment upstream, not a separate design authority.

1. Read [repository guidance](CLAUDE.md) and the [repository boundary](docs/governance-and-doctrine/repository-boundary.md).
2. Follow the [Lighting Design Playbook](docs/design-playbooks/lighting-design-playbook.md).
3. Use the [current model overview](docs/ontology/canonical-model/space-context-v0.3.md), [v0.3 schema](schemas/lighting-project-v0.3.schema.json), and [project template](templates/lighting-project-v0.3.template.json).
4. Review the [current synthetic examples](docs/reference-implementations/synthetic-spaces/README.md). They contain no client data.
5. Use the [first-project checklist](templates/first-project-checklist.md) to stress-test the foundation.

## Legacy v0.1 working rules

- Preserve source facts independently from LV design decisions and generated views.
- Use a 90 W design ceiling for this baseline's nominal 100 W channels; a verified lower product limit governs when applicable.
- Include each fixture exactly once, or explicitly exclude it with a documented reason.
- Preserve required room/control micro-zones. Check compatibility before combining loads.
- Unknown LV wattage, unclear controls, unresolved blocking items, and unknown node capacity block quantified design checks.
- Keep real plans, client takeoffs, markups, and project models in approved project storage outside Git. A public repository is not a project archive.

## Run the current checker

```bash
python -m generators.model_spaces PATH_TO_V03_MODEL
```

This emits checks and derived JSON for the current model. It does not extract plans, evaluate the complete code/application guide, generate editable PDF markups, or export v0.3 schedules.

## Run the legacy v0.1 tools

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
