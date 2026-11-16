from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

APP_DIR = Path(__file__).resolve().parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from inference import load_model_bundle, predict_message

app = FastAPI(
    title="API Deteksi Phishing WhatsApp Perpajakan",
    description=(
        "Layanan REST API berbasis LinearSVC (Kalibrasi Platt) dan Random Forest "
        "untuk deteksi pesan phishing WhatsApp mengatasnamakan otoritas perpajakan."
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://web.whatsapp.com",
        "http://localhost:8501",
        "http://127.0.0.1:8501",
    ],
    allow_origin_regex=r"^(chrome-extension://.*|http://localhost:\d+|http://127\.0\.0\.1:\d+)$",
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


class PredictRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000, description="Teks pesan WhatsApp")
    top_k: int = Field(default=8, ge=1, le=20, description="Jumlah token pemicu XAI")


class BatchPredictRequest(BaseModel):
    texts: list[str] = Field(..., min_length=1, max_length=200)
    top_k: int = Field(default=5, ge=1, le=20)


@app.get("/health")
def health_check() -> dict[str, Any]:
    """Return service readiness and loaded model bundle metadata."""
    try:
        bundle = load_model_bundle()
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    return {
        "status": "ok",
        "models_loaded": ["LinearSVC+Platt", "RandomForest"],
        "metadata": bundle.get("metadata", {}),
    }


@app.post("/predict")
def predict(req: PredictRequest) -> dict[str, Any]:
    """Classify a single message and return calibrated probabilities + XAI triggers."""
    try:
        return predict_message(req.text, top_k=req.top_k)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@app.post("/predict/batch")
def predict_batch(req: BatchPredictRequest) -> dict[str, Any]:
    """Classify up to 200 messages in a single request."""
    results: list[dict[str, Any]] = []
    for idx, text in enumerate(req.texts):
        cleaned_input = text.strip()
        if not cleaned_input:
            results.append({"index": idx, "error": "Teks kosong dilewati."})
            continue
        item = predict_message(cleaned_input, top_k=req.top_k)
        item["index"] = idx
        results.append(item)
    return {"total": len(req.texts), "results": results}
