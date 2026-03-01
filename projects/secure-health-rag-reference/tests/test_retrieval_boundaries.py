from app.storage import vector_store


def test_retrieval_scoped_by_tenant_and_patient() -> None:
    vector_store.VECTORS.clear()
    vector_store.upsert("tenant-a:patient-1:doc1", "A")
    vector_store.upsert("tenant-a:patient-2:doc2", "B")
    vector_store.upsert("tenant-b:patient-1:doc3", "C")

    results = vector_store.search("tenant-a", "patient-1", top_k=5)
    assert len(results) == 1
    assert results[0]["sourceId"] == "tenant-a:patient-1:doc1"
