---
name: flowtest
description: |
  Natural-language browser testing engine: turn a user journey into a .flow.yaml
  plan, run it in a real browser, report pass/fail with evidence, and learn from
  failures. Use when the user wants to plan a flow (describe a journey to test,
  "test that...", "write a flow"), run a flow (a .flow.yaml path, "run the flow",
  "run tests"), report on a run (a .result.json or .flow.yaml path, "test report"),
  or learn from a failure ("why did this flow fail", "save this lesson").
  Not for generic "check this code" or unit testing — this drives a real browser
  against a running web app.
---

# flowtest — browser test engine

You (the host agent) are the runtime. This skill is the loop:
**Plan** (intent → `.flow.yaml`) → **Run** (browser, step by step) →
**Report** (structured results + evidence) → **Learn** (failures become
knowledge-base notes that sharpen the next Plan).

The flow format contract is [references/flow-format.md](references/flow-format.md)
— read it before writing or editing any flow. Examples live in
[examples/](examples/).

## Workspace layout

All artifacts live under `flowtest/` in the System Under Test's repository
(never in the user's home directory):

```
flowtest/
  flows/          confirmed flows: <flow>.flow.yaml
  drafts/         unconfirmed plans: <flow>.draft.flow.yaml
  reports/        per-run artifacts: <flow>.<YYYYMMDD-HHMMSS>.result.json and .report.md
  screenshots/    <flow>-<step-id>-<n>.png
  kb/             KnowFlow workspace (optional — the flowtest-kb skill's home)
  lessons/        failure notes when no KB exists (degraded Learn)
  .env            optional variable overrides (gitignore it)
```

Create missing directories on first use. Suggest gitignoring `.env` and
`screenshots/`; flows, reports, and the reviewed `kb/` wiki belong in version
control.

## Routing

| User intent | Procedure | Detail |
|-------------|-----------|--------|
| Describes a journey to test, or names this skill with "plan" | **Plan** | [references/plan.md](references/plan.md) |
| Gives a `.flow.yaml` path, or says run/execute a flow | **Run** | [references/run.md](references/run.md) |
| Gives a `.result.json`/`.flow.yaml` path and wants a report | **Report** | [references/report.md](references/report.md) |
| Asks why a run failed, or wants a lesson captured | **Learn** | [references/learn.md](references/learn.md) |

Default to **Run** when a flow path is present, **Plan** otherwise. After any
run with failures, offer Learn (do not force it).

## Core rules

- **Flows are the artifact.** Everything else — runs, reports, lessons —
  references flow and step ids. Never execute a journey that exists only in
  conversation: write it as a flow first.
- **Validate before use.** `python3 <skillDir>/scripts/validate_flow.py <file>`
  gates every draft→flow promotion and every run. Invalid flows are fixed, not
  run.
- **Ask before executing anything new.** A fresh plan always gets user
  confirmation before the browser opens. Re-running an existing, previously
  confirmed flow needs no new confirmation.
- **Evidence or it didn't happen.** Failures and heals are screenshotted; the
  result JSON is written before any summary is spoken.
- **No secrets in flows.** Credentials come from `{{PLACEHOLDER}}` variables
  resolved at run time (environment or `flowtest/.env`) — never literal in the
  YAML.
- **Browser backend is pluggable.** Drive whatever browser automation the host
  provides (host browser MCP tools, e.g. Playwright-style, or an
  `agent-browser` CLI); [run.md](references/run.md) defines the detection and
  mapping. Flows stay backend-neutral.
- **Learn is the multiplier.** A failed run that produces no lesson will fail
  again. When Learn runs, it distills the failure into a note ingested via the
  `flowtest-kb` skill.
