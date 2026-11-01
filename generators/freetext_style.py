"""Form H live FreeText for the supported Bluebeam editing workflow.

Generated labels use standard-font WinAnsi metrics, absolute /BBox = /Rect,
4 pt text, a /DS CSS margin of 1 pt, and no /RD or /RC. This is a workflow
profile, not a claim that other valid PDF appearance conventions are invalid.
"""
import json
import math
import re
from functools import lru_cache
from pathlib import Path

from pypdf.errors import PdfReadError
from pypdf.generic import (ArrayObject, DecodedStreamObject, DictionaryObject,
                          FloatObject, NameObject, NumberObject, TextStringObject,
                          ContentStream)

FONT_SIZE_PT = 4.0
MARGIN_PT = 1.0
LINE_HEIGHT_PT = 4.6
INSET_PT = MARGIN_PT + 1.0
_NUM = r'[-+]?(?:\d*\.\d+|\d+\.?\d*)(?:[eE][-+]?\d+)?'
_ALIASES = {'Helv': 'Helvetica', 'TiRo': 'Times-Roman', 'Cour': 'Courier'}


def _finite(value):
    value = float(value)
    if not math.isfinite(value):
        raise ValueError('Non-finite label value')
    return value


def color_bytes(rgb):
    values = tuple(_finite(v) for v in rgb)
    if len(values) != 3 or any(not 0 <= v <= 1 for v in values):
        raise ValueError('Expected three RGB components in [0, 1]')
    return tuple(int(math.floor(v * 255 + .5)) for v in values)


def rgb_hex(rgb):
    return '#' + ''.join(f'{k:02X}' for k in color_bytes(rgb))


def _encoded(rgb):
    # Quarter-byte interior avoids six-decimal k/255 truncation drift. Clamp
    # the top byte, so white never exceeds PDF's legal [0, 1] range.
    return tuple(min(1., (k + .25) / 255) for k in color_bytes(rgb))


def da_string(rgb=(0, 0, 0), size=FONT_SIZE_PT, font='Helv'):
    if not re.fullmatch(r'[A-Za-z][A-Za-z0-9_-]*', font):
        raise ValueError('Unsafe PDF font resource name')
    return f'/{font} {_finite(size):g} Tf ' + ' '.join(f'{v:.10f}' for v in _encoded(rgb)) + ' rg'


def ds_string(rgb=(0, 0, 0), size=FONT_SIZE_PT, family='Helvetica'):
    if family not in _widths():
        raise ValueError('Unsupported standard font family: ' + family)
    return (f'font: {family} {_finite(size):g}pt; text-align:left; margin:1pt; '
            f'line-height:4.6pt; color:{rgb_hex(rgb)}')


def parse_da(da):
    """Read the last font and RGB/gray fill operators; never guess a font/color."""
    tokens = str(da or '').split()
    font = size = rgb = None
    try:
        for i, token in enumerate(tokens):
            if token == 'Tf' and i >= 2 and tokens[i-2].startswith('/'):
                font, size = tokens[i-2][1:], _finite(tokens[i-1])
            elif token == 'rg' and i >= 3:
                rgb = tuple(_finite(v) for v in tokens[i-3:i])
            elif token == 'g' and i:
                rgb = (_finite(tokens[i-1]),) * 3
            elif token == 'k':
                raise ValueError('CMYK FreeText needs explicit color reconciliation')
    except (ValueError, TypeError) as exc:
        raise ValueError('Unparseable /DA: ' + str(exc)) from exc
    if not font or size is None or size <= 0 or rgb is None:
        raise ValueError('Missing explicit font, size or fill color in /DA')
    color_bytes(rgb)
    return dict(font=font, size=size, rgb=rgb)


def ds_from_da(da, family=None):
    parsed = parse_da(da)
    family = family or _ALIASES.get(parsed['font'], parsed['font'])
    return ds_string(parsed['rgb'], parsed['size'], family)


@lru_cache(maxsize=1)
def _widths():
    # Standard Type 1 AFM advances in WinAnsi byte order, generated from
    # ReportLab's standard-font metrics. ReportLab is not a runtime dependency.
    return json.loads(Path(__file__).with_name('freetext_afm_widths.json').read_text())


def text_lines(text):
    return str(text).replace('\r\n', '\n').replace('\r', '\n').split('\n')


def line_width(text, size=FONT_SIZE_PT, family='Helvetica'):
    metrics = _widths().get(family)
    if metrics is None:
        raise ValueError('Unsupported standard font family: ' + family)
    encoded = str(text).encode('cp1252')
    try:
        return sum(metrics[str(k)] for k in encoded) * size / 1000
    except KeyError as exc:
        raise ValueError('Unsupported WinAnsi character') from exc


