from fastapi import FastAPI

from app.api.reports import router as reports_router

app = FastAPI(title="Secure Health RAG Reference", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(reports_router)
