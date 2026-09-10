---
type: source
title: "Lesson: not_text means visible text — hidden DOM nodes false-fail naive assertions"
created: 2026-09-10
created_from: raw/web/2026-09-10-1704-text.md
status: reviewed
source_url: 
---

# Lesson: not_text means visible text — hidden DOM nodes false-fail naive assertions

## 一句话总结

A failed sign-in assertion during the 2026-09-10 executor measurement was a
harness bug, not a product bug: absence checks must filter for visibility,
because error nodes commonly live in the DOM permanently, hidden.

## 核心要点

- `not_text` conditions in a flow mean "the string is not **visible** on the
  page", not "absent from the DOM" (EXTRACTED)
- The demo site keeps its "Invalid credentials" alert permanently in the DOM
  (hidden until shown) — a naive text-count assertion counts the hidden node
  and false-fails a passing sign-in (EXTRACTED)
- When writing flows, keep `not_text` strings unique on the page so even
  visibility-blind executors cannot trip over incidental copies (INFERRED:
  the demo hint text originally repeated the literal error string, which
  would have made this trap worse)
- Not every Playwright surface exposes `isChecked()`; verify checkbox state
  through observable effects — summary counters or snapshot state — instead
  (EXTRACTED)

## 提取的实体

- [[entities/demo-smoke-flow]] — the flow whose sign-in step surfaced this
  trap
- [[entities/flowtest-demo-site]] — the SUT whose alert node triggered it

## 提取的概念

- Self-heal vs harness bug — this failure was in the driving harness, the
  kind of failure Learn must attribute correctly or the lesson poisons
  future plans

## 与其他来源的关系

- 与 [[sources/flowtest-demo-site-notes]] 的关系: **互补**
- The product notes describe the always-present alert node; this lesson is
  what that implementation detail means for assertions.
