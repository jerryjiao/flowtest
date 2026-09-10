# T7 — E2E quickstart verification on a clean environment (2026-09-10)

The maintainer gate from the spec's testing decisions: follow only the
published docs, on a fresh clone with no maintainer shortcuts, and prove the
newcomer path end-to-end including one seeded failure that exercises Learn.

## Setup

- Fresh clone of the **public** repo (`https://github.com/jerryjiao/flowtest`)
  into a temporary directory, at `f5dd0bf` (= tag `v0.1.0`).
- Tooling a newcomer would have on this machine: Python 3 + PyYAML,
  `agent-browser` 0.26.0, `knowflow` 0.5.0, any static file server.
- Path followed: **README Quickstart only** — clone, `python3 -m http.server
  4173 -d demo`, run the shipped example flow.

## Results

| Check | Result |
|---|---|
| Demo site serves from the clone | 200 OK |
| Validate `skills/flowtest/examples/demo-smoke.flow.yaml` | OK (exit 0) |
| Run 1 — real browser, 9 steps | **PASS 9/9, 0 healed, 0 failed — 46 s host-paced** |
| Three artifact classes | `.result.json` (verdict PASS) + `.report.md` + screenshot on disk |
| Run 2 — determinism (after *Reset demo data* + *Sign out*) | **PASS 9/9 again; same counters (open=1, done=2)** |
| Seeded failure (`demo-lesson`: wrong password, expects `heading 'Tasks'`) | **FAIL as designed** — page stays on *Sign in*, shows `Invalid credentials`; screenshot captured |
| Learn | lesson distilled → `knowflow ingest` into the clone's `flowtest/kb` (raw captured) → synthesized wiki page `status: pending` (user review gate) → Plan-style keyword query (`grep -ri "invalid credentials" flowtest/kb/wiki/`) recalls it alongside the existing notes |

Newcomer-relevant time to first passing flow: **~2 minutes** (clone + serve +
validate ≈ 30 s; browser run 46 s; result/report writing under a minute) —
well inside the ~10-minute target. The seeded-failure + Learn loop added
≈ 4 minutes, including one CLI detour recorded below.

## Friction log

All non-blocking; filed as [#10](https://github.com/jerryjiao/flowtest/issues/10).

1. Re-running the demo flow in a browser that already holds demo-site state
   yields PARTIAL instead of PASS until *Reset demo data* + *Sign out* are
   clicked. Clean-profile newcomers never hit it.
2. The `knowflow` CLI resolves its workspace from the CWD — run from the repo
   root it silently creates a new workspace instead of using `flowtest/kb/`.
3. `agent-browser` resolves relative screenshot paths against its daemon's
   CWD, not the invoking shell's.

## Verdict

**T7 passes.** The published path is complete (no undocumented required
step), the three artifact classes land, the seeded failure produces a Learn
note behind the review gate, and the timing claim holds with wide margin.
