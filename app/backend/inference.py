from __future__ import annotations

import functools
import re
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import joblib
import numpy as np
from sklearn.pipeline import Pipeline

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from ml.eksperimen_baseline import STEM_WORD, clean_text

MODEL_PATH = Path(__file__).resolve().parent / "model_phishing_pajak.joblib"
APK_PATTERN = re.compile(r"\b[a-z0-9_.-]+\.apk\b", re.IGNORECASE)

_BARE_TLD_LIST = (
    "go\\.id|co\\.id|my\\.id|or\\.id|ac\\.id|sch\\.id|web\\.id|biz\\.id|net\\.id|"
    "id|com|net|org|info|biz|xyz|top|site|online|website|store|shop|app|dev|link|"
    "click|live|vip|icu|club|fun|me|cc|tv|io|co|ly|gl|gg|to|us|uk|sg|my|ru|cn|"
    "tk|ml|ga|cf|gq|pro|tech|cloud|space|asia|edu|gov|mil|win|loan|work|press|"
    "host|uno|cfd|sbs|cyou|monster|quest|rest|bar|buzz|surf|digital|portal|"
    "support|services|center"
)
URL_PATTERN = re.compile(
    rf"(?:https?://|www\.)[^\s<>\"']+|(?<!@)\b(?:[a-z0-9-]+\.)+(?:{_BARE_TLD_LIST})\b(?:/[^\s<>\"']*)?",
    re.IGNORECASE,
)

PRESETS: dict[str, str] = {
    "Phishing APK (Coretax Palsu)": (
        "Yth. Wajib Pajak, segera unduh dan instal berkas Pembaruan_Coretax_DJP.apk "
        "untuk verifikasi NPWP agar terhindar dari denda administratif."
    ),
    "Phishing Domain Palsu": (
        "Pemberitahuan resmi Direktorat Jenderal Pajak: terdapat selisih SPT Tahunan Anda. "
        "Segera login melalui https://djp-coretax-verifikasi.xyz/login sebelum pukul 17.00 WIB."
    ),
    "Pengumuman Resmi DJP": (
        "Direktorat Jenderal Pajak mengimbau Wajib Pajak melaporkan SPT Tahunan tepat waktu "
        "melalui laman resmi https://djponline.pajak.go.id atau hubungi Kring Pajak 1500200."
    ),
}

PRESET_CATALOG: list[dict[str, str]] = [
    {
        "id": "apk",
        "key": "Phishing APK (Coretax Palsu)",
        "label": "File .apk Palsu",
        "tag": "Scam",
        "tone": "danger",
        "text": PRESETS["Phishing APK (Coretax Palsu)"],
    },
    {
        "id": "domain",
        "key": "Phishing Domain Palsu",
        "label": "Link Pajak Palsu",
        "tag": "Scam",
        "tone": "danger",
        "text": PRESETS["Phishing Domain Palsu"],
    },
    {
        "id": "official",
        "key": "Pengumuman Resmi DJP",
        "label": "Chat Resmi DJP",
        "tag": "Aman",
        "tone": "safe",
        "text": PRESETS["Pengumuman Resmi DJP"],
    },
]

_URGENCY_STEMS = frozenset(
    {
        "segera",
        "cepat",
        "batas",
        "akhir",
        "hari",
        "jam",
        "langsung",
        "kedaluwarsa",
        "kadaluarsa",
        "hangus",
        "tenggat",
        "terakhir",
    }
)
_THREAT_STEMS = frozenset(
    {
        "denda",
        "blokir",
        "sanksi",
        "hukum",
        "pidana",
        "beku",
        "tutup",
        "selisih",
        "tagih",
        "tunggak",
        "batal",
        "cabut",
        "periksa",
        "sit",
        "sita",
    }
)
_ACTION_BAIT_STEMS = frozenset(
    {
        "unduh",
        "instal",
        "install",
        "download",
        "klik",
        "verifikasi",
        "mutakhir",
        "perbarui",
        "baru",
        "update",
        "aktivasi",
        "login",
        "masuk",
        "klaim",
        "hadiah",
        "menang",
        "transfer",
        "kirim",
        "rekening",
        "pin",
        "otp",
        "efin",
        "kode",
        "daftar",
        "isi",
        "buka",
    }
)
_NEUTRAL_TAX_STEMS = frozenset(
    {
        "pajak",
        "wajib",
        "npwp",
        "spt",
        "tahun",
        "djp",
        "direktorat",
        "jenderal",
        "lapor",
        "nik",
        "coretax",
        "layan",
        "resmi",
        "informasi",
        "imbau",
        "kantor",
        "kring",
        "yth",
        "hormat",
        "hindar",
        "berkas",
        "agar",
        "untuk",
        "mohon",
        "kepada",
        "bapak",
        "ibu",
        "saudara",
        "dengan",
        "berikut",
        "melalui",
        "atas",
        "terima",
        "kasih",
        "administratif",
        "administrasi",
        "anda",
    }
)


