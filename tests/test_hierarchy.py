"""Verify natural ownership, cross-references, loads, and outage control intent."""
import copy
import json
import unittest
from decimal import Decimal
from pathlib import Path

from jsonschema import Draft202012Validator

from generators.model_hierarchy import SCHEMA, check_model, load_watts
from generators.validate_model import read_model

ROOT=Path(__file__).resolve().parents[1]
EXAMPLE=ROOT/'docs/reference-implementations/synthetic-hierarchy/lighting-model.json'
EMERGENCY=ROOT/'docs/reference-implementations/synthetic-hierarchy/emergency-model.json'


class HierarchyTests(unittest.TestCase):
    def setUp(self):
        self.model=read_model(EXAMPLE)
    def rules(self):
        return {i['rule'] for i in check_model(self.model)['issues']}
    def unit(self):
        return self.model['branch_circuits'][0]['power_units'][0]
    def test_schema_and_nested_ownership(self):
        Draft202012Validator.check_schema(json.loads(SCHEMA.read_text()))
        result=check_model(self.model)
        self.assertTrue(result['checks_pass'],result['issues'])
        self.assertEqual(result['derived']['physical_quantities']['power_units'],1)
    def test_many_to_many_derived_from_individual_lights_without_double_count(self):
        data=check_model(self.model)['derived']
        self.assertEqual(data['channel_zone_ids']['CH-SYNTHETIC-1'],['ZONE-SYNTHETIC-A','ZONE-SYNTHETIC-B'])
        self.assertEqual(data['zone_channel_ids']['ZONE-SYNTHETIC-A'],['CH-SYNTHETIC-1','CH-SYNTHETIC-2'])
        self.assertEqual(data['zone_connected_watts']['ZONE-SYNTHETIC-A'],Decimal(45))
        self.assertEqual(data['channel_connected_watts']['CH-SYNTHETIC-1'],Decimal(50))
        self.assertEqual(data['power_unit_connected_output_watts']['PU-SYNTHETIC'],Decimal(75))
        self.assertEqual(data['branch_lighting_input_watts']['BRANCH-SYNTHETIC'],Decimal(100))
    def test_linear_load_bases(self):
        self.assertEqual(load_watts({'basis':'per_foot','watts':4,'length_ft':18,'reference_length_ft':None}),Decimal(72))
        self.assertEqual(load_watts({'basis':'per_reference_length','watts':23,'length_ft':8,'reference_length_ft':4}),Decimal(46))
        self.assertIsNone(load_watts({'basis':'per_foot','watts':4,'length_ft':None,'reference_length_ft':None}))
    def test_channel_overload_uses_only_the_lights_powered_by_that_channel(self):
        self.model['light_zones'][0]['light_objects'][0]['design']['load']['watts']=61
        self.assertIn('channel-load',self.rules())
    def test_duplicate_light_owner_rejected(self):
        self.model['light_zones'][1]['light_objects'].append(copy.deepcopy(self.model['light_zones'][0]['light_objects'][0]))
        self.assertIn('unique-ids',self.rules())
    def test_missing_channel_reference_rejected(self):
        self.model['light_zones'][0]['light_objects'][0]['design']['channel_id']='MISSING'
        self.assertIn('reference-integrity',self.rules())
    def test_unknown_assignment_is_provisional(self):
        self.model['light_zones'][0]['light_objects'][0]['design']['channel_id']=None
        self.assertIn('assignment-completeness',self.rules())
    def test_class2_baseline_cannot_be_reused_as_class4_rule(self):
        self.unit()['channels'][0]['power_class']='class_4'
        self.assertIn('schema',self.rules())
    def test_product_profile_is_not_globally_limited_to_90_w_or_56_v(self):
        c=self.unit()['channels'][0]
        c.update(power_class='class_4',validation_profile='product_specific',rated_output_watts=400,design_limit_watts=350)
        c['voltage']['nominal_v']=400
        self.unit()['lv_power_type']='mixed'
        # This only verifies representability and declared-capacity checks, not Class 4 compliance.
        self.assertTrue(check_model(self.model)['checks_pass'])
    def test_power_unit_aggregate_capacity(self):
        self.unit()['aggregate_design_limit_watts']=74
        self.assertIn('power-unit-capacity',self.rules())
    def test_mixed_channel_classes_require_explicit_unit_class(self):
        channel=self.unit()['channels'][0]
        channel.update(power_class='class_3',validation_profile='product_specific')
        self.assertIn('power-unit-basis',self.rules())
    def test_input_watts_do_not_equal_output_watts_by_assumption(self):
        self.unit()['design_input_watts']=None
        result=check_model(self.model)
        self.assertIn('power-unit-basis',{i['rule'] for i in result['issues']})
        self.assertIsNone(result['derived']['branch_lighting_input_watts']['BRANCH-SYNTHETIC'])
    def test_controller_four_output_limit(self):
        self.model['light_zones'][0]['controller_output']=5
        self.assertIn('controller-capacity',self.rules())
    def test_independent_zones_need_independent_control_paths(self):
        self.model['light_zones'][1]['controller_output']=1
        self.assertIn('controller-capacity',self.rules())
    def test_provisional_design_decision_blocks(self):
        self.model['decisions'][0]['status']='provisional'
        self.assertIn('decision-basis',self.rules())
    def test_integrated_controller_not_counted_as_separate_hardware(self):
        self.model['controllers'][0]['integrated_power_unit_id']='PU-SYNTHETIC'
        self.assertEqual(check_model(self.model)['derived']['physical_quantities']['separate_controllers'],0)
    def test_emergency_standby_requires_force_on_signal_and_backup_supply(self):
        self.model=read_model(EMERGENCY)
        self.assertTrue(check_model(self.model)['checks_pass'])
        self.model['light_zones'][1]['emergency_input_id']=None
        self.assertIn('emergency-signal',self.rules())
    def test_emergency_normally_on_still_has_separate_outage_response(self):
        self.model=read_model(EMERGENCY)
        self.model['light_zones'][1].update(egress_type='em_always_on',normal_behavior='always_on')
        self.assertTrue(check_model(self.model)['checks_pass'])
    def test_switched_emergency_fixture_keeps_normal_control_behavior(self):
        self.model=read_model(EMERGENCY)
        self.model['light_zones'][1].update(egress_type='em_normally_controlled',normal_behavior='controlled')
        self.assertTrue(check_model(self.model)['checks_pass'])
    def test_force_on_command_without_backup_power_is_incomplete(self):
        self.model=read_model(EMERGENCY)
        self.unit()['backup_supply_id']=None
        self.assertIn('emergency-supply',self.rules())
    def test_controller_must_operate_during_outage(self):
        self.model=read_model(EMERGENCY)
        self.model['controllers'][0]['control_power_backup_supply_id']=None
        self.assertIn('emergency-control-power',self.rules())
    def test_emergency_input_needs_source_connection_and_monitored_normal_circuit(self):
        self.model=read_model(EMERGENCY)
        inp=self.model['controllers'][0]['emergency_inputs'][0]
        inp['monitored_branch_circuit_id']=None
        self.assertIn('emergency-signal',self.rules())
    def test_fixture_integral_battery_and_central_backup_are_distinct_provisions(self):
        self.model=read_model(EMERGENCY)
        self.unit()['backup_supply_id']=None
        self.model['light_zones'][1]['light_objects'][0]['design']['backup_supply_id']='BACKUP-SYNTHETIC'
        self.assertTrue(check_model(self.model)['checks_pass'])
    def test_blank_v02_seed_cannot_claim_design_complete(self):
        self.model=read_model(ROOT/'templates/lighting-project-v0.2.template.json')
        self.assertIn('source-reconciliation',self.rules())
    def test_derived_views_do_not_rewrite_authoritative_objects(self):
        before=copy.deepcopy(self.model)
        check_model(self.model)
        self.assertEqual(self.model,before)


if __name__=='__main__':
    unittest.main()
