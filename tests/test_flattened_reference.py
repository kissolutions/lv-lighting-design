"""Synthetic saved-PDF boundaries for FRL; no native-viewer certification."""
import io
import shutil
import subprocess
import tempfile
import unittest
import importlib.util
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from pypdf.generic import (
    ArrayObject, DecodedStreamObject, DictionaryObject, FloatObject,
    IndirectObject, NameObject, NullObject, TextStringObject,
)

from generators.flattened_reference import (
    add_flattened_layer, declare_page_ocgs, content_references,
    reference_structure_issues,
)
from generators.validate_markup_pdf import inspect_pdf


LAYER = 'Light Points (Abridged, flattened reference M2-R3)'


def array(values):
    return ArrayObject([FloatObject(v) for v in values])


def group(writer, name):
    return writer._add_object(DictionaryObject({
        NameObject('/Type'): NameObject('/OCG'),
        NameObject('/Name'): TextStringObject(name),
    }))


def stream(writer, data):
    obj = DecodedStreamObject(); obj.set_data(data)
    return writer._add_object(obj)


def saved(writer):
    out = io.BytesIO(); writer.write(out); out.seek(0)
    return out


def fixture(pages=1):
    writer = PdfWriter(); records = []
    background = group(writer, 'CAD background')
    reference = group(writer, LAYER)
    for number in range(1, pages + 1):
        page = writer.add_blank_page(width=200, height=200)
        page[NameObject('/Resources')] = DictionaryObject({
            NameObject('/Properties'): DictionaryObject({NameObject('/CAD'): background})})
        page[NameObject('/Contents')] = stream(writer, b'q /OC /CAD BDC 0 .6 0 rg 10 10 40 40 re f EMC Q\n')
        writer.add_annotation(number - 1, DictionaryObject({
            NameObject('/Subtype'): NameObject('/Square'),
            NameObject('/Rect'): array([90, 90, 100, 100]),
            NameObject('/NM'): TextStringObject(f'ACTIVE-{number}'),
        }))
        records.append(dict(annotation_id=f'ACTIVE-{number}', entity_id=f'CHANNEL-{number}',
                            entity_type='channel', role='other', plan_page_number=number))
    return writer, background, reference, records


def add_reference(writer, ref, number=1, name='Reference'):
    return add_flattened_layer(writer, writer.pages[number - 1], ref,
                               b'q 0 0 1 rg 130 130 40 40 re f Q\n', name)


