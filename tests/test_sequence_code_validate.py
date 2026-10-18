"""IECC 2021/2024 rule evaluator regression: unknowns, applicability, deltas."""
import copy
import unittest
from generators.sequence_code_validate import validate,applicability,check

RULES=dict(catalog_id='TEST-IECC',revision='0.1.0',rules=[
  dict(id='21-occupancy',edition='2021',section='C405.2.1.1',
       verification='primary_text_reviewed',source_urls=['https://codes.iccsafe.org'],
       applies=dict(space_types=['enclosed_office','conference'],special_application=False),
       requirements=[dict(key='vacancy_timeout_minutes',op='max',value=20),
          dict(key='max_auto_on_percent',op='max',value=50,allow_alternative='manual_on'),
          dict(key='manual_off_available',op='eq',value=True)]),
  dict(id='21-daylight',edition='2021',section='C405.2.4.1',
       verification='primary_text_reviewed',source_urls=['https://codes.iccsafe.org'],
       applies=dict(daylight_control_required=True,special_application=False),
       requirements=[dict(key='daylight_dimming_scheme',op='eq',value='continuous'),
          dict(key='daylight_minimum_light_output_percent',op='max',value=15)]),
  dict(id='24-dimming',edition='2024',section='C405.2.3',
       verification='secondary_corroborated_needs_primary',source_urls=['https://assets.lutron.com'],
       applies=dict(space_types=['enclosed_office','conference'],special_application=False,high_end_trim_exception=False),
       requirements=[dict(key='dimming_scheme',op='eq',value='continuous'),
          dict(key='manual_minimum_power_percent',op='max',value=10),
          dict(key='manual_dim_to_off',op='eq',value=True)])])


def context(edition='2021',space_type='enclosed_office',daylight=False,**kwargs):
    regulatory=dict(standard='IECC',edition=edition,compliance_path='prescriptive',
       applicability_status='confirmed',adoption_evidence='AHJ documented',amendments_reviewed=True,exceptions_reviewed=True)
    space=dict(space_type=space_type,area_sq_ft=250,daylight_control_required=daylight,
       special_application=False,high_end_trim_exception=False)
    space.update(kwargs)
    assignment=dict(endpoint_zone_id='Z-1',sequence_id='PSEQ-001',sequence_revision='r1',parameters={})
    return regulatory,space,assignment


class RuleProcessTests(unittest.TestCase):
    def evaluate(self,edition='2021',**kwargs):
        basis,space,seq=context(edition,**kwargs)
        return validate(RULES,basis,space,seq)
    def test_2021_proposes_missing_timeout_without_mutation(self):
        basis,space,a=context('2021')
        before=copy.deepcopy(a)
        r=validate(RULES,basis,space,a)
        self.assertEqual(a,before)
        self.assertEqual(r['status'],'needs_review')
        self.assertEqual(r['proposed_missing_parameters']['manual_off_available']['proposed_value'],True)
        self.assertIn('vacancy_timeout_minutes',r['proposed_missing_parameters'])
    def test_2021_accepted_values_pass(self):
        basis,space,a=context('2021')
        a['parameters'].update(vacancy_timeout_minutes=20,manual_on=True,manual_off_available=True)
        r=validate(RULES,basis,space,a)
        self.assertEqual(r['status'],'rule_checks_passed')
    def test_2021_excess_timeout_is_conflict(self):
        basis,space,a=context('2021')
        a['parameters'].update(vacancy_timeout_minutes=25,manual_on=True,manual_off_available=True)
        r=validate(RULES,basis,space,a)
        self.assertEqual(r['status'],'conflict')
    def test_2021_daylight_15_percent(self):
        basis,space,a=context('2021',daylight=True)
        a['parameters'].update(vacancy_timeout_minutes=20,manual_on=True,manual_off_available=True,
           daylight_dimming_scheme='continuous',daylight_minimum_light_output_percent=20)
        r=validate(RULES,basis,space,a)
        self.assertTrue(any(f.get('parameter')=='daylight_minimum_light_output_percent' and f['status']=='conflict' for f in r['findings']))
    def test_2024_office_continuous_is_required(self):
        basis,space,a=context('2024')
        a['parameters'].update(dimming_scheme='stepped',manual_minimum_power_percent=10,manual_dim_to_off=True)
        r=validate(RULES,basis,space,a)
        self.assertEqual(r['status'],'conflict')
    def test_2024_secondary_evidence_cannot_certify(self):
        basis,space,a=context('2024')
        a['parameters'].update(dimming_scheme='continuous',manual_minimum_power_percent=10,manual_dim_to_off=True)
        r=validate(RULES,basis,space,a)
        self.assertEqual(r['status'],'needs_review')
        self.assertFalse(r['compliance_certified'])
    def test_high_end_trim_exception_requires_separate_review(self):
        basis,space,a=context('2024',high_end_trim_exception=True)
        r=validate(RULES,basis,space,a)
        self.assertEqual(r['status'],'needs_review')
        self.assertIn('COVERAGE',[f['rule_id'] for f in r['findings']])
    def test_unknown_exception_not_false(self):
        basis,space,a=context('2024',high_end_trim_exception=None)
        r=validate(RULES,basis,space,a)
        self.assertIn('24-dimming',r['unresolved_rules'])
    def test_provisional_adoption_never_passes(self):
        basis,space,a=context('2021')
        basis['applicability_status']='provisional'
        a['parameters'].update(vacancy_timeout_minutes=20,manual_on=True,manual_off_available=True)
        r=validate(RULES,basis,space,a)
        self.assertEqual(r['status'],'needs_review')
    def test_switch_code_revision_delta(self):
        basis,space,a=context('2021')
        a['parameters'].update(vacancy_timeout_minutes=20,manual_on=True,manual_off_available=True,
            dimming_scheme='none',manual_minimum_power_percent=30,manual_dim_to_off=True)
        old=validate(RULES,basis,space,a)
        basis['edition']='2024'
        new=validate(RULES,basis,space,a,old)
        self.assertEqual(old['status'],'rule_checks_passed')
        self.assertEqual(new['status'],'conflict')
        self.assertTrue(new['delta']['new_findings'])
    def test_wrong_path_rejected(self):
        basis,space,a=context('2024')
        basis['compliance_path']='ashrae_90_1'
        with self.assertRaises(ValueError):validate(RULES,basis,space,a)


if __name__=='__main__':unittest.main()
