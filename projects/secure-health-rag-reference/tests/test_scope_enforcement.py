from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_missing_scope_forbidden() -> None:
    r = client.get(
        "/patients/patient-demo/report",
        headers={
            "x-role": "clinician",
            "x-tenant": "tenant-demo",
            "x-patient": "patient-demo",
            "x-scope": "reports:write",
        },
    )
    assert r.status_code == 403
    assert r.json()["detail"] == "missing_scope"
