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

    def test_linear_per_foot_basis_matches_canonical_load(self):
        m,p=sample([20,20])
        m["light_objects"][0]["design"]["load"]=dict(
            basis="per_foot",watts=1.5,length_ft=20,reference_length_ft=None)
        result=pack(m,p)
        self.assertEqual(result["status"],"optimized")
        self.assertEqual(result["totals"]["total_input_watts"],50)
        self.assertEqual(result["totals"]["packed_watts"],50)
        self.assertTrue(result["totals"]["load_balance_verified"])
        self.assertEqual(result["totals"]["proposed_channel_count"],1)

    def test_reference_length_basis_matches_canonical_load(self):
        m,p=sample([20,20])
        m["light_objects"][0]["design"]["load"]=dict(
            basis="per_reference_length",watts=15,length_ft=8,reference_length_ft=4)
        result=pack(m,p)
        self.assertEqual(result["totals"]["total_input_watts"],50)
        self.assertEqual(result["totals"]["packed_watts"],50)

    def test_blocked_electrical_light_still_counts_in_model_total(self):
        m,p=sample([41,41,20])
        m["light_objects"][1]["design"]["compatibility_group"]=None
        result=pack(m,p)
        self.assertEqual(result["totals"]["total_input_watts"],102)
        self.assertEqual(result["totals"]["known_model_watts"],102)
        self.assertEqual(result["totals"]["packed_watts"],61)
        self.assertEqual(result["totals"]["excluded_known_watts"],41)
        self.assertFalse(result["totals"]["load_balance_verified"])
        self.assertEqual(result["totals"]["missing_model_load_light_ids"],[])
        self.assertIn("L002",result["unpacked_light_ids"])

    def test_unassigned_zone_still_counts_in_model_total(self):
        m,p=sample([41,41])
        m["light_zones"][0]["light_object_ids"].remove("L002")
        result=pack(m,p)
        self.assertEqual(result["totals"]["total_input_watts"],82)
        self.assertEqual(result["totals"]["excluded_known_watts"],41)

    def test_unknown_watts_marks_project_total_incomplete(self):
        m,p=sample([20,20])
        m["light_objects"][1]["design"]["load"]["watts"]=None
        result=pack(m,p)
        self.assertIsNone(result["totals"]["total_input_watts"])
        self.assertEqual(result["totals"]["known_model_watts"],20)
        self.assertEqual(result["totals"]["missing_model_load_light_ids"],["L002"])
        self.assertEqual(result["totals"]["packed_watts"],20)
        self.assertFalse(result["totals"]["load_balance_verified"])

    def test_y5_geometry_breaks_equal_watt_ties_without_changing_count(self):
        m,p=sample([40,40,40,40])
        points=[(0,0),(100,0),(0,10),(100,10)]
        for light,(x,y) in zip(m["light_objects"],points):
            light["source"]=dict(drawing_page_id="PAGE-1",
                                 drawing_anchor=dict(x_pt=x,y_pt=y))
        result=pack(m,p)
        groups={frozenset(ch["light_ids"]) for ch in result["proposed_channels"]}
        self.assertEqual(groups,{frozenset(("L001","L003")),
                                 frozenset(("L002","L004"))})
        self.assertEqual(result["totals"]["proposed_channel_count"],2)
        self.assertEqual(result["totals"]["total_input_watts"],160)
        self.assertEqual(result["totals"]["packed_watts"],160)

    def test_y5_coordinate_rotation_does_not_change_grouping(self):
        m,p=sample([40,40,40,40])
        points=[(0,0),(100,0),(0,10),(100,10)]
        for light,(x,y) in zip(m["light_objects"],points):
            light["source"]=dict(drawing_page_id="PAGE-1",
                                 drawing_anchor=dict(x_pt=x,y_pt=y))
        first=pack(m,p)
        for light in m["light_objects"]:
            point=light["source"]["drawing_anchor"]
            point["x_pt"],point["y_pt"]=-point["y_pt"],point["x_pt"]
        rotated=pack(m,p)
        self.assertEqual(
            {frozenset(ch["light_ids"]) for ch in first["proposed_channels"]},
            {frozenset(ch["light_ids"]) for ch in rotated["proposed_channels"]})

    def test_y5_cc_geometry_tie_preserves_additive_current(self):
        m,p=sample([40,40,40,40],mode="constant_current")
        p["approved_parallel_cc_cohorts"]=[dict(
            id="OEM-COHORT",approved=True,evidence_ref_ids=["OEM-APPROVAL"],
            light_ids=[x["id"] for x in m["light_objects"]])]
        points=[(0,0),(100,0),(0,10),(100,10)]
        for light,(x,y) in zip(m["light_objects"],points):
            light["source"]=dict(drawing_page_id="PAGE-1",
                                 drawing_anchor=dict(x_pt=x,y_pt=y))
        result=pack(m,p)
        groups={frozenset(ch["light_ids"]) for ch in result["proposed_channels"]}
        self.assertEqual(groups,{frozenset(("L001","L003")),
                                 frozenset(("L002","L004"))})
        self.assertEqual(result["totals"]["proposed_channel_count"],2)
        self.assertTrue(all(ch["current_setpoint_ma"]>2000 for ch in result["proposed_channels"]))

    def test_y5_without_complete_same_page_geometry_uses_stable_legacy_tie(self):
        m,p=sample([40,40,40,40])
        for light in m["light_objects"]:
            light["source"]=dict(drawing_page_id=None,drawing_anchor=None)
        first=pack(m,p)
        groups={frozenset(ch["light_ids"]) for ch in first["proposed_channels"]}
        self.assertEqual(groups,{frozenset(("L001","L002")),
                                 frozenset(("L003","L004"))})

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
