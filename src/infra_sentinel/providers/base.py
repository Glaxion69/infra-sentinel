
from typing import Any, Dict

class BaseProvider:
    def __init__(self, config: Dict):
        self.config = config or {}

    # Action handlers return a dict result
    def perform(self, action: Dict, variables: Dict, dry_run: bool = True) -> Dict[str, Any]:
        raise NotImplementedError
