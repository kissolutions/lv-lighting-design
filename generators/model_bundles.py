"""v0.9 flat power-bundle records. No routing, cycle repair or electrical approval."""
from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import json
import math
from collections import defaultdict
from decimal import Decimal
from pathlib import Path

from jsonschema import Draft202012Validator

from .model_access import iter_power_units

SCHEMAS = Path(__file__).resolve().parents[1] / 'schemas'
RECORD_SCHEMA = json.loads((SCHEMAS / 'bundle-records-v0.9.schema.json').read_text())
TABLES = RECORD_SCHEMA['properties']


def empty_records():
    return {name: [] for name in TABLES}


def bundle_id(serves, flow='upstream'):
    """Canonical UTF-8 sorted set; full SHA256, never sequence numbering."""
    if flow not in ('upstream', 'drop') or not serves or len(set(serves)) != len(serves):
        raise ValueError('Identity requires a nonempty unique served set and known flow.')
    encoded = json.dumps(sorted(serves), ensure_ascii=False, separators=(',', ':')).encode()
    return ('B-' if flow == 'upstream' else 'D-') + hashlib.sha256(encoded).hexdigest()


def upgrade_v09(model):
    """Explicit copy migration; never infer routes from positions or signal paths."""
    from .model_intake_review import upgrade_v08
    if model.get('schema_version') == '0.9.0':
        return copy.deepcopy(model)
    value = upgrade_v08(model)
    errors = list(Draft202012Validator(json.loads(
        (SCHEMAS / 'lighting-project-v0.8.schema.json').read_text())).iter_errors(value))
    if errors:
        raise ValueError('Invalid migration source: ' + errors[0].message)
    value['schema_version'] = '0.9.0'
    value['bundle_routes'] = empty_records()
    return value


def _index(rows, key):
    result = {}
    for row in rows:
        if row[key] in result:
            raise ValueError(f'Duplicate {key}: {row[key]}; do not deduplicate.')
        result[row[key]] = row
    return result


def _shape(records):
    errors = list(Draft202012Validator(RECORD_SCHEMA).iter_errors(records))
    if errors:
        e = errors[0]
        raise ValueError(f'{"/".join(map(str, e.path))}: {e.message}')
    for table in ('frames', 'geometry', 'attachments'):
        for row in records[table]:
            for value in row.values():
                if isinstance(value, (float, int, Decimal)) and not math.isfinite(value):
                    raise ValueError('Nonfinite coordinate, station or calibration.')


def _point(points, station, offset, scale):
    remaining = float(station) / scale
    for a, b in zip(points, points[1:]):
        dx, dy = b[0]-a[0], b[1]-a[1]
        length = math.hypot(dx, dy)
        if remaining <= length + 1e-8:
            t = min(remaining / length, 1)
            return (a[0]+t*dx-float(offset)/scale*dy/length,
                    a[1]+t*dy+float(offset)/scale*dx/length)
        remaining -= length
    raise ValueError('Station outside geometry.')


