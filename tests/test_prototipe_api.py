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
    assert len(data["top_triggers"]) > 0


def test_predict_phishing_fake_domain() -> None:
    resp = client.post(
        "/predict",
        json={
            "text": (
                "Pemberitahuan resmi pajak: segera klaim pengembalian dana melalui "
                "https://pajak-djp-verifikasi.xyz/login sebelum hari ini berakhir."
            )
        },
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["label"] == 1
    assert "pajak-djp-verifikasi.xyz" in data["suspicious_domains"]
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
    assert "djponline.pajak.go.id" in data["official_domains"]
    assert data["suspicious_domains"] == []


def test_official_domain_spoof_guard() -> None:
    assert is_official_djp_domain("pajak.go.id") is True
    assert is_official_djp_domain("djponline.pajak.go.id") is True
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
