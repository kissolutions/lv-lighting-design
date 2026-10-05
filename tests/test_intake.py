"""Physical intake stays independent of logical controls without losing engineering checks."""
import copy
import csv
import json
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

from jsonschema import Draft202012Validator

from generators.export_intake import export_intake
from generators.model_intake import SCHEMA, check_model, migrate_v03, model_json
from generators.validate_model import read_model

ROOT = Path(__file__).resolve().parents[1]


class IntakeTests(unittest.TestCase):
    def setUp(self):
        self.legacy = read_model(ROOT / 'docs/reference-implementations/synthetic-spaces/lighting-model.json')
        self.model = migrate_v03(self.legacy)

    def physical_only(self):
        self.model['light_zones'] = []
        self.model['branch_circuits'] = []
        self.model['controllers'] = []
        for s in self.model['spaces']:
            s['light_zone_ids'] = []
            s.update(area_sq_ft=None, area_basis='unknown', energy_code_space_type=None,
                     has_daylight_zone=None, daylight_control_required=None, code_references=[])
        for l in self.model['light_objects']:
            l['design'].update(channel_id=None, decision_id=None)
            l['design']['load']['watts'] = None

    def rules(self, phase='intake'):
        return {i['rule'] for i in check_model(self.model, phase)['issues']}

    def test_schema_and_full_migrated_design(self):
        Draft202012Validator.check_schema(json.loads(SCHEMA.read_text()))
        self.assertTrue(check_model(self.model, 'design')['checks_pass'])

    def test_lights_need_no_zones_or_loads_at_intake(self):
        self.physical_only()
        before = copy.deepcopy(self.model)
        r = check_model(self.model)
        self.assertTrue(r['checks_pass'], r['issues'])
        self.assertEqual(self.model, before)
        self.assertEqual(r['derived']['physical_quantities']['light_zones'], 0)
        self.assertEqual(len(r['derived']['unzoned_light_ids']), 3)
        self.assertTrue(all(w is None for w in r['derived']['space_connected_watts'].values()))
        self.assertIn('zone-assignment', self.rules('design'))

    def test_room_inventory_can_precede_fixture_counting(self):
        self.physical_only()
        self.model['light_objects'] = []
        for s in self.model['spaces']:
            s['light_object_ids'] = []
        self.assertTrue(check_model(self.model, 'inventory')['checks_pass'])
        self.assertIn('light-completeness', self.rules('intake'))

    def test_orphan_and_double_space_membership_are_primary_failures(self):
        self.physical_only()
        self.model['spaces'][0]['light_object_ids'].remove('LIGHT-SYNTHETIC-1')
        self.assertIn('space-light-membership', self.rules())
        self.model['spaces'][0]['light_object_ids'].append('LIGHT-SYNTHETIC-1')
        self.model['spaces'][1]['light_object_ids'].append('LIGHT-SYNTHETIC-1')
        self.assertIn('space-light-membership', self.rules())

    def test_zone_assignment_preserves_physical_identity_and_counts(self):
        before = {l['id'] for l in self.model['light_objects']}
        self.model['light_zones'][1]['light_object_ids'].append('LIGHT-SYNTHETIC-1')
        self.assertIn('zone-light-membership', self.rules())
        self.assertEqual(before, {l['id'] for l in self.model['light_objects']})

    def test_unlit_corridor_does_not_need_inventory_only_to_pass_intake(self):
        self.physical_only()
        s = copy.deepcopy(self.model['spaces'][0])
        s.update(id='SPACE-CORRIDOR', name='Proposed corridor', light_object_ids=[], light_zone_ids=[])
        self.model['spaces'].append(s)
        self.assertTrue(check_model(self.model)['checks_pass'])

    def test_stage_blockers_are_explicit_and_missing_phase_is_conservative(self):
        self.physical_only()
        item = dict(id='OI-LOAD', description='Load unknown', affects_ids=['LIGHT-SYNTHETIC-1'],
                    source_ref_ids=self.model['spaces'][0]['source_ref_ids'], blocking=True,
                    blocking_phases=['design'], status='open', resolution=None, decision_id=None)
        self.model['open_items'].append(item)
        self.assertTrue(check_model(self.model)['checks_pass'])
        item.pop('blocking_phases')
        self.assertIn('open-items', self.rules())

    def test_invalid_ref_and_off_page_anchor_block_provisional_export(self):
        self.physical_only()
        self.model['light_objects'][0]['source']['drawing_anchor'] = dict(x_pt=100000, y_pt=0)
        self.assertIn('spatial-context', self.rules())
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):
                export_intake(self.model, Path(d), True)
        self.model['light_objects'][0]['source_ref_ids'] = ['MISSING']
        self.assertIn('reference-integrity', self.rules())

    def test_original_migration_is_not_mutated_or_silently_dezoned(self):
        original = copy.deepcopy(self.legacy)
        m = migrate_v03(self.legacy)
        self.assertEqual(original, self.legacy)
        self.assertEqual(len(m['light_zones']), 2)
        self.assertEqual(len(m['light_objects']), 3)

    def test_migration_output_preserves_numeric_precision_at_limits(self):
        self.model['light_objects'][0]['design']['load']['watts'] = Decimal('90.0000000000000001')
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'migration.json'
            p.write_text(model_json(self.model))
            reopened = read_model(p)
            self.assertEqual(reopened['light_objects'][0]['design']['load']['watts'], Decimal('90.0000000000000001'))
            self.assertIn('channel-load', {i['rule'] for i in check_model(reopened, 'design')['issues']})

    def test_export_counts_and_unknowns_roundtrip_without_making_zones(self):
        self.physical_only()
        with tempfile.TemporaryDirectory() as d:
            export_intake(self.model, Path(d))
            rows = list(csv.DictReader((Path(d) / 'light_points.csv').read_text(encoding='utf-8-sig').splitlines()))
            self.assertEqual(len(rows), 3)
            self.assertTrue(all(r['zone_id'] == '' and r['lv_watts'] == '' for r in rows))
            counts = list(csv.DictReader((Path(d) / 'lighting_by_space.csv').read_text(encoding='utf-8-sig').splitlines()))
            self.assertEqual(sum(int(r['quantity']) for r in counts), 3)
            with self.assertRaises(ValueError):
                export_intake(self.model, Path(d))

    def test_existing_emergency_checks_are_retained(self):
        emergency = migrate_v03(read_model(ROOT / 'docs/reference-implementations/synthetic-spaces/emergency-model.json'))
        self.assertTrue(check_model(emergency, 'design')['checks_pass'])
        next(z for z in emergency['light_zones'] if z['egress_type'] != 'normal')['emergency_behavior'] = 'not_required'
        self.assertIn('emergency-intent', {i['rule'] for i in check_model(emergency, 'design')['issues']})

    def test_display_numbers_export_in_numeric_order_without_changing_identity(self):
        self.physical_only()
        labels = ['L1000', 'L010', 'L009']
        for light, label in zip(self.model['light_objects'], labels):
            light['label'] = label
        expected = {l['label']: l['id'] for l in self.model['light_objects']}
        before = copy.deepcopy(self.model)
        with tempfile.TemporaryDirectory() as d:
            export_intake(self.model, Path(d))
            with (Path(d) / 'light_points.csv').open(encoding='utf-8-sig', newline='') as f:
                reader = csv.DictReader(f)
                self.assertEqual(reader.fieldnames[3:5], ['light_label', 'light_id'])
                rows = list(reader)
            self.assertEqual([r['light_label'] for r in rows], ['L009', 'L010', 'L1000'])
            self.assertEqual({r['light_label']: r['light_id'] for r in rows}, expected)
            self.assertTrue(all(r['zone_id'] == '' for r in rows))
        self.assertEqual(self.model, before)

    def test_unknown_and_nonstandard_labels_are_not_invented_and_stay_csv_safe(self):
        self.physical_only()
        for light, label in zip(self.model['light_objects'], [None, '=1+1', 'L001']):
            light['label'] = label
        original_ids = [l['id'] for l in self.model['light_objects']]
        before = copy.deepcopy(self.model)
        with tempfile.TemporaryDirectory() as d:
            export_intake(self.model, Path(d))
            with (Path(d) / 'light_points.csv').open(encoding='utf-8-sig', newline='') as f:
                rows = list(csv.DictReader(f))
            self.assertEqual([r['light_id'] for r in rows], [original_ids[2], original_ids[0], original_ids[1]])
            self.assertEqual([r['light_label'] for r in rows], ['L001', '', "'=1+1"])
        self.assertEqual(self.model, before)

    def test_unknown_selected_load_does_not_pass_full_design(self):
        self.model['light_objects'][0]['design']['load']['watts'] = None
        self.assertIn('light-load', self.rules('design'))
