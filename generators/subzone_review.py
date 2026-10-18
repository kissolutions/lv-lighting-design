"""Repeatable M3 subzone detection/CSV review and additive label manifest.

Never edits existing Light Objects or accepted PDF marks. CSV is the ONLY edit
surface; markup is a deterministic derived output. Daylight can reopen work.
"""
import argparse
import csv
import json
import re
from collections import Counter,defaultdict
from pathlib import Path
from jsonschema import Draft202012Validator

SCHEMA=Path(__file__).resolve().parents[1]/'schemas/subzone-review-v0.1.schema.json'
FIELDS=['space_id','full_room_name','light_id','light_label','fixture_type_id','subzone_label','zone_id','basis','confidence','source_group','evidence','owner_comment']
CONFIDENCE={'LOW':0,'MEDIUM':1,'HIGH':2,'VERIFIED':3}
FLAGS={f'SZ-{i:02d}' for i in range(1,8)}


def validate(model,register,accept=False):
    issues=[]
    def fail(entity,msg):issues.append(dict(entity_id=str(entity),rule='subzone',message=msg))
    for e in Draft202012Validator(json.loads(SCHEMA.read_text())).iter_errors(register):
        fail('/'.join(map(str,e.absolute_path)),e.message)
    if issues:return issues
    if model['project']['id']!=register['project_id']:fail('project','Project ID mismatch.')
    if model['project']['model_revision']!=register['model_revision']:fail('project','Source model revision mismatch.')
    spaces={s['id']:s for s in model['spaces']};lights={l['id']:l for l in model['light_objects']}
    refs={r['id'] for r in model.get('source_references',[])}
    canonical={lid:sid for sid,s in spaces.items() for lid in s['light_object_ids']}
    counts=Counter(lid for s in spaces.values() for lid in s['light_object_ids'])
    for lid,n in counts.items():
        if n!=1:fail(lid,'Light Point does not have exactly one authoritative served Space.')
    seen_spaces=set();screen={}
    for s in register['spaces']:
        sid=s['space_id']
        if sid not in spaces:fail(sid,'Unknown Space.')
        if sid in seen_spaces:fail(sid,'Duplicate Space screening record.')
        seen_spaces.add(sid);screen[sid]=s
        if s['detection_disposition']=='single_zone_candidate':
            if s['subzone_required'] or s['code_screen']!='resolved_no_split' or s['daylight_screen']!='resolved_no_split':
                fail(sid,'Single-zone fast path requires resolved code/daylight screens and no split.')
            if s['source_control_intent_status']!='complete':
                fail(sid,'Single-zone fast path needs supported source intent; missing source information is not a negative flag.')
    seen_findings=set();flags=defaultdict(list)
    for f in register['detection_findings']:
        if f['id'] in seen_findings:fail(f['id'],'Duplicate detection finding ID.')
        seen_findings.add(f['id'])
        if f['space_id'] not in spaces:fail(f['id'],'Finding refers to unknown Space.')
        if any(x not in refs for x in f['source_ref_ids']):fail(f['id'],'Unknown evidence reference.')
        flags[f['space_id']].append(f)
    for sid,s in screen.items():
        if s['detection_disposition']=='single_zone_candidate' and any(f['status']!='dismissed' for f in flags[sid]):
            fail(sid,'Open detection flags prevent single-zone fast path.')
    seen_lights=set();zone_keys=defaultdict(set);labels=defaultdict(set)
    for a in register['assignments']:
        lid=a['light_id'];sid=a['space_id']
        if lid in seen_lights:fail(lid,'Duplicate Light Point membership in working register.')
        seen_lights.add(lid)
        if lid not in lights:fail(lid,'Unknown Light Point.')
        if sid not in spaces:fail(lid,'Unknown assignment Space.')
        elif canonical.get(lid)!=sid:fail(lid,'Assignment violates accepted served Space membership.')
        label=a['subzone_label'];zid=a['zone_id']
        if (label is None)!=(zid is None):fail(lid,'Unzoned scratch rows require both label and zone ID null.')
        if label is not None:
            if zid in zone_keys[sid] and any(x['zone_id']==zid and x['subzone_label']!=label for x in register['assignments']):
                fail(lid,'Stable Zone ID mapped to different labels.')
            zone_keys[sid].add(zid);labels[sid].add(label)
            if any(x['space_id']==sid and x['subzone_label']==label and x['zone_id']!=zid for x in register['assignments']):
                fail(lid,'Subzone label belongs to multiple Zone IDs in same Space.')
        if accept and label is None:fail(lid,'Unzoned scratch Light Point blocks acceptance and SEQ assignment.')
    for sid in screen:
        expected={x for x,s in canonical.items() if s==sid}
        actual={a['light_id'] for a in register['assignments'] if a['space_id']==sid}
        if expected!=actual:fail(sid,'Review register must enumerate every accepted Light Point exactly once.')
    for sid,ls in labels.items():
        ordered=sorted(ls)
        seq=[]
        for k in range(len(ordered)):
            n=k+1;word=''
            while n:
                n,rem=divmod(n-1,26);word=chr(97+rem)+word
            seq.append(word)
        if ordered!=seq:fail(sid,'Subzone labels must be sequential lowercase a,b,c... for multi-zone Spaces.')
        if len(zone_keys[sid])==1 and len(ls)==1:
            # Allowed as a provisional source-driven grouping; accepted single-zone spaces omit display lettering.
            if accept and not screen.get(sid,{}).get('subzone_required'):
                fail(sid,'Single-zone room should not produce unnecessary labelled child zone.')
    seen_daylight=set()
    for d in register['daylight_areas']:
        did=d['daylight_id']
        if did in seen_daylight:fail(did,'Duplicate daylight-zone ID.')
        seen_daylight.add(did)
        if any(sid not in spaces for sid in d['space_ids']):fail(did,'Daylight area references missing Space.')
        if any(lid not in lights for lid in d['light_ids']):fail(did,'Daylight area references missing Light Point.')
        for lid in d['light_ids']:
            if canonical.get(lid) not in d['space_ids']:fail(did,'Daylight Light Point must belong to one of covered Spaces.')
        if any(x not in refs for x in d['source_ref_ids']):fail(did,'Unknown daylight evidence reference.')
    if accept:
        if set(screen)!=set(spaces):fail('spaces','Acceptance requires a screening disposition for every Space.')
        if register['acceptance']['status']!='accepted':fail('review','Owner acceptance status required.')
        if not register['acceptance']['decision_id']:fail('review','Owner decision ID required.')
        if register['acceptance']['accepted_revision']!=register['review_revision']:fail('review','Accepted revision must match current review revision.')
        decisions={d['id']:d for d in model.get('decisions',[])}
        d=decisions.get(register['acceptance']['decision_id'])
        if not d or d.get('status')!='confirmed':fail('review','Owner decision must exist and be confirmed.')
        for sid,s in screen.items():
            if s['detection_disposition'] in ('source_review_required','reprocess_required') or s['code_screen']=='unresolved' or s['daylight_screen']=='unresolved':
                fail(sid,'Unresolved source, code or daylight screening blocks acceptance.')
            for f in flags[sid]:
                if f['status'] in ('ambiguous','probable') or (f['status']!='dismissed' and CONFIDENCE[f['confidence']]<CONFIDENCE['HIGH']):
                    fail(f['id'],'Unresolved low-confidence finding requires owner disposition.')
    return issues


