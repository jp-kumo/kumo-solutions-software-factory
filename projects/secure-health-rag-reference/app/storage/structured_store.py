REPORTS = {
    ("tenant-demo", "patient-demo"): {
        "tenant_id": "tenant-demo",
        "patient_id": "patient-demo",
        "age_years": 42,
        "lab_markers": {"LDL": 190},
        "genetics": ["BRCA1+"],
        "name": "Jane Doe",
        "dob": "1983-05-10",
    }
}


def get_patient_record(tenant_id: str, patient_id: str) -> dict:
    key = (tenant_id, patient_id)
    if key not in REPORTS:
        raise KeyError("not_found")
    return REPORTS[key]
