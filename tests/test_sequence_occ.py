"""Synthetic OCC applicability boundaries and evidence-preserving results.

The normative IECC catalog remains external in knowledgebase_wikijs.
"""
import copy
import unittest

from generators.sequence_code_validate import applicability, validate, PROCESS_REV


GENERAL = [dict(key='occupancy_required',op='eq',value=True),
    dict(key='vacancy_timeout_minutes',op='max',value=20),
    dict(key='max_auto_on_percent',op='max',value=50,allow_alternative='manual_on'),
    dict(key='manual_off_available',op='eq',value=True)]


def catalog():
    def rule(rid, types, requirements, **conditions):
        return dict(id=rid,edition='2021',section='synthetic-scope',
            verification='secondary_corroborated_needs_primary',
            source_urls=['https://codes.iccsafe.org'],
            applies=dict(space_types=types,special_application=False,**conditions),
            requirements=copy.deepcopy(requirements))
    return dict(catalog_id='SYNTHETIC-OCC',revision='0.2.0',
        minimum_process_revision='0.2.0',rules=[
            rule('TEST-FULL-ON',['restroom','locker_room'],GENERAL[:2]),
            rule('TEST-SMALL',['electrical_mechanical','it_telecom','janitorial','other'],
                 GENERAL,max_area_sq_ft=300,enclosed_full_height=True)])


def inputs(space_type='electrical_mechanical',area=300,enclosed=True):
    basis=dict(standard='IECC',edition='2021',compliance_path='prescriptive',
        applicability_status='confirmed',adoption_evidence='Synthetic confirmed basis',
        amendments_reviewed=True,exceptions_reviewed=True)
    context=dict(space_type=space_type,area_sq_ft=area,
        enclosed_full_height=enclosed,special_application=False)
    assignment=dict(endpoint_zone_id='SYNTH-ENDPOINT',sequence_id='PSEQ-TEST',
        sequence_revision='r1',parameters=dict(occupancy_required=True,
        vacancy_timeout_minutes=20,manual_on=True,manual_off_available=True))
    return basis,context,assignment


