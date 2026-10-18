"""Optional numeric CCT and CRI contract for original and selected fixtures."""
import copy
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT=Path(__file__).resolve().parents[1]
SCHEMA=json.loads((ROOT/'schemas/lighting-project-v0.9.schema.json').read_text())
MODEL=json.loads((ROOT/'docs/reference-implementations/synthetic-spaces/lighting-model.json').read_text())


class ColorAttributesTests(unittest.TestCase):
    def setUp(self):
        # Test nested contracts independently against a representative
        # existing model; project schema compatibility is checked by CI.
        self.ft=SCHEMA['$defs']['fixture_type_v02']['properties']
        self.design=SCHEMA['$defs']['light']['properties']['design']['properties']

    def test_exactly_four_optional_numeric_fields(self):
        for props,prefix in ((self.ft,'source'),(self.design,'selected')):
            for suffix in ('cct_k','cri'):
                field=props[prefix+'_'+suffix]
                self.assertEqual(field['type'],['number','null'])
                self.assertNotIn(prefix+'_'+suffix,SCHEMA['$defs']['fixture_type_v02'].get('required',[]))
                self.assertIsNone(Draft202012Validator(field).validate(None))
                self.assertIsNone(Draft202012Validator(field).validate(3500 if suffix=='cct_k' else 90))
                for wrong in ('3500','90',True,-1):
                    with self.assertRaises(Exception):
                        Draft202012Validator(field).validate(wrong)

    def test_zero_is_not_blank(self):
        for props,prefix in ((self.ft,'source'),(self.design,'selected')):
            with self.assertRaises(Exception):
                Draft202012Validator(props[prefix+'_cct_k']).validate(0)
            self.assertIsNone(Draft202012Validator(props[prefix+'_cri']).validate(0))

    def test_cri_maximum(self):
        for props,prefix in ((self.ft,'source'),(self.design,'selected')):
            with self.assertRaises(Exception):
                Draft202012Validator(props[prefix+'_cri']).validate(101)


    def test_v09_intake_projection_preserves_color_values_and_legacy_checks(self):
        from generators.model_intake import check_model
        model=json.loads((ROOT/'docs/reference-implementations/synthetic-bundles/lighting-model.json').read_text())
        baseline=check_model(copy.deepcopy(model),'intake')
        self.assertTrue(baseline['checks_pass'],baseline['issues'])
        for idx,fixture in enumerate(model['fixture_types']):
            fixture['source_cct_k']=3500 if idx%2==0 else None
            fixture['source_cri']=90 if idx%2==0 else 80
        for idx,light in enumerate(model['light_objects']):
            light['design']['selected_cct_k']=3500 if idx%2==0 else None
            light['design']['selected_cri']=None if idx%2==0 else 90
        before=copy.deepcopy(model)
        Draft202012Validator(SCHEMA).validate(model)
        report=check_model(model,'intake')
        self.assertTrue(report['checks_pass'],report['issues'][:10])
        self.assertEqual(model,before,'Checking must not erase authoritative color data')
        self.assertEqual(report['checks_pass'],baseline['checks_pass'])
        self.assertNotIn('schema',{x['rule'] for x in report['issues']})


if __name__=='__main__':
    unittest.main()
