"""Meaningful boundaries for hierarchy, printable schedules and annotation review."""
import copy,json,tempfile,unittest
from pathlib import Path
from decimal import Decimal
from jsonschema import Draft202012Validator
from generators.model_zone_hierarchy import hierarchy_projection, upgrade_v07, SCHEMA
from generators.model_intake import check_model
from generators.milestone_markup import calculated_label, render_order, boundary_style, schedules, export_schedules, validate_manifest, reconcile_annotation_return
from generators.validate_topology import validate
ROOT=Path(__file__).resolve().parents[1]

class MilestoneTests(unittest.TestCase):
    def setUp(self):
        example=ROOT/'docs/reference-implementations/synthetic-milestones'
        self.model=json.loads((example/'lighting-model.json').read_text())
        self.top=json.loads((example/'topology.json').read_text())
        self.manifest=json.loads((example/'markup-manifest.json').read_text())
    def test_new_schemas_and_seeds(self):
        for schema,seed in [('lighting-project-v0.7','lighting-project-v0.7'),('controller-power-topology-v1.1','controller-power-topology-v1.1'),('milestone-markup-v1','milestone-markup-v1')]:
            s=json.loads((ROOT/'schemas'/(schema+'.schema.json')).read_text());Draft202012Validator.check_schema(s)
            self.assertEqual(list(Draft202012Validator(s).iter_errors(json.loads((ROOT/'templates'/(seed+'.template.json')).read_text()))),[])
    def test_parent_derived_membership_and_no_duplicate_load(self):
        before=copy.deepcopy(self.model);report=check_model(self.model,'design')
        self.assertTrue(report['checks_pass'],report['issues']);self.assertEqual(self.model,before)
        derived=report['derived']['zone_derived_light_ids']['ZONE-SYNTHETIC-PARENT']
        self.assertEqual(set(derived),{l['id'] for l in self.model['light_objects']})
        self.assertEqual(self.model['light_zones'][-1]['light_object_ids'],[])
    def test_parent_cannot_duplicate_child_lights(self):
        self.model['light_zones'][-1]['light_object_ids']=[self.model['light_objects'][0]['id']]
        self.assertIn('zone-hierarchy',{i['rule'] for i in check_model(self.model)['issues']})
    def test_parent_cycle_and_missing_parent_rejected(self):
        self.model['light_zones'][-1]['parent_zone_id']=self.model['light_zones'][0]['id']
        self.assertIsNone(hierarchy_projection(self.model)[0])
        self.model['light_zones'][-1]['parent_zone_id']='MISSING'
        self.assertIsNone(hierarchy_projection(self.model)[0])
    def test_parent_ids_do_not_hide_global_identity_collisions(self):
        parent=self.model['light_zones'][-1];old=parent['id'];parent['id']=self.model['light_objects'][0]['id']
        for z in self.model['light_zones'][:-1]:z['parent_zone_id']=parent['id']
        self.assertIsNone(hierarchy_projection(self.model)[0])
    def test_unreviewed_upgrade_preserves_existing_lights(self):
        old=json.loads((ROOT/'docs/reference-implementations/synthetic-voltage/design-model.json').read_text());before=copy.deepcopy(old)
        upgraded=upgrade_v07(old)
        self.assertEqual(old,before);self.assertEqual(upgraded['project']['controls_narrative_review']['status'],'unreviewed')
        self.assertEqual([l['id'] for l in old['light_objects']],[l['id'] for l in upgraded['light_objects']])
    def test_narrative_lock_requires_confirmed_decision(self):
        self.model['project']['controls_narrative_review']['decision_id']=None
        self.assertFalse(check_model(self.model)['checks_pass'])
    def test_device_export_requires_narrative_lock(self):
        self.model['project']['controls_narrative_review']['status']='draft'
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):export_schedules(self.model,self.top,Path(d)/'out',3)
    def test_ceiling_preserves_small_values_and_whole_values(self):
        self.assertEqual(calculated_label(Decimal('18.000001')),'19')
        self.assertEqual(calculated_label(Decimal('18')),'18')
        self.assertEqual(calculated_label(Decimal('0.01')),'1')
        self.assertEqual(calculated_label(None),'')
    def test_sum_before_display_rounding(self):
        chan=self.model['light_objects'][0]['design']['channel_id'];lights=[l for l in self.model['light_objects'] if l['design']['channel_id']==chan]
        for l in lights:l['design']['load'].update(basis='per_fixture',watts=Decimal('10.1'))
        channel=next(c for b in self.model['branch_circuits'] for u in b['power_units'] for c in u['channels'] if c['id']==chan)
        channel['auxiliary_load_watts']=Decimal('0.2')
        row=next(r for r in schedules(self.model,self.top)['micro_channels'] if r['micro_channel_id']==chan)
        self.assertEqual(row['connected_watts'],calculated_label(Decimal('10.1')*len(lights)+Decimal('0.2')))
        self.assertEqual(lights[0]['design']['load']['watts'],Decimal('10.1'))
    def test_every_light_id_and_sensor_parent_association_exported_once(self):
        t=schedules(self.model,self.top)
        self.assertEqual({r['light_point_id'] for r in t['light_points_by_type']},{l['id'] for l in self.model['light_objects']})
        self.assertEqual(len(t['room_devices']),1);self.assertIn('ZONE-SYNTHETIC-PARENT',t['room_devices'][0]['zone_ids'])
        self.assertEqual(t['room_devices'][0]['tag'],'OS-01');self.assertTrue(t['room_devices'][0]['room_name'])
    def test_text_last_and_envelope_style(self):
        ops=[dict(kind='text',id='A'),dict(kind='shape',id='B'),dict(kind='text',id='C'),dict(kind='line',id='D')]
        self.assertEqual([o['id'] for o in render_order(ops)],['B','D','A','C'])
        self.assertEqual(boundary_style(True),'dashed');self.assertEqual(boundary_style(False),'solid')
    def test_device_metadata_and_owner_return_identity(self):
        self.assertEqual(validate_manifest(self.manifest,self.model,self.top),[])
        returned=copy.deepcopy(self.manifest);returned['annotations'][0].update(x_pt=20,y_pt=30,location_basis='owner_returned',review_status='accepted')
        self.assertIs(reconcile_annotation_return(self.manifest,returned),returned)
        returned['annotations'][0]['entity_id']='OTHER'
        with self.assertRaises(ValueError):reconcile_annotation_return(self.manifest,returned)
    def test_pdf_acceptance_requires_actual_readback(self):
        self.manifest['packages'][0]['review_status']='accepted'
        self.assertTrue(validate_manifest(self.manifest,self.model,self.top))
    def test_device_free_channel_map_and_wrong_layer_rejected(self):
        self.manifest['packages'][0]['kind']='micro_channels';self.manifest['annotations'][0]['layer']='lv_channels'
        self.assertGreaterEqual(len(validate_manifest(self.manifest,self.model,self.top)),2)
    def test_printable_export_has_ordered_schedules_without_pdf_claim(self):
        with tempfile.TemporaryDirectory() as d:
            export_schedules(self.model,self.top,d,3)
            lighting=(Path(d)/'02_lighting_takeoff.html').read_text()
            self.assertLess(lighting.index('<h2>Fixtures'),lighting.index('<h2>Light Points By Type'))
            zone=(Path(d)/'03_zones_room_devices.html').read_text()
            self.assertLess(zone.index('<h2>Zones'),zone.index('<h2>Room Devices'))
            self.assertFalse(json.loads((Path(d)/'schedule_export_report.json').read_text())['pdf_markup_generated'])
    def test_v11_device_tags_unique_and_room_links_checked(self):
        self.assertEqual(validate(self.top,self.model)[0],[])
        device=copy.deepcopy(self.top['devices'][0]);device['id']='DEVICE-2';device['room_id']='MISSING';self.top['devices'].append(device)
        self.assertIn('device-tag',{i['rule'] for i in validate(self.top,self.model)[0]})
        self.assertIn('topology-reference',{i['rule'] for i in validate(self.top,self.model)[0]})

if __name__=='__main__':unittest.main()
