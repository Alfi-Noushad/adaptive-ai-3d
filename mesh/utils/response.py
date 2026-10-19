from datetime import datetime, timezone


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def success_response(data: dict, message: str = "OK") -> dict:
    return {
        "status": "success",
        "message": message,
        "data": data,
        "error": None,
        "timestamp": _now(),
    }


def error_response(message: str, error: dict | str | None = None) -> dict:
    return {
        "status": "error",
        "message": message,
        "data": {},
        "error": error if error is not None else message,
        "timestamp": _now(),
    }