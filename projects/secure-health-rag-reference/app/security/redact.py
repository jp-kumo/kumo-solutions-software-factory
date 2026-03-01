import re
from typing import Any

SENSITIVE_KEYS = {"authorization", "token", "password", "secret", "api_key"}


def redact(data: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for k, v in data.items():
        if k.lower() in SENSITIVE_KEYS:
            out[k] = "[REDACTED]"
            continue
        if isinstance(v, str):
            # ultra-basic PHI-ish masking for demo
            v = re.sub(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+", "[REDACTED_EMAIL]", v)
            v = re.sub(r"\b\d{3}-\d{2}-\d{4}\b", "[REDACTED_ID]", v)
        out[k] = v
    return out
