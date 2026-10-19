"""Proposal Z: first real v0.10 project's CLI, projections and reader regressions."""
import copy
import json
import subprocess
import sys
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

from generators.model_equipment_v10 import check_v10, upgrade_v10
from generators.model_intake import model_json
from generators.model_access import iter_power_units, iter_channels
from generators.validate_model import read_model
from generators.model_bundles import build
from generators.milestone_markup import schedules
from generators.export_intake import export_intake

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs/reference-implementations/synthetic-bundles/lighting-model.json"


def fixture():
    return upgrade_v10(json.loads(SOURCE.read_text()))


def dc_fixture():
    model = fixture()
    unit = model["power_units"][0]
    for branch in model["branch_circuits"]:
        branch["power_unit_ids"] = [uid for uid in branch["power_unit_ids"] if uid != unit["id"]]
    unit["input_power_type"] = "dc"
    unit["ac_input_phases"] = None
    unit["input_voltage"] = {"nominal_v": 48, "min_v": 24, "max_v": 57}
    unit["input_feed_ids"] = ["FEED-001"]
    unit["design_input_watts"] = 50
    ref = model["source_references"][0]["id"]
    model["distribution_units"] = [{
        "id": "PDU-001", "label": "EPS PDU", "equipment_class": "eps_pdu",
        "input_branch_circuit_id": model["branch_circuits"][0]["id"],
        "input_power_type": "ac",
        "input_voltage": {"nominal_v": 120, "min_v": None, "max_v": None},
        "output_count": 16, "rated_total_output_watts": 1600,
        "source_ref_ids": [ref], "decision_id": None
    }]
    model["dc_power_feeds"] = [{
        "id": "FEED-001", "source_distribution_unit_id": "PDU-001",
        "source_output": 1, "target_power_unit_id": unit["id"],
        "target_input": 1, "rated_watts": 100, "demand_watts": 50.125,
        "source_ref_ids": [ref], "decision_id": None
    }]
    return model


def rules(report, key="issues"):
    return {r["rule"] for r in report[key]}


