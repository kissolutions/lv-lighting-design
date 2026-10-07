import copy
import csv
import io
import json
import tempfile
import unittest
from pathlib import Path
from pypdf import PdfWriter
from pypdf.generic import (DictionaryObject, NameObject, TextStringObject,
                          ArrayObject, FloatObject, DecodedStreamObject)
from generators.model_intake_review import upgrade_v08
from generators.model_intake import check_model
from generators.milestone_markup import schedules, export_schedules, ROOM_REVIEW_NOTE
from generators.export_intake import export_intake
from generators.room_geometry_review import derive_nested_in, smallest_containing_space, room_draw_order
from generators.validate_markup_pdf import inspect_pdf, write_annotation_register

ROOT=Path(__file__).resolve().parents[1]


def polygon(sid,points,level='L1',frame='FRAME-A'):
    return dict(space_id=sid,vertices=points,level=level,frame_id=frame)


def pdf_fixture(missing_label=False, missing_ap=False, bad_room=False):
    writer=PdfWriter();writer.add_blank_page(width=200,height=200)
    def arr(values):return ArrayObject([FloatObject(v) for v in values])
    a=DictionaryObject({NameObject('/Type'):NameObject('/Annot'),NameObject('/Subtype'):NameObject('/Square' if bad_room else '/Polygon'),
        NameObject('/Rect'):arr([10,10,190,190]),NameObject('/Vertices'):arr([10,10,190,10,190,190,10,190]),
        NameObject('/IC'):arr([0.3,0.5,0.9]),NameObject('/CA'):FloatObject(0.2),NameObject('/NM'):TextStringObject('ROOM-NM')})
    writer.add_annotation(0,a)
    if not missing_label:
        label=DictionaryObject({NameObject('/Type'):NameObject('/Annot'),NameObject('/Subtype'):NameObject('/FreeText'),
            NameObject('/Rect'):arr([30,30,100,50]),NameObject('/NM'):TextStringObject('LIGHT-NM'),NameObject('/Contents'):TextStringObject('L001')})
        if not missing_ap:
            stream=DecodedStreamObject();stream.set_data(b'q 0 0 10 10 re S Q')
            stream.update({NameObject('/Type'):NameObject('/XObject'),NameObject('/Subtype'):NameObject('/Form'),NameObject('/BBox'):arr([0,0,70,20])})
            label[NameObject('/AP')]=DictionaryObject({NameObject('/N'):writer._add_object(stream)})
        writer.add_annotation(0,label)
    buffer=io.BytesIO();writer.write(buffer);buffer.seek(0);return buffer


