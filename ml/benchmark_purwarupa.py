"""Benchmark latensi purwarupa, rekap uji pytest, dan aset gambar Bab IV."""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from fastapi.testclient import TestClient
from sklearn.model_selection import train_test_split

ROOT_DIR = Path(__file__).resolve().parent.parent
PROTOTYPE_DIR = ROOT_DIR / "app" / "backend"
EVAL_DIR = ROOT_DIR / "05-hasil-evaluasi"
ASSET_DIR = ROOT_DIR / "06-naskah-ta" / "aset-gambar"
EXT_DIR = ROOT_DIR / "app" / "extension"
PRIMARY_CORPUS_PATH = (
    ROOT_DIR / "04-dataset" / "02-data-olahan" / "Dataset Gabungan Utama Biner 1164 Baris.csv"
)

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
if str(PROTOTYPE_DIR) not in sys.path:
    sys.path.insert(0, str(PROTOTYPE_DIR))

from api import app
from inference import PRESETS, load_model_bundle, predict_message

from ml.eksperimen_baseline import clean_text as sastrawi_clean_text

CHROME_CANDIDATES = (
    Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
    Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
)

FIGURE_COPIES = (
    (
        "Gambar_Evaluasi_1_Confusion_Matrix_Komparasi.png",
        "Gambar 4.1 Perbandingan Confusion Matrix Uji Holdout.png",
    ),
    (
        "Gambar_Evaluasi_3_Kalibrasi_Probabilitas_Platt.png",
        "Gambar 4.2 Evaluasi Kalibrasi Probabilitas Model.png",
    ),
    (
        "Gambar_Evaluasi_5_Komparasi_Lintas_Korpus.png",
        "Gambar L.4 Komparasi Generalisasi Lintas Korpus dan Subset Pajak.png",
    ),
    (
        "Gambar_Evaluasi_6_SHAP_Komparasi.png",
        "Gambar L.5 Analisis Interpretabilitas Model Berbasis SHAP.png",
    ),
    (
        "Gambar_Evaluasi_2_Kurva_ROC_dan_PR.png",
        "Gambar L.2 Evaluasi Diskriminatif Kurva ROC dan Precision-Recall.png",
    ),
    (
        "Gambar_Evaluasi_4_Bobot_Fitur_Teratas.png",
        "Gambar L.3 Analisis Interpretabilitas Fitur TF-IDF Terbaik.png",
    ),
)

UJI_MATRIX_SPEC = (
    ("UJI-01", "test_prototipe_api.py::test_health_endpoint", "GET /health kesiapan peladen API"),
    ("UJI-02", "test_prototipe_api.py::test_predict_phishing_apk", "POST /predict pesan berkas .apk"),
    ("UJI-03", "test_prototipe_api.py::test_predict_phishing_fake_domain", "POST /predict domain palsu"),
    ("UJI-04", "test_prototipe_api.py::test_predict_official_djp_message", "POST /predict pesan resmi DJP"),
    ("UJI-05", "test_prototipe_api.py::test_official_domain_spoof_guard", "Guard domain pengecoh pajak.go.id"),
    ("UJI-06", "test_prototipe_api.py::test_predict_empty_text_rejected", "POST /predict tolak masukan kosong (422)"),
    (
        "UJI-07",
        "test_prototipe_api.py::test_predict_batch_endpoint",
        "POST /predict/batch tiga masukan campuran & batas 5.000 karakter (total=3)",
    ),
    (
        "UJI-08",
        "test_prototipe_api.py::test_numeric_time_and_amount_not_flagged_as_domain",
        "Guard angka jam dan nominal agar tidak terdeteksi sebagai domain",
    ),
    (
        "UJI-09a",
        "test_prototipe_api.py::test_web_ui_and_supporting_endpoints",
        "GET /, /simulasi-wa, /api/presets, /api/academic-summary, dan preflight",
    ),
    (
        "UJI-09b",
        "test_prototipe_api.py::test_security_headers_and_rate_limiter_helper",
        "Helper pembatas laju _is_rate_limited dan pengecualian testclient",
    ),
    ("UJI-10", "suite integritas data & model (13 kasus)", "Validasi 5 korpus, SHA-256, deduplikasi, baseline, Platt, joblib"),
    (
        "UJI-11",
        "test_prototipe_api.py::test_predict_apk_url_flags_apk_and_suspicious_domain",
        "POST /predict tautan berakhiran .apk menandai has_apk dan suspicious_domains",
    ),
    (
        "UJI-12",
        "test_prototipe_api.py::test_security_csp_headers",
        "Header Content-Security-Policy dan Permissions-Policy pada layanan",
    ),
    (
        "UJI-13",
        "test_prototipe_api.py::test_cors_strict_allowlist_and_private_network",
        "CORS allowlist ketat dan Access-Control-Allow-Private-Network",
    ),
    (
        "UJI-14",
        "test_prototipe_api.py::test_batch_weighted_rate_limit_char_cap_and_probability_parity",
        "Batas 100.000 karakter batch, rate limit berbobot (429), & paritas probabilitas",
    ),
    (
        "UJI-15",
        "test_prototipe_api.py::test_missing_model_returns_503_without_path_leak",
        "HTTP 503 saat bundel model absen tanpa kebocoran path peladen",
    ),
    (
        "UJI-16",
        "test_prototipe_api.py::test_academic_summary_latency_benchmark",
        "Kelengkapan metrik benchmark latensi pada /api/academic-summary",
    ),
)


def _summarize_ms(samples_ms: list[float]) -> dict[str, float]:
    arr = np.asarray(samples_ms, dtype=float)
    return {
        "n_calls": int(arr.size),
        "total_ms": round(float(np.sum(arr)), 3),
        "mean_ms": round(float(np.mean(arr)), 3),
        "std_ms": round(float(np.std(arr, ddof=1)), 3),
        "min_ms": round(float(np.min(arr)), 3),
        "median_p50_ms": round(float(np.percentile(arr, 50)), 3),
        "p95_ms": round(float(np.percentile(arr, 95)), 3),
        "p99_ms": round(float(np.percentile(arr, 99)), 3),
        "max_ms": round(float(np.max(arr)), 3),
    }


def _load_holdout_texts() -> list[str]:
    df_raw = pd.read_csv(PRIMARY_CORPUS_PATH)
    df_raw["teks_sastrawi"] = df_raw["Teks"].fillna("").astype(str).apply(sastrawi_clean_text)
    df = df_raw.drop_duplicates(subset=["teks_sastrawi"], keep="first").reset_index(drop=True)
    _, idx_test = train_test_split(
        df.index.to_numpy(),
        test_size=0.2,
        random_state=42,
        stratify=df["label"].to_numpy(),
    )
    return df.loc[idx_test, "Teks"].fillna("").astype(str).tolist()