def csv_rows(model,register):
    spaces={s['id']:s for s in model['spaces']}
    lights={l['id']:l for l in model['light_objects']}
    rows=[]
    for a in register['assignments']:
        l=lights[a['light_id']];s=spaces[a['space_id']]
        rows.append(dict(space_id=s['id'],full_room_name=' '.join(x for x in (s.get('room_number'),s['name']) if x),
            light_id=l['id'],light_label=l.get('label') or '',fixture_type_id=l['source']['fixture_type_id'],
            subzone_label=a['subzone_label'] or 'Unzoned',zone_id=a['zone_id'] or '',
            basis=a['basis'],confidence=a['confidence'],source_group=a['source_group'],evidence=a['evidence'],owner_comment=a['owner_comment']))
    return sorted(rows,key=lambda a:(a['full_room_name'].casefold(),a['space_id'],a['subzone_label'],a['light_label'],a['light_id']))


def discussion_findings(register):
    return [f for f in register['detection_findings']
        if f['status']!='dismissed' and (CONFIDENCE[f['confidence']]<CONFIDENCE['HIGH'] or f['status'] in ('probable','ambiguous'))]


def label_manifest(model,register):
    """Deterministic additional annotation roles; physical page coordinates follow accepted anchors."""
    lights={l['id']:l for l in model['light_objects']}
    out=[]
    for a in register['assignments']:
        if a['subzone_label'] is None:continue
        l=lights[a['light_id']]
        source=l['source'];anchor=source.get('drawing_anchor')
        out.append(dict(annotation_id='SZLABEL-'+a['light_id'],
            role='subzone_label',entity_type='light',light_id=a['light_id'],
            drawing_page_id=source.get('drawing_page_id'),source_annotation_id=source.get('source_annotation_id'),
            anchor=anchor,display_label=a['subzone_label'],
            comment_field='Subzone: '+a['subzone_label'],
            note='Add independent editable annotation beside existing light label; preserve all other comments.'))
    return sorted(out,key=lambda x:x['light_id'])


