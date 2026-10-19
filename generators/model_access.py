"""Version-aware read-only access to physical lighting power equipment.

v0.9 and earlier nest power units beneath actual or legacy branch records.
v0.10 stores power units independently of real AC circuits. Consumers must
never assume an empty branch list means no downstream QDCDs/channels.
"""
from __future__ import annotations


def iter_power_units(model):
    """Yield physical power-unit records without copying or changing identity.

    Explicit v0.10 access never falls back to legacy nesting. Earlier model
    shapes retain the existing nested behavior, including test fixtures that
    predate a schema_version attribute.
    """
    if model.get("schema_version") == "0.10.0":
        if not isinstance(model.get("power_units"), list):
            raise ValueError("v0.10 model lacks root power_units[]")
        yield from model["power_units"]
    else:
        for branch in model.get("branch_circuits", []):
            if not isinstance(branch.get("power_units"), list):
                raise ValueError("Legacy branch lacks power_units[]")
            yield from branch["power_units"]


def iter_channels(model):
    """Yield the modeled physical microchannels from either supported layout."""
    for unit in iter_power_units(model):
        yield from unit["channels"]
