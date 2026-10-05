"""Entered v0.5 source/selected voltage and power-mode checks; no product certification."""
from __future__ import annotations

from collections import defaultdict


def voltage_shape_issues(model):
    """Contradictory entered numbers fail every phase, including unused outputs."""
    issues = []
    profiles = [(t['id'], t['source_voltage']) for t in model['fixture_types']]
    profiles += [(l['id'], l['design']['input_voltage']) for l in model['light_objects']]
    profiles += [(c['id'], c['voltage']) for b in model['branch_circuits']
                 for u in b['power_units'] for c in u['channels']]
    for owner, voltage in profiles:
        low, high, nominal = (voltage[k] for k in ('min_v', 'max_v', 'nominal_v'))
        invalid = (low is not None and high is not None and low > high)
        invalid |= nominal is not None and low is not None and nominal < low
        invalid |= nominal is not None and high is not None and nominal > high
        if invalid:
            issues.append(dict(rule='voltage-shape', entity_id=owner,
                               message='Voltage range/nominal values contradict one another.'))
    return issues


def interface_issues(model):
    """Compare the selected input at the supply channel, never the original source input."""
    issues, members = [], defaultdict(list)
    channels = {c['id']: c for b in model['branch_circuits']
                for u in b['power_units'] for c in u['channels']}

    def fail(rule, owner, message):
        issues.append(dict(rule=rule, entity_id=owner, message=message))

    def confirmed_profile(voltage, mode, current):
        if voltage['current_type'] is None or mode is None:
            return False
        if mode == 'constant_voltage':
            return voltage['nominal_v'] is not None and current is None
        return (voltage['min_v'] is not None and voltage['max_v'] is not None
                and current is not None)

    for light in model['light_objects']:
        owner, design = light['id'], light['design']
        voltage, mode, current = (design[k] for k in ('input_voltage', 'input_power_mode', 'input_current_ma'))
        if design['driver_type'] is None:
            fail('light-driver-basis', owner, 'Confirm the selected driver/driverless/other architecture independently of dimming and CV/CC mode.')
        if not confirmed_profile(voltage, mode, current):
            fail('light-electrical-basis', owner,
                 'Confirm selected channel-interface AC/DC, power mode and nominal CV voltage or CC current/range; do not copy source voltage automatically.')
        cid = design['channel_id']
        if cid is not None:
            members[cid].append(light)
    for cid, lights in members.items():
        channel = channels[cid]  # Reference integrity is checked by the caller first.
        voltage, mode, current = (channel[k] for k in ('voltage', 'output_power_mode', 'output_current_ma'))
        if not confirmed_profile(voltage, mode, current):
            fail('channel-electrical-basis', cid,
                 'Confirm selected output AC/DC, power mode and fixed CV voltage or CC setpoint/compliance range.')
        if mode == 'constant_current' and len(lights) > 1:
            fail('cc-topology-review', cid,
                 'Multiple lights on a CC output require an explicit verified series/parallel/interface topology; this contract does not model it.')
        for light in lights:
            owner, design = light['id'], light['design']
            needed, needed_mode = design['input_voltage'], design['input_power_mode']
            if (mode is not None and needed_mode is not None and mode != needed_mode):
                fail('power-mode-compatibility', owner, 'Selected light input and channel output power modes disagree.')
            if (voltage['current_type'] is not None and needed['current_type'] is not None
                    and voltage['current_type'] != needed['current_type']):
                fail('voltage-compatibility', owner, 'Selected light input and channel output AC/DC types disagree.')
            if mode == needed_mode == 'constant_voltage':
                if (voltage['nominal_v'] is not None and needed['nominal_v'] is not None
                        and voltage['nominal_v'] != needed['nominal_v']):
                    fail('voltage-compatibility', owner,
                         'Fixed-voltage light input must match the selected channel setting, even when watts and compatibility-group labels match.')
            elif mode == needed_mode == 'constant_current':
                if (current is not None and design['input_current_ma'] is not None
                        and current != design['input_current_ma']):
                    fail('current-compatibility', owner, 'Selected CC drive current and channel setpoint disagree.')
                if (len(lights) == 1 and all(v is not None for v in
                        (voltage['min_v'], voltage['max_v'], needed['min_v'], needed['max_v']))
                        and (needed['min_v'] < voltage['min_v'] or needed['max_v'] > voltage['max_v'])):
                    fail('voltage-compatibility', owner, 'Required CC operating range is outside the channel compliance range.')
    return issues
