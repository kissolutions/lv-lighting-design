"""Flattened reference content and structural checks; no popup/rendering claim.

Coordinates/operations are already in the page's native PDF user space. Clone
source pages into the writer first. These helpers neither flatten annotations
automatically nor synthesize properties popups.
"""
from collections.abc import Mapping

from pypdf.errors import PdfReadError
from pypdf.generic import (
    ArrayObject, ContentStream, DecodedStreamObject, DictionaryObject,
    FloatObject, IndirectObject, NameObject, StreamObject,
)


def _obj(value):
    return value.get_object() if isinstance(value, IndirectObject) else value


def _key(value):
    if isinstance(value, IndirectObject):
        return (id(value.pdf), value.idnum, value.generation)
    return ('direct', id(value))


def _groups(value, seen=None):
    """Resolve OCGs in a group or OCMD, including visibility expressions."""
    seen = set() if seen is None else seen
    key = _key(value)
    if key in seen:
        return
    seen.add(key)
    node = _obj(value)
    if isinstance(node, ArrayObject):
        for item in node:
            yield from _groups(item, seen)
    elif isinstance(node, DictionaryObject):
        if node.get('/Type') == '/OCG':
            yield value
        elif node.get('/Type') == '/OCMD' or '/OCGs' in node or '/VE' in node:
            yield from _groups(node.get('/OCGs'), seen)
            yield from _groups(node.get('/VE'), seen)


def content_references(page):
    """Return original stream references; reject direct/null/invalid entries."""
    if '/Contents' not in page:
        return []
    raw = page.raw_get('/Contents')
    resolved = _obj(raw)
    entries = list(resolved) if isinstance(resolved, ArrayObject) else [raw]
    for entry in entries:
        if not isinstance(entry, IndirectObject):
            raise ValueError('/Contents entries must be indirect stream references (no direct/null entries).')
        if not isinstance(_obj(entry), StreamObject):
            raise ValueError('/Contents reference does not resolve to a stream (null/invalid entry).')
    return entries


def _resources(page):
    node = page; seen = set()
    while isinstance(node, DictionaryObject):
        if id(node) in seen:
            raise ValueError('Cycle in inherited page resources.')
        seen.add(id(node))
        if '/Resources' in node:
            resources = _obj(node.get('/Resources'))
            if not isinstance(resources, DictionaryObject):
                raise ValueError('Page /Resources must be a dictionary.')
            return resources
        node = _obj(node.get('/Parent'))
    return DictionaryObject()


def _operations(stream, owner):
    if stream is None:
        return []
    return ContentStream(stream, owner).operations


def page_ocgs(page):
    """Discover resource, nested Form, annotation and inline-content OCGs."""
    found = {}; visited = set()
    owner = page.indirect_reference.pdf if page.indirect_reference else None

    def collect(value):
        for ref in _groups(value):
            found[_key(ref)] = ref

    def walk(stream, resources):
        for value in _obj(resources.get('/Properties', DictionaryObject())).values():
            collect(value)
        for operands, operator in _operations(stream, owner):
            if operator == b'BDC' and len(operands) == 2 and operands[0] == '/OC':
                # Named property entries were scanned above; inline OCMDs may
                # carry additional indirect OCG references.
                if not isinstance(operands[1], NameObject):
                    collect(operands[1])
        xobjects = _obj(resources.get('/XObject', DictionaryObject()))
        for raw in xobjects.values():
            key = _key(raw)
            if key in visited:
                continue
            visited.add(key)
            form = _obj(raw)
            if not isinstance(form, DictionaryObject):
                continue
            collect(form.get('/OC'))
            if form.get('/Subtype') == '/Form':
                child = _obj(form.get('/Resources', resources))
                walk(form, child)

    walk(page.get('/Contents'), _resources(page))
    for raw in _obj(page.get('/Annots', ArrayObject())):
        annotation = _obj(raw)
        if isinstance(annotation, DictionaryObject):
            collect(annotation.get('/OC'))
    return list(found.values())


def _owned_page(writer, page):
    if isinstance(page, int) and not isinstance(page, bool):
        if not 1 <= page <= len(writer.pages):
            raise ValueError('Plan page number is outside the writer (1-based).')
        page = writer.pages[page - 1]
    if not getattr(page, 'indirect_reference', None) or page.indirect_reference.pdf is not writer:
        raise ValueError('Clone/add the page into this writer before adding references.')
    return page


def _ocg_reference(writer, ocg):
    ref = ocg if isinstance(ocg, IndirectObject) else getattr(ocg, 'indirect_reference', None)
    if ref is None and isinstance(ocg, DictionaryObject):
        if ocg.get('/Type') != '/OCG' or not ocg.get('/Name'):
            raise ValueError('Expected a named /OCG dictionary.')
        ref = writer._add_object(ocg)
    if not isinstance(ref, IndirectObject) or ref.pdf is not writer:
        raise ValueError('OCG must belong to this writer; clone foreign objects first.')
    node = _obj(ref)
    if not isinstance(node, DictionaryObject) or node.get('/Type') != '/OCG' or not node.get('/Name'):
        raise ValueError('Expected a named /OCG dictionary.')
    return ref


