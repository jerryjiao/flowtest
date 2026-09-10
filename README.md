# flowtest

> Natural-language browser testing for coding agents: describe the user journey, your agent turns it into a `.flow.yaml` plan, runs it in a real browser, reports, and learns from failures.

**Docs & demo: [jerryjiao.github.io/flowtest](https://jerryjiao.github.io/flowtest/)** ·
[中文说明](README.zh-CN.md)

```
skills/flowtest/       the engine: Plan → Run → Report → Learn (+ .flow.yaml format & validator)
skills/flowtest-kb/    the memory: a local KnowFlow workspace of lessons and product notes
demo/                  the demo site: zero-dependency SUT for the example flows
flowtest/              a live workspace: example run artifacts + seeded KnowFlow KB
site/                  the website (Astro + Starlight), deployed to GitHub Pages
tests/                 flow-format validator tests + repo structure & scrub gates
```

## Quickstart (measured: first passing flow in ~2 minutes)

You need a SKILL.md-convention host (Claude Code, zcode, …), Python 3 with
PyYAML, and any static file server:

```bash
git clone https://github.com/jerryjiao/flowtest && cd flowtest
python3 -m http.server 4173 -d demo        # serve the demo site
```

Then ask your agent: **“Run the flow at
`skills/flowtest/examples/demo-smoke.flow.yaml`.“** The engine skill takes
over: validate → resolve vars → drive a real browser → write the result JSON
and report under `flowtest/reports/`.

Re-running in the same browser? Click **Reset demo data** and **Sign out** on
the demo site first — with a live session the flow's sign-in precheck skips
and the run comes back PARTIAL instead of PASS.

Want to test your own app instead? Describe the journey — “test that a user
can sign up with an email and verify the confirmation screen” — and the
agent writes the flow for your confirmation before anything executes.

## What it does

- **Plan** — turn a plain-language intent ("a user can add a product to the cart and check out") into a structured `.flow.yaml` test plan you can read, edit, and version.
- **Run** — your coding agent executes the flow in a real browser, step by step, with screenshots.
- **Report** — structured pass/fail reports per flow, designed for humans and agents alike.
- **Learn** — failed runs feed a local knowledge base that sharpens future planning. Powered by [KnowFlow](https://github.com/jerryjiao/knowflow), entirely on your machine.

## Why skills, not a framework

flowtest ships as agent skills, not a test framework. Your existing coding agent (Claude Code, zcode, and hosts that follow the SKILL.md convention) is the runtime — no new lock-in, no daemon, and the same agent that writes your app can test it.

## Install

**Claude Code / zcode (plugin):** add this repo as a marketplace, then install —
the two skills (`flowtest`, `flowtest-kb`) are discovered automatically:

```bash
claude plugin marketplace add jerryjiao/flowtest
claude plugin install flowtest@flowtest
```

In zcode: Settings → Plugin Management → Discover → **+** → `jerryjiao/flowtest`
→ **Get**. (Verified install: `claude plugin install` reports *Skills (2):
flowtest, flowtest-kb*; zcode reads the same `.claude-plugin/` manifests.)

**Any SKILL.md host:** copy the [`skills/`](skills/) directory — each skill is
self-contained.

## License

[MIT](LICENSE)