_TRAILING_URL_PUNCT = ".,;:!?)\"'>]"


@functools.lru_cache(maxsize=4)
def load_model_bundle(model_path: str | Path = MODEL_PATH) -> dict[str, Any]:
    """Load the serialized TF-IDF + SVM + Random Forest model bundle and cache derivatives."""
    path = Path(model_path)
    if not path.exists():
        raise FileNotFoundError(f"Berkas model tidak ditemukan: {path}")
    bundle = dict(joblib.load(path))
    bundle["feature_names"] = bundle["vectorizer"].get_feature_names_out()
    bundle["svm_coefs"] = bundle["svm_linear"].coef_.ravel()
    bundle["svm_is_pipeline"] = isinstance(
        getattr(bundle["svm_calibrated"], "estimator", None), Pipeline
    )
    return bundle


def _extract_domain(raw_url: str) -> str:
    candidate = raw_url.strip().rstrip(_TRAILING_URL_PUNCT)
    if not candidate.lower().startswith(("http://", "https://")):
        candidate = f"https://{candidate}"
    parsed = urlparse(candidate)
    return (parsed.hostname or "").lower().strip(".")


def is_official_djp_domain(domain: str) -> bool:
    """Return True only for exact pajak.go.id or its subdomains."""
    clean = domain.lower().strip(".")
    return clean == "pajak.go.id" or clean.endswith(".pajak.go.id")


def _is_url_with_context(cleaned_url: str) -> bool:
    lower = cleaned_url.lower()
    return lower.startswith(("http://", "https://", "www.")) or "/" in cleaned_url


def analyze_urls_and_apk(raw_text: str) -> dict[str, Any]:
    """Inspect raw message text for .apk attachments and official vs suspicious domains."""
    apk_spans = [(m.start(), m.end(), m.group(0)) for m in APK_PATTERN.finditer(raw_text)]
    apk_matches = sorted({text for _, _, text in apk_spans})

    urls_found: list[str] = []
    official_domains: list[str] = []
    suspicious_domains: list[str] = []

    for match in URL_PATTERN.finditer(raw_text):
        cleaned = match.group(0).strip().rstrip(_TRAILING_URL_PUNCT)
        end_pos = match.start() + len(cleaned)
        has_context = _is_url_with_context(cleaned)
        if not has_context and any(s <= match.start() and end_pos <= e for s, e, _ in apk_spans):
            continue
        if cleaned.lower().endswith(".apk") and not has_context:
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
        return "Jangan download/install file .apk ini. Hapus chat & block pengirimnya."
    if label == 1 or suspicious_domains:
        return "Jangan klik link atau kasih OTP/PIN. Cek resmi di pajak.go.id / 1500200."
    if official_domains:
        return "Link resmi pajak.go.id. Tetap jaga kerahasiaan OTP & password."
    return "Tidak ada tanda scam. Tetap jangan bagikan OTP/PIN lewat WA."


def _collect_trigger_stems(top_triggers: list[dict[str, Any]]) -> set[str]:
    stems: set[str] = set()
    for item in top_triggers:
        if item["direction"] != "phishing" or item["contribution"] <= 0:
            continue
        for part in str(item["token"]).split():
            if part in ("token_apk", "token_url") or part.isdigit() or len(part) <= 2:
                continue
            if part in _NEUTRAL_TAX_STEMS:
                continue
            stems.add(part)
    return stems


