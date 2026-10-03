"""Draft v0.3 Space membership, conditions, and derived fixture-count views."""
from __future__ import annotations

import argparse
import copy
import json
from collections import Counter, defaultdict
from decimal import Decimal
from pathlib import Path

from jsonschema import Draft202012Validator

from .model_hierarchy import check_model as check_hierarchy, load_watts
from .validate_model import read_model

SCHEMA = Path(__file__).resolve().parents[1] / 'schemas/lighting-project-v0.3.schema.json'


def check_model(model):
    issues = []
    def fail(rule, entity_id, message):
        issues.append({'rule': rule, 'entity_id': entity_id, 'message': message})

    schema = json.loads(SCHEMA.read_text())
    for error in Draft202012Validator(schema).iter_errors(model):
        fail('schema', '/'.join(map(str, error.absolute_path)) or 'model', error.message)
    if issues:
        return {'checks_pass': False, 'issues': issues, 'derived': None}

    def object_ids(value):
        if isinstance(value, dict):
            if 'id' in value:
                yield value['id']
            for child in value.values():
                yield from object_ids(child)
        elif isinstance(value, list):
            for child in value:
                yield from object_ids(child)
    for identifier, count in Counter(object_ids(model)).items():
        if count > 1:
            fail('unique-ids', identifier, 'An ID has more than one authoritative object.')
    if issues:
        return {'checks_pass': False, 'issues': issues, 'derived': None}

    # Project only the unchanged v0.2 hierarchy; never mutate the submitted model.
    hierarchy = copy.deepcopy(model)
    hierarchy['schema_version'] = '0.2.0'
    hierarchy.pop('spaces')
    hierarchy['project'].pop('energy_code_basis')
    for zone in hierarchy['light_zones']:
        for light in zone['light_objects']:
            light.pop('mounting', None)
        for key in ['label_mode', 'control_area_sq_ft', 'control_area_basis']:
            zone.pop(key)
        if zone['label'] is None:
            zone['label'] = zone['id']
    base = check_hierarchy(hierarchy)
    issues.extend(base['issues'])
    if base['derived'] is None:
        return {'checks_pass': False, 'issues': issues, 'derived': None}

    spaces = {s['id']: s for s in model['spaces']}
    zones = {z['id']: z for z in model['light_zones']}
    lights = {light['id']: light for z in zones.values() for light in z['light_objects']}
    types = {f['id']: f for f in model['fixture_types']}
    light_zones = {light['id']: z['id'] for z in zones.values() for light in z['light_objects']}
    pages = {p['id']: p for p in model['drawing_pages']}
    refs = {r['id']: r for r in model['source_references']}
    decisions = {d['id']: d for d in model['decisions']}
    def reference(owner, value, index, nullable=False):
        if nullable and value is None:
            return
        if value not in index:
            fail('reference-integrity', owner, f'Missing referenced object: {value}')
    def confirmed(value):
        return value in decisions and decisions[value]['status'] == 'confirmed'

    basis = model['project']['energy_code_basis']
    reference(model['project']['id'], basis['decision_id'], decisions, True)
    for rid in basis['source_ref_ids']:
        reference(model['project']['id'], rid, refs)
    for s in spaces.values():
        sid = s['id']
        for value in s['drawing_page_ids']:
            reference(sid, value, pages)
        for value in s['source_ref_ids']:
            reference(sid, value, refs)
        for value in s['light_object_ids']:
            reference(sid, value, lights)
        for value in s['light_zone_ids']:
            reference(sid, value, zones)
        for value in [s['decision_id'], s['energy_classification_decision_id']]:
            reference(sid, value, decisions, True)
        for code in s['code_references']:
            reference(sid, code['decision_id'], decisions, True)
    for light in lights.values():
        for rid in light.get('mounting', {}).get('source_ref_ids', []):
            reference(light['id'], rid, refs)
    if any(i['rule'] == 'reference-integrity' for i in issues):
        return {'checks_pass': False, 'issues': issues, 'derived': None}

    membership = defaultdict(list)
    for s in spaces.values():
        sid = s['id']
        for lid in s['light_object_ids']:
            membership[lid].append(sid)
            page_id = lights[lid]['source']['drawing_page_id']
            if page_id is not None and page_id not in s['drawing_page_ids']:
                fail('space-source-page', lid, 'Light page is not registered for its Space.')
        actual_zones = {light_zones[lid] for lid in s['light_object_ids']}
        declared_zones = set(s['light_zone_ids'])
        if not actual_zones.issubset(declared_zones):
            fail('space-zone-membership', sid, 'Reference every zone containing this Space\'s lights.')
        for zid in declared_zones - actual_zones:
            if zones[zid]['label_mode'] != 'named' or not s['description'] or not confirmed(s['decision_id']):
                fail('space-zone-membership', sid, 'Additional shared-zone membership needs a named zone, description, and confirmed Space decision.')
    for lid in lights:
        if len(membership[lid]) != 1:
            fail('space-light-membership', lid, 'Each modeled light must be referenced by exactly one Space.')
    if any(i['rule'] in {'space-light-membership', 'space-zone-membership', 'space-source-page'} for i in issues):
        return {'checks_pass': False, 'issues': issues, 'derived': None}

    if not spaces:
        fail('space-completeness', model['project']['id'], 'Register the rooms/bounded areas containing the lights.')
    if (any(basis[k] is None for k in ['standard', 'edition', 'jurisdiction'])
            or basis['amendments_status'] == 'unreviewed' or not basis['source_ref_ids']
            or not confirmed(basis['decision_id'])):
        fail('energy-code-basis', model['project']['id'], 'Confirm the selected code, edition, jurisdiction, amendments, and evidence.')
    for s in spaces.values():
        sid = s['id']
        if s.get('inventory_only', False):
            if s['light_object_ids'] or s['light_zone_ids'] or not s['description']:
                fail('space-inventory-only', sid, 'An inventory-only service area needs a description and empty light/zone lists.')
            continue
        if not confirmed(s['decision_id']):
            fail('space-decision', sid, 'Confirm room conditions, membership, and their engineering basis.')
        if s['area_sq_ft'] is None or s['area_basis'] == 'unknown':
            fail('space-area', sid, 'Record area and whether it is sourced, measured, or estimated.')
        elif s['area_basis'] == 'estimated' and not s['area_note']:
            fail('space-area', sid, 'Preserve the estimate basis and threshold-review limitations.')
        if s['energy_code_space_type'] is None or s['energy_classification_basis'] == 'unknown' or s['enclosure'] is None:
            fail('space-energy-type', sid, 'Confirm the Energy Code Space Type and enclosure.')
        if s['energy_classification_basis'] in {'inferred', 'owner_classification'}:
            if not s['energy_classification_note'] or not confirmed(s['energy_classification_decision_id']):
                fail('space-energy-type', sid, 'An inferred/selected energy type requires an explanation and confirmed decision.')
        if any(s[k] is None for k in ['has_windows', 'has_daylight_zone', 'daylight_control_required']):
            fail('space-daylight-basis', sid, 'Assess window presence, geometric daylight zone, and required controls separately.')
        if (s['has_windows'] or s['has_daylight_zone']) and not s['daylight_assessment_note']:
            fail('space-daylight-basis', sid, 'Preserve the basis of the daylight assessment, including any control exemption.')
        if not s['code_references'] or any(c['applicability_status'] == 'provisional' for c in s['code_references']):
            fail('space-code-reference', sid, 'Record applicable code references and resolve provisional applicability.')
        for code in s['code_references']:
            if not confirmed(code['decision_id']):
                fail('space-code-reference', sid, 'Code applicability or exclusion needs a confirmed decision.')

    for light in lights.values():
        mounting = light.get('mounting')
        if mounting is None:
            continue
        height, basis = mounting['height_above_served_floor_ft'], mounting['height_basis']
        if height is None:
            fail('light-mounting-height', light['id'], 'Verify mounting height above the primary served floor; keep unknown height null.')
        elif basis == 'unknown' or not mounting['source_ref_ids']:
            fail('light-mounting-basis', light['id'], 'Known mounting height requires a stated basis and source evidence.')
        if basis == 'estimated' and not mounting['note']:
            fail('light-mounting-basis', light['id'], 'An estimated mounting height requires an estimate/verification note.')

    zone_spaces = {zid: sorted(sid for sid, s in spaces.items() if zid in s['light_zone_ids']) for zid in zones}
    display_labels, control_areas = {}, {}
    for zid, z in zones.items():
        area = z['control_area_sq_ft']
        if z['label_mode'] == 'room_default':
            if len(zone_spaces[zid]) != 1:
                fail('zone-room-default', zid, 'A room-default zone must serve exactly one Space.')
                display_labels[zid] = z['label'] or zid
            else:
                s = spaces[zone_spaces[zid][0]]
                display_labels[zid] = z['label'] or s['name']
                if set(l['id'] for l in z['light_objects']) != set(s['light_object_ids']):
                    fail('zone-room-default', zid, 'A room-default zone must cover all modeled lights in its Space.')
                if area is not None and s['area_sq_ft'] is not None and area != s['area_sq_ft']:
                    fail('zone-control-area', zid, 'Room-default control area must agree with the Space area.')
                if area is None:
                    area = s['area_sq_ft']
        else:
            display_labels[zid] = z['label']
            if area is None or z['control_area_basis'] == 'unknown':
                fail('zone-control-area', zid, 'Record named control-zone area and its basis for later code review.')
        control_areas[zid] = area

    def fixture_counts(ids):
        counts = Counter(lights[lid]['source']['fixture_type_id'] for lid in ids)
        return [{'fixture_type_id': fid, 'source_mark': types[fid]['source_mark'], 'quantity': counts[fid]} for fid in sorted(counts)]
    derived = copy.deepcopy(base['derived'])
    derived.update(
        light_space_ids={lid: membership[lid][0] for lid in lights}, zone_space_ids=zone_spaces,
        zone_display_labels=display_labels, zone_control_area_sq_ft=control_areas,
        space_fixture_counts={sid: fixture_counts(s['light_object_ids']) for sid, s in spaces.items()},
        zone_fixture_counts={zid: fixture_counts([l['id'] for l in z['light_objects']]) for zid, z in zones.items()},
        space_channel_ids={sid: sorted({lights[lid]['design']['channel_id'] for lid in s['light_object_ids'] if lights[lid]['design']['channel_id']}) for sid, s in spaces.items()},
        space_levels={sid: s.get('level') for sid, s in spaces.items()},
        light_mounting={lid: copy.deepcopy(l.get('mounting')) for lid, l in lights.items()},
        inventory_only_space_ids=sorted(sid for sid, s in spaces.items() if s.get('inventory_only', False)),
    )
    space_watts = {}
    for sid, s in spaces.items():
        values = [load_watts(lights[lid]['design']['load']) for lid in s['light_object_ids']]
        space_watts[sid] = None if any(v is None for v in values) else sum(values, Decimal(0))
    derived['space_connected_watts'] = space_watts
    return {'checks_pass': not issues, 'issues': issues, 'derived': derived}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('model', type=Path)
    args = parser.parse_args()
    try:
        result = check_model(read_model(args.model))
    except (OSError, ValueError) as error:
        parser.exit(2, f'Cannot read model: {error}\n')
    print(json.dumps(result, indent=2, default=lambda v: str(v) if isinstance(v, Decimal) else v))
    return 0 if result['checks_pass'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
