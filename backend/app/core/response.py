from datetime import datetime, timezone
from typing import Any, Optional

def api_response(
    status: str = "success",
    message: str = "",
    data: Optional[Any] = None,
    error: Optional[Any] = None
) -> dict:
    """Standard Master Integration Contract API response envelope."""
    return {
        "status": status,
        "message": message,
        "data": data,
        "error": error,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
