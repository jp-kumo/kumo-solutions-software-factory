from app.storage import vector_store


def retrieve_scoped(ctx: dict[str, str], top_k: int = 5) -> list[dict]:
    return vector_store.search(ctx["tenant"], ctx["patient"], top_k=top_k)
