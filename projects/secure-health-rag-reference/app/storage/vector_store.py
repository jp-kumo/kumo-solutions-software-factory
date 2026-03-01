VECTORS: dict[str, str] = {}


def upsert(doc_id: str, text: str) -> None:
    VECTORS[doc_id] = text


def search(tenant_id: str, patient_id: str, top_k: int = 5) -> list[dict]:
    prefix = f"{tenant_id}:{patient_id}:"
    out = []
    for k, v in VECTORS.items():
        if k.startswith(prefix):
            out.append({"sourceId": k, "text": v})
    return out[:top_k]


def delete_by_prefix(prefix: str) -> int:
    keys = [k for k in VECTORS if k.startswith(prefix)]
    for k in keys:
        del VECTORS[k]
    return len(keys)
