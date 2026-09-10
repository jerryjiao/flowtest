# Learn — failures become knowledge

Trigger: a run finished with `FAILED` steps or suspicious `HEALED` steps, or
the user asks "why did this fail" / "remember this lesson". Learn is the step
that makes the next Plan better — a failure that teaches nothing will repeat.

Learn uses the `flowtest-kb` skill (KnowFlow workspace) as its memory. No KB
yet? Offer to init one; if declined, still write the note under
`flowtest/lessons/` as plain Markdown and say Learn is degraded.

## 1. Read the run

Load the `.result.json`. Collect: every `FAILED` step (error + screenshot),
every `HEALED` step (strategy + what differed), SKIPPED reasons, and the flow
file. Look at the failure screenshots — text errors alone hide half the story.

## 2. Diagnose each distinct failure

Classify before writing anything:

| Class | Looks like | Lesson? |
|-------|-----------|---------|
| Bad target | Element name in flow doesn't match the page (renamed UI, guessed locator) | Yes — record the correct locator pattern for this SUT |
| Missing precondition | precheck skipped; data/account/flag absent | Yes — record what must exist and how to check |
| Timing | Element appears late; heal = fresh snapshot fixed it | Yes — record where this SUT is slow |
| Assertion too strict | Exact match on environmental data; existence check passed | Yes — record the loose form that works |
| Backend quirk | Automation-tool-specific behavior (ref staleness, frame handling) | Yes — record the workaround |
| Product bug | The SUT genuinely misbehaves | **No** — tell the user to file it in the SUT's tracker; a flow re-run after the fix is the lesson's proof |

One note per **root cause**, not per step — five steps failing on one renamed
button is one note.

## 3. Write the note

Fill in this template (keep it under ~40 lines; notes are read during Plan,
brevity is recall):

```markdown
Lesson: {one-line takeaway, imperative}
Flow: {flow} / step {step-id}
Date: {YYYY-MM-DD}
Category: {bad-target | precondition | timing | strict-assertion | backend-quirk}

Symptom:
{What the run showed — status, error text, what the screenshot revealed.}

Diagnosis:
{Root cause. Name the evidence. If uncertain, say so and mark (INFERRED).}

Fix:
{The concrete change: correct locator pattern, precondition to add, looser
assertion form, wait point, workaround. Written so a future Plan step applies
it without re-deriving anything.}
```

## 4. Ingest into the KB

Hand the note to the `flowtest-kb` skill: `knowflow ingest "<note text>" --source text`,
then follow its synthesis/review flow (pages land `status: pending`; the user
reviews). If the run revealed a flow defect (bad target, strict assertion),
**also offer to edit the flow file directly** — the KB sharpens the next
plan; the edit fixes this one.

## 5. Close the loop

Summarize: lessons written (titles), KB state (pending review / ingested /
degraded to `flowtest/lessons/`), flow edits made or offered, and product bugs
handed to the user. Do not claim a lesson "learned" until it is written down.
