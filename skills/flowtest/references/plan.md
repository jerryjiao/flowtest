# Plan — intent to `.flow.yaml`

Turn a plain-language intent ("a user can add a product to the cart and check
out") into a validated flow file. Ported principle from production use: **a
plan that guesses is worse than a plan that asks** — clarify uncertainties,
confirm before executing.

## Input

Free text describing a user journey, or a feature request / bug report quoted
at you. There is no issue-tracker integration — if the user pastes an issue,
treat the paste as the intent.

## Procedure

### 1. Gather context (skip what is absent)

1. **Lessons from past failures.** If a KnowFlow KB exists for this SUT, query
   it (`flowtest-kb` skill) for the journey's key nouns. Known traps found
   here shape steps and assertions.
2. **House style.** List `flowtest/flows/*.flow.yaml`; read 1–2 that touch the
   same area. Match their conventions (phases, assertion style, granularity).
3. **The SUT itself.** If a browser backend is available and the intent names
   screens you have not seen, open the entry URL and take an accessibility
   snapshot to learn real element names. Real names beat invented ones —
   invented element names are the top cause of first-run failures.

### 2. Analyze

Decompose the intent into: **scope** (which screens/journey), **preconditions**
(data, auth state, feature flags), **path** (ordered actions), **acceptance**
(what proves it worked — phrase as `expect` conditions). Tag each precondition
as satisfiable by the flow itself (`setup` steps) or environmental (must
`precheck`).

### 3. Clarify uncertainties

If any of these are unresolved, ask — do not guess:

- Scope ambiguity (multiple plausible journeys fit the words)
- Preconditions that may not exist (seeded data? test account? feature flag?)
- Acceptance is unstated ("works correctly" is not a condition)
- Destructive risk (the journey deletes or pays — confirm it is safe to run)

Ask at most 3 questions per round, at most 2 rounds, each with concrete
options (use the host's question mechanism; if headless, stop and present the
questions in your reply). If nothing is uncertain, say so and proceed.

### 4. Draft

Write `flowtest/drafts/<flow>.draft.flow.yaml` following
[flow-format.md](flow-format.md). Quality rules, in priority order:

- **One journey per flow.** Split "test checkout and also search" into two flows.
- **3–15 steps.** Shorter is not a flow, longer is several journeys or missing
  `setup` phases.
- **Precheck before verify.** A `precheck` step proves the data exists; never
  verify a feature against data that may be absent — an empty check proves
  nothing and wastes a run.
- **Match assertion strength to data control.** Controlled data (you created it
  in `setup`): exact values are fine. Environmental data: existence checks
  (`element`, `text`). Unsure: prefer the loose check and note why.
- **Name real elements.** Every `target` must reference an element you saw in a
  snapshot or a house-style flow — or clearly mark the step with
  `note: guessed target` so the first run treats its failure as diagnostic.
- **No bare `wait` steps** unless the SUT has a known slow async; prefer an
  `expect` that polls implicitly.

### 5. Confirm

Present the draft compactly — flow id, title, step count, the ordered path as
one line per step (`#id action target`), preconditions, and which KB lessons
shaped it. Then offer: **Run it** / **Save only** / **Revise**. Revise loops
back to step 4 (same draft file, overwrite). Never auto-run a new plan.

### 6. Formalize

On Run it or Save only:

1. Validate: `python3 <skillDir>/scripts/validate_flow.py <draft>`. Fix and
   re-validate until clean — do not proceed with warnings unexplained. If the
   validator itself cannot run (PyYAML missing), stop and say so; drafts are
   not formalized unvalidated.
2. Move: `flowtest/drafts/<flow>.draft.flow.yaml` → `flowtest/flows/<flow>.flow.yaml`.
3. Run it → hand off to [run.md](run.md). Save only → report the final path
   and stop.

## Output contract

End with the flow id, the final file path, step count, and — if run — the
result summary line from the run step.