def label_rect(left, top, text, size=FONT_SIZE_PT, family='Helvetica'):
    lines = text_lines(text)
    width = max(line_width(line, size, family) for line in lines) + 2 * INSET_PT + 1.5
    height = len(lines) * LINE_HEIGHT_PT + 2 * INSET_PT - .6
    return [_finite(left), _finite(top) - height, _finite(left) + width, _finite(top)]


def _arr(values):
    return ArrayObject([FloatObject(v) for v in values])


def _literal(text):
    data = text.encode('cp1252')
    # Octal escapes avoid control characters, parentheses and backslashes in
    # PDF literal strings. /Contents itself remains unchanged Unicode text.
    return b'(' + b''.join((bytes([k]) if 32 <= k <= 126 and k not in (40, 41, 92)
                           else f'\\{k:03o}'.encode()) for k in data) + b')'


def apply_style(writer, annotation, *, rgb=None, family='Helvetica', resize=True):
    """Regenerate one supported label, retaining its top-left and object metadata.

    Refuse unsupported text before mutating anything. Callers own scope and
    review state; this function does not accept geometry or change anchors.
    """
    if annotation.get('/Subtype') != '/FreeText':
        raise ValueError('Expected /FreeText')
    rect = [_finite(v) for v in annotation['/Rect']]
    if len(rect) != 4 or rect[2] <= rect[0] or rect[3] <= rect[1]:
        raise ValueError('Invalid /Rect')
    text = str(annotation.get('/Contents', ''))
    for line in text_lines(text):
        line_width(line, FONT_SIZE_PT, family)  # validate before mutation
    if rgb is None:
        rgb = parse_da(annotation.get('/DA'))['rgb']
    encoded = _encoded(rgb)
    if resize:
        rect = label_rect(rect[0], rect[3], text, family=family)
    font = DictionaryObject({NameObject('/Type'): NameObject('/Font'),
        NameObject('/Subtype'): NameObject('/Type1'),
        NameObject('/BaseFont'): NameObject('/' + family),
        NameObject('/Encoding'): NameObject('/WinAnsiEncoding')})
    stream = DecodedStreamObject()
    stream.update({NameObject('/Type'): NameObject('/XObject'),
        NameObject('/Subtype'): NameObject('/Form'), NameObject('/BBox'): _arr(rect),
        NameObject('/Resources'): DictionaryObject({NameObject('/Font'):
            DictionaryObject({NameObject('/Helv'): writer._add_object(font)})})})
    # Absolute page coordinates are intentional for the supported editor.
    commands = [b'q BT 0 Tc 0 Tw 100 Tz 0 Ts 0 Tr /Helv 4 Tf', (' '.join(f'{v:.10f}' for v in encoded) + ' rg').encode()]
    baseline = rect[3] - INSET_PT - .776 * FONT_SIZE_PT
    for i, line in enumerate(text_lines(text)):
        commands.append(f'1 0 0 1 {rect[0] + INSET_PT:.8f} {baseline - i * LINE_HEIGHT_PT:.8f} Tm'.encode())
        commands.append(_literal(line) + b' Tj')
    commands.append(b'ET Q')
    stream.set_data(b'\n'.join(commands))
    annotation[NameObject('/Rect')] = _arr(rect)
    annotation[NameObject('/DA')] = TextStringObject(da_string(rgb))
    annotation[NameObject('/DS')] = TextStringObject(ds_string(rgb, family=family))
    annotation[NameObject('/Q')] = NumberObject(0)
    annotation[NameObject('/AP')] = DictionaryObject({NameObject('/N'): writer._add_object(stream)})
    for key in ('/RD', '/RC'):
        annotation.pop(NameObject(key), None)
    return annotation


def resolved(obj):
    return obj.get_object() if hasattr(obj, 'get_object') else obj


def _normal(annotation):
    ap = resolved(annotation.get('/AP'))
    return resolved(ap.get('/N')) if hasattr(ap, 'get') else None


def appearance_fonts(normal):
    resources = resolved(normal.get('/Resources'))
    fonts = resolved(resources.get('/Font')) if hasattr(resources, 'get') else None
    return fonts if hasattr(fonts, 'get') else {}


