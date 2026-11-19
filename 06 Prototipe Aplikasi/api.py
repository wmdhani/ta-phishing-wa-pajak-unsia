from __future__ import annotations

import csv
import os
import sys
import threading
import time
from collections import defaultdict, deque
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Annotated, Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

APP_DIR = Path(__file__).resolve().parent
ROOT_DIR = APP_DIR.parent
WEB_DIR = APP_DIR / "web"
SIMULATION_HTML_PATH = APP_DIR / "extension" / "simulasi_whatsapp_web.html"
EVAL_TABLE_PATH = ROOT_DIR / "05 Hasil Evaluasi" / "tabel_komparasi_utama.csv"

if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from inference import PRESET_CATALOG, clean_text, load_model_bundle, predict_message


def _get_rate_limit_per_min() -> int:
    raw = os.getenv("RATE_LIMIT_PER_MIN", "60").strip()
    try:
        return max(0, int(raw))
    except ValueError:
        return 60


def _build_allowed_origins() -> list[str]:
    origins = [
        "https://web.whatsapp.com",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ]
    extra_raw = os.getenv("ALLOWED_ORIGINS", "")
    for origin in extra_raw.split(","):
        cleaned = origin.strip().rstrip("/")
        if cleaned and cleaned not in origins:
            origins.append(cleaned)
    return origins


_RATE_WINDOW_SEC = 60.0
_RATE_BUCKETS: dict[str, deque[float]] = defaultdict(deque)
_RATE_LOCK = threading.Lock()
_SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "SAMEORIGIN",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Permissions-Policy": "geolocation=(), microphone=(), camera=()",
}


def _resolve_client_ip(request: Request) -> str:
    host = request.client.host if request.client else "unknown"
    if host == "testclient":
        return host
    if os.getenv("TRUST_PROXY_HEADERS", "").strip().lower() in {"1", "true", "yes"}:
        forwarded = request.headers.get("x-forwarded-for", "")
        if forwarded:
            first_hop = forwarded.split(",")[0].strip()
            if first_hop:
                return first_hop
    return host


def _is_rate_limited(client_ip: str, limit: int) -> bool:
    if limit <= 0 or client_ip == "testclient":
        return False
    now = time.monotonic()
    cutoff = now - _RATE_WINDOW_SEC
    with _RATE_LOCK:
        bucket = _RATE_BUCKETS[client_ip]
        while bucket and bucket[0] <= cutoff:
            bucket.popleft()
        if len(bucket) >= limit:
            return True
        bucket.append(now)
        if len(_RATE_BUCKETS) > 10000:
            stale = [ip for ip, dq in _RATE_BUCKETS.items() if not dq or dq[-1] <= cutoff]
            for ip in stale:
                del _RATE_BUCKETS[ip]
    return False


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    """Warm up the serialized model bundle and Sastrawi stemmer cache at startup."""
    try:
        load_model_bundle()
        clean_text("warmup pajak.go.id")
    except FileNotFoundError:
        pass
    yield


app = FastAPI(
    title="Cek Pesan Pajak — API & Aplikasi Web Deteksi Phishing WA",
    description=(
        "Layanan web dan REST API berbasis LinearSVC (Kalibrasi Platt) serta heuristik "
        "domain pajak.go.id untuk membantu masyarakat memeriksa pesan WhatsApp mengatasnamakan DJP."
    ),
    version="2.0.0",
    lifespan=lifespan,
)


@app.middleware("http")
async def security_and_rate_limit_middleware(request: Request, call_next: Any) -> Response:
    if request.method == "POST" and request.url.path in {"/predict", "/predict/batch"}:
        client_ip = _resolve_client_ip(request)
        if _is_rate_limited(client_ip, _get_rate_limit_per_min()):
            return JSONResponse(
                status_code=429,
                content={"detail": "Terlalu banyak permintaan. Coba lagi dalam 1 menit."},
                headers=_SECURITY_HEADERS,
            )

    response = await call_next(request)
    for header_name, header_val in _SECURITY_HEADERS.items():
        response.headers.setdefault(header_name, header_val)
    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=_build_allowed_origins(),
    allow_origin_regex=(
        r"^(chrome-extension://.*|http://localhost:\d+|http://127\.0\.0\.1:\d+|"
        r"https://.*\.(?:hf\.space|onrender\.com|up\.railway\.app))$"
    ),
    allow_credentials=False,
    allow_private_network=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

