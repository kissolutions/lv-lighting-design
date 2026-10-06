"""Boundary checks for physical port/feed separation and installation constraints."""
import copy
import json
import unittest
from pathlib import Path
from generators.validate_topology import validate, SCHEMA
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[1]

class TopologyTests(unittest.TestCase):
    def setUp(self):
        self.top=json.loads((ROOT/'templates/controller-power-topology-v1.template.json').read_text())
        self.model=dict(project=dict(id='REPLACE-PROJECT-ID'),spaces=[dict(id='SP-1')],light_zones=[dict(id='Z-1')],drawing_pages=[dict(id='PAGE-1',width_pt=100,height_pt=100)],source_references=[],branch_circuits=[dict(power_units=[dict(id='PU-1',channels=[dict(id='CH-1',light_zone_id='Z-1',controller_id=None),dict(id='CH-2',light_zone_id='Z-1',controller_id=None)])])])
        self.top['areas']=[dict(id='AREA-1',space_ids=['SP-1'],return_air_plenum=False,source_ref_ids=[])]
        for kind,number in [('PDU',8),('QDCD',4),('CIO',None),('SW8',None),('sensor',None)]:
            self.top['devices'].append(dict(id=kind+'-1',kind=kind,canonical_entity_id=None,model=None,smart=False,output_count=number,rated_total_watts=None,available_input_watts=None,connected_demand_watts=None,bus_demand_ma=0,casambi=False,source_ref_ids=[],location=dict(area_id='AREA-1',drawing_page_id='PAGE-1',x_pt=1,y_pt=1,mounting='above_ceiling',owner_review='proposed'),rationale=None))
        self.top['channel_assignments']=[dict(micro_channel_id='CH-1',device_id='QDCD-1',output=1,connected_watts=40,control_zone_ids=['Z-1'])]
        self.top['power_feeds']=[dict(id='F-'+str(i),pdu_id='PDU-1',pdu_output=i,qdcd_id='QDCD-1',qdcd_input=i,demand_watts=45,rated_watts=100,source_ref_ids=[]) for i in range(1,5)]
        self.top['control_connections']=[dict(device_id='sensor-1',aggregator_id='SW8-1',input_port=1,control_zone_ids=['Z-1'],micro_channel_ids=['CH-1'],qdcd_ids=['QDCD-1'])]
    def rules(self):return {i['rule'] for i in validate(self.top,self.model)[0]}
    def test_schema_and_separate_power_output_domains(self):
        Draft202012Validator.check_schema(json.loads(SCHEMA.read_text()))
        self.assertEqual(self.rules(),set())
    def test_feed_and_direct_output_collision(self):
        self.top['devices'][0].update(output_count=16,smart=True)
        self.top['channel_assignments'].append(dict(micro_channel_id='CH-2',device_id='PDU-1',output=1,connected_watts=30,control_zone_ids=['Z-1']))
        self.assertIn('feed-collision',self.rules())
    def test_reduced_feed_is_exception(self):
        self.top['power_feeds'].pop();self.assertIn('reduced-feed',self.rules())
    def test_shared_wire_port_rejected(self):
        sensor=copy.deepcopy(self.top['devices'][-1]);sensor['id']='sensor-2';self.top['devices'].append(sensor)
        row=copy.deepcopy(self.top['control_connections'][0]);row['device_id']='sensor-2';self.top['control_connections'].append(row)
        self.assertIn('sensor-port',self.rules())
    def test_plenum_and_unknown_qdcd_sensor_inputs(self):
        self.top['areas'][0]['return_air_plenum']=True
        self.top['control_connections'][0]['aggregator_id']='QDCD-1'
        self.assertIn('plenum',self.rules());self.assertIn('sensor-capacity',self.rules())
    def test_bus_limits_and_sensor_count_are_separate(self):
        self.top['devices'][3]['bus_demand_ma']=251
        self.top['bus_assignments']=[dict(device_id='SW8-1',cio_id='CIO-1',bus='SDCnet',bus_units=17)]
        issues,counts=validate(self.top,self.model)
        self.assertIn('bus-power',{i['rule'] for i in issues});self.assertIn('bus-capacity',{i['rule'] for i in issues})
        self.assertEqual(counts['physical_sensor_count'],1)
    def test_smart_eight_output_unavailable(self):
        self.top['devices'][0]['smart']=True
        self.assertIn('smart-pdu',self.rules())
    def test_final_blocks_unconfirmed_locations_and_power(self):
        rules={i['rule'] for i in validate(self.top,self.model,final=True)[0]}
        self.assertIn('owner-location',rules);self.assertIn('input-budget',rules)

if __name__=='__main__':unittest.main()