def build(records, model=None):
    """Validate all references before deriving a read-only tree/count/position view.

    With model=None, validate the standalone flat set only. Project-reference
    validation is mandatory when integrating into a lighting-project export.
    """
    _shape(records)
    frames = _index(records['frames'], 'frame_id')
    bundles = _index(records['bundles'], 'bundle_id')
    cables = _index(records['cables'], 'cable_id')
    circuits = _index(records['circuits'], 'circuit_id')
    attachments = _index(records['attachments'], 'controller_id')
    _index(records['bundles'], 'annotation_id')
    children = defaultdict(list)
    for bid, b in bundles.items():
        parent = b['parent_bundle_id']
        if parent is not None and parent not in bundles:
            raise ValueError(f'{bid}: unknown parent {parent}')
        children[parent].append(bid)
    # Parent walks detect disconnected cycles too; edge count alone cannot.
    done = set()
    for start in bundles:
        path, seen, cursor = [], set(), start
        while cursor is not None and cursor not in done:
            if cursor in seen:
                cycle = path[path.index(cursor):] + [cursor]
                raise ValueError('Cycle edges: ' + ', '.join(
                    f'{a} -> {b}' for a, b in zip(cycle, cycle[1:])))
            seen.add(cursor); path.append(cursor)
            cursor = bundles[cursor]['parent_bundle_id']
        done.update(path)
    for bid, b in bundles.items():
        if b['serves'] != sorted(set(b['serves'])) or bid != bundle_id(b['serves'], b['flow']):
            raise ValueError(f'{bid}: identity must hash the canonical ordered served set.')
        f = frames.get(b['frame_id'])
        if not f or f['level'] != b['level']:
            raise ValueError(f'{bid}: missing or mismatched calibrated frame/level.')
        p = bundles.get(b['parent_bundle_id'])
        if p and any(p[k] != b[k] for k in ('flow', 'source_id', 'frame_id', 'level')):
            raise ValueError(f'{bid}: cross-flow/source/frame/level edge; explicit riser support required.')
    points = defaultdict(list)
    for g in records['geometry']:
        if g['bundle_id'] not in bundles:
            raise ValueError('Geometry references unknown bundle: ' + g['bundle_id'])
        points[g['bundle_id']].append(g)
    lengths, polylines = {}, {}
    for bid, b in bundles.items():
        rows = sorted(points[bid], key=lambda g:g['seq'])
        if len(rows) < 2 or [g['seq'] for g in rows] != list(range(len(rows))):
            raise ValueError(f'{bid}: requires contiguous unique vertex sequence starting at zero.')
        xy = [(float(g['x']), float(g['y'])) for g in rows]
        spans = [math.dist(a, c) for a, c in zip(xy, xy[1:])]
        if any(s <= 0 for s in spans):
            raise ValueError(f'{bid}: zero-length segment.')
        lengths[bid] = sum(spans)*float(frames[b['frame_id']]['feet_per_unit'])
        polylines[bid] = xy
    for bid, b in bundles.items():
        parent = b['parent_bundle_id']
        if parent and math.dist(polylines[parent][-1], polylines[bid][0]) > 1e-7:
            raise ValueError(f'{bid}: disconnected parent/child geometry.')
    terminating = defaultdict(list)
    positions = []
    for cid, a in attachments.items():
        bid = a['parent_bundle_id']; b = bundles.get(bid)
        if not b or b['flow'] != 'upstream' or cid not in b['serves']:
            raise ValueError(f'{cid}: invalid upstream attachment.')
        if float(a['station_ft']) > lengths[bid]+1e-8:
            raise ValueError(f'{cid}: station exceeds parent length.')
        terminating[bid].append(cid)
        x, y = _point(polylines[bid], a['station_ft'], a['offset_ft'],
                      float(frames[b['frame_id']]['feet_per_unit']))
        positions.append(dict(controller_id=cid, frame_id=b['frame_id'], x=x, y=y))
    position_by_id = {p['controller_id']:p for p in positions}
    for bid,b in bundles.items():
        if b['flow']=='drop' and b['source_id'] in position_by_id:
            p=position_by_id[b['source_id']]
            if p['frame_id'] != b['frame_id'] or math.dist(polylines[bid][0],(p['x'],p['y'])) > 1e-7:
                raise ValueError(f'{bid}: drop start differs from controller position.')
    endpoints = {}
    for bid, b in bundles.items():
        if b['flow'] == 'upstream':
            for cid in terminating[bid]:
                endpoints[('upstream', cid)] = bid
        else:
            # Drops are one-level channel branches, not controller-set bundles.
            if b['parent_bundle_id'] is not None or len(b['serves']) != 1:
                raise ValueError(f'{bid}: drop scope is one root per output channel.')
            key = ('drop', b['serves'][0])
            if key in endpoints:
                raise ValueError('Duplicate drop endpoint.')
            endpoints[key] = bid
    cable_ends = defaultdict(list)
    for cid, c in cables.items():
        bid = endpoints.get((c['flow'], c['endpoint_id']))
        if bid is None or bundles[bid]['source_id'] != c['source_id']:
            raise ValueError(f'{cid}: cable endpoint/source does not match tree.')
        cable_ends[bid].append(cid)
    for (flow, endpoint), bid in endpoints.items():
        if not any(c['flow']==flow and c['endpoint_id']==endpoint for c in cables.values()):
            raise ValueError(f'{endpoint}: no physical cable mapped to endpoint.')
    used_ports = set()
    for cid, circuit in circuits.items():
        cable = cables.get(circuit['cable_id'])
        if not cable:
            raise ValueError(f'{cid}: unknown physical cable.')
        for end, device, port in (
            ('source', cable['source_id'], circuit['source_port']),
            ('destination', cable['endpoint_id'], circuit['destination_port'])):
            key = (cable['flow'], end, device, port)
            if key in used_ports:
                raise ValueError(f'{cid}: reused {end} port {device}:{port}.')
            used_ports.add(key)
    conductor_keys, groups = set(), defaultdict(list)
    for c in records['conductors']:
        cable = cables.get(c['cable_id']); circuit = circuits.get(c['circuit_id'])
        key = (c['cable_id'], c['conductor_number'])
        if not cable or not circuit or circuit['cable_id'] != c['cable_id']:
            raise ValueError('Conductor references unknown or different cable/circuit.')
        if key in conductor_keys or c['conductor_number'] > cable['conductor_count']:
            raise ValueError('Duplicate or out-of-range conductor number.')
        conductor_keys.add(key)
        groups[(c['cable_id'], c['parallel_group'])].append(c)
    for group in groups.values():
        if len({(c['circuit_id'], c['polarity'], c['effective_gauge']) for c in group}) != 1:
            raise ValueError('Parallel group mixes circuits, polarity or effective gauge.')
    for cid, c in circuits.items():
        poles = {r['polarity'] for r in records['conductors'] if r['circuit_id'] == cid}
        if poles != {'positive', 'negative'}:
            raise ValueError(f'{cid}: circuit requires positive and negative conductors.')
    for cid in cables:
        if not any(c['cable_id'] == cid for c in circuits.values()):
            raise ValueError(f'{cid}: cable has no circuit mapping.')
    derived = {}
    # Iterative postorder handles long chains without recursion limits.
    order, pending = [], list(children[None])
    while pending:
        bid = pending.pop(); order.append(bid); pending.extend(children[bid])
    for bid in reversed(order):
        b = bundles[bid]
        served = list(terminating[bid]) if b['flow'] == 'upstream' else list(b['serves'])
        child_rows = [derived[c] for c in children[bid]]
        for child in child_rows:
            served.extend(child['serves'])
        if len(served) != len(set(served)) or sorted(served) != b['serves']:
            raise ValueError(f'{bid}: served set differs from disjoint children plus terminations.')
        local_cables = cable_ends[bid]
        all_cables = local_cables + [c for child in child_rows for c in child['cable_ids']]
        if not all_cables:
            raise ValueError(f'{bid}: no physical cables for served endpoints.')
        derived[bid] = dict(bundle_id=bid, serves=sorted(served), flow=b['flow'],
            controllers_terminating=sorted(terminating[bid]), cables_terminating=len(local_cables),
            downstream_controllers=len(served) if b['flow']=='upstream' else 0,
            downstream_cables=len(all_cables), cable_ids=sorted(all_cables),
            length_ft=lengths[bid])
    if model is not None:
        controllers = {c['id']:c for c in model['controllers']}
        units = {u['id']:u for u in iter_power_units(model)}
        channels = {c['id']:c for u in units.values() for c in u['channels']}
        pages = {p['id']:p for p in model['drawing_pages']}
        assumptions = {a['id'] for a in model['assumptions']}
        for f in frames.values():
            if f['drawing_page_id'] not in pages:
                raise ValueError('Unknown drawing page: ' + f['drawing_page_id'])
        for bid,b in bundles.items():
            page=pages[frames[b['frame_id']]['drawing_page_id']]
            if any(x<0 or y<0 or x>page['width_pt'] or y>page['height_pt'] for x,y in polylines[bid]):
                raise ValueError(f'{bid}: geometry outside displayed page.')
        for b in bundles.values():
            sources = units if b['flow']=='upstream' else controllers
            targets = controllers if b['flow']=='upstream' else channels
            if b['source_id'] not in sources or any(e not in targets for e in b['serves']):
                raise ValueError(f'{b["bundle_id"]}: unknown canonical source/endpoint.')
            if set(b['assumption_ids']) - assumptions:
                raise ValueError('Unknown route assumption.')
        for b in bundles.values():
            if b['flow']=='drop':
                channel = channels[b['serves'][0]]
                if channel.get('controller_id') != b['source_id']:
                    raise ValueError('Drop output channel is not assigned to its source controller.')
    cable_lengths = {}
    for cid, cable in cables.items():
        bid = endpoints[(cable['flow'], cable['endpoint_id'])]
        length = (float(attachments[cable['endpoint_id']]['station_ft'])
                  if cable['flow']=='upstream' else lengths[bid])
        parent = bundles[bid]['parent_bundle_id']
        while parent is not None:
            length += lengths[parent]; parent = bundles[parent]['parent_bundle_id']
        cable_lengths[cid] = length
    totals = {}
    for flow in ('upstream', 'drop'):
        roots = [derived[x] for x in children[None] if bundles[x]['flow']==flow]
        totals[flow] = dict(cables=sum(r['downstream_cables'] for r in roots),
                           controllers=sum(r['downstream_controllers'] for r in roots),
                           cable_centerline_ft=sum(cable_lengths[cid] for cid,c in cables.items() if c['flow']==flow))
    return dict(bundles=[derived[b] for b in sorted(derived)], controller_positions=positions,
                totals=totals, cable_centerline_ft=cable_lengths, installed_length_validated=False, electrical_routing_validated=False)


