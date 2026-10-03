"""Space ownership, code-condition evidence, and summary counts stay consistent."""
import copy
import json
import unittest
from decimal import Decimal
from pathlib import Path

from jsonschema import Draft202012Validator

from generators.model_spaces import SCHEMA, check_model
from generators.validate_model import read_model

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / 'docs/reference-implementations/synthetic-spaces/lighting-model.json'


class SpaceTests(unittest.TestCase):
    def setUp(self):
        self.model = read_model(EXAMPLE)

    def rules(self):
        return {i['rule'] for i in check_model(self.model)['issues']}

    def test_schema_and_space_example(self):
        Draft202012Validator.check_schema(json.loads(SCHEMA.read_text()))
        self.assertTrue(check_model(self.model)['checks_pass'])

    def test_emergency_hierarchy_still_valid_with_space_membership(self):
        self.model = read_model(ROOT / 'docs/reference-implementations/synthetic-spaces/emergency-model.json')
        self.assertTrue(check_model(self.model)['checks_pass'])

    def test_space_refs_and_derived_counts_do_not_duplicate_lights(self):
        data = check_model(self.model)['derived']
        self.assertEqual(data['physical_quantities']['light_objects'], 3)
        self.assertEqual(data['space_fixture_counts']['SPACE-SYNTHETIC-A'][0]['quantity'], 2)
        self.assertEqual(data['space_connected_watts']['SPACE-SYNTHETIC-A'], Decimal(45))
        self.assertEqual(data['space_channel_ids']['SPACE-SYNTHETIC-A'], ['CH-SYNTHETIC-1', 'CH-SYNTHETIC-2'])

    def test_dangling_light_reference_is_structural_failure(self):
        self.model['spaces'][0]['light_object_ids'].append('MISSING')
        result = check_model(self.model)
        self.assertIn('reference-integrity', self.rules())
        self.assertIsNone(result['derived'])

    def test_one_light_cannot_be_counted_in_two_spaces(self):
        self.model['spaces'][1]['light_object_ids'].append('LIGHT-SYNTHETIC-1')
        self.assertIn('space-light-membership', self.rules())

    def test_unreferenced_light_is_not_silently_dropped(self):
        self.model['spaces'][0]['light_object_ids'].remove('LIGHT-SYNTHETIC-1')
        self.assertIn('space-light-membership', self.rules())

    def test_zone_list_must_match_actual_room_lights(self):
        self.model['spaces'][0]['light_zone_ids'].append('ZONE-SYNTHETIC-B')
        self.assertIn('space-zone-membership', self.rules())

    def test_space_ids_share_the_global_identity_namespace(self):
        self.model['spaces'][0]['id'] = 'CTRL-SYNTHETIC'
        self.assertIn('unique-ids', self.rules())

    def test_room_default_zone_has_internal_id_without_visible_label(self):
        result = check_model(self.model)
        self.assertIsNone(self.model['light_zones'][0]['label'])
        self.assertEqual(result['derived']['zone_display_labels']['ZONE-SYNTHETIC-A'], 'Synthetic enclosed office A')

    def test_dollar_zone_label_is_display_text_and_does_not_change_identity(self):
        z = self.model['light_zones'][0]
        z.update(label='$z109', label_mode='named')
        result = check_model(self.model)
        self.assertTrue(result['checks_pass'])
        self.assertEqual(result['derived']['zone_display_labels'][z['id']], '$z109')
        self.assertEqual(z['id'], 'ZONE-SYNTHETIC-A')

    def test_room_default_area_can_be_derived_from_its_space(self):
        self.model['light_zones'][0].update(control_area_sq_ft=None, control_area_basis='unknown')
        result = check_model(self.model)
        self.assertTrue(result['checks_pass'])
        self.assertEqual(result['derived']['zone_control_area_sq_ft']['ZONE-SYNTHETIC-A'], Decimal(88))

    def test_inconsistent_room_default_control_area_fails(self):
        self.model['light_zones'][0]['control_area_sq_ft'] = 80
        self.assertIn('zone-control-area', self.rules())

    def test_estimate_remains_explicit_and_needs_a_basis(self):
        self.model['spaces'][0]['area_note'] = None
        self.assertIn('space-area', self.rules())

    def test_building_and_energy_classifications_are_independent(self):
        s = self.model['spaces'][0]
        s.update(building_code_space_type='SYNTHETIC BUILDING TYPE', building_code_occupancy_group='SYNTHETIC GROUP')
        self.assertTrue(check_model(self.model)['checks_pass'])
        self.assertEqual(s['energy_code_space_type'], 'enclosed_office')
        self.assertEqual(s['source_room_type'], 'Office')

    def test_window_does_not_automatically_require_daylight_controls(self):
        s = self.model['spaces'][0]
        s.update(has_windows=True, has_daylight_zone=True, daylight_control_required=False,
                 daylight_assessment_note='Synthetic verified control exemption; not a real code determination.')
        self.assertTrue(check_model(self.model)['checks_pass'])

    def test_unknown_daylight_geometry_remains_provisional(self):
        self.model['spaces'][0]['has_daylight_zone'] = None
        self.assertIn('space-daylight-basis', self.rules())

    def test_inferred_energy_classification_needs_decision_and_explanation(self):
        s = self.model['spaces'][0]
        s.update(energy_classification_basis='inferred', energy_classification_note=None,
                 energy_classification_decision_id=None)
        self.assertIn('space-energy-type', self.rules())

    def test_code_edition_and_adoption_are_not_inferred_from_room_name(self):
        self.model['project']['energy_code_basis']['edition'] = None
        self.assertIn('energy-code-basis', self.rules())

    def test_provisional_code_applicability_blocks_readiness(self):
        self.model['spaces'][0]['code_references'][0]['applicability_status'] = 'provisional'
        self.assertIn('space-code-reference', self.rules())

    def test_summary_counts_use_type_identity_even_when_marks_match(self):
        second = copy.deepcopy(self.model['fixture_types'][0])
        second['id'] = 'TYPE-SYNTHETIC-SECOND'
        self.model['fixture_types'].append(second)
        self.model['light_zones'][0]['light_objects'][1]['source']['fixture_type_id'] = second['id']
        rows = check_model(self.model)['derived']['space_fixture_counts']['SPACE-SYNTHETIC-A']
        self.assertEqual(len(rows), 2)
        self.assertEqual([r['quantity'] for r in rows], [1, 1])

    def test_rename_and_channel_reassignment_preserve_occurrence_ids(self):
        before = {l['id'] for z in self.model['light_zones'] for l in z['light_objects']}
        self.model['spaces'][0]['name'] = 'Renamed room'
        self.model['light_zones'][0]['light_objects'][1]['design']['channel_id'] = 'CH-SYNTHETIC-1'
        result = check_model(self.model)
        self.assertTrue(result['checks_pass'])
        self.assertEqual(result['derived']['physical_quantities']['light_objects'], len(before))
        self.assertEqual(set(result['derived']['light_space_ids']), before)

    def test_check_does_not_rewrite_model(self):
        original = copy.deepcopy(self.model)
        check_model(self.model)
        self.assertEqual(self.model, original)

    def test_upper_sheet_fixture_belongs_to_lower_served_level(self):
        space = self.model['spaces'][0]
        space['level'] = 'Level 1'
        upper = copy.deepcopy(self.model['drawing_pages'][0])
        upper.update(id='PAGE-SYNTHETIC-UPPER', sheet_id='SYNTHETIC UPPER LIGHTING')
        self.model['drawing_pages'].append(upper)
        space['drawing_page_ids'].append(upper['id'])
        light = self.model['light_zones'][0]['light_objects'][0]
        light['source']['drawing_page_id'] = upper['id']
        light['mounting'] = dict(height_above_served_floor_ft=24, height_basis='source_document',
                                 note='Synthetic high-mount example above the served floor.',
                                 source_ref_ids=space['source_ref_ids'])
        result = check_model(self.model)
        self.assertTrue(result['checks_pass'], result['issues'])
        self.assertEqual(result['derived']['light_space_ids'][light['id']], space['id'])
        self.assertEqual(result['derived']['space_levels'][space['id']], 'Level 1')
        self.assertEqual(result['derived']['physical_quantities']['light_objects'], 3)

    def test_qualitative_high_mounting_stays_unknown_and_requires_review(self):
        light = self.model['light_zones'][0]['light_objects'][0]
        light['mounting'] = dict(height_above_served_floor_ft=None, height_basis='unknown',
                                 note='High-mounted; verify height above served floor.', source_ref_ids=[])
        result = check_model(self.model)
        self.assertIn('light-mounting-height', {i['rule'] for i in result['issues']})
        self.assertIsNone(result['derived']['light_mounting'][light['id']]['height_above_served_floor_ft'])

    def test_mounting_evidence_and_estimate_note_are_required(self):
        light = self.model['light_zones'][0]['light_objects'][0]
        light['mounting'] = dict(height_above_served_floor_ft=24, height_basis='estimated',
                                 note=None, source_ref_ids=[])
        self.assertIn('light-mounting-basis', self.rules())
        light['mounting']['source_ref_ids'] = ['MISSING']
        self.assertIn('reference-integrity', self.rules())

    def test_named_zone_can_span_two_spaces_without_duplicate_lights(self):
        first, second = self.model['light_zones']
        first.update(label='Synthetic shared stair', label_mode='named',
                     control_area_sq_ft=176, control_area_basis='source_document')
        first['light_objects'].extend(second['light_objects'])
        self.model['light_zones'].remove(second)
        for space in self.model['spaces']:
            space['light_zone_ids'] = [first['id']]
        result = check_model(self.model)
        self.assertTrue(result['checks_pass'], result['issues'])
        self.assertEqual(len(result['derived']['zone_space_ids'][first['id']]), 2)
        self.assertEqual(result['derived']['physical_quantities']['light_objects'], 3)

    def test_stair_level_can_reference_shared_zone_without_duplicating_upper_lights(self):
        zone = self.model['light_zones'][0]
        zone.update(label='Synthetic Stair A', label_mode='named')
        lower = copy.deepcopy(self.model['spaces'][0])
        lower.update(id='SPACE-SYNTHETIC-LOWER', name='Synthetic Stair A lower level',
                     room_number=None, level='Level 1', light_object_ids=[],
                     description='Lower level of the stair served by the shared overhead zone.')
        self.model['spaces'].append(lower)
        result = check_model(self.model)
        self.assertTrue(result['checks_pass'], result['issues'])
        self.assertIn(lower['id'], result['derived']['zone_space_ids'][zone['id']])
        self.assertEqual(result['derived']['space_fixture_counts'][lower['id']], [])
        lower['decision_id'] = None
        self.assertIn('space-zone-membership', self.rules())

    def test_inventory_only_unnumbered_chase_needs_no_fictitious_lighting_design(self):
        chase = copy.deepcopy(self.model['spaces'][0])
        chase.update(id='SPACE-SYNTHETIC-CHASE', name='Unnumbered service enclosure',
                     room_number=None, level='Level 2', inventory_only=True,
                     description='Between synthetic storage and equipment room; chase use needs verification.',
                     light_object_ids=[], light_zone_ids=[], energy_code_space_type=None,
                     energy_classification_basis='unknown', code_references=[], decision_id=None,
                     area_sq_ft=None, area_basis='unknown', enclosure=None, has_windows=None,
                     has_daylight_zone=None, daylight_control_required=None)
        self.model['spaces'].append(chase)
        result = check_model(self.model)
        self.assertTrue(result['checks_pass'], result['issues'])
        self.assertEqual(result['derived']['inventory_only_space_ids'], [chase['id']])
        chase['description'] = None
        self.assertIn('space-inventory-only', self.rules())


if __name__ == '__main__':
    unittest.main()
