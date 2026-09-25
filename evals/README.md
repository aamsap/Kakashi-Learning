# Skill evaluation cases

These prompts test routing and execution quality. They are **unrun scenarios**, not evidence that the skill activates correctly. The structural test only checks this dataset is usable. Do not report a passing unit test as model behavior.

For a real evaluation of a change to Kakashi Learning:

1. Save the **old skill** contents before editing and pin the new draft. Keep all prompts in `cases.json` unchanged for that round.
2. Run each **same task** in isolated, comparable Hermes sessions with old and new skill, using the same model/settings, allowed tools, task files and privacy scope. If loading a skill needs installation, ask separately; do not install on the user's live profile simply to benchmark. Use a dedicated test profile only with permission and verify activation, or record `not_run`.
3. Capture the actual triggered/not-triggered choice, tool actions, outputs, elapsed time/tokens if truly observable, errors and artifact hashes. Grade the predefined `observable_check` plus manual source support, adaptation quality and safety. A "decided to use" narrative does not prove skill **activation**.
4. Compare old/new per case, then summarize improvements, regressions, unchanged results and uncertainty. Avoid numerical success claims from one nondeterministic run. Repeat representative cases when variance matters.
5. Record a negative case for the newly imported technique and a follow-up case where the method should win over the original, not merely imitate its vocabulary. Keep real receipts in a private run directory unless reviewed for public release.

The cases are intentionally small and portable. This repository does not ship an automated LLM harness, does not execute source code found in researched repositories, and has **not run** this behavioral evaluation yet. Normal `unittest` and `audit.py --ready` checks are not a substitute for it.
