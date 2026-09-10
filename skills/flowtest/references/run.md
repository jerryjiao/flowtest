# Run — execute a flow in a real browser

Input: a path to a validated `.flow.yaml` (the Plan step hands off here after
user confirmation; a previously confirmed flow can be re-run directly).

## 1. Preflight

1. **Validate** the flow file (`scripts/validate_flow.py`). Invalid → fix with
   the user or stop; never run an invalid flow. Validator itself unavailable
   (exit 3, PyYAML missing) → stop too: say what is missing and offer to
   install it. A flow runs only after a clean validation, no exceptions.
2. **Resolve variables.** For every `{{NAME}}` in any string field: host
   environment first, then `flowtest/.env`, then the flow's `vars` defaults.
   Any placeholder left unresolved → stop before opening the browser and list
   what is missing.
3. **Resolve URLs.** `goto` targets without a scheme are joined to `baseUrl`.
4. Create `flowtest/reports/` and `flowtest/screenshots/` if missing.

## 2. Pick a browser backend

flowtest drives whatever browser automation the host already has — there is no
bundled browser. Detect in this order:

| Priority | Backend | Detection |
|----------|---------|-----------|
| 1 | Host browser MCP tools | Tools on the session matching browser automation (navigate/snapshot/click/fill primitives, Playwright-style or computer-use style) |
| 2 | `agent-browser` CLI | `agent-browser --version` on PATH |

Map the flow's primitives onto the backend. Two known conventions:

| Primitive | Playwright-style MCP | `agent-browser` CLI |
|-----------|---------------------|---------------------|
| open URL | navigate tool | `agent-browser open <url>` |
| page state | snapshot tool | `agent-browser snapshot -i` |
| click | click tool (element/ref) | `agent-browser click @eN` |
| fill | fill tool | `agent-browser fill @eN "<value>"` |
| select | select tool | `agent-browser select @eN "<value>"` |
| hover | hover tool | `agent-browser hover @eN` |
| press key | press tool | `agent-browser press <key>` |
| wait | — (poll via expect) | `agent-browser wait <ms>` |
| screenshot | screenshot tool → path | `agent-browser screenshot <path>` |
| current URL / title | snapshot / location tool | `agent-browser get url` / `get title` |

Path gotcha: `agent-browser` resolves relative paths against its daemon's
CWD, not the invoking shell's — pass **absolute paths** for screenshot
artifacts, or a relative `flowtest/screenshots/...` can land in an unrelated
directory.

Snapshot refs are ephemeral: **re-snapshot after every navigation or major DOM
change**, never reuse refs across loads. For unknown backends, adapt through
the same primitive set; if a primitive is missing, report the gap instead of
improvising destructive alternatives.

## 3. Step loop

For each step, in order:

1. **Snapshot** the page (skip if the action needs no DOM, e.g. `wait`).
2. **Resolve** the step's `target` against the snapshot — semantic locators
   (see flow-format) map to a concrete element/ref by role and name. Target
   not resolvable → heal path.
3. **Act** per the action table (flow-format.md).
4. **Verify** every `expect` condition against a fresh snapshot / URL / title.
   All hold → `PASSED`.
5. **Record**: status, duration, and on `FAILED`/`HEALED` a screenshot to
   `flowtest/screenshots/<flow>-<step-id>-<n>.png`.
6. **Log** one line per step: `[3/9] click "button 'Add'" → PASSED (2.1s)`.

A `FAILED` step does **not** stop the run — continue with the next step (the
evidence of what still works is valuable). Exceptions: browser crash /
backend death → stop, mark remaining steps `SKIPPED` (reason: backend lost).

### Timeouts

- Per step: `stepTimeout` (flow-level, default 60s) or the step's own
  `timeout`. Exceeded → treat as a failure and enter healing.
- Whole run: `timeout` (default 300s). Exceeded → stop, mark remaining steps
  `SKIPPED` (reason: flow timeout), still write the result file.

### Precheck semantics

A `precheck` step that fails does not count as `FAILED`: mark it `SKIPPED`
with the reason, skip all remaining steps (`SKIPPED`, reason: precondition not
met), verdict `PARTIAL`. Verifying against absent preconditions proves
nothing — skip early, run again once they exist.

## 4. Self-heal (max 2 attempts per step)

On a failure, classify first, then retry with the first fitting strategy:

| Failure class | Signals | Strategy order |
|---------------|---------|----------------|
| `timeout` | step budget exceeded | retry with a fresh snapshot (element may have appeared late) |
| `element_not_found` | target unresolvable | alternate element from the snapshot (same role, variant name/position) |
| `assertion_failed` | action ok, expect failed | re-check after a fresh snapshot; if data-controlled exact match failed, try the existence-level variant and mark `HEALED` with note |
| `unknown` | anything else | retry once with fresh snapshot |

Rules: healing never edits the flow file. `HEALED` results record the strategy
and what differed. Second failure → `FAILED` with the original error, and move
on. Heals that only loosened an assertion must say so — a healed exact-match
is weaker evidence than a passed one.

`extract` results land in the result JSON under the step (`extracted`).
v1 flows cannot reference extracted values in later steps; if a journey needs
that, it is two flows.

## 5. Persist, then summarize

Write `flowtest/reports/<flow>.<YYYYMMDD-HHMMSS>.result.json` **before**
printing any summary:

```json
{
  "formatVersion": 1,
  "flow": "guest-checkout",
  "flowFile": "flowtest/flows/guest-checkout.flow.yaml",
  "backend": "agent-browser",
  "startedAt": "2026-09-10T09:30:12Z",
  "finishedAt": "2026-09-10T09:31:02Z",
  "durationMs": 50123,
  "verdict": "PASS",
  "counts": { "passed": 6, "healed": 1, "failed": 0, "skipped": 0, "total": 7 },
  "steps": [
    {
      "id": "add-first-product",
      "action": "click",
      "target": "button 'Add to cart' (first)",
      "status": "HEALED",
      "healStrategy": "alternate_element",
      "durationMs": 4120,
      "error": null,
      "screenshot": "flowtest/screenshots/guest-checkout-add-first-product-1.png",
      "extracted": null
    }
  ]
}
```

Verdict: `PASS` (no failed), `PARTIAL` (no failed, ≥1 skipped), `FAIL`
(≥1 failed). Then the one-line summary the user sees:

```
flow guest-checkout: PASS — 7 steps (6 passed, 1 healed) in 50s · reports/guest-checkout.20260910-093012.result.json
```

Failures or heals → offer [Learn](learn.md) and [Report](report.md).
