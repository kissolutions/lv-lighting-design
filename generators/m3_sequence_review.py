"""Validate M3 endpoint sequence assignments and export a review-first HTML/CSV package.

Companion v0.1 leaves existing project model schemas unchanged.
Usage: python -m generators.m3_sequence_review MODEL COMPANION OUTDIR
       [--standard-catalog APPROVED_CATALOG.json] [--lock-check]
"""
import argparse
import csv
import html
import json
from collections import defaultdict
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT=Path(__file__).resolve().parents[1]
SCHEMA=ROOT/'schemas/m3-sequence-assignments-v0.1.schema.json'
SCHEMA_V02=ROOT/'schemas/m3-sequence-assignments-v0.2.schema.json'
FUNCTIONS=('manual','occupancy','light_reduction','daylight','schedule','emergency')


def validate(model, companion, standard_catalog=None, locked=False):
    """Return finding records. The standard catalog MUST be independently approved."""
    standard_catalog=standard_catalog or []
    findings=[]
    def fail(scope,msg):
        findings.append(dict(entity_id=str(scope),rule='M3-SEQ',message=msg))
    version=companion.get('schema_version')
    schema=SCHEMA_V02 if version=='0.2.0' else SCHEMA
    for err in Draft202012Validator(json.loads(schema.read_text())).iter_errors(companion):
        fail('/'.join(map(str,err.absolute_path)),err.message)
    if findings:return findings
    if model.get('project',{}).get('id')!=companion['project_id']:fail('project','M3 companion project differs from model')
    if model.get('project',{}).get('model_revision')!=companion['model_revision']:fail('project','M3 companion revision differs from model')
    spaces={s['id']:s for s in model.get('spaces',[])}
    zones={z['id']:z for z in model.get('light_zones',[])}
    lights={l['id']:l for l in model.get('light_objects',[])}
    decisions={d['id']:d for d in model.get('decisions',[])}
    parents={z['parent_zone_id'] for z in zones.values() if z.get('parent_zone_id')}
    for z in zones.values():
        if z.get('parent_zone_id') and z['parent_zone_id'] not in zones:fail(z['id'],'Unknown zone parent')
    leaves=set(zones)-parents
    if len(spaces)!=len(model.get('spaces',[])):fail('spaces','Duplicate Space IDs in base model')
    if len(zones)!=len(model.get('light_zones',[])):fail('zones','Duplicate zone IDs in base model')
    for defs,label in ((companion['project_sequences'],'Project'),(standard_catalog,'Standard')):
        seen=set()
        for d in defs:
            ident=(d.get('id'),d.get('revision'))
            if ident in seen:fail(ident,'Duplicate '+label+' sequence definition revision')
            seen.add(ident)
    for definition in companion['project_sequences']:
        approval_id=definition['approval_decision_id']
        if definition['status']=='approved':
            decision=decisions.get(approval_id)
            if not decision or decision.get('status')!='confirmed':
                fail(definition['id'],'Approved project sequence definition requires a confirmed owner decision')
        elif approval_id is not None and approval_id not in decisions:
            fail(definition['id'],'Unknown project sequence approval decision')
    if version=='0.2.0':
        for d in companion['project_sequences']:
            f=d['functions'];scheme=f['dimming_scheme'];steps=f['dimming_steps']
            if scheme=='stepped' and steps is None:fail(d['id'],'Stepped dimming needs number of steps >= 2.')
            if scheme!='stepped' and steps is not None:fail(d['id'],'Dimming steps apply only to stepped sequence.')
            if d['status']=='approved' and scheme=='unknown':fail(d['id'],'Approved sequence must declare dimming scheme.')
        for d in standard_catalog:
            if d.get('status')!='approved':continue
            f=d.get('functions',{})
            scheme=f.get('dimming_scheme')
            if scheme not in ('continuous','stepped','none'):
                fail(d.get('id','standard'),'Approved standard sequence needs known dimming scheme.')
            if scheme=='stepped' and (not isinstance(f.get('dimming_steps'),int) or f['dimming_steps']<2):
                fail(d.get('id','standard'),'Approved stepped standard needs dimming_steps >= 2.')
            if scheme!='stepped' and f.get('dimming_steps') is not None:
                fail(d.get('id','standard'),'Non-stepped standard cannot specify dimming_steps.')
        for a in companion['assignments']:
            if a['dimming_scheme_override'] is not None:
                if a['decision_id'] is None or decisions.get(a['decision_id'],{}).get('status')!='confirmed':
                    fail(a['endpoint_zone_id'],'Dimming scheme override requires confirmed owner decision.')
                if not a['override_note']:fail(a['endpoint_zone_id'],'Dimming scheme override requires explanation and verification.')
    pseq={(x['id'],x['revision']):x for x in companion['project_sequences']}
    std={(x.get('id'),x.get('revision')):x for x in standard_catalog if isinstance(x,dict)}
    seen=set()
    for a in companion['assignments']:
        zid=a['endpoint_zone_id'];seq=a['sequence_id'];rev=a['sequence_revision'];key=(seq,rev)
        if zid in seen:fail(zid,'Multiple active sequence assignments for an endpoint')
        seen.add(zid)
        if zid not in zones:fail(zid,'Unknown zone assignment')
        elif zid in parents:fail(zid,'Parent zones cannot have a sequence assignment')
        is_std=seq.startswith('SEQ-')
        if is_std and a['origin_basis']!='matched_standard':fail(zid,'Standard SEQ must use matched_standard origin')
        if not is_std and a['origin_basis']!='owner_custom':fail(zid,'Project PSEQ must use owner_custom origin')
        definition=(std if is_std else pseq).get(key)
        if definition is None:fail(zid,'Unresolved sequence revision; standards need an independently approved catalog')
        elif definition.get('status')!='approved' and (is_std or a['assignment_status']=='accepted'):
            fail(zid,'Selected/accepted sequence definition is not approved')
        if a['assignment_status']=='accepted':
            decision=decisions.get(a['decision_id'])
            if not decision or decision.get('status')!='confirmed':
                fail(zid,'Accepted endpoint assignment requires a confirmed owner decision')
            if not a['requirement_refs']:fail(zid,'Accepted assignment requires requirement evidence')
        if a['decision_id'] is not None and a['decision_id'] not in decisions:fail(zid,'Unknown owner decision')
    for d in companion['daylight_determinations']:
        if d['space_id'] not in spaces:fail(d['space_id'],'Unknown daylight Space')
    for d in companion['space_direction_reviews']:
        sid=d['space_id']
        if sid not in spaces:fail(sid,'Unknown reviewed Space')
        if any(x not in zones for x in d['endpoint_zone_ids']):fail(sid,'Unknown zone referenced from Space direction review')
        if any(x in parents for x in d['endpoint_zone_ids']):fail(sid,'Space direction references parent instead of endpoint')
        if any(x not in lights for x in d['light_object_ids']):fail(sid,'Unknown Light Object')
        actual=set(spaces.get(sid,{}).get('light_object_ids',[]))
        if actual!=set(d['light_object_ids']):fail(sid,'Space review Light Objects do not match canonical Space membership')
        if d['disposition']=='lit_controlled' and (not actual or not d['endpoint_zone_ids']):fail(sid,'Lit-controlled Space needs lights and endpoint directions')
        if d['disposition']=='unlit_confirmed' and actual:fail(sid,'Unlit disposition contradicts registered lights')
    if locked:
        if set(zones)-parents != seen:fail('M3','Every leaf requires one active sequence assignment before lock')
        if any(a['assignment_status']!='accepted' for a in companion['assignments']):fail('M3','Every sequence assignment must be accepted for lock')
        for key,entries in (('daylight_determinations',companion['daylight_determinations']),('space_direction_reviews',companion['space_direction_reviews'])):
            counts=defaultdict(int)
            for e in entries:counts[e['space_id']]+=1
            if any(counts.get(sid,0)!=1 for sid in spaces):
                fail('M3',key+' must contain exactly one reviewed record per Space')
        if any(d['determination']=='unresolved' for d in companion['daylight_determinations']):
            fail('M3','Daylight determination unresolved; cannot lock')
        if any(d['disposition'] in ('missing_source_lights','unresolved') for d in companion['space_direction_reviews']):
            fail('M3','Space control coverage unresolved; cannot lock')
        if model.get('project',{}).get('controls_narrative_review',{}).get('status')!='locked':
            fail('M3','Base model owner narrative review is not locked')
        if not any(d.get('status')=='confirmed' for d in decisions.values()):
            fail('M3','No confirmed owner decision found in base model')
    return findings


