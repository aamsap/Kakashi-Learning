# Audit: challenge, findings and changes

Second requested audit of the Kakashi Learning prototype: challenge and improve skill workflow, technical capabilities, contextual awareness, transparency. Two independent read-only reviews were dispatched (adversarial validator review; workflow/intent review); their findings and the fixes applied are below. Nothing was installed or published as part of this audit.

## What was wrong

**Validator (`scripts/audit.py`)**
- A "pinned" evidence URL could smuggle dot-segment/encoded traversal that resolves to a mutable branch, not the cited commit.
- Valid-but-unexpected JSON types (lists/dicts/numbers/bool in string fields) crashed the validator with a Python traceback instead of a clean error.
- License-gate string comparison was whitespace/case sensitive and order-dependent: `" unknown "` passed, and duplicate `(repo, commit)` entries let a later record silently overwrite an earlier license.
- An untouched template passed validation and printed "Reviewable," implying real research had occurred.
- The ledger schema had no way to express context, discovery boundary, metric baseline/observation, evidence confidence, or an honest zero-findings/blocked outcome — an empty `candidates`/`decisions` list simply failed.
- No input-size, nesting-depth, duplicate-key or non-finite-number guard on the JSON decoder.

**Workflow (`SKILL.md`, templates, README)**
- The procedure proceeded unconditionally toward drafting even when nothing fit the goal, pressuring fabricated adaptations.
- Discovery happened before any privacy boundary was set, so private task details could leak into external search queries.
- "Agreed budget" and "small shortlist" were undefined.
- No place to record personalization context (user, task, environment, constraints, existing skills) even though the mission step asked for it verbally.
- The only worked example validated frontmatter shape, not any executed or tailored behavior — it was labeled honestly as a smoke test but nothing distinguished structural pass from behavioral evidence at the schema level.
- Install-approval language existed but wasn't backed by a manifest/verification procedure in the ledger contract.

## What changed

- Ledger schema versioned (`schema_version: 2`, `kind: run|template`, `status: draft|complete|blocked|no_findings`) with `context`, `discovery`, metric baseline/observation/status, evidence confidence, reuse review, and structured tests with receipts. See `docs/ledger-contract.md` for the full field contract.
- Evidence URLs are parsed structurally (`urllib.parse`) and rejected on empty path, dot segments, backslashes, control characters, or noncanonical host, instead of being pattern-matched and silently normalized.
- All type checks run before membership/string operations; malformed input across every field was fuzz-tested (`tests/test_contract.py::test_nested_type_mutations_never_raise`) to guarantee a clean `errors` list, never a traceback.
- License comparison normalizes `strip().casefold()`; duplicate `(repo, commit)` candidates are a hard error, not a silent overwrite.
- The template (`templates/ledger.json`) now has `kind: template` and fails audit by design; a real run must be copied out and its `kind` changed to `run`. The historical example fails `--ready` on purpose (structural pass only).
- `no_findings` and `blocked` statuses are valid with empty `candidates`/`decisions`; `--ready` still requires a complete run with a selected artifact, met metrics, cleared reuse, and passed typical+negative tests.
- Input hardening: 2,000,000-byte cap, nesting depth 32, duplicate-key rejection, non-finite number rejection.
- `SKILL.md` rewritten (v0.2.0): sanitize search queries before discovery (step 2), explicit default budget (3 queries / 10 candidates / 3 deep inspections), `no_findings` as a first-class outcome (step 4 exit criterion), evidence confidence labels (observed/documented/inferred), a genuine reuse-review distinction (idea vs. adapted vs. verbatim expression), and an installation handoff procedure requiring manifest/hash review, conflict handling, and activation verification separate from "files installed."
- Added `examples/json-boundaries/` — a second, tailored example that actually exercises this repository's own validator against a real bug class (ambiguous JSON intake), with real subprocess test output captured in `verification.txt`, distinct from the historical structural-only smoke test.

## Verification of that audit pass (historical; not the current suite size)

- `python3 -m unittest discover -s tests -v` — 24 tests, all passing (`examples/json-boundaries/verification.txt`, lines 5–34).
- `python3 scripts/audit.py examples/agent-skills-format/ledger.json --json` — valid, `readiness_checked: false` (historical smoke example correctly cannot claim readiness).
- `python3 scripts/audit.py examples/json-boundaries/ledger.json --ready --json` — valid, `readiness_checked: true` (the new tailored example meets the stricter gate on real evidence).
- `python3 scripts/audit.py templates/ledger.json --json` — now correctly **fails** (`kind must be run; a template is not a completed research record`), closing the "untouched template passes" finding.

The later skill-comparison work added `tests/test_eval_cases.py`, bringing the currently verified local suite to **27 tests**. See `examples/skill-comparison/report.md` for its separate, still-unverified behavioral claims; the 24-test receipt above remains an authentic record of the earlier pass.

## Still unverified / out of scope for this pass

- No fresh-session Hermes activation test of the installed skill (installation was never requested or performed).
- No cross-model or multi-run behavioral benchmark of an agent actually using Kakashi Learning end-to-end.
- License clearance is evidence-backed but not a legal certification; `reuse.status: cleared` remains a declaration for human/reviewer confirmation.
- Remote GitHub Actions CI has not executed (no commit/push yet); only local runs are verified above.

## Pre-publication challenge of the skill-comparison increment

An independent read-only review found no hard blocker in the pinned citations, applicable license references, public-file scan or local contract checks. It did find two documentation defects, both corrected before publication:

1. `examples/skill-comparison/report.md` described 20 search-result slots but identified only four deeply inspected sources. It now names all 16 uninspected slots by query, explains why inspection stopped, and labels search snippets as **unassessed** rather than rejected repositories. The four pinned inspections remain the only machine-ledger candidates. The slot reconciliation was checked programmatically: 5 + 3 + 3 + 5 uninspected = 16, plus four inspected = 20.
2. The 24-test receipt above was easy to mistake for the current suite. Its heading now marks it historical; the later comparison work added three tests for a current local total of **27**.

The CI workflow now checks both the recorded-ready JSON-boundaries example and the draft skill-comparison ledger, in addition to the historical example. A local run under the Python 3.11 Hermes venv passed all 27 tests and the three CI ledger checks. This is a pre-push review, **not** remote CI execution or an old-versus-new skill activation benchmark. No commit, remote or publication is claimed.
