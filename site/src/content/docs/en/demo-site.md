---
title: Demo site
description: The in-repo System Under Test — deterministic, offline, zero-dependency.
---

The demo site is a single HTML file (`demo/index.html`) with a sign-in gate
and a task list — enough surface for a real flow: add, rename, complete,
delete. It exists so a fresh clone can run its first flow in minutes: no
build step, no network, deterministic data.

## Serve it

```bash
python3 -m http.server 4173 -d demo     # from the repo root
# or: npx serve -l 4173 demo
```

## The demo account

| Field | Value |
|-------|-------|
| Email | `demo@flowtest.dev` |
| Password | `demo-password` |

Any other combination is rejected with a visible "Invalid credentials"
alert. The session lives in `sessionStorage` — a fresh browser session
starts signed out, so flow re-runs start clean. **Reset demo data** (app
footer) restores the seeded task list.

## Conventions flows rely on

- Every control has an accessible name, so semantic locators
  (`button 'Sign in'`, `textbox 'Email'`, `checkbox 'Buy oat milk'`)
  resolve without selectors.
- Extractable values are exposed as `data-field` spans — `open-count` and
  `done-count` in the summary line — which the `extract` action in
  `demo-smoke.flow.yaml` reads.

## Shipped example flows

| Flow | Journey |
|------|---------|
| `demo-smoke` | sign in → create a task → complete it → extract counters |

(Measured 2026-09-10: PASS, 9/9 steps, 70 s host-paced via agent-browser.)
