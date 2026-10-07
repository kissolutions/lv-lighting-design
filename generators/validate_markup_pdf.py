"""Fail a milestone build on absent/lost live annotations; no rendering claim."""
import argparse
import csv
import json
from pathlib import Path
from pypdf import PdfReader

REGISTER_FIELDS=('annotation_id','entity_id','entity_type','role','plan_page_number',
                 'nested_in','source_tag','assembly_id')


def write_annotation_register(path, records, model):
    """Write every delivered /NM, enriching room and light metadata by identity."""
    spaces={s['id']:s for s in model['spaces']}
    lights={l['id']:l for l in model['light_objects']}
    seen=set(); rows=[]
    for record in records:
        row={k:record.get(k) for k in REGISTER_FIELDS}
        if not row['annotation_id'] or row['annotation_id'] in seen:
            raise ValueError('Missing or duplicate annotation ID.')
        seen.add(row['annotation_id'])
        if row['entity_type']=='space':
            row['nested_in']=spaces[row['entity_id']].get('nested_in')
        if row['entity_type']=='light':
            l=lights[row['entity_id']]
            row.update(source_tag=l['source'].get('source_tag'),assembly_id=l.get('assembly_id'))
        rows.append(row)
    with Path(path).open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=REGISTER_FIELDS);writer.writeheader();writer.writerows(rows)


def inspect_pdf(pdf, records, plan_pages):
    """plan_pages uses final-PDF 1-based page numbers, excluding schedule pages.

    Register roles: room_footprint, light_label, other. Checks actual saved objects.
    """
    reader=PdfReader(pdf);issues=[];counts={};expected={};actual={}
    def fail(message):issues.append(message)
    if not plan_pages or len(set(plan_pages))!=len(plan_pages):
        fail('Declare a nonempty unique list of plan pages.')
    for row in records:
        aid=row.get('annotation_id')
        if not aid or aid in expected:fail('Missing or duplicate register annotation ID.');continue
        if not row.get('entity_id') or not row.get('entity_type'):
            fail('Register object identity missing: '+aid)
        if row.get('role') not in ('room_footprint','light_label','other'):
            fail('Register role missing/invalid: '+aid)
        try: page=int(row['plan_page_number'])
        except (KeyError,TypeError,ValueError):page=-1
        if page not in plan_pages:fail('Register page outside declared plan pages: '+aid)
        expected[aid]=(row,page)
    for page in plan_pages:
        if not isinstance(page,int) or page<1 or page>len(reader.pages):
            fail('Invalid plan page: '+str(page));continue
        annotations=reader.pages[page-1].get('/Annots',[])
        annotations=annotations.get_object() if hasattr(annotations,'get_object') else annotations
        counts[page]=len(annotations)
        if not annotations:fail(f'Plan page {page} has zero live annotations; build rejected.')
        for ref in annotations:
            a=ref.get_object();aid=a.get('/NM')
            if not aid or aid in actual:
                fail(f'Plan page {page}: missing or duplicate /NM.');continue
            actual[aid]=page
            row,registered_page=expected.get(aid,({},None))
            if not row:fail('Annotation absent from register: '+aid)
            elif registered_page!=page:fail('Annotation page differs from register: '+aid)
            if int(a.get('/F',0)) & (1|2|32|64|128|512):
                fail('Annotation is hidden or editing is restricted: '+aid)
            role=row.get('role');subtype=a.get('/Subtype')
            if role=='room_footprint' and subtype!='/Polygon':fail('Room footprint must be /Polygon: '+aid)
            if role=='light_label' and subtype!='/FreeText':fail('Light label must be /FreeText: '+aid)
            if role=='room_footprint' and subtype=='/Polygon':
                v=a.get('/Vertices',[]);color=a.get('/IC',[]);opacity=a.get('/CA')
                if len(v)<6 or len(v)%2:fail('Invalid room /Vertices: '+aid)
                else:
                    try:
                        from .room_geometry_review import _polygons
                        _polygons([dict(space_id=aid,level='check',frame_id='check',vertices=list(zip(v[::2],v[1::2])))])
                    except (ValueError,TypeError):fail('Invalid single-ring room geometry: '+aid)
                if len(color) not in (1,3,4) or any(not 0<=float(c)<=1 for c in color):fail('Room fill /IC missing/invalid: '+aid)
                if opacity is None or not 0<float(opacity)<=1:fail('Room opacity /CA missing/invalid: '+aid)
            if subtype=='/FreeText':
                ap=a.get('/AP');ap=ap.get_object() if hasattr(ap,'get_object') else ap
                normal=ap.get('/N') if ap else None
                normal=normal.get_object() if hasattr(normal,'get_object') else normal
                if not hasattr(normal,'get_data') or not normal.get_data():fail('FreeText appearance stream missing/empty: '+aid)
    for aid in set(expected)-set(actual):fail('Registered annotation missing from PDF: '+aid)
    return dict(checks_pass=not issues,issues=issues,annotations_per_plan_page=counts)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('pdf',type=Path);p.add_argument('register',type=Path)
    p.add_argument('--plan-pages',type=int,nargs='+',required=True)
    args=p.parse_args()
    with args.register.open(newline='') as f:records=list(csv.DictReader(f))
    report=inspect_pdf(args.pdf,records,args.plan_pages)
    print(json.dumps(report,indent=2));return 0 if report['checks_pass'] else 1


if __name__=='__main__':raise SystemExit(main())
