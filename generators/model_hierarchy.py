"""Draft v0.2 hierarchy checks and derived views. No construction approval implied."""
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from decimal import Decimal
from pathlib import Path

from jsonschema import Draft202012Validator

from .validate_model import read_model

SCHEMA = Path(__file__).resolve().parents[1] / 'schemas/lighting-project-v0.2.schema.json'


def load_watts(load):
    if load['watts'] is None:
        return None
    value = Decimal(str(load['watts']))
    if load['basis'] == 'per_fixture':
        return value
    if load['length_ft'] is None:
        return None
    value *= Decimal(str(load['length_ft']))
    if load['basis'] == 'per_reference_length':
        if load['reference_length_ft'] is None:
            return None
        value /= Decimal(str(load['reference_length_ft']))
    return value


def check_model(model):
    issues = []
    def fail(rule, id, message):
        issues.append({'rule':rule, 'entity_id':id, 'message':message})

    schema = json.loads(SCHEMA.read_text())
    for error in Draft202012Validator(schema).iter_errors(model):
        fail('schema', '/'.join(map(str,error.absolute_path)) or 'model', error.message)
    if issues:
        return {'checks_pass':False, 'issues':issues, 'derived':None}

    branches = model['branch_circuits']
    units = [u for b in branches for u in b['power_units']]
    channels = [c for u in units for c in u['channels']]
    zones = model['light_zones']
    lights = [light for z in zones for light in z['light_objects']]
    emergency_inputs = [i for c in model['controllers'] for i in c['emergency_inputs']]
    collections = {k:model[k] for k in ['source_documents','drawing_pages','source_references','fixture_types',
        'controllers','control_devices','control_systems','control_groups','backup_supplies','decisions','assumptions','open_items']}
    collections.update(branches=branches,units=units,channels=channels,zones=zones,lights=lights,emergency_inputs=emergency_inputs)
    every_id = [model['project']['id']] + [r['id'] for rows in collections.values() for r in rows]
    for id,count in Counter(every_id).items():
        if count > 1:
            fail('unique-ids',id,'An ID may have only one authoritative object/owner.')
    if issues:
        return {'checks_pass':False,'issues':issues,'derived':None}
    indexes = {k:{r['id']:r for r in rows} for k,rows in collections.items()}
    input_owner = {i['id']:c['id'] for c in model['controllers'] for i in c['emergency_inputs']}
    channel_owner = {c['id']:u['id'] for u in units for c in u['channels']}
    unit_owner = {u['id']:b['id'] for b in branches for u in b['power_units']}

    def ref(id,value,collection,nullable=False):
        if nullable and value is None:
            return
        if value not in indexes[collection]:
            fail('reference-integrity',id,f'Missing {collection} reference: {value}')
    for rows in collections.values():
        for row in rows:
            for rid in row.get('source_ref_ids',[]):
                ref(row['id'],rid,'source_references')
            if 'decision_id' in row:
                ref(row['id'],row['decision_id'],'decisions',True)
    for decision in model['decisions']:
        for aid in decision['assumption_ids']:
            ref(decision['id'],aid,'assumptions')
    for p in model['drawing_pages']:
        ref(p['id'],p['source_document_id'],'source_documents')
    for r in model['source_references']:
        ref(r['id'],r['source_document_id'],'source_documents')
        ref(r['id'],r['drawing_page_id'],'drawing_pages',True)
        page=indexes['drawing_pages'].get(r['drawing_page_id'])
        if page and page['source_document_id']!=r['source_document_id']:
            fail('source-traceability',r['id'],'Reference document and page document disagree.')
    for row in branches+units:
        ref(row['id'],row['backup_supply_id'],'backup_supplies',True)
    for u in units:
        for connection in u['connected_controls']:
            target=connection['target_id']
            if not any(target in indexes[k] for k in ['controllers','control_devices','control_systems']):
                fail('reference-integrity',u['id'],f'Missing connected controls target: {target}')
    for c in model['controllers']:
        ref(c['id'],c['integrated_power_unit_id'],'units',True)
        ref(c['id'],c['control_power_backup_supply_id'],'backup_supplies',True)
        for did in c['connected_control_device_ids']:
            ref(c['id'],did,'control_devices')
        for i in c['emergency_inputs']:
            ref(i['id'],i['source_device_id'],'control_devices',True)
            ref(i['id'],i['monitored_branch_circuit_id'],'branches',True)
    for z in zones:
        ref(z['id'],z['controller_id'],'controllers',True)
        ref(z['id'],z['emergency_input_id'],'emergency_inputs',True)
        for gid in z['control_group_ids']:
            ref(z['id'],gid,'control_groups')
        for light in z['light_objects']:
            ref(light['id'],light['source']['fixture_type_id'],'fixture_types')
            ref(light['id'],light['source']['drawing_page_id'],'drawing_pages',True)
            ref(light['id'],light['design']['channel_id'],'channels',True)
            ref(light['id'],light['design']['backup_supply_id'],'backup_supplies',True)
            ref(light['id'],light['design']['decision_id'],'decisions',True)
    if issues:
        return {'checks_pass':False,'issues':issues,'derived':None}

    channel_lights=defaultdict(list)
    channel_zones=defaultdict(set)
    controller_zones=defaultdict(list)
    zone_channels={}
    zone_totals={}
    output_owners={}
    if model['project']['takeoff_status']!='reconciled' or not lights:
        fail('source-reconciliation',model['project']['id'],'Takeoff must contain reconciled light objects.')
    for row in branches+units+channels+zones+model['controllers']:
        if row['decision_id'] is None:
            fail('decision-basis',row['id'],'Record the engineering assignment/selection decision.')
    for light in lights:
        if light['design']['decision_id'] is None:
            fail('decision-basis',light['id'],'Record the LV selection and channel assignment decision.')
    for decision in model['decisions']:
        if decision['status']!='confirmed':
            fail('decision-basis',decision['id'],'Decision remains provisional.')
        for aid in decision['assumption_ids']:
            if indexes['assumptions'][aid]['status']!='confirmed':
                fail('assumptions',decision['id'],'Dependent assumption is unverified or invalidated.')
    for item in model['open_items']:
        if item['blocking'] and item['status']=='open':
            fail('open-items',item['id'],item['description'])
        if item['status']=='resolved' and not item['resolution']:
            fail('open-items',item['id'],'A resolved item requires a resolution.')
    for z in zones:
        zid=z['id']
        watts=[]
        for light in z['light_objects']:
            lid=light['id']
            load=load_watts(light['design']['load'])
            watts.append(load)
            if load is None:
                fail('light-load',lid,'Confirmed LV watts and required length/reference length are missing.')
            cid=light['design']['channel_id']
            if cid is None:
                fail('assignment-completeness',lid,'One power channel is required for this single-input light object.')
            else:
                channel_lights[cid].append(light)
                channel_zones[cid].add(zid)
                group=light['design']['compatibility_group']
                if group is None or group!=indexes['channels'][cid]['compatibility_group']:
                    fail('compatibility',lid,'Light and power channel need matching confirmed compatibility groups.')
            page=indexes['drawing_pages'].get(light['source']['drawing_page_id'])
            point=light['source']['drawing_anchor']
            if point and (not page or point['x_pt']>page['width_pt'] or point['y_pt']>page['height_pt']):
                fail('spatial-context',lid,'Anchor needs a page and must be inside its displayed bounds.')
        zone_totals[zid]=None if any(w is None for w in watts) else sum(watts,Decimal(0))
        zone_channels[zid]=sorted({l['design']['channel_id'] for l in z['light_objects'] if l['design']['channel_id']})
        controller=indexes['controllers'].get(z['controller_id'])
        output=z['controller_output']
        if not controller or output is None or controller['number_of_control_outputs'] is None:
            fail('controller-assignment',zid,'A controller, output number, and confirmed output capacity are required.')
        else:
            controller_zones[controller['id']].append(zid)
            if output>controller['number_of_control_outputs']:
                fail('controller-capacity',zid,'Controller output is outside the device capacity.')
            key=(controller['id'],output)
            if key in output_owners:
                fail('controller-capacity',zid,'Distinct independently controlled zones cannot share one controller output.')
            output_owners[key]=zid
        if z['driver_type'] is None or z['on_off_type'] is None or z['normal_behavior'] is None:
            fail('zone-intent',zid,'Driver, normal behavior, and on/off behavior require confirmation.')
        role=z['egress_type']
        expected_normal={'em_always_off':'always_off','em_always_on':'always_on','em_normally_controlled':'controlled'}
        if role is None or z['emergency_behavior'] is None:
            fail('emergency-intent',zid,'Emergency classification and response require confirmation.')
        elif role=='normal':
            if z['emergency_behavior']!='not_required' or z['emergency_input_id'] is not None:
                fail('emergency-intent',zid,'Normal zones do not carry an emergency force-on assignment in this draft.')
        else:
            if z['normal_behavior']!=expected_normal[role] or z['emergency_behavior']!='force_on':
                fail('emergency-intent',zid,'Emergency label, normal behavior, and emergency force-on response disagree.')
            inp=indexes['emergency_inputs'].get(z['emergency_input_id'])
            if not inp or input_owner[inp['id']]!=z['controller_id']:
                fail('emergency-signal',zid,'Emergency zone requires an input on its assigned controller.')
            elif (not inp['verified'] or inp['source_device_id'] is None or inp['signal_type'] is None
                  or inp['monitored_branch_circuit_id'] is None or inp['trigger_condition']!='normal_power_lost'
                  or inp['source_device_id'] not in controller['connected_control_device_ids']):
                fail('emergency-signal',zid,'Confirm the normal-power-loss source, monitored circuit, interface, and controller connection.')
            if controller:
                control_backup=controller['control_power_backup_supply_id']
                integrated=indexes['units'].get(controller['integrated_power_unit_id'])
                if control_backup is None and integrated:
                    control_backup=integrated['backup_supply_id'] or indexes['branches'][unit_owner[integrated['id']]]['backup_supply_id']
                if control_backup is None or not indexes['backup_supplies'][control_backup]['verified']:
                    fail('emergency-control-power',zid,'Confirm that the controller remains powered to execute the outage override.')
            for light in z['light_objects']:
                backup_id=light['design']['backup_supply_id']
                cid=light['design']['channel_id']
                if backup_id is None and cid:
                    unit=indexes['units'][channel_owner[cid]]
                    backup_id=unit['backup_supply_id'] or indexes['branches'][unit_owner[unit['id']]]['backup_supply_id']
                if backup_id is None or not indexes['backup_supplies'][backup_id]['verified']:
                    fail('emergency-supply',light['id'],'Confirm a backup power provision independently of the force-on command.')

    channel_totals={}
    for c in channels:
        cid=c['id']
        watts=[load_watts(l['design']['load']) for l in channel_lights[cid]]
        aux=c['auxiliary_load_watts']
        channel_totals[cid]=(None if aux is None or any(w is None for w in watts)
                             else sum(watts,Decimal(str(aux))))
        if not channel_lights[cid]:
            continue  # Explicit spare output; no connected fixture load.
        if (c['rated_output_watts'] is None or c['design_limit_watts'] is None
            or c['power_class'] is None or c['validation_profile'] is None or aux is None
            or c['voltage']['current_type'] is None
            or (c['voltage']['nominal_v'] is None and (c['voltage']['min_v'] is None or c['voltage']['max_v'] is None))):
            fail('channel-basis',cid,'Used channel ratings, profile, voltage, and auxiliary load need confirmation.')
        if c['voltage']['min_v'] is not None and c['voltage']['max_v'] is not None and c['voltage']['min_v']>c['voltage']['max_v']:
            fail('channel-basis',cid,'Voltage range minimum exceeds maximum.')
        if c['design_limit_watts'] is not None and c['rated_output_watts'] is not None:
            if c['design_limit_watts']>c['rated_output_watts']:
                fail('channel-load',cid,'Design limit exceeds the verified rated output.')
            if channel_totals[cid] is not None and channel_totals[cid]>Decimal(str(c['design_limit_watts'])):
                fail('channel-load',cid,'Connected load exceeds the channel design limit.')
    unit_totals={}
    branch_totals={}
    for u in units:
        total=[channel_totals[c['id']] for c in u['channels']]
        unit_totals[u['id']]=None if any(w is None for w in total) else sum(total,Decimal(0))
        for field in ['input_voltage_v','input_phases','lv_power_type','number_of_channels','rated_output_watts',
                      'rated_input_watts','design_input_watts','aggregate_design_limit_watts']:
            if u[field] is None:
                fail('power-unit-basis',u['id'],f'Confirm {field}; do not substitute output watts for AC input watts.')
        if u['number_of_channels'] is not None and len(u['channels'])>u['number_of_channels']:
            fail('power-unit-capacity',u['id'],'Owned output objects exceed the hardware channel count.')
        if u['lv_power_type'] not in (None,'mixed'):
            for c in u['channels']:
                if c['power_class'] not in (None,u['lv_power_type']):
                    fail('power-unit-basis',c['id'],'Channel class differs from the unit class; confirm a mixed-output unit explicitly.')
        if u['aggregate_design_limit_watts'] is not None and u['rated_output_watts'] is not None:
            if u['aggregate_design_limit_watts']>u['rated_output_watts']:
                fail('power-unit-capacity',u['id'],'Aggregate design budget exceeds the rated output.')
            if unit_totals[u['id']] is not None and unit_totals[u['id']]>Decimal(str(u['aggregate_design_limit_watts'])):
                fail('power-unit-capacity',u['id'],'Connected output watts exceed the aggregate design budget.')
        if u['design_input_watts'] is not None and u['rated_input_watts'] is not None and u['design_input_watts']>u['rated_input_watts']:
            fail('power-unit-capacity',u['id'],'Design input watts exceed the selected input rating.')
        if unit_totals[u['id']] is not None and u['design_input_watts'] is not None and Decimal(str(u['design_input_watts']))<unit_totals[u['id']]:
            fail('power-unit-basis',u['id'],'Input load cannot be below connected output load for this AC-fed converter model.')
    for b in branches:
        values=[u['design_input_watts'] for u in b['power_units']]
        branch_totals[b['id']]=None if any(v is None for v in values) else sum((Decimal(str(v)) for v in values),Decimal(0))
        for u in b['power_units']:
            if b['voltage_v'] is not None and u['input_voltage_v'] is not None and b['voltage_v']!=u['input_voltage_v']:
                fail('input-compatibility',u['id'],'Selected operating input voltage and branch voltage disagree.')
            if b['phases'] is not None and u['input_phases'] is not None and b['phases']!=u['input_phases']:
                fail('input-compatibility',u['id'],'Branch connection phases and operating input phases disagree.')
    derived={
        'zone_connected_watts':zone_totals,'zone_channel_ids':zone_channels,
        'channel_connected_watts':channel_totals,
        'channel_zone_ids':{c['id']:sorted(channel_zones[c['id']]) for c in channels},
        'power_unit_connected_output_watts':unit_totals,'branch_lighting_input_watts':branch_totals,
        'controller_zone_ids':{c['id']:controller_zones[c['id']] for c in model['controllers']},
        'physical_quantities':{'power_units':len(units),'separate_controllers':sum(c['integrated_power_unit_id'] is None for c in model['controllers']),
                               'light_objects':len(lights),'modeled_power_outputs':len(channels)}}
    return {'checks_pass':not issues,'issues':issues,'derived':derived}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('model',type=Path)
    args=parser.parse_args()
    try:
        result=check_model(read_model(args.model))
    except (OSError,ValueError) as error:
        parser.exit(2,f'Cannot read model: {error}\n')
    print(json.dumps(result,indent=2,default=lambda v:str(v) if isinstance(v,Decimal) else v))
    return 0 if result['checks_pass'] else 1


if __name__=='__main__':
    raise SystemExit(main())
