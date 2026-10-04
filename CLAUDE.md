# Agent Guidance - LV Lighting Design

Applies to Claude, Codex, and other agents working in this repository.

## Parent framework

Use `kissolutions/knowledgebase_wikijs` as the main general electrical engineering knowledgebase and the authority for shared taxonomy, metadata, templates, vocabulary, physical device facts, room-by-room lighting energy-code analysis, sensor/switch/controller selection and configuration, decision trees, and the lighting application guide. If it is available as a sibling checkout, read it there; otherwise use the connected repository. The current verified entry points are:

- [AI Agent Framework Guide](https://github.com/kissolutions/knowledgebase_wikijs/blob/main/AI/AGENT-FRAMEWORK-GUIDE.md)
- [Framework Extension Doctrine](https://github.com/kissolutions/knowledgebase_wikijs/blob/main/governance-and-doctrine/framework-extension-doctrine.md)
- [Knowledge Model Map](https://github.com/kissolutions/knowledgebase_wikijs/blob/main/governance-and-doctrine/map-knowledge-model-structure.md)
- [Definitions](https://github.com/kissolutions/knowledgebase_wikijs/blob/main/governance-and-doctrine/definitions.md)
- [Templates](https://github.com/kissolutions/knowledgebase_wikijs/tree/main/templates)

Keep links to shared knowledge rather than duplicating it. Propose generic framework improvements upstream; do not edit the parent to accommodate this implementation. If retrieval is unavailable, state the limitation and use only the verified local guidance; do not claim to have reviewed current upstream content.

## Repository authority

This extension owns LV project extraction/reconciliation, the canonical project model, LV implementation and channel/grouping rules, spatial conventions, validation, markup conventions, and generators. General electrical lighting design knowledge remains in WikiJS. Follow the [full workflow and readiness map](docs/design-playbooks/lv-project-workflow-and-readiness.md). Read the [boundary](docs/governance-and-doctrine/repository-boundary.md), [page registry](docs/governance-and-doctrine/page-type-registry.md), [playbook](docs/design-playbooks/lighting-design-playbook.md), and [model overview](docs/ontology/canonical-model/README.md) before changing these interfaces.

Knowledge structure follows meaning; workflow lives in playbooks. Do not import BAS I/O, PLC/controller, or controls-narrative ontology unless a specific cross-domain need is established.

## Engineering invariants

Start room extraction with the Architectural Floor Plan or Dimension Plan and follow [architectural space intake](docs/design-playbooks/architectural-space-intake.md). Compare architectural floor, architectural RCP, and electrical room labels; record mismatches in the discrepancy list. Assign lights by their primary served Space/occupied level, preserve the fixture source sheet separately, and put mounting height/basis on the Light Object. Describe consequential partial-wall/open boundaries and request review before finalizing uncertain zoning; do not require a wall object catalog. Include unnumbered chases/service voids with location/purpose notes. Preserve the MEP stair-control scheme. One shared zone per physical stair is a reviewed implementation convention only when source behavior and independent-control constraints support it; retain one Space or separate level records without duplicating lights.

Apply [Milestone 1](docs/design-playbooks/architectural-space-intake.md#milestone-1-room-inventory-and-source-verification): independently verify the simple room list first, flag omissions for owner review and cause analysis, then verify other source facts. No assumptions are permitted in asserted source facts; each fact needs source evidence or identified owner confirmation, and unsupported values stay unknown. For boundary review, follow walls for enclosed rooms and draw visibly provisional logical-area polygons using architectural use/circulation, partial walls, finish/material transitions, features and ceiling evidence. Approximate geometry is permitted for owner editing, without inventing source names, room use or code/control conclusions. Follow the [annotation naming and identity convention](docs/design-playbooks/architectural-space-intake.md#annotation-type-naming-and-identity): room name in Subject, Space ID/basis in Comments, actual author, and a persistent annotation ID mapped to the Space. Capture clear architectural area labels with high confidence. Prefer floor/dimension-plan boundary markups, otherwise the applicable RCP, and use the printed view scale as the preferred dimension source. Preserve editable, unflattened annotations and Space IDs through the owner's PDF correction/return loop. Native Bluebeam Area output requires a successful compatibility test before being promised. Apply the untagged-area rules: an untagged door alcove belongs to its surrounding Space; a traffic corridor is its own proposed tracking Space; finish transitions can split corridor tracking. Fixture layout never sets a boundary. Inspect finish plans and confirm substantial shaded/hatched scope exclusions during registration/intake; excluded backgrounds need only a retained scope note. Verify saved raw annotation IDs and a human edit/save/readback, not an unchanged-file round trip.

For current work, read [Physical intake v0.4](docs/ontology/canonical-model/physical-intake-v0.4.md) and its [v0.2 device hierarchy](docs/ontology/canonical-model/device-hierarchy-v0.2.md). Start with architectural room facts and extract the specified MEP lighting/control scheme from all relevant plans, legends, schedules, notes, and details. Check that scheme through WikiJS using the reviewed energy-code basis; preserve source intent separately from findings and LV implementation. Do not invent controls to fill missing information. Group channels within verified electrical limits while preserving source/approved operation. Redesign only with established authority and documented approval of the departure. Building Code Space Type, Building Code Occupancy Group, and Energy Code Space Type are independent fields; preserve unknowns and classification decisions. Store physical lights once in root `light_objects[]`; every light must have exactly one primary served Space after boundary derivation/counting. This is a primary intake sanity check. Zones later reference lights by ID. Create no default/placeholder zones during room or fixture intake; empty zone lists are valid. Establish functional zones only from supported control intent/reviewed decisions, and flag missing assignments at the later design phase.

The owner has superseded the v0.1 one-zone-per-power-channel restriction: v0.4 separates physical light ownership from later zone ID lists, each single-input light references one power channel, and many-to-many channel/zone views are derived. Branch circuits own power units and power units own channels. Controller output identity is separate from supply-channel identity. Preserve shared source schedule groups, normal operating state, emergency force-on inputs, and separate backup power provisions. Use class-specific output profiles rather than globally imposing 100/90 W or 0-56 V limits. The original invariants below describe the narrower v0.1 tools, which remain available until migration is complete.

Use WikiJS for general room/control design knowledge. The local [application-guide draft](docs/design-playbooks/lighting-control-application-guide.md) and [IECC profiles](docs/design-playbooks/iecc-occupant-sensor-directives.md) are staging/support material for alignment upstream, not independent design authority. Apply supported guide/code rules as checks on extracted MEP intent; use them to develop alternatives only when redesign is authorized. Keep independent control zones, physical sensor counts, and supply channels distinct. Do not infer adoption, room use, exceptions, or coverage. The owner-agreed zone verification and implementation-review statuses are documented in the [workflow map](docs/design-playbooks/lv-project-workflow-and-readiness.md#control-review-results) but are not yet schema fields. Retain findings/evidence in project review records until a versioned extension is implemented.

- Facts from sources, assumptions, engineering decisions, and generated presentation remain distinguishable.
- Every source fact and consequential selection retains source references. Source revisions are explicit; never silently overwrite a fact when a plan changes.
- Nominal 100 W channel baseline: design load <= 90 W, with any lower verified equipment limit honored. This is KIS design doctrine, not a universal code/listing claim.
- Calculate with confirmed LV input load at the channel interface. Do not automatically reuse original AC fixture wattage or assume driver compatibility.
- Legacy v0.1: one explicit scope disposition per physical fixture; one channel per included fixture; no assignments to excluded fixtures.
- Legacy v0.1: one required room/micro-zone per channel. Independent daylight, manual, occupancy, dimming, or other source control boundaries survive the transformation.
- Unknown values are `null`, not zero. Create open items and mark decisions provisional; final grouping requires resolved blocking uncertainty.
- Source/control departures require established authority, approval and traceable decisions while preserving the observed intent. Legacy v0.1 uses `zone_assignment`; do not insert that field into v0.3. A confirmed decision alone does not establish external approval.
- Manufacturer electrical limits, output/driver type, aggregate power, and channel capacity require verified evidence and engineering review.

## Storage and publication

Keep real source PDFs, schedules, takeoffs, client identifiers, storage credentials, project-instance JSON, and generated client files outside Git. Only synthetic examples and approved anonymized precedent belong here. `.gitignore` is a convenience, not a privacy review. Inspect the staged files before publication.

## Scope and verification

The current v0.4 tools validate entered physical inventory/intake/design phases and export five source-review CSVs plus validation JSON; read-only v0.3 export is supported. Legacy v0.2/v0.3 emit full engineering JSON and v0.1 retains its dedicated exporter. Phase checks support review milestones but do not independently extract missing source items or establish owner approval. Never invent later design inputs to make an early intake pass. They do not extract plans, optimize channels, certify compatibility, design emergency lighting, or approve construction documents.

When changing the contract or engineering checks, update documentation, schema version as appropriate, synthetic fixtures, and meaningful boundary/failure tests together. Run:

```bash
python -m unittest discover -s tests -v
python -m generators.validate_model docs/reference-implementations/synthetic-room/lighting-model.json
python -m generators.model_intake docs/reference-implementations/synthetic-intake/lighting-model.json --phase intake
python -m generators.model_intake docs/reference-implementations/synthetic-intake/design-model.json --phase design
```

Use [extension page templates](templates/README.md) and retain required framework metadata. All initial domain pages are draft pending real-project review. Treat examples as precedent, never standards.
