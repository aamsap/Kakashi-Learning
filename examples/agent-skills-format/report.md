# Smoke run: portable skill structure

**Goal:** Produce a compact Hermes skill with a pinned evidence trail, without silently granting permissions from a researched repository. This is a *workflow smoke test*, not proof of improved agent performance.

## Boundary and search

- Query: `agent skills specification in:name,description` using GitHub repository search; API reported **303** results and returned five on the requested first page. Only `agentskills/agentskills` was inspected for this smoke test, selected as the format specification. The other results were not assessed.
- Inspected `docs/specification.mdx` at commit `69ef37e9424c0a7ea9dd2293b559e43ec8176379` via GitHub API. GitHub reports its license as Apache-2.0. [Pinned source](https://github.com/agentskills/agentskills/blob/69ef37e9424c0a7ea9dd2293b559e43ec8176379/docs/specification.mdx).

## Kakashi decisions

- **Adapt:** A required `SKILL.md` with optional companion files (lines 6-16 of the pinned source). Our skill's essential procedure lives in one file; ledger tooling remains optional. We wrote original instructions, not a copied specification.
- **Reject:** Automatic tool grants from an upstream `allowed-tools` field. That field is marked experimental in the inspected frontmatter table (lines 19-32) and is inappropriate for generated skills that analyze untrusted repositories.

## Actual verification

- `python3 -m unittest discover -s tests -v` returned **8 tests, OK**. The tests cover the skill file's basic shape and ledger success/failure paths, including an unpinned source and missing rejection reason.
- `python3 scripts/audit.py examples/agent-skills-format/ledger.json` returned `Reviewable ledger: 1 candidates, 2 decisions`.
- These checks do **not** demonstrate a measurable time saving or a live Hermes activation. Activation needs a separate approved installation and a fresh session. Claims about semantic source accuracy and license obligations still need human review.

**Gained:** a self-contained skill and an auditable accept/reject format. **Refused:** unreviewed permission transfer. **Pending:** broader repository comparisons, real-user task benchmarking, installation and publication approvals.