def _extract_highlights_and_triggers(
    raw_text: str,
    risk_level: str,
    trigger_stems: set[str],
) -> tuple[list[dict[str, Any]], list[str]]:
    """Highlight only .apk attachments and URLs in the chat bubble; extract cue words separately."""
    spans: list[tuple[int, int, str, str, str]] = []

    for match in URL_PATTERN.finditer(raw_text):
        trimmed = match.group(0).rstrip(_TRAILING_URL_PUNCT)
        if not trimmed or not trimmed.lower().endswith(".apk") or not _is_url_with_context(trimmed):
            continue
        end_pos = match.start() + len(trimmed)
        domain = _extract_domain(trimmed)
        domain_note = f" dari {domain}" if domain else ""
        spans.append(
            (
                match.start(),
                end_pos,
                trimmed,
                "apk",
                f"Tautan file .apk berbahaya{domain_note} (DJP tidak pernah kirim .apk lewat WA).",
            )
        )

    for match in APK_PATTERN.finditer(raw_text):
        if any(not (match.end() <= s or match.start() >= e) for s, e, *_ in spans):
            continue
        spans.append(
            (
                match.start(),
                match.end(),
                match.group(0),
                "apk",
                "File .apk berbahaya (DJP tidak pernah kirim .apk lewat WA).",
            )
        )

    for match in URL_PATTERN.finditer(raw_text):
        trimmed = match.group(0).rstrip(_TRAILING_URL_PUNCT)
        if not trimmed:
            continue
        has_context = _is_url_with_context(trimmed)
        if trimmed.lower().endswith(".apk") and not has_context:
            continue
        end_pos = match.start() + len(trimmed)
        if any(not (end_pos <= s or match.start() >= e) for s, e, *_ in spans):
            continue
        domain = _extract_domain(trimmed)
        if not domain or "." not in domain:
            continue
        if is_official_djp_domain(domain):
            spans.append(
                (
                    match.start(),
                    end_pos,
                    trimmed,
                    "official_url",
                    f"Website resmi DJP ({domain}).",
                )
            )
        else:
            spans.append(
                (
                    match.start(),
                    end_pos,
                    trimmed,
                    "suspicious_url",
                    f"Link di luar pajak.go.id ({domain}).",
                )
            )

    matched_words: list[str] = []
    if risk_level in ("TINGGI", "SEDANG"):
        cue_stems = trigger_stems | _URGENCY_STEMS | _THREAT_STEMS | _ACTION_BAIT_STEMS
        for match in re.finditer(r"[A-Za-z]{3,}", raw_text):
            start_pos, end_pos = match.start(), match.end()
            if any(not (end_pos <= s or start_pos >= e) for s, e, *_ in spans):
                continue
            word = match.group(0)
            low = word.lower()
            stem = STEM_WORD(low)
            if stem in _NEUTRAL_TAX_STEMS or low in _NEUTRAL_TAX_STEMS:
                continue
            if (stem in cue_stems or low in cue_stems) and low not in {
                w.lower() for w in matched_words
            }:
                matched_words.append(word)

    spans.sort(key=lambda item: item[0])
    highlights = [
        {
            "start": s,
            "end": e,
            "text": text,
            "kind": kind,
            "reason": reason,
        }
        for s, e, text, kind, reason in spans
    ]
    return highlights, matched_words[:5]


def _build_plain_reasons(
    risk_level: str,
    heuristics: dict[str, Any],
    matched_words: list[str],
    trigger_stems: set[str],
) -> list[dict[str, str]]:
    reasons: list[dict[str, str]] = []

    if heuristics["has_apk"]:
        files = ", ".join(heuristics["apk_matches"])
        reasons.append(
            {
                "type": "danger",
                "title": f"File .apk ({files})",
                "detail": "Bisa curi OTP & akses m-banking.",
            }
        )

    if heuristics["suspicious_domains"]:
        domains = ", ".join(heuristics["suspicious_domains"])
        reasons.append(
            {
                "type": "danger",
                "title": f"Link asing ({domains})",
                "detail": "Web resmi DJP selalu berakhiran pajak.go.id.",
            }
        )

    if risk_level in ("TINGGI", "SEDANG"):
        all_cue_stems = trigger_stems | {STEM_WORD(w.lower()) for w in matched_words}
        has_threat = bool(all_cue_stems & _THREAT_STEMS)
        has_urgency = bool(all_cue_stems & _URGENCY_STEMS)
        has_bait = bool(all_cue_stems & _ACTION_BAIT_STEMS)

        word_preview = ", ".join(matched_words[:4])
        if has_threat or has_urgency:
            reasons.append(
                {
                    "type": "warning",
                    "title": "Nada memaksa / ancam denda",
                    "detail": (
                        f"Kata pemicu: {word_preview}."
                        if word_preview
                        else "Membuat panik agar cepat klik."
                    ),
                }
            )
        elif has_bait and not heuristics["has_apk"]:
            reasons.append(
                {
                    "type": "warning",
                    "title": "Minta klik / install / login",
                    "detail": (
                        f"Kata pemicu: {word_preview}."
                        if word_preview
                        else "Mengarahkan korban mengisi data pribadi."
                    ),
                }
            )
        if not reasons:
            reasons.append(
                {
                    "type": "warning",
                    "title": "Pola kalimat scam",
                    "detail": "Mirip modus penipuan pajak di WA.",
                }
            )
    else:
        if heuristics["official_domains"]:
            domains = ", ".join(heuristics["official_domains"])
            reasons.append(
                {
                    "type": "safe",
                    "title": f"Link resmi ({domains})",
                    "detail": "Domain sah milik DJP.",
                }
            )
        reasons.append(
            {
                "type": "safe",
                "title": "Tidak ada file .apk / link palsu",
                "detail": "Gaya bahasa normal.",
            }
        )

    return reasons


