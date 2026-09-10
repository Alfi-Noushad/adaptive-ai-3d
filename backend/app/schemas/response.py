from datetime import datetime, timezone
from typing import Any, Optional
from pydantic import BaseModel, Field

class APIResponse(BaseModel):
    status: str = Field(default="success", description="Status string: success | error")
    message: str = Field(default="", description="Human-readable response message")
    data: Optional[Any] = Field(default=None, description="Payload data")
    error: Optional[Any] = Field(default=None, description="Error detail if status is error")
    timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
        description="UTC ISO-8601 timestamp"
    )