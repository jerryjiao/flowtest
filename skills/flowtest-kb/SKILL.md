---
name: flowtest-kb
description: |
  flowtest's memory: a local KnowFlow workspace holding product knowledge and
  failure lessons for the System Under Test. Use when the flowtest engine needs
  to query past lessons while planning (Plan step context), ingest a failure
  lesson (Learn step), or when the user asks to set up, inspect, or search the
  flowtest knowledge base. Requires the knowflow CLI for full function; without
  it the engine still works, just without Learn.
---

# flowtest-kb — KnowFlow as flowtest's memory

flowtest keeps its knowledge layer in a [KnowFlow](https://github.com/jerryjiao/knowflow)
workspace: plain Markdown, reviewed by humans, searchable locally, no server.
This skill is the thin contract between the engine and KnowFlow — it adds
nothing on top.

## Setup

```bash
npm install -g @jerryjiao/knowflow     # Node 18+, Python 3.10+
knowflow init flowtest/kb              # workspace inside the SUT repo
knowflow status                        # confirm raw/ wiki/ and index state
```

The workspace lives at `flowtest/kb/` in the SUT repository so lessons version
with the code they describe. Commit the wiki; keep the index out of git
(KnowFlow marks its own ignores on init).

No `knowflow` CLI? Say so and continue without it: the engine's Plan and Run
steps work unchanged, Learn degrades to writing notes under `flowtest/lessons/`.

## The contract

| Engine moment | KnowFlow call | Notes |
|---------------|---------------|-------|
| Plan: what traps exist for this SUT | `knowflow query "<journey keywords>"` | Use the intent's key nouns; 2–4 queries beat one long one |
| Plan: what the product should do (docs) | `knowflow query "<feature terms>"` | Only if product docs were ingested |
| Learn: save a lesson | `knowflow ingest "<lesson markdown>" --source text` | Note template in the engine's [learn.md](../flowtest/references/learn.md) |
| Seed: capture product docs | `knowflow ingest <doc-url>` | User-driven; deterministic capture into `raw/` |
| Health / state | `knowflow status` | Before relying on query results |

### Query, two ways

1. **Semantic** — `knowflow query "<text>"` against a built index
   (`knowflow index build`; needs an embedding API key configured in the
   workspace). Best recall for "what do we know about checkout".
2. **Keyword fallback** — no index or no key: the KB is still plain Markdown;
   search it directly (`grep -ri "<term>" flowtest/kb/wiki/`) and Read the
   hits. Fewer surprises than silence.

Report which path you used; recall quality differs, and Plan weighs evidence
accordingly.

### After ingest

`ingest` captures raw material only. Synthesis into wiki pages follows
KnowFlow's agent contract (in the knowflow repo:
`docs/agents/synthesize.md`): draft pages land with `status: pending` and the
**user reviews** — flip `pending` → `reviewed` (or delete to reject). Pending
pages stay out of the graph and the search index, so say clearly when a lesson
is "captured, pending review", not "in the KB".

## Rules

- Never write wiki pages directly around the contract — capture via `ingest`,
  synthesize per the contract, let the user review.
- The KB holds generalizable lessons and product knowledge, not run logs —
  those are `.result.json` files in `flowtest/reports/`.
- Product bugs go to the SUT's issue tracker, not the KB (the engine's Learn
  step already enforces this classification).
