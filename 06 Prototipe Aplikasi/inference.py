from __future__ import annotations

import functools
import re
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import joblib
import numpy as np

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.eksperimen_baseline import clean_text

MODEL_PATH = Path(__file__).resolve().parent / "model_phishing_pajak.joblib"
APK_PATTERN = re.compile(r"\b[a-z0-9_.-]+\.apk\b", re.IGNORECASE)
URL_PATTERN = re.compile(
    r"(?:https?://|www\.)[^\s<>\"']+|(?<!@)\b[a-z0-9-]+(?:\.[a-z0-9-]+)+\b(?:/[^\s<>\"']*)?",
    re.IGNORECASE,
)


@functools.lru_cache(maxsize=1)
def load_model_bundle(model_path: str | Path = MODEL_PATH) -> dict[str, Any]:
    """Load the serialized TF-IDF + SVM + Random Forest model bundle."""
    path = Path(model_path)
    if not path.exists():
        raise FileNotFoundError(f"Berkas model tidak ditemukan: {path}")
    return joblib.load(path)


def _extract_domain(raw_url: str) -> str:
    candidate = raw_url.strip().rstrip(".,;:!?)")
    if not candidate.lower().startswith(("http://", "https://")):
        candidate = f"https://{candidate}"
    parsed = urlparse(candidate)
    host = (parsed.hostname or "").lower().strip(".")
    return host


def is_official_djp_domain(domain: str) -> bool:
    """Return True only for exact pajak.go.id or its subdomains."""
    clean = domain.lower().strip(".")
    return clean == "pajak.go.id" or clean.endswith(".pajak.go.id")


def analyze_urls_and_apk(raw_text: str) -> dict[str, Any]:
    """Inspect raw message text for .apk attachments and official vs suspicious domains."""
    apk_matches = sorted(set(APK_PATTERN.findall(raw_text)))
    raw_urls = URL_PATTERN.findall(raw_text)

    urls_found: list[str] = []
    official_domains: list[str] = []
    suspicious_domains: list[str] = []

    for item in raw_urls:
        cleaned = item.strip().rstrip(".,;:!?)")
        if cleaned.lower().endswith(".apk"):
            continue
        domain = _extract_domain(cleaned)
        if not domain or "." not in domain:
            continue
        if cleaned not in urls_found:
            urls_found.append(cleaned)
        if is_official_djp_domain(domain):
            if domain not in official_domains:
                official_domains.append(domain)
        elif domain not in suspicious_domains:
            suspicious_domains.append(domain)

    return {
        "has_apk": len(apk_matches) > 0,
        "apk_matches": apk_matches,
        "urls_found": urls_found,
        "official_domains": official_domains,
        "suspicious_domains": suspicious_domains,
    }


def _extract_top_triggers(
    tfidf_row: Any,
    feature_names: np.ndarray,
    svm_coefs: np.ndarray,
    top_k: int = 8,
) -> list[dict[str, Any]]:
    """Compute per-token LinearSVC contributions (TF-IDF weight * coefficient)."""
    indices = tfidf_row.nonzero()[1]
    if len(indices) == 0:
        return []

    contributions: list[tuple[str, float, float]] = []
    for idx in indices:
        tfidf_val = float(tfidf_row[0, idx])
        coef_val = float(svm_coefs[idx])
        score = tfidf_val * coef_val
        contributions.append((str(feature_names[idx]), round(score, 4), round(coef_val, 4)))

    contributions.sort(key=lambda item: abs(item[1]), reverse=True)
    return [
        {
            "token": token,
            "contribution": score,
            "svm_coef": coef,
            "direction": "phishing" if score > 0 else "resmi",
        }
        for token, score, coef in contributions[:top_k]
    ]


def _build_recommendation(
    label: int,
    has_apk: bool,
    suspicious_domains: list[str],
    official_domains: list[str],
) -> str:
    if has_apk:
        return (
            "BAHAYA: Pesan mengandung pola berkas .apk. Direktorat Jenderal Pajak tidak "
            "pernah mengirimkan file aplikasi (.apk) melalui WhatsApp. Jangan unduh atau pasang berkas."
        )
    if label == 1 or suspicious_domains:
        return (
            "WASPADA PHISHING: Pesan terindikasi penipuan atau memuat tautan di luar domain resmi "
            "pajak.go.id. Verifikasi melalui Kring Pajak 1500200 atau laman resmi djponline.pajak.go.id."
        )
    if official_domains:
        return (
            "AMAN: Pesan terklasifikasi normal/resmi dan hanya merujuk pada domain resmi pajak.go.id."
        )
    return "AMAN: Pesan tidak menunjukkan indikator phishing perpajakan, tetap jaga kerahasiaan data."


def predict_message(
    raw_text: str,
    model_path: str | Path = MODEL_PATH,
    top_k: int = 8,
) -> dict[str, Any]:
    """Run full preprocessing, SVM Platt + RF inference, heuristic checks, and XAI."""
    text = raw_text.strip()
    if not text:
        raise ValueError("Teks pesan tidak boleh kosong.")

    bundle = load_model_bundle(model_path)
    vectorizer = bundle["vectorizer"]
    svm_linear = bundle["svm_linear"]
    svm_calibrated = bundle["svm_calibrated"]
    random_forest = bundle["random_forest"]

    cleaned = clean_text(text)
    features = vectorizer.transform([cleaned])

    svm_prob = float(svm_calibrated.predict_proba(features)[0, 1])
    rf_prob = float(random_forest.predict_proba(features)[0, 1])
    label = int(svm_prob >= 0.5)

    heuristics = analyze_urls_and_apk(text)
    if heuristics["has_apk"] and svm_prob < 0.75:
        risk_level = "TINGGI"
        label = 1
    elif svm_prob >= 0.75:
        risk_level = "TINGGI"
    elif svm_prob >= 0.50 or heuristics["suspicious_domains"]:
        risk_level = "SEDANG"
    else:
        risk_level = "RENDAH"

    triggers = _extract_top_triggers(
        features,
        vectorizer.get_feature_names_out(),
        svm_linear.coef_.ravel(),
        top_k=top_k,
    )

    return {
        "label": label,
        "label_text": "Phishing / Penipuan" if label == 1 else "Normal / Resmi",
        "risk_level": risk_level,
        "svm_probability": round(svm_prob, 4),
        "rf_probability": round(rf_prob, 4),
        "cleaned_text": cleaned,
        "has_apk": heuristics["has_apk"],
        "apk_matches": heuristics["apk_matches"],
        "urls_found": heuristics["urls_found"],
        "official_domains": heuristics["official_domains"],
        "suspicious_domains": heuristics["suspicious_domains"],
        "top_triggers": triggers,
        "recommendation": _build_recommendation(
            label=label,
            has_apk=heuristics["has_apk"],
            suspicious_domains=heuristics["suspicious_domains"],
            official_domains=heuristics["official_domains"],
        ),
    }
