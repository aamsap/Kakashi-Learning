# Ledger contract, version 2

This is an offline record validator, not an agent runner, license scanner or installer. The narrative report remains necessary for contextual reasoning. Extra fields are permitted for notes but **not validated**; they cannot replace required fields. Only the documented fields affect gates. No ledger content is executed or fetched, and no referenced local path is opened.

## Required root fields

- `schema_version`: integer `2`. Older unversioned ledgers are rejected, not silently upgraded.
- `kind`: `run`. The starter uses `template` so untouched templates cannot masquerade as research.
- `status`: `draft`, `complete`, `blocked`, `no_findings`. Complete describes research completion, not readiness or consent. Draft allows selected methods with unrun tests. Blocked records access/capability barriers. No-findings may have zero candidates or only rejected/deferred techniques; it cannot contain adopt/adapt decisions.
- `goal`: nonempty task outcome.
- `context`: `task`, `environment` strings, and lists of strings `constraints`, `assumptions`, `existing_skills`, `missing_capabilities`. Empty lists mean none recorded, not proof none exist. Record non-goals, proficiency, user-stated preferences, privacy scope and observed/assumed distinctions in the narrative report as needed; do not expose sensitive originals.
- `discovery`: `mode` (`search`, `provided`, `offline`), `budget`, `stop_reason`. The strings describe the actual scope, not a promise of exhaustive coverage. Search mode needs a search record unless explicitly blocked.
- `metrics`: nonempty list with unique `name`, plus `target`, `method`, `baseline`, `observation` strings and `status` (`met`, `not_met`, `unverified`). Unknown baseline/observation must be explicit. State the evaluation conditions in the report.
- `searches`: list of `query`, `source`, `total_count` (nonnegative integer or null if unknown), `returned_count` (nonnegative integer, not greater than a known total). Booleans are not counts. Counts are per recorded query/page boundary, not asserted totals of all repository inspections. An empty list is valid for supplied/offline work.
- `candidates`: distinct repositories, fields below. Can be empty for no-findings or blocked work.
- `decisions`: technique-level decisions, fields below. A complete run requires decisions; no-findings/blocked/draft can have none.
- `risks`, `artifacts`: lists of nonempty strings, possibly empty. Artifact paths are pointers only. The validator does not open them or grant access.

## Candidates and evidence

Each candidate has `repo` (`owner/repo`), `commit` (full lowercase 40-character Git SHA for inspected sources), `license` (declared label or `unknown`), `disposition` (`inspected`, `skipped`, `unavailable`) and `reason`.

No zero-SHA placeholders. An uninspected source may have `commit: null`; it cannot supply pinned evidence for a technique decision. Case-insensitive duplicate repository identities are rejected instead of overwriting license claims. Consolidate observations at the revision chosen for this run. A source access failure requires draft/blocked status, not a completed no-findings result. Use candidate reasons for inaccessible repos rather than fabricating a technique/evidence record.

Every decision needs `technique`, `outcome` (`adopt`, `adapt`, `defer`, `reject`), `reason`, `metric` (a listed metric name), `confidence` (`observed`, `documented`, `inferred`), and nonempty `evidence`.

Evidence entries have `url` and `note`. URLs must be HTTPS GitHub blob files at the exact listed inspected commit. Optional line fragments are supported. Empty paths, dot segments, encoded separators/dot traversal, residual double encoding, backslashes, control characters, query strings and noncanonical hosts are rejected, not normalized. This conservative format rejects some unusual but legitimate filenames; cite another unambiguous file or use manual reporting. It does **not** prove the SHA/file/lines exist or that the note follows from the source. Dated issues and web documentation belong in supplemental narrative evidence, not as substitutes for a pinned implementation/specification.

## Selected techniques: reuse and tests

Adopt/adapt entries also need:

- `reuse`: `mode` (`idea`, `adaptation`, `verbatim`), `status` (`cleared`, `needs_review`, `blocked`) and `note`. Note the actual applicable license evidence, obligations, preserved notices and reviewer rationale. Cleared is a declaration, not legal advice. Unknown licenses cannot be marked cleared for expression reuse. An independently expressed idea is distinct from copying, but that distinction still requires judgment; do not relabel copying as an idea to avoid review.
- `tests`: nonempty list of `case` (`typical`, `negative`), `status` (`passed`, `failed`, `not_run`), `method`, `result`. Executed tests additionally need `receipt`, a location of observed output. It is not opened or authenticated. A structural check must be described as structural, not as a task demonstration.

With `--ready`, the validator additionally requires complete status, at least one selected technique and artifact, every metric declared met, every selected reuse review cleared, every recorded selected test passed, and both typical and negative cases. This is a **recorded prerequisites gate**, not proof of measurements or a safe installation. A self-reported lie can pass. Independent review of source, receipts and artifacts remains essential.

## Input limits and outputs

UTF-8 JSON, at most 2,000,000 bytes and nesting depth 32. Duplicate keys and non-finite numbers are rejected. No network access or third-party dependencies. Exit codes: 0 selected checks passed; 1 validation errors; 2 unreadable/malformed/oversized input or CLI usage. `--json` emits `valid`, `readiness_checked`, `status`, `errors`, `limits` for ledger validation/input errors. Argparse help and argument errors retain standard argparse output. Input diagnostics avoid echoing raw report content.

## Migration from the initial prototype

1. Add version/kind/status and contextual mission/discovery fields. Do not infer missing facts; use draft/unverified and explain gaps.
2. Replace ambiguous `result_count` with separate total/returned counts, preserving historical dates and boundaries.
3. Convert candidate free-text dispositions to the enumerated disposition plus reason. Remove fake SHAs; mark inaccessible sources explicitly.
4. Add metric baseline/observation/status, decision metric reference and evidence confidence.
5. Replace a free-text `test` with structured tests and receipt pointers; add reuse review. Do not manufacture tests for an old report.
6. Add artifacts/risks; run normal audit. `--ready` is optional and should fail for incomplete historical examples.

Approval manifests and publication review live in the human report, not a boolean that would invite automated installation. This repository intentionally has no installer.
