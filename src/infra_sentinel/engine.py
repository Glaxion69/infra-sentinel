
import time, yaml, json, pathlib
from typing import Dict, Any, List
from .models import Event
from .approvals import Approvals
from .audit import Auditor
from .providers import K8sProvider, HttpProvider, SlackProvider

COOLDOWNS = {}  # rule_id -> last_ts

def load_yaml_files(dirpath: str) -> List[Dict[str, Any]]:
    rules = []
    for p in sorted(pathlib.Path(dirpath).glob("*.yaml")):
        with open(p, "r", encoding="utf-8") as f:
            rules.append(yaml.safe_load(f))
    # Sort by declared priority ascending
    rules.sort(key=lambda r: r.get("priority", 100))
    return rules

def match_expr(expr: str, variables: Dict[str, Any]) -> bool:
    try:
        return bool(eval(expr, {}, variables))
    except Exception:
        return False

def matches(rule: Dict, variables: Dict[str, Any]) -> bool:
    cond = rule.get("match", {})
    if "all" in cond:
        return all(match_expr(e, variables) for e in cond["all"])
    if "any" in cond:
        return any(match_expr(e, variables) for e in cond["any"])
    return False

def cooldown_ok(rule_id: str, cooldown: int) -> bool:
    now = time.time()
    last = COOLDOWNS.get(rule_id, 0)
    if now - last >= cooldown:
        COOLDOWNS[rule_id] = now
        return True
    return False

def dispatch_action(action: Dict, providers: Dict[str, Any], variables: Dict[str, Any], dry_run: bool):
    atype = action.get("type","")
    if atype.startswith("k8s."):
        return providers["k8s"].perform(action, variables, dry_run)
    if atype.startswith("http."):
        act = {"method": atype.split(".")[1], **action}
        return providers["http"].perform(act, variables, dry_run)
    if atype.startswith("slack."):
        return providers["slack"].perform(action, variables, dry_run)
    if atype == "approval.require":
        return {"provider":"approval","required":True,"reason":action.get("reason","")}
    return {"provider":"unknown","action":atype}

def run_engine(config_path: str, events_path: str, audit_path: str = None, dry_run: bool = True):
    # Load config and rules
    with open(config_path, "r", encoding="utf-8") as f:
        conf = yaml.safe_load(f) or {}
    approvals = Approvals(conf.get("approvals", {}))
    rules = load_yaml_files("rules")
    auditor = Auditor(audit_path or conf.get("sinks", [{}])[0].get("path"))

    # Providers
    providers = {
        "k8s": K8sProvider({}),
        "http": HttpProvider({"base_url": "https://example.com"}),
        "slack": SlackProvider({}),
    }

    # Stream events
    with open(events_path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            raw = json.loads(line)
            event = Event(**raw)
            env = event.env or "dev"
            variables = {"event": event.model_dump(), "env": env, "dry_run": dry_run}
            for rule in rules:
                rid = rule.get("id","unnamed")
                if matches(rule, variables):
                    # Respect cooldown if specified on actions
                    for action in rule.get("actions", []):
                        cd = int(action.get("cooldown", 0))
                        if cd and not cooldown_ok(f"{rid}:{action.get('type')}", cd):
                            continue
                        # Approval gate
                        if approvals.required(rule.get("tags", []), env) and action.get("type") != "approval.require":
                            auditor.log({"rule": rid, "event": event.model_dump(), "skipped":"approval_required"})
                            continue
                        result = dispatch_action(action, providers, variables, dry_run)
                        auditor.log({"rule": rid, "event": event.model_dump(), "action": action, "result": result})
