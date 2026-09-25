#!/usr/bin/env python3
"""Offline ledger contract checks. Never executes tests or certifies truth/safety."""
import argparse
import json
import math
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

SHA = re.compile(r"^[0-9a-f]{40}$")
OUTCOMES = {"adopt", "adapt", "defer", "reject"}


def present(value):
    return isinstance(value, str) and bool(value.strip())


def source_key(url):
    """Reject ambiguous URLs rather than normalizing away provenance defects."""
    if not present(url) or any(c.isspace() or ord(c) < 32 or ord(c) == 127 for c in url) or "\\" in url:
        return None
    try:
        parsed = urlsplit(url)
    except ValueError:
        return None
    if parsed.scheme != "https" or parsed.netloc != "github.com" or parsed.query:
        return None
    if parsed.fragment and not re.fullmatch(r"L[1-9][0-9]*(?:-L[1-9][0-9]*)?", parsed.fragment):
        return None
    segments = parsed.path.split("/")
    if len(segments) < 6 or segments[3] != "blob" or not SHA.fullmatch(segments[4]):
        return None
    for segment in segments[1:]:
        decoded = unquote(segment)
        # Residual '%' rejects double encoding; encoded separators change path identity.
        if not decoded or decoded in (".", "..") or any(c in decoded for c in ("/", "\\", "%")) or any(ord(c) < 32 or ord(c) == 127 for c in decoded):
            return None
    return (segments[1] + "/" + segments[2], segments[4])


