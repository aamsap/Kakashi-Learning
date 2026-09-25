"""Guard the human-run skill evaluation set against vacuous examples."""
import json
import subprocess
import sys
import unittest
from pathlib import Path

CASES = Path(__file__).resolve().parents[1] / "evals" / "cases.json"


class EvaluationCasesTests(unittest.TestCase):
    def test_skill_comparison_remains_a_draft_not_a_ready_claim(self):
        root = CASES.parent.parent
        ledger = root / "examples" / "skill-comparison" / "ledger.json"
        audit = root / "scripts" / "audit.py"
        regular = subprocess.run([sys.executable, str(audit), str(ledger), "--json"], capture_output=True, text=True)
        self.assertEqual(regular.returncode, 0, regular.stdout + regular.stderr)
        ready = subprocess.run([sys.executable, str(audit), str(ledger), "--ready", "--json"], capture_output=True, text=True)
        self.assertEqual(ready.returncode, 1, ready.stdout + ready.stderr)
        self.assertFalse(json.loads(ready.stdout)["valid"])

    def test_each_boundary_has_a_decision_and_check(self):
        entries = json.loads(CASES.read_text(encoding="utf-8"))["cases"]
        self.assertGreaterEqual(len(entries), 6)
        names = set()
        buckets = set()
        for item in entries:
            self.assertIn(item["bucket"], {"trigger", "non_trigger", "boundary"})
            self.assertIn(item["expected_route"], {"kakashi", "other", "clarify"})
            self.assertTrue(item["prompt"].strip())
            self.assertTrue(item["expected_behavior"].strip())
            self.assertTrue(item["observable_check"].strip())
            self.assertNotIn(item["id"], names)
            names.add(item["id"])
            buckets.add(item["bucket"])
        self.assertEqual(buckets, {"trigger", "non_trigger", "boundary"})
        self.assertTrue(any(item["expected_route"] == "other" for item in entries))

    def test_comparison_protocol_explains_limits(self):
        protocol = (CASES.parent / "README.md").read_text(encoding="utf-8")
        for phrase in ("old skill", "same task", "activation", "not run"):
            self.assertIn(phrase, protocol.lower())


if __name__ == "__main__":
    unittest.main()