def style_issues(annotation, aid='unknown'):
    """Structural form-H checks; not a viewer certification or blanket PDF rule."""
    issues = []
    def fail(message):
        issues.append(f'FreeText {aid}: {message}')
    try:
        da = parse_da(annotation.get('/DA'))
    except (ValueError, TypeError) as exc:
        fail(str(exc))
        return issues
    if abs(da['size'] - FONT_SIZE_PT) > 1e-6:
        fail('font size must be 4 pt')
    props = {}
    for chunk in str(annotation.get('/DS', '')).split(';'):
        if not chunk.strip():
            continue
        if ':' not in chunk:
            fail('malformed /DS declaration')
            continue
        key, value = chunk.split(':', 1)
        if key.strip().lower() in props:
            fail('duplicate /DS property')
        props[key.strip().lower()] = value.strip()
    fontmatch = re.fullmatch(r'(.+?)\s+(' + _NUM + r')pt', props.get('font', ''))
    family = None
    if not fontmatch:
        fail('missing/malformed /DS font; form H uses family before size')
    else:
        family = fontmatch[1]
        if abs(float(fontmatch[2]) - da['size']) > 1e-6:
            fail('/DS size disagrees with /DA')
        if family not in _widths():
            fail('unsupported /DS font metrics')
    for key, value in [('margin', MARGIN_PT), ('line-height', LINE_HEIGHT_PT)]:
        match = re.fullmatch(r'(' + _NUM + r')pt', props.get(key, ''))
        if not match or not math.isfinite(float(match[1])) or abs(float(match[1]) - value) > 1e-6:
            fail(f'/DS {key} must be {value:g}pt')
    if props.get('text-align') != 'left':
        fail('/DS text-align must be left')
    if props.get('color', '').upper() != rgb_hex(da['rgb']):
        fail('/DS color disagrees with /DA or is missing')
    if any(int(v * 255) != k for v, k in zip(da['rgb'], color_bytes(da['rgb']))):
        fail('/DA color is unstable across truncating/rounding viewers')
    if '/RD' in annotation:
        fail('/RD must be absent; margin belongs in /DS')
    if '/RC' in annotation:
        fail('/RC must be absent from generated/normalized live labels')
    try:
        rect = [_finite(v) for v in annotation['/Rect']]
        if len(rect) != 4 or rect[2] <= rect[0] or rect[3] <= rect[1]:
            raise ValueError('invalid rectangle')
        lines = text_lines(annotation.get('/Contents', ''))
        if family in _widths():
            if max(line_width(line, da['size'], family) for line in lines) > rect[2] - rect[0] - 2 * INSET_PT + 1e-6:
                fail('text would wrap in Bluebeam re-layout')
        if rect[3] - rect[1] + 1e-6 < len(lines) * LINE_HEIGHT_PT + 2 * INSET_PT - .6:
            fail('text box height would clip Bluebeam re-layout')
    except (KeyError, ValueError, TypeError, UnicodeError) as exc:
        fail('unsupported text or /Rect: ' + str(exc))
        rect = None
    normal = _normal(annotation)
    if not hasattr(normal, 'get_data') or not normal.get_data():
        fail('appearance stream missing/empty')
        return issues
    try:
        bbox = [_finite(v) for v in normal.get('/BBox', [])]
        if rect is None or len(bbox) != 4 or any(abs(a-b) > .001 for a, b in zip(bbox, rect)):
            fail('appearance /BBox must equal /Rect for Bluebeam workflow')
        matrix = [_finite(v) for v in normal.get('/Matrix', [1, 0, 0, 1, 0, 0])]
        if len(matrix) != 6 or any(abs(a-b) > 1e-8 for a, b in zip(matrix, [1, 0, 0, 1, 0, 0])):
            fail('appearance has a non-identity /Matrix')
        fonts = appearance_fonts(normal)
        dafont = resolved(fonts.get('/' + da['font']))
        if not dafont or str(dafont.get('/BaseFont', '')).lstrip('/') != family:
            fail('/DA font resource disagrees with /DS family')
        size = rgb = fontkey = None
        stack = []
        shown = 0
        for args, op in ContentStream(normal, None).operations:
            if op == b'q':
                stack.append((size, rgb, fontkey))
            elif op == b'Q' and stack:
                size, rgb, fontkey = stack.pop()
            elif op == b'Tf':
                fontkey, size = str(args[0]), _finite(args[1])
            elif op == b'rg':
                rgb = tuple(_finite(v) for v in args)
            elif op == b'g':
                rgb = (_finite(args[0]),) * 3
            elif op in (b'Tj', b'TJ', b"'", b'"'):
                shown += 1
                if size is None or abs(size-da['size']) > 1e-6 or rgb is None or color_bytes(rgb) != color_bytes(da['rgb']):
                    fail('appearance text size/color disagrees with /DA')
                actualfont = resolved(fonts.get(fontkey)) if fontkey else None
                if not actualfont or str(actualfont.get('/BaseFont', '')).lstrip('/') != family:
                    fail('appearance font disagrees with /DS family')
        if not shown:
            fail('appearance contains no text-showing operation')
    except (ValueError, TypeError, KeyError, IndexError, AttributeError, PdfReadError) as exc:
        fail('invalid appearance: ' + str(exc))
    return issues
