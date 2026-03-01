from app.models.schemas import ReportResponse


def generate_scoped_report(question: str, contexts: list[dict], ctx: dict[str, str]) -> ReportResponse:
    # Minimal deterministic output for MVP; replace with model call later.
    summary = f"Scoped answer for tenant={ctx['tenant']} patient={ctx['patient']} to: {question}"
    provenance = [c["sourceId"] for c in contexts]
    return ReportResponse(
        patient_id=ctx["patient"],
        tenant_id=ctx["tenant"],
        summary=summary,
        provenance=provenance,
    )
