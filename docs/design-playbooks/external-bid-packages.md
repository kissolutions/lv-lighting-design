---
title: "External LV Bid Packages"
page_type: playbook
page_status: draft
confidence_level: medium
domain_primary: low-voltage-lighting
ai_role: prescriptive_standard
invocation_triggers:
  systems_present: [low_voltage_lighting]
decision_axes: [external_package_scope, readiness, logical_connections, publication, bidder_response]
related_pages:
  - "milestone-review-packages.md"
  - "markup-deliverable-presentation-contracts.md"
  - "lv-project-workflow-and-readiness.md"
  - "../governance-and-doctrine/october-16-consolidated-reconciliation.md"
---

# External LV Bid Packages — Design Playbook

Revision: 2026-11-01, v0.1. Status: owner-adopted package/reconciliation direction; reusable generation and saved-PDF viewer verification are separate implementation work. Draft metadata does not reopen explicit owner decisions.

## 1. Purpose and Use

Assemble external selection/pricing requests for fixture distributors (BID-FX), controls vendors (BID-CTL) and LV installers (BID-LV). These are a separate family from M1–M6 milestone gates, P1–P6 owner reviews and the named Full/Abridged Basis of Design sets. Each package reuses authoritative registers, schedules and the specified markup forms; it is not a new design database or a renumbered milestone.

## 2. Design Intent

Shape information to the recipient while preserving one set of engineering identities, selected requirements, quantities and accepted associations. A bidder reviews an issued exhibit and returns a separate commercial/technical response. They do not develop the authoritative design by editing the supplied PDF objects.

## 3. Space / System Definition (Decision-Oriented)

| Package | Recipient / purpose | Routing dependency |
|---|---|---|
| BID-FX | Fixture distributor/rep: compatible fixture/driver selections, product data, price and lead time | No equipment placement, M4 channel assignments or cable routing prerequisite |
| BID-CTL | Controls vendor/contractor: equipment pricing and separately scoped services; logical single-line fan-outs | Logical connections only; physical routing is excluded |
| BID-LV | LV installer: installation labor/material scope and comparable pricing | Reviewed placements and a declared physical routing/quantity basis, with proposed portions identified |

Package form, review/acceptance state, estimate class and commercial price commitment are independent. Do not assign an AACE class or promise a firm price from a package name or PDF appearance.

## 4. Constraint Envelope

### 4.1 Hard Constraints

Use identified model/requirement/assignment revisions and supported product facts. Preserve approved source types, Light Point/device IDs, channel membership, first fixture, chain order and logical port/network associations. Packaging cannot silently move equipment, recompute accepted chains, select products or change the narrative.

### 4.2 Soft Constraints

Reuse the established symbols and colors, including the owner room-device colors and CV/CC channel/reach-line conventions. Audience changes affect composition and visible detail, not physical identity or a competing bid-package legend.

### 4.3 Hidden Constraints

Declared estimates can contain allowances, unknown selections and proposed routes. Missing facts stay explicit. Support methods/spacing, cable separation, mounting/access provisions, plenum/rating, voltages, gauges, network limits and termination rules require a project/evidence basis; no beta-job values become global defaults.

## 5. Baseline / Default Design Pattern

### 5.1 Readiness and basis

Generate from the current reviewed project records; accepted facts remain protected and proposed content is separately identified. Include only scope whose requirements can support the requested response. Pricing an explicit allowance does not accept its design.

Identify package scope, purpose, model/requirements/selection revisions, quantity basis and all applicable placement/route/estimate revisions. For BID-CTL state physical routing is outside this package rather than inventing a route revision. Each quantity is labelled **firm**, **allowance** or **TBD**, with its basis and linked open question where applicable. Here firm describes a reconciled quantity on the stated basis, not a binding commercial price or construction release.

### 5.2 External PDF publication

**All issued design graphics, symbols, labels, callouts and connection/route linework in every external bidder PDF are fully flattened. Retain the defined properties tooltips/popups.** Locked live markups are not a substitute.