def _build_action_steps(risk_level: str, has_apk: bool) -> list[str]:
    if has_apk:
        return [
            "Jangan download / install file .apk.",
            "Hapus chat & block nomor pengirim.",
            "Terlanjur install? Buka tab Darurat .apk.",
        ]
    if risk_level in ("TINGGI", "SEDANG"):
        return [
            "Jangan klik link atau kasih OTP, PIN, & EFIN.",
            "Cek info asli di pajak.go.id atau Kring Pajak 1500200.",
            "Share info ini ke grup jika pesan beredar.",
        ]
    return [
        "Aman dibaca, tetap rahasiakan OTP & password.",
        "Akses layanan pajak langsung di pajak.go.id.",
    ]


def _build_human_verdict(
    label: int,
    risk_level: str,
    svm_prob: float,
    has_apk: bool,
    suspicious_domains: list[str],
    official_domains: list[str],
) -> tuple[str, str, str, str]:
    risk_pct = round(svm_prob * 100)
    safe_pct = max(0, 100 - risk_pct)

    if risk_level == "TINGGI":
        badge = "BAHAYA / SCAM"
        title = "Jangan Klik atau Download!"
        if has_apk:
            summary = "Ada file .apk berbahaya. DJP tidak pernah kirim aplikasi lewat WA."
        elif suspicious_domains:
            summary = "Link mengarah ke web palsu (bukan pajak.go.id)."
        else:
            summary = "Kalimatnya cocok dengan pola chat scam pajak."
        confidence_note = f"Scam {max(risk_pct, 85 if has_apk else risk_pct)}%"
    elif risk_level == "SEDANG":
        badge = "WASPADA"
        title = "Cek Dulu Sebelum Klik"
        if suspicious_domains and label == 0:
            summary = "Ada link di luar pajak.go.id. Pastikan dulu pengirimnya."
            confidence_note = "Link eksternal"
        else:
            summary = "Ada kata yang mirip pola scam. Cek langsung ke pajak.go.id."
            confidence_note = f"Risiko {risk_pct}%"
    else:
        badge = "AMAN"
        title = "Pola Chat Resmi / Normal"
        if official_domains:
            summary = "Link resmi pajak.go.id & tidak ada ciri scam."
        else:
            summary = "Tidak ada file .apk, link palsu, atau paksaan."
        confidence_note = f"Aman {safe_pct}%"

    return title, badge, summary, confidence_note


