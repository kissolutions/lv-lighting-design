"""Normalize live form-H FreeText into a NEW revision before Bluebeam editing.

Never reconstruct an already-jumped label's original position by guessing.
Unsupported labels are reported; the CLI fails instead of claiming completion.
"""
import argparse
import json
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from generators.freetext_style import apply_style, parse_da, _normal, appearance_fonts


def _family(annotation, parsed):
    names = {'Helv': 'Helvetica', 'TiRo': 'Times-Roman', 'Cour': 'Courier'}
    normal = _normal(annotation)
    fonts = appearance_fonts(normal) if normal else {}
    font = fonts.get('/' + parsed['font'])
    font = font.get_object() if hasattr(font, 'get_object') else font
    if font and font.get('/Subtype') == '/Type1':
        return str(font.get('/BaseFont', '')).lstrip('/')
    return names.get(parsed['font'], parsed['font'])


def normalize(source, output, plan_pages=None):
    source, output = Path(source), Path(output)
    if source.resolve() == output.resolve() or output.exists():
        raise ValueError('Input and any existing output must not be overwritten')
    reader = PdfReader(str(source))
    writer = PdfWriter()
    writer.clone_document_from_reader(reader)
    pages = list(range(1, len(writer.pages) + 1)) if plan_pages is None else list(plan_pages)
    if not pages or len(set(pages)) != len(pages) or any(not isinstance(p, int) or not 1 <= p <= len(writer.pages) for p in pages):
        raise ValueError('Declare unique valid 1-based plan pages')
    changed, skipped = [], []
    for page in pages:
        for ref in writer.pages[page-1].get('/Annots', []):
            a = ref.get_object()
            if a.get('/Subtype') != '/FreeText':
                continue
            aid = str(a.get('/NM', ''))
            try:
                if not aid:
                    raise ValueError('Missing persistent /NM identity')
                if int(a.get('/F', 0)) & (1 | 2 | 32 | 64 | 128 | 512):
                    raise ValueError('Hidden/locked publication or restricted annotation; no normalization')
                if a.get('/CL') or a.get('/IT') == '/FreeTextCallout' or int(a.get('/Rotate', 0)) % 360:
                    raise ValueError('Callout/rotated FreeText needs explicit layout review')
                parsed = parse_da(a.get('/DA'))
                if abs(parsed['size'] - 4) > .1 + 1e-8:
                    raise ValueError('Font size is outside the 4 pt +/-0.1 normalization range')
                apply_style(writer, a, rgb=parsed['rgb'], family=_family(a, parsed))
                changed.append(dict(annotation_id=aid, page=page))
            except (ValueError, TypeError, KeyError, UnicodeError) as exc:
                skipped.append(dict(annotation_id=aid, page=page, reason=str(exc)))
    # Exclusive create protects other revisions even if the output appeared
    # after the initial existence check. Source bytes are never opened to write.
    with output.open('xb') as stream:
        writer.write(stream)
    return dict(normalized=len(changed), labels=changed, skipped=skipped,
                checks_pass=not skipped, scope='Live FreeText only; current top-left retained; no lost-position recovery')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('source', type=Path)
    p.add_argument('output', type=Path)
    p.add_argument('--plan-pages', type=int, nargs='+')
    args = p.parse_args()
    report = normalize(args.source, args.output, args.plan_pages)
    print(json.dumps(report, indent=2))
    return 0 if report['checks_pass'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
