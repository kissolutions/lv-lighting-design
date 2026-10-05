"""Repeatable source-review CSVs for v0.3/v0.4; no model or spreadsheet writeback."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from .export_review import write_csv
from .model_intake import check_model, migrate_v03
from .validate_model import read_model


def export_intake(model, output_dir, allow_provisional=False):
    original_version = model['schema_version']
    if original_version in ('0.3.0', '0.3.1'):
        model = migrate_v03(model)
    report = check_model(model, 'intake')
    if report['derived'] is None:
        raise ValueError('Structural, reference, spatial or membership failures prevent export.')
    if not report['checks_pass'] and not allow_provisional:
        raise ValueError('Intake is unreconciled/blocked; use --allow-provisional for a clearly marked review draft.')
    output_dir = Path(output_dir)
    if output_dir.exists() and any(output_dir.iterdir()):
        raise ValueError('Choose an empty output directory for this review revision.')
    output_dir.mkdir(parents=True, exist_ok=True)
    common = dict(model_revision=model['project']['model_revision'], input_schema_version=original_version,
                  review_status='INTAKE DATA CHECKS PASSED - ENGINEERING REVIEW REQUIRED' if report['checks_pass'] else 'PROVISIONAL - INTAKE REVIEW PENDING')
    lights = {l['id']: l for l in model['light_objects']}
    types = {t['id']: t for t in model['fixture_types']}
    derived = report['derived']

    def emit(name, fields, rows):
        write_csv(output_dir / name, list(common) + fields, [{**common, **r} for r in rows])

    fields = ['space_id', 'name', 'room_number', 'level', 'description', 'source_room_type',
              'area_sq_ft', 'area_basis', 'area_note', 'building_code_space_type',
              'building_code_occupancy_group', 'energy_code_space_type', 'enclosure',
              'has_windows', 'has_daylight_zone', 'daylight_control_required',
              'light_count', 'light_object_ids', 'light_zone_ids', 'inventory_only', 'source_ref_ids']
    room_rows = []
    for s in model['spaces']:
        row = {k: s.get(k) for k in fields}
        row.update(space_id=s['id'], light_count=len(s['light_object_ids']))
        for k in ('light_object_ids', 'light_zone_ids', 'source_ref_ids'):
            row[k] = ';'.join(s[k])
        room_rows.append(row)
    emit('room_schedule.csv', fields, room_rows)
    type_rows = []
    for tid, t in types.items():
        count = sum(l['source']['fixture_type_id'] == tid for l in lights.values())
        type_rows.append(dict(fixture_type_id=tid, source_mark=t['source_mark'], description=t['description'],
                              source_load_basis=t['source_load']['basis'], source_watts=t['source_load']['watts'],
                              occurrence_or_run_count=count, manufacturer_options=';'.join(t['manufacturer_options']),
                              source_ref_ids=';'.join(t['source_ref_ids'])))
    emit('fixture_type_schedule.csv', ['fixture_type_id', 'source_mark', 'description', 'source_load_basis',
         'source_watts', 'occurrence_or_run_count', 'manufacturer_options', 'source_ref_ids'], type_rows)
    summary_rows = []
    for s in model['spaces']:
        for r in derived['space_fixture_counts'][s['id']]:
            summary_rows.append(dict(space_id=s['id'], space_name=s['name'], **r))
    emit('lighting_by_space.csv', ['space_id', 'space_name', 'fixture_type_id', 'source_mark', 'quantity'], summary_rows)
    point_rows = []
    for lid, l in lights.items():
        mounting = l.get('mounting', {})
        point = l['source']['drawing_anchor'] or {}
        tid = l['source']['fixture_type_id']
        point_rows.append(dict(light_id=lid, fixture_type_id=tid, source_mark=types[tid]['source_mark'],
                               space_id=derived['light_space_ids'][lid], zone_id=derived['light_zone_ids'][lid],
                               drawing_page_id=l['source']['drawing_page_id'], x_pt=point.get('x_pt'), y_pt=point.get('y_pt'),
                               quantity_basis=types[tid]['source_load']['basis'],
                               length_ft=l['design']['load']['length_ft'], lv_watts=l['design']['load']['watts'],
                               channel_id=l['design']['channel_id'],
                               mounting_height_ft=mounting.get('height_above_served_floor_ft'),
                               height_basis=mounting.get('height_basis'), mounting_note=mounting.get('note'),
                               source_ref_ids=';'.join(l['source_ref_ids'])))
    # Display numbering is entered/reviewed separately; exporting never assigns or changes identity.
    def label_order(row):
        match = re.fullmatch(r'L([0-9]+)', row['light_label'] or '')
        return (0, int(match.group(1))) if match else (1, 0)

    for row in point_rows:
        row['light_label'] = lights[row['light_id']]['label']
    point_rows.sort(key=label_order)  # Stable for unlabeled/nonstandard labels and ties.
    emit('light_points.csv', ['light_label', 'light_id', 'fixture_type_id', 'source_mark', 'space_id', 'zone_id',
         'drawing_page_id', 'x_pt', 'y_pt', 'quantity_basis', 'length_ft', 'lv_watts', 'channel_id',
         'mounting_height_ft', 'height_basis', 'mounting_note', 'source_ref_ids'], point_rows)
    emit('discrepancy_list.csv', ['id', 'description', 'affects_ids', 'source_ref_ids', 'blocking',
         'blocking_phases', 'status', 'resolution', 'decision_id'],
         [{**i, 'affects_ids': ';'.join(i['affects_ids']), 'source_ref_ids': ';'.join(i['source_ref_ids']),
           'blocking_phases': ';'.join(i.get('blocking_phases', ('inventory', 'intake', 'design')))} for i in model['open_items']])
    (output_dir / 'intake_validation.json').write_text(json.dumps(report, indent=2, default=str) + '\n')
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('model', type=Path)
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--allow-provisional', action='store_true')
    args = parser.parse_args()
    try:
        report = export_intake(read_model(args.model), args.output_dir, args.allow_provisional)
    except (OSError, ValueError) as error:
        parser.exit(2, f'Cannot export: {error}\n')
    print(f'Review tables written to {args.output_dir}; no source/design state changed.')
    return 0 if report['checks_pass'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
