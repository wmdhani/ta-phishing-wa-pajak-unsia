from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any

import httpx
import pandas as pd
import streamlit as st

APP_DIR = Path(__file__).resolve().parent
ROOT_DIR = APP_DIR.parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from inference import load_model_bundle, predict_message

DEFAULT_API_URL = os.environ.get("PHISHING_API_URL", "http://127.0.0.1:8000")
EVAL_TABLE_PATH = ROOT_DIR / "05 Hasil Evaluasi" / "tabel_komparasi_utama.csv"

PRESETS = {
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

st.set_page_config(
    page_title="Deteksi Phishing WA Pajak - UNSIA",
    page_icon="🛡️",
    layout="wide",
)


def _check_api_health(api_url: str) -> tuple[bool, dict[str, Any]]:
    try:
        resp = httpx.get(f"{api_url.rstrip('/')}/health", timeout=1.5)
        if resp.status_code == 200:
            return True, resp.json()
    except httpx.HTTPError:
        pass
    return False, {}


def _run_prediction(text: str, api_url: str, top_k: int = 8) -> tuple[dict[str, Any], str]:
    try:
        resp = httpx.post(
            f"{api_url.rstrip('/')}/predict",
            json={"text": text, "top_k": top_k},
            timeout=5.0,
        )
        if resp.status_code == 200:
            return resp.json(), "FastAPI REST API"
    except httpx.HTTPError:
        pass
    return predict_message(text, top_k=top_k), "Fallback Lokal (inference.py)"


def _render_result(result: dict[str, Any], engine_source: str) -> None:
    is_phishing = result["label"] == 1
    risk = result["risk_level"]

    if risk == "TINGGI":
        st.error(f"**Status: {result['label_text']} | Risiko {risk}**")
    elif risk == "SEDANG":
        st.warning(f"**Status: {result['label_text']} | Risiko {risk}**")
    else:
        st.success(f"**Status: {result['label_text']} | Risiko {risk}**")

    col1, col2, col3 = st.columns(3)
    col1.metric("Probabilitas LinearSVC (Platt)", f"{result['svm_probability'] * 100:.2f}%")
    col2.metric("Probabilitas Random Forest", f"{result['rf_probability'] * 100:.2f}%")
    col3.metric("Deteksi Pola .apk", "TERDETEKSI" if result["has_apk"] else "Tidak Ada")

    st.info(result["recommendation"])

    dom_col1, dom_col2 = st.columns(2)
    with dom_col1:
        st.markdown("**Domain Resmi `pajak.go.id`**")
        if result["official_domains"]:
            st.write(", ".join(result["official_domains"]))
        else:
            st.caption("Tidak ada tautan domain resmi DJP.")
    with dom_col2:
        st.markdown("**Domain Mencurigakan / Eksternal**")
        if result["suspicious_domains"]:
            st.write(", ".join(result["suspicious_domains"]))
        else:
            st.caption("Tidak ada domain eksternal mencurigakan.")

    st.markdown("**Penjelasan Kata Pemicu (*Explainable AI* - Bobot LinearSVC)**")
    if result["top_triggers"]:
        df_trig = pd.DataFrame(result["top_triggers"])
        st.dataframe(
            df_trig.rename(
                columns={
                    "token": "Token TF-IDF",
                    "contribution": "Kontribusi Skor",
                    "svm_coef": "Koefisien LinearSVC",
                    "direction": "Arah Kelas",
                }
            ),
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.caption("Tidak ada token fitur TF-IDF yang cocok pada kamus model.")

    with st.expander(f"Detail Teknis Praproses & Mesin ({engine_source})"):
        st.code(result["cleaned_text"] or "(kosong setelah praproses)", language="text")
        if is_phishing and result["apk_matches"]:
            st.write("Berkas `.apk` terdeteksi:", result["apk_matches"])


def main() -> None:
    st.title("Purwarupa Deteksi Phishing WhatsApp Perpajakan")
    st.caption(
        "Tugas Akhir PJJ Sistem Informasi UNSIA | Komparasi LinearSVC (Kalibrasi Platt) "
        "dan Random Forest"
    )

    with st.sidebar:
        st.header("Konfigurasi Layanan")
        api_url = st.text_input("Endpoint FastAPI", value=DEFAULT_API_URL)
        api_online, health_data = _check_api_health(api_url)
        if api_online:
            st.success("FastAPI Terhubung (`GET /health` OK)")
        else:
            st.warning("FastAPI Offline: menggunakan Fallback Lokal")

        bundle_meta = health_data.get("metadata") or load_model_bundle().get("metadata", {})
        if bundle_meta:
            st.markdown("**Metadata Model**")
            st.write(f"- Korpus Latih: `{bundle_meta.get('n_samples', '-')}` baris")
            st.write(
                f"- Akurasi Holdout SVM: `{bundle_meta.get('holdout_accuracy_svm', 0):.4f}`"
            )
            st.write(
                f"- Akurasi Holdout RF: `{bundle_meta.get('holdout_accuracy_rf', 0):.4f}`"
            )

    tab_single, tab_batch, tab_eval = st.tabs(
        ["Uji Pesan Tunggal", "Uji Batch (CSV)", "Ringkasan Evaluasi Model"]
    )

    with tab_single:
        st.subheader("Analisis Pesan WhatsApp")
        preset_col1, preset_col2, preset_col3 = st.columns(3)
        if preset_col1.button("Contoh Phishing .apk", use_container_width=True):
            st.session_state["input_msg"] = PRESETS["Phishing APK (Coretax Palsu)"]
        if preset_col2.button("Contoh Domain Palsu", use_container_width=True):
            st.session_state["input_msg"] = PRESETS["Phishing Domain Palsu"]
        if preset_col3.button("Contoh Resmi DJP", use_container_width=True):
            st.session_state["input_msg"] = PRESETS["Pengumuman Resmi DJP"]

        msg_text = st.text_area(
            "Tempelkan teks pesan WhatsApp yang ingin diperiksa:",
            key="input_msg",
            height=130,
            placeholder="Contoh: Segera unduh file pajak.apk untuk pembaruan data NPWP...",
        )

        if st.button("Periksa Pesan", type="primary"):
            if not msg_text.strip():
                st.warning("Masukkan teks pesan terlebih dahulu.")
            else:
                result, source = _run_prediction(msg_text, api_url)
                _render_result(result, source)

    with tab_batch:
        st.subheader("Analisis Batch Berkas CSV")
        uploaded = st.file_uploader("Unggah berkas CSV dengan kolom `text`", type=["csv"])
        if uploaded is not None:
            df_in = pd.read_csv(uploaded)
            if "text" not in df_in.columns:
                st.error("Berkas CSV wajib memiliki kolom bernama `text`.")
            else:
                st.write(f"Jumlah baris terbaca: `{len(df_in)}`")
                if st.button("Proses Seluruh Baris"):
                    rows: list[dict[str, Any]] = []
                    for text in df_in["text"].fillna("").astype(str):
                        if not text.strip():
                            continue
                        res, _ = _run_prediction(text, api_url, top_k=3)
                        rows.append(
                            {
                                "text": text,
                                "label": res["label_text"],
                                "risk_level": res["risk_level"],
                                "svm_probability": res["svm_probability"],
                                "rf_probability": res["rf_probability"],
                                "has_apk": res["has_apk"],
                                "suspicious_domains": ", ".join(res["suspicious_domains"]),
                            }
                        )
                    df_out = pd.DataFrame(rows)
                    st.dataframe(df_out, use_container_width=True)
                    st.download_button(
                        "Unduh Hasil CSV",
                        data=df_out.to_csv(index=False).encode("utf-8"),
                        file_name="hasil_deteksi_batch.csv",
                        mime="text/csv",
                    )

    with tab_eval:
        st.subheader("Komparasi Kinerja Model (Hasil Eksperimen)")
        if EVAL_TABLE_PATH.exists():
            df_eval = pd.read_csv(EVAL_TABLE_PATH)
            st.dataframe(df_eval, use_container_width=True, hide_index=True)
        else:
            st.info("Berkas tabel_komparasi_utama.csv belum tersedia di 05 Hasil Evaluasi.")


if __name__ == "__main__":
    main()