def tables(model,companion,standard_catalog=None):
    byseq={(d['id'],d['revision']):d for d in companion['project_sequences']}
    byseq.update({(d['id'],d['revision']):d for d in (standard_catalog or [])})
    zones={z['id']:z for z in model['light_zones']}
    spaces={s['id']:s for s in model['spaces']}
    zone_spaces=defaultdict(set)
    for s in spaces.values():
        for zid in s.get('light_zone_ids',[]):zone_spaces[zid].add(s['id'])
    # If a Space lists only a parent, project its descendant endpoint associations.
    for zid,z in zones.items():
        parent=z.get('parent_zone_id')
        while parent in zones:
            zone_spaces[zid].update(zone_spaces[parent])
            parent=zones[parent].get('parent_zone_id')
    grouped=defaultdict(list)
    for a in companion['assignments']:grouped[a['sequence_id'],a['sequence_revision']].append(a)
    sections=[]
    for key in sorted(grouped):
        definition=byseq.get(key,{})
        assignments=[]
        for a in sorted(grouped[key],key=lambda x:x['endpoint_zone_id']):
            ids=sorted(zone_spaces.get(a['endpoint_zone_id'],[]))
            assignments.append(dict(sequence_id=a['sequence_id'],sequence_revision=a['sequence_revision'],
                endpoint_zone_id=a['endpoint_zone_id'],room_ids='; '.join(ids),
                room_names='; '.join(spaces[s]['name'] for s in ids),
                assignment_status=a['assignment_status'],
                dimming_scheme=a.get('dimming_scheme_override') or definition.get('functions',{}).get('dimming_scheme','UNSPECIFIED_V01'),
                dimming_steps=definition.get('functions',{}).get('dimming_steps'),
                parameters=json.dumps(a['parameters'],sort_keys=True),
                light_reduction=definition.get('functions',{}).get('light_reduction','UNKNOWN'),
                manual=definition.get('functions',{}).get('manual','UNKNOWN'),
                occupancy=definition.get('functions',{}).get('occupancy','UNKNOWN'),
                daylight=definition.get('functions',{}).get('daylight','UNKNOWN'),
                schedule=definition.get('functions',{}).get('schedule','UNKNOWN'),
                emergency=definition.get('functions',{}).get('emergency','UNKNOWN'),
                decision_id=a['decision_id'] or '',override_note=a['override_note'] or ''))
        sections.append(dict(sequence_id=key[0],revision=key[1],title=definition.get('title','UNRESOLVED DEFINITION'),
            narrative=definition.get('narrative','Sequence definition missing; not approved'),
            status=definition.get('status','unresolved'),assignments=assignments))
    return sections


