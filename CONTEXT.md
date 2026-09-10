# Glossary

- **Flow** — a YAML test plan (`.flow.yaml`) describing one user journey: steps, targets, assertions. The core artifact everything else reads or produces.
- **Engine** — the `flowtest` skill running the Plan → Run → Report → Learn loop against a Host.
- **Host** — the coding agent executing the skills (Claude Code, zcode, or any SKILL.md-convention runtime). flowtest never ships its own agent loop.
- **Demo Site** — the in-repo, offline web app that serves as the default System Under Test, so a fresh clone can run its first flow in minutes.
- **System Under Test (SUT)** — whatever web app a Flow targets; the Demo Site is one instance, the user's own app is another.
- **Knowledge Base (KB)** — a [KnowFlow](https://github.com/jerryjiao/knowflow) workspace holding product docs and failure notes, queried during Plan. Optional.
- **Learn** — the step where failed runs are distilled into KB notes so future Plans avoid known traps.
- **Result** — the `.result.json` written by every run: per-step statuses (PASSED / HEALED / FAILED / SKIPPED), timings, evidence paths, and the flow-level verdict (PASS / PARTIAL / FAIL). Reports and lessons are derived from it.
