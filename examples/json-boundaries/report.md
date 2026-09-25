# Tailored run: unambiguous JSON research records

Status: **complete for the helper change, not an installed-agent benchmark**.

## Mission

The user requested an adversarial audit of Kakashi Learning. The concrete local task is to prevent ambiguous or malformed ledger inputs from looking like trustworthy research records. The environment is a stdlib-only Python CLI; no new dependency, remote execution, profile installation or publication is permitted by this run.

Metric: duplicate/non-finite/malformed input must receive a controlled input error while a well-formed draft remains valid. This is a binary correctness target, not a statistical claim about agent quality. The generated artifact is a patch to the existing audit helper and a strengthened verification procedure, not another redundant installed skill.

## Discovery and evidence

Mode: targeted supplied-source inspection. No broad repository search was needed once the issue was isolated. Budget: one repository, the relevant JSON documentation and license. Retrieved on 2026-09-25 UTC.

Inspected `python/cpython` at `68d86eb18a91226975eec5523d2d55d4796b1211`:

- [JSON docs, input-size caution](https://github.com/python/cpython/blob/68d86eb18a91226975eec5523d2d55d4796b1211/Doc/library/json.rst#L23-L26).
- [Ordered object-pair hook](https://github.com/python/cpython/blob/68d86eb18a91226975eec5523d2d55d4796b1211/Doc/library/json.rst#L295-L303).
- [Rejecting non-finite constants](https://github.com/python/cpython/blob/68d86eb18a91226975eec5523d2d55d4796b1211/Doc/library/json.rst#L330-L336).
- [License scope](https://github.com/python/cpython/blob/68d86eb18a91226975eec5523d2d55d4796b1211/LICENSE#L59-L70): the license text identifies PSF License Version 2 for software/documentation and a separate dual-license statement for examples. The GitHub metadata endpoint returned `NOASSERTION`, demonstrating why metadata alone is insufficient.

## What we kept and refused

**Adapt:** use stdlib JSON decoder hooks to reject duplicate keys and non-finite constants, then add bounded input/nesting and explicit type validation for this ledger. Original helper code was written locally; no upstream source or example code was copied. Local checks also cover numeric overflow to infinity, which constant parsing alone does not catch.

**Reject for this task:** permissive default JSON decoding as the entire ledger ingestion boundary. Duplicate keys can silently replace earlier declarations and non-finite numbers can enter a supposedly strict record. This is a contextual rejection, not a claim that Python's defaults are universally wrong.

**No new service or skill:** a new validator framework, vector database or crawler would not solve this failure. Extend the existing helper instead.

## Actual evaluation

See [`verification.txt`](verification.txt), generated from real local commands. It records the baseline standard-library decoding behavior, the revised test suite, a valid draft audit and this example's recorded-readiness gate. The tests include real subprocess invocations of the helper for representative and malformed inputs; they are not a fake GitHub API response or an installed-Hermes test.

The baseline `json.loads` probe is a controlled comparison with the previous ingestion method, not a re-execution of a saved old repository revision (the original project had no commit). Reported pre-fix URL and type failures are documented separately in `docs/audit.md`.

Reuse review: independently written code using documented stdlib interfaces; pinned source attribution retained here. This is not blanket legal clearance for copying CPython. Approval to install or publish remains absent.

## Limits

The gate can still accept a deliberately false receipt or status. No remote source existence check, automatic legal assessment or automated agent-effectiveness claim is made. Strict GitHub URL rules intentionally reject some unusual filenames. Real fresh-session skill activation, model-to-model comparisons and remote CI are not covered by these local tests.
