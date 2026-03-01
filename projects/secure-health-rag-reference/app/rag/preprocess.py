from app.security.redact import redact


def preprocess_for_rag(record: dict, ctx: dict[str, str]) -> str:
    if record["tenant_id"] != ctx["tenant"]:
        raise PermissionError("tenant_mismatch")

    safe = {
        "age": record.get("age_years"),
        "key_markers": record.get("lab_markers"),
        "genetic_flags": record.get("genetics"),
    }
    return str(redact(safe))
