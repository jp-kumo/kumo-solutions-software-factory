import pytest
from pydantic import ValidationError

from app.models.schemas import ReportResponse


def test_output_schema_rejects_empty_summary() -> None:
    with pytest.raises(ValidationError):
        ReportResponse(
            patient_id="patient-demo",
            tenant_id="tenant-demo",
            summary="",
            provenance=[],
        )
