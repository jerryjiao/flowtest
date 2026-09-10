---
title: The flow format
description: .flow.yaml v1 — one YAML file per user journey.
---

A Flow is a YAML test plan describing one user journey: an ordered list of
steps against a System Under Test (SUT), each with an action, an optional
target, and optional expected conditions. A flow file is written both for
humans to read and for machines to validate: it reads in one screen and
validates mechanically.

```bash
python3 skills/flowtest/scripts/validate_flow.py path/to/flow.flow.yaml
```

The full contract lives in
[`skills/flowtest/references/flow-format.md`](https://github.com/jerryjiao/flowtest/blob/main/skills/flowtest/references/flow-format.md);
this page is the tour.

## A flow, in brief

```yaml
flow: demo-smoke
title: "Visitor can sign in, create a task, and complete it"
sut: demo-site
baseUrl: http://localhost:4173
tags: [smoke, demo]
vars:
  DEMO_USER: demo@flowtest.dev

steps:
  - id: submit-signin
    action: click
    target: "button 'Sign in'"
    expect:
      - element: "heading 'Tasks'"
      - not_text: "Invalid credentials"
```

## Steps

Every step has a kebab-case `id`, an `action` from a closed set
(`goto`, `click`, `fill`, `select`, `hover`, `press`, `wait`, `check`,
`extract`), an optional `target`, and an `expect` list — every condition
must hold for the step to pass.

### Targets are semantic locators

1. Role and name: `button 'Sign in'`, `textbox 'Email'`, `heading 'Tasks'`
2. Role plus position when names repeat: `button 'Add' (first)`
3. Plain language as a last resort — the host agent resolves it against a
   page snapshot

No CSS/XPath: a control with no accessible name is an accessibility bug in
your app worth filing, not something to work around with a selector.

### Expect conditions

`text`, `not_text`, `url`, `title`, `element` — existence checks are
preferred over exact-value matches unless the test data is controlled.
`not_text` is a **visibility** assertion: hidden DOM nodes do not count.

### Phases

`precheck` (fail fast, skip the flow), `setup` (create data), `verify`
(the journey under test — default), `conclude` (summarize/clean up).

## Variables

`{{NAME}}` placeholders may appear in any string field. At run time:
environment first, then `flowtest/.env` (never committed), then the flow's
`vars` defaults. Unresolved placeholders stop the run before the browser
opens. **No secrets in flows.**

## Statuses

Steps end `PASSED`, `HEALED` (passed only after a bounded self-heal retry —
recorded, and weaker evidence), `FAILED`, or `SKIPPED` (with a reason). The
flow-level verdict derives from them: `PASS`, `PARTIAL`, `FAIL`.