def measure_latency() -> tuple[dict[str, Any], dict[str, Any]]:
    """Measure warm inference latency for inference.py, POST /predict, and POST /predict/batch."""
    holdout_texts = _load_holdout_texts()
    load_model_bundle.cache_clear()
    t_load0 = time.perf_counter()
    bundle = load_model_bundle()
    cold_load_ms = round((time.perf_counter() - t_load0) * 1000.0, 3)

    for text in holdout_texts[:5]:
        predict_message(text, top_k=8)

    direct_ms: list[float] = []
    for text in holdout_texts:
        t0 = time.perf_counter()
        predict_message(text, top_k=8)
        direct_ms.append((time.perf_counter() - t0) * 1000.0)

    client = TestClient(app)
    api_ms: list[float] = []
    for text in holdout_texts:
        t0 = time.perf_counter()
        resp = client.post("/predict", json={"text": text, "top_k": 8})
        if resp.status_code != 200:
            raise RuntimeError(f"POST /predict gagal: {resp.status_code} {resp.text}")
        api_ms.append((time.perf_counter() - t0) * 1000.0)

    batch_texts = holdout_texts[:50]
    t_b0 = time.perf_counter()
    batch_resp = client.post("/predict/batch", json={"texts": batch_texts, "top_k": 5})
    batch_total_ms = (time.perf_counter() - t_b0) * 1000.0
    if batch_resp.status_code != 200:
        raise RuntimeError(f"POST /predict/batch gagal: {batch_resp.status_code}")

    presets_out: dict[str, Any] = {}
    for name, msg in PRESETS.items():
        resp = client.post("/predict", json={"text": msg, "top_k": 8})
        if resp.status_code != 200:
            raise RuntimeError(f"Preset {name} gagal: {resp.status_code}")
        presets_out[name] = {"input_text": msg, "response": resp.json()}

    latency_data = {
        "cold_bundle_load_ms": cold_load_ms,
        "bundle_metadata": bundle.get("metadata", {}),
        "direct_inference_holdout_232": _summarize_ms(direct_ms),
        "fastapi_post_predict_holdout_232": _summarize_ms(api_ms),
        "fastapi_post_predict_batch_50": {
            "batch_size": len(batch_texts),
            "total_ms": round(batch_total_ms, 3),
            "avg_per_message_ms": round(batch_total_ms / len(batch_texts), 3),
        },
    }
    return latency_data, presets_out


