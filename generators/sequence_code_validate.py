"""Independent, repeatable IECC lighting sequence code-validation micro-process.

Consumes external versioned rules and existing effective sequence assignment
parameters. Never rewrites library SEQ definitions, canonical model, or owner
approvals. Outputs proposed missing values, conflicts, evidence and revision
comparisons. Provisional/secondary-only rule evidence cannot yield code-qualified.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path

PROCESS_ID='PROC-SEQ-VALIDATE'
PROCESS_REV='0.2.0'
PASS='passed'; FAIL='conflict'; PENDING='needs_review'


def _hash(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()


_APPLICABILITY_KEYS = {'specific_application_types','space_types','min_area_sq_ft',
    'max_area_exclusive_sq_ft','max_area_sq_ft','enclosed_full_height',
    'daylight_control_required','special_application','high_end_trim_exception',
    'requires_no_compliant_occupancy_control','specific_application'}


def _area(context):
    value=context.get('area_sq_ft')
    if not isinstance(value,(int,float)) or isinstance(value,bool):return None
    return value if math.isfinite(value) and value>=0 else None


def _revision(value):
    parts=str(value).split('.')
    if len(parts)!=3 or not all(p.isdigit() for p in parts):
        raise ValueError('Expected a numeric three-part process revision')
    return tuple(int(p) for p in parts)


def applicability(rule,context):
    """True / False / None. Never interpret missing evidence as 'does not apply'."""
    c=rule['applies'];tests=[]
    unknown=set(c)-_APPLICABILITY_KEYS
    if unknown:raise ValueError('Unsupported rule applicability keys: '+', '.join(sorted(unknown)))
    if 'specific_application' in c:
        n=context.get('specific_application')
        tests.append(None if not isinstance(n,bool) else n==c['specific_application'])
    if 'specific_application_types' in c:
        typ=context.get('specific_application_type')
        tests.append(None if typ is None else typ in c['specific_application_types'])
    if 'space_types' in c:
        typ=context.get('space_type')
        tests.append(None if typ is None else typ in c['space_types'])
    if 'min_area_sq_ft' in c:
        n=_area(context)
        tests.append(None if n is None else n>=c['min_area_sq_ft'])
    if 'max_area_exclusive_sq_ft' in c:
        n=_area(context)
        tests.append(None if n is None else n<c['max_area_exclusive_sq_ft'])
    if 'max_area_sq_ft' in c:
        n=_area(context)
        tests.append(None if n is None else n<=c['max_area_sq_ft'])
    if 'enclosed_full_height' in c:
        n=context.get('enclosed_full_height')
        tests.append(None if not isinstance(n,bool) else n==c['enclosed_full_height'])
    if 'daylight_control_required' in c:
        n=context.get('daylight_control_required')
        tests.append(None if n is None else n==c['daylight_control_required'])
    if 'special_application' in c:
        n=context.get('special_application')
        tests.append(None if n is None else n==c['special_application'])
    if 'high_end_trim_exception' in c:
        n=context.get('high_end_trim_exception')
        tests.append(None if n is None else n==c['high_end_trim_exception'])
    if 'requires_no_compliant_occupancy_control' in c:
        n=context.get('compliant_occupancy_control')
        tests.append(None if n is None else n is False)
    if False in tests:return False
    if None in tests:return None
    return True


def check(actual,req):
    """None is an unknown, never an automatically passing/complying setting."""
    if actual is None:return PENDING
    op=req['op'];v=req['value']
    try:
        if op=='eq':return PASS if type(actual)==type(v) and actual==v else FAIL
        if op=='max':return PASS if isinstance(actual,(int,float)) and not isinstance(actual,bool) and actual<=v else FAIL
        if op=='min':return PASS if isinstance(actual,(int,float)) and not isinstance(actual,bool) and actual>=v else FAIL
        if op=='one_of':return PASS if actual in v else FAIL
    except (TypeError,ValueError):return FAIL
    raise ValueError('Unrecognized operator '+str(op))


def validate(catalog,code_basis,context,sequence_assignment,prior=None):
    """Single endpoint validation; multiple independently callable runs supported."""
    if catalog.get('revision') is None or not isinstance(catalog.get('rules'),list):
        raise ValueError('Versioned rule catalog required')
    minimum=catalog.get('minimum_process_revision')
    if minimum is not None and _revision(PROCESS_REV)<_revision(minimum):
        raise ValueError('Rule catalog requires newer process revision '+str(minimum))
    if code_basis.get('standard')!='IECC' or str(code_basis.get('edition')) not in ('2021','2024'):
        raise ValueError('Only IECC 2021 and 2024 implemented. No silent fallback.')
    if code_basis.get('compliance_path')!='prescriptive':
        raise ValueError('Only reviewed IECC prescriptive path supported. ASHRAE/LLLC paths require their own rules.')
    if not sequence_assignment.get('endpoint_zone_id') or not sequence_assignment.get('sequence_id'):
        raise ValueError('Endpoint and selected SEQ/PSEQ required')
    edition=str(code_basis['edition']);values=sequence_assignment.get('parameters') or {}
    if not isinstance(values,dict):raise ValueError('Assignment parameters must be a dictionary')
    findings=[];proposals={};applicable=[];skipped=[];unresolved_rules=[]
    for rule in catalog['rules']:
        if rule['edition']!=edition:continue
        state=applicability(rule,context)
        if state is False:
            skipped.append(rule['id']);continue
        if state is None:
            unresolved_rules.append(rule['id'])
            findings.append(dict(rule_id=rule['id'],status=PENDING,reason='Rule applicability unresolved: required Space/exception facts not established',section=rule['section'],sources=rule['source_urls']))
            continue
        applicable.append(rule['id'])
        if rule['verification']!='primary_text_reviewed':
            findings.append(dict(rule_id=rule['id'],status=PENDING,reason='Rule source not yet verified against final unamended primary model code',section=rule['section'],sources=rule['source_urls']))
        for req in rule['requirements']:
            key=req['key'];actual=values.get(key)
            if req.get('allow_alternative') and values.get(req['allow_alternative']) is True:
                continue
            result=check(actual,req)
            if result==PENDING:
                if req['op']=='eq':
                    # Proposal ONLY. Never modify original assignment or qualify it from a proposal.
                    if key not in proposals:proposals[key]=dict(proposed_value=req['value'],based_on=[rule['id']])
                    elif proposals[key]['proposed_value']==req['value']:proposals[key]['based_on'].append(rule['id'])
                    else:
                        findings.append(dict(rule_id=rule['id'],status=FAIL,parameter=key,reason='Conflicting rule-derived proposals',section=rule['section'],sources=rule['source_urls']))
                findings.append(dict(rule_id=rule['id'],status=PENDING,parameter=key,
                    reason='Required design parameter missing; proposal requires reviewed acceptance',required=req,section=rule['section'],sources=rule['source_urls']))
            elif result==FAIL:
                if req.get('allow_alternative') and values.get(req['allow_alternative']) is True:
                    continue
                findings.append(dict(rule_id=rule['id'],status=FAIL,parameter=key,
                    reason='Selected effective sequence parameter conflicts with applicable code rule',actual=actual,required=req,section=rule['section'],sources=rule['source_urls']))
    if code_basis.get('applicability_status')!='confirmed' or not code_basis.get('adoption_evidence'):
        findings.append(dict(rule_id='REGULATORY-BASIS',status=PENDING,
            reason='Code edition/jurisdiction/adoption evidence not confirmed; assumptions cannot qualify a sequence'))
    if code_basis.get('amendments_reviewed') is not True or code_basis.get('exceptions_reviewed') is not True:
        findings.append(dict(rule_id='JURISDICTION-EXCEPTIONS',status=PENDING,
            reason='Jurisdiction amendments and applicable exceptions need documented review'))
    if not applicable and not unresolved_rules:
        findings.append(dict(rule_id='COVERAGE',status=PENDING,
            reason='No rule matched; catalog is partial and cannot certify this endpoint'))
    if any(f['status']==FAIL for f in findings):status='conflict'
    elif findings:status='needs_review'
    else:status='rule_checks_passed'
    result=dict(process_id=PROCESS_ID,process_revision=PROCESS_REV,
      catalog_id=catalog.get('catalog_id'),catalog_revision=catalog['revision'],
      input_fingerprint=_hash(dict(code_basis=code_basis,context=context,assignment=sequence_assignment,catalog_revision=catalog['revision'])),
      code_basis=dict(code_basis),endpoint_zone_id=sequence_assignment['endpoint_zone_id'],
      sequence_id=sequence_assignment['sequence_id'],sequence_revision=sequence_assignment.get('sequence_revision'),
      status=status,applied_rules=applicable,skipped_rules=skipped,unresolved_rules=unresolved_rules,
      effective_parameters=dict(values),proposed_missing_parameters=proposals,findings=findings,
      compliance_certified=False,assignment_modified=False)
    if prior is not None:
        if prior.get('endpoint_zone_id')!=result['endpoint_zone_id']:
            raise ValueError('Prior result belongs to another endpoint')
        old={(f.get('rule_id'),f.get('parameter'),f.get('status')) for f in prior.get('findings',[])}
        new={(f.get('rule_id'),f.get('parameter'),f.get('status')) for f in findings}
        result['delta']=dict(previous_code=prior.get('code_basis'),
          new_findings=[list(k) for k in sorted(new-old,key=str)],
          resolved_findings=[list(k) for k in sorted(old-new,key=str)],
          prior_run_input_fingerprint=prior.get('input_fingerprint'))
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('rule_catalog',type=Path)
    p.add_argument('project_context',type=Path,help='JSON: code_basis, space_context, sequence_assignment')
    p.add_argument('output_json',type=Path)
    p.add_argument('--prior-result',type=Path)
    a=p.parse_args()
    data=json.loads(a.project_context.read_text())
    previous=json.loads(a.prior_result.read_text()) if a.prior_result else None
    result=validate(json.loads(a.rule_catalog.read_text()),data['code_basis'],
        data['space_context'],data['sequence_assignment'],previous)
    if a.output_json.exists():raise SystemExit('Choose a new output path; preserve previous results')
    a.output_json.parent.mkdir(parents=True,exist_ok=True)
    a.output_json.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status=result['status'],findings=len(result['findings']),
        proposed_parameters=result['proposed_missing_parameters']),indent=2))


if __name__=='__main__':main()
