---
title: The engine loop
description: How Plan, Run, Report, and Learn actually behave.
---

The `flowtest` skill is the loop. Your agent is the runtime; the skill is
the procedure. Full procedures live in the repo under
`skills/flowtest/references/` ([plan](https://github.com/jerryjiao/flowtest/blob/main/skills/flowtest/references/plan.md),
[run](https://github.com/jerryjiao/flowtest/blob/main/skills/flowtest/references/run.md),
[report](https://github.com/jerryjiao/flowtest/blob/main/skills/flowtest/references/report.md),
[learn](https://github.com/jerryjiao/flowtest/blob/main/skills/flowtest/references/learn.md)).

## Plan

Interview the intent, read the SUT's pages (or its docs), check the
knowledge base for known traps, then draft a flow under `flowtest/drafts/`.
Validate, show the plan, **wait for confirmation** — a fresh plan never
executes unconfirmed. Confirmed flows live in `flowtest/flows/`.

## Run

Preflight (validate → resolve variables → resolve URLs), then a step loop:
snapshot the page, resolve the target, act, verify `expect` conditions,
record. Key behaviors:

- **A failed step does not stop the run** — the evidence of what still
  works is valuable. Only backend death or the whole-flow timeout skips the
  rest.
- **Self-heal is bounded** — at most 2 attempts per step, classified by
  failure type (timeout / element not found / assertion), strategies
  recorded. Healing never edits the flow file, and a healed exact-match
  says so.
- **Executor-neutral** — the agent maps flow primitives onto whatever
  browser automation the host provides: host browser MCP tools first,
  `agent-browser` CLI second (measured — see
  [ADR-0002](https://github.com/jerryjiao/flowtest/blob/main/docs/adr/0002-executor-priority.md)).

## Report

The result JSON is written **before** any summary. It carries per-step
statuses, durations, heal strategies, extracted values, evidence paths, and
the verdict (`PASS` / `PARTIAL` / `FAIL`). The report step turns it into
the human-facing `.report.md` — verdict first, then per-step table, then
evidence.

## Learn

A failed run that produces no lesson will fail again. Learn distills the
failure into a note — what trap, which flows it affects, how to avoid it —
and ingests it via the [knowledge base](/flowtest/en/kb/) skill. Without a
KB configured, lessons degrade to plain markdown under `flowtest/lessons/`.
