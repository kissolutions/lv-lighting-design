"""Add CSV-derived editable subzone labels to an existing accepted Light Point PDF.

Original drawings/Light Point positions are never redrawn. Uses pypdf annotations.
Supply explicit PDF page ID -> zero-based page index mapping.
Accepted M1/M2 drawing anchors are TOP_LEFT (PyMuPDF points) by default.
A manifest record can opt into 'anchor_origin': 'bottom_left'. Run each revision
on the ORIGINAL accepted M2 PDF, never on a prior subzone output.
"""
import argparse
import json
import re
from pathlib import Path
from pypdf import PdfReader,PdfWriter
from pypdf.generic import DictionaryObject,NameObject,TextStringObject,ArrayObject,FloatObject,NumberObject

def render(source_pdf,output_pdf,manifest,page_map):
    reader=PdfReader(str(source_pdf))
    writer=PdfWriter()
    writer.append(reader)
    updated=[];unmatched=[]
    for a in manifest:
        anchor=a.get('anchor')
        if not isinstance(anchor,dict) or not {'x_pt','y_pt'}<=set(anchor):
            raise ValueError('Accepted Light Point anchor coordinates required: '+a['light_id'])
        pageid=a['drawing_page_id']
        if pageid not in page_map:raise ValueError('No explicit PDF page mapping for '+str(pageid))
        idx=page_map[pageid]
        if not isinstance(idx,int) or not 0<=idx<len(writer.pages):raise ValueError('Page mapping out of range')
        x=float(anchor['x_pt']);y=float(anchor['y_pt'])
        origin=a.get('anchor_origin',anchor.get('origin','top_left'))
        if origin not in ('top_left','bottom_left'):
            raise ValueError('Unknown anchor origin for '+a['light_id']+': '+str(origin))
        page=writer.pages[idx]
        # The model stores DISPLAYED-page coordinates after crop/rotation.
        # A plain height inversion only applies to unrotated uncropped pages;
        # refuse ambiguous transforms rather than misplacing every label.
        if int(page.get('/Rotate',0) or 0)%360:
            raise ValueError('Rotated PDF page requires explicit displayed-to-native transform: '+str(pageid))
        mb=[float(v) for v in page.mediabox]
        cb=[float(v) for v in page.cropbox]
        if mb!=cb or abs(mb[0])>1e-6 or abs(mb[1])>1e-6:
            raise ValueError('Cropped or offset PDF page needs explicit coordinate transform: '+str(pageid))
        width=float(page.mediabox.width);height=float(page.mediabox.height)
        if not 0<=x<=width or not 0<=y<=height:
            raise ValueError('Light Point anchor outside page before conversion: '+a['light_id'])
        if origin=='top_left':y=height-y
        if not 0<=x<=width or not 0<=y<=height:
            raise ValueError('Light Point anchor outside PDF page: '+a['light_id'])
        # PyMuPDF/M1/M2 top-left points convert to native PDF bottom-left
        # coordinates using the actual page height; explicit bottom_left stays unchanged.
        # Place badge next to the existing anchor. The source Light Point stays unchanged.
        rect=ArrayObject([FloatObject(x+12),FloatObject(y-19),FloatObject(x+29),FloatObject(y-2)])
        annotation=DictionaryObject({
            NameObject('/Type'):NameObject('/Annot'),
            NameObject('/Subtype'):NameObject('/FreeText'),
            NameObject('/Rect'):rect,
            NameObject('/NM'):TextStringObject(a['annotation_id']),
            NameObject('/Contents'):TextStringObject(a['display_label']),
            NameObject('/DA'):TextStringObject('/Helv 11 Tf 0 0 0 rg'),
            NameObject('/F'):NumberObject(4),
            NameObject('/T'):TextStringObject('KIS Subzone Label'),
            NameObject('/Subj'):TextStringObject('Subzone '+a['display_label']),
            NameObject('/C'):ArrayObject([FloatObject(.85),FloatObject(.92),FloatObject(.98)])
        })
        writer.add_annotation(page_number=idx,annotation=annotation)
        # Match original annotation by persistent PDF /NM (source annotation ID),
        # then append/upsert one structured comment field without altering others.
        original_id=a.get('source_annotation_id')
        found=False
        if original_id:
            for item in writer.pages[idx].get('/Annots',[]):
                target=item.get_object()
                if str(target.get('/NM',''))!=str(original_id):continue
                if str(target.get('/Subtype',''))=='/FreeText' and str(target.get('/T',''))=='KIS Subzone Label':continue
                old=str(target.get('/Contents','') or '')
                new=re.sub(r'(?:^|\n)Subzone: [a-z]+(?=\n|$)','',old).strip()
                target[NameObject('/Contents')]=TextStringObject((new+'\n' if new else '')+'Subzone: '+a['display_label'])
                found=True
                break
        (updated if found else unmatched).append(a['light_id'])
    with Path(output_pdf).open('wb') as f:writer.write(f)
    return dict(created=len(manifest),comments_updated=updated,unmatched_source_annotations=unmatched,
        warning='Unmatched /NM comments need owner/manual PDF ID reconciliation; graphic labels remain added.' if unmatched else None)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('source_pdf',type=Path);p.add_argument('manifest_json',type=Path)
    p.add_argument('page_map_json',type=Path);p.add_argument('output_pdf',type=Path)
    a=p.parse_args()
    result=render(a.source_pdf,a.output_pdf,json.loads(a.manifest_json.read_text()),
        json.loads(a.page_map_json.read_text()))
    print(json.dumps(result,indent=2))
    if result['unmatched_source_annotations']:raise SystemExit(1)

if __name__=='__main__':main()
