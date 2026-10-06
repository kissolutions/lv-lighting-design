# Milestone Markup Framework Update — 2026-10-06

Copy this ZIP's contents into its matching repository root, preserving `.git`, then commit/sync normally. Apply both repository ZIPs. No Python, updater or build step is required to install these finished framework files. Reconcile newer local edits before overwriting changed pages.

Six print packages: Room Boundaries schedule and review plans; fixture schedule plus every Light Point ID grouped by type over lightly hatched rooms; zone list and narrative-locked room-device schedule/location review; device-free micro-channel boxes with output tag upper left/watts lower right; controller/power equipment review; accepted coordinated six-layer markup.

Room devices get scheduled immediately after narrative lock and receive device-specific provisional positions under the milestone placement rules, then are finalized by the owner. Tags OS/DS/WC/WD and stable metadata link devices to rooms and parent/child zones. Controller equipment receives a later reasonable-location review. Every open-office occupancy cluster is a first-class child zone; parent records shared manual/aggregate behavior without duplicating lights or loads.

Queued display directives implemented in guidance/helpers: calculated values ceiling-round to whole numbers after calculation; text rendered last/in front; more-enveloped zone/channel boundaries dashed without polyline detours. Source/nameplate and underlying engineering precision remain unchanged.

Contracts: lighting v0.7 (parent_zone_id and narrative review), topology v1.1 (device tag/name/room/category), markup manifest v1 (deliverables, immutable annotations, layers, location/review basis and actual readback status). Older versions remain supported. Existing project-instance JSON is not automatically migrated; agents populate/upgrade records in project work with reviewed facts. No real client/source documents are in this package.

Implemented: contracts, hierarchy/electrical integration, metadata review checks, formatting helpers, CSV/printable HTML schedule exporter and synthetic example. The exporter produces schedule front sheets, not PDF plan overlays. Actual PDF layering, annotation promotion/placement and human edit/save/readback still require a suitable PDF workflow and verification; this package does not claim them completed.

Verification: all 156 tests passed (17 new milestone tests); required legacy phase/model checks passed; synthetic v0.7 design and v1.1 topology checks passed; all six schedule sections exported; ZIP integrity, schema seeds and internal links verified. A legacy v0.6 hierarchy projection was also corrected to retain AC/DC information and the selected 95 W design limit through older checks.

No repository was pushed. Per-file SHA-256 and pinned base commits are in the manifest.

Target: `lv-lighting-design`
Base commit: `aa3699ef29d8c8aa3430c18ebba3f295a14e6ed9`