class OccupantCatalogTests(unittest.TestCase):
    def test_inclusive_300_and_exclusive_boundaries_are_distinct(self):
        c=catalog();rule=c['rules'][1]
        for n,expected in [(0,True),(299.9,True),(300,True),(300.5,False)]:
            with self.subTest(area=n):
                basis,context,assignment=inputs(area=n)
                self.assertIs(applicability(rule,context),expected)
                r=validate(c,basis,context,assignment)
                self.assertIn(rule['id'],r['applied_rules'] if expected else r['skipped_rules'])
        exclusive=copy.deepcopy(rule)
        del exclusive['applies']['max_area_sq_ft']
        exclusive['applies']['max_area_exclusive_sq_ft']=300
        self.assertIs(applicability(exclusive,inputs()[1]),False)

    def test_unknown_full_height_is_unresolved_not_false(self):
        for value in (None,'true',1):
            with self.subTest(value=value):
                basis,context,assignment=inputs(enclosed=value)
                result=validate(catalog(),basis,context,assignment)
                self.assertIn('TEST-SMALL',result['unresolved_rules'])
                self.assertEqual(result['status'],'needs_review')
        basis,context,assignment=inputs();del context['enclosed_full_height']
        self.assertIsNone(applicability(catalog()['rules'][1],context))

    def test_known_false_enclosure_skips_without_claiming_coverage(self):
        basis,context,assignment=inputs(enclosed=False)
        r=validate(catalog(),basis,context,assignment)
        self.assertIn('TEST-SMALL',r['skipped_rules'])
        self.assertTrue(any(f['rule_id']=='COVERAGE' for f in r['findings']))
        self.assertFalse(r['compliance_certified'])

    def test_unknown_invalid_area_stays_unresolved(self):
        for value in (None,False,'300',float('nan'),float('inf'),-1):
            with self.subTest(area=value):
                basis,context,assignment=inputs(area=value)
                self.assertIsNone(applicability(catalog()['rules'][1],context))
        # A known failed prerequisite still excludes a rule despite another unknown.
        self.assertIs(applicability(catalog()['rules'][1],inputs(area=301,enclosed=None)[1]),False)

    def test_restroom_and_locker_full_on_have_no_manual_off_conflict(self):
        for typ in ('restroom','locker_room'):
            for manual_off in (None,False,True):
                with self.subTest(space_type=typ,manual_off=manual_off):
                    basis,context,a=inputs(typ)
                    a['parameters']=dict(occupancy_required=True,
                        vacancy_timeout_minutes=20,max_auto_on_percent=100,manual_on=False)
                    if manual_off is not None:a['parameters']['manual_off_available']=manual_off
                    before=copy.deepcopy(a)
                    r=validate(catalog(),basis,context,a)
                    self.assertEqual(r['status'],'needs_review')
                    self.assertEqual(r['applied_rules'],['TEST-FULL-ON'])
                    self.assertFalse(any(f['status']=='conflict' for f in r['findings']))
                    self.assertFalse(any(f.get('parameter')=='manual_off_available' for f in r['findings']))
                    self.assertFalse(r['compliance_certified'])
                    self.assertEqual(a,before)

    def test_full_on_exception_still_checks_occupancy_and_timeout(self):
        for params in (dict(occupancy_required=False,vacancy_timeout_minutes=20),
                       dict(occupancy_required=True,vacancy_timeout_minutes=21)):
            with self.subTest(params=params):
                basis,context,a=inputs('restroom');a['parameters']=params
                self.assertEqual(validate(catalog(),basis,context,a)['status'],'conflict')
        basis,context,a=inputs('restroom');a['parameters']={}
        pending=validate(catalog(),basis,context,a)
        self.assertTrue(any(f.get('parameter')=='vacancy_timeout_minutes' for f in pending['findings']))

    def test_small_room_keeps_manual_on_off_and_secondary_evidence_gates(self):
        basis,context,a=inputs()
        c=catalog();r=validate(c,basis,context,a)
        self.assertEqual(r['status'],'needs_review')
        self.assertEqual(len(r['findings']),1)
        self.assertIn('not yet verified',r['findings'][0]['reason'])
        a['parameters'].update(manual_on=False,max_auto_on_percent=100,manual_off_available=False)
        r=validate(c,basis,context,a)
        self.assertEqual(r['status'],'conflict')
        self.assertEqual({f.get('parameter') for f in r['findings'] if f['status']=='conflict'},
                         {'max_auto_on_percent','manual_off_available'})

    def test_revision_delta_does_not_rewrite_accepted_parameters(self):
        basis,context,a=inputs('restroom')
        a['parameters'].update(manual_on=False,max_auto_on_percent=100,manual_off_available=False)
        old=catalog();old['revision']='0.1.0'
        old['rules'][0]['requirements']=copy.deepcopy(GENERAL)
        before=copy.deepcopy(a)
        prior=validate(old,basis,context,a)
        current=validate(catalog(),basis,context,a,prior)
        self.assertEqual(prior['status'],'conflict')
        self.assertEqual(current['status'],'needs_review')
        self.assertTrue(current['delta']['resolved_findings'])
        self.assertNotEqual(prior['input_fingerprint'],current['input_fingerprint'])
        self.assertEqual(a,before)

    def test_specific_application_prerequisite_is_not_ignored(self):
        r=catalog()['rules'][1]
        r['applies']['specific_application']=False
        ctx=inputs()[1]
        self.assertIsNone(applicability(r,ctx))
        ctx['specific_application']=False
        self.assertIs(applicability(r,ctx),True)
        ctx['specific_application']=True
        self.assertIs(applicability(r,ctx),False)

    def test_future_engine_requirement_and_unknown_constraint_fail_explicitly(self):
        basis,context,a=inputs()
        future=catalog();future['minimum_process_revision']='999.0.0'
        with self.assertRaisesRegex(ValueError,'newer process'):
            validate(future,basis,context,a)
        bad=catalog();bad['rules'][1]['applies']['unknown_condition']=True
        with self.assertRaisesRegex(ValueError,'Unsupported rule applicability'):
            validate(bad,basis,context,a)
        self.assertEqual(validate(catalog(),basis,context,a)['process_revision'],PROCESS_REV)


if __name__=='__main__':
    unittest.main()
