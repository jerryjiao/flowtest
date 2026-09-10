# Demo Site — the default System Under Test

A single-file, zero-dependency task-list app (`index.html`) with a sign-in
gate and list CRUD. It exists so a fresh clone of flowtest can run its first
flow in minutes: no build step, no network, deterministic data.

## Serve it

Any static file server on port 4173 (the port the shipped example flows
expect):

```bash
python3 -m http.server 4173 -d demo     # from the repo root
# or: npx serve -l 4173 demo
```

Open <http://localhost:4173>.

## The demo account

| Field   | Value              |
|---------|--------------------|
| Email   | `demo@flowtest.dev` |
| Password | `demo-password`    |

Any other combination shows “Invalid credentials”. The session lives in
`sessionStorage`, so every fresh browser session starts signed out — re-runs
of the smoke flow start clean. **Reset demo data** (in the app footer)
restores the seeded task list.

## What it exercises

- **Forms** — the sign-in form, with a wrong-credentials path.
- **Multi-step flows** — sign in → work → sign out.
- **List CRUD** — add, rename inline, complete, delete tasks; open/done
  counters.

## Conventions flows rely on

- Every control has an accessible name (`label`, `aria-label`), so
  flow-format semantic locators (`button 'Sign in'`, `textbox 'Email'`,
  `checkbox 'Buy oat milk'`) resolve without CSS selectors.
- Extractable values are exposed as `data-field="<name>"` spans —
  `open-count` and `done-count` in the summary line — which the
  `extract` action in `demo-smoke.flow.yaml` reads.
