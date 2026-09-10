---
title: Describe the journey. Your agent tests it in a real browser.
description: Turn a sentence like "a user can add a product to the cart and check out" into a .flow.yaml file. Your coding agent runs it step by step in a real browser, records a screenshot and timing for every step, and writes failures down as notes the next run reads. Open source, hosted in the agent you already use.
template: splash
hero:
  tagline: Open source, MIT licensed. Say "a user can add a product to the cart and check out"; flowtest turns that sentence into a .flow.yaml file. Your coding agent runs it step by step in a real browser, records a screenshot and a timing for every step, and writes failures down as notes the next run reads.
  image:
    html: |
      <div class="ft-card">
        <div class="ft-card-bar"><i></i><i></i><i></i><span class="ft-card-file">demo-smoke.flow.yaml</span></div>
        <pre><span class="k">flow:</span> <span class="s">demo-smoke</span>
      <span class="k">sut:</span> <span class="s">demo-site</span>
      <span class="k">vars:</span>
        <span class="k">DEMO_USER:</span> <span class="s">demo@flowtest.dev</span>

      <span class="k">steps:</span>
        - <span class="k">id:</span> <span class="s">fill-email</span>
          <span class="k">action:</span> <span class="s">fill</span>
          <span class="k">target:</span> <span class="s">"textbox 'Email'"</span>
          <span class="k">value:</span> <span class="s">"{{DEMO_USER}}"</span>

        - <span class="k">id:</span> <span class="s">submit-signin</span>
          <span class="k">action:</span> <span class="s">click</span>
          <span class="k">target:</span> <span class="s">"button 'Sign in'"</span>
          <span class="k">expect:</span>
            - <span class="k">element:</span> <span class="s">"heading 'Tasks'"</span>
            - <span class="k">not_text:</span> <span class="s">"Invalid credentials"</span>

        - <span class="k">id:</span> <span class="s">complete-task</span>
          <span class="k">action:</span> <span class="s">click</span>
          <span class="k">target:</span> <span class="s">"checkbox 'Buy oat milk'"</span></pre>
      </div>
  actions:
    - text: Run your first flow
      link: /flowtest/en/quickstart/
      variant: primary
      icon: right-arrow
    - text: GitHub
      link: https://github.com/jerryjiao/flowtest
      variant: secondary
      icon: github
---

<section class="ft-lead">
  <p class="ft-lead-strip">
    <span>A flow is a YAML file</span>
    <span>Runs in the coding agent you already use</span>
    <span>No daemon to install</span>
  </p>
</section>

<section class="ft-section">
  <div class="ft-section-head">
    <h2>It tests the layer unit tests cannot see</h2>
    <p>A redesign renames a button and checkout silently breaks — unit tests and CI do not catch that</p>
  </div>
  <div class="ft-duo">
    <div class="ft-pain">
      <p>Unit tests check functions one by one; integration tests check endpoints one by one. Whether <em>a user can walk the whole journey</em> — sign up, add to cart, check out — is a layer most projects leave unwatched.</p>
      <p>flowtest covers that layer: you describe the journey in one sentence, and the agent turns it into a browser test it can run again and again.</p>
    </div>
    <figure class="ft-shot">
      <img src="/flowtest/demo.gif" alt="Demo: the agent drives a browser through sign-in, task creation, completing a task, and reading the counters" />
      <figcaption>Recorded: the demo-smoke flow — sign in → create a task → complete it → read the counters. 9 steps, all passed, in 70 s.</figcaption>
    </figure>
  </div>
</section>

<section class="ft-section">
  <div class="ft-section-head">
    <h2>One loop, four moves</h2>
    <p>The agent walks the same path every time it runs a flow</p>
  </div>
  <div class="ft-feats">
    <div class="ft-feat"><div class="ico"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="6" cy="19" r="2"/><circle cx="18" cy="3" r="2"/><path d="M8 19h6a4 4 0 0 0 0-8h-4a4 4 0 0 1 0-8h6"/></svg></div><b>Plan</b><span>You describe the journey in plain language; the agent writes it as a <code>.flow.yaml</code>: steps, targets, expected conditions. A new file waits for your confirmation before anything executes.</span></div>
    <div class="ft-feat"><div class="ico"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polygon points="5 3 19 12 5 21 5 3"/></svg></div><b>Run</b><span>The agent drives a real browser step by step. Targets use semantic locators (button <code>'Sign in'</code>), not CSS selectors.</span></div>
    <div class="ft-feat"><div class="ico"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><rect x="8" y="2" width="8" height="4" rx="1"/><path d="M9 12h6M9 16h4"/></svg></div><b>Report</b><span>Every step lands as PASSED / HEALED / FAILED / SKIPPED with a screenshot and a timing. The result is written to a JSON file first, then turned into a human-readable report.</span></div>
    <div class="ft-feat"><div class="ico"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg></div><b>Learn</b><span>Failures become notes: what the trap was, which flows it affects, how to avoid it. The next Plan reads those notes.</span></div>
  </div>
