---
title: "Live FreeText Form H"
page_type: playbook
page_status: draft
confidence_level: medium
domain_primary: low-voltage-lighting
ai_role: prescriptive_standard
invocation_triggers:
  systems_present: [low_voltage_lighting]
decision_axes: [live_annotation_style, viewer_interoperability, publication_revision]
related_pages:
  - "markup-deliverable-presentation-contracts.md"
  - "visual-spatial-extraction.md"
---

# Live FreeText Form H

Revision: 2026-11-01. Owner-selected form H supersedes the initial Proposal FT
rules and intermediate test variants. The implementation is reconstructed from
the final supplied specification; the earlier external patch was not supplied
or applied. Owner-reported viewer results are distinguished from local tests.

## Supported editing workflow

**Bluebeam is the editing tool. Foxit is view-only.** A file saved by Foxit
must be normalized into a new revision before further Bluebeam editing.
Foxit can rewrite appearances even for labels that were not moved. Do not
assume that only labels deliberately edited need attention.

The owner accepted form H after Bluebeam/Foxit comparison. Foxit may lay out
multi-line labels with different padding/leading and clip their final line.
That viewer difference is accepted for this Bluebeam editing workflow; it is
not fixed or universally certified by the implementation. Alternative J/K
multi-line/single-line forms were withdrawn, not adopted as new defaults.

## Generated and normalized live label contract

Use `generators.freetext_style` for live Light Point IDs, type marks, room
text, device/channel IDs, subzone badges and any generated live legend text.
Ordinary PDF page-content schedules and flattened publication content are
not live FreeText labels. Read-only/locked external issues are not repair
targets; their live sources remain the authority for a later revision.

- Text is **4 pt**. The user-visible **1.00 margin** is represented by
  `margin:1pt` in `/DS`, not `/RD`.
- `/DS`: `font: Helvetica 4pt; text-align:left; margin:1pt;
  line-height:4.6pt; color:#RRGGBB`. Supported standard-font variants may
  retain their family. Family-before-size matches the owner-tested final
  form; the earlier assertion that it was intrinsically invalid is withdrawn.
- `/DA` and appearance text use matching 4 pt font and byte-equivalent RGB.
  For byte k, encode a component as `(k + 0.25)/255`, clamped to 1 for k=255,
  at sufficient precision. Truncating and rounding readers recover the same
  hex byte. This explicitly permits that small interior encoding offset.
- **No `/RD` and no generated `/RC`.** Owner read-back showed Bluebeam stores
  the margin in `/DS`, can inset/shrink a box by `/RD`, then removes `/RD`.
  Bluebeam can add its own `/RC` when it saves; normalize before publishing a
  generated-profile revision rather than treating viewer metadata as a new
  framework writer convention.
- Explicit normal appearance: **`/BBox` equals the annotation `/Rect`** in
  page coordinates, without a placement `/Matrix`. The checker accepts an
  explicit identity matrix. A legal local-coordinate appearance may fail this
  Bluebeam-specific workflow profile; it is not declared invalid PDF.
- Compute box width from the maximum line's standard AFM advance plus
  `2*(margin+1)+1.5` pt. Height is `line_count*4.6+2*(margin+1)-0.6` pt.
  Text origin x is left+margin+1; first baseline is
  top-(margin+1)-0.776*font_size. Later baselines use 4.6 pt leading.
- Preserve accepted physical anchors independently of label-box layout.
  Normalization preserves each label's current top-left, `/NM`, `/Contents`,
  Subject and layer membership. Its width/height and appearance can change.
  Do not promise byte-identical `/Rect` or `/AP` as the initial FT patch did.

The shared helper includes standard Type 1 WinAnsi advance metrics generated
from ReportLab's standard-font AFM data; no new runtime package is required.
Unmapped/custom fonts, unencodable glyphs, rotated text and callouts require
explicit review instead of replacement by a guessed font or lost text.

## Diagnosis and evidence boundary

The earlier limited test suggested zero margins triggered restyling. Later
owner tests/read-back found inconsistent `/DA`, `/DS` and saved appearances,
missing CSS margin, wrapping, color truncation, and the Foxit-to-Bluebeam
appearance-coordinate interaction. **The margin-only causal explanation is
superseded.** Keep the owner's initial observation as history, not a current
implementation diagnosis.

Owner-reported results: the corrected form opened/moved acceptably in
Bluebeam; single-line labels retained size/color in Foxit; Foxit multi-line
leading/padding differed; Foxit-saved local-BBox appearances subsequently
jumped on individual Bluebeam moves. Normalized form H opened acceptably.
These are scoped field observations, not reproduction by the maintaining
agent. Acrobat behavior was not established and is not claimed.

## Checker

`generators.validate_markup_pdf` checks every FreeText on declared live plan
pages, irrespective of annotation-register role. It enforces 4 pt; canonical
`/DS` font, size, color, margin and leading; no `/RD` or `/RC`; an explicit
nonempty text appearance; matching appearance font/size/color; workflow BBox
and matrix; and AFM width/height sufficient to avoid Bluebeam re-layout wrap
or clipping. Existing identity, editability and appearance gates remain.

It does not inspect every viewer engine or prove that the box moves correctly
on screen. Preserve the representative two-move/save/reopen review in
Bluebeam. Do not pass locked or flattened external publications to the live
plan checker as though they were editable masters.

## Normalization and revision procedure

```bash
python -m tools.normalize_freetext_ap INPUT.pdf NEW_REVISION.pdf --plan-pages 1 2
python -m generators.validate_markup_pdf NEW_REVISION.pdf REGISTER.csv --plan-pages 1 2
```

Omitting `--plan-pages` normalizes all live FreeText; explicit pages are
preferred for assembled documents. The tool clones the document to retain
pages, outlines, layers and unrelated annotations, refuses source or existing
output overwrite, and reports each normalized/skipped label. The CLI exits 1
if any selected label was skipped; a partly normalized output is not a pass.

It removes `/RD`/`/RC`, rebuilds style and appearances, and snaps fonts within
4 pt +/-0.1 to 4 pt. It reports other sizes, unsupported fonts/text, callouts,
rotated annotations, missing identities/DA, and restricted/locked annotations
for review. It does not unlock external issues or choose new project scope.

Retain the previous issued/frozen file. Verify IDs, contents, layer membership,
physical anchors and the intended top-left positions against the prior
revision; issue the presentation repair as a new revision. Historical issues
are not edited in place. Presentation correction does not itself reopen
accepted engineering decisions, but changes or lost location evidence must
be reported honestly.

**Already-jumped labels:** current top-left preservation cannot recover their
former position. Restore from a known prior revision/identity mapping under
owner review; automatic lost-position recovery is not implemented. Do not
guess positions from neighboring labels or a source fixture.

## Implementation and verification limits

The subzone label writer now uses form H at 4 pt with explicit appearances.
Its label box changes from the historical 11 pt badge to fit the new layout;
the existing label top-left and source Light Point anchor remain. Geometry
regression checks must assert that distinction, not preserve the old 11 pt box.

Synthetic tests exercise style failures, colors including 0/255, wrapping,
multi-line height, local-BBox/matrix findings, appearance disagreement,
identity/layer/outline preservation, idempotence, exclusions and overwrite
protection. They do not establish a new real-project or native-viewer proof.
Project-side writers must adopt the helper explicitly; changing the framework
does not rewrite or validate unmodified external scripts automatically.
