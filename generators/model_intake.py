"""Physical-first v0.4 intake checks; later design uses the existing engineering checks."""
from __future__ import annotations

import argparse
import copy
import json
from collections import Counter, defaultdict
from decimal import Decimal
from pathlib import Path

from jsonschema import Draft202012Validator

from .model_hierarchy import load_watts
from .model_spaces import check_model as check_spaces
from .validate_model import read_model

SCHEMA = Path(__file__).resolve().parents[1] / 'schemas/lighting-project-v0.4.schema.json'
PHASES = ('inventory', 'intake', 'design')


def model_json(value, level=0):
    """Preserve Decimal JSON numbers, including values just above an engineering limit."""
    if isinstance(value, Decimal):
        if not value.is_finite():
            raise ValueError('Non-finite model number.')
        return str(value)
    if isinstance(value, dict):
        if not value:
            return '{}'
        rows = ['  ' * (level + 1) + json.dumps(k) + ': ' + model_json(v, level + 1)
                for k, v in value.items()]
        return '{\n' + ',\n'.join(rows) + '\n' + '  ' * level + '}'
    if isinstance(value, list):
        if not value:
            return '[]'
        rows = ['  ' * (level + 1) + model_json(v, level + 1) for v in value]
        return '[\n' + ',\n'.join(rows) + '\n' + '  ' * level + ']'
    return json.dumps(value, allow_nan=False)


def migrate_v03(model):
    """Move existing physical records without guessing boundaries or removing zones."""
    if model.get('schema_version') not in ('0.3.0', '0.3.1'):
        raise ValueError('Migration requires a v0.3 model.')
    legacy_schema = json.loads(SCHEMA.with_name('lighting-project-v0.3.schema.json').read_text())
    error = next(Draft202012Validator(legacy_schema).iter_errors(model), None)
    if error is not None:
        raise ValueError(f'Invalid legacy structure: {error.message}')
    result = copy.deepcopy(model)
    result['schema_version'] = '0.4.0'
    result['light_objects'] = []
    for zone in result['light_zones']:
        lights = zone.pop('light_objects')
        result['light_objects'].extend(lights)
        zone['light_object_ids'] = [light['id'] for light in lights]
        if zone['label_mode'] == 'room_default':
            zone['label_mode'] = 'room'
    return result


