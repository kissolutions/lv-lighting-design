"""v0.8 source identity and owner section-count metadata; no geometry inference."""
import copy
import json
from pathlib import Path
from jsonschema import Draft202012Validator

SCHEMA = Path(__file__).resolve().parents[1] / 'schemas/lighting-project-v0.8.schema.json'


def upgrade_v08(model):
    from .model_zone_hierarchy import upgrade_v07
    value = copy.deepcopy(model)
    if value.get('schema_version') == '0.8.0':
        return value
    if value.get('schema_version') != '0.7.0':
        value = upgrade_v07(value)
    value['schema_version'] = '0.8.0'
    for space in value['spaces']:
        space['nested_in'] = None
    for light in value['light_objects']:
        light.update(assembly_id=None, count_basis='unknown', count_decision_id=None)
        light['source'].update(source_tag=None, schedule_match_status='unknown')
    for fixture in value['fixture_types']:
        fixture['schedule_presence'] = 'unknown'
    return value


def check_v08(model, phase='intake'):
    from .model_intake import check_model
    issues = [dict(rule='schema', entity_id='/'.join(map(str,e.path)), message=e.message)
              for e in Draft202012Validator(json.loads(SCHEMA.read_text())).iter_errors(model)]
    def fail(owner, message):
        issues.append(dict(rule='intake-review', entity_id=owner, message=message))
    if not issues:
        spaces = {s['id']:s for s in model['spaces']}
        decisions = {d['id']:d for d in model['decisions']}
        types = {t['id']:t for t in model['fixture_types']}
        for s in spaces.values():
            host = s['nested_in']
            if host is not None:
                if host not in spaces or host == s['id']:
                    fail(s['id'], 'Nested host must reference another Space.')
                elif s.get('level') is None or s.get('level') != spaces[host].get('level'):
                    fail(s['id'], 'Nesting requires the same known served level.')
            trail=set(); cursor=s['id']
            while cursor in spaces:
                if cursor in trail:
                    fail(s['id'], 'Nested Space cycle.'); break
                trail.add(cursor); cursor=spaces[cursor]['nested_in']
        for light in model['light_objects']:
            decision=decisions.get(light['count_decision_id'])
            if light['count_decision_id'] is not None and decision is None:
                fail(light['id'], 'Unknown count decision.')
            if light['count_basis']=='physical_section' and (not decision or decision['status']!='confirmed'):
                fail(light['id'], 'Owner section-count override requires a confirmed decision.')
            t=types.get(light['source']['fixture_type_id'])
            if t and t['schedule_presence']=='keynote_only' and light['source']['schedule_match_status']!='not_on_schedule':
                fail(light['id'], 'Keynote-only type must be marked not_on_schedule.')
    if issues:
        return dict(checks_pass=False,phase=phase,issues=issues,deferred_issues=[],derived=None,
                    review_note='Resolve intake metadata references before downstream checks.')
    projected=copy.deepcopy(model); projected['schema_version']='0.7.0'
    for s in projected['spaces']: s.pop('nested_in')
    for l in projected['light_objects']:
        for key in ('assembly_id','count_basis','count_decision_id'): l.pop(key)
        for key in ('source_tag','schedule_match_status'): l['source'].pop(key)
    for t in projected['fixture_types']: t.pop('schedule_presence')
    report=check_model(projected,phase)
    if phase in ('intake','design'):
        for l in model['light_objects']:
            source=l['source']; fixture=types.get(source['fixture_type_id'])
            unexplained=(source['source_tag'] is not None and fixture is not None
                         and source['source_tag']!=fixture['source_mark']
                         and source['schedule_match_status'] not in ('verified','not_on_schedule'))
            if source['schedule_match_status']=='provisional' or unexplained:
                report['issues'].append(dict(rule='schedule-mark-reconciliation',entity_id=l['id'],
                    message='Plan tag to schedule mark remains provisional; do not accept affected counts.'))
        report['checks_pass']=not report['issues']
    return report