if WEB_DIR.exists():
    app.mount("/static", StaticFiles(directory=WEB_DIR), name="static")


class PredictRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000, description="Teks pesan WhatsApp")
    top_k: int = Field(default=8, ge=1, le=20, description="Jumlah kata pemicu teratas")


class BatchPredictRequest(BaseModel):
    texts: list[Annotated[str, Field(max_length=5000)]] = Field(..., min_length=1, max_length=200)
    top_k: int = Field(default=5, ge=1, le=20)


@app.get("/", include_in_schema=False)
def serve_web_app() -> FileResponse:
    """Serve the primary layperson-friendly web application."""
    index_path = WEB_DIR / "index.html"
    if not index_path.exists():
        raise HTTPException(status_code=404, detail="Halaman antarmuka web tidak ditemukan.")
    return FileResponse(index_path)


@app.get("/simulasi-wa", include_in_schema=False)
def serve_wa_simulation() -> FileResponse:
    """Serve the Manifest V3 WhatsApp Web extension interactive simulation page."""
    if not SIMULATION_HTML_PATH.exists():
        raise HTTPException(status_code=404, detail="Halaman simulasi WhatsApp Web tidak ditemukan.")
    return FileResponse(SIMULATION_HTML_PATH)


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


@app.get("/api/presets")
def get_presets() -> dict[str, Any]:
    """Return curated sample WhatsApp messages for quick layperson testing."""
    return {"presets": PRESET_CATALOG}


@app.get("/api/academic-summary")
def get_academic_summary() -> dict[str, Any]:
    """Return research metadata and model comparison metrics for the thesis modal."""
    metadata: dict[str, Any] = {}
    try:
        metadata = load_model_bundle().get("metadata", {})
    except FileNotFoundError:
        metadata = {}

    rows: list[dict[str, str]] = []
    if EVAL_TABLE_PATH.exists():
        with EVAL_TABLE_PATH.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))

    return {
        "thesis": {
            "title": (
                "Komparasi Algoritma Support Vector Machine dan Random Forest dalam "
                "Deteksi Pesan Phishing WhatsApp Mengatasnamakan Otoritas Perpajakan"
            ),
            "author": "Wan Mirza Dhani (240101020194)",
            "advisor": "Bapak Novi Dian Nathasia, S.Kom., MMSI",
            "program": "PJJ Sistem Informasi — Universitas Siber Asia",
            "scheme": "Tugas Akhir Prototype (TKT Level 6)",
        },
        "metadata": metadata,
        "evaluation_rows": rows,
    }


@app.post("/predict")
def predict(req: PredictRequest) -> dict[str, Any]:
    """Classify a single message and return verdict, layperson reasons, and highlights."""
    cleaned_raw = req.text.replace("\x00", "")
    try:
        t0 = time.perf_counter()
        result = predict_message(cleaned_raw, top_k=req.top_k)
        result["inference_ms"] = round((time.perf_counter() - t0) * 1000, 2)
        return result
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@app.post("/predict/batch")
def predict_batch(req: BatchPredictRequest) -> dict[str, Any]:
    """Classify up to 200 messages in a single request."""
    results: list[dict[str, Any]] = []
    for idx, text in enumerate(req.texts):
        cleaned_input = text.replace("\x00", "").strip()
        if not cleaned_input:
            results.append({"index": idx, "error": "Teks kosong dilewati."})
            continue
        try:
            item = predict_message(cleaned_input, top_k=req.top_k)
        except FileNotFoundError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc
        except ValueError as exc:
            results.append({"index": idx, "error": str(exc)})
            continue
        item["index"] = idx
        results.append(item)
    return {"total": len(req.texts), "results": results}
