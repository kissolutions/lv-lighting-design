"""Dimming scheme and fixture interface regression cases."""
import copy
import tempfile
import unittest
from pathlib import Path
from generators.dimming_interfaces import validate as fixture_validate, export as fixture_export
from generators.m3_sequence_review import validate as m3_validate
from tests.test_m3_sequence_review import example

def setup_fixtures():
    model={'project':{'id':'P1','model_revision':'R1'},
      'source_references':[{'id':'SRC1'}],
      'fixture_types':[{'id':'F1','source_mark':'A1','source_dimming_capability':'dimmable'}]}
    record={'schema_version':'0.1.0','project_id':'P1','model_revision':'R1',
      'fixtures':[{'fixture_type_id':'F1','interface_basis':'source',
        'dimming_interfaces':['zero_to_ten_v'],'supported_dimming_schemes':['continuous'],
        'minimum_dim_percent':1,'dim_to_off':False,'signal_mode':'sink',
        'driver_location':'remote','source_ref_ids':['SRC1'],'notes':'Manufacturer schedule'}]}
    return model,record

class DimmingInterfaceTests(unittest.TestCase):
    def test_valid_and_csv(self):
        model,record=setup_fixtures()
        self.assertEqual(fixture_validate(model,record,True),[])
        with tempfile.TemporaryDirectory() as folder:
            self.assertEqual(fixture_export(model,record,Path(folder)/'out',True),[])
            self.assertIn('zero_to_ten_v',(Path(folder)/'out/fixture_dimming_schedule.csv').read_text())
    def test_enum_rejects_unapproved_value(self):
        model,r=setup_fixtures();r['fixtures'][0]['dimming_interfaces']=['triac']
        self.assertTrue(fixture_validate(model,r))
    def test_none_exclusive(self):
        model,r=setup_fixtures();r['fixtures'][0]['dimming_interfaces']=['none','zero_to_ten_v']
        self.assertTrue(any('mutually exclusive' in x['message'] for x in fixture_validate(model,r)))
    def test_non_dimmable_contradiction(self):
        model,r=setup_fixtures();model['fixture_types'][0]['source_dimming_capability']='non_dimmable'
        self.assertTrue(any('conflicts' in x['message'] for x in fixture_validate(model,r)))
    def test_no_dimming_cannot_report_minimum(self):
        model,r=setup_fixtures();r['fixtures'][0].update(dimming_interfaces=['none'],supported_dimming_schemes=['none'])
        self.assertTrue(any('null minimum' in x['message'] for x in fixture_validate(model,r)))
    def test_incomplete_source_schedule(self):
        model,r=setup_fixtures();r['fixtures']=[]
        self.assertTrue(any('missing' in x['message'] for x in fixture_validate(model,r,True)))

class M3DimmingSchemeTests(unittest.TestCase):
    def make_v02(self):
        model,c=example();c['schema_version']='0.2.0'
        c['project_sequences'][0]['functions'].update(dimming_scheme='continuous',dimming_steps=None)
        for a in c['assignments']:a['dimming_scheme_override']=None
        return model,c
    def test_continuous_passes(self):
        model,c=self.make_v02();self.assertEqual(m3_validate(model,c,locked=True),[])
    def test_stepped_requires_step_count(self):
        model,c=self.make_v02();c['project_sequences'][0]['functions']['dimming_scheme']='stepped'
        self.assertTrue(any('needs number' in x['message'] for x in m3_validate(model,c)))
        c['project_sequences'][0]['functions']['dimming_steps']=3
        self.assertEqual(m3_validate(model,c),[])
    def test_none_cannot_have_steps(self):
        model,c=self.make_v02();c['project_sequences'][0]['functions'].update(dimming_scheme='none',dimming_steps=3)
        self.assertTrue(any('only to stepped' in x['message'] for x in m3_validate(model,c)))
    def test_override_requires_owner_explanation(self):
        model,c=self.make_v02();c['assignments'][0]['dimming_scheme_override']='stepped'
        self.assertTrue(any('requires explanation' in x['message'] for x in m3_validate(model,c)))
    def test_unknown_blocks_approved(self):
        model,c=self.make_v02();c['project_sequences'][0]['functions']['dimming_scheme']='unknown'
        self.assertTrue(any('must declare' in x['message'] for x in m3_validate(model,c)))

if __name__=='__main__':unittest.main()
