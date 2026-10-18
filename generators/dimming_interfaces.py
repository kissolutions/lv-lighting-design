"""Validated source/selected fixture dimming-interface companion and schedule export.

These electrical signaling types are not synonyms for fixture dimming capability,
driver architecture, CV/CC regulation, or M3 continuous/stepped behavior.
"""
import argparse
import csv
import json
from pathlib import Path
from jsonschema import Draft202012Validator

SCHEMA=Path(__file__).resolve().parents[1]/'schemas/fixture-dimming-interface-v0.1.schema.json'
ANALOG={'zero_to_ten_v','one_to_ten_v'}
UNKNOWN={'unknown'}
NON_DIM={'none'}

def validate(model, register, require_complete=False):
    issues=[]
    def fail(owner,message):issues.append(dict(entity_id=str(owner),rule='fixture-dimming',message=message))
    for error in Draft202012Validator(json.loads(SCHEMA.read_text())).iter_errors(register):
        fail('/'.join(map(str,error.absolute_path)),error.message)
    if issues:return issues
    if model.get('project',{}).get('id') != register['project_id']:fail('project','Project identity mismatch.')
    if model.get('project',{}).get('model_revision') != register['model_revision']:fail('project','Model revision mismatch.')
    fixtures={x['id']:x for x in model.get('fixture_types',[])}
    refs={x['id'] for x in model.get('source_references',[])}
    seen=set()
    for record in register['fixtures']:
        fid=record['fixture_type_id'];basis=record['interface_basis'];key=(fid,basis)
        if key in seen:fail(fid,'Duplicate source/selected dimming interface record.')
        seen.add(key)
        if fid not in fixtures:fail(fid,'Dimming record references unknown fixture type.')
        choices=set(record['dimming_interfaces']);schemes=set(record['supported_dimming_schemes'])
        if len(choices)>1 and choices.intersection({'none','unknown'}):
            fail(fid,'none/unknown interface is mutually exclusive with known interfaces.')
        if len(schemes)>1 and schemes.intersection({'none','unknown'}):
            fail(fid,'none/unknown scheme is mutually exclusive with known schemes.')
        if choices=={'none'} and schemes!={'none'}:fail(fid,'Non-dimming interface must have none scheme.')
        if schemes=={'none'} and choices not in ({'none'},{'unknown'}):
            fail(fid,'Non-dimming fixture cannot declare a dimming interface.')
        if (choices=={'none'} or schemes=={'none'}) and record['minimum_dim_percent'] is not None:
            fail(fid,'Non-dimming fixture must have null minimum dim level.')
        if choices=={'none'} and record['dim_to_off'] is True:
            fail(fid,'Non-dimming fixture cannot have dim-to-off true.')
        if record['signal_mode'] in ('sink','source','sink_or_source') and not choices.intersection(ANALOG):
            fail(fid,'Analog sink/source signal mode requires 0-10 V or 1-10 V interface.')
        if any(x not in refs for x in record['source_ref_ids']):
            fail(fid,'Dimming evidence references unknown source document.')
        if basis=='source' and fid in fixtures:
            cap=fixtures[fid].get('source_dimming_capability')
            if cap=='non_dimmable' and schemes!={'none'} and schemes!={'unknown'}:
                fail(fid,'Source capability non_dimmable conflicts with source dimming schemes.')
            if cap=='dimmable' and schemes=={'none'}:
                fail(fid,'Source capability dimmable conflicts with declared none scheme.')
    if require_complete:
        for fid in fixtures:
            if (fid,'source') not in seen:fail(fid,'Source fixture dimming interface record is missing.')
    return issues


def export(model,register,outdir,require_complete=False):
    issues=validate(model,register,require_complete)
    out=Path(outdir)
    if out.exists() and any(out.iterdir()):raise ValueError('Output directory must be empty.')
    out.mkdir(parents=True,exist_ok=True)
    fixtures={x['id']:x for x in model.get('fixture_types',[])}
    rows=[]
    for r in register['fixtures']:
        fixture=fixtures.get(r['fixture_type_id'],{})
        rows.append(dict(fixture_type_id=r['fixture_type_id'],source_mark=fixture.get('source_mark',''),
            interface_basis=r['interface_basis'],dimming_interfaces='; '.join(r['dimming_interfaces']),
            supported_dimming_schemes='; '.join(r['supported_dimming_schemes']),
            minimum_dim_percent=r['minimum_dim_percent'],dim_to_off=r['dim_to_off'],
            signal_mode=r['signal_mode'],driver_location=r['driver_location'],
            source_ref_ids='; '.join(r['source_ref_ids']),notes=r['notes']))
    fields=['fixture_type_id','source_mark','interface_basis','dimming_interfaces',
            'supported_dimming_schemes','minimum_dim_percent','dim_to_off',
            'signal_mode','driver_location','source_ref_ids','notes']
    with (out/'fixture_dimming_schedule.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
        for row in rows:
            w.writerow({k:("'"+v if isinstance(v,str) and v.lstrip().startswith(('=','+','-','@')) else v)
                for k,v in row.items()})
    (out/'fixture_dimming_validation.json').write_text(json.dumps(dict(findings=issues,
        source_fixture_records_complete=require_complete and not issues,
        model_revision=register['model_revision']),indent=2)+'\n')
    return issues


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('model',type=Path)
    p.add_argument('register',type=Path)
    p.add_argument('output',type=Path)
    p.add_argument('--require-complete',action='store_true')
    a=p.parse_args()
    issues=export(json.loads(a.model.read_text()),json.loads(a.register.read_text()),a.output,a.require_complete)
    print(json.dumps(dict(findings=issues),indent=2))
    if issues:raise SystemExit(1)

if __name__=='__main__':main()
