"""Boundary and failure cases for the engineering contract and review export."""
import copy
import csv
import json
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

from jsonschema import Draft202012Validator

from generators.export_review import export_review
from generators.validate_model import SCHEMA_PATH, read_model, validate

ROOT = Path(__file__).resolve().parents[1]
DEMO = ROOT / "docs/reference-implementations/synthetic-room/lighting-model.json"


class Phase1Tests(unittest.TestCase):
    def setUp(self):
        self.model = read_model(DEMO)

    def rules(self):
        return {issue["rule"] for issue in validate(self.model)}

    def test_schema_and_synthetic_seed(self):
        schema = json.loads(SCHEMA_PATH.read_text())
        Draft202012Validator.check_schema(schema)
        self.assertEqual(validate(self.model), [])

    def test_blank_template_is_structural_seed_not_validated_design(self):
        model = read_model(ROOT / "templates/lighting-project.template.json")
        issues = validate(model)
        self.assertNotIn("schema", {r["rule"] for r in issues})
        self.assertIn("source-reconciliation", {r["rule"] for r in issues})

    def test_exactly_90_w_passes(self):
        self.model["design"]["fixture_selections"][0]["lv_input_watts"] = 22.5
        self.assertEqual(validate(self.model), [])

    def test_fraction_over_90_w_fails(self):
        self.model["design"]["fixture_selections"][0]["lv_input_watts"] = 22.500025
        self.assertIn("channel-wattage", self.rules())

    def test_decimal_json_does_not_round_a_load_below_the_limit(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "model.json"
            content = DEMO.read_text().replace('"lv_input_watts": 20', '"lv_input_watts": 22.500000000000000025')
            path.write_text(content)
            self.model = read_model(path)
            self.assertIsInstance(self.model["design"]["fixture_selections"][0]["lv_input_watts"], Decimal)
            self.assertIn("channel-wattage", self.rules())

    def test_lower_verified_design_limit_applies(self):
        self.model["design"]["lv_channels"][0]["design_limit_watts"] = 79
        self.assertIn("channel-wattage", self.rules())

    def test_cannot_inflate_design_limit_to_100(self):
        self.model["design"]["lv_channels"][0]["design_limit_watts"] = 100
        self.assertIn("schema", self.rules())

    def test_source_watts_are_not_used_as_lv_load(self):
        self.model["facts"]["fixture_types"][0]["source_input_watts"] = 1000
        self.assertEqual(validate(self.model), [])

    def test_unknown_source_watts_do_not_override_confirmed_lv_selection(self):
        self.model["facts"]["fixture_types"][0]["source_input_watts"] = None
        self.assertEqual(validate(self.model), [])

    def test_unknown_lv_watts_block_checks(self):
        self.model["design"]["fixture_selections"][0]["lv_input_watts"] = None
        self.assertIn("channel-wattage", self.rules())

    def test_missing_scope_blocks(self):
        self.model["design"]["fixture_scope"].pop()
        self.assertIn("fixture-assignment-completeness", self.rules())

    def test_duplicate_scope_blocks(self):
        row = copy.deepcopy(self.model["design"]["fixture_scope"][0])
        row["id"] = "OTHER-SCOPE"
        self.model["design"]["fixture_scope"].append(row)
        self.assertIn("fixture-assignment-completeness", self.rules())

    def test_unassigned_fixture_blocks(self):
        self.model["design"]["lv_channels"][0]["fixture_ids"].pop()
        self.assertIn("fixture-assignment-completeness", self.rules())

    def test_double_assignment_blocks(self):
        row = copy.deepcopy(self.model["design"]["lv_channels"][0])
        row["id"] = "OTHER-CHANNEL"
        self.model["design"]["lv_channels"].append(row)
        self.assertIn("fixture-assignment-completeness", self.rules())

    def test_exclusion_requires_reason_and_no_assignment(self):
        row = self.model["design"]["fixture_scope"][0]
        row["disposition"] = "excluded"
        self.assertIn("fixture-assignment-completeness", self.rules())
        row["reason"] = "Special system outside this LV scope"
        self.model["design"]["lv_channels"][0]["fixture_ids"].remove("A1")
        self.assertEqual(validate(self.model), [])

    def add_zone(self):
        zone = copy.deepcopy(self.model["facts"]["control_zones"][0])
        zone["id"] = "Z-OTHER"
        self.model["facts"]["control_zones"].append(zone)

    def test_cross_zone_channel_blocks(self):
        self.add_zone()
        self.model["facts"]["fixture_instances"][0]["source_control_zone_id"] = "Z-OTHER"
        self.assertIn("zone-boundary-preservation", self.rules())

    def test_traceable_design_zone_correction_preserves_source(self):
        self.add_zone()
        self.model["facts"]["fixture_instances"][0]["source_control_zone_id"] = "Z-OTHER"
        self.model["design"]["zone_assignments"].append({"id": "ZONE-CORRECTION", "fixture_id": "A1",
                                                       "control_zone_id": "Z-204", "decision_id": "DEC-GROUP"})
        self.assertEqual(validate(self.model), [])
        self.assertEqual(self.model["facts"]["fixture_instances"][0]["source_control_zone_id"], "Z-OTHER")

    def test_unknown_control_intent_blocks(self):
        self.model["facts"]["control_zones"][0]["intent_status"] = "unknown"
        self.assertIn("zone-boundary-preservation", self.rules())

    def test_incompatible_fixture_group_blocks(self):
        self.model["design"]["fixture_selections"][0]["compatibility_group"] = "DIFFERENT-DRIVER"
        self.assertIn("electrical-compatibility", self.rules())

    def test_missing_type_reference_blocks(self):
        self.model["facts"]["fixture_instances"][0]["fixture_type_id"] = "MISSING"
        self.assertIn("reference-integrity", self.rules())

    def test_missing_evidence_reference_blocks(self):
        self.model["design"]["fixture_selections"][0]["source_ref_ids"] = ["MISSING"]
        self.assertIn("reference-integrity", self.rules())

    def test_duplicate_id_blocks_before_dereference(self):
        self.model["facts"]["fixture_instances"][1]["id"] = "A1"
        self.assertIn("unique-ids", self.rules())

    def test_empty_evidence_is_not_a_confirmed_selection(self):
        self.model["design"]["fixture_selections"][0]["source_ref_ids"] = []
        self.assertIn("schema", self.rules())

    def test_duplicate_source_mark_blocks(self):
        fixture_type = copy.deepcopy(self.model["facts"]["fixture_types"][0])
        fixture_type["id"] = "OTHER-TYPE"
        self.model["facts"]["fixture_types"].append(fixture_type)
        self.assertIn("fixture-schedule-consistency", self.rules())

    def test_provisional_decision_blocks(self):
        self.model["design"]["decisions"][0]["status"] = "provisional"
        self.assertIn("decision-confirmation", self.rules())

    def test_invalidated_dependent_assumption_blocks(self):
        self.model["design"]["assumptions"].append({"id": "ASM-1", "statement": "Fixture unchanged",
            "source_ref_ids": ["REF-DEMO-PLAN"], "invalidated_if": "Fixture revised", "status": "invalidated"})
        self.model["design"]["decisions"][0]["assumption_ids"] = ["ASM-1"]
        self.assertIn("assumptions", self.rules())

    def test_open_blocking_item_blocks(self):
        self.model["open_items"].append({"id": "OPEN-1", "description": "Driver unconfirmed", "affects_ids": ["TYPE-L3"],
            "source_ref_ids": ["REF-DEMO-PLAN"], "blocking": True, "status": "open", "resolution": None, "decision_id": None})
        self.assertIn("open-items", self.rules())
        self.model["open_items"][0]["blocking"] = False
        self.assertEqual(validate(self.model), [])

    def test_unknown_power_node_capacity_blocks(self):
        self.model["design"]["power_nodes"][0]["capacity_channels"] = None
        self.assertIn("component-capacity", self.rules())

    def test_node_aggregate_capacity_independent_of_channel_capacity(self):
        self.model["design"]["power_nodes"][0]["aggregate_design_limit_watts"] = 79
        self.assertIn("component-capacity", self.rules())
        self.assertNotIn("channel-wattage", self.rules())

    def test_node_channel_capacity_independent_of_watts(self):
        row = copy.deepcopy(self.model["design"]["lv_channels"][0])
        row["id"] = "OTHER-CHANNEL"
        row["fixture_ids"] = ["A3", "A4"]
        self.model["design"]["lv_channels"][0]["fixture_ids"] = ["A1", "A2"]
        self.model["design"]["lv_channels"].append(row)
        self.assertIn("component-capacity", self.rules())
        self.assertNotIn("fixture-assignment-completeness", self.rules())

    def test_null_geometry_allowed_but_known_outside_page_blocks(self):
        self.model["facts"]["fixture_instances"][0]["drawing_anchor"] = None
        self.assertEqual(validate(self.model), [])
        self.model["facts"]["fixture_instances"][0]["drawing_anchor"] = {"x_pt": 3000, "y_pt": 400}
        self.assertIn("spatial-context", self.rules())

    def test_export_derives_80_w_and_counts_one_physical_node(self):
        before = copy.deepcopy(self.model)
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "review"
            report = export_review(self.model, output)
            self.assertTrue(report["phase1_checks_pass"])
            self.assertEqual(len(list(output.iterdir())), 6)
            with (output / "channel_schedule.csv").open(encoding="utf-8-sig") as stream:
                rows = list(csv.DictReader(stream))
            self.assertEqual(rows[0]["connected_watts"], "80")
            self.assertEqual(rows[0]["unused_watts"], "10")
            with (output / "component_quantities.csv").open(encoding="utf-8-sig") as stream:
                quantities = list(csv.DictReader(stream))
            self.assertEqual(quantities[0]["component_category"], "power_nodes")
            self.assertEqual(quantities[0]["quantity"], "1")
            with self.assertRaises(ValueError):
                export_review(self.model, output)
        self.assertEqual(self.model, before)

    def test_provisional_export_labels_unknown_load_and_does_not_pass(self):
        self.model["design"]["fixture_selections"][0]["lv_input_watts"] = None
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "review"
            with self.assertRaises(ValueError):
                export_review(self.model, output)
            self.assertFalse(output.exists())
            report = export_review(self.model, output, allow_provisional=True)
            self.assertFalse(report["phase1_checks_pass"])
            with (output / "channel_schedule.csv").open(encoding="utf-8-sig") as stream:
                row = next(csv.DictReader(stream))
            self.assertEqual(row["connected_watts"], "")
            self.assertEqual(row["review_status"], "PROVISIONAL - BLOCKED")

    def test_structural_failures_never_export(self):
        self.model["facts"]["fixture_instances"][0]["fixture_type_id"] = "MISSING"
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaises(ValueError):
                export_review(self.model, Path(temporary) / "review", allow_provisional=True)

    def test_csv_escapes_source_formula_labels(self):
        self.model["facts"]["fixture_types"][0]["description"] = ' =HYPERLINK("example")'
        with tempfile.TemporaryDirectory() as temporary:
            export_review(self.model, Path(temporary))
            with (Path(temporary) / "lv_fixture_schedule.csv").open(encoding="utf-8-sig") as stream:
                row = next(csv.DictReader(stream))
            self.assertTrue(row["source_description"].startswith("'"))

    def test_nonfinite_json_and_duplicate_keys_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "bad.json"
            for text in ('{"watts": NaN}', '{"watts": Infinity}', '{"watts": 1, "watts": 2}'):
                path.write_text(text)
                with self.assertRaises(ValueError):
                    read_model(path)


if __name__ == "__main__":
    unittest.main()