def validate(report, ready=False):
    errors = []
    if not isinstance(report, dict):
        return ["report must be an object"]
    if type(report.get("schema_version")) is not int or report["schema_version"] != 2:
        return ["schema_version must be 2; migrate old ledgers explicitly"]
    if report.get("kind") != "run":
        return ["kind must be run; a template is not a completed research record"]
    status = report.get("status")
    if status not in ("draft", "complete", "blocked", "no_findings"):
        errors.append("status must be draft/complete/blocked/no_findings")
    if not present(report.get("goal")):
        errors.append("goal is required")
    for field in ("metrics", "searches", "candidates", "decisions", "risks", "artifacts"):
        if not isinstance(report.get(field), list):
            errors.append(f"{field} must be a list")
    if errors:
        return errors
    context = report.get("context")
    if not isinstance(context, dict):
        errors.append("context must describe the task, environment and constraints")
    else:
        for field in ("task", "environment"):
            if not present(context.get(field)):
                errors.append(f"context.{field} is required")
        for field in ("constraints", "assumptions", "existing_skills", "missing_capabilities"):
            if not isinstance(context.get(field), list) or not all(present(x) for x in context[field]):
                errors.append(f"context.{field} must be a list of nonempty strings")
    discovery = report.get("discovery")
    if not isinstance(discovery, dict):
        errors.append("discovery must describe mode, budget and stop_reason")
    else:
        if discovery.get("mode") not in ("search", "provided", "offline"):
            errors.append("discovery.mode must be search/provided/offline")
        for field in ("budget", "stop_reason"):
            if not present(discovery.get(field)):
                errors.append(f"discovery.{field} is required")
        if discovery.get("mode") == "search" and not report["searches"] and status != "blocked":
            errors.append("search mode needs searches (or an explicitly blocked run)")
    if not report["metrics"]:
        errors.append("metrics must be nonempty")
    metric_names = set()
    for index, metric in enumerate(report["metrics"]):
        label = f"metrics[{index}]"
        if not isinstance(metric, dict):
            errors.append(f"{label} must be an object")
            continue
        for field in ("name", "target", "method", "baseline", "observation"):
            if not present(metric.get(field)):
                errors.append(f"{label}.{field} is required")
        name = metric.get("name")
        if present(name):
            if name in metric_names:
                errors.append(f"{label}.name is a duplicate")
            metric_names.add(name)
        if metric.get("status") not in ("met", "not_met", "unverified"):
            errors.append(f"{label}.status must be met/not_met/unverified")
        if ready and metric.get("status") != "met":
            errors.append(f"{label} is not measured and met")
    for index, search in enumerate(report["searches"]):
        label = f"searches[{index}]"
        if not isinstance(search, dict):
            errors.append(f"{label} must be an object")
            continue
        if not all(present(search.get(k)) for k in ("query", "source")):
            errors.append(f"{label} needs query and source")
        total, returned = search.get("total_count"), search.get("returned_count")
        if "total_count" not in search or (total is not None and (type(total) is not int or total < 0)):
            errors.append(f"{label}.total_count must be nonnegative or null if unknown")
        if type(returned) is not int or returned < 0:
            errors.append(f"{label}.returned_count must be nonnegative")
        elif type(total) is int and returned > total:
            errors.append(f"{label}.returned_count exceeds total_count")
    sources = {}
    seen_repos = set()
    for index, candidate in enumerate(report["candidates"]):
        label = f"candidates[{index}]"
        if not isinstance(candidate, dict):
            errors.append(f"{label} must be an object")
            continue
        repo, commit = candidate.get("repo"), candidate.get("commit")
        valid_repo = present(repo) and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9-]*/[A-Za-z0-9_.-]+", repo) and repo.split("/")[1] not in (".", "..")
        if not valid_repo:
            errors.append(f"{label}.repo must be owner/repo")
        elif repo.lower() in seen_repos:
            errors.append(f"{label}.repo is a duplicate; consolidate it")
        else:
            seen_repos.add(repo.lower())
        disposition = candidate.get("disposition")
        if disposition not in ("inspected", "skipped", "unavailable"):
            errors.append(f"{label}.disposition must be inspected/skipped/unavailable")
        valid_commit = isinstance(commit, str) and SHA.fullmatch(commit) and commit != "0" * 40
        if not valid_commit and (disposition == "inspected" or commit is not None):
            errors.append(f"{label}.commit needs a non-placeholder 40-character SHA (null only if not inspected)")
        if not present(candidate.get("license")):
            errors.append(f"{label}.license needs a value (unknown if unresolved)")
        if not present(candidate.get("reason")):
            errors.append(f"{label}.reason is required")
        if valid_repo and valid_commit and disposition == "inspected":
            sources[(repo, commit)] = candidate.get("license")
    selected = 0
    for index, decision in enumerate(report["decisions"]):
        label = f"decisions[{index}]"
        if not isinstance(decision, dict):
            errors.append(f"{label} must be an object")
            continue
        for field in ("technique", "reason"):
            if not present(decision.get(field)):
                errors.append(f"{label}.{field} is required")
        if not isinstance(decision.get("outcome"), str) or decision["outcome"] not in OUTCOMES:
            errors.append(f"{label}.outcome must be adopt/adapt/defer/reject")
        if not present(decision.get("metric")) or decision["metric"] not in metric_names:
            errors.append(f"{label}.metric must reference a listed metric name")
        if decision.get("confidence") not in ("observed", "documented", "inferred"):
            errors.append(f"{label}.confidence must be observed/documented/inferred")
        evidence = decision.get("evidence")
        referenced = []
        if not isinstance(evidence, list) or not evidence:
            errors.append(f"{label}.evidence needs a pinned URL and note")
            evidence = []
        for item in evidence:
            url = item.get("url") if isinstance(item, dict) else None
            note = item.get("note") if isinstance(item, dict) else None
            key = source_key(url)
            if key is None or key not in sources or not present(note):
                errors.append(f"{label}.evidence must reference a listed repo at its pinned commit with a note")
            else:
                referenced.append(sources[key])
        if decision.get("outcome") not in ("adopt", "adapt"):
            continue
        selected += 1
        reuse = decision.get("reuse")
        if not isinstance(reuse, dict):
            errors.append(f"{label}.reuse needs mode, status and note")
        else:
            if reuse.get("mode") not in ("idea", "adaptation", "verbatim"):
                errors.append(f"{label}.reuse.mode must be idea/adaptation/verbatim")
            if reuse.get("status") not in ("cleared", "needs_review", "blocked") or not present(reuse.get("note")):
                errors.append(f"{label}.reuse needs a review status and explanation")
            if ready and reuse.get("status") != "cleared":
                errors.append(f"{label}.reuse has unresolved license/attribution review")
            if reuse.get("mode") != "idea" and reuse.get("status") == "cleared" and any(not present(x) or x.strip().lower() in ("unknown", "none", "no license", "noassertion") for x in referenced):
                errors.append(f"{label}.license is unknown; expression reuse cannot be cleared")
        tests = decision.get("tests")
        if not isinstance(tests, list) or not tests:
            errors.append(f"{label}.tests must be a nonempty list, including explicit not_run cases")
            continue
        cases = set()
        for number, test in enumerate(tests):
            test_label = f"{label}.tests[{number}]"
            if not isinstance(test, dict):
                errors.append(f"{test_label} must be an object")
                continue
            if test.get("case") not in ("typical", "negative"):
                errors.append(f"{test_label}.case must be typical/negative")
            else:
                cases.add(test["case"])
            if test.get("status") not in ("passed", "failed", "not_run"):
                errors.append(f"{test_label}.status must be passed/failed/not_run")
            for field in ("method", "result"):
                if not present(test.get(field)):
                    errors.append(f"{test_label}.{field} is required")
            if test.get("status") in ("passed", "failed") and not present(test.get("receipt")):
                errors.append(f"{test_label}.receipt must locate recorded evidence")
            if ready and test.get("status") != "passed":
                errors.append(f"{test_label} has not passed")
        if ready and cases != {"typical", "negative"}:
            errors.append(f"{label}.tests need both typical and negative cases")
    for field in ("risks", "artifacts"):
        if not all(present(x) for x in report[field]):
            errors.append(f"{field} must contain only nonempty strings")
    if status in ("complete", "no_findings") and any(isinstance(c, dict) and c.get("disposition") == "unavailable" for c in report["candidates"]):
        errors.append("unavailable candidates require draft or blocked status, not a completed finding")
    if status == "complete" and not report["decisions"]:
        errors.append("complete needs decisions; use no_findings or blocked instead")
    if status == "no_findings" and selected:
        errors.append("no_findings cannot contain adopted/adapted techniques")
    if ready and (status != "complete" or not selected or not report["artifacts"]):
        errors.append("ready requires complete status, a selected technique and a draft artifact")
    return errors


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key")
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError("non-finite JSON number")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path)
    parser.add_argument("--ready", action="store_true", help="check recorded adoption prerequisites, not permission to install")
    parser.add_argument("--json", action="store_true", help="machine-readable diagnostics")
    args = parser.parse_args()
    report = None
    try:
        with args.report.open("rb") as stream:
            content = stream.read(2_000_001)
        if len(content) > 2_000_000:
            raise ValueError("report exceeds 2 MB limit")
        report = json.loads(content.decode("utf-8"), object_pairs_hook=unique_object, parse_constant=reject_constant)
        pending = [(report, 0)]
        while pending:
            value, depth = pending.pop()
            if depth > 32:
                raise ValueError("report nesting exceeds 32 levels")
            if isinstance(value, float) and not math.isfinite(value):
                raise ValueError("non-finite JSON number")
            if isinstance(value, (list, dict)):
                children = value.values() if isinstance(value, dict) else value
                pending.extend((child, depth + 1) for child in children)
        errors = validate(report, ready=args.ready)
        code = 1 if errors else 0
    except (OSError, ValueError, RecursionError) as exc:
        errors, code = [f"Input error ({type(exc).__name__}): cannot read a bounded, unique-key UTF-8 JSON ledger"], 2
    result = {
        "valid": not errors, "readiness_checked": args.ready,
        "status": report.get("status") if isinstance(report, dict) else None,
        "errors": errors,
        "limits": "Offline contract check only: no source fetching, test execution, legal clearance or install approval.",
    }
    if args.json:
        print(json.dumps(result, ensure_ascii=True))
    elif errors:
        for error in errors:
            print(error, file=sys.stderr)
    else:
        label = "Recorded readiness checks passed" if args.ready else "Ledger structure valid"
        print(f"{label}; status={report['status']}. {result['limits']}")
    return code


if __name__ == "__main__":
    sys.exit(main())
