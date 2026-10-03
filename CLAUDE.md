# Agent Guidance - LV Lighting Design

Applies to Claude, Codex, and other agents working in this repository.

## Parent framework

Use `kissolutions/knowledgebase_wikijs` as the authority for shared taxonomy, metadata, templates, vocabulary, and physical device facts. If it is available as a sibling checkout, read it there; otherwise use the connected repository. The current verified entry points are:

- [AI Agent Framework Guide](https://github.com/kissolutions/knowledgebase_wikijs/blob/main/AI/AGENT-FRAMEWORK-GUIDE.md)
- [Framework Extension Doctrine](https://github.com/kissolutions/knowledgebase_wikijs/blob/main/governance-and-doctrine/framework-extension-doctrine.md)
- [Knowledge Model Map](https://github.com/kissolutions/knowledgebase_wikijs/blob/main/governance-and-doctrine/map-knowledge-model-structure.md)
- [Definitions](https://github.com/kissolutions/knowledgebase_wikijs/blob/main/governance-and-doctrine/definitions.md)
- [Templates](https://github.com/kissolutions/knowledgebase_wikijs/tree/main/templates)

Keep links to shared knowledge rather than duplicating it. Propose generic framework improvements upstream; do not edit the parent to accommodate this implementation. If retrieval is unavailable, state the limitation and use only the verified local guidance; do not claim to have reviewed current upstream content.

## Repository authority

This extension owns lighting-specific design method, vocabulary, canonical project model, grouping rules, spatial conventions, validation, and generators. Read the [boundary](docs/governance-and-doctrine/repository-boundary.md), [page registry](docs/governance-and-doctrine/page-type-registry.md), [playbook](docs/design-playbooks/lighting-design-playbook.md), and [model overview](docs/ontology/canonical-model/README.md) before changing these interfaces.

Knowledge structure follows meaning; workflow lives in playbooks. Do not import BAS I/O, PLC/controller, or controls-narrative ontology unless a specific cross-domain need is established.

## Engineering invariants

For the current v0.2 device hierarchy, read [device-hierarchy-v0.2.md](docs/ontology/canonical-model/device-hierarchy-v0.2.md) first. The owner has superseded the v0.1 one-zone-per-power-channel restriction: zones own light objects, each single-input light references one power channel, and many-to-many channel/zone views are derived. Branch circuits own power units and power units own channels. Controller output identity is separate from supply-channel identity. Preserve shared source schedule groups, normal operating state, emergency force-on inputs, and separate backup power provisions. Use class-specific output profiles rather than globally imposing 100/90 W or 0-56 V limits. The original invariants below describe the narrower v0.1 tools, which remain available until migration is complete.

- Facts from sources, assumptions, engineering decisions, and generated presentation remain distinguishable.
- Every source fact and consequential selection retains source references. Source revisions are explicit; never silently overwrite a fact when a plan changes.
- Nominal 100 W channel baseline: design load <= 90 W, with any lower verified equipment limit honored. This is KIS design doctrine, not a universal code/listing claim.
- Calculate with confirmed LV input load at the channel interface. Do not automatically reuse original AC fixture wattage or assume driver compatibility.
- One explicit scope disposition per physical fixture; one channel per included fixture; no assignments to excluded fixtures.
- One required room/micro-zone per channel. Independent daylight, manual, occupancy, dimming, or other source control boundaries survive the transformation.
- Unknown values are `null`, not zero. Create open items and mark decisions provisional; final grouping requires resolved blocking uncertainty.
- Source-zone changes require an explicit `zone_assignment` and confirmed, traceable decision. Changes outside the current one-space model require schema/playbook review.
- Manufacturer electrical limits, output/driver type, aggregate power, and channel capacity require verified evidence and engineering review.

## Storage and publication

Keep real source PDFs, schedules, takeoffs, client identifiers, storage credentials, project-instance JSON, and generated client files outside Git. Only synthetic examples and approved anonymized precedent belong here. `.gitignore` is a convenience, not a privacy review. Inspect the staged files before publication.

## Scope and verification

Phase 1 tools validate manual takeoff/assignment data and export review tables. They do not extract plans, optimize channels, certify compatibility, design emergency lighting, or approve construction documents.

When changing the contract or engineering checks, update documentation, schema version as appropriate, synthetic fixtures, and meaningful boundary/failure tests together. Run:

```bash
python -m unittest discover -s tests -v
python -m generators.validate_model docs/reference-implementations/synthetic-room/lighting-model.json
```

Use [extension page templates](templates/README.md) and retain required framework metadata. All initial domain pages are draft pending real-project review. Treat examples as precedent, never standards.
