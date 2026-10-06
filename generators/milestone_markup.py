"""Milestone review tables, printable schedule sheets and markup conventions.

Does not place PDF annotations or establish actual PDF layer/readback compatibility.
"""
import argparse
import csv
import html
import json
from decimal import Decimal, ROUND_CEILING
from pathlib import Path
from collections import defaultdict
from jsonschema import Draft202012Validator
from .model_hierarchy import load_watts
from .model_intake import check_model
from .validate_model import read_model

ROOT=Path(__file__).resolve().parents[1]
LAYERS=('rooms','lights','zones','lv_channels','controllers','cabling')
PACKAGES=('room_boundaries','lighting_takeoff','zones_room_devices','micro_channels','equipment','coordinated')
TITLES=('Room Boundaries','Lighting Takeoff','Lighting Zones and Room Devices','Micro LV Channels','Controller and Power Equipment','Coordinated System')
LAYER_FOR={'space':'rooms','light':'lights','zone':'zones','channel':'lv_channels','device':'controllers','route':'cabling'}


def calculated_label(value):
    """Ceiling display only. No rounding of model, capacities or source values."""
    if value is None:return ''
    number=Decimal(str(value))
    if not number.is_finite():raise ValueError('Calculated label must be finite.')
    return str(number.to_integral_value(rounding=ROUND_CEILING))


def render_order(operations):
    """Final pass draws every text label after lines/shapes, stably."""
    return sorted(operations,key=lambda op:op.get('kind')=='text')


def boundary_style(enveloped):return 'dashed' if enveloped else 'solid'


def validate_manifest(manifest,model,topology=None):
    schema=json.loads((ROOT/'schemas/milestone-markup-v1.schema.json').read_text())
    issues=[]
    def fail(owner,message):issues.append(dict(rule='markup-review',entity_id=owner,message=message))
    for error in Draft202012Validator(schema).iter_errors(manifest):fail('/'.join(map(str,error.path)),error.message)
    if issues:return issues
    if manifest['project_id']!=model['project']['id']:fail('project','Markup project ID differs from model.')
    if manifest['model_revision']!=model['project']['model_revision']:fail('revision','Markup model revision differs from paired model.')
    channels={c['id'] for b in model['branch_circuits'] for u in b['power_units'] for c in u['channels']}
    sets=dict(space={s['id'] for s in model['spaces']},light={l['id'] for l in model['light_objects']},zone={z['id'] for z in model['light_zones']},channel=channels,device={d['id'] for d in (topology or {}).get('devices',[])},route={r['id'] for r in (topology or {}).get('routes',[])})
    pages={p['id']:p for p in model['drawing_pages']};anns={}
    for a in manifest['annotations']:
        owner=a['annotation_id']
        if owner in anns:fail(owner,'Duplicate annotation identity.')
        anns[owner]=a
        if a['entity_id'] not in sets[a['entity_type']]:fail(owner,'Unknown entity reference.')
        if a['layer']!=LAYER_FOR[a['entity_type']]:fail(owner,'Entity is on incorrect final layer.')
        page=pages.get(a['drawing_page_id'])
        if page is None:fail(owner,'Unknown drawing page.')
        if (a['x_pt'] is None)!=(a['y_pt'] is None):fail(owner,'Position requires both coordinates.')
        if page and a['x_pt'] is not None and (a['x_pt']>page['width_pt'] or a['y_pt']>page['height_pt']):fail(owner,'Position is outside displayed page bounds.')
        if any(s not in sets['space'] for s in a['room_ids']) or any(z not in sets['zone'] for z in a['zone_ids']):fail(owner,'Unknown room/zone association.')
        if a['entity_type'] in ('zone','channel') and a['enveloped'] and a['boundary_style']!='dashed':fail(owner,'Enveloped boundary must be dashed.')
        if a['entity_type']=='device' and not a['display_tag']:fail(owner,'Device requires visible identifying tag.')
        if a['review_status']=='accepted' and a['entity_type']=='device' and a['location_basis'] in ('room_center_provisional','reasonable_equipment_proposal'):fail(owner,'Accepted device placement must record owner-returned location basis.')
    pkg_ids=set()
    locked=model['project'].get('controls_narrative_review',{}).get('status')=='locked'
    for p in manifest['packages']:
        if p['id'] in pkg_ids:fail(p['id'],'Duplicate package ID.')
        pkg_ids.add(p['id'])
        if p['kind'] in PACKAGES[2:] and p['review_status']!='draft' and not locked:fail(p['id'],'Narrative must be locked before dependent device/channel reviews.')
        for pid in p['plan_page_ids']:
            if pid not in pages:fail(p['id'],'Unknown plan page.')
        for aid in p['annotation_ids']:
            if aid not in anns:fail(p['id'],'Unknown annotation ID.')
        if p['review_status']=='accepted' and (not p['pdf_filename'] or not p['edit_save_readback_verified']):fail(p['id'],'Accepted markup requires PDF identity and verified edit/save/readback.')
        if p['kind']=='micro_channels' and any(anns.get(a,{}).get('entity_type')=='device' for a in p['annotation_ids']):fail(p['id'],'Micro-channel review map excludes devices.')
    return issues


