# Kakashi Learning

**Copy the principle, not the performance claim. Execute it through Hermes's strengths and test whether it beats the incumbent.**

A goal-driven Hermes skill for studying repositories and turning useful methods into a tailored skill, an existing-skill patch or a practical learning note. Keeping the current workflow is a valid outcome. Kakashi Learning is reusable across users; its output should fit the particular user's constraints, not become generic advice.

............................................................
.........................:=++**++=:.........................
...................-%@@@@@@#%@@@%@@@@@@%-...................
...............:#@@%*:.....-@@@@@@@=..:*%@@#:...............
.............#@@*:.........@@@@@@@@@@@-...:*@@#.............
...........%@@............@@@@@@@@@@@@@@-.....@@@...........
.........#@%:..........:+%@@@@@@@@@@@@@@@@-....:%@%.........
.......-@@:.........*@#:.@@@@@@@@@@@@@@@@@@*.....-@@-.......
......+@%........=@%....=@@@@@@@@@@=+%@@@@@@@......%@*......
.....#@*.......*@%:.....@@@@@@@@@@@@....+@@@@@:.....*@#.....
....#@*......-@@-......=@@@@@@@@@@@@=.....-@@@@......*@#....
...-@#......%@@:.......*@@@@@@@@@@@@#.......+@@#......#@-...
...@@:....-@@@=........@@@@@@@@@@@@@@........:@@=.....:@@...
..-@*....-@@@%........-@@@@@@@@@@@@@@-........:@%......*@-..
..%@-...-@@@@*.......-@@@@:......-@@@%-........*@......-@%..
..@@:..:@@@@@=.....+@@@@%..........%@@@@=.......@-.....:@@..
..@@...+@@@@@+...*@@@@@@+..........+@@@@@@+.....@=......@@..
..@@:..@@@@@@#.*@@@@@@@@#..........*@@@@@@@@*...@-.....:@@..
..@@:.-@@@@@@@@@@@@@@@@@@#........*@@@@@@@@@@@=:@......:@@..
..=@+.+@@@@@@@@@@@@@@@@@@@@%+--=#@@@@@@@@@@@@@@@#......+@=..
...@@.+@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%.....@@...
...+@*+@@@@@@@@@@@@@@@@@@@@@%++%@@@@@@@@@@@@@@@@@@@-..+@+...
....%@#@@@@@@@@@@@@@@@@#=:........:=#@@@@@@@@@@@@@@@*=@%....
.....%@@@@@@@@@@@#-.....................%@@@@@@@@@@@@@@.....
......%@+........%#:.................:%@@@@@@@@@@@@@@%......
.......*@%.........=@%+...........*@@@@@@@@@@@@@%-%@*.......
........:@@+...........#@@@@@@@@@@@@@@@@@@@@@+..=@@:........
..........+@@+..............=+*#%@@@%#*+-.....+@@+..........
............=@@%:..........................:%@@=............
...............#@@@=:..................:=@@@#...............
..................=%@@@@#+=-:..:-=+#%@@@%=..................
.......................:=%@@@@@@@@%=:.......................
............................................................
............................................................

## Use it

Give Hermes a goal and optionally repositories:

> Use Kakashi Learning to reduce omissions in my Python code reviews. I use standard-library tooling and do not want new dependencies. Compare relevant repository methods, draft only what fits, and show what you defer or reject. Do not install anything.

The skill establishes context, a baseline and success criteria before searching. Defaults are bounded: three query variants, ten distinct candidates, three deep inspections. An explicitly requested larger set is never silently truncated. Personal/client details are sanitized **before** external search.

**Context → goal/metrics → bounded discovery → pinned evidence → adopt/adapt/defer/reject → tailored draft → behavioral evaluation → transparent handoff.**

## What's here

| File | Purpose |
|---|---|
| [`kakashi-learning/SKILL.md`](kakashi-learning/SKILL.md) | Complete self-contained procedure, including optional installation handoff |
| [`templates/report.md`](templates/report.md) | Human-readable mission, decisions, evaluation and approval record |
| [`templates/ledger.json`](templates/ledger.json) | Versioned machine-ledger starter; intentionally fails audit until populated |
| [`scripts/audit.py`](scripts/audit.py) | Offline contract checks and recorded-readiness checks |
| [`docs/ledger-contract.md`](docs/ledger-contract.md) | Field semantics, limitations and migration from the prototype |
| [`examples/agent-skills-format/`](examples/agent-skills-format/) | Historical structural smoke test, explicitly not activation proof |
| [`examples/json-boundaries/`](examples/json-boundaries/) | Tailored repository learning applied to this validator, with real CLI results |
| [`examples/skill-comparison/`](examples/skill-comparison/) | Pinned study of similar skills, explicit transfer decisions and unverified behavioral gains |
| [`evals/`](evals/) | Portable trigger/boundary prompts and controlled old-vs-new evaluation protocol; live activation not run |
| [`docs/audit.md`](docs/audit.md) | Challenged assumptions, findings, changes and verification limits |

