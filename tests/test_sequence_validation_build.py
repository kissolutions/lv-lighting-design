"""Test mandatory build process and safe source validation against SEQ definitions."""
import copy
import unittest
from generators.sequence_validation_build import build
from test_sequence_code_validate import RULES,context


class BuildValidationTests(unittest.TestCase):
    def setup_case(self,edition='2021'):
        basis,space,assignment=context(edition)
        model={'project':{'id':'P','model_revision':'R1'},'spaces':[{'id':'S1'}],
            'light_zones':[{'id':'Z-1','parent_zone_id':None}]}
        companion={'project_id':'P','model_revision':'R1','project_sequences':[
            dict(id='PSEQ-001',revision='r1',status='reviewed',
                functions=dict(dimming_scheme='unknown'))],
            'assignments':[dict(endpoint_zone_id='Z-1',sequence_id='PSEQ-001',
                sequence_revision='r1',parameters={},dimming_scheme_override=None)]}
        return model,companion,basis,{'Z-1':dict(space,space_id='S1')}
    def test_valid_missing_fields_proposes_but_does_not_mutate(self):
        m,c,b,s=self.setup_case('2021')
        before=copy.deepcopy(c)
        result=build(m,c,RULES,b,s)
        self.assertEqual(c,before)
        self.assertEqual(result['status'],'needs_review')
        self.assertIn('vacancy_timeout_minutes',result['results'][0]['proposed_missing_parameters'])
    def test_code_change_does_not_silently_change_original_sequence(self):
        m,c,b,s=self.setup_case('2021')
        c['project_sequences'][0]['functions']['dimming_scheme']='none'
        c['assignments'][0]['parameters'].update(vacancy_timeout_minutes=20,manual_on=True,manual_off_available=True)
        before=copy.deepcopy(c)
        old=build(m,c,RULES,b,s)
        b['edition']='2024'
        later=build(m,c,RULES,b,s,prior=old)
        self.assertEqual(c,before)
        self.assertEqual(later['status'],'conflict')
        self.assertTrue(later['results'][0]['delta']['new_findings'])
    def test_missing_space_context_is_failure_not_skipped(self):
        m,c,b,s=self.setup_case()
        res=build(m,c,RULES,b,{})
        self.assertEqual(res['status'],'conflict')
        self.assertIn('Missing',res['blocking_integration_issues'][0]['error'])
    def test_parent_zone_is_blocked(self):
        m,c,b,s=self.setup_case()
        m['light_zones'].append(dict(id='Z-child',parent_zone_id='Z-1'))
        res=build(m,c,RULES,b,s)
        self.assertEqual(res['status'],'conflict')
    def test_sequence_definitions_are_pinned(self):
        m,c,b,s=self.setup_case()
        c['assignments'][0]['sequence_revision']='other'
        res=build(m,c,RULES,b,s)
        self.assertEqual(res['status'],'conflict')


if __name__=='__main__':unittest.main()
