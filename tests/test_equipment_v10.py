"""X1/X2/X4 v0.10 staged electrical model and read-only migration regression."""
import copy
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator
from generators.model_equipment_v10 import SCHEMA, check_v10, upgrade_v10
from generators.model_intake import check_model

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"docs/reference-implementations/synthetic-bundles/lighting-model.json"


class ElectricalModelV10Tests(unittest.TestCase):
    def setUp(self):
        self.source=json.loads(SOURCE.read_text())
        self.model=upgrade_v10(self.source)

    def test_upgrade_preserves_original_and_passes_v10_shape(self):
        original=copy.deepcopy(self.source)
        Draft202012Validator.check_schema(json.loads(SCHEMA.read_text()))
        Draft202012Validator(json.loads(SCHEMA.read_text())).validate(self.model)
        self.assertEqual(self.source,original)
        self.assertEqual(self.model["schema_version"],"0.10.0")
        self.assertEqual(sum(len(b["power_unit_ids"]) for b in self.model["branch_circuits"]),
                         len(self.model["power_units"]))
        self.assertTrue(all("controller_output" not in z for z in self.model["light_zones"]))

    def test_v10_valid_existing_synthetic_and_nonmutating(self):
        baseline=check_model(self.source,"intake")
        result=check_model(self.model,"intake")
        # New graph validation must not introduce false errors for v0.9 projects.
        self.assertEqual(result["checks_pass"],baseline["checks_pass"],(result["issues"][:8],baseline["issues"][:8]))
        before=copy.deepcopy(self.model)
        check_v10(self.model,"intake")
        self.assertEqual(self.model,before)

    def _with_dc_qdcd(self):
        m=self.model
        # Existing modeled power unit is now a programmable DC-fed driver.
        u=m["power_units"][0]
        for b in m["branch_circuits"]:
            b["power_unit_ids"]=[uid for uid in b["power_unit_ids"] if uid!=u["id"]]
        u["input_power_type"]="dc"
        u["ac_input_phases"]=None
        u["input_voltage"]={"nominal_v":48,"min_v":24,"max_v":57}
        u["input_feed_ids"]=["FEED-001"]
        bid=m["branch_circuits"][0]["id"]
        base=m["source_references"][0]["id"]
        pdu={"id":"PDU-001","label":"EPS PDU","equipment_class":"eps_pdu",
             "input_branch_circuit_id":bid,"input_power_type":"ac",
             "input_voltage":{"nominal_v":120,"min_v":None,"max_v":None},
             "output_count":16,"rated_total_output_watts":1600,
             "source_ref_ids":[base],"decision_id":None}
        m["distribution_units"]=[pdu]
        m["dc_power_feeds"]=[{"id":"FEED-001","source_distribution_unit_id":"PDU-001",
             "source_output":1,"target_power_unit_id":u["id"],"target_input":1,
             "rated_watts":100,"demand_watts":50,"source_ref_ids":[base],"decision_id":None}]
        return m,u

    def test_dc_input_without_ac_phases_and_explicit_pdu_feed(self):
        m,u=self._with_dc_qdcd()
        report=check_v10(m)
        rules={i["rule"] for i in report["issues"]}
        self.assertNotIn("schema",rules,report["issues"][:12])
        self.assertNotIn("power-input",rules)
        self.assertNotIn("ac-branch-map",rules)
        self.assertNotIn("dc-feed-mapping",rules)
        self.assertNotIn("pdu-ac-circuit",rules)
        self.assertEqual(report["derived"]["equipment_graph"]["dc_feeds"],1)
        self.assertEqual(report["derived"]["equipment_graph"]["pdus"],1)

    def test_dc_phase_rejected(self):
        m,u=self._with_dc_qdcd()
        u["ac_input_phases"]=1
        self.assertIn("schema",{i["rule"] for i in check_v10(m)["issues"]})

    def test_missing_feed_is_detected(self):
        m,u=self._with_dc_qdcd()
        m["dc_power_feeds"].clear()
        self.assertIn("dc-feed-mapping",{i["rule"] for i in check_v10(m)["issues"]})

    def test_real_ac_circuit_required_for_pdu(self):
        m,u=self._with_dc_qdcd()
        m["distribution_units"][0]["input_branch_circuit_id"]=None
        self.assertIn("pdu-ac-circuit",{i["rule"] for i in check_v10(m,"design")["issues"]})
        self.assertIn("pdu-ac-circuit",{i["rule"] for i in check_v10(m,"intake")["deferred_issues"]})

    def test_pdu_feed_capacity_and_no_double_claims(self):
        m,u=self._with_dc_qdcd()
        m["dc_power_feeds"][0]["demand_watts"]=101
        self.assertIn("dc-feed-load",{i["rule"] for i in check_v10(m)["issues"]})
        m["dc_power_feeds"][0]["demand_watts"]=50
        extra=copy.deepcopy(m["dc_power_feeds"][0])
        extra["id"]="FEED-002"
        u["input_feed_ids"].append("FEED-002")
        m["dc_power_feeds"].append(extra)
        self.assertIn("pdu-output-ownership",{i["rule"] for i in check_v10(m)["issues"]})

    def test_zone_can_map_multiple_channels_no_single_controller_field(self):
        m=self.model
        zone=next(z for z in m["light_zones"] if z["channel_ids"])
        ch=next(c for u in m["power_units"] for c in u["channels"] if c["light_zone_id"]==zone["id"])
        clone=copy.deepcopy(ch)
        clone["id"]="CH-ADDITIONAL"
        clone["controller_id"]=None
        clone["controller_output"]=None
        m["power_units"][0]["channels"].append(clone)
        zone["channel_ids"].append(clone["id"])
        result=check_v10(m)
        self.assertNotIn("zone-channel-map",{i["rule"] for i in result["issues"]})
        self.assertNotIn("schema",{i["rule"] for i in result["issues"]})

    def test_optional_cc_ma_schedule_metadata_preserves_legacy_projection(self):
        from generators.export_intake import export_intake
        import csv
        import tempfile
        from decimal import Decimal
        m=self.model
        f=m["fixture_types"][0]
        light=next(x for x in m["light_objects"] if x["source"]["fixture_type_id"]==f["id"])
        ref=m["source_references"][0]["id"]
        f.update(lv_cc_rated_current_ma=Decimal("1139.0"),
                 lv_cc_min_current_ma=Decimal("1100"),
                 lv_cc_max_current_ma=Decimal("1200"),
                 lv_cc_current_source_ref_ids=[ref])
        light["design"].update(input_current_ma=Decimal("1139.00"),
                  input_current_min_ma=Decimal("1100"),
                  input_current_max_ma=Decimal("1200"),
                  input_current_source_ref_ids=[ref])
        before=copy.deepcopy(m)
        report=check_v10(m,"intake")
        self.assertNotIn("schema",{x["rule"] for x in report["issues"]},report["issues"])
        self.assertEqual(report["legacy_projection_status"],"complete",report["issues"])
        self.assertNotIn("cc-rated-current-range",{x["rule"] for x in report["issues"]})
        self.assertEqual(m,before)
        with tempfile.TemporaryDirectory() as temp:
            export_intake(m,temp,allow_provisional=True)
            with open(Path(temp)/"fixture_type_schedule.csv",encoding="utf-8-sig",newline="") as h:
                fixture_row=next(x for x in csv.DictReader(h) if x["fixture_type_id"]==f["id"])
            with open(Path(temp)/"light_points.csv",encoding="utf-8-sig",newline="") as h:
                point_row=next(x for x in csv.DictReader(h) if x["light_id"]==light["id"])
            self.assertEqual(Decimal(fixture_row["lv_cc_rated_current_ma"]),Decimal("1139"))
            self.assertEqual(Decimal(fixture_row["lv_cc_min_current_ma"]),Decimal("1100"))
            self.assertEqual(Decimal(fixture_row["lv_cc_max_current_ma"]),Decimal("1200"))
            self.assertEqual(fixture_row["lv_cc_current_source_ref_ids"],ref)
            self.assertEqual(Decimal(point_row["lv_input_current_ma"]),Decimal("1139"))
            self.assertEqual(Decimal(point_row["lv_input_current_min_ma"]),Decimal("1100"))
            self.assertEqual(Decimal(point_row["lv_input_current_max_ma"]),Decimal("1200"))
            self.assertEqual(point_row["lv_input_current_source_ref_ids"],ref)

    def test_fixture_cc_range_contradiction_and_point_mismatch_detected(self):
        m=self.model
        f=m["fixture_types"][0]
        light=next(x for x in m["light_objects"] if x["source"]["fixture_type_id"]==f["id"])
        f.update(lv_cc_rated_current_ma=1139,lv_cc_min_current_ma=1200,
                 lv_cc_max_current_ma=1100)
        light["design"].update(input_power_mode="constant_current",
                      input_current_ma=1000,
                      input_current_min_ma=1100,input_current_max_ma=1250)
        report=check_v10(m,"intake")
        rules={x["rule"] for x in report["issues"]}
        self.assertIn("cc-rated-current-range",rules)
        self.assertIn("cc-selected-current-vs-fixture-type",rules)
        self.assertEqual(report["legacy_projection_status"],"complete")

    def test_unknown_cc_rating_source_id_does_not_hide_legacy_validation(self):
        m=self.model
        f=m["fixture_types"][0]
        f["lv_cc_current_source_ref_ids"]=["OEM-NOT-IN-SOURCE-REGISTER"]
        report=check_v10(m,"intake")
        self.assertIn("cc-current-source-reference",{x["rule"] for x in report["issues"]})
        self.assertEqual(report["legacy_projection_status"],"complete")

    def test_unlisted_zone_channel_detected(self):
        m=self.model
        zone=next(z for z in m["light_zones"] if z["channel_ids"])
        zone["channel_ids"].clear()
        self.assertIn("zone-channel-map",{i["rule"] for i in check_v10(m)["issues"]})


if __name__=="__main__":
    unittest.main()
