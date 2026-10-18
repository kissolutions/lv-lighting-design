"""Remote driver parallel-load channel optimizer regression tests."""
import copy
import unittest

from generators.channel_pack import pack


def sample(loads, mode="constant_voltage", zone="ZONE-A"):
    lights=[]
    for i,watts in enumerate(loads,1):
        lid=f"L{i:03d}"
        lights.append(dict(id=lid,design=dict(
            load=dict(basis="per_fixture",watts=watts),
            input_power_type="dc",input_power_mode=mode,
            input_voltage=dict(nominal_v=36,min_v=30,max_v=40),
            input_current_ma=round(watts/36*1000,4) if mode=="constant_current" else None,
            compatibility_group="MATCH")))
    model=dict(project=dict(model_revision="M4-TEST"),light_objects=lights,
               light_zones=[dict(id=zone,parent_zone_id=None,light_object_ids=[x["id"] for x in lights])])
    policy=dict(target_watts=90,design_max_watts=95,rated_watts=100,topology="parallel",
                output_capability=dict(cc_min_current_a=1,cc_max_current_a=4,
                   cc_min_voltage_v=12,cc_max_voltage_v=55,
                   manufacturer_evidence_ref_ids=["OEM-QDCD-VERIFIED"]))
    return model,policy


class ChannelPackingTests(unittest.TestCase):
    def test_parallel_cv_three_30w_lights_fill_one_channel(self):
        m,p=sample([30,30,30])
        result=pack(m,p)
        self.assertEqual(result["status"],"optimized")
        self.assertEqual(result["totals"]["proposed_channel_count"],1)
        self.assertEqual(result["proposed_channels"][0]["watts"],90)
        self.assertEqual(result["proposed_channels"][0]["topology"],"parallel")

    def test_ninety_is_target_not_hard_ceiling(self):
        m,p=sample([46,46])
        result=pack(m,p)
        self.assertEqual(result["totals"]["proposed_channel_count"],1)
        self.assertEqual(result["proposed_channels"][0]["watts"],92)

    def test_above_ninety_five_not_permitted(self):
        m,p=sample([49,49])
        result=pack(m,p)
        self.assertEqual(result["totals"]["proposed_channel_count"],2)
        self.assertEqual(result["status"],"optimized")

    def test_zone_boundary_blocks_combination(self):
        m,p=sample([30,30])
        m["light_zones"]=[dict(id="ZA",parent_zone_id=None,light_object_ids=["L001"]),
                           dict(id="ZB",parent_zone_id=None,light_object_ids=["L002"])]
        self.assertEqual(pack(m,p)["totals"]["proposed_channel_count"],2)

    def test_unverified_parallel_cc_is_not_approved(self):
        m,p=sample([18,18,18,18,18],mode="constant_current")
        result=pack(m,p)
        self.assertEqual(result["status"],"needs_review")
        self.assertTrue(any(f["issue"]=="cc_parallel_evidence_missing" for f in result["findings"]))
        self.assertFalse(result["electrically_verified"])

    def test_verified_remote_cc_adds_branch_currents(self):
        m,p=sample([18,18,18,18,18],mode="constant_current")
        p["approved_parallel_cc_cohorts"]=[dict(id="OEM-COHORT",approved=True,
            evidence_ref_ids=["OEM-TEST-PARALLEL-LOAD-APPROVAL"],
            light_ids=[x["id"] for x in m["light_objects"]])]
        result=pack(m,p)
        self.assertEqual(result["status"],"optimized")
        self.assertEqual(result["totals"]["proposed_channel_count"],1)
        out=result["proposed_channels"][0]
        self.assertEqual(out["watts"],90)
        self.assertAlmostEqual(out["current_setpoint_ma"],2500,delta=.01)
        self.assertEqual(out["cc_parallel_evidence_cohort"],"OEM-COHORT")

    def test_driver_cc_minimum_current_enforced(self):
        m,p=sample([18,18],mode="constant_current")
        p["approved_parallel_cc_cohorts"]=[dict(id="OEM-COHORT",approved=True,
            evidence_ref_ids=["OEM-TEST-PARALLEL-LOAD-APPROVAL"],light_ids=["L001","L002"])]
        result=pack(m,p)
        self.assertEqual(result["status"],"optimized")
        self.assertAlmostEqual(result["proposed_channels"][0]["current_setpoint_ma"],1000,delta=.01)

    def test_insufficient_current_blocks_output(self):
        m,p=sample([17.7],mode="constant_current")
        result=pack(m,p)
        self.assertEqual(result["status"],"needs_review")
        self.assertEqual(result["proposed_channels"],[])
        self.assertIn("L001",result["unpacked_light_ids"])

    def test_no_series_topology(self):
        m,p=sample([20,20])
        p["topology"]="series"
        with self.assertRaises(ValueError):
            pack(m,p)

    def test_no_cross_mode_or_voltage_packing(self):
        m,p=sample([30,30,30])
        m["light_objects"][1]["design"]["input_voltage"]["nominal_v"]=48
        m["light_objects"][2]["design"]["input_power_mode"]="constant_current"
        m["light_objects"][2]["design"]["input_current_ma"]=1000
        result=pack(m,p)
        self.assertEqual(result["totals"]["proposed_channel_count"],3)
        self.assertEqual(result["status"],"needs_review")

    def test_read_only(self):
        m,p=sample([30,30,30])
        before=copy.deepcopy(m)
        pack(m,p)
        self.assertEqual(m,before)


if __name__=="__main__":
    unittest.main()
