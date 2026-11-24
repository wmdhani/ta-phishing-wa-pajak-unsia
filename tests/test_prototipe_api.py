from __future__ import annotations

import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

ROOT_DIR = Path(__file__).resolve().parent.parent
PROTOTYPE_DIR = ROOT_DIR / "app" / "backend"
if str(PROTOTYPE_DIR) not in sys.path:
    sys.path.insert(0, str(PROTOTYPE_DIR))

import api as api_module
import inference as inference_module
from api import app
from inference import analyze_urls_and_apk, is_official_djp_domain

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
                "   ",
                "Lapor SPT melalui https://djponline.pajak.go.id",
            ]
        },
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 3
    assert len(data["results"]) == 3
    assert "error" in data["results"][1]

    oversized_resp = client.post("/predict/batch", json={"texts": ["a" * 5001]})
    assert oversized_resp.status_code == 422


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
    assert acad_payload["thesis"]["advisor"] == "Bapak Novi Dian Nathasia, S.Kom., M.M.S.I."
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


def test_predict_apk_url_flags_apk_and_suspicious_domain() -> None:
    apk_url = "https://pajak-coretax-resmi.xyz/files/Coretax_Update.apk"
    resp = client.post(
        "/predict",
        json={"text": f"Yth Wajib Pajak segera unduh {apk_url} sekarang juga."},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["label"] == 1
    assert data["risk_level"] == "TINGGI"
    assert data["has_apk"] is True
    assert "Coretax_Update.apk" in data["apk_matches"]
    assert "pajak-coretax-resmi.xyz" in data["suspicious_domains"]
    assert apk_url in data["urls_found"]
    assert any(h["kind"] == "apk" and h["text"] == apk_url for h in data["highlights"])
    assert analyze_urls_and_apk("Unduh Coretax_DJP.apk segera")["suspicious_domains"] == []


def test_security_csp_headers() -> None:
    expected_directives = (
        "default-src 'self'",
        "script-src 'self'",
        "object-src 'none'",
        "frame-ancestors 'self'",
        "base-uri 'self'",
    )
    for path in ("/", "/health", "/simulasi-wa"):
        resp = client.get(path)
        assert resp.status_code == 200
        csp = resp.headers.get("content-security-policy", "")
        for directive in expected_directives:
            assert directive in csp
        assert "geolocation=()" in resp.headers.get("permissions-policy", "")


def test_cors_strict_allowlist_and_private_network() -> None:
    wa_preflight = client.options(
        "/predict",
        headers={
            "Origin": "https://web.whatsapp.com",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Private-Network": "true",
        },
    )
    assert wa_preflight.status_code == 200
    assert wa_preflight.headers.get("access-control-allow-origin") == "https://web.whatsapp.com"
    assert wa_preflight.headers.get("access-control-allow-private-network") == "true"

    ext_origin = "chrome-extension://aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    ext_preflight = client.options(
        "/predict",
        headers={
            "Origin": ext_origin,
            "Access-Control-Request-Method": "POST",
        },
    )
    assert ext_preflight.status_code == 200
    assert ext_preflight.headers.get("access-control-allow-origin") == ext_origin

    for blocked_origin in (
        "https://evil-phishing.example.com",
        "chrome-extension://invalid-short",
    ):
        blocked = client.options(
            "/predict",
            headers={
                "Origin": blocked_origin,
                "Access-Control-Request-Method": "POST",
            },
        )
        assert blocked.headers.get("access-control-allow-origin") is None


def test_batch_weighted_rate_limit_char_cap_and_probability_parity(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    samples = [
        (
            "Pemberitahuan resmi pajak: segera verifikasi di "
            "https://djp-coretax-verifikasi.xyz/login sebelum akun diblokir."
        ),
        (
            "Direktorat Jenderal Pajak mengimbau Wajib Pajak lapor SPT melalui "
            "https://djponline.pajak.go.id atau Kring Pajak 1500200."
        ),
    ]
    single_results = [
        client.post("/predict", json={"text": text, "top_k": 5}).json() for text in samples
    ]
    batch_resp = client.post("/predict/batch", json={"texts": samples, "top_k": 5})
    assert batch_resp.status_code == 200
    batch_results = batch_resp.json()["results"]
    for single_item, batch_item in zip(single_results, batch_results, strict=True):
        assert batch_item["svm_probability"] == single_item["svm_probability"]
        assert batch_item["rf_probability"] == single_item["rf_probability"]
        assert batch_item["label"] == single_item["label"]
        assert batch_item["risk_level"] == single_item["risk_level"]

    oversized_total = client.post("/predict/batch", json={"texts": ["a" * 5000] * 21})
    assert oversized_total.status_code == 422

    test_ip = "198.51.100.42"
    api_module._RATE_BUCKETS.pop(test_ip, None)
    monkeypatch.setattr(api_module, "_resolve_client_ip", lambda _request: test_ip)
    monkeypatch.setenv("RATE_LIMIT_PER_MIN", "3")
    try:
        first = client.post("/predict", json={"text": "Cek status pajak resmi"})
        assert first.status_code == 200

        weighted_batch = client.post(
            "/predict/batch",
            json={"texts": [f"Pesan pajak nomor {i}" for i in range(30)]},
        )
        assert weighted_batch.status_code == 429
        assert int(weighted_batch.headers["retry-after"]) >= 1
        assert "default-src 'self'" in weighted_batch.headers.get("content-security-policy", "")

        third = client.post("/predict", json={"text": "Cek status pajak resmi"})
        assert third.status_code == 200

        fourth = client.post("/predict", json={"text": "Cek status pajak resmi"})
        assert fourth.status_code == 429
        assert int(fourth.headers["retry-after"]) >= 1
        assert "default-src 'self'" in fourth.headers.get("content-security-policy", "")
    finally:
        api_module._RATE_BUCKETS.pop(test_ip, None)


def test_missing_model_returns_503_without_path_leak(monkeypatch: pytest.MonkeyPatch) -> None:
    def _missing_bundle(*_args: object, **_kwargs: object) -> dict[str, object]:
        raise FileNotFoundError(
            "Berkas model tidak ditemukan: /internal/secret/model_phishing_pajak.joblib"
        )

    monkeypatch.setattr(api_module, "load_model_bundle", _missing_bundle)
    monkeypatch.setattr(inference_module, "load_model_bundle", _missing_bundle)

    responses = [
        client.get("/health"),
        client.post("/predict", json={"text": "Cek pesan pajak resmi"}),
        client.post("/predict/batch", json={"texts": ["Cek pesan pajak resmi"]}),
    ]
    for resp in responses:
        assert resp.status_code == 503
        assert resp.json()["detail"] == "Model klasifikasi sedang tidak tersedia."
        assert "/internal/secret" not in resp.text
        assert "model_phishing_pajak.joblib" not in resp.text

    acad = client.get("/api/academic-summary")
    assert acad.status_code == 200
    assert acad.json()["metadata"] == {}


def test_academic_summary_latency_benchmark() -> None:
    resp = client.get("/api/academic-summary")
    assert resp.status_code == 200
    bench = resp.json()["latency_benchmark"]
    for key in ("direct_p50_ms", "api_p50_ms", "api_mean_ms", "batch_avg_ms"):
        assert key in bench
        assert isinstance(bench[key], float)
        assert bench[key] > 0
