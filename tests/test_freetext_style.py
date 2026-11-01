"""Synthetic form-H failure, migration and document-preservation cases."""
import copy
import hashlib
import io
import tempfile
import unittest
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from pypdf.generic import (ArrayObject, DictionaryObject, FloatObject, NameObject,
                          NumberObject, TextStringObject, ContentStream)
from generators.freetext_style import (apply_style, color_bytes, da_string,
    ds_string, ds_from_da, label_rect, line_width, parse_da, style_issues)
from generators.validate_markup_pdf import inspect_pdf
from tools.normalize_freetext_ap import normalize


def arr(values):
    return ArrayObject([FloatObject(v) for v in values])


def label(writer, text='L101', aid='LABEL-1', rgb=(.1, .25, .7)):
    a = DictionaryObject({NameObject('/Type'): NameObject('/Annot'),
        NameObject('/Subtype'): NameObject('/FreeText'),
        NameObject('/Rect'): arr([100, 200, 200, 230]),
        NameObject('/NM'): TextStringObject(aid),
        NameObject('/Contents'): TextStringObject(text),
        NameObject('/Subj'): TextStringObject('L101 A2'),
        NameObject('/F'): NumberObject(4)})
    return apply_style(writer, a, rgb=rgb)


def saved(writer):
    stream = io.BytesIO()
    writer.write(stream)
    stream.seek(0)
    return stream


