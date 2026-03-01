from app.rag.preprocess import preprocess_for_rag


def test_preprocess_removes_direct_identifiers() -> None:
    record = {
        "tenant_id": "tenant-demo",
        "patient_id": "patient-demo",
        "age_years": 42,
        "lab_markers": {"LDL": 190},
        "genetics": ["BRCA1+"],
        "name": "Jane Doe",
        "dob": "1983-05-10",
    }
    ctx = {"tenant": "tenant-demo", "patient": "patient-demo", "role": "clinician"}
    txt = preprocess_for_rag(record, ctx)
    assert "Jane" not in txt
    assert "1983" not in txt
    assert "LDL" in txt
