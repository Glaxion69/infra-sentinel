
# Architecture

Infra Sentinel core components:
- **cli.py** — Entry point. Loads config, providers, rules, event stream. Runs the engine loop.
- **engine.py** — Rule evaluation, cooldowns, variable interpolation, action dispatch.
- **approvals.py** — Policy for when to require human approval; pluggable backends later.
- **audit.py** — Structured JSONL logging of decisions and actions.
- **providers/** — Integrations for actions/inputs (k8s, http, slack). Stubs by default.
- **rules/*.yaml** — Declarative rules with `match` conditions and `actions` array.