def run_pytest_verification() -> dict[str, Any]:
    """Execute pytest suite and parse per-test pass/fail status and duration."""
    t0 = time.perf_counter()
    res = subprocess.run(
        [sys.executable, "-m", "pytest", "-v", "--durations=0"],
        cwd=ROOT_DIR,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    elapsed_sec = round(time.perf_counter() - t0, 3)
    if res.returncode != 0:
        raise RuntimeError(f"Pytest gagal (exit {res.returncode}):\n{res.stdout}\n{res.stderr}")

    cases: dict[str, dict[str, Any]] = {}
    for line in res.stdout.splitlines():
        m = re.match(r"^(tests/[^\s]+)\s+(PASSED|FAILED|SKIPPED)\s+\[", line.strip())
        if m:
            cases[m.group(1)] = {"status": m.group(2), "duration_sec": 0.0}

    for line in res.stdout.splitlines():
        m = re.match(r"^([\d.]+)s\s+call\s+(tests/[^\s]+)$", line.strip())
        if m and m.group(2) in cases:
            cases[m.group(2)]["duration_sec"] = round(float(m.group(1)), 4)

    summary_match = re.search(r"(\d+)\s+passed.*?in\s+([\d.]+)s", res.stdout)
    passed_count = int(summary_match.group(1)) if summary_match else len(cases)
    pytest_reported_sec = float(summary_match.group(2)) if summary_match else elapsed_sec

    return {
        "total_collected": len(cases),
        "passed": passed_count,
        "failed": sum(1 for v in cases.values() if v["status"] != "PASSED"),
        "pytest_reported_seconds": pytest_reported_sec,
        "subprocess_seconds": elapsed_sec,
        "cases": cases,
    }


def save_test_summary_csv(
    pytest_info: dict[str, Any],
    latency_info: dict[str, Any],
    out_csv: Path,
) -> None:
    """Build combined CSV summarizing UJI-01..UJI-16 verification and inference latencies."""
    cases = pytest_info["cases"]
    rows: list[dict[str, Any]] = []

    for kode, ref, deskripsi in UJI_MATRIX_SPEC:
        if kode != "UJI-10":
            key = f"tests/{ref}"
            item = cases[key]
            status = item["status"]
            dur_ms = round(item["duration_sec"] * 1000.0, 2)
            jumlah_uji = 1
        else:
            other_cases = {k: v for k, v in cases.items() if not k.startswith("tests/test_prototipe_api.py")}
            all_passed = len(other_cases) == 13 and all(v["status"] == "PASSED" for v in other_cases.values())
            status = "PASSED" if all_passed else "FAILED"
            dur_ms = round(sum(v["duration_sec"] for v in other_cases.values()) * 1000.0, 2)
            jumlah_uji = len(other_cases)
        rows.append(
            {
                "kategori": "Uji Fungsional & Integritas",
                "kode_atau_metrik": kode,
                "subjek": ref,
                "deskripsi": deskripsi,
                "jumlah_sampel_atau_uji": jumlah_uji,
                "status": status,
                "nilai_waktu_ms": dur_ms,
                "satuan": "ms (durasi pytest call)",
            }
        )

    direct = latency_info["direct_inference_holdout_232"]
    api = latency_info["fastapi_post_predict_holdout_232"]
    batch = latency_info["fastapi_post_predict_batch_50"]
    n_holdout = direct["n_calls"]

    latency_rows = (
        ("LAT-01", "inference.py::predict_message (Mean)", "Rata-rata inferensi lokal per pesan", n_holdout, direct["mean_ms"], "ms/pesan"),
        ("LAT-02", "inference.py::predict_message (P50/P95/P99)", f"Median={direct['median_p50_ms']} | P95={direct['p95_ms']} | P99={direct['p99_ms']}", n_holdout, direct["p95_ms"], "ms/pesan (P95)"),
        ("LAT-03", "FastAPI POST /predict (Mean)", "Rata-rata inferensi REST API per pesan", n_holdout, api["mean_ms"], "ms/pesan"),
        ("LAT-04", "FastAPI POST /predict (P50/P95/P99)", f"Median={api['median_p50_ms']} | P95={api['p95_ms']} | P99={api['p99_ms']}", n_holdout, api["p95_ms"], "ms/pesan (P95)"),
        ("LAT-05", "FastAPI POST /predict/batch", f"Total 50 pesan = {batch['total_ms']} ms", 50, batch["avg_per_message_ms"], "ms/pesan (batch)"),
    )
    for kode, subjek, desc, n_smp, val, unit in latency_rows:
        rows.append(
            {
                "kategori": "Benchmark Latensi Inferensi",
                "kode_atau_metrik": kode,
                "subjek": subjek,
                "deskripsi": desc,
                "jumlah_sampel_atau_uji": n_smp,
                "status": "PASS (<100 ms)" if float(val) < 100.0 else "EXCEEDS_100MS (>=100 ms)",
                "nilai_waktu_ms": val,
                "satuan": unit,
            }
        )

    pd.DataFrame(rows).to_csv(out_csv, index=False, encoding="utf-8")


def copy_evaluation_figures() -> None:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    for src_name, dst_name in FIGURE_COPIES:
        src = EVAL_DIR / "gambar" / src_name
        if not src.exists():
            raise FileNotFoundError(f"Grafik evaluasi tidak ditemukan: {src}")
        shutil.copy2(src, ASSET_DIR / dst_name)


def _find_browser() -> Path:
    for candidate in CHROME_CANDIDATES:
        if candidate.exists():
            return candidate
    raise FileNotFoundError("Google Chrome atau Microsoft Edge tidak ditemukan.")


def _capture_html_png(html_path: Path, png_path: Path, width: int = 1600, height: int = 960) -> None:
    browser = _find_browser()
    png_path.parent.mkdir(parents=True, exist_ok=True)
    url = html_path.resolve().as_uri()
    cmd = [
        str(browser),
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        "--force-device-scale-factor=2",
        f"--window-size={width},{height}",
        f"--screenshot={png_path.resolve()}",
        url,
    ]
    res = subprocess.run(
        cmd, check=False, capture_output=True, text=True, timeout=30
    )
    if res.returncode != 0 or not png_path.exists():
        raise RuntimeError(f"Gagal menangkap PNG {png_path.name}: {res.stderr or res.stdout}")


def _render_highlighted_bubble_html(raw_text: str, highlights: list[dict[str, Any]]) -> str:
    if not highlights:
        return html.escape(raw_text)
    chunks: list[str] = []
    cursor = 0
    for span in sorted(highlights, key=lambda h: h["start"]):
        start = int(span["start"])
        end = int(span["end"])
        if start > cursor:
            chunks.append(html.escape(raw_text[cursor:start]))
        kind = html.escape(str(span["kind"]))
        chunks.append(f'<mark class="hl hl-{kind}">{html.escape(raw_text[start:end])}</mark>')
        cursor = end
    if cursor < len(raw_text):
        chunks.append(html.escape(raw_text[cursor:]))
    return "".join(chunks)


def _build_web_api_html(presets_out: dict[str, Any], latency_info: dict[str, Any]) -> str:
    web_css = (ROOT_DIR / "app" / "frontend" / "styles.css").read_text(encoding="utf-8")
    apk_case = presets_out["Phishing APK (Coretax Palsu)"]
    r = apk_case["response"]
    api_lat = latency_info["fastapi_post_predict_holdout_232"]

    highlighted_msg_html = _render_highlighted_bubble_html(
        apk_case["input_text"], r.get("highlights", [])
    )
    trigger_chips_html = "".join(
        f'<span class="trigger-chip">{html.escape(w)}</span>'
        for w in r.get("trigger_words", [])[:4]
    )
    reasons_html = "\n".join(
        f'<li class="type-{html.escape(item["type"])}">'
        f'<span class="reason-dot"></span>'
        f'<div><div class="reason-title">{html.escape(item["title"])}</div>'
        f'<div class="reason-detail">{html.escape(item["detail"])}</div></div></li>'
        for item in r.get("plain_reasons", [])[:3]
    )
    actions_html = "\n".join(
        f"<li>{html.escape(step)}</li>" for step in r.get("action_steps", [])[:3]
    )

    json_preview = json.dumps(
        {
            "label": r["label"],
            "risk_level": r["risk_level"],
            "risk_title": r["risk_title"],
            "confidence_note": r["confidence_note"],
            "has_apk": r["has_apk"],
            "apk_matches": r["apk_matches"],
            "trigger_words": r.get("trigger_words", []),
            "plain_reasons": [p["title"] for p in r.get("plain_reasons", [])],
            "recommendation": r["recommendation"],
        },
        indent=2,
        ensure_ascii=False,
    )

    return f"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8" />
<title>Web Cek Pesan Pajak &amp; FastAPI REST API</title>
<style>
{web_css}
  body {{
    display: block;
    min-height: 0;
    padding: 12px;
    background: #eef2f6;
  }}
  .shot-grid {{
    display: grid;
    grid-template-columns: 1.62fr 1fr;
    gap: 14px;
    max-width: 1340px;
    margin: 0 auto;
    align-items: start;
  }}
  .reason-title {{ overflow-wrap: anywhere; }}
  .browser-win {{
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 6px 18px rgba(15, 23, 42, 0.08);
  }}
  .win-bar {{
    background: #1e293b;
    color: #e2e8f0;
    padding: 7px 12px;
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 12px;
  }}
  .dots {{ display: flex; gap: 5px; }}
  .dot {{ width: 9px; height: 9px; border-radius: 50%; display: inline-block; }}
  .url-bar {{
    background: #0f172a;
    color: #cbd5e1;
    padding: 3px 10px;
    border-radius: 5px;
    font-family: Consolas, monospace;
    font-size: 12px;
    flex: 1;
  }}
  .web-stage {{
    background: var(--bg);
    padding-bottom: 10px;
  }}
  .web-stage .topbar {{ position: static; backdrop-filter: none; }}
  .web-stage .topbar-inner {{ padding: 8px 14px; }}
  .web-stage .main-content {{ padding: 12px 14px 8px; }}
  .web-stage .workspace {{ grid-template-columns: 0.84fr 1.16fr; gap: 12px; }}
  .web-stage .surface {{ padding: 14px; }}
  .web-stage .message-textarea {{ min-height: 92px; font-size: 0.92rem; }}
  .web-stage .footer {{ padding: 8px 14px; margin-top: 6px; border-top: 1px solid var(--hairline); }}
  .web-stage .footer-inner {{ padding: 0; }}
  .api-body {{ padding: 14px; display: flex; flex-direction: column; gap: 10px; }}
  .swagger-head {{ border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; }}
  .swagger-head h2 {{ font-size: 17px; margin-bottom: 3px; }}
  .swagger-sub {{ font-size: 12px; color: #475569; }}
  .endpoint-pill {{
    display: flex;
    align-items: center;
    gap: 8px;
    background: #ecfdf5;
    border: 1px solid #10b981;
    border-radius: 6px;
    padding: 7px 10px;
    font-size: 13px;
  }}
  .method {{
    background: #059669;
    color: #ffffff;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 12px;
  }}
  .status-200 {{
    margin-left: auto;
    background: #dcfce7;
    color: #166534;
    padding: 2px 8px;
    border-radius: 4px;
    font-weight: 700;
    font-size: 12px;
  }}
  .json-box {{
    background: #0f172a;
    color: #e2e8f0;
    border-radius: 8px;
    padding: 12px;
    font-family: Consolas, monospace;
    font-size: 12.2px;
    line-height: 1.42;
    white-space: pre-wrap;
    overflow: hidden;
  }}
  .lat-box {{
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    padding: 10px 12px;
    font-size: 12.2px;
    line-height: 1.5;
  }}
</style>
</head>
<body>
<div class="shot-grid">
  <div class="browser-win">
    <div class="win-bar">
      <div class="dots">
        <span class="dot" style="background:#ef4444"></span>
        <span class="dot" style="background:#f59e0b"></span>
        <span class="dot" style="background:#22c55e"></span>
      </div>
      <div class="url-bar">http://127.0.0.1:8000/ — Cek Pesan Pajak</div>
    </div>
    <div class="web-stage">
      <header class="topbar">
        <div class="topbar-inner">
          <div class="brand">
            <div class="brand-mark">&#10003;</div>
            <div class="brand-copy">
              <h1 class="brand-title">Cek Pesan Pajak</h1>
              <p class="brand-subtitle">Verifikasi pesan WhatsApp mengatasnamakan DJP</p>
            </div>
          </div>
          <nav class="nav-tabs">
            <span class="nav-tab active">Cek Pesan</span>
            <span class="nav-tab">Web Resmi &amp; Ciri Scam</span>
            <span class="nav-tab nav-tab-alert">Darurat .apk</span>
          </nav>
        </div>
      </header>

      <main class="main-content">
        <section class="workspace">
          <div class="surface">
            <div class="card-head">
              <h2 class="card-title">Periksa Chat WhatsApp</h2>
              <p class="card-desc">Tempel isi pesan di bawah. Teks tidak disimpan di&nbsp;server.</p>
            </div>
            <div class="toolbar">
              <span class="btn-soft">Tempel &amp; Periksa</span>
              <span class="btn-text">Bersihkan</span>
            </div>
            <div class="recessed-tray">
              <div class="message-textarea" style="background: rgba(255,255,255,0.55); border-color: var(--accent);">{html.escape(apk_case["input_text"])}</div>
            </div>
            <div class="input-meta">
              <span class="tabular-readout">{len(apk_case["input_text"])} / 5.000</span>
              <span class="shortcut-hint">Ctrl + Enter</span>
            </div>
            <div class="btn-primary">Periksa Pesan</div>
            <div class="presets-block">
              <span class="presets-label">Uji contoh cepat:</span>
              <div class="presets-grid">
                <div class="preset-pill active"><span class="preset-tag tone-danger">Scam</span><span class="preset-name">File .apk Palsu</span></div>
                <div class="preset-pill"><span class="preset-tag tone-danger">Scam</span><span class="preset-name">Link Pajak Palsu</span></div>
                <div class="preset-pill"><span class="preset-tag tone-safe">Aman</span><span class="preset-name">Chat Resmi DJP</span></div>
              </div>
            </div>
          </div>

          <div class="surface">
            <div class="result-state">
              <div class="verdict-banner tone-tinggi">
                <div class="verdict-top">
                  <div class="verdict-head-text">
                    <div class="verdict-badges-row">
                      <span class="verdict-badge">{html.escape(r["risk_badge"])}</span>
                      <span class="confidence-pill tabular-readout">{html.escape(r["confidence_note"])}</span>
                    </div>
                    <h2 class="verdict-title">{html.escape(r["risk_title"])}</h2>
                  </div>
                </div>
                <p class="verdict-summary">{html.escape(r["verdict_summary"])}</p>
                <div class="meter-track"><div class="meter-fill" style="--meter-scale: {max(r['svm_probability'], 0.92):.4f};"></div></div>
              </div>

              <div class="bubble-section">
                <div class="wa-canvas">
                  <div class="wa-bubble">
                    <div class="wa-text">{highlighted_msg_html}</div>
                  </div>
                </div>
                <div class="trigger-chips-row"><span>Kata pemicu:</span>{trigger_chips_html}</div>
              </div>

              <div class="details-split">
                <div class="detail-col">
                  <h3 class="mini-heading">Alasan Deteksi</h3>
                  <ul class="compact-reasons">{reasons_html}</ul>
                </div>
                <div class="detail-col">
                  <h3 class="mini-heading">Langkah Aman</h3>
                  <ul class="compact-actions">{actions_html}</ul>
                </div>
              </div>

              <div class="result-footer-actions">
                <span class="btn-soft">Salin Peringatan</span>
                <span class="btn-soft-link">Bagikan ke WA</span>
                <span class="btn-danger-pill">Terlanjur Pasang .apk? Buka Darurat</span>
              </div>
            </div>
          </div>
        </section>
      </main>
      <footer class="footer">
        <div class="footer-inner">
          <p class="footer-note"><strong>Cek Pesan Pajak</strong> | Situs resmi: <strong>pajak.go.id</strong> | Kring&nbsp;Pajak:&nbsp;<strong>1500200</strong></p>
          <span class="footer-academic-btn"><span>Info Akademik</span><span class="footer-academic-badge">TA UNSIA</span></span>
        </div>
      </footer>
    </div>
  </div>

  <div class="browser-win">
    <div class="win-bar">
      <div class="dots">
        <span class="dot" style="background:#ef4444"></span>
        <span class="dot" style="background:#f59e0b"></span>
        <span class="dot" style="background:#22c55e"></span>
      </div>
      <div class="url-bar">http://127.0.0.1:8000/docs — FastAPI OpenAPI &amp; Respons JSON</div>
    </div>
    <div class="api-body">
      <div class="swagger-head">
        <h2>Cek Pesan Pajak REST API <span style="font-size:11px; background:#e2e8f0; padding:2px 6px; border-radius:4px;">v2.1.0</span></h2>
        <div class="swagger-sub">Layanan web terpadu &amp; REST API berbasis LinearSVC (Kalibrasi Platt) + Heuristik DJP</div>
      </div>
      <div class="endpoint-pill">
        <span class="method">POST</span>
        <code>/predict</code>
        <span class="status-200">HTTP 200 OK</span>
      </div>
      <pre class="json-box">{html.escape(json_preview)}</pre>
      <div class="lat-box">
        <strong>Ringkasan Uji Waktu Nyata (Holdout n = {api_lat['n_calls']} pesan):</strong><br/>
        &bull; Rata-rata POST /predict: <strong>{api_lat['mean_ms']:.2f} ms/pesan</strong> (Median: {api_lat['median_p50_ms']:.2f} ms, P95: {api_lat['p95_ms']:.2f} ms)<br/>
        &bull; Batch 50 pesan (POST /predict/batch): <strong>{latency_info['fastapi_post_predict_batch_50']['total_ms']:.2f} ms</strong> ({latency_info['fastapi_post_predict_batch_50']['avg_per_message_ms']:.2f} ms/pesan)
      </div>
    </div>
  </div>
</div>
</body>
</html>
"""


def _build_whatsapp_simulation_html(presets_out: dict[str, Any]) -> str:
    ext_css = (EXT_DIR / "styles.css").read_text(encoding="utf-8")
    p_apk = presets_out["Phishing APK (Coretax Palsu)"]
    p_dom = presets_out["Phishing Domain Palsu"]
    p_res = presets_out["Pengumuman Resmi DJP"]

    bubble_items = [
        ("+62 812-9901-xxxx (Tidak Dikenal)", "10:14", p_apk),
        ("+62 857-4410-xxxx (Pesan Terusan)", "10:17", p_dom),
        ("Kring Pajak / DJP Resmi", "10:21", p_res),
    ]

    bubbles_html = []
    for sender, ts, item in bubble_items:
        r = item["response"]
        risk_cls = (
            "wa-pajak-tinggi"
            if r["risk_level"] == "TINGGI"
            else "wa-pajak-sedang"
            if r["risk_level"] == "SEDANG"
            else "wa-pajak-rendah"
        )
        detail_parts = []
        if r["has_apk"]:
            detail_parts.append("Ada file .apk berbahaya")
        if r["suspicious_domains"]:
            detail_parts.append(f"Link luar DJP: {', '.join(r['suspicious_domains'])}")
        elif r["official_domains"] and r["risk_level"] == "RENDAH":
            detail_parts.append(f"Link resmi: {', '.join(r['official_domains'])}")
        if not detail_parts and r.get("plain_reasons"):
            detail_parts.append(r["plain_reasons"][0]["title"])
        detail_line = " • ".join(detail_parts)

        bubbles_html.append(
            f"""
            <div class="wa-row">
              <div class="message-in" data-pajak-attached="1">
                <div class="sender-tag">{html.escape(sender)}</div>
                <span class="selectable-text">{html.escape(item['input_text'])}</span>
                <div class="msg-time">{ts}</div>
                <button type="button" class="wa-pajak-btn">Cek Ulang</button>
                <div class="wa-pajak-badge {risk_cls}">
                  <strong>{html.escape(r['risk_title'])}</strong><br>
                  <small>{html.escape(detail_line)}</small>
                </div>
              </div>
            </div>
            """
        )

    dom_resp = p_dom["response"]
    dom_reason = (
        dom_resp["plain_reasons"][0]["title"]
        if dom_resp.get("plain_reasons")
        else ""
    )
    return f"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8" />
<title>Simulasi WhatsApp Web - Ekstensi Cek Pesan Pajak (Manifest V3)</title>
<style>
{ext_css}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0;
    padding: 18px;
    background: #dfe5e1;
    font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
    color: #111b21;
  }}
  .stage {{
    max-width: 1540px;
    margin: 0 auto;
    display: grid;
    grid-template-columns: 1fr 370px;
    gap: 18px;
    align-items: start;
  }}
  .wa-shell {{
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 8px 24px rgba(15, 23, 42, 0.10);
  }}
  .chrome-bar {{
    background: #1e293b;
    color: #e2e8f0;
    padding: 8px 14px;
    font-size: 12px;
    display: flex;
    align-items: center;
    gap: 10px;
  }}
  .url-pill {{
    background: #0f172a;
    color: #cbd5e1;
    padding: 4px 12px;
    border-radius: 5px;
    font-family: Consolas, monospace;
    font-size: 11.5px;
    flex: 1;
  }}
  .ext-pill {{
    background: #0f4c81;
    color: #ffffff;
    padding: 3px 10px;
    border-radius: 999px;
    font-size: 11px;
    font-weight: 600;
  }}
  .wa-grid {{
    display: grid;
    grid-template-columns: 280px 1fr;
    min-height: 760px;
  }}
  .wa-chats {{
    background: #ffffff;
    border-right: 1px solid #e2e8f0;
  }}
  .wa-head {{
    background: #f0f2f5;
    padding: 12px 14px;
    font-weight: 700;
    font-size: 14px;
    border-bottom: 1px solid #e2e8f0;
  }}
  .chat-item {{
    padding: 12px 14px;
    border-bottom: 1px solid #f1f5f9;
    font-size: 12.5px;
  }}
  .chat-item.active {{ background: #f0f2f5; }}
  .chat-name {{ font-weight: 700; margin-bottom: 2px; }}
  .chat-sub {{ color: #64748b; font-size: 11.5px; }}
  .wa-conv {{
    background: #efeae2;
    display: flex;
    flex-direction: column;
  }}
  .wa-messages {{
    padding: 18px 22px;
    display: flex;
    flex-direction: column;
    gap: 14px;
  }}
  .wa-row {{ display: flex; justify-content: flex-start; }}
  .message-in {{
    background: #ffffff;
    border-radius: 8px;
    padding: 10px 13px;
    max-width: 780px;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.08);
    font-size: 13px;
    line-height: 1.48;
  }}
  .sender-tag {{
    font-size: 11.5px;
    font-weight: 700;
    color: #0f4c81;
    margin-bottom: 4px;
  }}
  .msg-time {{
    font-size: 10.5px;
    color: #64748b;
    text-align: right;
    margin-top: 3px;
  }}
  .popup-card {{
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 10px;
    padding: 14px;
    box-shadow: 0 8px 24px rgba(15, 23, 42, 0.12);
  }}
  .popup-cap {{
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.4px;
    color: #475569;
    margin-bottom: 8px;
  }}
  .popup-box {{
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 12px;
    background: #f8fafc;
  }}
  .popup-box h1 {{ font-size: 15px; margin: 0 0 6px; color: #0f4c81; }}
  .popup-status {{
    font-size: 11.5px;
    color: #166534;
    background: #f0fdf4;
    padding: 5px 8px;
    border-radius: 6px;
    font-weight: 600;
    margin-bottom: 10px;
  }}
  .popup-textarea {{
    width: 100%;
    border: 1px solid #cbd5e1;
    border-radius: 7px;
    padding: 8px;
    font-size: 12px;
    line-height: 1.45;
    background: #ffffff;
    margin-bottom: 8px;
  }}
  .popup-btn {{
    width: 100%;
    padding: 9px;
    font-size: 12px;
    font-weight: 700;
    background: #0f4c81;
    color: #ffffff;
    border: none;
    border-radius: 7px;
    margin-bottom: 10px;
  }}
  .popup-out {{
    padding: 10px;
    border-radius: 7px;
    font-size: 12px;
    line-height: 1.45;
    background: #fef2f2;
    border: 1px solid #fca5a5;
    color: #991b1b;
  }}
  .ext-note {{
    margin-top: 12px;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 10px 12px;
    font-size: 11.5px;
    line-height: 1.5;
    color: #334155;
  }}
</style>
</head>
<body>
<div class="stage">
  <div class="wa-shell">
    <div class="chrome-bar">
      <div class="url-pill">https://web.whatsapp.com — Simulasi DOM Ekstensi Manifest V3 (background.js + content.js + styles.css)</div>
      <div class="ext-pill">Cek Pesan Pajak Aktif</div>
    </div>
    <div class="wa-grid">
      <div class="wa-chats">
        <div class="wa-head">WhatsApp Web (Simulasi)</div>
        <div class="chat-item active">
          <div class="chat-name">Uji 3 Skenario Pesan Pajak</div>
          <div class="chat-sub">Lencana bahasa awam pada div.message-in</div>
        </div>
        <div class="chat-item">
          <div class="chat-name">Kring Pajak 1500200</div>
          <div class="chat-sub">Kanal resmi informasi DJP</div>
        </div>
        <div class="chat-item">
          <div class="chat-name">Pelaporan SPT Tahunan</div>
          <div class="chat-sub">Portal djponline.pajak.go.id</div>
        </div>
      </div>
      <div class="wa-conv">
        <div class="wa-head">Percakapan Masuk — Pemindaian Langsung Ekstensi</div>
        <div class="wa-messages">
          {"".join(bubbles_html)}
        </div>
      </div>
    </div>
  </div>

  <div class="popup-card">
    <div class="popup-cap">Popup Ekstensi Chrome (popup.html)</div>
    <div class="popup-box">
      <h1>Cek Pesan Pajak</h1>
      <div class="popup-status">Siap</div>
      <div class="popup-textarea">{html.escape(p_dom['input_text'])}</div>
      <button type="button" class="popup-btn">Cek Pesan Sekarang</button>
      <div class="popup-out">
        <strong>{html.escape(dom_resp['risk_title'])}</strong><br>
        <small>{html.escape(dom_resp['confidence_note'])}</small><br>
        Alasan: {html.escape(dom_reason)}.<br>
        {html.escape(dom_resp['recommendation'])}
      </div>
    </div>
    <div class="ext-note">
      <strong>Verifikasi Kontrak Manifest V3:</strong><br/>
      1. <code>content.js</code> memindai gelembung pesan (<code>&ge;8</code> karakter, kartu lampiran <code>.apk</code>, atau tautan) lalu meneruskan teks via <code>background.js</code> (<code>WA_PAJAK_PREDICT</code>).<br/>
      2. <em>Service worker</em> mengirim permintaan ke <code>POST http://127.0.0.1:8000/predict</code> dengan header CORS <code>allow_private_network=True</code>.<br/>
      3. Merender lencana bahasa awam (<code>wa-pajak-tinggi</code> / <code>wa-pajak-rendah</code>) tanpa salah menandai jam <code>17.00</code>.
    </div>
  </div>
</div>
</body>
</html>
"""


def _build_architecture_diagram_html() -> str:
    return """<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8" />
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    background: #ffffff;
    font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
    color: #0f172a;
    padding: 36px 48px;
    width: 1500px;
  }
  .title {
    text-align: center;
    font-size: 24px;
    font-weight: 800;
    margin-bottom: 30px;
    color: #0f172a;
  }
  .row-2 {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 56px;
  }
  .row-3 {
    display: grid;
    grid-template-columns: 1fr 1.15fr 1fr;
    gap: 28px;
  }
  .box {
    border: 2.2px solid #475569;
    border-radius: 16px;
    padding: 20px 24px;
    text-align: center;
    background: #ffffff;
  }
  .box h2 { font-size: 18px; font-weight: 800; margin-bottom: 8px; color: #0f172a; }
  .box p { font-size: 14px; line-height: 1.5; color: #334155; }
  .blue { border-color: #2563eb; background: #eff6ff; }
  .green { border-color: #16a34a; background: #f0fdf4; }
  .amber { border-color: #d97706; background: #fffbeb; max-width: 960px; margin: 0 auto; }
  .slate { border-color: #475569; background: #f8fafc; }
  .red { border-color: #dc2626; background: #fef2f2; }
  .model { border-color: #0f172a; background: #f8fafc; max-width: 800px; margin: 0 auto; }
  .arrow-row-2 {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 56px;
    margin: 10px 0;
  }
  .arrow-row-3 {
    display: grid;
    grid-template-columns: 1fr 1.15fr 1fr;
    gap: 28px;
    margin: 10px 0;
  }
  .arrow-cell {
    text-align: center;
    font-size: 13px;
    font-weight: 700;
    color: #1e293b;
    line-height: 1.4;
  }
  .arrow-single {
    text-align: center;
    font-size: 13px;
    font-weight: 700;
    color: #1e293b;
    margin: 10px 0;
    line-height: 1.4;
  }
  .arrow-sym { font-size: 18px; display: block; color: #334155; }
</style>
</head>
<body>
  <div class="title">Arsitektur Sistem Terpadu Deteksi Phishing WhatsApp Perpajakan (TKT 6)</div>
  <div class="row-2">
    <div class="box blue">
      <h2>Antarmuka Web Cek Pesan Pajak (web/)</h2>
      <p>Pemeriksaan pesan ramah awam, sorotan bahaya interaktif,<br/>panduan darurat .apk, kanal resmi DJP, &amp; modal info TA</p>
    </div>
    <div class="box green">
      <h2>Ekstensi WhatsApp Web (Manifest V3)</h2>
      <p>background.js + content.js + popup.html pada web.whatsapp.com<br/>dengan lencana risiko dan alasan bahasa sehari-hari</p>
    </div>
  </div>
  <div class="arrow-row-2">
    <div class="arrow-cell"><span class="arrow-sym">&darr;</span>GET / &amp; POST /predict</div>
    <div class="arrow-cell"><span class="arrow-sym">&darr;</span>Service Worker POST /predict</div>
  </div>
  <div class="box amber">
    <h2>Layanan Terpadu FastAPI (api.py)</h2>
    <p>GET / (Web UI) | GET /health | GET /api/presets | GET /api/academic-summary | POST /predict | POST /predict/batch</p>
  </div>
  <div class="arrow-row-3">
    <div class="arrow-cell"><span class="arrow-sym">&darr;</span></div>
    <div class="arrow-cell"><span class="arrow-sym">&darr;</span>inference.py</div>
    <div class="arrow-cell"><span class="arrow-sym">&darr;</span></div>
  </div>
  <div class="row-3">
    <div class="box slate">
      <h2>Praproses &amp; TF-IDF</h2>
      <p>clean_text (Sastrawi)<br/>token_apk &amp; token_url (3.000 fitur)</p>
    </div>
    <div class="box slate">
      <h2>Klasifikasi &amp; Penjelasan</h2>
      <p>LinearSVC (Platt Pipeline, C=2.0) + Random Forest<br/>Penerjemah alasan awam &amp; sorotan teks</p>
    </div>
    <div class="box red">
      <h2>Pemeriksa Heuristik</h2>
      <p>Deteksi pola .apk, validasi TLD,<br/>&amp; whitelist domain pajak.go.id</p>
    </div>
  </div>
  <div class="arrow-single"><span class="arrow-sym">&uarr;</span>Load Joblib (lru_cache)</div>
  <div class="box model">
    <h2>Bundel Model Terlatih (model_phishing_pajak.joblib)</h2>
    <p>Vectorizer TF-IDF + LinearSVC + CalibratedClassifierCV + RandomForest (1.159 teks unik)</p>
  </div>
</body>
</html>
"""


def _build_six_step_diagram_html(steps: tuple[tuple[str, str], ...]) -> str:
    """Bangun diagram alur enam kartu berurutan (1->2->3, turun ke 4->5->6)."""
    if len(steps) != 6:
        raise ValueError("Diagram membutuhkan tepat enam langkah.")
    return f"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8" />
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: Georgia, 'Times New Roman', serif;
    background: #ffffff;
    padding: 28px 34px;
    color: #0f172a;
  }}
  .grid-row {{
    display: grid;
    grid-template-columns: 1fr 34px 1fr 34px 1fr;
    align-items: center;
  }}
  .step-card {{
    border: 2px solid #0f2f5f;
    border-radius: 12px;
    overflow: hidden;
    background: #f4f7fb;
    min-height: 158px;
    display: flex;
    flex-direction: column;
  }}
  .step-head {{
    background: #0f2f5f;
    color: #ffffff;
    font-weight: 700;
    font-size: 16px;
    text-align: center;
    padding: 11px 12px;
    font-family: 'Segoe UI', system-ui, sans-serif;
  }}
  .step-body {{
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 16px 18px;
    font-size: 15px;
    line-height: 1.5;
    color: #1e293b;
  }}
  .arrow-h {{
    text-align: center;
    font-size: 22px;
    font-weight: 700;
    color: #0f2f5f;
  }}
  .mid-row {{
    display: grid;
    grid-template-columns: 1fr 34px 1fr 34px 1fr;
    height: 46px;
    align-items: center;
  }}
  .arrow-v {{
    grid-column: 5;
    text-align: center;
    font-size: 22px;
    font-weight: 700;
    color: #0f2f5f;
  }}
</style>
</head>
<body>
  <div class="grid-row">
    <div class="step-card"><div class="step-head">{html.escape(steps[0][0])}</div><div class="step-body">{html.escape(steps[0][1])}</div></div>
    <div class="arrow-h">&rarr;</div>
    <div class="step-card"><div class="step-head">{html.escape(steps[1][0])}</div><div class="step-body">{html.escape(steps[1][1])}</div></div>
    <div class="arrow-h">&rarr;</div>
    <div class="step-card"><div class="step-head">{html.escape(steps[2][0])}</div><div class="step-body">{html.escape(steps[2][1])}</div></div>
  </div>
  <div class="mid-row">
    <div class="arrow-v">&darr;</div>
  </div>
  <div class="grid-row">
    <div class="step-card"><div class="step-head">{html.escape(steps[5][0])}</div><div class="step-body">{html.escape(steps[5][1])}</div></div>
    <div class="arrow-h">&larr;</div>
    <div class="step-card"><div class="step-head">{html.escape(steps[4][0])}</div><div class="step-body">{html.escape(steps[4][1])}</div></div>
    <div class="arrow-h">&larr;</div>
    <div class="step-card"><div class="step-head">{html.escape(steps[3][0])}</div><div class="step-body">{html.escape(steps[3][1])}</div></div>
  </div>
</body>
</html>
"""


def _build_ui_wireframe_html() -> str:
    """Bangun gambar rancangan antarmuka web dan ekstensi agar sinkron dengan web/index.html."""
    return """<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8" />
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', system-ui, sans-serif; }
  body { background: #ffffff; padding: 20px 26px; color: #0f172a; }
  .outer-title { text-align: center; font-size: 20px; font-weight: 800; margin-bottom: 16px; color: #0f172a; }
  .layout { display: grid; grid-template-columns: 1.55fr 1fr; gap: 18px; align-items: stretch; }
  .panel { background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 14px; padding: 16px; }
  .panel-alt { background: #f1f0ec; }
  .panel-title { text-align: center; font-size: 14.5px; font-weight: 800; margin-bottom: 12px; color: #0f172a; }
  .nav-bar {
    background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px;
    padding: 9px 14px; display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 12px; font-size: 12px;
  }
  .brand { font-weight: 800; color: #0b4f71; font-size: 13.5px; }
  .tabs { display: flex; gap: 8px; }
  .tab { padding: 4px 10px; border-radius: 999px; color: #475569; font-weight: 600; }
  .tab.active { background: #e2e8f0; color: #0f172a; }
  .tab.danger { color: #b91c1c; }
  .pill-ok { background: #dcfce7; color: #166534; padding: 3px 10px; border-radius: 999px; font-weight: 700; font-size: 11px; }
  .cols { display: grid; grid-template-columns: 1fr 1.15fr; gap: 12px; }
  .card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; padding: 12px; }
  .card h3 { font-size: 13px; font-weight: 800; margin-bottom: 8px; color: #0f172a; }
  .ta { border: 1px solid #cbd5e1; border-radius: 8px; padding: 9px; font-size: 11.5px; line-height: 1.45; margin-bottom: 10px; }
  .hl { background: #fee2e2; color: #991b1b; font-weight: 700; padding: 1px 4px; border-radius: 4px; }
  .btn-main { background: #0b4f71; color: #ffffff; text-align: center; padding: 8px; border-radius: 8px; font-weight: 700; font-size: 12.5px; margin-bottom: 8px; }
  .presets { display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; }
  .pbtn { border: 1px solid #e2e8f0; background: #f8fafc; border-radius: 7px; padding: 5px; font-size: 10.5px; text-align: center; font-weight: 600; color: #334155; }
  .verdict { background: #fef2f2; border: 1px solid #fecaca; border-radius: 8px; padding: 9px; margin-bottom: 8px; }
  .verdict strong { color: #b91c1c; font-size: 12px; display: block; margin-bottom: 3px; }
  .verdict span { font-size: 11px; color: #991b1b; }
  .bubble-box { border: 1px solid #e2e8f0; background: #fafaf9; border-radius: 8px; padding: 8px; font-size: 11.5px; margin-bottom: 8px; }
  .chips { font-size: 11px; margin-bottom: 8px; color: #475569; }
  .chip { background: #fef3c7; color: #92400e; padding: 2px 6px; border-radius: 4px; font-weight: 700; margin-right: 4px; }
  .two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; font-size: 11px; line-height: 1.45; }
  .wa-card { background: #ffffff; border: 1px solid #cbd5e1; border-radius: 10px; padding: 10px 12px; margin-bottom: 10px; font-size: 11.8px; line-height: 1.45; }
  .badge-bad { margin-top: 7px; background: #fef2f2; border-radius: 7px; padding: 7px 9px; color: #991b1b; font-size: 11.2px; }
  .badge-good { margin-top: 7px; background: #f0fdf4; border-radius: 7px; padding: 7px 9px; color: #166534; font-size: 11.2px; }
</style>
</head>
<body>
  <div class="outer-title">Rancangan Antarmuka Web Cek Pesan Pajak (FastAPI) dan Ekstensi WhatsApp Web</div>
  <div class="layout">
    <div class="panel">
      <div class="panel-title">A. Antarmuka Web Cek Pesan Pajak (127.0.0.1:8000/)</div>
      <div class="nav-bar">
        <div class="brand">Cek Pesan Pajak</div>
        <div class="tabs">
          <span class="tab active">Cek Pesan</span>
          <span class="tab">Web Resmi &amp; Ciri Scam</span>
          <span class="tab danger">Darurat .apk</span>
        </div>
        <div class="pill-ok">Siap</div>
      </div>
      <div class="cols">
        <div class="card">
          <h3>1. Cek Chat WhatsApp</h3>
          <div class="ta">"Yth. Wajib Pajak, segera unduh dan instal <span class="hl">Pembaruan_Coretax_DJP.apk</span> untuk verifikasi NPWP agar terhindar dari denda..."</div>
          <div class="btn-main">Cek Sekarang</div>
          <div class="presets">
            <div class="pbtn">File .apk Palsu</div>
            <div class="pbtn">Link Pajak Palsu</div>
            <div class="pbtn">Chat Resmi DJP</div>
          </div>
        </div>
        <div class="card">
          <h3>2. Vonis, Sorotan Fokus &amp; Solusi</h3>
          <div class="verdict">
            <strong>BAHAYA / SCAM (Scam 92%) — Jangan Klik atau Download!</strong>
            <span>Ada file .apk berbahaya. DJP tidak pernah kirim aplikasi lewat WA.</span>
          </div>
          <div class="bubble-box">Sorot fokus hanya pada <span class="hl">Pembaruan_Coretax_DJP.apk</span> &amp; link eksternal</div>
          <div class="chips">Kata pemicu: <span class="chip">segera</span><span class="chip">unduh</span><span class="chip">instal</span><span class="chip">verifikasi</span></div>
          <div class="two-col">
            <div><strong>Kenapa?</strong><br/>&bull; File .apk pencuri OTP<br/>&bull; Nada memaksa / ancam</div>
            <div><strong>Solusi</strong><br/>&bull; Jangan install .apk<br/>&bull; Copy Alert / Share WA</div>
          </div>
        </div>
      </div>
    </div>
    <div class="panel panel-alt">
      <div class="panel-title">B. Ekstensi WhatsApp Web (Manifest V3)</div>
      <div class="wa-card">
        <strong>Pesan Masuk (+62 857-xxxx):</strong><br/>
        Segera login melalui https://djp-coretax-verifikasi.xyz/login sebelum 17.00 WIB.
        <div class="badge-bad"><strong>Jangan Klik atau Download! (Scam 84%)</strong><br/>Link luar DJP: djp-coretax-verifikasi.xyz</div>
      </div>
      <div class="wa-card">
        <strong>Pesan Masuk (Info Pajak Resmi):</strong><br/>
        Lapor SPT Tahunan melalui laman resmi https://djponline.pajak.go.id atau 1500200.
        <div class="badge-good"><strong>Pola Chat Resmi / Normal (Aman 90%)</strong><br/>Link resmi: djponline.pajak.go.id</div>
      </div>
      <div class="wa-card" style="margin-bottom:0;">
        <strong>Info Akademik &amp; Evaluasi di Footer:</strong><br/>
        Tersedia tautan khusus demo sidang di footer untuk menampilkan tabel evaluasi komparasi model tanpa membebani pengguna awam.
      </div>
    </div>
  </div>
</body>
</html>
"""


def generate_methodology_and_ui_diagrams() -> None:
    """Hasilkan ulang Gambar 1.1, Gambar 2.1, dan Gambar L.1 agar sinkron dengan data final."""
    steps_1_1 = (
        ("1. Pengumpulan Data Publik", "Korpus Dasar SMS (904 baris) & Korpus Pajak Seimbang (260 baris; 65 dari 68 sumber)"),
        ("2. Praproses Teks Indonesia", "Pembersihan, Case Folding, Tokenisasi (token_apk & token_url), Stopword & Stemming Sastrawi"),
        ("3. Pembobotan Fitur TF-IDF", "Deduplikasi 1.159 teks unik, fitur n-gram (1, 2) maks. 3.000 & Stratified Split 80:20 (927 : 232)"),
        ("4. Pelatihan & Komparasi", "Support Vector Machine (LinearSVC C=2,0) & Random Forest (100 pohon) via GridSearchCV"),
        ("5. Evaluasi Kinerja Sistem", "Confusion Matrix, ROC/PR-AUC, Kalibrasi Platt, Uji Ablasi, & Kontrol vs Bias Pajak (n=45)"),
        ("6. Integrasi Purwarupa (TKT 6)", "REST API & Web Cek Pesan Pajak (FastAPI) serta Ekstensi WhatsApp Web Berpenjelasan Awam"),
    )
    steps_2_1 = (
        ("1. Kurasi & Integrasi Korpus", "Kurasi 260 teks pajak seimbang (130 phishing, 130 resmi; 65/68 sumber) + 904 SMS umum menjadi korpus induk (1.164 -> 1.159 unik) & diperluas (2.519 unik)"),
        ("2. Praproses & Token Entitas", "Case folding, penyandian token_apk dan token_url, penghapusan simbol, stopword removal, serta stemming Confix-Stripping Sastrawi"),
        ("3. Ekstraksi TF-IDF & Split Data", "Pembobotan matriks sparse TF-IDF n-gram (1, 2) maks. 3.000 fitur pada pembagian Stratified Split 80:20 (927 data latih : 232 data uji)"),
        ("4. Penalaan & Kalibrasi Platt", "GridSearchCV 36 kandidat pada Stratified 10-Fold CV (LinearSVC C=2,0 vs Random Forest 100 pohon) & kalibrasi Platt Scaling (5-fold sigmoid)"),
        ("5. Evaluasi & Uji Lintas-Korpus", "Uji Confusion Matrix, ROC/PR-AUC, Brier Score, 6 uji ablatif, kontrol vs bias pajak (n=45), serta zero-shot eksternal (1.360 baris unik)"),
        ("6. Ekspor Model & Purwarupa", "Serialisasi bundel .joblib ke purwarupa TKT 6: REST API & Web Cek Pesan Pajak (FastAPI) serta Ekstensi WhatsApp Web"),
    )
    targets = (
        (ASSET_DIR / "Gambar 1.1 Tahapan Metode Penelitian.png", _build_six_step_diagram_html(steps_1_1), 1340, 560),
        (ASSET_DIR / "Gambar 2.1 Bagan Alir Prosedur Eksperimen.png", _build_six_step_diagram_html(steps_2_1), 1340, 590),
        (ASSET_DIR / "Gambar L.1 Rancangan Antarmuka Purwarupa dan Ekstensi.png", _build_ui_wireframe_html(), 1440, 620),
    )
    for out_png, html_body, w, h in targets:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".html", encoding="utf-8", delete=False) as tmp:
            tmp.write(html_body)
            tmp_path = Path(tmp.name)
        try:
            _capture_html_png(tmp_path, out_png, width=w, height=h)
        finally:
            tmp_path.unlink(missing_ok=True)


def generate_prototype_screenshots(
    presets_out: dict[str, Any],
    latency_info: dict[str, Any],
    include_methodology_diagrams: bool = False,
) -> None:
    """Perbarui tangkapan layar purwarupa Bab IV tanpa menimpa diagram Bab I-III atau simulasi_whatsapp_web.html."""
    EXT_DIR.mkdir(parents=True, exist_ok=True)
    sim_html_path = EXT_DIR / "simulasi_whatsapp_web.html"
    if not sim_html_path.exists():
        sim_html_path.write_text(
            _build_whatsapp_simulation_html(presets_out), encoding="utf-8"
        )

    stale_names = (
        "Gambar 3.2 Rancangan Antarmuka Purwarupa dan Ekstensi.png",
        "Gambar 4.2 Evaluasi Diskriminatif Kurva ROC dan Precision-Recall.png",
        "Gambar 4.3 Evaluasi Kalibrasi Probabilitas Model.png",
        "Gambar 4.3 Komparasi Generalisasi Lintas Korpus dan Subset Pajak.png",
        "Gambar 4.4 Analisis Interpretabilitas Fitur TF-IDF Terbaik.png",
        "Gambar 4.4 Analisis Interpretabilitas Model Berbasis SHAP.png",
        "Gambar 4.5 Komparasi Generalisasi Lintas Korpus dan Subset Pajak.png",
        "Gambar 4.5 Tangkapan Layar Antarmuka Web Cek Pesan Pajak dan Respons API.png",
        "Gambar 4.6 Tangkapan Layar Antarmuka Dashboard Streamlit dan Respons API.png",
        "Gambar 4.6 Tangkapan Layar Antarmuka Web Cek Pesan Pajak dan Respons API.png",
        "Gambar 4.6 Tangkapan Layar Ekstensi Chrome pada Simulasi WhatsApp Web.png",
        "Gambar 4.7 Tangkapan Layar Ekstensi Chrome pada Simulasi WhatsApp Web.png",
        "Gambar 4.8 Analisis Interpretabilitas Model Berbasis SHAP.png",
    )
    for old_name in stale_names:
        old_path = ASSET_DIR / old_name
        if old_path.exists():
            old_path.unlink()

    web_png = (
        ASSET_DIR
        / "Gambar 4.3 Tangkapan Layar Antarmuka Web Cek Pesan Pajak dan Respons API.png"
    )
    ext_png = (
        ASSET_DIR
        / "Gambar L.6 Tangkapan Layar Ekstensi Chrome pada Simulasi WhatsApp Web.png"
    )

    if include_methodology_diagrams:
        generate_methodology_and_ui_diagrams()
        arch_png = ASSET_DIR / "Gambar 3.1 Arsitektur Sistem Terpadu.png"
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".html", encoding="utf-8", delete=False
        ) as tmp_arch:
            tmp_arch.write(_build_architecture_diagram_html())
            tmp_arch_html = Path(tmp_arch.name)
        try:
            _capture_html_png(tmp_arch_html, arch_png, width=1500, height=790)
        finally:
            tmp_arch_html.unlink(missing_ok=True)

    copy_evaluation_figures()

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".html", encoding="utf-8", delete=False
    ) as tmp:
        tmp.write(_build_web_api_html(presets_out, latency_info))
        tmp_html = Path(tmp.name)

    try:
        _capture_html_png(tmp_html, web_png, width=1360, height=900)
    finally:
        tmp_html.unlink(missing_ok=True)

    _capture_html_png(sim_html_path, ext_png, width=1440, height=870)


def refresh_screenshots_only() -> None:
    """Render ulang Gambar 4.3 & L.6 dari benchmark_latensi_purwarupa.json tersimpan."""
    json_path = EVAL_DIR / "json" / "benchmark_latensi_purwarupa.json"
    saved = json.loads(json_path.read_text(encoding="utf-8"))
    latency_info = saved["latency_benchmark"]
    presets_out = saved["preset_verification"]
    generate_prototype_screenshots(presets_out, latency_info, include_methodology_diagrams=False)


def main() -> None:
    parser = argparse.ArgumentParser(description="Benchmark & tangkapan layar purwarupa TKT 6.")
    parser.add_argument(
        "--screenshots-only",
        action="store_true",
        help="Render ulang tangkapan layar Gambar 4.3 & L.6 tanpa menimpa JSON/CSV benchmark.",
    )
    args = parser.parse_args()
    if args.screenshots_only:
        refresh_screenshots_only()
        print("Gambar 4.3 dan L.6 berhasil dirender ulang dari JSON tersimpan.")
        return
    (EVAL_DIR / "json").mkdir(parents=True, exist_ok=True)
    (EVAL_DIR / "csv").mkdir(parents=True, exist_ok=True)
    latency_info, presets_out = measure_latency()
    pytest_info = run_pytest_verification()

    full_json = {
        "pytest_verification": pytest_info,
        "latency_benchmark": latency_info,
        "preset_verification": presets_out,
    }
    json_path = EVAL_DIR / "json" / "benchmark_latensi_purwarupa.json"
    json_path.write_text(
        json.dumps(full_json, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    csv_path = EVAL_DIR / "csv" / "tabel_pengujian_purwarupa.csv"
    save_test_summary_csv(pytest_info, latency_info, csv_path)

    generate_prototype_screenshots(presets_out, latency_info)

    direct = latency_info["direct_inference_holdout_232"]
    api = latency_info["fastapi_post_predict_holdout_232"]
    batch = latency_info["fastapi_post_predict_batch_50"]
    print(
        f"Pytest: {pytest_info['passed']}/{pytest_info['total_collected']} PASSED "
        f"({pytest_info['pytest_reported_seconds']}s)"
    )
    print(
        f"Latensi inference.py (n={direct['n_calls']}): mean={direct['mean_ms']} ms, "
        f"p50={direct['median_p50_ms']} ms, p95={direct['p95_ms']} ms, p99={direct['p99_ms']} ms"
    )
    print(
        f"Latensi POST /predict (n={api['n_calls']}): mean={api['mean_ms']} ms, "
        f"p50={api['median_p50_ms']} ms, p95={api['p95_ms']} ms, p99={api['p99_ms']} ms"
    )
    print(
        f"Latensi POST /predict/batch (n=50): total={batch['total_ms']} ms, "
        f"avg={batch['avg_per_message_ms']} ms/pesan"
    )
    print("Aset gambar Bab IV dan simulasi_whatsapp_web.html selesai dibuat.")


if __name__ == "__main__":
    main()
