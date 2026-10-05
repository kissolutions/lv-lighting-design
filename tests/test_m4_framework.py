"""M4 contract checks added by the October 2026 framework update."""
import copy
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

from generators.model_intake import SCHEMA_V06, check_model, upgrade_v06
from generators.validate_model import read_model

ROOT = Path(__file__).resolve().parents[1]


class M4FrameworkTests(unittest.TestCase):
    def setUp(self):
        old = read_model(ROOT / "docs/reference-implementations/synthetic-voltage/design-model.json")
        self.model = upgrade_v06(old)
        self.light = self.model["light_objects"][0]
        self.channel = self.model["branch_circuits"][0]["power_units"][0]["channels"][0]
        self.zone = next(z for z in self.model["light_zones"] if self.light["id"] in z["light_object_ids"])

        # Complete the new M4 fields for the synthetic fixture/channel.
        self.model["fixture_types"][0]["source_dimming_capability"] = "dimmable"
        self.light["design"]["dimming_capability"] = "dimmable"
        self.channel["light_zone_id"] = self.zone["id"]
        self.channel["validation_profile"] = "class2_100w_95w_design"
        self.channel["design_limit_watts"] = 95
        # Existing synthetic controller ID/output are not guaranteed to describe a physical output;
        # null/null is allowed until physical output assignment.
        self.channel["controller_id"] = None
        self.channel["controller_output"] = None

    def rules(self):
        return {i["rule"] for i in check_model(self.model, "design")["issues"]}

    def test_schema_is_valid(self):
        Draft202012Validator.check_schema(json.loads(SCHEMA_V06.read_text()))

    def test_power_type_is_peer_to_numeric_voltage(self):
        voltage = self.light["design"]["input_voltage"]
        self.assertNotIn("current_type", voltage)
        self.assertEqual(self.light["design"]["input_power_type"], "dc")
        self.assertIn("min_v", voltage)
        self.assertIn("max_v", voltage)

    def test_dimmable_fixture_may_be_used_without_dimming(self):
        self.zone["driver_type"] = "non_dimming"
        self.light["design"]["dimming_capability"] = "dimmable"
        self.assertNotIn("fixture-control-capability", self.rules())

    def test_non_dimmable_fixture_cannot_satisfy_dimming_zone(self):
        self.zone["driver_type"] = "dimming"
        self.light["design"]["dimming_capability"] = "non_dimmable"
        self.assertIn("fixture-control-capability", self.rules())

    def test_zone_narrative_does_not_change_physical_voltage(self):
        before = copy.deepcopy(self.light["design"]["input_voltage"])
        self.zone["driver_type"] = "non_dimming"
        check_model(self.model, "design")
        self.assertEqual(before, self.light["design"]["input_voltage"])

    def test_ac_dc_mismatch_is_separate_from_voltage(self):
        self.light["design"]["input_power_type"] = "ac"
        self.assertIn("power-type-compatibility", self.rules())

    def test_micro_channel_cannot_span_zones(self):
        other = self.model["light_objects"][1]
        other["design"]["channel_id"] = self.channel["id"]
        other["design"]["input_power_type"] = self.light["design"]["input_power_type"]
        other["design"]["input_voltage"] = copy.deepcopy(self.light["design"]["input_voltage"])
        other["design"]["input_power_mode"] = self.light["design"]["input_power_mode"]
        other["design"]["input_current_ma"] = self.light["design"]["input_current_ma"]
        other["design"]["driver_type"] = self.light["design"]["driver_type"]
        other["design"]["dimming_capability"] = "dimmable"
        # Move the other light to a different existing zone if necessary.
        other_zone = next((z for z in self.model["light_zones"] if z["id"] != self.zone["id"]), None)
        if other_zone is None:
            self.skipTest("Synthetic model has only one zone")
        for z in self.model["light_zones"]:
            if other["id"] in z["light_object_ids"]:
                z["light_object_ids"].remove(other["id"])
        other_zone["light_object_ids"].append(other["id"])
        self.assertIn("micro-channel-zone", self.rules())

    def test_95w_profile_rejects_larger_limit(self):
        self.channel["design_limit_watts"] = 96
        self.assertIn("schema", self.rules())


if __name__ == "__main__":
    unittest.main()
