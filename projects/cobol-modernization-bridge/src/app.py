from __future__ import annotations

import json
from pathlib import Path
from fastapi import FastAPI, HTTPException

app = FastAPI(title="COBOL Modernization Bridge API", version="0.1.0")

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "processed" / "customers.json"


@app.get("/healthz")
def healthz() -> dict:
    return {"ok": True}


@app.get("/customers")
def customers() -> list[dict]:
    if not DATA_PATH.exists():
        raise HTTPException(status_code=404, detail="Processed data not found. Run parser first.")
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))
