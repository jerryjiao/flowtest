# Report — a run, readable by humans and agents

Input: a `.result.json` path, or a `.flow.yaml` path (find its newest
`flowtest/reports/<flow>.*.result.json`). Output: a Markdown report next to
the result file, same timestamp stem (`.report.md`).

The report is the artifact people link to each other and attach to issues.
Write it for a reader who has never seen the run: verdict first, evidence
one click away, no engine jargon without a plain-language gloss.

## Template

```markdown
# {title}

**{verdict}** — {passed} passed · {healed} healed · {failed} failed · {skipped} skipped
({duration}, {startedAt}, backend: {backend})

Flow `{flow}` · plan: `{flowFile}` · raw result: `{resultFile}`

## What this journey covers
{1–3 sentences: the journey in user terms, and what "pass" proves. Quote the
flow title/description; do not invent scope.}

## Failures
<!-- omit section when verdict is PASS with no heals -->
### {step.id} — {status}
- **Step**: {action} `{target}`
- **Error**: {error}
- **Heal strategy**: {healStrategy} <!-- only when healed -->
- **Evidence**: ![{step.id}]({relative screenshot path})

## Steps
| # | Step | Action | Status | Time | Note |
|---|------|--------|--------|------|------|
| 1 | open-catalog | goto /products | PASSED | 0.8s | |

<!-- Note column: heal strategy, skip reason, or extracted values -->

## Extracted data
<!-- omit when no extract steps -->
| Step | Field | Value |
|------|-------|-------|

## Verdict notes
- SKIPPED reasons, precondition state, anything that weakens the verdict.
- If verdict is PARTIAL: state plainly what was and was not verified.
```

## Rules

- Screenshot links are **relative paths** from the report file so the report
  tree can be moved or zipped and still work.
- Never editorialize beyond the data ("probably a flake" is a diagnosis —
  put it in Learn notes with reasoning, or leave it out).
- Report the run you had: healed steps are healed, not passed; skipped steps
  say why.
- Print the report path when done; do not paste the whole report into chat —
  paste the verdict block and link the file.