</section>

<section class="ft-section">
  <div class="ft-section-head">
    <h2>Three steps to your first flow</h2>
    <p>Everything happens inside the coding agent you already have — nothing new to install</p>
  </div>
  <div class="ft-steps">
    <div class="ft-step"><span class="n">1</span><b>Serve the demo site</b><span>The repo ships a zero-dependency demo site; one command serves it.</span><code>python3 -m http.server 4173 -d demo</code></div>
    <div class="ft-step"><span class="n">2</span><b>Point your agent</b><span>Name the flow file; the engine takes over: validate, resolve variables, open the browser.</span><code>run demo-smoke.flow.yaml</code></div>
    <div class="ft-step"><span class="n">3</span><b>Read the report</b><span>Verdict, per-step statuses, screenshots, timings — all under flowtest/reports/.</span><code>flowtest/reports/*.result.json</code></div>
  </div>
</section>

<section class="ft-section">
  <div class="ft-section-head">
    <h2>The agent executes; you decide</h2>
    <p>Three boundaries are written into the engine rules — the agent cannot cross them</p>
  </div>
  <div class="ft-bounds">
    <ul>
      <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="20 6 9 17 4 12"/></svg><span>A new plan waits for your confirmation before the browser opens. Re-running a confirmed flow never asks again.</span></li>
      <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="20 6 9 17 4 12"/></svg><span>Credentials never go into flow files: they resolve from environment variables or .env placeholders at run time.</span></li>
      <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="20 6 9 17 4 12"/></svg><span>Every action maps to a real browser operation; the agent never invents substitute actions.</span></li>
    </ul>
    <p class="ft-quote">flowtest ships as agent skills. The coding agent you already have (Claude Code, zcode, or any SKILL.md-convention host) is the runtime — there is no separate test framework and no daemon.</p>
  </div>
</section>

<section class="ft-section">
  <div class="ft-section-head">
    <h2>Six design decisions</h2>
    <p>Each one has a full explanation in the docs</p>
  </div>
  <div class="ft-grid">
    <div class="ft-feat"><div class="ico"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg></div><b>Flows are YAML files</b><span>One file reads in one screen and validates mechanically. Commit it, review it, diff it.</span></div>
    <div class="ft-feat"><div class="ico"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><line x1="22" y1="12" x2="18" y2="12"/><line x1="6" y1="12" x2="2" y2="12"/><line x1="12" y1="6" x2="12" y2="2"/><line x1="12" y1="22" x2="12" y2="18"/></svg></div><b>Semantic locators</b><span>Targets are roles and names, not selectors. A control with no accessible name gets reported — that is an accessibility bug in your app.</span></div>
    <div class="ft-feat"><div class="ico"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 2v6"/><path d="M15 2v6"/><path d="M6 8h12v3a6 6 0 0 1-12 0z"/><path d="M12 17v5"/></svg></div><b>Executor-neutral</b><span>If the host provides browser MCP tools, use them; otherwise fall back to the agent-browser CLI. The same flow runs on either.</span></div>
    <div class="ft-feat"><div class="ico"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/></svg></div><b>Evidence on disk</b><span>Failed and healed steps are screenshotted automatically. The result JSON is written before any summary.</span></div>
    <div class="ft-feat"><div class="ico"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><polyline points="9 11.5 11 13.5 15 9.5"/></svg></div><b>Bounded self-heal</b><span>Max two retries per step; retry strategies are recorded in the report. A loosened assertion is labeled as such: HEALED is weaker than PASSED.</span></div>
    <div class="ft-feat"><div class="ico"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg></div><b>Knowledge base optional</b><span>Everything works without one. Learn degrades to plain Markdown notes under flowtest/lessons/.</span></div>
  </div>
</section>

<section class="ft-section">
  <div class="ft-cta">
    <h2>Start with one journey</h2>
    <p>Clone the repo, serve the demo, run demo-smoke — see PASS within two minutes.</p>
    <a class="cta" href="/flowtest/en/quickstart/">Start →</a>
  </div>
</section>