def export(model,companion,outdir,standard_catalog=None,locked=False):
    findings=validate(model,companion,standard_catalog,locked)
    out=Path(outdir)
    if out.exists() and any(out.iterdir()):raise ValueError('Output directory must be empty')
    out.mkdir(parents=True,exist_ok=True)
    sections=tables(model,companion,standard_catalog)
    rows=[a for s in sections for a in s['assignments']]
    with (out/'m3_endpoint_assignments.csv').open('w',newline='') as f:
        fields=list(rows[0]) if rows else ['sequence_id','endpoint_zone_id','assignment_status']
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
        for row in rows:
            # Prevent spreadsheet formula execution when opened in Excel.
            w.writerow({k:("'"+v if isinstance(v,str) and v.lstrip().startswith(('=','+','-','@')) else v)
                for k,v in row.items()})
    with (out/'m3_daylight_review.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['space_id','determination','basis','source_refs']);w.writeheader()
        for d in companion['daylight_determinations']:
            w.writerow({**d,'source_refs':'; '.join(d['source_refs'])})
    with (out/'m3_space_direction_review.csv').open('w',newline='') as f:
        fields=['space_id','disposition','endpoint_zone_ids','light_object_ids','source_refs','notes']
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
        for d in companion['space_direction_reviews']:
            w.writerow({k:'; '.join(v) if isinstance(v,list) else v for k,v in d.items()})
    esc=lambda x:html.escape(str(x))
    parts=['<!doctype html><html><head><meta charset="utf-8"><style>body{font:11pt Arial;margin:2em}table{border-collapse:collapse;width:100%}th,td{border:1px solid #aaa;padding:5px;text-align:left}section{break-before:page}h2{margin-bottom:0}thead{display:table-header-group}</style></head><body>']
    parts.append('<h1>M3 Lighting Control Narrative Review</h1><p>'+esc(model['project']['name'])+' / '+esc(companion['model_revision'])+' / '+('LOCK CHECK' if locked else 'PROVISIONAL REVIEW')+'</p>')
    if findings:parts.append('<h2>Review findings</h2><ul>'+''.join('<li>'+esc(x['entity_id']+': '+x['message'])+'</li>' for x in findings)+'</ul>')
    for s in sections:
        parts.append('<section><h2>'+esc(s['sequence_id']+' r'+s['revision']+' — '+s['title'])+'</h2><p>Status: '+esc(s['status'])+'</p><p>'+esc(s['narrative'])+'</p>')
        if s['assignments']:
            fields=list(s['assignments'][0]);parts.append('<table><thead><tr>'+''.join('<th>'+esc(f)+'</th>' for f in fields)+'</tr></thead><tbody>')
            for a in s['assignments']:parts.append('<tr>'+''.join('<td>'+esc(a[f])+'</td>' for f in fields)+'</tr>')
            parts.append('</tbody></table>')
        parts.append('</section>')
    parts.append('</body></html>')
    (out/'m3_sequence_narratives.html').write_text(''.join(parts))
    (out/'m3_review_report.json').write_text(json.dumps(dict(findings=findings,lock_check=locked,project_id=companion['project_id'],model_revision=companion['model_revision'],printable_pdf_generated=False,source_code_compliance_certified=False),indent=2)+'\n')
    return findings


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('model',type=Path);p.add_argument('companion',type=Path);p.add_argument('outdir',type=Path)
    p.add_argument('--standard-catalog',type=Path)
    p.add_argument('--lock-check',action='store_true')
    a=p.parse_args()
    catalog=json.loads(a.standard_catalog.read_text()) if a.standard_catalog else []
    findings=export(json.loads(a.model.read_text()),json.loads(a.companion.read_text()),a.outdir,catalog,a.lock_check)
    print(json.dumps(dict(findings=findings,reviewable=not bool(findings)),indent=2))
    if findings:raise SystemExit(1)


if __name__=='__main__':main()
