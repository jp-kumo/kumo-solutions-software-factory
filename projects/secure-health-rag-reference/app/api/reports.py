from fastapi import APIRouter, Depends, HTTPException

from app.rag.generate import generate_scoped_report
from app.rag.preprocess import preprocess_for_rag
from app.rag.retrieve import retrieve_scoped
from app.security.audit import audit_log
from app.security.claims import can_view_patient, parse_ctx, require_scope
from app.storage.structured_store import get_patient_record
from app.storage.vector_store import upsert

router = APIRouter(prefix="/patients", tags=["reports"])


@router.get("/{patient_id}/report")
def get_report(patient_id: str, q: str = "Summarize key risk factors", ctx: dict = Depends(parse_ctx)) -> dict:
    require_scope(ctx, "reports:read")

    if not can_view_patient(ctx, tenant=ctx["tenant"], patient_id=patient_id):
        raise HTTPException(status_code=403, detail="forbidden")

    record = get_patient_record(ctx["tenant"], patient_id)
    sanitized_text = preprocess_for_rag(record, ctx)
    doc_id = f"{ctx['tenant']}:{patient_id}:record"
    upsert(doc_id=doc_id, text=sanitized_text)

    contexts = retrieve_scoped(ctx, top_k=5)
    report = generate_scoped_report(q, contexts, ctx)

    audit_log(
        "report.viewed",
        {"route": f"/patients/{patient_id}/report", "reportId": doc_id},
        {"reqId": ctx["reqId"], "tenant": ctx["tenant"], "patient": patient_id, "sub": ctx["sub"]},
    )
    return report.model_dump()
