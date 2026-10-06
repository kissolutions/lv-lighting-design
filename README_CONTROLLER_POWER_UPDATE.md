# Controller, Power and Sensor Framework Update — 2026-10-06

Copy the contents of this ZIP into the matching repository root, preserving `.git`. These are finished files: no Python, update script or build step is required to install them. Commit/sync using your normal workflow. Apply both repository-specific ZIPs so cross-links resolve.

The update captures the 2026-10-05 owner directives: existing micro channels first; logical QDCD clustering; PDU family/Smart rules and default four-feed mapping with 1–3 exceptions; sensor counts and default SW4/SW8 aggregation; CIO owner location decision; early AHJ and area plenum facts; placement, device strings, manufacturer routing checks and owner markup loop; red/blue/purple shape legend.

Hardware pages distinguish supplied-sheet facts, owner policy and outstanding manufacturer/owner decisions. The topology companion is separately versioned and paired with v0.6; it does not change fixture/channel membership. Existing project JSON is not automatically upgraded. Use the new companion template for early project facts and later allocation records; existing electrical checks still run independently. Nothing in this ZIP allocates actual project devices or produces project plan markup.

Verification: 139 tests passed, including 8 new topology boundary/failure tests; all five required synthetic phase/model checks passed. Companion schema and seed validated. Product sheet pages inspected; local/internal links checked against both pinned repository trees and update files. Actual edited-PDF round-trip and missing manufacturer limits remain explicit review items.

Existing M4 defects corrected: v0.5 projection no longer crashes on removal of v0.6-only fields; cross-zone test now preserves Space-zone links so it reaches its intended micro-channel check. Current M4 Class 2 profile remains 100 W rated / <=95 W design.

No repositories were pushed. Manifest includes base commit and per-file SHA-256. Reconcile any newer local edits before overwriting changed existing pages.

Target repository: `lv-lighting-design`
Base commit: `0440513a62954105c23c2b4d7e846513964d503a`
