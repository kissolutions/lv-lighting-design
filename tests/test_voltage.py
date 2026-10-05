"""Electrical-interface incompatibilities must not disappear behind watt/group checks."""
import copy
import csv
import json
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

from jsonschema import Draft202012Validator

from generators.export_intake import export_intake
from generators.model_intake import SCHEMA_V05, check_model, model_json, upgrade_v05
from generators.validate_model import read_model

ROOT = Path(__file__).resolve().parents[1]


class VoltageTests(unittest.TestCase):
    def setUp(self):
        self.model = read_model(ROOT / 'docs/reference-implementations/synthetic-voltage/design-model.json')
        self.light = self.model['light_objects'][0]
        self.channel = self.model['branch_circuits'][0]['power_units'][0]['channels'][0]

    def rules(self, phase='design'):
        return {i['rule'] for i in check_model(self.model, phase)['issues']}

    def cc_single(self):
        for light in self.model['light_objects'][1:]:
            light['design']['channel_id'] = 'CH-SYNTHETIC-2'
        self.light['design'].update(input_voltage=dict(current_type='dc', nominal_v=None, min_v=25, max_v=35),
                                    input_power_mode='constant_current', input_current_ma=700)
        self.channel.update(voltage=dict(current_type='dc', nominal_v=None, min_v=20, max_v=40),
                            output_power_mode='constant_current', output_current_ma=700)

    def test_schema_and_selected_cv_design(self):
        Draft202012Validator.check_schema(json.loads(SCHEMA_V05.read_text()))
        report = check_model(self.model, 'design')
        self.assertTrue(report['checks_pass'], report['issues'])
        self.assertTrue(report['derived']['electrical_interface_checks_available'])

    def test_source_ac_voltage_is_not_selected_lv_voltage(self):
        self.model['fixture_types'][0]['source_voltage']['nominal_v'] = 277
        self.assertTrue(check_model(self.model, 'design')['checks_pass'])

    def test_source_driver_type_is_separate_from_selected_architecture(self):
        self.model['fixture_types'][0]['source_driver_type'] = 'driverless'
        self.assertEqual(self.light['design']['driver_type'], 'driver')
        self.assertTrue(check_model(self.model, 'design')['checks_pass'])
        self.light['design']['driver_type'] = 'driverless'
        self.assertTrue(check_model(self.model, 'design')['checks_pass'])
        self.assertEqual(self.light['design']['input_power_mode'], 'constant_voltage')

    def test_other_driver_type_requires_description(self):
        self.light['design'].update(driver_type='other', driver_note=None)
        self.assertIn('schema', self.rules())
        self.light['design']['driver_note'] = 'Synthetic alternative electrical interface architecture.'
        self.assertTrue(check_model(self.model, 'design')['checks_pass'])
        self.model['fixture_types'][0].update(source_driver_type='other', source_driver_note=None)
        self.assertIn('schema', self.rules('intake'))

    def test_unknown_selected_driver_type_defers_then_blocks_design(self):
        self.light['design']['driver_type'] = None
        report = check_model(self.model, 'intake')
        self.assertTrue(report['checks_pass'])
        self.assertIn('light-driver-basis', {i['rule'] for i in report['deferred_issues']})
        self.assertIn('light-driver-basis', self.rules())

    def test_mixed_cv_voltage_fails_despite_same_watts_and_group(self):
        before = self.light['design']['load']['watts']
        self.light['design']['input_voltage']['nominal_v'] = 24
        self.assertIn('voltage-compatibility', self.rules())
        self.assertEqual(self.light['design']['load']['watts'], before)
        self.assertNotIn('compatibility', self.rules())

    def test_decimal_voltage_mismatch_is_not_rounded_away(self):
        self.light['design']['input_voltage']['nominal_v'] = Decimal('48.0000000000000001')
        self.assertIn('voltage-compatibility', self.rules())

    def test_ac_dc_mismatch_and_cv_cc_mismatch(self):
        self.light['design']['input_voltage']['current_type'] = 'ac'
        self.assertIn('voltage-compatibility', self.rules())
        self.light['design']['input_power_mode'] = 'constant_current'
        self.assertIn('power-mode-compatibility', self.rules())

    def test_unknown_interfaces_defer_at_intake_but_block_design(self):
        old = read_model(ROOT / 'docs/reference-implementations/synthetic-intake/design-model.json')
        self.model = upgrade_v05(old)
        report = check_model(self.model, 'intake')
        self.assertTrue(report['checks_pass'], report['issues'])
        self.assertIn('light-electrical-basis', {i['rule'] for i in report['deferred_issues']})
        self.assertIn('light-electrical-basis', self.rules())
        self.assertIn('channel-electrical-basis', self.rules())

    def test_cv_range_without_selected_setting_stays_unconfirmed(self):
        self.channel['voltage'].update(nominal_v=None, min_v=12, max_v=48)
        self.assertIn('channel-electrical-basis', self.rules())

    def test_contradictory_voltage_numbers_block_every_phase_and_export(self):
        self.model['fixture_types'][0]['source_voltage'].update(min_v=277, max_v=120)
        for phase in ['inventory', 'intake', 'design']:
            self.assertIn('voltage-shape', self.rules(phase))
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                export_intake(self.model, directory, True)

    def test_single_cc_current_and_range_compatibility(self):
        self.cc_single()
        self.assertTrue(check_model(self.model, 'design')['checks_pass'])
        self.light['design']['input_current_ma'] = 350
        self.assertIn('current-compatibility', self.rules())
        self.light['design']['input_current_ma'] = 700
        self.light['design']['input_voltage']['max_v'] = 41
        self.assertIn('voltage-compatibility', self.rules())

    def test_cc_range_endpoints_are_inclusive(self):
        self.cc_single()
        self.light['design']['input_voltage'].update(min_v=20, max_v=40)
        self.assertTrue(check_model(self.model, 'design')['checks_pass'])

    def test_cc_nominal_alone_and_unknown_current_are_not_enough(self):
        self.cc_single()
        self.light['design']['input_voltage'].update(nominal_v=30, min_v=None, max_v=None)
        self.assertIn('light-electrical-basis', self.rules())
        self.channel['output_current_ma'] = None
        self.assertIn('channel-electrical-basis', self.rules())

    def test_multiple_cc_lights_require_unimplemented_topology_review(self):
        self.cc_single()
        other = self.model['light_objects'][1]
        other['design'].update(input_voltage=copy.deepcopy(self.light['design']['input_voltage']),
                               input_power_mode='constant_current', input_current_ma=700,
                               channel_id=self.channel['id'])
        self.assertIn('cc-topology-review', self.rules())

    def test_upgrade_preserves_identity_decimals_and_original_unknowns(self):
        old = read_model(ROOT / 'docs/reference-implementations/synthetic-intake/design-model.json')
        old['light_objects'][0]['design']['load']['watts'] = Decimal('20.0000000000000001')
        before = copy.deepcopy(old)
        upgraded = upgrade_v05(old)
        self.assertEqual(old, before)
        self.assertEqual([l['id'] for l in old['light_objects']], [l['id'] for l in upgraded['light_objects']])
        self.assertEqual(upgraded['light_objects'][0]['design']['load']['watts'], Decimal('20.0000000000000001'))
        self.assertIsNone(upgraded['fixture_types'][0]['source_voltage']['nominal_v'])
        self.assertIsNone(upgraded['light_objects'][0]['design']['input_voltage']['nominal_v'])
        self.assertIn('20.0000000000000001', model_json(upgraded))

    def test_v03_upgrade_and_legacy_check_do_not_claim_new_checks(self):
        old = read_model(ROOT / 'docs/reference-implementations/synthetic-spaces/lighting-model.json')
        upgraded = upgrade_v05(old)
        self.assertEqual(upgraded['schema_version'], '0.5.0')
        legacy = read_model(ROOT / 'docs/reference-implementations/synthetic-intake/design-model.json')
        report = check_model(legacy, 'design')
        self.assertTrue(report['checks_pass'])
        self.assertFalse(report['derived']['electrical_interface_checks_available'])

    def test_voltage_schedule_export_and_legacy_blank_fields(self):
        original = copy.deepcopy(self.model)
        with tempfile.TemporaryDirectory() as directory:
            export_intake(self.model, directory)
            with (Path(directory) / 'fixture_type_schedule.csv').open(encoding='utf-8-sig', newline='') as f:
                reader = csv.DictReader(f)
                row = next(reader)
                columns = reader.fieldnames
            self.assertEqual(columns[columns.index('source_watts') + 1], 'source_voltage')
            self.assertEqual(row['source_voltage'], '120')
            self.assertEqual(row['source_voltage_current_type'], 'ac')
            self.assertEqual(row['source_driver_type'], 'driver')
            with (Path(directory) / 'light_points.csv').open(encoding='utf-8-sig', newline='') as f:
                point = next(csv.DictReader(f))
                self.assertEqual(point['lv_input_voltage'], '48')
                self.assertEqual(point['lv_driver_type'], 'driver')
        self.assertEqual(self.model, original)
        old = read_model(ROOT / 'docs/reference-implementations/synthetic-intake/design-model.json')
        with tempfile.TemporaryDirectory() as directory:
            export_intake(old, directory)
            with (Path(directory) / 'fixture_type_schedule.csv').open(encoding='utf-8-sig', newline='') as f:
                self.assertEqual(next(csv.DictReader(f))['source_voltage'], '')

    def test_existing_emergency_checks_survive_electrical_extension(self):
        old = read_model(ROOT / 'docs/reference-implementations/synthetic-spaces/emergency-model.json')
        model = upgrade_v05(old)
        zone = next(z for z in model['light_zones'] if z['egress_type'] != 'normal')
        zone['emergency_behavior'] = 'not_required'
        self.assertIn('emergency-intent', {i['rule'] for i in check_model(model, 'design')['issues']})
