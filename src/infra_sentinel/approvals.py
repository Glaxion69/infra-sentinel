
from typing import Dict

class Approvals:
    def __init__(self, policy: Dict):
        self.policy = policy or {}

    def required(self, tags, env) -> bool:
        need_tags = set(self.policy.get("require_for_tags", []))
        auto_envs = set(self.policy.get("auto_approve_environments", []))
        if env in auto_envs:
            return False
        return bool(need_tags.intersection(set(tags or [])))
