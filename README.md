# LV Lighting Design

KIS Solutions' LV lighting implementation workspace. WikiJS owns the general electrical lighting workflow and design knowledge. This repository extracts/reconciles the MEP scheme, checks it through that knowledgebase, and records the LV model, grouping, validation and markup/output conventions.

The current draft is [Electrical interfaces v0.5](docs/ontology/canonical-model/electrical-interfaces-v0.5.md), retaining [physical intake v0.4](docs/ontology/canonical-model/physical-intake-v0.4.md). Store physical lights once with primary served Space membership; logical lighting zones come later and no default zones are created. Use the [v0.5 schema](schemas/lighting-project-v0.5.schema.json), [seed](templates/lighting-project-v0.5.template.json), and [synthetic examples](docs/reference-implementations/synthetic-voltage/README.md). Source voltage is a peer of source wattage, separate from selected LV input. Design checks include fixed-voltage, AC/DC, power-mode and single-input CC current/range compatibility. Older contracts/tools remain available; an older pass does not perform these new checks.

The current path is **architectural inventory -> lighting/control source intake -> check MEP intent through WikiJS -> compatible LV implementation -> zones/controllers/channels -> review markups -> coordinated issue -> field changes, commissioning and as-built reconciliation**. Follow the [workflow and readiness map](docs/design-playbooks/lv-project-workflow-and-readiness.md) for outputs, six review milestones, implemented capabilities and remaining development. Redesign is conditional on authority and approval; source ambiguity is not resolved by inventing controls.

The model and documented method are sufficient to attempt a supervised one-room/one-sheet review markup. PDF generation/edit/readback and native Bluebeam Area behavior still need a practical proof. Room/boundary markups can precede final electrical assignments; the current checker separates inventory/intake/design data phases; independent source and owner review still establish actual milestone acceptance. Follow [architectural intake](docs/design-playbooks/architectural-space-intake.md) for independent no-assumptions room verification, source areas/scales, owner corrections, served levels and source discrepancies. The two agreed zone-review status attributes are documented but have not been added to the schemas/generators.

## Start here

WikiJS owns room definitions, code analysis, controls selection/configuration, decision trees and the application guide. General [application-guide](https://github.com/kissolutions/knowledgebase_wikijs/blob/main/design-playbooks/lighting-control-application-guide.md) and [IECC draft profile](https://github.com/kissolutions/knowledgebase_wikijs/blob/main/design-playbooks/iecc-occupant-sensor-directives.md) content now lives there; the old local paths are navigation-only pointers. Follow the [classification/narrative handoff](docs/design-playbooks/lv-project-workflow-and-readiness.md#room-classification-and-controls-narrative-handoff) for owner-confirmed room types, authorized source-gap filling and reviewed primary-source fallback when WikiJS guidance is unfinished. Local system constraints narrow compatible selections while preserving required behavior.

1. Read [repository guidance](CLAUDE.md) and the [repository boundary](docs/governance-and-doctrine/repository-boundary.md).
2. Follow the [Lighting Design Playbook](docs/design-playbooks/lighting-design-playbook.md).
3. Use the [current model overview](docs/ontology/canonical-model/electrical-interfaces-v0.5.md), [v0.5 schema](schemas/lighting-project-v0.5.schema.json), and [project template](templates/lighting-project-v0.5.template.json).
4. Review the [current synthetic examples](docs/reference-implementations/synthetic-voltage/README.md). They contain no client data.
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
python -m generators.model_intake PATH_TO_V05_MODEL --phase intake
python -m generators.model_intake PATH_TO_V05_MODEL --phase design
python -m generators.export_intake PATH_TO_V05_MODEL --output-dir NEW_REVIEW_DIRECTORY --allow-provisional
```

This emits phase checks/derived JSON and repeatable Room, Fixture-Type, Lighting by Space, Light Points and Discrepancy CSVs. v0.4 and read-only v0.3 export remain supported with blank new electrical columns. Explicitly upgrade an existing model with `--upgrade-output NEW_PATH`; new source/selected electrical fields start unknown. It does not extract plans, evaluate the complete code/application guide, generate editable PDF markups, or import spreadsheet edits automatically.

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


## Controller, power and sensor allocation

[Placement workflow](docs/design-playbooks/controller-power-placement.md) · [Markup legend](docs/design-playbooks/control-system-markup-legend.md) · [Topology companion](docs/ontology/canonical-model/controller-power-topology-v1.md). Device knowledge/mini playbooks live in [WikiJS](https://github.com/kissolutions/knowledgebase_wikijs/blob/main/design-playbooks/smartdc-allocation-index.md).
