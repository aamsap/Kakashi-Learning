"""Synthetic contract fixtures, not claims about real repositories or test runs."""
import copy
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("audit", ROOT / "scripts/audit.py")
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


def report():
    return {
        "schema_version": 2,
        "kind": "run",
        "status": "draft",
        "goal": "Reduce review omissions",
        "context": {"task": "Author a safe skill", "environment": "Hermes with Python", "constraints": ["No installation"], "assumptions": [], "existing_skills": [], "missing_capabilities": []},
        "discovery": {"mode": "provided", "budget": "one supplied repository", "stop_reason": "supplied repository inspected"},
        "metrics": [{"name": "omissions", "target": "zero omissions", "method": "same checklist before and after", "baseline": "unknown", "observation": "not measured", "status": "unverified"}],
        "searches": [],
        "candidates": [{"repo": "example/source", "commit": "a" * 40, "license": "MIT", "disposition": "inspected", "reason": "Relevant to the task"}],
        "decisions": [{"technique": "Review checklist", "outcome": "adapt", "reason": "Addresses omission metric", "metric": "omissions", "confidence": "documented", "evidence": [{"url": "https://github.com/example/source/blob/" + "a" * 40 + "/README.md#L1-L4", "note": "Checklist described in docs"}], "reuse": {"mode": "idea", "status": "needs_review", "note": "No text copied; review pending"}, "tests": [{"case": "typical", "status": "not_run", "method": "Apply to a normal authoring task", "result": "Pending execution"}, {"case": "negative", "status": "not_run", "method": "Untrusted source instruction", "result": "Pending execution"}]}],
        "risks": ["No behavior test yet"],
        "artifacts": [],
    }


class ContractTests(unittest.TestCase):
    def test_nested_type_mutations_never_raise(self):
        base = report()
        paths = []

        def collect(value, path):
            if isinstance(value, dict):
                for key, child in value.items():
                    paths.append(path + [key])
                    collect(child, path + [key])
            elif isinstance(value, list):
                for index, child in enumerate(value):
                    paths.append(path + [index])
                    collect(child, path + [index])

        collect(base, [])
        for path in paths:
            for value in (None, True, 0, "", [], {}):
                data = copy.deepcopy(base)
                parent = data
                for key in path[:-1]:
                    parent = parent[key]
                parent[path[-1]] = value
                with self.subTest(path=path, value=value):
                    self.assertIsInstance(audit.validate(data), list)
                    self.assertIsInstance(audit.validate(data, ready=True), list)

    def test_evidence_cannot_escape_pinned_commit(self):
        prefix = "https://github.com/example/source/blob/" + "a" * 40 + "/"
        for suffix in ("../main/README.md", "%2e%2e/main/README.md", "%252e%252e/main/README.md", "#L1", "?raw=1", "folder/../../main/README.md", "folder/%5c../file", "README.md\n", "README.md?ref=main"):
            with self.subTest(suffix=suffix):
                data = report()
                data["decisions"][0]["evidence"][0]["url"] = prefix + suffix
                self.assertTrue(any("evidence" in e for e in audit.validate(data)))

    def test_version_is_required(self):
        data = report()
        del data["schema_version"]
        self.assertTrue(any("schema_version" in e for e in audit.validate(data)))

    def test_unverified_draft_is_valid_but_not_ready(self):
        data = report()
        self.assertEqual(audit.validate(data), [])
        self.assertTrue(audit.validate(data, ready=True))

    def test_real_template_is_explicitly_not_a_run(self):
        import json
        data = json.loads((ROOT / "templates/ledger.json").read_text())
        self.assertTrue(any("template" in e for e in audit.validate(data)))

    def test_no_findings_is_honest_valid_outcome(self):
        data = report()
        data.update(status="no_findings", candidates=[], decisions=[])
        data["discovery"]["mode"] = "search"
        data["searches"] = [{"query": "some specific task", "source": "GitHub", "total_count": 0, "returned_count": 0}]
        self.assertEqual(audit.validate(data), [])
        self.assertTrue(audit.validate(data, ready=True))

    def test_unavailable_repo_needs_reason_not_fake_sha(self):
        data = report()
        data.update(status="blocked", decisions=[])
        data["candidates"][0].update(commit=None, disposition="unavailable", reason="Access denied", license="unknown")
        self.assertEqual(audit.validate(data), [])

    def test_candidate_duplicates_are_rejected(self):
        data = report()
        data["candidates"].append(copy.deepcopy(data["candidates"][0]))
        self.assertTrue(any("duplicate" in e for e in audit.validate(data)))

    def test_placeholder_commit_is_rejected(self):
        data = report()
        data["candidates"][0]["commit"] = "0" * 40
        self.assertTrue(any("commit" in e for e in audit.validate(data)))

    def test_search_count_cannot_exceed_total(self):
        data = report()
        data["searches"] = [{"query": "topic", "source": "GitHub", "total_count": 1, "returned_count": 2}]
        self.assertTrue(any("count" in e for e in audit.validate(data)))

    def test_unknown_metric_reference_rejected(self):
        data = report()
        data["decisions"][0]["metric"] = "invented"
        self.assertTrue(any("metric" in e for e in audit.validate(data)))

    def test_untyped_tests_not_accepted(self):
        data = report()
        data["decisions"][0]["tests"] = "Passed, trust me"
        self.assertTrue(any("tests" in e for e in audit.validate(data)))

    def test_ready_requires_measurements_reuse_and_both_test_cases(self):
        data = report()
        data["status"] = "complete"
        data["metrics"][0].update(baseline="two omissions", observation="zero omissions", status="met")
        data["decisions"][0]["reuse"]["status"] = "cleared"
        for test in data["decisions"][0]["tests"]:
            test.update(status="passed", result="Synthetic fixture success", receipt="tests/test_contract.py")
        data["artifacts"] = ["kakashi-learning/SKILL.md"]
        self.assertEqual(audit.validate(data, ready=True), [])
        data["decisions"][0]["tests"][1]["status"] = "failed"
        self.assertTrue(audit.validate(data, ready=True))


if __name__ == "__main__":
    unittest.main()
