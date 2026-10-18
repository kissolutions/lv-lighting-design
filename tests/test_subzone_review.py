"""Subzone M3 round-trip, detection confidence, daylight reopening and PDF markups."""
import copy
import csv
import json
import tempfile
import unittest
from pathlib import Path
from pypdf import PdfWriter,PdfReader
from pypdf.generic import DictionaryObject,NameObject,TextStringObject,ArrayObject,FloatObject
from generators.subzone_review import (validate,export,import_review,label_manifest,
    proposed_zone_tree,sequence_reverification_impact,discussion_findings)
from generators.subzone_pdf import render


def case():
    model={'project':{'id':'TEST','model_revision':'M2-R1','name':'Example'},
      'spaces':[{'id':'S201','name':'Conference Room','room_number':'201',
                 'light_object_ids':['L101','L102','L103'],'light_zone_ids':[]},
                {'id':'S202','name':'Closet','room_number':'202',
                 'light_object_ids':['L201'],'light_zone_ids':[]}],
      'source_references':[{'id':'REF1'}],
      'decisions':[{'id':'DEC1','status':'confirmed'}],
      'light_objects':[dict(id=lid,label=lid,source=dict(
          fixture_type_id='TYPE1',drawing_page_id='PG1',drawing_anchor=dict(x_pt=100+i*100,y_pt=200),
          source_annotation_id='ORIG-'+lid)) for i,lid in enumerate(['L101','L102','L103','L201'])]}
    findings=[dict(id='F1',space_id='S201',flag='SZ-04',confidence='HIGH',status='confirmed',
        evidence='Two separate lettered switch groups a/b',source_ref_ids=['REF1']),
      dict(id='F2',space_id='S201',flag='SZ-03',confidence='MEDIUM',status='dismissed',
        evidence='Two circuits share one switching group',source_ref_ids=['REF1'])]
    register=dict(schema_version='0.1.0',project_id='TEST',model_revision='M2-R1',review_revision='R1',
      detection_findings=findings,
      spaces=[dict(space_id='S201',detection_disposition='subzone_extraction_required',
         code_screen='resolved_no_split',daylight_screen='resolved_no_split',
         source_control_intent_status='complete',subzone_required=True,notes='Two dimmers'),
       dict(space_id='S202',detection_disposition='single_zone_candidate',
         code_screen='resolved_no_split',daylight_screen='resolved_no_split',
         source_control_intent_status='complete',subzone_required=False,notes='Single control')],
      daylight_areas=[],
      assignments=[dict(space_id='S201',light_id=lid,subzone_label=lab,zone_id='SZ-S201-'+lab,
            basis='mep',confidence='HIGH',source_group=lab,evidence='Switch '+lab,owner_comment='')
        for lid,lab in [('L101','a'),('L102','a'),('L103','b')]],
      acceptance=dict(status='draft',decision_id=None,accepted_revision=None))
    return model,register


