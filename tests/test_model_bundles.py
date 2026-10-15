"""Synthetic v0.9 invariants, review failures and legacy integration."""
import copy
import json
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator
from generators.model_bundles import (SCHEMAS, apply_geometry_return,
    apply_model_geometry_return, build, bundle_id, read_tables, write_tables,
    upgrade_v09, nested_view)
from generators.model_intake import check_model

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT/'docs/reference-implementations/synthetic-bundles'


class BundleTests(unittest.TestCase):
    def setUp(self):
        self.model = json.loads((FIXTURE/'lighting-model.json').read_text())
        self.r = self.model['bundle_routes']
        self.up = [b for b in self.r['bundles'] if b['flow']=='upstream']

    def returned(self, dx=0):
        rows = []
        for b in self.r['bundles']:
            row = {k:b[k] for k in ('annotation_id','bundle_id','parent_bundle_id','serves','source_id','flow','frame_id')}
            row['vertices'] = [[g['x']+dx,g['y']] for g in sorted(
                (g for g in self.r['geometry'] if g['bundle_id']==b['bundle_id']),key=lambda g:g['seq'])]
            rows.append(row)
        return rows

    def test_three_level_counts_and_physical_circuit_distinction(self):
        report = build(self.r,self.model)
        byid = {b['bundle_id']:b for b in report['bundles']}
        self.assertEqual([byid[b['bundle_id']]['downstream_cables'] for b in self.up], [4,3,1])
        self.assertEqual([byid[b['bundle_id']]['downstream_controllers'] for b in self.up], [3,2,1])
        self.assertEqual([byid[b['bundle_id']]['cables_terminating'] for b in self.up], [1,2,1])
        self.assertEqual(report['totals']['upstream']['cables'],4)
        self.assertEqual(report['totals']['upstream']['cable_centerline_ft'],80)
        self.assertEqual(report['totals']['drop']['cables'],1)
        self.assertFalse(report['electrical_routing_validated'])
        self.assertFalse(report['installed_length_validated'])
        self.assertEqual(sum(c['flow']=='upstream' for c in self.r['cables']),4)
        self.assertEqual(len(self.r['circuits']),6)  # five upstream feeds plus one drop

    def test_disconnected_cycle_names_edges_without_repair(self):
        self.up[0]['parent_bundle_id'] = self.up[-1]['bundle_id']
        original=copy.deepcopy(self.r)
        with self.assertRaisesRegex(ValueError,'Cycle edges:') as error:
            build(self.r)
        for b in self.up:
            self.assertIn(b['bundle_id'],str(error.exception))
        self.assertEqual(self.r,original)

    def test_geometry_translation_preserves_ids_topology_and_station(self):
        before=build(self.r)
        result=apply_geometry_return(self.r,self.returned(20))
        self.assertEqual(result['records']['bundles'], self.r['bundles'])
        self.assertEqual(result['records']['attachments'], self.r['attachments'])
        for a,b in zip(before['controller_positions'],result['derived']['controller_positions']):
            self.assertAlmostEqual(b['x']-a['x'],20)
            self.assertEqual(a['y'],b['y'])
        self.assertEqual(result['invalidated_assumption_ids'],['ASM-ROUTE-SYNTHETIC'])
        self.assertIn('voltage_drop',result['recompute_required'])

    def test_served_set_identity_changes_only_affected_branches(self):
        root, middle, leaf=self.up
        old_middle=middle['bundle_id']
        # Move C's branch from below B to directly below the unchanged ABC root.
        middle['serves']=[self.r['attachments'][1]['controller_id']]
        middle['bundle_id']=bundle_id(middle['serves'])
        leaf['parent_bundle_id']=root['bundle_id']
        self.r['attachments'][1]['parent_bundle_id']=middle['bundle_id']
        self.r['attachments'][2]['station_ft']=20
        for g in self.r['geometry']:
            if g['bundle_id']==old_middle:g['bundle_id']=middle['bundle_id']
            if g['bundle_id']==leaf['bundle_id'] and g['seq']==0:g['x']=10
        result=build(self.r,self.model)
        ids={b['bundle_id'] for b in result['bundles']}
        self.assertNotIn(old_middle,ids)
        self.assertIn(root['bundle_id'],ids)
        self.assertIn(leaf['bundle_id'],ids)
        self.assertIn(middle['bundle_id'],ids)
        self.assertEqual(result['totals']['upstream']['cables'],4)
        self.assertEqual(bundle_id(root['serves']),bundle_id(list(reversed(root['serves']))))

    def test_duplicate_served_set_is_not_deduplicated(self):
        self.r['bundles'].append(copy.deepcopy(self.up[0]))
        with self.assertRaises(ValueError):build(self.r)

    def test_topology_edit_rejected(self):
        returned=self.returned();returned[0]['serves']=['OTHER']
        with self.assertRaisesRegex(ValueError,'topology/frame change'):
            apply_geometry_return(self.r,returned)

    def test_missing_unknown_duplicate_annotation_rejected(self):
        for mode in ('missing','unknown','duplicate'):
            with self.subTest(mode=mode):
                returned=self.returned()
                if mode=='missing':returned.pop()
                if mode=='unknown':returned[0]['annotation_id']='UNKNOWN'
                if mode=='duplicate':returned.append(copy.deepcopy(returned[0]))
                with self.assertRaises(ValueError):apply_geometry_return(self.r,returned)

    def test_fixed_owner_device_does_not_silently_move(self):
        self.r['attachments'][0].update(review_status='accepted',location_basis='owner_returned')
        with self.assertRaisesRegex(ValueError,'accepted owner-returned device'):
            apply_geometry_return(self.r,self.returned(20))

    def test_model_assumptions_invalidated_without_mutating_input(self):
        updated,result=apply_model_geometry_return(self.model,self.returned(20))
        self.assertEqual(updated['assumptions'][0]['status'],'invalidated')
        self.assertEqual(self.model['assumptions'][0]['status'],'confirmed')
        self.assertFalse(result['derived']['electrical_routing_validated'])

    def test_station_bounds_and_shortened_geometry(self):
        self.r['attachments'][0]['station_ft']=11
        with self.assertRaisesRegex(ValueError,'station exceeds'):build(self.r)

    def test_cross_flow_parent_rejected(self):
        self.r['bundles'][-1]['parent_bundle_id']=self.up[-1]['bundle_id']
        with self.assertRaisesRegex(ValueError,'cross-flow'):build(self.r)

    def test_duplicate_endpoint_across_sources_rejected(self):
        duplicate=copy.deepcopy(self.r['attachments'][0]);duplicate['offset_ft']=2
        self.r['attachments'].append(duplicate)
        with self.assertRaisesRegex(ValueError,'Duplicate controller_id'):build(self.r)

    def test_invalid_derived_values_cannot_be_stored(self):
        self.up[0]['downstream_cables']=99
        with self.assertRaisesRegex(ValueError,'Additional properties'):build(self.r)

    def test_bad_served_set_and_unknown_parent_rejected(self):
        self.up[0]['parent_bundle_id']='UNKNOWN'
        with self.assertRaisesRegex(ValueError,'unknown parent'):build(self.r)
        self.up[0]['parent_bundle_id']=None
        self.up[0]['serves']=['OTHER']
        with self.assertRaisesRegex(ValueError,'identity'):build(self.r)

    def test_conductor_polarity_and_port_conflicts(self):
        self.r['conductors'][0]['parallel_group']=self.r['conductors'][1]['parallel_group']
        with self.assertRaisesRegex(ValueError,'Parallel group mixes'):build(self.r)

    def test_disconnected_child_geometry_rejected(self):
        g=next(g for g in self.r['geometry'] if g['bundle_id']==self.up[1]['bundle_id'] and g['seq']==0)
        g['y']+=1
        with self.assertRaisesRegex(ValueError,'disconnected'):build(self.r)

    def test_unknown_model_references_and_drop_assignment(self):
        m=copy.deepcopy(self.model);m['controllers']=[]
        with self.assertRaisesRegex(ValueError,'unknown canonical'):build(self.r,m)
        m=copy.deepcopy(self.model)
        m['branch_circuits'][0]['power_units'][0]['channels'][0]['controller_id']=None
        with self.assertRaisesRegex(ValueError,'not assigned'):build(self.r,m)

    def test_csv_roundtrip_and_source_matches_export(self):
        self.assertEqual(read_tables(FIXTURE/'tables'),self.r)
        with tempfile.TemporaryDirectory() as directory:
            write_tables(self.r,directory)
            self.assertEqual(read_tables(directory),self.r)
            with self.assertRaisesRegex(ValueError,'empty directory'):write_tables(self.r,directory)

    def test_nested_view_is_derived(self):
        view=nested_view(self.r)
        root=next(v for v in view if v['flow']=='upstream')
        self.assertEqual(root['children'][0]['children'][0]['downstream_cables'],1)

    def test_exported_review_is_derived_and_flows_are_explicit(self):
        from generators.export_intake import export_intake
        import csv
        with tempfile.TemporaryDirectory() as directory:
            report=export_intake(self.model,directory)
            self.assertTrue(report['checks_pass'])
            with (Path(directory)/'bundle_review_derived.csv').open() as f:
                rows=list(csv.DictReader(f))
            self.assertEqual({r['flow'] for r in rows},{'upstream','drop'})
            self.assertEqual(len(rows),4)

    def test_markup_manifest_binds_bundle_id_page_and_review(self):
        from generators.milestone_markup import validate_manifest
        manifest=json.loads((ROOT/'docs/reference-implementations/synthetic-milestones/markup-manifest.json').read_text())
        b=self.up[0]
        a=manifest['annotations'][0]
        a.update(annotation_id=b['annotation_id'],entity_type='route',entity_id=b['bundle_id'],
                 layer='cabling',location_basis=b['location_basis'])
        manifest['packages'][0]['annotation_ids']=[b['annotation_id']]
        result=validate_manifest(manifest,self.model)
        self.assertEqual(result,[])
        a['annotation_id']='WRONG-ID'
        manifest['packages'][0]['annotation_ids']=['WRONG-ID']
        result=validate_manifest(manifest,self.model)
        self.assertTrue(result)
        self.assertTrue(any('authoritative flat records' in i['message'] for i in result))

    def test_schema_and_intake_dispatch(self):
        Draft202012Validator.check_schema(json.loads((SCHEMAS/'lighting-project-v0.9.schema.json').read_text()))
        report=check_model(self.model,'intake')
        self.assertTrue(report['checks_pass'],report['issues'])
        self.assertIn('bundle_routes',report['derived'])

    def test_migration_keeps_legacy_valid_and_invents_no_routes(self):
        old=json.loads((ROOT/'docs/reference-implementations/synthetic-intake-review/lighting-model.json').read_text())
        snapshot=copy.deepcopy(old)
        new=upgrade_v09(old)
        self.assertEqual(old,snapshot)
        self.assertEqual(new['schema_version'],'0.9.0')
        self.assertTrue(all(not rows for rows in new['bundle_routes'].values()))
        new.pop('bundle_routes');new['schema_version']='0.8.0'
        self.assertEqual(new,old)


if __name__=='__main__':unittest.main()
