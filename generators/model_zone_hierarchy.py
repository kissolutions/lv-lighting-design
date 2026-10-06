"""v0.7 zone hierarchy: preserve leaf ownership and derive parent membership."""
import copy
import json
from collections import Counter, defaultdict
from pathlib import Path
from jsonschema import Draft202012Validator

SCHEMA=Path(__file__).resolve().parents[1]/'schemas/lighting-project-v0.7.schema.json'


def upgrade_v07(model):
    from .model_intake import upgrade_v06
    value=copy.deepcopy(model)
    if value.get('schema_version')!='0.6.0':value=upgrade_v06(value)
    value['schema_version']='0.7.0'
    value['project']['controls_narrative_review']=dict(status='unreviewed',decision_id=None)
    for zone in value['light_zones']:zone['parent_zone_id']=None
    return value


def hierarchy_projection(model):
    issues=[]
    def fail(owner,message):issues.append(dict(rule='zone-hierarchy',entity_id=owner,message=message))
    for error in Draft202012Validator(json.loads(SCHEMA.read_text())).iter_errors(model):
        issues.append(dict(rule='schema',entity_id='/'.join(map(str,error.path)),message=error.message))
    if issues:return None,{},issues
    def record_ids(value):
        if isinstance(value,dict):
            if 'id' in value: yield value['id']
            for child in value.values(): yield from record_ids(child)
        elif isinstance(value,list):
            for child in value: yield from record_ids(child)
    for identifier,count in Counter(record_ids(model)).items():
        if count>1:fail(identifier,'An ID has more than one authoritative record.')
    zones={z['id']:z for z in model['light_zones']}
    if len(zones)!=len(model['light_zones']):fail('zones','Duplicate zone IDs.')
    children=defaultdict(list)
    for zone in zones.values():
        pid=zone['parent_zone_id']
        if pid is not None:
            if pid not in zones:fail(zone['id'],'Unknown parent zone.')
            else:children[pid].append(zone['id'])
        trail=set();cursor=zone['id']
        while cursor in zones:
            if cursor in trail:fail(zone['id'],'Zone parent cycle.');break
            trail.add(cursor);cursor=zones[cursor]['parent_zone_id']
    parents=set(children)
    channel_ids={c['light_zone_id'] for b in model['branch_circuits'] for u in b['power_units'] for c in u['channels'] if c['light_zone_id'] is not None}
    refs={r['id'] for r in model['source_references']};decisions={r['id']:r for r in model['decisions']}
    controllers={r['id'] for r in model['controllers']};groups={r['id'] for r in model['control_groups']}
    for zone in zones.values():
        owner=zone['id']
        for ref in zone['source_ref_ids']:
            if ref not in refs:fail(owner,'Unknown source reference.')
        if zone['decision_id'] is not None and zone['decision_id'] not in decisions:fail(owner,'Unknown zone decision.')
        if zone['controller_id'] is not None and zone['controller_id'] not in controllers:fail(owner,'Unknown controller.')
        if any(g not in groups for g in zone['control_group_ids']):fail(owner,'Unknown source control group.')
        if owner in parents:
            if zone['light_object_ids']:fail(owner,'Parent lighting membership is derived; do not duplicate child lights.')
            if owner in channel_ids or zone['controller_id'] is not None or zone['controller_output'] is not None:fail(owner,'Assign physical outputs to leaf zones, not parent containers.')
            if zone['label_mode']!='named':fail(owner,'Parent zones require an explicit name.')
    for space in model['spaces']:
        if any(zid not in zones for zid in space['light_zone_ids']):fail(space['id'],'Unknown declared zone.')
    review=model['project']['controls_narrative_review']
    if review['decision_id'] is not None and review['decision_id'] not in decisions:fail('narrative','Unknown narrative review decision.')
    if review['status']=='locked':
        decision=decisions.get(review['decision_id'])
        if not decision or decision['status']!='confirmed':fail('narrative','Locked narrative requires a confirmed owner-review decision.')
        if any(not z.get('control_narrative') for z in zones.values()):fail('narrative','Locked narrative requires recorded behavior for each zone.')
    if issues:return None,{},issues
    membership={}
    def lights(zid):
        if zid not in membership:
            membership[zid]=sorted(set(zones[zid]['light_object_ids']).union(*(set(lights(c)) for c in children[zid])))
        return membership[zid]
    for zid in zones:lights(zid)
    projected=copy.deepcopy(model);projected['schema_version']='0.6.0';projected['project'].pop('controls_narrative_review')
    projected['light_zones']=[z for z in projected['light_zones'] if z['id'] not in parents]
    for zone in projected['light_zones']:
        for field in ('parent_zone_id','control_narrative','occupancy_aggregation'):zone.pop(field,None)
    for space in projected['spaces']:space['light_zone_ids']=[z for z in space['light_zone_ids'] if z not in parents]
    return projected,dict(zone_children=dict(children),zone_derived_light_ids=membership,parent_zone_ids=sorted(parents)),issues


def check_v07(model,phase='intake'):
    from .model_intake import check_model
    projected,derived,issues=hierarchy_projection(model)
    if issues:return dict(checks_pass=False,phase=phase,issues=issues,deferred_issues=[],derived=None,review_note='Resolve hierarchy/contract issues before downstream checks.')
    report=check_model(projected,phase)
    if report['derived'] is not None:report['derived'].update(derived)
    return report