def export(model,register,outdir):
    issues=validate(model,register)
    if issues:raise ValueError(json.dumps(issues))
    out=Path(outdir)
    if out.exists() and any(out.iterdir()):raise ValueError('Choose a new empty output directory.')
    out.mkdir(parents=True,exist_ok=True)
    tables={'subzone_owner_review.csv':csv_rows(model,register),
      'subzone_detection.csv':[
        dict(space_id=f['space_id'],flag=f['flag'],confidence=f['confidence'],status=f['status'],
          evidence=f['evidence'],source_ref_ids='; '.join(f['source_ref_ids']),finding_id=f['id'])
        for f in register['detection_findings']],
      'subzone_owner_discussion.csv':[
        dict(space_id=f['space_id'],flag=f['flag'],confidence=f['confidence'],status=f['status'],
          evidence=f['evidence'],finding_id=f['id']) for f in discussion_findings(register)]}
    defaults={'subzone_owner_review.csv':FIELDS,
      'subzone_detection.csv':['space_id','flag','confidence','status','evidence','source_ref_ids','finding_id'],
      'subzone_owner_discussion.csv':['space_id','flag','confidence','status','evidence','finding_id']}
    for name,rows in tables.items():
        with (out/name).open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=defaults[name]);w.writeheader()
            for r in rows:
                w.writerow({k:("'"+str(v) if isinstance(v,str) and v.lstrip().startswith(('=','+','-','@')) else v) for k,v in r.items()})
    (out/'subzone_label_annotations.json').write_text(json.dumps(label_manifest(model,register),indent=2)+'\n')
    (out/'subzone_report.json').write_text(json.dumps(dict(project_id=register['project_id'],
        model_revision=register['model_revision'],review_revision=register['review_revision'],
        low_confidence_findings=len(discussion_findings(register)),
        scratch_unzoned_count=sum(a['zone_id'] is None for a in register['assignments']),
        accepted=not validate(model,register,accept=True),source_pdf_modified=False),indent=2)+'\n')
    return tables


def import_review(model,previous,edited_csv):
    """Import ONLY owner editable label/comment; reject added/deleted/changed identities."""
    updated=json.loads(json.dumps(previous))
    expected={a['light_id']:a for a in updated['assignments']}
    with Path(edited_csv).open(newline='') as f:
        rows=list(csv.DictReader(f))
    if len(rows)!=len(expected) or len({r['light_id'] for r in rows})!=len(rows) or {r['light_id'] for r in rows}!=set(expected):
        raise ValueError('CSV Light Point identities are missing, added or duplicated.')
    baseline={r['light_id']:r for r in csv_rows(model,previous)}
    for row in rows:
        lid=row['light_id'];orig=baseline[lid]
        for col in ('space_id','full_room_name','light_label','fixture_type_id'):
            if row.get(col)!=str(orig[col]):raise ValueError('Immutable CSV evidence/identity changed: '+lid+'/'+col)
        a=expected[lid];label=row['subzone_label'].strip()
        if label=='Unzoned' or not label:
            a['subzone_label']=None;a['zone_id']=None
        else:
            if not re.fullmatch('[a-z]+',label):raise ValueError('Invalid lowercase subzone label for '+lid)
            a['subzone_label']=label
            # Reuse stable previously owned zone ID whenever the label already exists;
            # owner-added new label is provisional and needs later explicit stable ID allocation.
            keys={x['subzone_label']:x['zone_id'] for x in previous['assignments']
                if x['space_id']==a['space_id'] and x['zone_id'] is not None}
            a['zone_id']=keys.get(label) or 'SZ-'+a['space_id']+'-'+label
        a['owner_comment']=row.get('owner_comment','')
        a['basis']='owner' if a['subzone_label']!=expected[lid]['subzone_label'] else a['basis']
    updated['acceptance']=dict(status='draft',decision_id=None,accepted_revision=None)
    updated['review_revision']=previous['review_revision']+'-R'
    issues=validate(model,updated)
    if issues:raise ValueError(json.dumps(issues))
    return updated


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('model',type=Path);p.add_argument('register',type=Path)
    p.add_argument('output',type=Path)
    p.add_argument('--owner-csv',type=Path,help='Import owner edits, then export revised register and markup manifest')
    p.add_argument('--lock-check',action='store_true')
    a=p.parse_args()
    model=json.loads(a.model.read_text());reg=json.loads(a.register.read_text())
    if a.owner_csv:reg=import_review(model,reg,a.owner_csv)
    if a.lock_check:
        issues=validate(model,reg,accept=True)
        if issues:raise SystemExit(json.dumps(issues,indent=2))
    export(model,reg,a.output)
    if a.owner_csv:(a.output/'updated_subzone_register.json').write_text(json.dumps(reg,indent=2)+'\n')

if __name__=='__main__':main()