- Flatten a derivative of the identified live master; retain the source privately. Disable **Allow Markup Recovery (Unflatten)** in issued copies.
- Enable **Show Properties in Popup** and select the defined component fields. Preserve layers and layer/bookmark navigation where the composition uses them; layers contain flattened content, not editable design objects.
- For Light Point graphics retain the exact Subject `<Light Point ID> <fixture type mark>`. Use the defined room/device properties for those objects.
- Do not substitute print-to-PDF, rasterization or plain drawn graphics that discard required properties. A read-only popup/link annotation used solely to expose metadata/navigation may remain; no recoverable live design graphic/text/route object may remain.
- Bidders may add their own notes, clouds or other overlay markups. Do not impose PDF permissions that prevent those additions. Their annotations are a separate response, not edits to the issued design or automatic owner-return model input.
- Retain the issued original and checksum. Flattening is publication protection, not a claim that no PDF editor can alter page content. Keep the authentic issue distinguishable from a bidder-marked copy.

The [Bluebeam flatten settings](https://support.bluebeam.com/user-manual/menus/document/flatten-markups.html) support this workflow. Verify the actual saved issue in the intended viewer; a generic renderer or permission flag does not prove retained popups/layers or irreversible flattening.

### 5.3 Page order and presentation

BID-FX and BID-CTL start with their pricing schedule, followed by scope/support information as needed, drawings/diagrams and the detailed list. BID-LV explicitly starts with scope/response, then directives/schedules and specifications, printed plan sets and detailed tables. This is an audience-specific exception to schedule-first wording.

Use enough pages for readable tables; one schedule page is not an artificial limit. Repeat table headers. Every page identifies project/job, package/revision, issue status and date. Plan/diagram title bands identify the sheet purpose, source/basis and level or logical scope. Label schematics as logical/not to scale; show the applicable length basis on physical-route sheets. Markup ID text follows 4 pt / 1.00 margins and the existing appearance rules before flattening.

## 6. Typical Variants

### 6.1 BID-FX — Fixture distributor package

**Gate:** reviewed M2 physical takeoff plus adopted M3 energy-code/control requirements establishing dimming needs for each included fixture group. Follow [the distributor schedule gate](lv-project-workflow-and-readiness.md#distributor-fixture-schedule--after-m3-requirements). This replaces the proposal's description of BID-FX as merely external P2.

Order: fixture schedule; source-plan sheets with **Light Points — Flattened / External**; individual Light Point table; optional data companion/open-item pages. Room boundaries are not a default requirement.

Schedule information: exact source designation and description; source manufacturer/catalog option separately identified from requested/selected replacement; quantity by applicable level/group and total; load with per-fixture/per-length basis; required dimming behavior and known selection-critical performance; known LV input/interface facts; scope, confidence and open-item remarks. Unknown vendor-dependent products/electrical values are requested/TBD. Do not assume a voltage or driver type from a generic dimming label.

When a source type serves different control requirements, distinguish group quantities/requirements without silently renaming source types. Preserve the existing **Paired Fixture Schedule** definition where that named comparison is used; the vendor pricing schedule does not redefine it or the procurement BOM.

The individual list traces Light Point ID, exact type, physical kind/counting basis, level/served room, emergency status where supported and relevant requirements/unknowns. Channel fields are included only when established and useful; M4 assignments are not a gate.

**Return:** distributor's own separate fixture schedule/proposal, keyed to source types/groups and package revision, with proposed selections, electrical/dimming data, pricing/lead time, exclusions and alternates. A bidder-marked PDF can explain a proposal but does not become the selected fixture register.

### 6.2 BID-CTL — Controls vendor package

**Gate:** reviewed equipment quantities/selections or explicit selection requests, system architecture, applicable M3 operating requirements and supported logical connections sufficient for pricing. Geographic placement acceptance, physical pathways, routing and installed cable estimates are not prerequisites.

Order: device/orderable-part schedule; scope and separately priced programming/commissioning support/spares; **logical single-line fan-outs**; physical device/connection list and open items. Do not import the routed coordinated-system PDF as this package.

Reuse the named single-line fan-out view and current logical assignment records. Retain IDs and supported input/output/channel/port relationships: power-distribution relationships where applicable; controller-to-light/channel assignments; CIO/PDnet relationships; CIO/SDCnet/SW relationships; room-device input/service associations and applicable wireless relationships. Preserve distinct power and signal roles. These are information requirements, not a replacement diagram layout or a new schematic generator.

Fan-outs express logical connectivity, not spatial routing, cable lengths or an assumed star-wired physical topology. Retain any specified bus/port membership and order; do not convert a daisy chain to separate home runs. Shared devices remain one physical quantity, even if referenced in several diagrams. Unknown logical assignments remain explicitly unassigned/TBD, not invented.

Exclude physical PDnet/SDCnet/cable routes, pathway geometry, cable-length labels, J-hooks, raceway and installer labor quantities. Any requested location-only reference is supplemental and carries no route information or new readiness gate.

Device schedule: short item code, name, manufacturer, supported part number/model or TBD, concise description, quantity/unit and basis. Detailed list: physical ID/type, known level/location context where useful, logical connects-to information and relevant outputs/loads/feeds/inputs/zones. Scope services separately; missing programming responsibility remains an explicit question.

**Return:** separate vendor equipment/services quotation, product data, clarifications and alternates keyed to the package and logical identities. Rerouting is not a vendor deliverable under BID-CTL.

### 6.3 BID-LV — LV installer package

**Gate:** scoped equipment/device placements, physical routes/endpoints and cable choices suitable for an installation estimate, with accepted versus proposed portions explicit; a frozen cable/installation-quantity basis; and recorded supply/install/termination/programming/testing responsibility splits. It is an estimate issue, not automatic construction release.

Order: scope/response and assumptions; cable-role directives; cable schedule; installation quantities; project support/access specification; separate printed **device locations**, **power routes** and **control routes** sheet sets; segment/support tables, alternates and open items. Use one or more sheets per applicable level as required.

Reuse the corresponding location/channel/network components in full-information Flattened forms. Keep IDs, mounting information, endpoints and installation-critical labels readable in print. Popups/layers may supplement the sheets, but bidders must not need them to understand required printed scope. Do not replace accepted fixture chains with estimate nearest-neighbour chains.

State physical route versus straight-line estimate basis, scale, vertical travel, slack/end allowances and waste inclusion/exclusion separately. Do not measure logical fan-out lines for quantities. Deduplicate overlapping pathway/support runs under the declared count method; exclude portions assigned no hooks, such as applicable wall drops. Shared support locations do not turn two specified hooks into one physical item. Keep unresolved firestopping/access conditions and route-limit findings visible.

Cable/installation schedules distinguish cable types/jackets, terminations by family, equipment and device mounting, fixture connections, supports, hard-ceiling pathways/ends, testing/labelling, lifts/mobilization and other declared scope. Unknowns are TBD or explicit allowances, not zero.

Provide an editable **bid-response workbook** for lump sum plus unit-price breakdown, package quantities, optional bidder quantity, unit price, extended amount, notes, exclusions and alternates. An entered bidder quantity, including zero, overrides the package quantity for that response calculation; blank uses the package quantity. Show the breakdown total and bidder's lump sum separately and explain differences. This response workbook is not the authoritative design workbook.

**Return:** completed bid form/quotation, qualifications, bidder quantities, proposed routes or other alternates and optional annotated-copy explanations, all retained separately from the issued basis.

## 7. Decision Gates

Before issue, verify scoped readiness, consistent component revisions and quantities, visible provisional content, supported selection facts, flattening/popups, printed completeness and the expected bidder return. No new per-room approval form is required.

BID-FX waits for dimming requirements; BID-CTL waits for logical equipment/connectivity readiness; BID-LV waits for a declared physical installation basis. Do not delay the first two for installer routing work. An unresolved quantity/selection may be priced only as a clearly declared allowance/request; an unresolved required function cannot silently become no requirement.

## 8. Design Zoning / Grouping Strategy

Preserve M3 functional groups and M4 electrical assignments; package filters do not change them. Reuse component forms and established colors rather than a separate external legend. No universal room-background insertion. For the installer only, explicitly selected faint room/location context may aid orientation without becoming authoritative routing geometry.

## 9. Common Failure Modes

### Design-Time Failures

Re-solving accepted chains during export; inventing connections to fill a diagram; using a logical line for footage; defaulting unsupported electrical values.

### Documentation Failures

Locked live annotations presented as flattened; dropped tooltips; stale schedule/header/length metadata; optional layer states leaking physical routing into BID-CTL; double-counted devices or included assembly parts.

### Construction / Operational Failures

Treating an estimate as construction authority; adopting vendor substitutions or routing alternates without review; copying unverified support/network limits into installation directives.

## 10. Safe Assumptions (and Limits)

Unknown selection is TBD, unknown quantity is TBD, and absence needs evidence. A reviewed quantity allowance does not prove a physical location/port binding. A vendor's separate schedule/proposal does not approve itself. External PDF properties identify the issued design; they do not make it an editable source model.

## 11. Documentation Expectations

Use the canonical file pattern `<JOB>_<PACKAGE>_DD-R<n>_<YYYY-MM-DD>.<ext>` for this design-estimate family, with an independent revision series per package. Record presentation form, purpose and actual review/issue status separately.

Working drafts may be replaced before designation. **Every designated frozen draft and every issued file set is immutable**; corrections receive the next package revision. There is no pre-issue exception allowing a frozen file to be overwritten.

Freeze exact PDF/companion files with SHA256SUMS and a short README identifying what/when/by whom and the input basis in a package-scoped frozen folder. Use the existing issue/DD register rather than a second authoritative design register: package, revision, file set/hashes, status/date, approver/recipient, source basis, assumptions/open items and supersedes/superseded-by links. Retain the linked live master separately. Date/time entries include their timezone.

Bidder overlays, fixture schedules, quotations and bid forms are separate response records referencing that frozen issue. Review proposed changes into the authoritative model/selection/route records first, then regenerate affected outputs under a new issue. Do not treat external overlays as the internal milestone annotation readback stream.

## 12. When to Go Deeper / Exit This Playbook

The original BP proposal cites unrecovered DD1–DD17 addenda. This owner-adopted contract resolves the stated package, publication and logical-versus-physical questions without claiming the missing texts were reviewed. Unspecified allowance formulas, installation defaults, technical limits and construction-issue package definitions remain separate work.

Reusable fan-out/PDF/workbook generation, flatten-with-popup conversion and native-viewer verification remain implementation tasks. This contract does not alter a canonical schema, implement a generator or certify an actual project issue. Keep real project source files, counts and proposals out of this repository.

## 13. Cross-Links to Supporting Knowledge

- [Markup presentation forms and dependencies](markup-deliverable-presentation-contracts.md)
- [Internal milestone review packages](milestone-review-packages.md)
- [Workflow and distributor readiness](lv-project-workflow-and-readiness.md)
- [Existing named schedules and Basis of Design sets](../governance-and-doctrine/october-16-consolidated-reconciliation.md#4-preserve-the-exact-presentation-contracts)
- [Control-system symbols/colors](control-system-markup-legend.md)
- [Bluebeam flatten settings](https://support.bluebeam.com/user-manual/menus/document/flatten-markups.html)
- [Bluebeam layer preservation](https://support.bluebeam.com/user-manual/menus/window/add-layers-pdf.html)

## 14. Status and Stewardship

Owner-adopted direction, 2026-11-01; draft implementation readiness. The later explicit decisions require fully flattened external design content with properties popups and separate bidder responses, and replace routed BID-CTL exhibits with logical fan-outs. These override conflicting original proposal examples. Owner: KIS Solutions.

## 15. Author Notes (Institutional Context)

Audience-specific documents share the same engineering basis. Distinct package readiness avoids waiting for installation design to ask a distributor or controls vendor for the product information that later design needs.
