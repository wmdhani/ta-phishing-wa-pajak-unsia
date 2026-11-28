from __future__ import annotations

import csv
import functools
import json
import logging
import math
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
from pydantic import BaseModel, Field, field_validator, model_validator

BACKEND_DIR = Path(__file__).resolve().parent
APP_DIR = BACKEND_DIR.parent
ROOT_DIR = APP_DIR.parent
WEB_DIR = APP_DIR / "frontend"
SIMULATION_HTML_PATH = APP_DIR / "extension" / "simulasi_whatsapp_web.html"
EVAL_TABLE_PATH = ROOT_DIR / "05-hasil-evaluasi" / "csv" / "tabel_komparasi_utama.csv"
BENCHMARK_JSON_PATH = (
    ROOT_DIR / "05-hasil-evaluasi" / "json" / "benchmark_latensi_purwarupa.json"
)

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from inference import (
    PRESET_CATALOG,
    clean_text,
    load_model_bundle,
    predict_message,
    predict_messages_batch,
)

logger = logging.getLogger("cek_pesan_pajak")


def _get_rate_limit_per_min() -> int:
    raw = os.getenv("RATE_LIMIT_PER_MIN", "60").strip()
    try:
        return max(0, int(raw))
    except ValueError:
        return 60


def _build_allowed_origins() -> list[str]:
    origins = [
        "https://web.whatsapp.com",
        "https://cek-pesan-pajak-production.up.railway.app",
        "https://cek-pesan-pajak.onrender.com",
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
_MAX_BATCH_TOTAL_CHARS = 100_000
_RATE_BUCKETS: dict[str, deque[float]] = defaultdict(deque)
_RATE_LOCK = threading.Lock()
_SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "SAMEORIGIN",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Permissions-Policy": "geolocation=(), microphone=(), camera=()",
    "Content-Security-Policy": (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self' https://fonts.googleapis.com 'unsafe-inline'; "
        "font-src 'self' https://fonts.gstatic.com; "
        "img-src 'self' data:; "
        "connect-src 'self'; "
        "base-uri 'self'; "
        "object-src 'none'; "
        "frame-ancestors 'self'"
    ),
}


def _resolve_client_ip(request: Request) -> str:
    host = request.client.host if request.client else "unknown"
    if host == "testclient":
        return host
    if os.getenv("TRUST_PROXY_HEADERS", "").strip().lower() in {"1", "true", "yes"}:
        forwarded = request.headers.get("x-forwarded-for", "")
        if forwarded:
            hops = [part.strip() for part in forwarded.split(",") if part.strip()]
            if hops:
                try:
                    trusted_hops = max(1, int(os.getenv("TRUST_PROXY_HOPS", "1").strip()))
                except ValueError:
                    trusted_hops = 1
                return hops[-trusted_hops] if len(hops) >= trusted_hops else hops[0]
    return host


def _is_rate_limited(client_ip: str, limit: int, cost: int = 1) -> bool:
    if limit <= 0 or client_ip == "testclient":
        return False
    effective_cost = max(1, cost)
    now = time.monotonic()
    cutoff = now - _RATE_WINDOW_SEC
    with _RATE_LOCK:
        bucket = _RATE_BUCKETS[client_ip]
        while bucket and bucket[0] <= cutoff:
            bucket.popleft()
        if len(bucket) + effective_cost > limit:
            return True
        bucket.extend([now] * effective_cost)
        if len(_RATE_BUCKETS) > 10000:
            stale = [ip for ip, dq in _RATE_BUCKETS.items() if not dq or dq[-1] <= cutoff]
            for ip in stale:
                del _RATE_BUCKETS[ip]
    return False


def _seconds_until_reset(client_ip: str) -> int:
    now = time.monotonic()
    with _RATE_LOCK:
        bucket = _RATE_BUCKETS.get(client_ip)
        if bucket:
            remaining = _RATE_WINDOW_SEC - (now - bucket[0])
            return max(1, math.ceil(remaining))
    return int(_RATE_WINDOW_SEC)


@functools.lru_cache(maxsize=1)
def _load_evaluation_rows() -> list[dict[str, str]]:
    if not EVAL_TABLE_PATH.exists():
        return []
    with EVAL_TABLE_PATH.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