def schedules(model,topology=None):
    """Model facts stay unrounded; calculated output cells use ceiling labels."""
    topology=topology or {};spaces={s['id']:s for s in model['spaces']}
    lights={l['id']:l for l in model['light_objects']};zones={z['id']:z for z in model['light_zones']}
    room_for={lid:s for s in spaces.values() for lid in s['light_object_ids']}
    zone_for={lid:z['id'] for z in zones.values() for lid in z['light_object_ids']}
    children=defaultdict(list)
    for z in zones.values():
        if z.get('parent_zone_id'):children[z['parent_zone_id']].append(z['id'])
    def members(zid,trail=None):
        trail=set() if trail is None else trail
        if zid in trail:raise ValueError('Zone parent cycle.')
        return set(zones[zid]['light_object_ids']).union(*(members(c,trail|{zid}) for c in children[zid]))
    def room_names(sids):return '; '.join(spaces[s]['name'] for s in sids if s in spaces)
    rows={}
    rows['rooms']=[dict(room_id=s['id'],room_tag=s.get('room_number'),room_name=s['name'],level=s.get('level'),area_sq_ft=(calculated_label(s['area_sq_ft']) if s['area_basis'] in ('measured','estimated') else s['area_sq_ft']),area_basis=s['area_basis'],notes=s.get('area_note') or s.get('description')) for s in spaces.values()]
    rows['fixtures']=[];rows['light_points_by_type']=[]
    for t in model['fixture_types']:
        ids=[l['id'] for l in lights.values() if l['source']['fixture_type_id']==t['id']]
        rows['fixtures'].append(dict(fixture_type_id=t['id'],source_mark=t['source_mark'],description=t['description'],source_watts=t['source_load']['watts'],load_basis=t['source_load']['basis'],light_point_count=len(ids)))
        for lid in ids:
            l=lights[lid];room=room_for.get(lid,{})
            rows['light_points_by_type'].append(dict(fixture_type_id=t['id'],source_mark=t['source_mark'],light_point_id=lid,display_label=l.get('label'),room_id=room.get('id'),room_name=room.get('name'),source_page_id=l['source']['drawing_page_id']))
    rows['zones']=[]
    for z in zones.values():
        ids=members(z['id']);sids=sorted({room_for[l]['id'] for l in ids if l in room_for})
        rows['zones'].append(dict(zone_id=z['id'],name=z.get('label') or room_names(sids),parent_zone_id=z.get('parent_zone_id'),child_zone_ids='; '.join(children[z['id']]),room_ids='; '.join(sids),room_names=room_names(sids),light_ids='; '.join(sorted(ids)),occupancy_aggregation=z.get('occupancy_aggregation'),narrative=z.get('control_narrative')))
    connections={c['device_id']:c for c in topology.get('control_connections',[])}
    rows['room_devices']=[];rows['equipment']=[]
    for d in topology.get('devices',[]):
        room=spaces.get(d.get('room_id'),{});c=connections.get(d['id'],{})
        row=dict(device_id=d['id'],tag=d.get('display_tag',d['id']),name=d.get('name',d['kind']),room_id=d.get('room_id'),room_name=room.get('name'),zone_ids='; '.join(c.get('control_zone_ids',[])),micro_channel_ids='; '.join(c.get('micro_channel_ids',[])),model=d.get('model'),location_status=d['location']['owner_review'])
        row['narrative_function']=d.get('rationale') if d.get('review_category')=='room_device' or d['kind'] in ('sensor','wall_controller','wall_dimmer') else None
        category=d.get('review_category', 'room_device' if d['kind'] in ('sensor','wall_controller','wall_dimmer') else 'equipment')
        rows['room_devices' if category=='room_device' else 'equipment'].append(row)
    assigned={a['micro_channel_id']:a for a in topology.get('channel_assignments',[])};devices={d['id']:d for d in topology.get('devices',[])}
    rows['micro_channels']=[]
    for branch in model['branch_circuits']:
        for unit in branch['power_units']:
            for c in unit['channels']:
                ml=[l for l in lights.values() if l['design']['channel_id']==c['id']]
                loads=[load_watts(l['design']['load']) for l in ml]
                aux=c['auxiliary_load_watts']
                watts=None if aux is None or any(w is None for w in loads) else sum(loads,Decimal(str(aux)))
                a=assigned.get(c['id']);tag=c['id'] if not a else devices[a['device_id']].get('display_tag',a['device_id'])+':CH'+str(a['output'])
                rows['micro_channels'].append(dict(micro_channel_id=c['id'],display_channel=tag,zone_id=c.get('light_zone_id'),connected_watts=calculated_label(watts),light_point_ids='; '.join(l['id'] for l in ml)))
    rows['cabling']=[dict(route_id=r['id'],network=r['network'],device_string='; '.join(r['device_ids']),length_ft=calculated_label(r['length_ft']),cio_id=r['cio_id'],spec_verified=r['spec_verified']) for r in topology.get('routes',[])]
    return rows


