"""Y4 contract regression tests: arithmetic, manufacturer evidence and read-only validation."""
import copy
import json
import unittest
from decimal import Decimal
from pathlib import Path

from generators.model_equipment_v10 import upgrade_v10, check_v10
from generators.qdcd_y4 import validate_y4
from generators.validate_model import read_model

ROOT = Path(__file__).resolve().parents[1]


def fixture():
    source = read_model(ROOT / "docs/reference-implementations/synthetic-bundles/lighting-model.json")
    m = upgrade_v10(source)
    u = m["power_units"][0]
    controller = m["controllers"][0]
    controller["device_class"] = "SmartDC QDCD 4CHDR1"
    controller["integrated_power_unit_id"] = u["id"]
    a, b = m["light_objects"][:2]
    zone = m["light_zones"][0]
    for z in m["light_zones"]:
        for x in [a, b]:
            if x["id"] in z["light_object_ids"]:
                z["light_object_ids"].remove(x["id"])
    zone["light_object_ids"].extend([a["id"], b["id"]])
    channel = u["channels"][0]
    for x in [a, b]:
        x["design"].update(channel_id=channel["id"], input_power_type="dc",
                           input_power_mode="constant_current", input_current_ma=1000,
                           input_voltage=dict(nominal_v=None, min_v=24, max_v=40))
        x["design"]["load"] = dict(basis="per_fixture", watts=30,
                                    length_ft=None, reference_length_ft=None)
        x["source"]["fixture_type_id"] = m["fixture_types"][0]["id"]
    for x in m["light_objects"][2:]:
        if x["design"]["channel_id"] == channel["id"]:
            x["design"]["channel_id"] = None
    channel.update(output_power_mode="constant_current", output_power_type="dc",
                   output_current_ma=2000,
                   voltage=dict(nominal_v=None,min_v=12,max_v=55))
    return m, u, channel, a, b


def contract(m):
    f = m["fixture_types"][0]["id"]
    ref = m["source_references"][0]["id"]
    return dict(schema_version="1.0.0",
                fixture_evidence=[dict(fixture_type_id=f,rated_current_ma=1000,
                                       basis="manufacturer_verified",source_ref_ids=[ref])],
                combination_qualifications=[dict(fixture_type_ids=[f],
                    manufacturer_status="fixture_combination_verified",
                    manufacturer_evidence_ref_ids=[ref],
                    owner_decision_id=None,project_review_status="qualified",
                    emergency_status="qualified")],
                driver_programming=dict(current_step_ma=100,current_step_origin_ma=1000,
                                        manufacturer_evidence_ref_ids=[ref]))


class Y4Tests(unittest.TestCase):
    def setUp(self):
        self.m, self.u, self.ch, self.a, self.b = fixture()
        self.q = contract(self.m)

    def rules(self, q=None):
        return {x["rule"] for x in validate_y4(self.m,self.q if q is None else q)["findings"]}

    def test_equal_ma_parallel_sum_and_positive_qualification(self):
        rules=self.rules()
        self.assertNotIn("cc-output-sum-mismatch",rules)
        self.assertNotIn("cc-parallel-rated-current-mismatch",rules)
        self.assertNotIn("cc-combination-qualification-pending",rules)

    def test_same_voltage_unequal_branch_ma_remains_engineering_conflict(self):
        self.b["design"]["input_current_ma"]=1100
        self.ch["output_current_ma"]=2150
        rules=self.rules()
        self.assertIn("cc-parallel-rated-current-mismatch",rules)
        self.assertIn("cc-output-step-incompatible",rules)

    def test_sum_is_compared_with_driver_not_each_branch(self):
        self.ch["output_current_ma"]=1000
        self.assertIn("cc-output-sum-mismatch",self.rules())

    def test_driver_minimum_and_maximum(self):
        self.b["design"]["channel_id"]=None
        self.a["design"]["input_current_ma"]=900
        self.ch["output_current_ma"]=900
        self.assertIn("cc-output-below-driver-min",self.rules())
        self.assertIn("cc-branch-sum-below-driver-min",self.rules())
        self.a["design"]["input_current_ma"]=4500
        self.ch["output_current_ma"]=4500
        self.assertIn("cc-output-above-driver-max",self.rules())
        self.assertIn("cc-branch-sum-above-driver-max",self.rules())

    def test_missing_exact_programming_evidence_is_not_assumed(self):
        q=copy.deepcopy(self.q)
        q["driver_programming"]=None
        self.assertIn("cc-programming-step-unverified",self.rules(q))

    def test_voltage_limits_and_disjoint_parallel_operating_ranges(self):
        self.a["design"]["input_voltage"]["min_v"]=10
        self.b["design"]["input_voltage"].update(min_v=41,max_v=50)
        rules=self.rules()
        self.assertIn("cc-fixture-voltage-incompatible",rules)
        self.assertIn("cc-parallel-voltage-no-overlap",rules)

    def test_channel_and_unit_power_constraints(self):
        self.a["design"]["load"]["watts"]=50
        self.b["design"]["load"]["watts"]=50
        self.assertIn("qdcd-design-power-exceeded",self.rules())
        self.a["design"]["load"]["watts"]=60
        self.assertIn("qdcd-rated-power-exceeded",self.rules())
        # Aggregate limit applies independently of an individual over-100 W channel.
        self.a["design"]["load"]["watts"]=401
        self.assertIn("qdcd-unit-power-exceeded",self.rules())

    def test_general_parallel_document_is_not_fixture_combination_proof(self):
        q=copy.deepcopy(self.q)
        q["combination_qualifications"][0]["manufacturer_status"]="general_topology_only"
        self.assertIn("cc-combination-qualification-pending",self.rules(q))
        q["combination_qualifications"]=[]
        self.assertIn("cc-combination-qualification-pending",self.rules(q))

    def test_calculated_ma_is_not_nameplate_evidence(self):
        q=copy.deepcopy(self.q)
        q["fixture_evidence"][0]["basis"]="calculated"
        self.assertIn("cc-fixture-rated-ma-unverified",self.rules(q))

    def test_emergency_variant_is_independent_approval(self):
        self.m["fixture_types"][0]["source_emergency_provision"]="emergency"
        q=copy.deepcopy(self.q)
        q["combination_qualifications"][0]["emergency_status"]="pending"
        self.assertIn("cc-emergency-qualification-pending",self.rules(q))

    def test_read_only_and_stable_validation_shape(self):
        prior=copy.deepcopy(self.m)
        result=validate_y4(self.m,self.q)
        self.assertEqual(self.m,prior)
        self.assertIn("rule_counts",result["summary"])
        self.assertEqual(result["summary"]["qdcd_cc_channels"],1)

    def test_legacy_warnings_replaced_only_for_qdcd(self):
        report=check_v10(self.m,"design")
        for item in report["issues"]:
            if item["entity_id"] in (self.ch["id"],self.a["id"],self.b["id"]):
                self.assertNotIn(item["rule"],("cc-topology-review","current-compatibility"))
        self.assertIn("y4_validation_summary",report)

if __name__=="__main__":
    unittest.main()