@functools.lru_cache(maxsize=1)
def _load_latency_benchmark() -> dict[str, float]:
    if not BENCHMARK_JSON_PATH.exists():
        return {}
    try:
        payload = json.loads(BENCHMARK_JSON_PATH.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        logger.warning("Gagal membaca data benchmark latensi: %s", exc)
        return {}
    bench = payload.get("latency_benchmark", {})
    direct = bench.get("direct_inference_holdout_232", {})
    api_bench = bench.get("fastapi_post_predict_holdout_232", {})
    batch_bench = bench.get("fastapi_post_predict_batch_50", {})
    summary: dict[str, float] = {}
    if isinstance(direct.get("median_p50_ms"), (int, float)):
        summary["direct_p50_ms"] = round(float(direct["median_p50_ms"]), 2)
    if isinstance(api_bench.get("median_p50_ms"), (int, float)):
        summary["api_p50_ms"] = round(float(api_bench["median_p50_ms"]), 2)
    if isinstance(api_bench.get("mean_ms"), (int, float)):
        summary["api_mean_ms"] = round(float(api_bench["mean_ms"]), 2)
    if isinstance(batch_bench.get("avg_per_message_ms"), (int, float)):
        summary["batch_avg_ms"] = round(float(batch_bench["avg_per_message_ms"]), 2)
    return summary


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    """Warm up the serialized model bundle, evaluation caches, and Sastrawi stemmer."""
    try:
        load_model_bundle()
        clean_text("warmup pajak.go.id")
        _load_evaluation_rows()
        _load_latency_benchmark()
    except FileNotFoundError as exc:
        logger.warning("Model bundle belum tersedia saat startup: %s", exc)
    yield


app = FastAPI(
    title="Cek Pesan Pajak: API & Aplikasi Web Deteksi Phishing WA",
    description=(
        "Layanan web dan REST API berbasis LinearSVC (Kalibrasi Platt) serta heuristik "
        "domain pajak.go.id untuk membantu masyarakat memeriksa pesan WhatsApp mengatasnamakan DJP."
    ),
    version="2.1.0",
    lifespan=lifespan,
)


@app.middleware("http")
async def security_and_rate_limit_middleware(request: Request, call_next: Any) -> Response:
    if request.method == "POST" and request.url.path in {"/predict", "/predict/batch"}:
        client_ip = _resolve_client_ip(request)
        if _is_rate_limited(client_ip, _get_rate_limit_per_min(), cost=1):
            retry_after = _seconds_until_reset(client_ip)
            return JSONResponse(
                status_code=429,
                content={"detail": "Terlalu banyak permintaan. Coba lagi dalam 1 menit."},
                headers={**_SECURITY_HEADERS, "Retry-After": str(retry_after)},
            )

    response = await call_next(request)
    for header_name, header_val in _SECURITY_HEADERS.items():
        response.headers.setdefault(header_name, header_val)
    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=_build_allowed_origins(),
    allow_origin_regex=(
        r"^(chrome-extension://[a-p]{32}|http://localhost:\d+|http://127\.0\.0\.1:\d+)$"
    ),
    allow_credentials=False,
    allow_private_network=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Accept"],
)

if WEB_DIR.exists():
    app.mount("/static", StaticFiles(directory=WEB_DIR), name="static")


class PredictRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000, description="Teks pesan WhatsApp")
    top_k: int = Field(default=8, ge=1, le=20, description="Jumlah kata pemicu teratas")

    @field_validator("text")
    @classmethod
    def validate_non_empty_text(cls, value: str) -> str:
        cleaned = value.replace("\x00", "")
        if not cleaned.strip():
            raise ValueError("Teks pesan tidak boleh kosong.")
        return cleaned


class BatchPredictRequest(BaseModel):
    texts: list[Annotated[str, Field(max_length=5000)]] = Field(..., min_length=1, max_length=200)
    top_k: int = Field(default=5, ge=1, le=20)

    @model_validator(mode="after")
    def validate_total_batch_chars(self) -> BatchPredictRequest:
        total_chars = sum(len(item) for item in self.texts)
        if total_chars > _MAX_BATCH_TOTAL_CHARS:
            raise ValueError("Total panjang teks dalam satu batch maksimal 100.000 karakter.")
        return self


class HighlightItem(BaseModel):
    start: int
    end: int
    text: str
    kind: str
    reason: str


class TriggerItem(BaseModel):
    token: str
    contribution: float
    svm_coef: float
    direction: str


class PlainReasonItem(BaseModel):
    type: str
    title: str
    detail: str


class PredictResponse(BaseModel):
    label: int
    label_text: str
    risk_level: str
    risk_title: str
    risk_badge: str
    verdict_summary: str
    confidence_note: str
    svm_probability: float
    rf_probability: float
    cleaned_text: str
    has_apk: bool
    apk_matches: list[str]
    urls_found: list[str]
    official_domains: list[str]
    suspicious_domains: list[str]
    top_triggers: list[TriggerItem]
    highlights: list[HighlightItem]
    trigger_words: list[str]
    plain_reasons: list[PlainReasonItem]
    action_steps: list[str]
    recommendation: str
    inference_ms: float | None = None


class BatchPredictItem(PredictResponse):
    index: int


class BatchErrorItem(BaseModel):
    index: int
    error: str


class BatchPredictResponse(BaseModel):
    total: int
    results: list[BatchPredictItem | BatchErrorItem]


class HealthResponse(BaseModel):
    status: str
    models_loaded: list[str]
    metadata: dict[str, Any]


class PresetItem(BaseModel):
    id: str
    key: str
    label: str
    tag: str
    tone: str
    text: str


class PresetsResponse(BaseModel):
    presets: list[PresetItem]