def add_flattened_layer(writer, page, ocg, content_ops, name, *, resources=None):
    """Append one /OC Form invocation; return the new Form's indirect reference.

    ``name`` is a PDF resource-name stem; collisions receive a numeric suffix.
    ``resources`` optionally supplies the Form's fonts/graphics resources;
    otherwise it snapshots the page's resources before registering the Form.
    Existing content references and bytes, annotations and page geometry stay
    unchanged. This does not register the catalog OCGs: call declare_page_ocgs.
    """
    page = _owned_page(writer, page)
    existing = content_references(page)  # Refuse malformed input, not a silent repair.
    data = content_ops.encode('ascii') if isinstance(content_ops, str) else bytes(content_ops)
    if not data.strip():
        raise ValueError('Reference content must not be empty.')
    if not isinstance(name, str) or not name.lstrip('/') or any(c not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-' for c in name.lstrip('/')):
        raise ValueError('Use a nonempty ASCII PDF resource-name stem.')
    ref = _ocg_reference(writer, ocg)
    page_resources = DictionaryObject(_resources(page))
    form_resources = DictionaryObject(_obj(resources) if resources is not None else page_resources)
    xobjects = DictionaryObject(_obj(page_resources.get('/XObject', DictionaryObject())))
    stem = '/' + name.lstrip('/'); chosen = stem; suffix = 1
    while chosen in xobjects:
        chosen = f'{stem}_{suffix}'; suffix += 1
    form = DecodedStreamObject(); form.set_data(data)
    form.update({NameObject('/Type'): NameObject('/XObject'),
                 NameObject('/Subtype'): NameObject('/Form'),
                 NameObject('/BBox'): ArrayObject([FloatObject(v) for v in page.mediabox]),
                 NameObject('/Resources'): form_resources, NameObject('/OC'): ref})
    form_ref = writer._add_object(form)
    xobjects[NameObject(chosen)] = form_ref
    page_resources[NameObject('/XObject')] = xobjects
    # Isolate the existing drawing without rewriting its streams: a valid CAD
    # background may leave a transformed CTM/color/clip active at its end.
    prefix = []
    if existing:
        guard = DecodedStreamObject(); guard.set_data(b'q\n')
        prefix = [writer._add_object(guard)]
    invocation = DecodedStreamObject()
    invocation.set_data((('Q\n' if existing else '') + f'q\n{chosen} Do\nQ\n').encode('ascii'))
    invocation_ref = writer._add_object(invocation)
    page[NameObject('/Resources')] = page_resources
    page[NameObject('/Contents')] = ArrayObject(prefix + existing + [invocation_ref])
    return form_ref


def _unique(refs):
    seen = set(); result = []
    for ref in refs:
        if _key(ref) not in seen:
            seen.add(_key(ref)); result.append(ref)
    return result


def declare_page_ocgs(writer, plan_pages, markup_layers, include_background_in_order=False):
    """Register markup + reachable page OCGs ON, preserving other configuration.

    Pages are writer-owned PageObjects or 1-based page numbers. New background
    groups are omitted from /Order by default. Existing order/configurations and
    unrelated groups' visibility are retained; explicitly included groups are ON.
    """
    pages = [_owned_page(writer, p) for p in plan_pages]
    markup = [_ocg_reference(writer, r) for r in markup_layers]
    backgrounds = []
    for page in pages:
        for ref in page_ocgs(page):
            if not isinstance(ref, IndirectObject):
                raise ValueError('Referenced background OCG must be indirect; repair the source explicitly.')
            backgrounds.append(_ocg_reference(writer, ref))
    included = _unique(markup + backgrounds)
    props = DictionaryObject(_obj(writer.root_object.get('/OCProperties', DictionaryObject())))
    current = list(_obj(props.get('/OCGs', ArrayObject())))
    for ref in current:
        _ocg_reference(writer, ref)
    props[NameObject('/OCGs')] = ArrayObject(_unique(current + included))
    default = DictionaryObject(_obj(props.get('/D', DictionaryObject())))
    default[NameObject('/ON')] = ArrayObject(_unique(list(_obj(default.get('/ON', ArrayObject()))) + included))
    keys = {_key(r) for r in included}
    default[NameObject('/OFF')] = ArrayObject([r for r in _obj(default.get('/OFF', ArrayObject())) if _key(r) not in keys])
    order = list(_obj(default.get('/Order', ArrayObject())))
    ordered = {_key(r) for item in order for r in _groups(item)}
    for ref in _unique(markup + (backgrounds if include_background_in_order else [])):
        if _key(ref) not in ordered:
            order.append(ref); ordered.add(_key(ref))
    default[NameObject('/Order')] = ArrayObject(order)
    props[NameObject('/D')] = default
    writer.root_object[NameObject('/OCProperties')] = props
    return included


_PAINT = {b'S', b's', b'f', b'F', b'f*', b'B', b'B*', b'b', b'b*',
          b'Tj', b'TJ', b"'", b'"', b'sh', b'INLINE IMAGE'}


def _painted_groups(page):
    """Find OCGs on invoked paint operations, not merely unused resources.

    This is potential painting only: clipping, color/opacity, OCMD logic and
    viewer behavior still require rendering verification.
    """
    painted = set()
    owner = page.indirect_reference.pdf

    def walk(stream, resources, active, ancestors):
        stack = [set(active)]
        properties = _obj(resources.get('/Properties', DictionaryObject()))
        xobjects = _obj(resources.get('/XObject', DictionaryObject()))
        for operands, operator in _operations(stream, owner):
            if operator in (b'BDC', b'BMC'):
                groups = set(stack[-1])
                if operator == b'BDC' and len(operands) == 2 and operands[0] == '/OC':
                    value = properties.get(operands[1]) if isinstance(operands[1], NameObject) else operands[1]
                    groups.update(_key(r) for r in _groups(value))
                stack.append(groups)
            elif operator == b'EMC':
                if len(stack) > 1:
                    stack.pop()
            elif operator == b'Do' and operands:
                raw = xobjects.get(operands[0]); form = _obj(raw)
                if not isinstance(form, StreamObject):
                    continue
                active_groups = stack[-1] | {_key(r) for r in _groups(form.get('/OC'))}
                if form.get('/Subtype') == '/Form' and _key(raw) not in ancestors:
                    walk(form, _obj(form.get('/Resources', resources)), active_groups, ancestors | {_key(raw)})
                elif form.get('/Subtype') == '/Image' and form.get_data():
                    painted.update(active_groups)
            elif operator in _PAINT:
                painted.update(stack[-1])

    walk(page.get('/Contents'), _resources(page), set(), set())
    return painted


def reference_structure_issues(reader, plan_pages, reference_layers=None):
    """Structural FRL checks, independent of live-annotation identity checks.

    reference_layers is a name sequence required on every selected plan page,
    or a mapping of names to the 1-based pages that should contain them.
    """
    issues = []
    try:
        props = _obj(reader.trailer['/Root'].get('/OCProperties', DictionaryObject()))
        declared = list(_obj(props.get('/OCGs', ArrayObject())))
        default = _obj(props.get('/D', DictionaryObject()))
        declared_keys = {_key(r) for r in declared}
        on = {_key(r) for r in _obj(default.get('/ON', ArrayObject()))}
        off = {_key(r) for r in _obj(default.get('/OFF', ArrayObject()))}
        names = {}
        for ref in declared:
            node = _obj(ref)
            if not isinstance(ref, IndirectObject) or not isinstance(node, DictionaryObject) or node.get('/Type') != '/OCG':
                issues.append('Catalog /OCGs entries must be indirect OCG references.'); continue
            names.setdefault(str(node.get('/Name', '')), []).append(ref)
    except (AttributeError, TypeError, ValueError, PdfReadError) as error:
        return ['Invalid optional-content catalog: ' + str(error)]
    required = (dict(reference_layers) if isinstance(reference_layers, Mapping)
                else {name: plan_pages for name in (reference_layers or [])})
    for name, pages in required.items():
        if not pages or any(p not in plan_pages for p in pages):
            issues.append(f'Reference layer {name}: expected pages must be selected plan pages.')
        matches = names.get(name, [])
        if len(matches) != 1:
            issues.append(f'Reference layer {name}: must be declared exactly once by name.'); continue
        key = _key(matches[0])
        if key in off or (key not in on and default.get('/BaseState', '/ON') != '/ON'):
            issues.append(f'Reference layer {name}: must be default ON.')
    for number in plan_pages:
        if not isinstance(number, int) or isinstance(number, bool) or not 1 <= number <= len(reader.pages):
            continue  # Main live checker reports invalid page numbers.
        page = reader.pages[number - 1]
        try:
            content_references(page)
        except (TypeError, ValueError, PdfReadError) as error:
            issues.append(f'Plan page {number}: {error}')
        try:
            for ref in page_ocgs(page):
                if not isinstance(ref, IndirectObject) or _key(ref) not in declared_keys:
                    issues.append(f'Plan page {number}: referenced OCG missing from catalog /OCGs or not indirect.')
            if required:
                painted = _painted_groups(page)
                for name, pages in required.items():
                    matches = names.get(name, [])
                    if number in pages and len(matches) == 1 and _key(matches[0]) not in painted:
                        issues.append(f'Plan page {number}: reference layer {name} has no invoked non-empty painting content.')
        except (AttributeError, TypeError, ValueError, PdfReadError) as error:
            issues.append(f'Plan page {number}: cannot inspect reference content/resources: {error}')
    return issues
