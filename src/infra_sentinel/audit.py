
import json, pathlib, sys, datetime
from typing import Any, Dict, Optional

class Auditor:
    def __init__(self, path: Optional[str] = None):
        self.path = pathlib.Path(path) if path else None
        if self.path:
            self.path.parent.mkdir(parents=True, exist_ok=True)

    def log(self, record: Dict[str, Any]):
        record.setdefault("ts", datetime.datetime.utcnow().isoformat() + "Z")
        line = json.dumps(record)
        if self.path:
            with open(self.path, "a", encoding="utf-8") as f:
                f.write(line + "\n")
        else:
            print(line, file=sys.stdout)
