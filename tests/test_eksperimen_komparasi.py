import json
import os
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import pytest
from sklearn.pipeline import Pipeline

from ml.eksperimen_baseline import clean_text
from ml.eksperimen_komparasi import (
    EVALUATION_DIR,
    MODEL_PATH,
    _make_calibrated_svm_pipeline,
    load_datasets,
    run_all_experiments,
)

ROOT_DIR = Path(__file__).resolve().parent.parent

EXPECTED_EVAL_FILES = (
    "json/ringkasan_eksperimen_lengkap.json",
    "csv/tabel_komparasi_utama.csv",
    "csv/hasil_gridsearch_10fold.csv",
    "csv/studi_ablatif_fitur.csv",
    "csv/fitur_teratas_svm_vs_rf.csv",
    "csv/shap_fitur_teratas_svm_vs_rf.csv",
    "csv/analisis_kesalahan_prediksi.csv",
    "laporan/laporan-hasil-eksperimen-komparasi.md",
)

EXPECTED_PLOT_FILES = (
    "gambar/Gambar_Evaluasi_1_Confusion_Matrix_Komparasi.png",
    "gambar/Gambar_Evaluasi_2_Kurva_ROC_dan_PR.png",
    "gambar/Gambar_Evaluasi_3_Kalibrasi_Probabilitas_Platt.png",
    "gambar/Gambar_Evaluasi_4_Bobot_Fitur_Teratas.png",
    "gambar/Gambar_Evaluasi_5_Komparasi_Lintas_Korpus.png",
    "gambar/Gambar_Evaluasi_6_SHAP_Komparasi.png",
)


@pytest.fixture(scope="module")
def experiment_results() -> dict:
    summary_path = EVALUATION_DIR / "json" / "ringkasan_eksperimen_lengkap.json"
    force_fresh = os.environ.get("RUN_FRESH_EXPERIMENTS") == "1"
    if not force_fresh and summary_path.is_file() and MODEL_PATH.is_file():
        return json.loads(summary_path.read_text(encoding="utf-8"))
    return run_all_experiments(save_outputs=True)


def test_load_datasets_deduplicates_and_pipeline_calibration() -> None:
    df_primary, df_extended, df_tax = load_datasets()
    assert len(df_primary) == 1159
    assert df_primary.attrs["raw_rows"] == 1164
    assert df_primary.attrs["duplicates_removed"] == 5
    assert not df_primary["teks_sastrawi"].duplicated().any()

    assert len(df_extended) == 2519
    assert not df_extended["teks_sastrawi"].duplicated().any()
    assert len(df_tax) == 260
    assert not df_tax["teks_sastrawi"].duplicated().any()

    cal = _make_calibrated_svm_pipeline({"C": 2.0, "class_weight": None})
    assert isinstance(cal.estimator, Pipeline)
    assert list(cal.estimator.named_steps.keys()) == ["tfidf", "svm"]


def test_baseline_reproduction_matches_locked_metrics(experiment_results: dict) -> None:
    baseline = experiment_results["baseline"]
    svm = baseline["svm_linear"]
    rf = baseline["random_forest"]

    assert svm["n_samples"] == 232
    assert round(svm["accuracy"], 4) == 0.9612
    assert svm["tn"] == 138
    assert svm["fp"] == 2
    assert svm["fn"] == 7
    assert svm["tp"] == 85
    assert round(rf["accuracy"], 4) == 0.9612


def test_multistage_sections_and_calibration_validity(experiment_results: dict) -> None:
    for key in (
        "cv_10fold",
        "tuning",
        "calibration",
        "ablation",
        "tax_subset",
        "external_cross_corpus",
        "extended_2521",
        "shap_top_features",
    ):
        assert key in experiment_results
        assert experiment_results[key]

    calibration = experiment_results["calibration"]
    svm_cal = calibration["svm_calibrated"]
    assert svm_cal["brier_score"] < 0.05
    assert 0.0 <= svm_cal["specificity"] <= 1.0

    mcnemar = calibration["mcnemar"]
    assert mcnemar["discordant_total"] == mcnemar["svm_correct_rf_error"] + mcnemar["svm_error_rf_correct"]
    assert 0.0 <= mcnemar["p_value_exact_two_sided"] <= 1.0

    boot = calibration["bootstrap_95ci"]
    assert boot["n_bootstrap"] == 2000
    assert boot["svm_calibrated_accuracy"][0] <= svm_cal["accuracy"] <= boot["svm_calibrated_accuracy"][1]

    unc = calibration["uncertainty_band"]
    assert unc["svm_calibrated_count"] < unc["random_forest_count"]

    probas = np.asarray(calibration["holdout_proba_svm_calibrated"])
    assert probas.shape == (232, 2)
    assert np.all((probas >= 0.0) & (probas <= 1.0))
    assert np.allclose(probas.sum(axis=1), 1.0, atol=1e-6)

    ext = experiment_results["external_cross_corpus"]
    assert ext["raw_external_rows"] == 3091
    assert ext["internal_duplicates_removed"] == 1483
    assert ext["overlap_with_primary_removed"] == 248
    assert ext["unseen_external_rows"] == 1360

    tax_s = experiment_results["tax_subset"]
    assert "holdout_general_only_svm_calibrated" in tax_s
    assert "holdout_general_only_random_forest" in tax_s
    assert tax_s["holdout_svm_calibrated"]["accuracy"] > tax_s["holdout_general_only_svm_calibrated"]["accuracy"]


