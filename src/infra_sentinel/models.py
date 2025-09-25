
from typing import Any, Dict, Optional
from pydantic import BaseModel

class Event(BaseModel):
    timestamp: Optional[str] = None
    type: str
    metric: Optional[str] = None
    value: Optional[float] = None
    window: Optional[str] = None
    reason: Optional[str] = None
    count: Optional[int] = None
    stage: Optional[str] = None
    involvedObject: Optional[Dict[str, Any]] = None
    labels: Dict[str, Any] = {}
    env: Optional[str] = None