class ThesisInfo(BaseModel):
    title: str
    author: str
    advisor: str
    program: str
    scheme: str


class AcademicSummaryResponse(BaseModel):
    thesis: ThesisInfo
    metadata: dict[str, Any]
    evaluation_rows: list[dict[str, str]]
    latency_benchmark: dict[str, float]


@app.get("/", include_in_schema=False)
def serve_web_app() -> FileResponse:
    """Serve the primary layperson-friendly web application."""
    index_path = WEB_DIR / "index.html"
    if not index_path.exists():
        raise HTTPException(status_code=404, detail="Halaman antarmuka web tidak ditemukan.")
    return FileResponse(index_path, headers={"Cache-Control": "no-cache"})


@app.get("/simulasi-wa", include_in_schema=False)
def serve_wa_simulation() -> FileResponse:
    """Serve the Manifest V3 WhatsApp Web extension interactive simulation page."""
    if not SIMULATION_HTML_PATH.exists():
        raise HTTPException(status_code=404, detail="Halaman simulasi WhatsApp Web tidak ditemukan.")
    return FileResponse(SIMULATION_HTML_PATH, headers={"Cache-Control": "no-cache"})


@app.get("/health", response_model=HealthResponse)
def health_check() -> dict[str, Any]:
    """Return service readiness and loaded model bundle metadata."""
    try:
        bundle = load_model_bundle()
    except FileNotFoundError as exc:
        logger.error("Model bundle tidak ditemukan saat /health: %s", exc)
        raise HTTPException(
            status_code=503, detail="Model klasifikasi sedang tidak tersedia."
        ) from exc

    return {
        "status": "ok",
        "models_loaded": ["LinearSVC+Platt", "RandomForest"],
        "metadata": bundle.get("metadata", {}),
    }


@app.get("/api/presets", response_model=PresetsResponse)
def get_presets() -> dict[str, Any]:
    """Return curated sample WhatsApp messages for quick layperson testing."""
    return {"presets": PRESET_CATALOG}


@app.get("/api/academic-summary", response_model=AcademicSummaryResponse)
def get_academic_summary() -> dict[str, Any]:
    """Return research metadata, benchmark latency, and model comparison metrics."""
    metadata: dict[str, Any] = {}
    try:
        metadata = load_model_bundle().get("metadata", {})
    except FileNotFoundError as exc:
        logger.warning("Metadata model belum tersedia untuk ringkasan akademik: %s", exc)
        metadata = {}

    return {
        "thesis": {
            "title": (
                "Komparasi Algoritma Support Vector Machine dan Random Forest dalam "
                "Deteksi Pesan Phishing WhatsApp Mengatasnamakan Otoritas Perpajakan"
            ),
            "author": "Wan Mirza Dhani (240101020194)",
            "advisor": "Bapak Novi Dian Nathasia, S.Kom, MMSI.",
            "program": "PJJ Sistem Informasi, Universitas Siber Asia",
            "scheme": "Tugas Akhir Prototype (TKT Level 6)",
        },
        "metadata": metadata,
        "evaluation_rows": _load_evaluation_rows(),
        "latency_benchmark": _load_latency_benchmark(),
    }


@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest) -> dict[str, Any]:
    """Classify a single message and return verdict, layperson reasons, and highlights."""
    try:
        t0 = time.perf_counter()
        result = predict_message(req.text, top_k=req.top_k)
        result["inference_ms"] = round((time.perf_counter() - t0) * 1000, 2)
        return result
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except FileNotFoundError as exc:
        logger.error("Model bundle tidak ditemukan saat /predict: %s", exc)
        raise HTTPException(
            status_code=503, detail="Model klasifikasi sedang tidak tersedia."
        ) from exc


@app.post("/predict/batch", response_model=BatchPredictResponse)
def predict_batch(req: BatchPredictRequest, request: Request) -> JSONResponse | dict[str, Any]:
    """Classify up to 200 messages in a single vectorized request."""
    limit = _get_rate_limit_per_min()
    extra_cost = max(0, math.ceil(len(req.texts) / 10) - 1)
    if extra_cost > 0:
        client_ip = _resolve_client_ip(request)
        capped_cost = min(limit, extra_cost) if limit > 0 else extra_cost
        if _is_rate_limited(client_ip, limit, cost=capped_cost):
            retry_after = _seconds_until_reset(client_ip)
            return JSONResponse(
                status_code=429,
                content={"detail": "Kuota batch terlampaui. Coba lagi dalam 1 menit."},
                headers={**_SECURITY_HEADERS, "Retry-After": str(retry_after)},
            )

    try:
        results = predict_messages_batch(req.texts, top_k=req.top_k)
    except FileNotFoundError as exc:
        logger.error("Model bundle tidak ditemukan saat /predict/batch: %s", exc)
        raise HTTPException(
            status_code=503, detail="Model klasifikasi sedang tidak tersedia."
        ) from exc
    return {"total": len(req.texts), "results": results}