class FreeTextStyleTests(unittest.TestCase):
    def setUp(self):
        self.writer = PdfWriter()
        self.writer.add_blank_page(width=400, height=800)
        self.a = label(self.writer)

    def test_generated_form_survives_saved_object_readback(self):
        self.writer.add_annotation(0, self.a)
        reopened = PdfReader(saved(self.writer)).pages[0]['/Annots'][0].get_object()
        self.assertEqual(style_issues(reopened), [])
        self.assertEqual([float(x) for x in reopened['/Rect']][::3], [100, 230])
        self.assertNotIn('/RD', reopened)
        self.assertNotIn('/RC', reopened)
        self.assertNotIn('/Matrix', reopened['/AP']['/N'])

    def test_color_encoding_is_stable_for_every_byte_including_endpoints(self):
        for k in range(256):
            with self.subTest(byte=k):
                parsed = parse_da(da_string((k/255,)*3))
                self.assertEqual(color_bytes(parsed['rgb']), (k,)*3)
                self.assertTrue(all(int(v*255) == k for v in parsed['rgb']))
                self.assertTrue(all(0 <= v <= 1 for v in parsed['rgb']))

    def test_gray_da_and_explicit_font_are_parsed(self):
        self.assertEqual(parse_da('/Helv 4 Tf 0.2 g')['rgb'], (.2,)*3)
        self.assertIn('font: Helvetica 4pt', ds_from_da('/Helv 4 Tf 0.2 g'))
        for bad in ('', '/Helv 4 Tf', '0 0 0 rg', '/Helv 0 Tf 0 g', '/Helv 4 Tf 0 0 0 1 k'):
            with self.subTest(da=bad), self.assertRaises(ValueError):
                parse_da(bad)

    def test_bad_style_keys_are_rejected(self):
        good = str(self.a['/DS'])
        variants = [None, good.replace('Helvetica 4pt', '4pt Helvetica'),
            good.replace('Helvetica 4pt', 'Helvetica 11pt'),
            good.replace('#1A40B3', '#000000'), good.replace('margin:1pt', 'margin:0pt'),
            good.replace('margin:1pt;', ''), good.replace('line-height:4.6pt', 'line-height:6.46pt'),
            good + ';margin:0pt']
        for ds in variants:
            with self.subTest(style=ds):
                a = copy.deepcopy(self.a)
                if ds is None:
                    a.pop(NameObject('/DS'))
                else:
                    a[NameObject('/DS')] = TextStringObject(ds)
                self.assertTrue(style_issues(a))

    def test_rd_and_rich_text_fail_generated_profile(self):
        for key, value in [('/RD', arr([1,1,1,1])), ('/RC', TextStringObject('<body>text</body>'))]:
            with self.subTest(key=key):
                a = copy.deepcopy(self.a)
                a[NameObject(key)] = value
                self.assertTrue(any(key in i for i in style_issues(a)))

    def test_multiline_layout_has_room_for_bluebeam_relayout(self):
        a = label(self.writer, 'RESTROOM\nSP-001\nEnergy type: restroom')
        self.assertEqual(style_issues(a), [])
        r = [float(v) for v in a['/Rect']]
        self.assertAlmostEqual(r[3]-r[1], 17.2)
        a[NameObject('/Rect')] = arr([r[0],r[1],r[0]+8,r[3]])
        self.assertTrue(any('wrap' in x for x in style_issues(a)))

    def test_short_height_is_a_failure_even_when_width_fits(self):
        a = label(self.writer, 'ROOM\nSP-001\nOffice')
        r = list(a['/Rect'])
        r[1] = float(r[3])-8
        a[NameObject('/Rect')] = arr(r)
        self.assertTrue(any('height' in x for x in style_issues(a)))

    def test_foxit_local_bbox_is_flagged_as_workflow_incompatible(self):
        normal = self.a['/AP']['/N'].get_object()
        normal[NameObject('/BBox')] = arr([0,-8,20,0])
        self.assertTrue(any('/BBox' in x for x in style_issues(self.a)))
        normal[NameObject('/BBox')] = arr(self.a['/Rect'])
        normal[NameObject('/Matrix')] = arr([1,0,0,1,50,100])
        self.assertTrue(any('/Matrix' in x for x in style_issues(self.a)))
        normal[NameObject('/Matrix')] = arr([1,0,0,1,0,0])
        self.assertEqual(style_issues(self.a), [])

    def test_appearance_font_and_color_must_agree(self):
        for old,new in [(b'/Helv 4 Tf',b'/Helv 11 Tf'),
                        (b'0.1029411765 0.2519607843 0.7029411765 rg',b'0 0 0 rg')]:
            with self.subTest(replacement=new):
                a = label(self.writer)
                normal = a['/AP']['/N'].get_object()
                data = normal.get_data()
                self.assertIn(old,data)
                normal.set_data(data.replace(old,new))
                self.assertTrue(any('appearance text size/color' in x for x in style_issues(a)))

    def test_simple_pdf_text_literals_are_escaped_and_retained(self):
        text = 'ROOM (A) \\ west – café'
        a = label(self.writer,text)
        self.writer.add_annotation(0,a)
        reopened = PdfReader(saved(self.writer)).pages[0]['/Annots'][0].get_object()
        self.assertEqual(str(reopened['/Contents']),text)
        self.assertEqual(style_issues(reopened),[])
        self.assertIn(b'\\050',reopened['/AP']['/N'].get_data())

    def test_unknown_font_or_glyph_refused_before_mutation(self):
        before = copy.deepcopy(self.a)
        with self.assertRaises(ValueError):
            apply_style(self.writer,self.a,rgb=(0,0,0),family='Missing-Font')
        self.assertEqual(self.a,before)
        with self.assertRaises(UnicodeEncodeError):
            line_width('房间')

    def test_core_font_metrics_are_family_specific(self):
        self.assertGreater(line_width('WWW'),line_width('iii'))
        self.assertEqual(line_width('WWW',family='Courier'),line_width('iii',family='Courier'))
        a = label(self.writer,'TEMP')
        apply_style(self.writer,a,rgb=(0,0,0),family='Times-Roman')
        self.assertEqual(style_issues(a),[])

    def test_plan_checker_enforces_profile_and_ignores_other_pages(self):
        self.writer.add_annotation(0,self.a)
        self.writer.add_blank_page(width=400,height=800)
        other = label(self.writer,'REFERENCE','REF-TEXT')
        other.pop(NameObject('/DS'))
        self.writer.add_annotation(1,other)
        records=[dict(annotation_id='LABEL-1',entity_id='L101',entity_type='light',role='light_label',plan_page_number=1)]
        self.assertTrue(inspect_pdf(saved(self.writer),records,[1])['checks_pass'])
        self.a[NameObject('/DS')] = TextStringObject('font: Helvetica 4pt; color:#000000')
        # add_annotation copies the dictionary; mutate the page's actual object.
        actual=self.writer.pages[0]['/Annots'][0].get_object()
        actual[NameObject('/DS')] = self.a['/DS']
        self.assertFalse(inspect_pdf(saved(self.writer),records,[1])['checks_pass'])


