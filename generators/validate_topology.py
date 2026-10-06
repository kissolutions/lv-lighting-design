"""Validate a topology companion paired with the accepted lighting model."""
import argparse
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from jsonschema import Draft202012Validator

SCHEMA = Path(__file__).resolve().parents[1] / 'schemas/controller-power-topology-v1.schema.json'


def validate(topology, model, final=False):
    issues = []
    def fail(rule, owner, message):
        issues.append(dict(rule=rule, entity_id=owner, message=message))
    schema_path = SCHEMA.with_name('controller-power-topology-v1.1.schema.json') if topology.get('topology_version') == '1.1.0' else SCHEMA
    for error in Draft202012Validator(json.loads(schema_path.read_text())).iter_errors(topology):
        fail('topology-schema', '/'.join(map(str, error.path)), error.message)
    if issues:
        return issues, {}
    collections = ('areas', 'devices', 'power_feeds', 'routes', 'open_items')
    seen = set()
    for name in collections:
        for row in topology[name]:
            if row['id'] in seen:
                fail('topology-id', row['id'], 'Duplicate companion ID.')
            seen.add(row['id'])
    devices = {d['id']: d for d in topology['devices']}
    areas = {a['id']: a for a in topology['areas']}
    canonical = {row['id'] for key in ('spaces','controllers','control_devices','control_systems','light_zones','source_references','drawing_pages','decisions') for row in model.get(key, [])}
    spaces = {r['id'] for r in model.get('spaces', [])}
    zones = {r['id'] for r in model.get('light_zones', [])}
    pages = {r['id']: r for r in model.get('drawing_pages', [])}
    refs = {r['id'] for r in model.get('source_references', [])}
    channels = {c['id']: c for b in model.get('branch_circuits', []) for u in b['power_units'] for c in u['channels']}
    canonical.update(channels)
    canonical.update(u['id'] for b in model.get('branch_circuits', []) for u in b['power_units'])
    if topology['project_id'] != model['project']['id']:
        fail('project-link', topology['project_id'], 'Companion and lighting project IDs differ.')
    def reference(owner, value, allowed):
        if value is not None and value not in allowed:
            fail('topology-reference', owner, f'Unknown reference: {value}')
    def evidence(owner, values):
        for value in values: reference(owner, value, refs)
    evidence('AHJ', topology['ahj_source_ref_ids'])
    if final and (topology['ahj'] is None or not topology['ahj_source_ref_ids']):
        fail('early-facts', 'AHJ', 'Confirm AHJ and evidence.')
    for area in areas.values():
        for value in area['space_ids']: reference(area['id'], value, spaces)
        evidence(area['id'], area['source_ref_ids'])
    for d in devices.values():
        owner=d['id']; loc=d['location']
        if 'room_id' in d: reference(owner,d['room_id'],spaces)
        reference(owner, d['canonical_entity_id'], canonical)
        reference(owner, loc['area_id'], areas)
        reference(owner, loc['drawing_page_id'], pages)
        evidence(owner, d['source_ref_ids'])
        coords=(loc['x_pt'],loc['y_pt'])
        if (coords[0] is None) != (coords[1] is None) or (coords[0] is not None and loc['drawing_page_id'] is None):
            fail('location',owner,'Both coordinates require a drawing page.')
        page=pages.get(loc['drawing_page_id'])
        if page and coords[0] is not None and (coords[0]>page['width_pt'] or coords[1]>page['height_pt']):
            fail('location',owner,'Point is outside displayed page bounds.')
        if d['kind'] in ('QDCD','CIO') and loc['mounting']=='above_ceiling':
            area=areas.get(loc['area_id'])
            if area and area['return_air_plenum'] is True:
                fail('plenum',owner,'Selected QDCD/CIO is not plenum rated.')
            if final and (not area or area['return_air_plenum'] is None or not area['source_ref_ids']):
                fail('plenum',owner,'Confirm mounting-area non-plenum status and evidence.')
        if d['kind']=='QDCD' and d['output_count'] not in (4,None):
            fail('qdcd-capacity',owner,'QDCD has four lighting outputs.')
        if d['kind']=='PDU':
            if d['output_count'] not in (8,16,32,None):fail('pdu-capacity',owner,'EPS family is 8/16/32 outputs.')
            if d['output_count']==8 and d['smart'] is True:fail('smart-pdu',owner,'8-output Smart is unavailable.')
        if final and (loc['owner_review']!='accepted' or loc['area_id'] is None or page is None or coords[0] is None):
            fail('owner-location',owner,'Accept and document physical device location.')
        if final and not d['source_ref_ids']:fail('device-evidence',owner,'Confirm device basis.')
    tags=[d['display_tag'] for d in devices.values() if 'display_tag' in d]
    if len(tags)!=len(set(tags)):fail('device-tag','devices','Display tags must be unique.')
    outputs=set(); channel_claims=set(); assigned_watts=defaultdict(float)
    for a in topology['channel_assignments']:
        owner=a['micro_channel_id']; reference(owner,owner,channels);reference(owner,a['device_id'],devices)
        for zid in a['control_zone_ids']:reference(owner,zid,zones)
        if owner in channel_claims:fail('micro-channel-assignment',owner,'Micro channel is assigned more than once.')
        channel_claims.add(owner)
        key=(a['device_id'],a['output'])
        if key in outputs:fail('output-collision',owner,'Output is already assigned.')
        outputs.add(key); d=devices.get(a['device_id'])
        if not d:continue
        if d['kind'] not in ('QDCD','PDU'):fail('output-kind',owner,'Lighting output must belong to QDCD or PDU.')
        if d['output_count'] is not None and a['output']>d['output_count']:fail('output-capacity',owner,'Output exceeds device capacity.')
        if d['kind']=='PDU' and d['smart'] is not True:fail('smart-pdu',d['id'],'Direct PDU-controlled lighting requires Smart.')
        channel=channels.get(owner)
        if channel and channel.get('light_zone_id') and a['control_zone_ids'] != [channel['light_zone_id']]:
            fail('zone-preservation',owner,'Assignment must preserve the designated channel functional zone.')
        if channel and channel.get('controller_id') is not None and (channel['controller_id'],channel.get('controller_output')) != (d['canonical_entity_id'],a['output']):
            fail('canonical-output',owner,'Companion conflicts with existing controller/output assignment.')
        if d['kind']=='QDCD' and a['connected_watts'] is not None and a['connected_watts']>100:
            fail('qdcd-output-watts',owner,'QDCD output exceeds 100 W hardware maximum.')
        if a['connected_watts'] is not None:assigned_watts[d['id']]+=a['connected_watts']
        elif final:fail('output-load',owner,'Confirm connected watts.')
    feed_counts=Counter(); input_claims=set(); pdu_demand=defaultdict(float)
    for f in topology['power_feeds']:
        owner=f['id'];pdu=devices.get(f['pdu_id']);qdcd=devices.get(f['qdcd_id'])
        reference(owner,f['pdu_id'],devices);reference(owner,f['qdcd_id'],devices);evidence(owner,f['source_ref_ids'])
        if not pdu or not qdcd:continue
        if pdu['kind']!='PDU' or qdcd['kind']!='QDCD':fail('feed-kind',owner,'Feed must connect PDU to QDCD.')
        key=(f['pdu_id'],f['pdu_output']);ikey=(f['qdcd_id'],f['qdcd_input'])
        if key in outputs or ikey in input_claims:fail('feed-collision',owner,'PDU output or QDCD input already used.')
        outputs.add(key);input_claims.add(ikey);feed_counts[f['qdcd_id']]+=1
        if pdu['output_count'] is not None and f['pdu_output']>pdu['output_count']:fail('feed-capacity',owner,'PDU output exceeds capacity.')
        if f['demand_watts'] is not None:pdu_demand[f['pdu_id']]+=f['demand_watts']
        if f['rated_watts'] is not None and f['demand_watts'] is not None and f['demand_watts']>f['rated_watts']:fail('feed-watts',owner,'Feed demand exceeds rating.')
        if final and (None in (f['rated_watts'],f['demand_watts']) or not f['source_ref_ids']):fail('feed-evidence',owner,'Confirm feed rating/demand and evidence.')
    exceptions={x['qdcd_id']:x for x in topology['reduced_feed_decisions']}
    for e in topology['reduced_feed_decisions']:
        reference(e['qdcd_id'],e['qdcd_id'],devices);reference(e['qdcd_id'],e['decision_id'],canonical);evidence(e['qdcd_id'],e['source_ref_ids'])
    for d in devices.values():
        owner=d['id']
        if d['kind']=='QDCD':
            count=feed_counts[owner]
            if count>4:fail('feed-count',owner,'At most four feeds.')
            if 0<count<4 and owner not in exceptions:fail('reduced-feed',owner,'One to three feeds requires documented exception.')
            e=exceptions.get(owner)
            if final and (count==0 or (count<4 and (not e or not e['hardware_verified'] or not e['source_ref_ids']))):fail('reduced-feed',owner,'Confirm supply mapping and reduced-feed hardware support.')
            if d['available_input_watts'] is not None and d['connected_demand_watts'] is not None and d['connected_demand_watts']>d['available_input_watts']:fail('input-budget',owner,'QDCD demand exceeds verified available input power.')
            if final and (d['available_input_watts'] is None or d['connected_demand_watts'] is None):fail('input-budget',owner,'Verify input demand including losses/auxiliaries and available power.')
        load=assigned_watts[owner]+pdu_demand[owner]
        if d['kind']=='QDCD' and assigned_watts[owner]>400:fail('qdcd-total-watts',owner,'QDCD lighting output exceeds 400 W hardware maximum.')
        if d['rated_total_watts'] is not None and load>d['rated_total_watts']:fail('aggregate-watts',owner,'Assigned demand exceeds recorded device rating.')
    ports=set(); control_claims=set()
    for c in topology['control_connections']:
        owner=c['device_id'];reference(owner,owner,devices);reference(owner,c['aggregator_id'],devices)
        for name,allowed in (('control_zone_ids',zones),('micro_channel_ids',channels),('qdcd_ids',devices)):
            for value in c[name]:reference(owner,value,allowed)
        if owner in control_claims:fail('control-identity',owner,'Physical device has duplicate connection rows.')
        control_claims.add(owner);d=devices.get(owner); agg=devices.get(c['aggregator_id'])
        if not d:continue
        if d['casambi']:
            if agg or c['input_port'] is not None:fail('wireless-port',owner,'Casambi association does not consume wired aggregator port.')
        elif agg:
            capacity={'SW4':4,'SW8':8,'CIO':8}.get(agg['kind'])
            if capacity is None:fail('sensor-capacity',owner,'Direct wired QDCD/other input capability unconfirmed.')
            if c['input_port'] is None or (capacity and c['input_port']>capacity):fail('sensor-port',owner,'Wired port missing or exceeds capacity.')
            key=(agg['id'],c['input_port'])
            if key in ports:fail('sensor-port',owner,'Wired port already occupied.')
            ports.add(key)
        elif final:fail('sensor-port',owner,'Assign wired device to a verified input.')
    bus_counts=defaultdict(int);bus_current=defaultdict(float);bus_seen=set()
    for b in topology['bus_assignments']:
        owner=b['device_id'];reference(owner,owner,devices);reference(owner,b['cio_id'],devices)
        d=devices.get(owner);cio=devices.get(b['cio_id'])
        if not d or not cio:continue
        if owner in bus_seen:fail('bus-membership',owner,'Device belongs to more than one bus/CIO.')
        bus_seen.add(owner)
        if cio['kind']!='CIO':fail('cio-kind',owner,'Bus root must be CIO.')
        if (b['bus']=='PDnet') != (d['kind']=='QDCD'):fail('bus-kind',owner,'QDCD uses PDnet; peripherals use SDCnet.')
        units=1 if b['bus']=='PDnet' else b['bus_units']
        if units is None:
            if final:fail('bus-count',owner,'Verify bus-device counting.')
        else:bus_counts[(b['cio_id'],b['bus'])]+=units
        if b['bus']=='SDCnet':
            if d['bus_demand_ma'] is not None:bus_current[b['cio_id']]+=d['bus_demand_ma']
            elif final:fail('bus-power',owner,'Verify peripheral current including attached sensors.')
    for (cio,bus),count in bus_counts.items():
        if count>(8 if bus=='PDnet' else 16):fail('bus-capacity',cio,f'{bus} device capacity exceeded.')
    for cio,current in bus_current.items():
        if current>250:fail('bus-power',cio,'Combined SDCnet demand exceeds 250 mA.')
    for r in topology['routes']:
        owner=r['id'];reference(owner,r['cio_id'],devices);reference(owner,r['drawing_page_id'],pages);evidence(owner,r['source_ref_ids'])
        for value in r['device_ids']:reference(owner,value,devices)
        page=pages.get(r['drawing_page_id'])
        if page and any(p['x_pt']>page['width_pt'] or p['y_pt']>page['height_pt'] for p in r['points']):fail('route-location',owner,'Route point outside page.')
        if r['network'] in ('PDnet','SDCnet') and r['distance_from_cio_ft'] is not None and r['distance_from_cio_ft']>250:fail('bus-distance',owner,'Recorded distance from CIO exceeds 250 ft.')
        if final and (not r['spec_verified'] or r['length_ft'] is None or not r['source_ref_ids']):fail('route-spec',owner,'Verify routing and manufacturer length/connection rules.')
    if final:
        for cid in channels:
            if cid not in channel_claims:
                fail('channel-completeness',cid,'Assign each designated micro channel to a physical output.')
        for b in topology['bus_assignments']:
            if not any(r['network']==b['bus'] and r['cio_id']==b['cio_id'] and b['device_id'] in r['device_ids'] for r in topology['routes']):
                fail('route-completeness',b['device_id'],'Document the assigned bus path back to CIO.')
        for d in devices.values():
            if d['kind'] in ('sensor','wall_controller','wall_dimmer') and d['id'] not in control_claims:fail('control-completeness',d['id'],'Missing functional control association.')
            if d['kind'] in ('QDCD','SW4','SW8') and d['id'] not in bus_seen and not (d['kind']=='QDCD' and d['casambi']):fail('bus-completeness',d['id'],'Missing CIO bus assignment.')
        for o in topology['open_items']:
            if o['blocking'] and o['status']=='open':fail('open-item',o['id'],o['description'])
    kinds=Counter(d['kind'] for d in devices.values()); sensors=[d for d in devices.values() if d['kind']=='sensor']
    wired=sum(not d['casambi'] for d in sensors)
    dimming_zones={z['id'] for z in model.get('light_zones',[]) if z.get('driver_type')=='dimming'}
    required_qchannels={cid for cid,c in channels.items() if c.get('light_zone_id') in dimming_zones}
    required_qchannels.update(a['micro_channel_id'] for a in topology['channel_assignments'] if devices.get(a['device_id'],{}).get('kind')=='QDCD')
    qchannels=len(required_qchannels)
    counts=dict(qdcd_output_lower_bound=math.ceil(qchannels/4),wired_sensor_count=wired,casambi_sensor_count=len(sensors)-wired,physical_sensor_count=len(sensors),wall_control_count=kinds['wall_controller']+kinds['wall_dimmer'],sensor_aggregator_global_lower_bound=math.ceil(wired/8),installed_qdcds=kinds['QDCD'],installed_aggregators=kinds['SW4']+kinds['SW8'],installed_cios=kinds['CIO'],installed_pdus=kinds['PDU'])
    return issues, counts


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('topology',type=Path);parser.add_argument('--model',type=Path,required=True);parser.add_argument('--final',action='store_true')
    args=parser.parse_args()
    issues,counts=validate(json.loads(args.topology.read_text()),json.loads(args.model.read_text()),args.final)
    print(json.dumps(dict(checks_pass=not issues,counts=counts,issues=issues),indent=2))
    return bool(issues)

if __name__=='__main__':raise SystemExit(main())