class FlattenedReferenceTests(unittest.TestCase):
    def test_saved_form_indirect_content_and_background_registration(self):
        w, bg, ref, rows = fixture(); page = w.pages[0]
        original = page.raw_get('/Contents'); original_data = original.get_object().get_data()
        form = add_reference(w, ref)
        declare_page_ocgs(w, [page], [ref])
        self.assertIn(original, content_references(page))
        self.assertEqual(original.get_object().get_data(), original_data)
        self.assertEqual(form.get_object()['/OC'], ref.get_object())
        self.assertEqual(list(form.get_object()['/BBox']), [0, 0, 200, 200])
        self.assertIn('/Resources', form.get_object())
        self.assertNotIn('/Matrix', form.get_object())
        pdf = saved(w); reader = PdfReader(pdf)
        self.assertTrue(all(isinstance(x, IndirectObject) for x in content_references(reader.pages[0])))
        self.assertEqual(reference_structure_issues(reader, [1], [LAYER]), [])
        report = inspect_pdf(pdf, rows, [1], [LAYER])
        self.assertTrue(report['checks_pass'], report['issues'])
        self.assertEqual(report['annotations_per_plan_page'], {1: 1})
        props = reader.trailer['/Root']['/OCProperties']
        self.assertEqual(len(props['/OCGs']), 2)
        self.assertEqual(len(props['/D']['/ON']), 2)
        self.assertEqual([x.get_object()['/Name'] for x in props['/D']['/Order']], [LAYER])

    def test_direct_stream_null_and_nonstream_contents_rejected(self):
        for bad in (DecodedStreamObject(), NullObject(), DictionaryObject()):
            with self.subTest(kind=type(bad).__name__):
                w, bg, ref, rows = fixture(); page = w.pages[0]
                page[NameObject('/Contents')] = ArrayObject([bad])
                with self.assertRaises(ValueError):
                    add_reference(w, ref)
                self.assertTrue(any('/Contents' in s for s in reference_structure_issues(PdfReader(saved(w)), [1])))
        w, bg, ref, rows = fixture()
        w.pages[0][NameObject('/Contents')] = w._add_object(NullObject())
        self.assertTrue(any('/Contents' in s for s in reference_structure_issues(PdfReader(saved(w)), [1])))

    def test_undeclared_background_is_caught_even_if_reference_declared(self):
        w, bg, ref, rows = fixture(); add_reference(w, ref)
        w.root_object[NameObject('/OCProperties')] = DictionaryObject({
            NameObject('/OCGs'): ArrayObject([ref]), NameObject('/D'): DictionaryObject()})
        report = inspect_pdf(saved(w), rows, [1], [LAYER])
        self.assertTrue(any('referenced OCG missing' in s for s in report['issues']), report)

    def test_declared_but_uninvoked_or_empty_form_does_not_count(self):
        for kind in ('uninvoked', 'empty', 'no_paint'):
            with self.subTest(kind=kind):
                w, bg, ref, rows = fixture(); form = add_reference(w, ref)
                if kind == 'uninvoked':
                    w.pages[0]['/Contents'].pop()
                else:
                    form.get_object().set_data(b'' if kind == 'empty' else b'q Q\n')
                declare_page_ocgs(w, [1], [ref])
                report = inspect_pdf(saved(w), rows, [1], [LAYER])
                self.assertTrue(any('no invoked non-empty' in s for s in report['issues']), report)

    def test_default_off_unknown_or_ambiguous_named_layer_fails(self):
        w, bg, ref, rows = fixture(); add_reference(w, ref); declare_page_ocgs(w, [1], [ref])
        default = w.root_object['/OCProperties']['/D']
        default[NameObject('/OFF')] = ArrayObject([ref])
        self.assertTrue(any('default ON' in s for s in reference_structure_issues(PdfReader(saved(w)), [1], [LAYER])))
        self.assertTrue(any('declared exactly once' in s for s in reference_structure_issues(PdfReader(saved(w)), [1], ['MISSING'])))
        w.root_object['/OCProperties']['/OCGs'].append(group(w, LAYER))
        self.assertTrue(any('declared exactly once' in s for s in reference_structure_issues(PdfReader(saved(w)), [1], [LAYER])))

    def test_inherited_nested_membership_resources_are_declared(self):
        w, bg, ref, rows = fixture(); page = w.pages[0]
        second = group(w, 'Nested background')
        membership = w._add_object(DictionaryObject({NameObject('/Type'): NameObject('/OCMD'),
                                                     NameObject('/OCGs'): ArrayObject([bg, second])}))
        child = DecodedStreamObject(); child.set_data(b'/OC /CAD BDC 1 1 10 10 re f EMC')
        child.update({NameObject('/Type'): NameObject('/XObject'), NameObject('/Subtype'): NameObject('/Form'),
                      NameObject('/BBox'): array([0, 0, 200, 200]),
                      NameObject('/Resources'): DictionaryObject({NameObject('/Properties'): DictionaryObject({NameObject('/CAD'): membership})})})
        inherited = DictionaryObject({NameObject('/XObject'): DictionaryObject({NameObject('/Nested'): w._add_object(child)})})
        page['/Parent'][NameObject('/Resources')] = inherited
        del page['/Resources']
        page[NameObject('/Contents')] = stream(w, b'/Nested Do')
        add_reference(w, ref); declare_page_ocgs(w, [1], [ref])
        reader = PdfReader(saved(w))
        self.assertEqual(len(reader.trailer['/Root']['/OCProperties']['/OCGs']), 3)
        self.assertEqual(reference_structure_issues(reader, [1], [LAYER]), [])

    def test_registration_preserves_unrelated_visibility_order_and_configs(self):
        w, bg, ref, rows = fixture(); unrelated = group(w, 'Unrelated hidden group')
        w.root_object[NameObject('/OCProperties')] = DictionaryObject({
            NameObject('/OCGs'): ArrayObject([unrelated]),
            NameObject('/Configs'): ArrayObject([DictionaryObject({NameObject('/Name'): TextStringObject('Retained')})]),
            NameObject('/D'): DictionaryObject({NameObject('/BaseState'): NameObject('/OFF'),
                NameObject('/OFF'): ArrayObject([unrelated, bg]),
                NameObject('/Order'): ArrayObject([unrelated])})})
        add_reference(w, ref); declare_page_ocgs(w, [1], [ref]); declare_page_ocgs(w, [1], [ref])
        props = w.root_object['/OCProperties']; default = props['/D']
        self.assertEqual(len(props['/OCGs']), 3)
        self.assertEqual(default['/OFF'], [unrelated])
        self.assertEqual(default['/Order'], [unrelated, ref])
        self.assertEqual(props['/Configs'][0]['/Name'], 'Retained')
        self.assertEqual(reference_structure_issues(PdfReader(saved(w)), [1], [LAYER]), [])

    def test_unique_names_preserve_existing_xobjects_and_nonzero_media_box(self):
        w, bg, ref, rows = fixture(); page = w.pages[0]
        page[NameObject('/MediaBox')] = array([10, 20, 210, 220])
        first = add_reference(w, ref, name='Reference')
        second = add_reference(w, ref, name='Reference')
        xobjects = page['/Resources']['/XObject']
        self.assertEqual(xobjects['/Reference'], first.get_object())
        self.assertEqual(xobjects['/Reference_1'], second.get_object())
        self.assertEqual(list(second.get_object()['/BBox']), [10, 20, 210, 220])

    def test_shared_resources_do_not_leak_reference_into_another_page(self):
        w, bg, ref, rows = fixture(pages=2)
        shared = w._add_object(w.pages[0]['/Resources'])
        for page in w.pages:
            page[NameObject('/Resources')] = shared
        add_reference(w, ref)
        self.assertNotIn('/XObject', w.pages[1]['/Resources'])
        declare_page_ocgs(w, [1, 2], [ref])
        reader = PdfReader(saved(w))
        self.assertEqual(reference_structure_issues(reader, [1, 2], {LAYER: [1]}), [])

    def test_indirect_contents_array_keeps_each_original_stream_reference(self):
        w, bg, ref, rows = fixture(); page = w.pages[0]
        originals = content_references(page) + [stream(w, b'q Q')]
        page[NameObject('/Contents')] = w._add_object(ArrayObject(originals))
        add_reference(w, ref)
        self.assertEqual(content_references(page)[1:3], originals)
        self.assertEqual(len(content_references(page)), 4)

    @unittest.skipUnless(importlib.util.find_spec('fitz'), 'optional MuPDF renderer not installed')
    def test_existing_cad_transform_does_not_move_reference_and_toggle_keeps_background(self):
        import fitz
        w, bg, ref, rows = fixture(); page = w.pages[0]
        page['/Contents'].set_data(b'2 0 0 2 0 0 cm /OC /CAD BDC 0 .6 0 rg 10 10 20 20 re f EMC')
        add_reference(w, ref); declare_page_ocgs(w, [1], [ref])
        for enabled in (True, False):
            default = w.root_object['/OCProperties']['/D']
            default[NameObject('/ON')] = ArrayObject([bg, ref] if enabled else [bg])
            default[NameObject('/OFF')] = ArrayObject([] if enabled else [ref])
            with fitz.open(stream=saved(w).getvalue(), filetype='pdf') as rendered:
                pixels = rendered[0].get_pixmap(alpha=False)
                self.assertEqual(pixels.pixel(30, 170), (0, 153, 0))
                self.assertEqual(pixels.pixel(150, 50), (0, 0, 255) if enabled else (255, 255, 255))

    def test_inline_membership_visibility_expression_discovers_groups(self):
        w, bg, ref, rows = fixture(); extra = group(w, 'Expression background')
        membership = DictionaryObject({NameObject('/Type'): NameObject('/OCMD'),
            NameObject('/VE'): ArrayObject([NameObject('/Or'), bg, extra])})
        w.pages[0]['/Resources']['/Properties'][NameObject('/Membership')] = membership
        add_reference(w, ref); declare_page_ocgs(w, [1], [ref])
        self.assertEqual(len(w.root_object['/OCProperties']['/OCGs']), 3)
        self.assertEqual(reference_structure_issues(PdfReader(saved(w)), [1], [LAYER]), [])

    def test_per_page_expectation_and_bdc_structural_support(self):
        w, bg, ref, rows = fixture(pages=2)
        page = w.pages[0]
        page['/Resources']['/Properties'][NameObject('/LP')] = ref
        page[NameObject('/Contents')] = ArrayObject(content_references(page) + [stream(w, b'/OC /LP BDC 20 20 5 5 re f EMC')])
        declare_page_ocgs(w, [1, 2], [ref])
        reader = PdfReader(saved(w))
        self.assertEqual(reference_structure_issues(reader, [1, 2], {LAYER: [1]}), [])
        self.assertTrue(any('Plan page 2' in s for s in reference_structure_issues(reader, [1, 2], [LAYER])))
        self.assertTrue(any('expected pages' in s for s in reference_structure_issues(reader, [1], {LAYER: [2]})))

    def test_helper_rejects_empty_content_or_foreign_writer_without_modifying_page(self):
        w, bg, ref, rows = fixture(); original = list(content_references(w.pages[0]))
        with self.assertRaises(ValueError):
            add_flattened_layer(w, w.pages[0], ref, b'', 'Ref')
        other = PdfWriter(); other.add_blank_page(width=200, height=200)
        with self.assertRaises(ValueError):
            add_flattened_layer(other, w.pages[0], ref, b'0 0 10 10 re f', 'Ref')
        self.assertEqual(content_references(w.pages[0]), original)

    def test_references_do_not_bypass_live_identity_or_locked_annotation_checks(self):
        w, bg, ref, rows = fixture(); add_reference(w, ref); declare_page_ocgs(w, [1], [ref])
        w.pages[0]['/Annots'][0].get_object()[NameObject('/F')] = FloatObject(128)
        report = inspect_pdf(saved(w), rows, [1], [LAYER])
        self.assertTrue(any('editing is restricted' in s for s in report['issues']))
        del w.pages[0]['/Annots']
        report = inspect_pdf(saved(w), [], [1], [LAYER])
        self.assertTrue(any('zero live' in s for s in report['issues']))

    @unittest.skipUnless(shutil.which('qpdf'), 'qpdf CLI not installed')
    def test_saved_synthetic_pdf_passes_qpdf_without_warnings(self):
        w, bg, ref, rows = fixture(); add_reference(w, ref); declare_page_ocgs(w, [1], [ref])
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'synthetic.pdf'; path.write_bytes(saved(w).getvalue())
            result = subprocess.run(['qpdf', '--check', str(path)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertNotIn('WARNING', result.stdout + result.stderr)


if __name__ == '__main__':
    unittest.main()
