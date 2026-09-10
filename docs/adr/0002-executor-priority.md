# ADR-0002: Executor priority — host browser MCP first, agent-browser CLI second

- **Status**: Accepted
- **Date**: 2026-09-10
- **Context**: [Consensus decision #8](../plans/2026-09-10-rebirth-consensus.md)
  left the default browser backend to measurement: keep the legacy
  `agent-browser` CLI path or switch to Playwright — "whichever gets a
  newcomer from zero to first passing flow faster".

## Measurement (2026-09-10, this repo)

Same flow (`demo-smoke`, 9 steps), same demo site, two backends:

| | agent-browser CLI 0.26.0 | Host browser MCP (Playwright surface, IAB) |
|---|---|---|
| Extra setup for a newcomer | separate install (`brew install agent-browser`) | none — ships with the host |
| Steps passed | 9/9 | 9/9 |
| Host-paced wall clock | 70 s (one shell call per primitive) | ~12 s batched (browser-side ≈1 s) |
| Locator resolution | snapshot shows role+name; refs `@eN` | `getByRole(..., { name })` direct from snapshot |
| Friction observed | ref churn across navigations (re-snapshot each step — run.md already mandates this) | one transient 3 s actionability timeout (tab activation); fresh-kernel re-bootstrap per call is an agent-side cost, invisible to the user |

Both backends resolve the flow-format's semantic locators cleanly — which is
the point of executor-neutral targets. The measurement confirms the priority
order already encoded in [run.md](../../skills/flowtest/references/run.md):
**host browser MCP tools first, `agent-browser` CLI second.**

## Consequences

- No change to shipped skills; the detection table stands as written.
- agent-browser remains a fully supported fallback and the only path for
  hosts with no browser tooling (plain terminal agents).
- `backend` in the result JSON records which path drove the run, so reports
  stay comparable across hosts.