class ProposalZTests(unittest.TestCase):
    def test_z1_z2_decimal_read_model_and_both_validation_clis(self):
        model = dc_fixture()
        with tempfile.TemporaryDirectory() as folder:
            filename = Path(folder) / "model.json"
            filename.write_text(model_json(model) + "\n")
            parsed = read_model(filename)
            self.assertIsInstance(parsed["dc_power_feeds"][0]["demand_watts"], Decimal)
            result = check_v10(parsed, "design")
            self.assertEqual(result["legacy_projection_status"], "complete")
            self.assertIsNotNone(result["derived"])
            for module in ("generators.model_equipment_v10", "generators.model_intake"):
                p = subprocess.run(
                    [sys.executable, "-m", module, str(filename), "--phase", "design"],
                    cwd=ROOT, capture_output=True, text=True)
                self.assertIn(p.returncode, (0, 1), (module, p.stderr))
                cli = json.loads(p.stdout)
                self.assertEqual(cli["legacy_projection_status"], "complete")
                self.assertEqual(cli["issues"], json.loads(json.dumps(result, default=str))["issues"])

    def test_z1_upgrade_cli_preserves_numeric_type_and_refuses_overwrite(self):
        source=json.loads(SOURCE.read_text())
        source["light_objects"][0]["design"]["load"]["watts"]=20.125
        with tempfile.TemporaryDirectory() as folder:
            old=Path(folder)/"legacy.json"
            new=Path(folder)/"v10.json"
            old.write_text(model_json(source)+"\\n")
            command=[sys.executable,"-m","generators.model_equipment_v10",
                     str(old),"--upgrade-output",str(new)]
            first=subprocess.run(command,cwd=ROOT,capture_output=True,text=True)
            self.assertEqual(first.returncode,0,first.stderr)
            content=json.loads(new.read_text())
            self.assertIsInstance(content["light_objects"][0]["design"]["load"]["watts"],float)
            self.assertEqual(content["light_objects"][0]["design"]["load"]["watts"],20.125)
            again=subprocess.run(command,cwd=ROOT,capture_output=True,text=True)
            self.assertNotEqual(again.returncode,0)
            self.assertEqual(json.loads(new.read_text()),content)

    def test_z2_decimal_feeds_aggregate_exactly_and_detect_limit(self):
        model = dc_fixture()
        model["distribution_units"][0]["rated_total_output_watts"] = Decimal("50.12")
        model["dc_power_feeds"][0]["demand_watts"] = Decimal("50.125")
        result = check_v10(model, "design")
        self.assertIn("pdu-total-load", rules(result))

    def test_z3_new_equipment_open_item_keeps_all_legacy_checks(self):
        model = dc_fixture()
        # Deliberately create an unrelated old-style engineering failure.
        model["power_units"][0]["channels"][0]["design_limit_watts"] = 1
        before = check_v10(model, "design")
        self.assertEqual(before["legacy_projection_status"], "complete")
        self.assertIn("channel-design-profile", rules(before))
        untouched = copy.deepcopy(model)
        model["open_items"].append({
            "id": "OI-TRACK-PDU", "description": "PDU/feed evidence follow-up",
            "affects_ids": ["PDU-001", "FEED-001"],
            "source_ref_ids": [model["source_references"][0]["id"]],
            "blocking": False, "status": "open", "resolution": None, "decision_id": None
        })
        after = check_v10(model, "design")
        self.assertEqual(after["legacy_projection_status"], "complete")
        self.assertNotIn("reference-integrity", rules(after), after["issues"])
        self.assertIn("channel-design-profile", rules(after))
        self.assertGreaterEqual(len(after["issues"]), len(before["issues"]))
        self.assertEqual(untouched["power_units"], model["power_units"])
        self.assertEqual(model["open_items"][0]["affects_ids"], ["PDU-001", "FEED-001"])

    def test_z3_invalid_open_item_is_visible_with_explicit_halt(self):
        model = dc_fixture()
        model["open_items"] = [{
            "id": "OI-BAD-PDU", "description": "Invalid reference",
            "affects_ids": ["NOT-A-REAL-PDU"], "source_ref_ids": ["REF-SYNTHETIC"],
            "blocking": False, "status": "open", "resolution": None, "decision_id": None
        }]
        result = check_v10(model, "design")
        self.assertIn("reference-integrity", rules(result))
        self.assertIn("legacy-projection-incomplete", rules(result))
        self.assertEqual(result["legacy_projection_status"], "halted")
        self.assertIsNone(result["derived"])

    def test_z4_synthetic_container_has_no_decision_artifact(self):
        model = dc_fixture()
        result = check_v10(model, "design")
        self.assertEqual(result["legacy_projection_status"], "complete")
        self.assertFalse(any(x["rule"] == "decision-basis" and
                             x["entity_id"] == "X10-COMPATIBILITY-ONLY"
                             for x in result["issues"]))

    def test_z5_missing_design_evidence_deferred_from_intake(self):
        model = dc_fixture()
        model["distribution_units"][0]["input_branch_circuit_id"] = None
        model["dc_power_feeds"][0]["rated_watts"] = None
        intake = check_v10(model, "intake")
        design = check_v10(model, "design")
        self.assertNotIn("pdu-ac-circuit", rules(intake))
        self.assertNotIn("dc-feed-rating", rules(intake))
        self.assertIn("pdu-ac-circuit", rules(intake, "deferred_issues"))
        self.assertIn("dc-feed-rating", rules(intake, "deferred_issues"))
        self.assertIn("pdu-ac-circuit", rules(design))
        self.assertIn("dc-feed-rating", rules(design))

    def test_z5_known_invalid_graph_reference_is_immediate_at_intake(self):
        model=dc_fixture()
        model["distribution_units"][0]["input_branch_circuit_id"]="NO-SUCH-BRANCH"
        intake=check_v10(model,"intake")
        self.assertIn("pdu-ac-circuit",rules(intake))
        self.assertNotIn("pdu-ac-circuit",rules(intake,"deferred_issues"))

    def test_z6_dc_input_power_language_is_not_ac(self):
        model = dc_fixture()
        model["power_units"][0]["rated_input_watts"] = None
        issues = check_v10(model, "design")["issues"]
        messages = [x["message"] for x in issues
                    if x["entity_id"] == "PU-SYNTHETIC"
                    and x["rule"] == "power-unit-basis"]
        self.assertTrue(messages)
        self.assertTrue(all("AC input watts" not in m for m in messages))

    def test_z7_shared_reader_and_microchannel_schedule_v10(self):
        v09 = json.loads(SOURCE.read_text())
        v10 = fixture()
        self.assertEqual([u["id"] for u in iter_power_units(v09)],
                         [u["id"] for u in iter_power_units(v10)])
        self.assertEqual([c["id"] for c in iter_channels(v09)],
                         [c["id"] for c in iter_channels(v10)])
        rows = schedules(v10)["micro_channels"]
        self.assertEqual({row["micro_channel_id"] for row in rows},
                         {c["id"] for c in iter_channels(v10)})
        self.assertEqual({row["micro_channel_id"] for row in rows},
                         {row["micro_channel_id"] for row in schedules(v09)["micro_channels"]})

    def test_z7_bundle_and_review_exports_support_v10(self):
        model = fixture()
        self.assertIsNotNone(build(model["bundle_routes"], model))
        with tempfile.TemporaryDirectory() as folder:
            out = Path(folder) / "review"
            report = export_intake(model, out, allow_provisional=True)
            self.assertIsNotNone(report["derived"])
            self.assertTrue((out / "bundle_review_derived.csv").exists())
            self.assertTrue((out / "light_points.csv").exists())


if __name__ == "__main__":
    unittest.main()
