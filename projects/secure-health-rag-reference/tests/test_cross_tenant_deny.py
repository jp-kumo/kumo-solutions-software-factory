from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_cross_tenant_or_patient_forbidden() -> None:
    r = client.get(
        "/patients/patient-other/report",
        headers={
            "x-role": "clinician",
            "x-tenant": "tenant-demo",
            "x-patient": "patient-demo",
            "x-scope": "reports:read",
        },
    )
    assert r.status_code == 403
