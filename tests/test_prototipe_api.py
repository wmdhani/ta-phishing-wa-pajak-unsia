from __future__ import annotations

import sys
from pathlib import Path

from fastapi.testclient import TestClient

ROOT_DIR = Path(__file__).resolve().parent.parent
PROTOTYPE_DIR = ROOT_DIR / "06 Prototipe Aplikasi"
if str(PROTOTYPE_DIR) not in sys.path:
    sys.path.insert(0, str(PROTOTYPE_DIR))

from api import app
from inference import is_official_djp_domain

client = TestClient(app)


def test_health_endpoint() -> None:
    resp = client.get("/health")
    assert resp.status_code == 200
    payload = resp.json()
    assert payload["status"] == "ok"
    assert "LinearSVC+Platt" in payload["models_loaded"]


def test_predict_phishing_apk() -> None:
    resp = client.post(
        "/predict",
        json={
            "text": (
                "Yth Wajib Pajak segera unduh Coretax_DJP_Update.apk untuk verifikasi "
                "NPWP Anda agar terhindar dari blokir rekening."
            )
        },
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["label"] == 1
    assert data["has_apk"] is True
    assert "Coretax_DJP_Update.apk" in data["apk_matches"]
    assert data["risk_level"] == "TINGGI"
    assert isinstance(data["inference_ms"], float)
    assert data["inference_ms"] >= 0.0
    assert len(data["top_triggers"]) > 0
    assert len(data["plain_reasons"]) > 0
    assert len(data["trigger_words"]) > 0
    assert any(h["kind"] == "apk" for h in data["highlights"])
    assert all(h["kind"] in {"apk", "official_url", "suspicious_url"} for h in data["highlights"])


def test_predict_phishing_fake_domain() -> None:
    resp = client.post(
        "/predict",
        json={
            "text": (
                "Pemberitahuan resmi pajak: segera klaim pengembalian dana melalui "
                "https://pajak-djp-verifikasi.xyz/login sebelum pukul 17.00 WIB."
            )
        },
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["label"] == 1
    assert "pajak-djp-verifikasi.xyz" in data["suspicious_domains"]
    assert "17.00" not in data["suspicious_domains"]
    assert data["official_domains"] == []


def test_predict_official_djp_message() -> None:
    resp = client.post(
        "/predict",
        json={
            "text": (
                "Direktorat Jenderal Pajak mengimbau Wajib Pajak melaporkan SPT Tahunan "
                "melalui laman resmi https://djponline.pajak.go.id atau Kring Pajak 1500200."
            )
        },
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["label"] == 0
    assert data["risk_level"] == "RENDAH"
    assert "djponline.pajak.go.id" in data["official_domains"]
    assert data["suspicious_domains"] == []
    assert any(h["kind"] == "official_url" for h in data["highlights"])


def test_numeric_time_and_amount_not_flagged_as_domain() -> None:
    resp = client.post(
        "/predict",
        json={
            "text": (
                "Pelayanan tatap muka KPP dibuka sampai pukul 16.00 WIB dengan batas "
                "pembayaran Rp1.500.000 melalui kanal resmi pajak.go.id."
            )
        },
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["suspicious_domains"] == []
    assert "pajak.go.id" in data["official_domains"]
    assert data["risk_level"] == "RENDAH"


def test_official_domain_spoof_guard() -> None:
    assert is_official_djp_domain("pajak.go.id") is True
    assert is_official_djp_domain("djponline.pajak.go.id") is True
    assert is_official_djp_domain("coretaxdjp.pajak.go.id") is True
    assert is_official_djp_domain("pajak.go.id.evil.com") is False
    assert is_official_djp_domain("coretax-pajak.xyz") is False


def test_predict_empty_text_rejected() -> None:
    resp = client.post("/predict", json={"text": "   "})
    assert resp.status_code == 422


def test_predict_batch_endpoint() -> None:
    resp = client.post(
        "/predict/batch",
        json={
            "texts": [
                "Segera instal pajak_update.apk sekarang",
                "Lapor SPT melalui https://djponline.pajak.go.id",
            ]
        },
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 2
    assert len(data["results"]) == 2


def test_web_ui_and_supporting_endpoints() -> None:
    home = client.get("/")
    assert home.status_code == 200
    assert "Cek Pesan Pajak" in home.text
    assert home.headers.get("x-content-type-options") == "nosniff"
    assert home.headers.get("x-frame-options") == "SAMEORIGIN"
    assert home.headers.get("referrer-policy") == "strict-origin-when-cross-origin"

    sim = client.get("/simulasi-wa")
    assert sim.status_code == 200
    assert "Simulasi WhatsApp Web" in sim.text

    presets = client.get("/api/presets")
    assert presets.status_code == 200
    assert len(presets.json()["presets"]) == 3

    academic = client.get("/api/academic-summary")
    assert academic.status_code == 200
    acad_payload = academic.json()
    assert "Wan Mirza Dhani" in acad_payload["thesis"]["author"]
    assert acad_payload["thesis"]["advisor"] == "Bapak Novi Dian Nathasia, S.Kom., MMSI"
    assert acad_payload["thesis"]["scheme"] == "Tugas Akhir Prototype (TKT Level 6)"
    assert len(acad_payload["evaluation_rows"]) > 0

    preflight = client.options(
        "/predict",
        headers={
            "Origin": "https://web.whatsapp.com",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Private-Network": "true",
        },
    )
    assert preflight.status_code == 200
    assert preflight.headers.get("access-control-allow-private-network") == "true"


def test_security_headers_and_rate_limiter_helper() -> None:
    import api as api_module

    ip = "203.0.113.99"
    api_module._RATE_BUCKETS.pop(ip, None)
    assert api_module._is_rate_limited(ip, 2) is False
    assert api_module._is_rate_limited(ip, 2) is False
    assert api_module._is_rate_limited(ip, 2) is True
    assert api_module._is_rate_limited("testclient", 1) is False
    api_module._RATE_BUCKETS.pop(ip, None)