def export_schedules(model,topology,output_dir,through=2):
    if through not in range(1,7):raise ValueError('through must be 1–6.')
    report=check_model(model,'inventory' if through==1 else 'intake')
    if report['derived'] is None:raise ValueError('Resolve structural/reference/membership errors before export.')
    if through>=3 and model['project'].get('controls_narrative_review',{}).get('status')!='locked':raise ValueError('Lock the approved control narrative before device review.')
    if topology:
        from .validate_topology import validate
        issues,_=validate(topology,model)
        if issues:raise ValueError('Resolve topology contract/assignment issues before export: '+json.dumps(issues))
    output=Path(output_dir)
    if output.exists() and any(output.iterdir()):raise ValueError('Choose empty output directory for this revision.')
    output.mkdir(parents=True,exist_ok=True);tables=schedules(model,topology)
    content_groups=[('rooms',),('fixtures','light_points_by_type'),('zones','room_devices'),('micro_channels',),('equipment',),tuple(tables)]
    selected=set(k for group in content_groups[:through] for k in group)
    def cell(value):return '' if value is None else str(value)
    for key in selected:
        table=tables[key];fields=list(table[0]) if table else ['status']
        with (output/(key+'.csv')).open('w',newline='') as f:
            writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader();writer.writerows(table)
    for i,group in enumerate(content_groups[:through]):
        parts=['<!doctype html><html><head><meta charset="utf-8"><style>@page{size:landscape;margin:0.4in}body{font:10pt Arial}table{width:100%;border-collapse:collapse;overflow-wrap:anywhere}th,td{border:1px solid #999;padding:4px;text-align:left}thead{display:table-header-group}tr{break-inside:avoid}section+section{break-before:page}h1{font-size:18pt}</style></head><body>']
        parts.append('<h1>'+TITLES[i]+'</h1><p>'+html.escape(model['project']['name'])+' — '+html.escape(model['project']['model_revision'])+' — REVIEW SCHEDULES / PLAN MARKUP TO FOLLOW</p>')
        for key in group:
            rows=tables[key];parts.append('<section><h2>'+html.escape(key.replace('_',' ').title())+'</h2>')
            if rows:
                fields=list(rows[0]);parts.append('<table><thead><tr>'+''.join('<th>'+html.escape(k)+'</th>' for k in fields)+'</tr></thead><tbody>')
                for row in rows:parts.append('<tr>'+''.join('<td>'+html.escape(cell(row[k]))+'</td>' for k in fields)+'</tr>')
                parts.append('</tbody></table>')
            else:parts.append('<p>No entries recorded at this milestone; verify completeness.</p>')
            parts.append('</section>')
        parts.append('</body></html>');(output/(f'{i+1:02d}_'+PACKAGES[i]+'.html')).write_text(''.join(parts))
    (output/'schedule_export_report.json').write_text(json.dumps(dict(project_id=model['project']['id'],model_revision=model['project']['model_revision'],through=through,phase_checks_pass=report['checks_pass'],phase_issues=report['issues'],pdf_markup_generated=False,pdf_edit_readback_verified=False),indent=2)+'\n')


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('model',type=Path);p.add_argument('output',type=Path);p.add_argument('--topology',type=Path);p.add_argument('--through',type=int,default=2)
    a=p.parse_args();export_schedules(read_model(a.model),json.loads(a.topology.read_text()) if a.topology else None,a.output,a.through)



def reconcile_annotation_return(previous,returned):
    """Reject identity/association loss before adopting owner-returned geometry."""
    old={a['annotation_id']:a for a in previous['annotations']}
    new={a['annotation_id']:a for a in returned['annotations']}
    if len(new)!=len(returned['annotations']) or set(old)!=set(new):
        raise ValueError('Returned annotations lost, duplicated or replaced stable IDs; reconcile explicitly.')
    for aid,a in old.items():
        for field in ('entity_type','entity_id','room_ids','zone_ids'):
            if a[field]!=new[aid][field]:raise ValueError('Returned identity/control association changed; explicit review required: '+aid)
    return returned


if __name__=='__main__':main()
