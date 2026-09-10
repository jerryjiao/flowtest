# Run report — demo-smoke

| | |
|---|---|
| Flow | `demo-smoke` — Visitor can sign in, create a task, and complete it on the demo site |
| Result file | `demo-smoke.20260910-085722.result.json` |
| Backend | `agent-browser` 0.26.0 (CLI) |
| Started | 2026-09-10 08:56:12 UTC |
| Duration | 70 s (host-paced; wall clock including per-step snapshots) |
| SUT | demo site (`demo/index.html`) at `http://localhost:4173` |

## Verdict: PASS

9 steps: **9 passed, 0 healed, 0 failed, 0 skipped.**

## Steps

| # | Step | Action | Target | Status | Note |
|---|------|--------|--------|--------|------|
| 1 | `open-app` | goto | `/` | PASSED | heading “Sign in” present (precheck) |
| 2 | `fill-email` | fill | `textbox 'Email'` | PASSED | `{{DEMO_USER}}` resolved from flow vars |
| 3 | `fill-password` | fill | `textbox 'Password'` | PASSED | `{{DEMO_PASSWORD}}` resolved from flow vars |
| 4 | `submit-signin` | click | `button 'Sign in'` | PASSED | “Tasks” heading shown; no “Invalid credentials” |
| 5 | `name-task` | fill | `textbox 'New task'` | PASSED | setup phase |
| 6 | `add-task` | click | `button 'Add'` | PASSED | task text appears in the list |
| 7 | `complete-task` | click | `checkbox 'Buy oat milk'` | PASSED | verify phase |
| 8 | `confirm-done` | check | — | PASSED | list item present; screenshot captured |
| 9 | `grab-summary` | extract | `open-count`, `done-count` | PASSED | extracted `1` open, `2` done |

## Evidence

- Screenshot: `flowtest/screenshots/demo-smoke-confirm-done-1.png`

## Notes

- Semantic locators resolved on the first snapshot at every step — no heals,
  no CSS selectors. This is the demo site doing its job: every control has an
  accessible name.
- Variables were resolved from the flow's `vars` defaults; no `.env` needed.
