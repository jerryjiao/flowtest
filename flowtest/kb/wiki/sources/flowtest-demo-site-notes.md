---
type: source
title: flowtest demo site product notes
created: 2026-09-10
created_from: raw/web/2026-09-10-1703-text.md
status: reviewed
source_url: http://localhost:4173
---

# flowtest demo site product notes

## 一句话总结

The in-repo demo site (System Under Test for the smoke flow): a single-page
task list with a sign-in gate, list CRUD, and extractable counters — the
surface every shipped example flow targets.

## 核心要点

- Served as a static file from `demo/index.html` on port 4173; the sign-in
  gate accepts demo@flowtest.dev / demo-password, any other combination is
  rejected with a visible "Invalid credentials" alert (EXTRACTED)
- The "Invalid credentials" alert node stays in the DOM hidden at all
  times — it is only made visible on rejection (EXTRACTED)
- Signed-in app: heading "Tasks"; create via textbox "New task" + button
  "Add"; complete via the per-task checkbox whose accessible name equals the
  task text; rename inline via "Edit" (Enter saves, Escape cancels); remove
  via "Delete" (EXTRACTED)
- The summary line exposes extractable counters as `data-field` spans:
  `open-count` and `done-count` (EXTRACTED)
- "Reset demo data" restores the seeded task list — "Set up flowtest" done,
  "Write first flow" open (EXTRACTED)
- Session lives in sessionStorage (a fresh browser session starts signed
  out); tasks live in localStorage, so flows survive reloads within one
  session but reset across sessions (EXTRACTED)

## 提取的实体

- [[entities/flowtest-demo-site]] — the SUT these notes describe
- [[entities/demo-smoke-flow]] — the shipped smoke flow that exercises this
  surface end to end

## 提取的概念

- Semantic locators — every control on the site has an accessible name so
  flow targets like `checkbox 'Buy oat milk'` resolve without CSS selectors
- Phases (`precheck`/`setup`/`verify`) — the smoke flow relies on the
  signed-out start as its `precheck`