def test_expected_artifacts_and_plots_exist(experiment_results: dict) -> None:
    assert EVALUATION_DIR == ROOT_DIR / "05-hasil-evaluasi"

    for filename in EXPECTED_EVAL_FILES:
        file_path = EVALUATION_DIR / filename
        assert file_path.is_file(), f"File hasil tidak ditemukan: {file_path}"
        assert file_path.stat().st_size > 0

    for filename in EXPECTED_PLOT_FILES:
        plot_path = EVALUATION_DIR / filename
        assert plot_path.is_file(), f"Plot tidak ditemukan: {plot_path}"
        assert plot_path.stat().st_size > 20_000

    assert MODEL_PATH.is_file()

    df_tbl = pd.read_csv(EVALUATION_DIR / "csv" / "tabel_komparasi_utama.csv")
    row_cal = df_tbl[
        (df_tbl["tahap_evaluasi"] == "Tahap 3: Holdout Tuned & Kalibrasi")
        & (df_tbl["model"] == "SVM Linear (Platt Sigmoid)")
    ].iloc[0]
    assert row_cal["accuracy"] == round(experiment_results["calibration"]["svm_calibrated"]["accuracy"], 4)

    df_err = pd.read_csv(EVALUATION_DIR / "csv" / "analisis_kesalahan_prediksi.csv")
    assert len(df_err) == experiment_results["error_analysis_count"]

    df_shap = pd.read_csv(EVALUATION_DIR / "csv" / "shap_fitur_teratas_svm_vs_rf.csv")
    svm_nama1 = df_shap[(df_shap["model"] == "SVM_Linear_SHAP") & (df_shap["fitur"] == "nama1")]
    assert not svm_nama1.empty
    assert svm_nama1.iloc[0]["arah_dominan"] == "Resmi/Normal"
    rf_no = df_shap[(df_shap["model"] == "Random_Forest_SHAP") & (df_shap["fitur"] == "no")]
    assert not rf_no.empty
    assert rf_no.iloc[0]["arah_dominan"] == "Phishing"


def test_exported_joblib_bundle_predicts_tax_phishing_and_official_messages(experiment_results: dict) -> None:
    bundle = joblib.load(MODEL_PATH)
    for key in ("vectorizer", "svm_linear", "svm_calibrated", "random_forest", "metadata"):
        assert key in bundle

    phishing_msg = (
        "Yth Wajib Pajak, NPWP Anda terindikasi selisih SPT Tahunan. "
        "Segera unduh SuratPemberitahuanPajak.apk dan konfirmasi melalui http://djp-verifikasi.my.id"
    )
    official_msg = (
        "Pengingat resmi Direktorat Jenderal Pajak: batas akhir pelaporan SPT Tahunan Orang Pribadi "
        "adalah 31 Maret melalui laman resmi pajak.go.id tanpa biaya apa pun."
    )

    vec = bundle["vectorizer"]
    cal_svm = bundle["svm_calibrated"]
    assert isinstance(cal_svm.estimator, Pipeline)

    clean_phishing = clean_text(phishing_msg)
    pred_phishing = int(cal_svm.predict([clean_phishing])[0])
    prob_phishing = float(cal_svm.predict_proba([clean_phishing])[0, 1])

    clean_official = clean_text(official_msg)
    pred_official = int(cal_svm.predict([clean_official])[0])
    prob_official = float(cal_svm.predict_proba([clean_official])[0, 1])

    assert pred_phishing == 1
    assert prob_phishing > 0.80
    assert pred_official == 0
    assert prob_official < 0.20

    assert vec.transform([clean_phishing]).shape[1] == 3000