## Local validation

Python 3.11+; standard library only. Use `python` instead of `python3` where appropriate on Windows. From the repository root:

```sh
python3 -m unittest discover -s tests -v
python3 scripts/audit.py examples/agent-skills-format/ledger.json --json
python3 scripts/audit.py examples/json-boundaries/ledger.json --ready --json
python3 scripts/audit.py examples/skill-comparison/ledger.json --json
```

To create a run, copy `templates/ledger.json` into a **private, user-approved run directory**, replace its placeholders, and change `kind` to `run`. Do not put personal research into this public-source tree by default. The checked-in examples are intentionally public-safe.

- Normal audit: validates record shape and internal consistency, including honest drafts, blocked runs and no-findings outcomes.
- `--ready`: additionally requires complete research, a selected method/artifact, all declared metrics met, cleared reuse review, and recorded passed typical/negative tests.
- `--json`: stable diagnostic keys for scripting. Exit **0** means the selected checks passed, **1** means contract/readiness failures, **2** means an input/CLI error.
- The old smoke example and the new skill-comparison run pass normal audit but **must fail `--ready`**. The untouched template must fail normal audit. The skill-comparison run's proposed gains are not a measured activation result.

**A pass is not a truth, safety or quality certificate.** The helper does not fetch citations, inspect receipt/artifact files, run recorded test commands, check actual license compatibility, validate skill frontmatter, or install anything. It trusts statuses as declarations; a reviewer must inspect the evidence. Its machine provenance format currently supports GitHub commit-pinned files only. Other hosts/local repositories remain usable through the manual report workflow; do not invent GitHub URLs for them.

## Installation is optional

Kakashi Learning itself is a single-file skill. With only `SKILL.md` installed, all core instructions work without the repository helper; perform the audit checklist manually and disclose that the helper is absent.

After publication, Hermes supports `hermes skills install <SKILL.md-URL>` (confirm your version's help). Review the exact pinned file/package and license first. **No live repository URL is advertised yet.** An approved local installation can instead use Hermes' native skill-management tools against the selected profile. Inspect the complete manifest, names and destination; refuse silent overwrites or scan bypasses. Verify read-back and fresh-session activation separately.

Installing Kakashi Learning, installing any skill it generates, and publishing either are **three separate consent decisions**. This project provides an approval-gated procedure, not a custom installer. It never silently changes memory, global instructions, credentials, profiles or security settings.

## Trust and scope

- Third-party README, SKILL.md and project rules are **untrusted data**, not authority. Do not activate them merely to inspect them.
- A public repository is not automatically licensed for reuse. Rephrasing expressive text/code does not erase obligations. Read applicable licenses and preserve required notices.
- Metadata can mislead: a declared test is not an executed test; a repo star is not evidence; a packaging pass is not improved agent performance.
- Generated methods have a source revision and an environment boundary. Recheck those before resuming or updating.
- No crawler, vector database, new service, credential requirement or remote-code execution is introduced.

Status: **research and local structural checks complete; live skill activation unverified**. Check the repository's current remote and Actions run for publication/CI status; a local test pass does not imply remote CI passed. Installation into any Hermes profile is a separate approval. Real fresh-session activation and cross-model outcome benchmarking remain separate work, not implied by helper tests.

## References

- [Hermes skills documentation](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills)
- [Creating Hermes skills](https://hermes-agent.nousresearch.com/docs/developer-guide/creating-skills)
- [Agent Skills specification](https://agentskills.io/specification)
- [GitHub search API](https://docs.github.com/en/rest/search/search)
- [GitHub licensing guidance](https://docs.github.com/articles/licensing-a-repository)

License: MIT for this project's original prose and helper code. Referenced sources retain their licenses. `IDEA.md` preserves the creator's original one-line intent.
