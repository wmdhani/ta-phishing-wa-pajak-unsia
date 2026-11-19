import hashlib
import json
import re
from pathlib import Path
from urllib.parse import urlparse

import pandas as pd

from src.korpus_pajak import (
    CURATED_TAX_RECORDS,
    OFFICIAL_IOCS_DJP,
    SOURCE_METADATA,
)

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "04 Dataset"
RAW_DIR = DATA_DIR / "01 Data Mentah"
PROCESSED_DIR = DATA_DIR / "02 Data Olahan"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def clean_text(text: str) -> str:
    text = str(text).lower()
    text = re.sub(r"\.apk\b", " token_apk ", text)
    text = re.sub(
        r"https?://\S+|www\.\S+|bit\.ly/\S+|\b[a-z0-9.-]+\.(?:go\.id|co\.id|my\.id|com|net|org|xyz|id|cc)\S*",
        " token_url ",
        text,
    )
    text = re.sub(r"[^a-z0-9\s_]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def strip_djp_boilerplate(raw_text: str) -> str:
    lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
    skip_exact = {
        "Tax Treaty dan Multilateral Instrument",
        "Tema UU Harmonisasi Peraturan Perpajakan Program Pengungkapan Sukarela DJP Tanggap Covid-19 Pajak Digital Infografis Jurnal Pajak Lapor Tahunan Buku Elektronik Kerja Sama dan Kemitraan Klaster Kemudahan Berusaha Bidang Perpajakan Penegakan Hukum FAQ Podcast Cermati Podcast Pamorku",
        "Klaster Kemudahan Berusaha Bidang Perpajakan",
        "Coretax DJP Reformasi Perpajakan DJP Pembaruan Sistem Inti Administrasi Perpajakan (PSIAP) [Coretax]",
        "Pembaruan Sistem Inti Administrasi Perpajakan (PSIAP) [Coretax]",
        "Jalan Gatot Subroto, Kav. 40-42, Jakarta 12190 Telp: (+62) 21 - 525 0208",
        "Copyright © 2022 Direktorat Jenderal Pajak.",
        "Ikuti Kami",
        "Back to Top",
    }
    filtered = [line for line in lines if line not in skip_exact]
    return "\n".join(filtered)


def export_scraped_official_sources(staged_json_path: Path) -> pd.DataFrame:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    raw_items = json.loads(staged_json_path.read_text(encoding="utf-8"))

    enriched_records = []
    summary_rows = []

    for item in raw_items:
        sid = item["id"]
        domain = urlparse(item["url"]).netloc.lower()
        meta = SOURCE_METADATA.get(
            sid,
            {
                "id_sumber": sid,
                "kategori_sumber": "Portal_Berita_Pajak_dan_Cek_Fakta",
                "instansi_penerbit": domain,
                "nomor_dokumen_resmi": "-",
                "tanggal_publikasi": "-",
                "url": item["url"],
            },
        )
        raw_body = item.get("body", item.get("cleaned_text", ""))
        cleaned_body = strip_djp_boilerplate(raw_body)
        content_hash = sha256_text(cleaned_body)

        record = {
            "id_sumber": sid,
            "kategori_sumber": meta["kategori_sumber"],
            "instansi_penerbit": meta["instansi_penerbit"],
            "nomor_dokumen_resmi": meta["nomor_dokumen_resmi"],
            "tanggal_publikasi": meta["tanggal_publikasi"],
            "judul_halaman": item.get("title", ""),
            "url": item["url"],
            "domain": domain,
            "http_status": item.get("status", 200),
            "jumlah_karakter_bersih": len(cleaned_body),
            "sha256_konten": content_hash,
            "teks_hasil_scrape": cleaned_body,
        }
        enriched_records.append(record)
        summary_rows.append({k: v for k, v in record.items() if k != "teks_hasil_scrape"})

    json_out = RAW_DIR / "DJP Hasil Scrape 68 Sumber Resmi.json"
    json_out.write_text(json.dumps(enriched_records, ensure_ascii=False, indent=2), encoding="utf-8")

    df_summary = pd.DataFrame(summary_rows)
    csv_out = RAW_DIR / "DJP Ringkasan Scrape 68 Sumber Resmi.csv"
    df_summary.to_csv(csv_out, index=False, encoding="utf-8")

    ioc_out = RAW_DIR / "DJP Indikator Penipuan dan Kanal Resmi.json"
    ioc_out.write_text(json.dumps(OFFICIAL_IOCS_DJP, ensure_ascii=False, indent=2), encoding="utf-8")
    return df_summary


def export_curated_tax_dataset() -> pd.DataFrame:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    df_tax = pd.DataFrame(CURATED_TAX_RECORDS)

    if df_tax["Teks"].duplicated().any():
        dups = df_tax[df_tax["Teks"].duplicated(keep=False)]["Teks"].tolist()
        raise ValueError(f"Duplicate texts found in CURATED_TAX_RECORDS: {dups}")

    df_tax.to_csv(
        PROCESSED_DIR / "Dataset Pajak Terkurasi 260 Baris.csv", index=False, encoding="utf-8"
    )
    return df_tax


def build_combined_datasets(df_tax: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    df_rahmi = pd.read_csv(RAW_DIR / "Rahmi 2016 Korpus SMS Spam Utama v1.csv")
    df_rahmi_bin = df_rahmi[df_rahmi["label"].isin([0, 1])][["Teks", "label"]].copy()
    df_rahmi_bin["sumber"] = "Korpus_Umum_Rahmi2016"
    df_rahmi_bin["kategori_modus"] = df_rahmi_bin["label"].map(
        {0: "SMS_Normal_Umum", 1: "SMS_Penipuan_Umum"}
    )
    df_rahmi_bin["id_sumber"] = "EXT-RAHMI-2016"
    df_rahmi_bin["url_sumber"] = (
        "https://raw.githubusercontent.com/agustinustheo/indonesian-sms-spam-filtering/master/training_script/corpus/external/rahmi2016/dataset_sms_spam_v1.csv"
    )

    df_tax_bin = df_tax[["Teks", "label", "kategori_modus", "id_sumber", "url_sumber"]].copy()
    df_tax_bin["sumber"] = "Korpus_Pajak_Terverifikasi"

    df_primary = pd.concat([df_rahmi_bin, df_tax_bin], ignore_index=True)
    df_primary["clean_text"] = df_primary["Teks"].apply(clean_text)
    df_primary["ada_token_apk"] = df_primary["clean_text"].str.contains(r"\btoken_apk\b").astype(int)
    df_primary["ada_token_url"] = df_primary["clean_text"].str.contains(r"\btoken_url\b").astype(int)
    df_primary["jumlah_kata"] = df_primary["clean_text"].str.split().str.len()
    df_primary["jumlah_karakter"] = df_primary["Teks"].str.len()

    df_primary.to_csv(
        PROCESSED_DIR / "Dataset Gabungan Utama Biner 1164 Baris.csv",
        index=False,
        encoding="utf-8",
    )

    df_theo = pd.read_csv(RAW_DIR / "Theodorus 2021 Korpus SMS Spam IEEE.csv")
    df_theo_bin = df_theo[df_theo["Label"].isin([0, 2])].copy()
    df_theo_bin["Teks"] = df_theo_bin["Text"].astype(str).str.strip()
    df_theo_bin["label"] = df_theo_bin["Label"].map({0: 0, 2: 1})
    df_theo_bin["sumber"] = "Korpus_Umum_Theodorus2021_IEEE"
    df_theo_bin["kategori_modus"] = df_theo_bin["label"].map(
        {0: "SMS_Normal_Theodorus2021", 1: "SMS_Fraud_Theodorus2021"}
    )
    df_theo_bin["id_sumber"] = "EXT-THEODORUS-2021"
    df_theo_bin["url_sumber"] = "https://doi.org/10.1109/EIConCIT50028.2021.9431859"
    df_theo_bin = df_theo_bin[["Teks", "label", "kategori_modus", "id_sumber", "url_sumber", "sumber"]]

    df_saragih = pd.read_csv(RAW_DIR / "Saragih 2024 Korpus SMS Spam Indo.csv")
    df_saragih["kat_clean"] = df_saragih["Jenis_spam"].astype(str).str.strip().str.lower()
    df_saragih_bin = df_saragih[df_saragih["kat_clean"].isin(["non-spam", "penipuan"])].copy()
    df_saragih_bin["Teks"] = df_saragih_bin["pesan"].astype(str).str.strip()
    df_saragih_bin["label"] = df_saragih_bin["kat_clean"].map({"non-spam": 0, "penipuan": 1})
    df_saragih_bin["sumber"] = "Korpus_Umum_Saragih2024"
    df_saragih_bin["kategori_modus"] = df_saragih_bin["label"].map(
        {0: "SMS_Normal_Saragih2024", 1: "SMS_Penipuan_Saragih2024"}
    )
    df_saragih_bin["id_sumber"] = "EXT-SARAGIH-2024"
    df_saragih_bin["url_sumber"] = (
        "https://github.com/Sctian514/Indonesian-sms-spam-classifier"
    )
    df_saragih_bin = df_saragih_bin[
        ["Teks", "label", "kategori_modus", "id_sumber", "url_sumber", "sumber"]
    ]

    df_ext = pd.concat(
        [
            df_primary[["Teks", "label", "kategori_modus", "id_sumber", "url_sumber", "sumber"]],
            df_theo_bin,
            df_saragih_bin,
        ],
        ignore_index=True,
    )
    df_ext["clean_text"] = df_ext["Teks"].apply(clean_text)
    df_ext = df_ext.drop_duplicates(subset=["clean_text"], keep="first").reset_index(drop=True)
    df_ext["ada_token_apk"] = df_ext["clean_text"].str.contains(r"\btoken_apk\b").astype(int)
    df_ext["ada_token_url"] = df_ext["clean_text"].str.contains(r"\btoken_url\b").astype(int)
    df_ext["jumlah_kata"] = df_ext["clean_text"].str.split().str.len()
    df_ext["jumlah_karakter"] = df_ext["Teks"].str.len()

    df_ext.to_csv(
        PROCESSED_DIR / "Dataset Gabungan Diperluas Biner 2521 Baris.csv",
        index=False,
        encoding="utf-8",
    )
    return df_primary, df_ext


def build_provenance_catalog(df_summary: pd.DataFrame) -> pd.DataFrame:
    dataset_files = [
        {
            "id_katalog": "FILE-RAW-01",
            "nama_file": "04 Dataset/01 Data Mentah/Rahmi 2016 Korpus SMS Spam Utama v1.csv",
            "jenis_data": "File Mentah (Korpus Dasar Utama)",
            "instansi_atau_penulis": "Ferdila Rahmi & Yudi Wibisono (Universitas Pendidikan Indonesia, 2016)",
            "lisensi": "CC BY-SA 4.0",
            "jumlah_baris": 1143,
            "url_sumber": "https://raw.githubusercontent.com/agustinustheo/indonesian-sms-spam-filtering/master/training_script/corpus/external/rahmi2016/dataset_sms_spam_v1.csv",
            "sha256": sha256_file(RAW_DIR / "Rahmi 2016 Korpus SMS Spam Utama v1.csv"),
        },
        {
            "id_katalog": "FILE-RAW-02",
            "nama_file": "04 Dataset/01 Data Mentah/Rahmi 2016 Arsip Asli SMS Spam.csv",
            "jenis_data": "File Mentah (Salinan Arsip Rahmi & Wibisono 2016)",
            "instansi_atau_penulis": "Ferdila Rahmi & Yudi Wibisono (UPI, 2016)",
            "lisensi": "CC BY-SA 4.0",
            "jumlah_baris": 1143,
            "url_sumber": "https://yudiwbs.wordpress.com/2018/08/05/dataset-klasifikasi-bahasa-indonesia-sms-spam-klasifikasi-teks-dengan-scikit-learn/",
            "sha256": sha256_file(RAW_DIR / "Rahmi 2016 Arsip Asli SMS Spam.csv"),
        },
        {
            "id_katalog": "FILE-RAW-03",
            "nama_file": "04 Dataset/01 Data Mentah/Theodorus 2021 Korpus SMS Spam IEEE.csv",
            "jenis_data": "File Mentah (Korpus Benchmark IEEE EIConCIT 2021)",
            "instansi_atau_penulis": "Agustinus Theodorus, Tio K. Prasetyo, Reynaldi Hartono, Derwin Suhartono (BINUS University, 2021)",
            "lisensi": "CC BY-SA 4.0",
            "jumlah_baris": 4125,
            "url_sumber": "https://doi.org/10.1109/EIConCIT50028.2021.9431859",
            "sha256": sha256_file(RAW_DIR / "Theodorus 2021 Korpus SMS Spam IEEE.csv"),
        },
        {
            "id_katalog": "FILE-RAW-04",
            "nama_file": "04 Dataset/01 Data Mentah/Kurniawan 2024 Korpus Phishing SMS dan Email Indo.csv",
            "jenis_data": "File Mentah (Korpus Phishing SMS & Email Bahasa Indonesia)",
            "instansi_atau_penulis": "Rasen Kurniawan (2024) - Kompilasi Kaggle & Gist Yudi Wibisono",
            "lisensi": "Open Source GitHub",
            "jumlah_baris": 1772,
            "url_sumber": "https://github.com/rasen-kurniawan/phishing-detection-eda",
            "sha256": sha256_file(RAW_DIR / "Kurniawan 2024 Korpus Phishing SMS dan Email Indo.csv"),
        },
        {
            "id_katalog": "FILE-RAW-05",
            "nama_file": "04 Dataset/01 Data Mentah/Saragih 2024 Korpus SMS Spam Indo.csv",
            "jenis_data": "File Mentah (Korpus Klasifikasi SMS Spam Indonesia)",
            "instansi_atau_penulis": "Samuel Cristian Saragih (2024)",
            "lisensi": "MIT License",
            "jumlah_baris": 690,
            "url_sumber": "https://github.com/Sctian514/Indonesian-sms-spam-classifier",
            "sha256": sha256_file(RAW_DIR / "Saragih 2024 Korpus SMS Spam Indo.csv"),
        },
        {
            "id_katalog": "FILE-RAW-06",
            "nama_file": "04 Dataset/01 Data Mentah/DJP Hasil Scrape 68 Sumber Resmi.json",
            "jenis_data": "File Mentah Hasil Web Scraping 68 Halaman Resmi Pajak & Cek Fakta",
            "instansi_atau_penulis": "DJP (pajak.go.id), DDTC News, Ortax, Jalahoaks DKI, BCA, Antara, DetikFinance",
            "lisensi": "Informasi Publik Pemerintah & Berita Terverifikasi",
            "jumlah_baris": len(df_summary),
            "url_sumber": "https://www.pajak.go.id/id/pengumuman",
            "sha256": sha256_file(RAW_DIR / "DJP Hasil Scrape 68 Sumber Resmi.json"),
        },
        {
            "id_katalog": "FILE-RAW-07",
            "nama_file": "04 Dataset/01 Data Mentah/DJP Indikator Penipuan dan Kanal Resmi.json",
            "jenis_data": "File Mentah Ekstraksi IOC (Domain/Nomor Penipu) & Kanal Resmi DJP",
            "instansi_atau_penulis": "Direktorat Jenderal Pajak (PENG-31/PJ.09/2024 s.d. PENG-50/PJ.09/2025)",
            "lisensi": "Informasi Publik DJP",
            "jumlah_baris": 31,
            "url_sumber": "https://www.pajak.go.id/id/pengumuman/waspada-penipuan-yang-mengatasnamakan-direktorat-jenderal-pajak",
            "sha256": sha256_file(RAW_DIR / "DJP Indikator Penipuan dan Kanal Resmi.json"),
        },
        {
            "id_katalog": "FILE-PROC-01",
            "nama_file": "04 Dataset/02 Data Olahan/Dataset Pajak Terkurasi 260 Baris.csv",
            "jenis_data": "File Olahan (Korpus Spesifik Domain Perpajakan Seimbang)",
            "instansi_atau_penulis": "Kurasi Terverifikasi dari 68 Sumber Resmi DJP, KPP/KP2KP, Jalahoaks, DDTC, Ortax, BCA",
            "lisensi": "CC BY-SA 4.0",
            "jumlah_baris": 260,
            "url_sumber": "https://www.pajak.go.id",
            "sha256": sha256_file(PROCESSED_DIR / "Dataset Pajak Terkurasi 260 Baris.csv"),
        },
        {
            "id_katalog": "FILE-PROC-02",
            "nama_file": "04 Dataset/02 Data Olahan/Dataset Gabungan Utama Biner 1164 Baris.csv",
            "jenis_data": "File Olahan Utama (Korpus Dasar Biner Rahmi 2016 + Korpus Pajak 260 Baris)",
            "instansi_atau_penulis": "Pipeline Eksperimen Tugas Akhir (Rahmi 2016 + Kurasi DJP 2024-2026)",
            "lisensi": "CC BY-SA 4.0",
            "jumlah_baris": 1164,
            "url_sumber": "https://www.pajak.go.id",
            "sha256": sha256_file(PROCESSED_DIR / "Dataset Gabungan Utama Biner 1164 Baris.csv"),
        },
        {
            "id_katalog": "FILE-PROC-03",
            "nama_file": "04 Dataset/02 Data Olahan/Dataset Gabungan Diperluas Biner 2521 Baris.csv",
            "jenis_data": "File Olahan Diperluas (Lintas Korpus Rahmi 2016 + Theodorus 2021 + Saragih 2024 + Pajak)",
            "instansi_atau_penulis": "Pipeline Eksperimen Tugas Akhir (Multi-Corpus Benchmark)",
            "lisensi": "CC BY-SA 4.0",
            "jumlah_baris": len(
                pd.read_csv(PROCESSED_DIR / "Dataset Gabungan Diperluas Biner 2521 Baris.csv")
            ),
            "url_sumber": "https://doi.org/10.1109/EIConCIT50028.2021.9431859",
            "sha256": sha256_file(PROCESSED_DIR / "Dataset Gabungan Diperluas Biner 2521 Baris.csv"),
        },
    ]

    df_cat = pd.DataFrame(dataset_files)
    df_cat.to_csv(PROCESSED_DIR / "Katalog Asal Sumber Data.csv", index=False, encoding="utf-8")
    (PROCESSED_DIR / "Katalog Asal Sumber Data.json").write_text(
        json.dumps(dataset_files, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return df_cat


def main(snapshot_path: Path | None = None) -> None:
    resolved_snapshot = snapshot_path or (RAW_DIR / "DJP Snapshot Scrape Mentah.json")
    df_summary = export_scraped_official_sources(resolved_snapshot)
    df_tax = export_curated_tax_dataset()
    df_primary, df_ext = build_combined_datasets(df_tax)
    df_cat = build_provenance_catalog(df_summary)

    print(f"Scraped official web sources saved : {len(df_summary)} articles")
    print(f"Curated tax corpus saved           : {len(df_tax)} rows (Class 1={(df_tax['label']==1).sum()}, Class 0={(df_tax['label']==0).sum()})")
    print(f"Primary combined binary dataset    : {len(df_primary)} rows (Class 1={(df_primary['label']==1).sum()}, Class 0={(df_primary['label']==0).sum()})")
    print(f"Extended combined binary dataset   : {len(df_ext)} rows (Class 1={(df_ext['label']==1).sum()}, Class 0={(df_ext['label']==0).sum()})")
    print(f"Provenance catalog entries         : {len(df_cat)} dataset artifacts")


if __name__ == "__main__":
    main()
