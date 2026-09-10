# Contributing to flowtest

Thanks for helping shape flowtest — natural-language browser testing for
coding agents. Issues and PRs are both welcome; this file is the short path
from "I found something" to "it's merged".

## Ground rules

- **No real credentials, ever.** Flows reference secrets through
  `{{PLACEHOLDER}}` vars resolved at run time. The scrub gate in CI rejects
  secret-shaped literals, hardcoded service IPs, and legacy identifiers —
  keep it that way.
- **Flows are the artifact.** Feature work on the engine should show up as a
  `.flow.yaml` someone can read, run, and diff. Bug fixes to the format land
  in [skills/flowtest/references/flow-format.md](skills/flowtest/references/flow-format.md)
  and the validator together — the tests pin them to each other.
- **Docs mirror reality.** If you change the quickstart, the format, or the
  demo site's semantic anchors, update the README, the site docs, and the
  tests in the same PR.

## Development setup

```bash
git clone https://github.com/jerryjiao/flowtest && cd flowtest
pip install pyyaml                      # the only runtime dependency
python3 -m unittest discover -s tests   # validator + structure + scrub gates
python3 -m http.server 4173 -d demo     # serve the demo SUT
```

The website lives in `site/` (Astro + Starlight; `npm install && npm run
build` inside it). It deploys to GitHub Pages on merge to `main`.

## Triage vocabulary

Issues start with `needs-triage`. During triage they get exactly one next
state:

| Label | Meaning |
|---|---|
| `ready-for-agent` | fully specified — an AI agent can execute it without further decisions |
| `ready-for-human` | needs a human (judgment calls, design taste, maintainer secrets) |
| `needs-info` | waiting on the reporter — reproduction, environment, or examples |

Bug reports use the issue template; please fill in the environment section —
"host agent + version" is the single most useful datum for a host-agnostic
project.

## Pull requests

1. Branch from `main`, keep the diff focused.
2. `python3 -m unittest discover -s tests` green locally.
3. Describe the behavior change in terms of artifacts: flows, reports,
   result JSONs, rendered pages — not internal wording.
4. CI must be green (tests + scrub gate + site build). A planted-violation
   check of the scrub gate is occasionally re-verified by maintainers; don't
   weaken the gate to go green.

## Security

Report vulnerabilities privately to the maintainer via a GitHub security
advisory rather than a public issue. Do not include real credentials, keys,
or customer data in issues, flows, or screenshots.

## License

By contributing you agree your contributions ship under the repo's
[MIT license](LICENSE).
