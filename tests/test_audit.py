import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from test_contract import report

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "audit.py"


def valid_report():
    data = report()
    data["decisions"].append({"technique": "automatic loading", "outcome": "reject", "reason": "Would trust unknown material", "metric": "omissions", "confidence": "inferred", "evidence": data["decisions"][0]["evidence"]})
    return data


class AuditTests(unittest.TestCase):
    def test_json_type_mutations_never_crash(self):
        for field, values in (("outcome", [[], {}, 1, None]), ("license", [[], {}, 1, None])):
            for value in values:
                with self.subTest(field=field, value=value):
                    report = valid_report()
                    target = report["decisions"][0] if field == "outcome" else report["candidates"][0]
                    target[field] = value
                    result = self.run_audit(report)
                    self.assertEqual(result.returncode, 1, result.stderr)
                    self.assertNotIn("Traceback", result.stderr)

    def run_audit(self, report, *args):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "report.json"
            path.write_text(json.dumps(report), encoding="utf-8")
            return subprocess.run([sys.executable, str(SCRIPT), str(path), *args], capture_output=True, text=True)

    def test_cli_json_distinguishes_valid_draft_from_readiness(self):
        result = self.run_audit(valid_report(), "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["valid"])
        self.assertEqual(payload["status"], "draft")
        self.assertFalse(payload["readiness_checked"])
        result = self.run_audit(valid_report(), "--ready", "--json")
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertFalse(json.loads(result.stdout)["valid"])

    def test_cli_malformed_files_are_input_errors(self):
        payloads = [b'\xff', b'{"goal":1,"goal":2}', b'{"goal":NaN}', b'{"extra":1e999}', b'[' * 1100 + b']' * 1100, b' ' * 2_000_001]
        for payload in payloads:
            with self.subTest(payload=payload[:30]), tempfile.TemporaryDirectory() as tmp:
                path = Path(tmp) / "bad.json"
                path.write_bytes(payload)
                result = subprocess.run([sys.executable, str(SCRIPT), str(path), "--json"], capture_output=True, text=True)
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertNotIn("Traceback", result.stderr)
                self.assertFalse(json.loads(result.stdout)["valid"])

    def test_skill_frontmatter_is_installable_single_file(self):
        skill = (ROOT / "kakashi-learning" / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(skill.startswith("---\n"))
        metadata = skill.split("\n---\n", 1)[0]
        self.assertIn("name: kakashi-learning", metadata)
        description = next(line.partition(": ")[2] for line in metadata.splitlines() if line.startswith("description: "))
        self.assertLessEqual(len(description), 60)
        self.assertTrue(description.endswith("."))
        self.assertIn("## Verification", skill)
        self.assertNotIn("Read `references/", skill)

    def test_valid_reviewed_report_passes(self):
        result = self.run_audit(valid_report())
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_unpinned_source_fails(self):
        report = valid_report()
        report["candidates"][0]["commit"] = "main"
        result = self.run_audit(report)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("commit", result.stderr)

    def test_missing_reason_for_rejection_fails(self):
        report = valid_report()
        report["decisions"][1]["reason"] = ""
        result = self.run_audit(report)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("reason", result.stderr)

    def test_adoption_requires_test_and_known_license(self):
        report = valid_report()
        report["candidates"][0]["license"] = "unknown"
        report["decisions"][0]["tests"] = ""
        report["decisions"][0]["reuse"] = {"mode": "adaptation", "status": "cleared", "note": "Synthetic invalid clearance"}
        result = self.run_audit(report)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("license", result.stderr)
        self.assertIn("test", result.stderr)

    def test_unrelated_unlicensed_candidate_does_not_block_adoption(self):
        report = valid_report()
        report["candidates"].append({"repo": "other/project", "commit": "b" * 40, "license": "unknown", "disposition": "skipped", "reason": "Unrelated"})
        result = self.run_audit(report)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_malformed_evidence_reports_error_without_traceback(self):
        report = valid_report()
        report["decisions"][0]["evidence"][0]["url"] = 17
        result = self.run_audit(report)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("evidence", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_unreferenced_source_fails(self):
        report = valid_report()
        report["decisions"][0]["evidence"][0]["url"] = "https://github.com/other/repo/blob/" + "b" * 40 + "/README.md"
        result = self.run_audit(report)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("evidence", result.stderr)


if __name__ == "__main__":
    unittest.main()
