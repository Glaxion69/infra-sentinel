# Infra Sentinel

**Infra Sentinel** is a modular **SRE incident prevention + auto‑remediation toolkit** for Kubernetes and Cloud.
It ingests signals (metrics, events, logs), matches them to **YAML rules**, and executes **safe, idempotent actions**
(e.g., restart a pod, cordon+drain a node, roll back a deployment, scale a workload, open a ticket, or notify Slack).

> This is a professional repository skeleton designed for GitHub. It ships with dry‑run safety, unit tests, a Dockerfile, and CI.
> Actions are pluggable—swap in real integrations later (Kubernetes, AWS, Slack, PagerDuty, etc.).

## Features
- Rule‑based engine (`rules/*.yaml`) with priorities, cooldowns, and match conditions
- Dry‑run mode (no side effects)
- Pluggable **sources** (metrics, events, logs) and **actions** (k8s, shell, webhooks, tickets)
- **Approval gates** for risky actions (policy-driven)
- Structured **audit log** in JSONL
- GitHub Actions CI, tests, and linting

## Quick Start

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e .[dev]

# Validate rules and run a demo event stream
infra-sentinel run --config config/sentinel.yaml --events demo/events.jsonl --dry-run
```

## Repo Structure
```
infra-sentinel/
├─ README.md
├─ LICENSE
├─ pyproject.toml
├─ setup.cfg
├─ Makefile
├─ .gitignore
├─ .github/workflows/ci.yml
├─ config/
│  ├─ sentinel.yaml              # global settings, approvals, sinks
│  └─ providers.yaml             # provider wiring (k8s, slack, http, aws)
├─ rules/
│  ├─ 10_high_cpu.yaml
│  ├─ 20_pod_crashloop.yaml
│  └─ 30_error_rate_spike.yaml
├─ demo/
│  ├─ events.jsonl               # synthetic event stream
│  └─ k8s_mock_state.json        # example cluster state
├─ docs/
│  ├─ ARCHITECTURE.md
│  ├─ SCENARIOS.md
│  └─ OPERATIONS.md
├─ docker/
│  └─ Dockerfile
├─ src/infra_sentinel/
│  ├─ __init__.py
│  ├─ cli.py
│  ├─ engine.py
│  ├─ models.py
│  ├─ approvals.py
│  ├─ audit.py
│  ├─ providers/
│  │  ├─ __init__.py
│  │  ├─ base.py
│  │  ├─ k8s.py                  # placeholder integration
│  │  ├─ http.py                 # webhook/action
│  │  └─ slack.py                # notifier (stubbed)
│  └─ utils.py
└─ tests/
   ├─ test_rules.py
   └─ test_engine.py
```

## Example
```bash
infra-sentinel run   --config config/sentinel.yaml   --events demo/events.jsonl   --audit results/audit.jsonl   --dry-run
```