def check_v09(model, phase='intake'):
    from .model_intake_review import check_v08
    errors = list(Draft202012Validator(json.loads(
        (SCHEMAS/'lighting-project-v0.9.schema.json').read_text())).iter_errors(model))
    issues = [dict(rule='schema', entity_id='/'.join(map(str,e.path)), message=e.message) for e in errors]
    bundle_view = None
    if not issues:
        try:
            bundle_view = build(model['bundle_routes'], model)
        except ValueError as e:
            issues.append(dict(rule='bundle-tree', entity_id='bundle_routes', message=str(e)))
    if issues:
        return dict(checks_pass=False, phase=phase, issues=issues, deferred_issues=[], derived=None)
    projected = copy.deepcopy(model); projected.pop('bundle_routes'); projected['schema_version']='0.8.0'
    # v0.9-only color attributes remain authoritative in the original model.
    # Strip them only from the v0.8 compatibility projection, whose strict schema
    # predates the optional paired-fixture schedule CCT/CRI fields.
    for fixture in projected['fixture_types']:
        for key in ('source_cct_k', 'source_cri'):
            fixture.pop(key, None)
    for light in projected['light_objects']:
        for key in ('selected_cct_k', 'selected_cri'):
            light['design'].pop(key, None)
    report = check_v08(projected, phase)
    if report['derived'] is not None:
        report['derived']['bundle_routes'] = bundle_view
    return report