def _assemble_prediction(
    text: str,
    cleaned: str,
    features_row: Any,
    svm_prob: float,
    rf_prob: float,
    feature_names: np.ndarray,
    svm_coefs: np.ndarray,
    top_k: int,
) -> dict[str, Any]:
    """Combine calibrated model probabilities, domain/APK rules, and layperson XAI."""
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

    if label == 1:
        label_text = "Indikasi Scam"
    elif risk_level == "SEDANG":
        label_text = "Perlu Verifikasi / Waspada"
    else:
        label_text = "Pesan Aman / Resmi"

    triggers = _extract_top_triggers(
        features_row,
        feature_names,
        svm_coefs,
        top_k=top_k,
    )
    trigger_stems = _collect_trigger_stems(triggers)
    highlights, trigger_words = _extract_highlights_and_triggers(text, risk_level, trigger_stems)
    risk_title, risk_badge, verdict_summary, confidence_note = _build_human_verdict(
        label=label,
        risk_level=risk_level,
        svm_prob=svm_prob,
        has_apk=heuristics["has_apk"],
        suspicious_domains=heuristics["suspicious_domains"],
        official_domains=heuristics["official_domains"],
    )
    plain_reasons = _build_plain_reasons(
        risk_level=risk_level,
        heuristics=heuristics,
        matched_words=trigger_words,
        trigger_stems=trigger_stems,
    )
    action_steps = _build_action_steps(risk_level=risk_level, has_apk=heuristics["has_apk"])

    return {
        "label": label,
        "label_text": label_text,
        "risk_level": risk_level,
        "risk_title": risk_title,
        "risk_badge": risk_badge,
        "verdict_summary": verdict_summary,
        "confidence_note": confidence_note,
        "svm_probability": round(svm_prob, 4),
        "rf_probability": round(rf_prob, 4),
        "cleaned_text": cleaned,
        "has_apk": heuristics["has_apk"],
        "apk_matches": heuristics["apk_matches"],
        "urls_found": heuristics["urls_found"],
        "official_domains": heuristics["official_domains"],
        "suspicious_domains": heuristics["suspicious_domains"],
        "top_triggers": triggers,
        "highlights": highlights,
        "trigger_words": trigger_words,
        "plain_reasons": plain_reasons,
        "action_steps": action_steps,
        "recommendation": _build_recommendation(
            label=label,
            has_apk=heuristics["has_apk"],
            suspicious_domains=heuristics["suspicious_domains"],
            official_domains=heuristics["official_domains"],
        ),
    }


def predict_message(
    raw_text: str,
    model_path: str | Path = MODEL_PATH,
    top_k: int = 8,
) -> dict[str, Any]:
    """Run full preprocessing, SVM Platt + RF inference, heuristic checks, and layperson XAI."""
    text = raw_text.replace("\x00", "").strip()
    if not text:
        raise ValueError("Teks pesan tidak boleh kosong.")

    bundle = load_model_bundle(model_path)
    vectorizer = bundle["vectorizer"]
    svm_calibrated = bundle["svm_calibrated"]
    random_forest = bundle["random_forest"]

    cleaned = clean_text(text)
    features = vectorizer.transform([cleaned])
    svm_cal_input = [cleaned] if bundle["svm_is_pipeline"] else features
    svm_prob = float(svm_calibrated.predict_proba(svm_cal_input)[0, 1])
    rf_prob = float(random_forest.predict_proba(features)[0, 1])

    return _assemble_prediction(
        text=text,
        cleaned=cleaned,
        features_row=features,
        svm_prob=svm_prob,
        rf_prob=rf_prob,
        feature_names=bundle["feature_names"],
        svm_coefs=bundle["svm_coefs"],
        top_k=top_k,
    )


def predict_messages_batch(
    raw_texts: list[str],
    model_path: str | Path = MODEL_PATH,
    top_k: int = 5,
) -> list[dict[str, Any]]:
    """Run vectorized batch preprocessing and model inference across multiple messages."""
    bundle = load_model_bundle(model_path)
    vectorizer = bundle["vectorizer"]
    svm_calibrated = bundle["svm_calibrated"]
    random_forest = bundle["random_forest"]
    feature_names = bundle["feature_names"]
    svm_coefs = bundle["svm_coefs"]
    svm_is_pipeline = bundle["svm_is_pipeline"]

    outputs: list[dict[str, Any] | None] = [None] * len(raw_texts)
    valid_entries: list[tuple[int, str, str]] = []

    for idx, raw in enumerate(raw_texts):
        cleaned_input = raw.replace("\x00", "").strip()
        if not cleaned_input:
            outputs[idx] = {"index": idx, "error": "Teks kosong dilewati."}
            continue
        valid_entries.append((idx, cleaned_input, clean_text(cleaned_input)))

    if valid_entries:
        cleaned_batch = [entry[2] for entry in valid_entries]
        features_matrix = vectorizer.transform(cleaned_batch)
        svm_cal_inputs = cleaned_batch if svm_is_pipeline else features_matrix
        svm_probs = svm_calibrated.predict_proba(svm_cal_inputs)[:, 1]
        rf_probs = random_forest.predict_proba(features_matrix)[:, 1]

        for row_idx, (orig_idx, text, cleaned) in enumerate(valid_entries):
            item = _assemble_prediction(
                text=text,
                cleaned=cleaned,
                features_row=features_matrix[row_idx],
                svm_prob=float(svm_probs[row_idx]),
                rf_prob=float(rf_probs[row_idx]),
                feature_names=feature_names,
                svm_coefs=svm_coefs,
                top_k=top_k,
            )
            item["index"] = orig_idx
            outputs[orig_idx] = item

    return [item for item in outputs if item is not None]
