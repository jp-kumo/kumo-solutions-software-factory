from fastapi import Header, HTTPException


def parse_ctx(
    x_sub: str = Header(default="demo-user"),
    x_role: str = Header(default="clinician"),
    x_tenant: str = Header(default="tenant-demo"),
    x_patient: str = Header(default="patient-demo"),
    x_scope: str = Header(default="reports:read"),
    x_request_id: str = Header(default="req-demo"),
) -> dict[str, str]:
    return {
        "sub": x_sub,
        "role": x_role,
        "tenant": x_tenant,
        "patient": x_patient,
        "scope": x_scope,
        "reqId": x_request_id,
    }


def require_scope(ctx: dict[str, str], needed: str) -> None:
    if needed not in ctx.get("scope", ""):
        raise HTTPException(status_code=403, detail="missing_scope")


def can_view_patient(ctx: dict[str, str], tenant: str, patient_id: str) -> bool:
    # Demo ABAC: tenant + patient must match request context unless role=admin
    if ctx.get("role") == "admin":
        return True
    return ctx.get("tenant") == tenant and ctx.get("patient") == patient_id
