
from typing import Any, Dict
from .base import BaseProvider

class SlackProvider(BaseProvider):
    def perform(self, action: Dict, variables: Dict, dry_run: bool = True) -> Dict[str, Any]:
        msg = action.get("message","").format(**variables)
        result = {"provider":"slack","message":msg,"dry_run":dry_run}
        if dry_run:
            result["note"] = "dry-run: not hitting webhook"
        else:
            result["note"] = "Pretend we posted to Slack webhook."
        return result
