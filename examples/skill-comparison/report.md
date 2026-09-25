# Kakashi run: learn from adjacent skill workflows

Status: **draft**. Research and local edits completed; agent behavior improvement is **not measured**. [Machine ledger](ledger.json) records the four inspected candidates and technique decisions. Search hits not inspected are accounted for below, not represented as evaluated candidates.

## Mission and incumbent

Sir's standard: Kakashi is a Copy Ninja who improves a jutsu by executing it through his own strengths, not by mimicking it. For this repository, the target is a **better goal-fit Hermes procedure**. The incumbent v0.2 already had bounded search, pinned evidence, explicit refusals, a no-findings result and install consent. The missing operational test was whether a learned method beats that incumbent for a user task, and whether the skill triggers only where appropriate. Those are the gaps, not a mandate to import more skills.

Current constraints: public-safe research only, no profile installation, no third-party script execution, no publishing. Web search used sanitized generic terms. Four targeted queries returned five items apiece; this is 20 result slots, **not** a claim of 20 unique repos. Four distinct, relevant repositories were deeply inspected at pinned commits. Provider totals were not reported. Stop reason: four complementary method families identified within this search budget; other hits were not inspected and could still be useful.

### Search-hit accounting

The following are the **16 returned slots not deeply inspected**. This is a search-result log, not a quality judgment or a claim about each repository's license/content. The first query's five hits were broad collections; the second and third produced the four inspected sources plus the listed alternatives; the fourth concerned wider self-improvement patterns rather than a narrow skill-evaluation procedure.

| Query theme | Other returned hits (not inspected) | Boundary reason |
|---|---|---|
| Repository learning/adaptation | `jurgendn/agent-skills`, `orchestra-research/AI-research-SKILLs`, `sreerevanth/AI-Agent-Skills`, `jbrhsn/agent_skills`, `addyosmani/agent-skills` | Collection-level results; prioritized four focused skills from the other queries. |
| Skill creation/evaluation | `anthropics/claude-plugins-official`, `microsoft/agent-skills`, `jeremylongshore/claude-code-plugins-plus-skills` | Alternate skill-creator entries; focused on the pinned Anthropic and OpenClaw files instead. |
| Skill discovery | `CodeSigils/skill-discovery` (mirror result), `naimkatiman/repo-skill-advisor`, `wyattowalsh/agents` | More discovery approaches beyond the two inspected discovery/overlap sources. |
| Self-improvement | `GrayCodeAI/iterate`, `juandelossantos/another-agent-skills`, `zhaono1/agent-playbook`, `yologdev/yoyo-evolve`, a SkillsLLM directory listing | Broad self-improvement results outside the focused skill-level transfer test. |

The ledger's `candidates` means the four **selected for pinned inspection**, not all search results. These identities come from returned titles/URLs only; none of their files, licenses or behavior was assessed. No fork/mirror deduplication beyond these slots is asserted.

## Pinned sources and technique decisions

| Source | What its file establishes | Kakashi decision and local change |
|---|---|---|
| [Anthropic skill-creator, pinned SKILL.md § running evals](https://github.com/anthropics/skills/blob/33375500bcea98d610eb30ce10ac4e59b89c390d/skills/skill-creator/SKILL.md#L163-L188) | For revising a skill, compare old and new on the same evaluation prompt; its tooling is Claude-specific. [License](https://github.com/anthropics/skills/blob/33375500bcea98d610eb30ce10ac4e59b89c390d/skills/skill-creator/LICENSE.txt) is Apache-2.0. | **Adapt principle:** a minimal Hermes paired-run protocol. Rejected importing its runner, viewer, token benchmark machinery and any inference that a single run proves improvement. |
| [OpenClaw skill-eval, pinned SKILL.md § workflow](https://github.com/SaluteYB/openclaw-skill-eval/blob/b25fb1a23a48a41448dc020b99d8c233f6ca63fe/skill-eval/SKILL.md#L20-L39) | Differentiates should-trigger, should-not-trigger, boundary and execution-quality cases. [License](https://github.com/SaluteYB/openclaw-skill-eval/blob/b25fb1a23a48a41448dc020b99d8c233f6ca63fe/LICENSE) is MIT. | **Adapt principle:** nine original, Hermes-targeted routing scenarios in `evals/cases.json`; no upstream template copied. Static dataset validity checked, actual activation still unrun. |
| [Skill Hunter, pinned SKILL.md § inspection/overlap](https://github.com/CE0Alex/skill-hunter/blob/05fe1cbc4d8f56a7c3674f7c4573519fc3fb4db3/SKILL.md#L126-L147) | Inspect fit, compatibility and overlap before recommendation. [License](https://github.com/CE0Alex/skill-hunter/blob/05fe1cbc4d8f56a7c3674f7c4573519fc3fb4db3/LICENSE) is MIT. | **Adapt principle:** transfer test in Kakashi: upstream method → incumbent strength/gap → Hermes-native implementation → expected advantage over both → failure condition. Reject its heavyweight mandatory registry matrix/intake for this task. |
| [Skill Seeker, pinned SKILL.md § exclusions/install](https://github.com/mmmantasrrr/skill-seeker/blob/09fbad7830e8155c71017dd0942d27fc13f09cb3/skills/seeking-skills/SKILL.md#L16-L33) | Its own exclusions include simple tasks and domains with a loaded skill; it offers install and project-profile commands. [License](https://github.com/mmmantasrrr/skill-seeker/blob/09fbad7830e8155c71017dd0942d27fc13f09cb3/LICENSE) is MIT. | **Retain the boundary; reject the shortcut:** no global discovery for local bugs and no installation/profile persistence during research. Existing Kakashi approval gate remains. |

These citations show **documented upstream techniques**. They do not prove that the revision improves Hermes behavior. The source text was treated as evidence, not instructions; no scripts were executed, no upstream material copied. License identification is not a legal clearance claim.

## Transfer versus mimicry

- **Original jutsu:** iterate a skill against evaluation tasks.
- **Current strength:** Hermes has its own tools, existing skills, user context and separate approval gates; v0.2 already extracts evidence safely.
- **Adaptation:** use those strengths to avoid redundant skills and to grade **whether the learned approach actually improves the user's task versus the incumbent**. Full-repo evaluation prompts are optional: the single-file skill retains three small built-in boundary prompts.
- **Failure condition:** if the same task under comparable conditions shows no gain, worse safety or higher unjustified maintenance cost, defer the imported idea or revert the revision. A neat report or passing unit tests alone does not prove benefit.

## Checks and limitations

Local tests validate the eval-set contract and existing ledger checks. A controlled old-vs-new Hermes activation run has **not** been performed, so metrics in the ledger remain `unverified` and `--ready` must fail. The previous skill was uncommitted, so no byte-for-byte immutable v0.2 baseline exists; the old procedure can be reconstructed from prior audit/session history if an authorized isolated test is later needed. A single session or cherry-picked prompt would be insufficient to claim a reliable superiority result.

New or modified local artifacts: `kakashi-learning/SKILL.md`, `templates/report.md`, `evals/cases.json`, `evals/README.md`, `tests/test_eval_cases.py`, this report and ledger, and README links. Nothing installed, committed or published.
