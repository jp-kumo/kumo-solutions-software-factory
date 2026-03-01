from pydantic import BaseModel, Field


class ReportResponse(BaseModel):
    patient_id: str
    tenant_id: str
    summary: str = Field(min_length=1)
    provenance: list[str]


class RequestContext(BaseModel):
    sub: str
    role: str
    tenant: str
    patient: str
    scope: str
