import json
from datetime import UTC, datetime
from typing import Any

from app.security.redact import redact


def audit_log(event: str, data: dict[str, Any], ctx: dict[str, str]) -> str:
    payload = {
        "ts": datetime.now(UTC).isoformat(),
        "evt": event,
        "reqId": ctx.get("reqId"),
        "tenant": ctx.get("tenant"),
        "patient": ctx.get("patient"),
        "sub": ctx.get("sub"),
    }
    payload.update(redact(data))
    line = json.dumps(payload)
    print(line)
    return line
