---
title: Quickstart
description: From a fresh clone to a passing flow in about two minutes.
---

You need a SKILL.md-convention host (Claude Code, zcode, …), Python 3 with
PyYAML, and any static file server. Measured end to end on 2026-09-10: the
smoke flow passes 9/9 steps in 70 seconds, host-paced.

## 1. Clone and serve the demo site

```bash
git clone https://github.com/jerryjiao/flowtest
cd flowtest
python3 -m http.server 4173 -d demo
```

The demo site is a single-page task list with a sign-in gate —
`demo@flowtest.dev` / `demo-password` — and list CRUD. Zero dependencies,
fully offline.

## 2. Ask your agent to run the flow

> Run the flow at `skills/flowtest/examples/demo-smoke.flow.yaml`.

The engine skill takes over:

1. **Validate** — the flow is checked by `scripts/validate_flow.py`.
2. **Resolve** — `{{PLACEHOLDER}}` variables resolve from the environment,
   `flowtest/.env`, then the flow's `vars` defaults.
3. **Run** — the agent drives a real browser (host browser MCP tools if the
   host has them, otherwise the `agent-browser` CLI), step by step.

## 3. Read the report

The run writes, before printing anything:

- `flowtest/reports/demo-smoke.<timestamp>.result.json` — machine-readable:
  verdict, per-step statuses, durations, evidence paths.
- `flowtest/reports/demo-smoke.<timestamp>.report.md` — the human version.
- `flowtest/screenshots/` — evidence for failures and heals.

```
flow demo-smoke: PASS — 9 steps (9 passed, 0 healed) in 70s
```

## 4. Test your own app

Serve it (or point at a deployed URL), then describe the journey:

> Test that a user can sign up with an email and see the confirmation
> screen.

The agent drafts a `.flow.yaml` under `flowtest/drafts/` and **waits for
your confirmation** before the browser opens. Confirmed flows move to
`flowtest/flows/` and re-run without asking again.

## Troubleshooting

- **PyYAML missing** — the validator exits with code 3 and says what to
  install (`pip install pyyaml`).
- **Port 4173 busy** — serve on another port and change `baseUrl` in the
  flow.
- **Re-run came back PARTIAL?** — the demo session lives in `sessionStorage`,
  and the flow's sign-in precheck skips when one is already active. Before
  re-running in the same browser, click **Reset demo data** and **Sign out**
  on the demo site. A fresh browser session starts signed out.