def check_model(model, phase='intake'):
    if phase not in PHASES:
        raise ValueError(f'Unknown phase: {phase}')
    issues, deferred = [], []

    def fail(rule, owner, message):
        issues.append(dict(rule=rule, entity_id=owner, message=message))

    def result(derived=None):
        return dict(checks_pass=not issues, phase=phase, issues=issues,
                    deferred_issues=deferred, derived=derived,
                    review_note='Checks verify entered data; independent source and owner review remain required.')

    schema = json.loads(SCHEMA.read_text())
    for error in Draft202012Validator(schema).iter_errors(model):
        fail('schema', '/'.join(map(str, error.absolute_path)) or 'model', error.message)
    if issues:
        return result()

    def records(value):
        if isinstance(value, dict):
            if 'id' in value:
                yield value
            for child in value.values():
                yield from records(child)
        elif isinstance(value, list):
            for child in value:
                yield from records(child)

    rows = list(records(model))
    for identifier, count in Counter(r['id'] for r in rows).items():
        if count > 1:
            fail('unique-ids', identifier, 'An ID has more than one authoritative record.')
    if issues:
        return result()
    all_ids = {r['id'] for r in rows}
    indexes = {k: {r['id']: r for r in model[k]} for k in
               ('source_documents', 'drawing_pages', 'source_references', 'fixture_types',
                'spaces', 'light_objects', 'light_zones', 'controllers', 'control_devices',
                'control_systems', 'control_groups', 'backup_supplies', 'decisions', 'assumptions')}
    branches = model['branch_circuits']
    units = [u for b in branches for u in b['power_units']]
    channels = [c for u in units for c in u['channels']]
    indexes.update(branches={r['id']: r for r in branches}, units={r['id']: r for r in units},
                   channels={r['id']: r for r in channels},
                   emergency_inputs={r['id']: r for c in model['controllers'] for r in c['emergency_inputs']})
    fields = dict(source_ref_ids='source_references', decision_id='decisions',
                  energy_classification_decision_id='decisions', assumption_ids='assumptions',
                  drawing_page_ids='drawing_pages', drawing_page_id='drawing_pages',
                  source_document_id='source_documents', fixture_type_id='fixture_types',
                  light_object_ids='light_objects', light_zone_ids='light_zones',
                  controller_id='controllers', control_group_ids='control_groups',
                  connected_control_device_ids='control_devices', channel_id='channels',
                  backup_supply_id='backup_supplies', control_power_backup_supply_id='backup_supplies',
                  integrated_power_unit_id='units', emergency_input_id='emergency_inputs',
                  source_device_id='control_devices', monitored_branch_circuit_id='branches')

    def references(value, owner):
        if isinstance(value, dict):
            owner = value.get('id', owner)
            for key, child in value.items():
                if key in fields:
                    for identifier in child if isinstance(child, list) else [child]:
                        if identifier is not None and identifier not in indexes[fields[key]]:
                            fail('reference-integrity', owner, f'Missing {key} reference: {identifier}')
                elif key == 'affects_ids':
                    for identifier in child:
                        if identifier not in all_ids:
                            fail('reference-integrity', owner, f'Missing affected object: {identifier}')
                elif key == 'target_id' and not any(child in indexes[k] for k in ('controllers', 'control_devices', 'control_systems')):
                    fail('reference-integrity', owner, f'Missing connected-control target: {child}')
                references(child, owner)
        elif isinstance(value, list):
            for child in value:
                references(child, owner)

    references(model, model['project']['id'])
    if issues:
        return result()
    pages, lights, zones, spaces = (indexes[k] for k in ('drawing_pages', 'light_objects', 'light_zones', 'spaces'))
    for ref in model['source_references']:
        page = pages.get(ref['drawing_page_id'])
        if page and page['source_document_id'] != ref['source_document_id']:
            fail('source-traceability', ref['id'], 'Reference document and page document disagree.')
    membership, zoned = defaultdict(list), defaultdict(list)
    for space in spaces.values():
        for lid in space['light_object_ids']:
            membership[lid].append(space['id'])
            pid = lights[lid]['source']['drawing_page_id']
            if pid is not None and pid not in space['drawing_page_ids']:
                fail('space-source-page', lid, 'Register the fixture source page on its served Space.')
        if space.get('inventory_only') and (space['light_object_ids'] or space['light_zone_ids'] or not space['description']):
            fail('space-inventory-only', space['id'], 'Inventory-only records need a description and empty light/zone lists.')
    for zone in zones.values():
        for lid in zone['light_object_ids']:
            zoned[lid].append(zone['id'])
    for lid, light in lights.items():
        if len(membership[lid]) != 1:
            fail('space-light-membership', lid, 'Every physical light must have exactly one primary served Space.')
        if len(zoned[lid]) > 1:
            fail('zone-light-membership', lid, 'A light cannot belong to multiple functional zones.')
        page = pages.get(light['source']['drawing_page_id'])
        point = light['source']['drawing_anchor']
        if point and (not page or not (0 <= point['x_pt'] <= page['width_pt'] and 0 <= point['y_pt'] <= page['height_pt'])):
            fail('spatial-context', lid, 'Anchor needs a page and must lie within its displayed bounds.')
        if len(zoned[lid]) == 1 and len(membership[lid]) == 1:
            sid = membership[lid][0]
            if zoned[lid][0] not in spaces[sid]['light_zone_ids']:
                fail('space-zone-membership', sid, 'Reference the real zone containing this Space\'s light.')
    for item in model['open_items']:
        if item['status'] == 'resolved' and not item['resolution']:
            fail('open-items', item['id'], 'Resolved items require a resolution.')
    if issues:
        return result()

    def counts(ids):
        values = Counter(lights[lid]['source']['fixture_type_id'] for lid in ids)
        return [dict(fixture_type_id=fid, source_mark=indexes['fixture_types'][fid]['source_mark'], quantity=qty)
                for fid, qty in sorted(values.items())]

    def watts(ids):
        values = [load_watts(lights[lid]['design']['load']) for lid in ids]
        return None if any(v is None for v in values) else sum(values, Decimal(0))

    derived = dict(physical_quantities=dict(spaces=len(spaces), light_objects=len(lights), light_zones=len(zones), fixture_types=len(indexes['fixture_types'])),
                   light_space_ids={lid: membership[lid][0] for lid in lights},
                   light_zone_ids={lid: zoned[lid][0] if zoned[lid] else None for lid in lights},
                   unzoned_light_ids=sorted(lid for lid in lights if not zoned[lid]),
                   space_fixture_counts={sid: counts(s['light_object_ids']) for sid, s in spaces.items()},
                   space_connected_watts={sid: watts(s['light_object_ids']) for sid, s in spaces.items()},
                   zone_fixture_counts={zid: counts(z['light_object_ids']) for zid, z in zones.items()},
                   engineering_views_available=False)
    if not spaces:
        fail('space-completeness', model['project']['id'], 'Register the observed Spaces.')
    if phase != 'inventory' and not lights:
        fail('light-completeness', model['project']['id'], 'Complete the physical lighting intake.')
    if model['project']['takeoff_status'] != 'reconciled':
        fail('source-reconciliation', model['project']['id'], 'Independent source review has not been recorded as reconciled.')
    for item in model['open_items']:
        if item['blocking'] and item['status'] == 'open':
            issue = dict(rule='open-items', entity_id=item['id'], message=item['description'])
            (issues if phase in item.get('blocking_phases', PHASES) else deferred).append(issue)
    for lid in derived['unzoned_light_ids']:
        issue = dict(rule='zone-assignment', entity_id=lid, message='Establish the functional zone during the later zoning/design review.')
        (issues if phase == 'design' else deferred).append(issue)
    if not derived['unzoned_light_ids'] and lights:
        projection = copy.deepcopy(model)
        projection['schema_version'] = '0.3.1'
        projection.pop('light_objects')
        for zone in projection['light_zones']:
            zone['light_objects'] = [copy.deepcopy(lights[lid]) for lid in zone.pop('light_object_ids')]
            if zone['label_mode'] == 'room':
                zone['label_mode'] = 'room_default'
        for item in projection['open_items']:
            item.pop('blocking_phases', None)
        engineering = check_spaces(projection)
        engineering_issues = [i for i in engineering['issues'] if i['rule'] not in ('source-reconciliation', 'open-items')]
        (issues if phase == 'design' else deferred).extend(engineering_issues)
        if engineering['derived'] is not None:
            derived.update(engineering['derived'])
            derived['physical_quantities']['spaces'] = len(spaces)
            derived['engineering_views_available'] = True
    elif phase == 'design':
        fail('engineering-review-pending', model['project']['id'], 'Complete zone membership before evaluating the full electrical hierarchy; no partial load totals are issued.')
    return result(derived)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('model', type=Path)
    parser.add_argument('--phase', choices=PHASES, default='intake')
    parser.add_argument('--migrate-output', type=Path, help='Write a v0.3-to-v0.4 copy; preserves all existing zones.')
    args = parser.parse_args()
    try:
        model = read_model(args.model)
        if args.migrate_output:
            model = migrate_v03(model)
            if args.migrate_output.exists():
                raise ValueError('Migration output already exists.')
            report = check_model(model, args.phase)
            if report['derived'] is None:
                raise ValueError('Migration is structurally invalid; review the legacy input before migrating.')
            args.migrate_output.write_text(model_json(model) + '\n')
        else:
            report = check_model(model, args.phase)
    except (OSError, ValueError) as error:
        parser.exit(2, f'Cannot check model: {error}\n')
    print(json.dumps(report, indent=2, default=str))
    return 0 if report['checks_pass'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
