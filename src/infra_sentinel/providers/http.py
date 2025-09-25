
import json, requests
from typing import Any, Dict
from .base import BaseProvider

class HttpProvider(BaseProvider):
    def perform(self, action: Dict, variables: Dict, dry_run: bool = True) -> Dict[str, Any]:
        url = action.get("url", "").format(**variables)
        method = action.get("method","POST").upper()
        payload = action.get("json")
        if isinstance(payload, str):
            payload = payload.format(**variables)
            try:
                payload = json.loads(payload)
            except Exception:
                payload = {"message": payload}
        result = {"provider":"http","method":method,"url":url,"payload":payload,"dry_run":dry_run}
        if dry_run:
            result["note"] = "dry-run: not calling HTTP"
            return result
        # Minimal real call
        resp = requests.request(method, self.config.get("base_url","") + url, json=payload, timeout=5)
        result["status_code"] = resp.status_code
        return result
