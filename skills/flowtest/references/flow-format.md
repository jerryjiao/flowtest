# The `.flow.yaml` format (v1)

A Flow is a YAML test plan describing one user journey: an ordered list of
steps against a System Under Test (SUT), each with an action, an optional
target, and optional expected conditions. Flows are written for humans and
agents alike — short enough to read in one screen, strict enough to validate
mechanically.

Validate any flow with the shipped validator (the Plan and Run steps call it
automatically):

```bash
python3 <skillDir>/scripts/validate_flow.py path/to/flow.flow.yaml
```

## Example

```yaml
flow: guest-checkout
title: "Guest can add a product to the cart and check out"
sut: demo-site
baseUrl: http://localhost:4173
tags: [smoke, cart]
vars:
  COUPON: WELCOME10

steps:
  - id: open-catalog
    action: goto
    target: /products
    expect:
      - text: "All products"

  - id: add-first-product
    action: click
    target: "button 'Add to cart' (first)"
    expect:
      - text: "Added to cart"

  - id: apply-coupon
    action: fill
    target: "textbox 'Coupon'"
    value: "{{COUPON}}"

  - id: confirm-discount
    action: check
    expect:
      - text: "Discount applied"
      - not_text: "Invalid code"
```

## Top-level keys

| Key | Required | Type | Meaning |
|-----|----------|------|---------|
| `flow` | ✔ | kebab-case slug | Flow identifier; also the file stem (`<flow>.flow.yaml`) |
| `title` | ✔ | string | One-sentence, user-journey phrasing — what a human would call this test |
| `steps` | ✔ | non-empty list | Ordered steps; see below |
| `description` | | string | Context for future readers: why this journey matters |
| `sut` | | string | Which System Under Test this flow targets (name or base URL) |
| `baseUrl` | | string | Prepended to relative `goto` targets |
| `tags` | | list of strings | Grouping labels (`smoke`, `regression`, domain names) |
| `timeout` | | positive number | Whole-flow budget in seconds (default 300) |
| `stepTimeout` | | positive number | Per-step budget in seconds (default 60) |
| `vars` | | map, scalar values | Defaults for `{{PLACEHOLDER}}` substitution; environment variables and `flowtest/.env` override them |

Unknown top-level keys are validation errors — the key set is closed so typos
fail fast instead of silently doing nothing.

## Steps

Every step is a mapping with:

| Key | Required | Type | Meaning |
|-----|----------|------|---------|
| `id` | ✔ | kebab-case slug | Stable identifier, unique within the flow; used in results, screenshots, and learned notes |
| `action` | ✔ | see actions table | What to do |
| `target` | for most actions | string | What to act on — see "Targets" below |
| `value` | for some actions | string / number / list | The fill text, key, wait duration, or extract field list |
| `expect` | | list of conditions | Conditions checked after the action; all must hold |
| `phase` | | `precheck` \| `setup` \| `verify` \| `conclude` | Lifecycle label (see "Phases") |
| `screenshot` | | boolean | Force a screenshot after this step (defaults: after failures and heals) |
| `timeout` | | positive number | Per-step budget override in seconds |
| `note` | | string | Free-form comment for maintainers |

### Actions

| Action | Needs `target` | Needs `value` | Semantics |
|--------|:---:|:---:|-----------|
| `goto` | ✔ | | Navigate; target is a URL or a path resolved against `baseUrl` |
| `click` | ✔ | | Click the element |
| `fill` | ✔ | ✔ | Type the value into the input (replaces content) |
| `select` | ✔ | ✔ | Choose the option in the dropdown |
| `hover` | ✔ | | Hover the element |
| `press` | | ✔ | Press a key (`Enter`, `Tab`, …); target optional |
| `wait` | | ✔ | Pause for `value` milliseconds — use sparingly; prefer `expect` |
| `check` | | | Act on nothing; assert the `expect` conditions against the current page |
| `extract` | | ✔ | Read the fields listed in `value` (list of names) into the run result, for reports and later analysis |

### Targets

`target` is deliberately executor-neutral so the same flow runs under any
browser backend (decision on the default backend is pending measurement; see
the consensus plan). Write targets as **semantic locators** in this style,
most-to-least preferred:

1. Role and name: `"button 'Sign in'"`, `"textbox 'Email'"`, `"heading 'Tasks'"`,
   `"checkbox 'Buy oat milk'"`, `"combobox 'Shipping'"`
2. Role plus position when names repeat: `"button 'Add' (first)"`,
   `"listitem 'Buy oat milk' (2)"`
3. Plain language as a last resort: `"the product card for 'Oat milk'"` — the
   host agent resolves it against a page snapshot

Avoid CSS/XPath selectors in flows: they encode implementation detail and rot
on redesigns. If an element has no accessible name, that is an accessibility
bug in the SUT worth filing.

### Expect conditions

`expect` is a list; each item is a mapping with exactly one key:

| Condition | Passes when |
|-----------|-------------|
| `text: "..."` | The string is visible anywhere on the page |
| `not_text: "..."` | The string is **not** visible anywhere on the page |
| `url: "..."` | The current URL contains the string |
| `title: "..."` | The page title contains the string |
| `element: "..."` | An element matching the semantic locator exists and is visible |

Prefer existence checks (`element`, `text`) over exact-value matches unless
the test data is controlled — flaky exact-match assertions are the most
common way flows go wrong. If nothing else fits, a `check` step with several
loose conditions beats one brittle condition.

### Phases

Label steps with `phase` so readers (and the Learn step) can tell structure
from detail:

- `precheck` — fail fast if preconditions are missing (seeded data, logged-out
  state). A failing precheck skips the flow with a reason, it does not fail it.
- `setup` — create the data the journey needs (a task, a cart item).
- `verify` — the actual journey under test (default when unlabeled).
- `conclude` — summarize or clean up; a failure here fails the flow but the
  earlier phases' results stand.

## Variables

`{{NAME}}` placeholders may appear in any string field. At run time the Run
step resolves them from, in order: the host environment, then
`flowtest/.env` (never committed), then `vars` defaults from the flow.
Unresolved placeholders are reported before the browser opens — a flow never
runs with a literal `{{...}}` in it.

## Statuses

Steps end in one of four states:

| Step status | Meaning |
|-------------|---------|
| `PASSED` | Action and all `expect` conditions held |
| `HEALED` | Passed only after a self-heal retry; the strategy is recorded |
| `FAILED` | Action or assertions failed after retries |
| `SKIPPED` | Precondition missing (`precheck` phase) or explicitly skipped; records a reason |

The flow-level verdict (PASS / PARTIAL / FAIL) derives from these; full rules
live in [run.md](run.md).