class SubzoneTests(unittest.TestCase):
    def accepted(self):
        model,r=case()
        r['acceptance']=dict(status='accepted',decision_id='DEC1',accepted_revision='R1')
        return model,r
    def test_valid_draft_and_acceptance(self):
        m,r=self.accepted()
        self.assertEqual(validate(m,r),[])
        self.assertEqual(validate(m,r,accept=True),[])
        tree=proposed_zone_tree(m,r)
        self.assertEqual(tree[0]['parent_zone_id'],'SZP-S201')
        self.assertEqual(len(tree[0]['leaves']),2)
    def test_unzoned_blocks_acceptance(self):
        m,r=self.accepted()
        r['assignments'][0].update(zone_id=None,subzone_label=None,basis='unresolved')
        self.assertEqual(validate(m,r),[])
        self.assertTrue(any('Unzoned' in f['message'] for f in validate(m,r,accept=True)))
    def test_low_confidence_owner_report(self):
        m,r=case();r['detection_findings'][1]['status']='probable'
        self.assertEqual(len(discussion_findings(r)),1)
        r['acceptance']=dict(status='accepted',decision_id='DEC1',accepted_revision='R1')
        self.assertTrue(any('low-confidence' in f['message'] for f in validate(m,r,accept=True)))
    def test_no_unnecessary_single_room(self):
        m,r=case()
        self.assertEqual(len(r['assignments']),3)
        self.assertEqual(validate(m,r),[])
        r['assignments'].append(dict(r['assignments'][0],space_id='S202',light_id='L201'))
        self.assertTrue(any('fast-path' in f['message'] for f in validate(m,r)))
    def test_late_daylight_reprocessing(self):
        m,r=self.accepted()
        updated=copy.deepcopy(r)
        updated['daylight_areas']=[dict(daylight_id='DL-01',space_ids=['S201'],
          light_ids=['L101'],extent_basis='owner_asserted',extent_note='Owner added window',
          source_ref_ids=['REF1'])]
        self.assertEqual(sequence_reverification_impact(r,updated),['S201'])
    def test_csv_round_trip_preserves_ids_and_regenerates_labels(self):
        m,r=case()
        with tempfile.TemporaryDirectory() as d:
            export(m,r,Path(d)/'review')
            csvpath=Path(d)/'review/subzone_owner_review.csv'
            with csvpath.open(newline='') as f:rows=list(csv.DictReader(f))
            target=next(x for x in rows if x['light_id']=='L103')
            target['subzone_label']='a';target['zone_id']='SZ-S201-a';target['owner_comment']='Move by owner'
            with csvpath.open('w',newline='') as f:
                w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
            nxt=import_review(m,r,csvpath)
            self.assertEqual(nxt['assignments'][2]['subzone_label'],'a')
            self.assertEqual(nxt['assignments'][2]['basis'],'owner')
            self.assertEqual(nxt['acceptance']['status'],'draft')
            self.assertEqual(sequence_reverification_impact(r,nxt),['S201'])
            self.assertEqual(label_manifest(m,nxt)[2]['display_label'],'a')
    def test_csv_missing_id_is_blocked(self):
        m,r=case()
        with tempfile.TemporaryDirectory() as d:
            export(m,r,Path(d)/'review')
            csvpath=Path(d)/'review/subzone_owner_review.csv'
            with csvpath.open(newline='') as f:rows=list(csv.DictReader(f))
            with csvpath.open('w',newline='') as f:
                w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows[1:])
            with self.assertRaises(ValueError):import_review(m,r,csvpath)
    def test_pdf_adds_editable_labels_and_upserts_original_comment(self):
        m,r=case()
        with tempfile.TemporaryDirectory() as d:
            input_pdf=Path(d)/'original.pdf';output_pdf=Path(d)/'subzones.pdf'
            w=PdfWriter();w.add_blank_page(width=612,height=792)
            for lid in ('L101','L102','L103'):
                a=DictionaryObject({
                    NameObject('/Type'):NameObject('/Annot'),
                    NameObject('/Subtype'):NameObject('/Text'),
                    NameObject('/Rect'):ArrayObject([FloatObject(90),FloatObject(180),FloatObject(100),FloatObject(190)]),
                    NameObject('/NM'):TextStringObject('ORIG-'+lid),
                    NameObject('/Contents'):TextStringObject('Original verified comment')})
                w.add_annotation(page_number=0,annotation=a)
            with input_pdf.open('wb') as f:w.write(f)
            result=render(input_pdf,output_pdf,label_manifest(m,r),{'PG1':0})
            self.assertEqual(result['created'],3)
            self.assertEqual(len(result['comments_updated']),3)
            reader=PdfReader(str(output_pdf))
            anns=[x.get_object() for x in reader.pages[0]['/Annots']]
            self.assertEqual(len(anns),6)
            self.assertTrue(any(str(x.get('/NM'))=='SZLABEL-L101' for x in anns))
            orig=next(x for x in anns if str(x.get('/NM'))=='ORIG-L101')
            self.assertIn('Original verified comment',str(orig.get('/Contents')))
            self.assertIn('Subzone: a',str(orig.get('/Contents')))

if __name__=='__main__':unittest.main()
