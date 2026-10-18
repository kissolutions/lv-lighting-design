"""Mandatory M3 sequence-assignment validation build using external KIS IECC rules.

This is the controlled entrypoint for SEQ/PSEQ assignments after initial selection,
and for ad hoc code-edition revalidation. Never edits the underlying SEQ library,
the canonical project schema, or owner approval decisions.
"""
import argparse
import json
from pathlib import Path
from .sequence_code_validate import validate


def build(model,companion,catalog,code_basis,space_contexts,standard_sequences=None,prior=None):
    if model.get('project',{}).get('id')!=companion.get('project_id'):
        raise ValueError('M3 companion project identity mismatch')
    if model.get('project',{}).get('model_revision')!=companion.get('model_revision'):
        raise ValueError('M3 companion revision mismatch')
    space_ids={s['id'] for s in model.get('spaces',[])}
    zones={z['id']:z for z in model.get('light_zones',[])}
    parents={z['parent_zone_id'] for z in zones.values() if z.get('parent_zone_id')}
    defs={(d['id'],d['revision']):d for d in companion.get('project_sequences',[])}
    defs.update({(d['id'],d['revision']):d for d in (standard_sequences or [])})
    previous={r['endpoint_zone_id']:r for r in (prior or {}).get('results',[])}
    results=[];issues=[]
    for assignment in companion.get('assignments',[]):
        zid=assignment['endpoint_zone_id']
        if zid not in zones or zid in parents:
            issues.append(dict(zone=zid,error='Unknown or parent zone cannot execute a sequence'))
            continue
        if zid not in space_contexts:
            issues.append(dict(zone=zid,error='Missing per-endpoint Space, code, daylight and exceptions context'))
            continue
        context=space_contexts[zid]
        sid=context.get('space_id')
        if sid not in space_ids:
            issues.append(dict(zone=zid,error='Unrecognized Space context ID'))
            continue
        definition=defs.get((assignment['sequence_id'],assignment['sequence_revision']))
        if definition is None:
            issues.append(dict(zone=zid,error='Unresolved or unavailable pinned SEQ definition'))
            continue
        parameters=dict(assignment.get('parameters') or {})
        defined_scheme=definition.get('functions',{}).get('dimming_scheme')
        override=assignment.get('dimming_scheme_override')
        scheme=override or defined_scheme
        if scheme in ('continuous','stepped','none'):
            if 'dimming_scheme' in parameters and parameters['dimming_scheme']!=scheme:
                issues.append(dict(zone=zid,error='Dimming assignment parameter conflicts with SEQ definition/approved override'))
                continue
            parameters['dimming_scheme']=scheme
        result=validate(catalog,code_basis,context,
            dict(endpoint_zone_id=zid,sequence_id=assignment['sequence_id'],
              sequence_revision=assignment['sequence_revision'],parameters=parameters),
            previous.get(zid))
        result['space_id']=sid
        results.append(result)
    status='conflict' if issues or any(r['status']=='conflict' for r in results) else (
      'needs_review' if not results or any(r['status']!='rule_checks_passed' for r in results) else 'rule_checks_passed')
    return dict(process_id='PROC-SEQ-VALIDATE',process_revision='0.1.0',
      project_id=companion['project_id'],model_revision=companion['model_revision'],
      catalog_revision=catalog['revision'],code_basis=code_basis,status=status,
      blocking_integration_issues=issues,results=results,
      sequence_library_modified=False,canonical_model_modified=False,
      project_assignments_modified=False,compliance_certified=False)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('model',type=Path);p.add_argument('m3_companion',type=Path)
    p.add_argument('rule_catalog',type=Path);p.add_argument('validation_context',type=Path)
    p.add_argument('new_output_file',type=Path)
    p.add_argument('--standard-sequences',type=Path)
    p.add_argument('--prior-result',type=Path)
    p.add_argument('--require-resolved',action='store_true',
        help='Fail on any unresolved/conflict finding; only qualifying rules can yield rule_checks_passed')
    a=p.parse_args()
    read=lambda path:json.loads(path.read_text())
    inp=read(a.validation_context)
    result=build(read(a.model),read(a.m3_companion),read(a.rule_catalog),
       inp['code_basis'],inp['endpoint_contexts'],
       read(a.standard_sequences) if a.standard_sequences else [],
       read(a.prior_result) if a.prior_result else None)
    if a.new_output_file.exists():raise SystemExit('Do not overwrite previous validation report')
    a.new_output_file.parent.mkdir(parents=True,exist_ok=True)
    a.new_output_file.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status=result['status'],endpoints=len(result['results']),
       unresolved_or_conflicting=sum(r['status']!='rule_checks_passed' for r in result['results']),
       integration_issues=len(result['blocking_integration_issues'])),indent=2))
    if a.require_resolved and result['status']!='rule_checks_passed':raise SystemExit(1)


if __name__=='__main__':main()
