"""Regression tests for the M3 companion without modifying v0.7+ project schemas."""
import copy
import tempfile
import unittest
from pathlib import Path
from generators.m3_sequence_review import validate, export


def example():
    model=dict(project=dict(id='TEST',name='Synthetic Open Office',model_revision='M3-T1',
        controls_narrative_review=dict(status='locked',decision_id='DEC-1')),
        spaces=[
            dict(id='S1',name='Open Office',light_zone_ids=['Z-P'],light_object_ids=['L1','L2']),
            dict(id='S2',name='Unlit Storage',light_zone_ids=[],light_object_ids=[])],
        light_zones=[
            dict(id='Z-P',parent_zone_id=None,light_object_ids=[],label='Open Office Parent'),
            dict(id='Z-A',parent_zone_id='Z-P',light_object_ids=['L1'],label='Occupancy A'),
            dict(id='Z-B',parent_zone_id='Z-P',light_object_ids=['L2'],label='Occupancy B')],
        light_objects=[dict(id='L1'),dict(id='L2')],
        decisions=[dict(id='DEC-1',status='confirmed')])
    f=dict(manual='Manual off',occupancy='Vacancy off',light_reduction='Off',
        daylight='No daylight control for this example',schedule='None',
        emergency='Separately reviewed')
    companion=dict(schema_version='0.1.0',project_id='TEST',model_revision='M3-T1',
        project_sequences=[dict(id='PSEQ-001',revision='1',status='approved',
            title='Synthetic private use',narrative='Owner-approved test narrative.',functions=f,source_refs=[])],
        assignments=[dict(endpoint_zone_id=z,sequence_id='PSEQ-001',sequence_revision='1',
            assignment_status='accepted',origin_basis='owner_custom',decision_id='DEC-1',
            parameters={},requirement_refs=['R1'],source_intent_refs=[],override_note=None) for z in ('Z-A','Z-B')],
        daylight_determinations=[dict(space_id=s,determination='no',basis='Reviewed no-glazing evidence',
            source_refs=[]) for s in ('S1','S2')],
        space_direction_reviews=[
            dict(space_id='S1',disposition='lit_controlled',endpoint_zone_ids=['Z-A','Z-B'],
                light_object_ids=['L1','L2'],source_refs=[],notes=''),
            dict(space_id='S2',disposition='unlit_confirmed',endpoint_zone_ids=[],
                light_object_ids=[],source_refs=[],notes='Owner-confirmed no lights')],
        deferred_items=[])
    return model,companion


class SequenceReviewTests(unittest.TestCase):
    def test_valid_leaf_assignments_and_export(self):
        model,companion=example()
        self.assertEqual(validate(model,companion,locked=True),[])
        with tempfile.TemporaryDirectory() as dest:
            findings=export(model,companion,Path(dest)/'m3',locked=True)
            self.assertEqual(findings,[])
            content=(Path(dest)/'m3/m3_sequence_narratives.html').read_text()
            self.assertEqual(content.count('Owner-approved test narrative.'),1)
            self.assertIn('Z-A',content)
            self.assertIn('Z-B',content)
            self.assertTrue((Path(dest)/'m3/m3_endpoint_assignments.csv').exists())

    def test_parent_assignment_rejected(self):
        model,c=example();c['assignments'][0]['endpoint_zone_id']='Z-P'
        self.assertTrue(any('Parent zones' in f['message'] for f in validate(model,c)))

    def test_missing_leaf_blocks_lock(self):
        model,c=example();c['assignments'].pop()
        self.assertTrue(any('Every leaf' in f['message'] for f in validate(model,c,locked=True)))

    def test_unknown_or_draft_standard_rejected(self):
        model,c=example();c['assignments'][0].update(sequence_id='SEQ-006',origin_basis='matched_standard')
        self.assertTrue(any('Unresolved sequence' in f['message'] for f in validate(model,c)))
        catalog=[dict(id='SEQ-006',revision='1',status='draft',title='Example')]
        self.assertTrue(any('not approved' in f['message'] for f in validate(model,c,catalog)))

    def test_duplicate_assignment_rejected(self):
        model,c=example();c['assignments'].append(copy.deepcopy(c['assignments'][0]))
        self.assertTrue(any('Multiple active' in f['message'] for f in validate(model,c)))

    def test_acceptance_needs_owner_decision(self):
        model,c=example();c['assignments'][0]['decision_id']=None
        self.assertTrue(any('confirmed owner decision' in f['message'] for f in validate(model,c)))

    def test_daylight_unknown_blocks_lock(self):
        model,c=example();c['daylight_determinations'][0]['determination']='unresolved'
        self.assertTrue(any('Daylight determination unresolved' in f['message'] for f in validate(model,c,locked=True)))

    def test_project_and_revision_mismatch_rejected(self):
        model,c=example();c['model_revision']='OTHER'
        self.assertTrue(any('revision differs' in f['message'] for f in validate(model,c)))


if __name__=='__main__':
    unittest.main()