class BetaReviewTests(unittest.TestCase):
    def setUp(self):
        self.old=json.loads((ROOT/'docs/reference-implementations/synthetic-milestones/lighting-model.json').read_text())
        self.model=upgrade_v08(self.old)
        self.register=[dict(annotation_id='ROOM-NM',entity_id='SPACE-1',entity_type='space',role='room_footprint',plan_page_number=1),
                       dict(annotation_id='LIGHT-NM',entity_id='LIGHT-1',entity_type='light',role='light_label',plan_page_number=1)]
    def test_upgrade_preserves_identity_and_existing_engineering(self):
        old=copy.deepcopy(self.old);m=upgrade_v08(old)
        self.assertEqual(old,self.old)
        self.assertTrue(check_model(m,'design')['checks_pass'])
        self.assertEqual(m['light_objects'][0]['source']['source_tag'],None)
        self.assertEqual(m['light_objects'][0]['design'],old['light_objects'][0]['design'])
    def test_plan_tag_does_not_change_schedule_mark_and_provisional_blocks_acceptance(self):
        l=self.model['light_objects'][0];mark=self.model['fixture_types'][0]['source_mark']
        l['source'].update(source_tag='L4A',schedule_match_status='provisional')
        report=check_model(self.model,'intake')
        self.assertFalse(report['checks_pass']);self.assertIsNotNone(report['derived'])
        self.assertEqual(self.model['fixture_types'][0]['source_mark'],mark)
        with tempfile.TemporaryDirectory() as d:
            export_intake(self.model,d,allow_provisional=True)
            with (Path(d)/'light_points.csv').open() as f:rows=list(csv.DictReader(f))
            self.assertEqual(next(x for x in rows if x['light_id']==l['id'])['source_tag'],'L4A')
    def test_section_override_requires_confirmed_decision_and_does_not_add_assembly_light(self):
        l=self.model['light_objects'][0];l.update(count_basis='physical_section',assembly_id='RING-A')
        self.assertIsNone(check_model(self.model)['derived'])
        l['count_decision_id']=next(d['id'] for d in self.model['decisions'] if d['status']=='confirmed')
        self.assertTrue(check_model(self.model)['checks_pass'])
        self.assertEqual(len(schedules(self.model)['light_points_by_type']),len(self.old['light_objects']))
    def test_unknown_suffix_and_nested_cycle_cannot_pass(self):
        self.model['light_objects'][0]['source']['source_tag']='UNEXPLAINED-SUFFIX'
        self.assertFalse(check_model(self.model)['checks_pass'])
        a,b=self.model['spaces'][:2]
        a['level']=b['level']='L1';a['nested_in']=b['id'];b['nested_in']=a['id']
        self.assertIsNone(check_model(self.model)['derived'])
    def test_keynote_mapping_and_nesting_references(self):
        t=self.model['fixture_types'][0];t['schedule_presence']='keynote_only'
        self.assertIsNone(check_model(self.model)['derived'])
        for l in self.model['light_objects']:
            if l['source']['fixture_type_id']==t['id']:l['source']['schedule_match_status']='not_on_schedule'
        self.assertTrue(check_model(self.model)['checks_pass'])
        self.model['spaces'][0]['nested_in']='MISSING'
        self.assertIsNone(check_model(self.model)['derived'])
    def test_real_containment_not_bbox_and_served_frame_is_required(self):
        host=polygon('HOST',[(0,0),(10,0),(10,4),(4,4),(4,10),(0,10)])
        outside=polygon('OUT',[(6,6),(8,6),(8,8),(6,8)])
        inside=polygon('IN',[(1,1),(2,1),(2,2),(1,2)])
        other=polygon('UPPER',[(1,1),(2,1),(2,2),(1,2)],level='L2')
        fs=[host,outside,inside,other];before=copy.deepcopy(fs)
        self.assertEqual(derive_nested_in(fs),dict(HOST=None,OUT=None,IN='HOST',UPPER=None))
        self.assertEqual(smallest_containing_space((1.5,1.5),list(reversed(fs)),'L1','FRAME-A'),'IN')
        self.assertEqual(fs,before);self.assertEqual(room_draw_order(fs)[0]['space_id'],'HOST')
    def test_zero_width_slit_rejected_and_missing_space_does_not_force_assignment(self):
        slit=polygon('S',[(0,0),(10,0),(10,10),(0,10),(0,5),(3,5),(3,3),(5,3),(5,7),(3,7),(3,5),(0,5)])
        with self.assertRaises(ValueError):derive_nested_in([slit])
        with self.assertRaises(ValueError):smallest_containing_space((99,99),[polygon('A',[(0,0),(2,0),(2,2),(0,2)])],'L1','FRAME-A')
    def test_required_notes_and_room_columns_in_both_packages(self):
        with tempfile.TemporaryDirectory() as d:
            export_schedules(self.model,None,d,2)
            for path in ['01_room_boundaries.html','02_lighting_takeoff.html']:
                self.assertIn(ROOM_REVIEW_NOTE,(Path(d)/path).read_text())
            rooms=(Path(d)/'rooms.csv').read_text()
            self.assertIn('Area sf (check only)',rooms);self.assertIn('Nested in',rooms)
    def test_valid_annotations_then_missing_or_flattened_content_fails(self):
        self.assertTrue(inspect_pdf(pdf_fixture(),self.register,[1])['checks_pass'])
        self.assertFalse(inspect_pdf(pdf_fixture(missing_label=True),self.register,[1])['checks_pass'])
        w=PdfWriter();w.add_blank_page(width=200,height=200);b=io.BytesIO();w.write(b);b.seek(0)
        report=inspect_pdf(b,self.register,[1]);self.assertTrue(any('zero live' in x for x in report['issues']))
    def test_free_text_appearance_polygon_type_and_page_register_required(self):
        self.assertFalse(inspect_pdf(pdf_fixture(missing_ap=True),self.register,[1])['checks_pass'])
        self.assertFalse(inspect_pdf(pdf_fixture(bad_room=True),self.register,[1])['checks_pass'])
        self.register[1]['plan_page_number']=2
        self.assertFalse(inspect_pdf(pdf_fixture(),self.register,[1])['checks_pass'])
    def test_annotation_register_preserves_source_identity(self):
        l=self.model['light_objects'][0];l['source']['source_tag']='L4A';l['assembly_id']='RING-A'
        row=dict(annotation_id='LABEL',entity_id=l['id'],entity_type='light',role='light_label',plan_page_number=1)
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'register.csv';write_annotation_register(p,[row],self.model)
            with p.open() as f:r=next(csv.DictReader(f))
            self.assertEqual(r['source_tag'],'L4A');self.assertEqual(r['assembly_id'],'RING-A')


if __name__=='__main__':unittest.main()