class NormalizerTests(unittest.TestCase):
    def make_pdf(self,path,*,size=4,locked=False,unicode=False):
        w=PdfWriter();w.add_blank_page(width=400,height=800);w.add_blank_page(width=400,height=800)
        w.add_metadata({'/Title':'Synthetic live-markup normalization'})
        w.add_outline_item('Plan 1',0)
        ocg=DictionaryObject({NameObject('/Type'):NameObject('/OCG'),NameObject('/Name'):TextStringObject('Labels')})
        oc=w._add_object(ocg)
        w.root_object[NameObject('/OCProperties')]=DictionaryObject({NameObject('/OCGs'):ArrayObject([oc]),NameObject('/D'):DictionaryObject({NameObject('/ON'):ArrayObject([oc])})})
        a=label(w,'OFFICE\nSP-001\nOffice')
        a[NameObject('/OC')]=oc
        a[NameObject('/DA')]=TextStringObject(f'/Helv {size} Tf 0.1 0.25 0.7 rg')
        a[NameObject('/DS')]=TextStringObject('font: Helvetica 4pt; color:#000000')
        a[NameObject('/RD')]=arr([1,1,1,1])
        a[NameObject('/RC')]=TextStringObject('<body>viewer generated rich text</body>')
        a['/AP']['/N'][NameObject('/BBox')]=arr([0,-30,100,0])
        a['/AP']['/N'][NameObject('/Matrix')]=arr([1,0,0,1,0,0])
        if locked:a[NameObject('/F')]=NumberObject(4|128)
        if unicode:a[NameObject('/Contents')]=TextStringObject('房间')
        w.add_annotation(0,a)
        shape=DictionaryObject({NameObject('/Subtype'):NameObject('/Square'),NameObject('/Rect'):arr([5,5,20,20]),NameObject('/NM'):TextStringObject('FIXTURE-ANCHOR'),NameObject('/Contents'):TextStringObject('L101 A2')})
        w.add_annotation(0,shape)
        with path.open('wb') as f:w.write(f)

    def test_normalize_keeps_source_ids_layers_outline_top_left_and_nontext(self):
        with tempfile.TemporaryDirectory() as d:
            src,out,out2=[Path(d)/n for n in ('source.pdf','r2.pdf','r3.pdf')]
            self.make_pdf(src)
            digest=hashlib.sha256(src.read_bytes()).digest()
            before=PdfReader(src)
            a=before.pages[0]['/Annots'][0].get_object()
            report=normalize(src,out,[1])
            self.assertTrue(report['checks_pass']);self.assertEqual(report['normalized'],1)
            after=PdfReader(out);b=after.pages[0]['/Annots'][0].get_object()
            self.assertEqual(style_issues(b),[])
            for k in ('/NM','/Contents','/Subj','/F'):
                self.assertEqual(a[k],b[k])
            self.assertEqual(a['/OC'].get_object(),b['/OC'].get_object())
            self.assertEqual([float(a['/Rect'][i]) for i in [0,3]],[float(b['/Rect'][i]) for i in [0,3]])
            for k in ('/Subtype','/Rect','/NM','/Contents'):
                self.assertEqual(before.pages[0]['/Annots'][1].get_object()[k],after.pages[0]['/Annots'][1].get_object()[k])
            self.assertEqual(len(after.pages),2)
            self.assertEqual(after.metadata.title,before.metadata.title)
            self.assertEqual(after.outline[0].title,before.outline[0].title)
            self.assertEqual(hashlib.sha256(src.read_bytes()).digest(),digest)
            normalize(out,out2,[1])
            b2=PdfReader(out2).pages[0]['/Annots'][0].get_object()
            for k in ('/Rect','/DA','/DS','/Contents'):
                self.assertEqual(b[k],b2[k])

    def test_small_font_drift_snaps_to_four_without_moving_top_left(self):
        for size in (3.9,4.1):
            with self.subTest(size=size),tempfile.TemporaryDirectory() as d:
                src,out=Path(d)/'source.pdf',Path(d)/'new.pdf'
                self.make_pdf(src,size=size)
                self.assertTrue(normalize(src,out)['checks_pass'])
                a=PdfReader(out).pages[0]['/Annots'][0].get_object()
                self.assertEqual(parse_da(a['/DA'])['size'],4)
                self.assertEqual([float(a['/Rect'][i]) for i in (0,3)],[100,230])

    def test_rejects_input_overwrite_and_existing_revision(self):
        with tempfile.TemporaryDirectory() as d:
            src=Path(d)/'source.pdf';self.make_pdf(src)
            with self.assertRaises(ValueError):normalize(src,src)
            out=Path(d)/'existing.pdf';out.write_bytes(b'protected')
            with self.assertRaises(ValueError):normalize(src,out)
            self.assertEqual(out.read_bytes(),b'protected')

    def test_unknown_da_unsupported_glyph_locked_and_wrong_size_are_reported(self):
        for options in [dict(size=11),dict(locked=True),dict(unicode=True)]:
            with self.subTest(options=options), tempfile.TemporaryDirectory() as d:
                src=Path(d)/'source.pdf';out=Path(d)/'out.pdf';self.make_pdf(src,**options)
                report=normalize(src,out)
                self.assertFalse(report['checks_pass'])
                self.assertEqual(report['normalized'],0)
                self.assertEqual(len(report['skipped']),1)

    def test_refuses_unparseable_da_and_callout(self):
        for key,value in [('/DA',TextStringObject('/Helv 4 Tf')),('/IT',NameObject('/FreeTextCallout'))]:
            with self.subTest(key=key),tempfile.TemporaryDirectory() as d:
                src=Path(d)/'source.pdf';self.make_pdf(src)
                w=PdfWriter();w.clone_document_from_reader(PdfReader(src))
                w.pages[0]['/Annots'][0].get_object()[NameObject(key)]=value
                with src.open('wb') as f:w.write(f)
                report=normalize(src,Path(d)/'out.pdf')
                self.assertEqual(report['normalized'],0)
                self.assertFalse(report['checks_pass'])


if __name__=='__main__':
    unittest.main()