def read_tables(directory):
    """CSV scalar cells; array cells use JSON. Every header is exact and required."""
    records = empty_records()
    for name, schema in TABLES.items():
        props = schema['items']['properties']
        with (Path(directory)/(name+'.csv')).open(newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            if reader.fieldnames != list(props):
                raise ValueError(f'{name}: incorrect CSV header.')
            for row in reader:
                if None in row or any(v is None for v in row.values()):
                    raise ValueError(f'{name}: malformed CSV row.')
                decoded = {}
                for k, v in row.items():
                    p = props[k]
                    if v == '' and 'anyOf' in p:
                        decoded[k] = None
                    elif p.get('type') in ('array', 'number', 'integer'):
                        decoded[k] = json.loads(v)
                    else:
                        decoded[k] = v
                records[name].append(decoded)
    build(records)
    return records


def write_tables(records, directory):
    """Write a new revision, never overwrite authoritative source tables in place."""
    build(records)
    directory = Path(directory)
    if directory.exists() and any(directory.iterdir()):
        raise ValueError('Choose an empty directory for the new table revision.')
    directory.mkdir(parents=True, exist_ok=True)
    for name, schema in TABLES.items():
        fields = list(schema['items']['properties'])
        with (directory/(name+'.csv')).open('w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fields); writer.writeheader()
            for row in records[name]:
                writer.writerow({k:json.dumps(v, ensure_ascii=False) if isinstance(v,list)
                                 else ('' if v is None else v) for k,v in row.items()})


def apply_geometry_return(records, returned):
    """Strict full-issued-set readback adapter. Input comes from live annotation extraction.

    Does not itself extract a PDF, grant acceptance, or change source records.
    """
    before = build(records)
    issued = _index(records['bundles'], 'annotation_id')
    received = _index(returned, 'annotation_id')
    if set(issued) != set(received):
        raise ValueError(f'Annotation reconciliation required; missing={sorted(set(issued)-set(received))}; '
                         f'unknown={sorted(set(received)-set(issued))}')
    result = copy.deepcopy(records); geometry = []; changed = []
    for aid, b in issued.items():
        r = received[aid]
        for field in ('bundle_id', 'parent_bundle_id', 'serves', 'source_id', 'flow', 'frame_id'):
            if r.get(field) != b[field]:
                raise ValueError(f'{aid}: topology/frame change ({field}); explicit reconciliation required.')
        new = [dict(bundle_id=b['bundle_id'], seq=i, x=p[0], y=p[1])
               for i,p in enumerate(r['vertices']) if len(p)==2]
        if len(new) != len(r['vertices']):
            raise ValueError('Vertices must be coordinate pairs.')
        old = sorted((g for g in records['geometry'] if g['bundle_id']==b['bundle_id']), key=lambda g:g['seq'])
        if new != old:
            changed.append(b['bundle_id'])
        geometry.extend(new)
    result['geometry'] = geometry
    after = build(result)
    oldpos = {p['controller_id']:p for p in before['controller_positions']}
    for p in after['controller_positions']:
        a = next(a for a in records['attachments'] if a['controller_id']==p['controller_id'])
        if a['review_status']=='accepted' and a['location_basis']=='owner_returned' and p != oldpos[p['controller_id']]:
            raise ValueError(f'{p["controller_id"]}: geometry would move an accepted owner-returned device; reconcile station/offset.')
    invalidated = sorted({a for b in records['bundles'] if b['bundle_id'] in changed for a in b['assumption_ids']})
    return dict(records=result, derived=after, changed_bundle_ids=changed,
                invalidated_assumption_ids=invalidated,
                recompute_required=['voltage_drop','conductor_selection','labour','drop_distances'] if changed else [])


def apply_model_geometry_return(model, returned):
    """Reconcile a model export; callers write returned flat tables as a new revision."""
    result = apply_geometry_return(model['bundle_routes'], returned)
    updated = copy.deepcopy(model)
    updated['bundle_routes'] = result['records']
    for assumption in updated['assumptions']:
        if assumption['id'] in result['invalidated_assumption_ids']:
            assumption['status'] = 'invalidated'
    build(updated['bundle_routes'], updated)
    return updated, result


def nested_view(records):
    """On-demand read-only view, never authoritative storage."""
    report = build(records)
    nodes = {r['bundle_id']:dict(r, children=[]) for r in report['bundles']}
    roots = []
    for row in records['bundles']:
        if row['parent_bundle_id'] is None:
            roots.append(nodes[row['bundle_id']])
        else:
            nodes[row['parent_bundle_id']]['children'].append(nodes[row['bundle_id']])
    return roots


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('model', type=Path)
    parser.add_argument('--tables', type=Path, help='Authoritative CSV directory; overrides any bundle export.')
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    from .validate_model import read_model
    from .model_intake import model_json
    model = upgrade_v09(read_model(args.model))
    if args.tables:
        model['bundle_routes'] = read_tables(args.tables)
    elif model['bundle_routes']['bundles']:
        parser.error('Regenerate nonempty routing exports from authoritative --tables.')
    build(model['bundle_routes'], model)
    if args.output.exists():
        parser.error('Output exists; choose a new export revision.')
    args.output.write_text(model_json(model)+'\n')


if __name__ == '__main__':
    main()
