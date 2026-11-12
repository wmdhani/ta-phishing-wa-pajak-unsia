import hashlib
import json
from pathlib import Path

import pandas as pd

from src.tax_corpus_records import SOURCE_METADATA

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"


def test_raw_corpora_exist_and_row_counts() -> None:
    df_v1 = pd.read_csv(DATA_DIR / "raw_sms_spam_v1.csv")
    assert len(df_v1) == 1143
    assert set(df_v1["label"].unique()) == {0, 1, 2}

    df_rahmi = pd.read_csv(RAW_DIR / "raw_sms_spam_rahmi2016.csv")
    assert len(df_rahmi) == 1143

    df_theo = pd.read_csv(RAW_DIR / "raw_sms_theodorus2021.csv")
    assert len(df_theo) == 4125

    df_kurniawan = pd.read_csv(RAW_DIR / "raw_phishing_sms_indo_kurniawan2024.csv")
    assert len(df_kurniawan) == 1772

    df_saragih = pd.read_csv(RAW_DIR / "raw_sms_spam_saragih2024.csv")
    assert len(df_saragih) == 690


def test_scraped_official_tax_sources_valid() -> None:
    scraped_json = json.loads(
        (RAW_DIR / "scraped_official_tax_sources.json").read_text(encoding="utf-8")
    )
    df_summary = pd.read_csv(RAW_DIR / "scraped_official_tax_sources_summary.csv")
    assert len(scraped_json) == 68
    assert len(df_summary) == 68
    for item in scraped_json:
        assert item["url"].startswith("http")
        assert item["jumlah_karakter_bersih"] > 200
        assert len(item["sha256_konten"]) == 64


def test_curated_tax_dataset_balance_and_provenance() -> None:
    df_tax = pd.read_csv(DATA_DIR / "dataset_pajak_curated.csv")
    assert len(df_tax) == 260
    assert (df_tax["label"] == 1).sum() == 130
    assert (df_tax["label"] == 0).sum() == 130
    assert not df_tax.isna().any().any()
    assert not df_tax["Teks"].duplicated().any()
    for _, row in df_tax.iterrows():
        assert row["id_sumber"] in SOURCE_METADATA
        assert row["url_sumber"].startswith("https://")


def test_processed_combined_datasets() -> None:
    df_primary = pd.read_csv(PROCESSED_DIR / "dataset_gabungan_utama_biner.csv")
    assert len(df_primary) == 1164
    assert set(df_primary["label"].unique()) == {0, 1}
    assert (df_primary["label"] == 1).sum() == 465
    assert (df_primary["label"] == 0).sum() == 699
    assert not df_primary["clean_text"].isna().any()

    df_ext = pd.read_csv(PROCESSED_DIR / "dataset_gabungan_diperluas_biner.csv")
    assert len(df_ext) == 2521
    assert set(df_ext["label"].unique()) == {0, 1}
    assert not df_ext["clean_text"].duplicated().any()


def test_provenance_catalog_sha256_matches_files() -> None:
    df_cat = pd.read_csv(PROCESSED_DIR / "katalog_asal_sumber_data.csv")
    assert len(df_cat) == 10
    for _, row in df_cat.iterrows():
        file_path = ROOT_DIR / row["nama_file"]
        assert file_path.exists()
        actual_sha = hashlib.sha256(file_path.read_bytes()).hexdigest()
        assert actual_sha == row["sha256"]
