---
title: Introduction
description: What flowtest is, who it is for, and the shape of the loop.
---

flowtest is **natural-language browser testing for coding agents**. You
describe a user journey; your agent turns it into a `.flow.yaml` plan, runs
it in a real browser, records a screenshot and a timing for every step, and
writes failures down as notes.

It ships as **agent skills, not a framework**. Your existing coding agent
(Claude Code, zcode, or any host that follows the SKILL.md convention) is
the runtime — there is no new service to install and no daemon.

## The loop

- **Plan** — a plain-language intent ("a user can add a product to the cart
  and check out") becomes a structured `.flow.yaml` you can read, edit, and
  version. Nothing executes before you confirm it.
- **Run** — the agent drives a real browser step by step using semantic
  locators (`button 'Sign in'`, `textbox 'Email'`) — no CSS selectors, and
  nothing to update when the page is redesigned.
- **Report** — every step lands as `PASSED` / `HEALED` / `FAILED` /
  `SKIPPED` with a screenshot and a timing; the result is written to disk
  first, then a summary is generated.
- **Learn** — failed runs distill into knowledge-base notes (optional,
  [KnowFlow](https://github.com/jerryjiao/knowflow)) so future Plans avoid
  known traps.

## What it is not

- Not a test framework — no runner process, no config matrix, nothing to
  migrate to.
- Not a cloud service — everything runs on your machine, in your agent.
- Not multi-project orchestration — one System Under Test (SUT) at a time.

## Repository map

| Path | What it is |
|------|------------|
| `skills/flowtest/` | The engine skill: Plan → Run → Report → Learn, flow format, validator |
| `skills/flowtest-kb/` | The memory skill: a local KnowFlow workspace of lessons |
| `demo/` | A zero-dependency demo site — the default SUT |
| `flowtest/` | A live workspace: example run artifacts + a seeded KB |
| `tests/` | Flow-format validator tests + repo structure & scrub gates |

Next: the [Quickstart](/flowtest/en/quickstart/) — your first passing flow
in about two minutes.
