import json
from pathlib import Path

import joblib
import numpy as np
import pytest

from src.eksperimen_baseline import clean_text
from src.eksperimen_komparasi import EVALUATION_DIR, MODEL_PATH, run_all_experiments

ROOT_DIR = Path(__file__).resolve().parent.parent

EXPECTED_EVAL_FILES = (
    "ringkasan_eksperimen_lengkap.json",
    "tabel_komparasi_utama.csv",
    "hasil_gridsearch_10fold.csv",
    "studi_ablatif_fitur.csv",
    "fitur_teratas_svm_vs_rf.csv",
    "analisis_kesalahan_prediksi.csv",
    "Laporan Hasil Eksperimen Komparasi.md",
)

EXPECTED_PLOT_FILES = (
    "Gambar_Evaluasi_1_Confusion_Matrix_Komparasi.png",
    "Gambar_Evaluasi_2_Kurva_ROC_dan_PR.png",
    "Gambar_Evaluasi_3_Kalibrasi_Probabilitas_Platt.png",
    "Gambar_Evaluasi_4_Bobot_Fitur_Teratas.png",
    "Gambar_Evaluasi_5_Komparasi_Lintas_Korpus.png",
)


@pytest.fixture(scope="module")
def experiment_results() -> dict:
    summary_path = EVALUATION_DIR / "ringkasan_eksperimen_lengkap.json"
    if summary_path.is_file() and MODEL_PATH.is_file():
        return json.loads(summary_path.read_text(encoding="utf-8"))
    return run_all_experiments(save_outputs=True)


def test_baseline_reproduction_matches_locked_metrics(experiment_results: dict) -> None:
    baseline = experiment_results["baseline"]
    svm = baseline["svm_linear"]
    rf = baseline["random_forest"]

    assert round(svm["accuracy"], 4) == 0.9828
    assert svm["tn"] == 138
    assert svm["fp"] == 2
    assert svm["fn"] == 2
    assert svm["tp"] == 91
    assert round(rf["accuracy"], 4) == 0.9528


def test_multistage_sections_and_calibration_validity(experiment_results: dict) -> None:
    for key in ("cv_10fold", "tuning", "calibration", "ablation", "tax_subset", "external_cross_corpus", "extended_2521"):
        assert key in experiment_results
        assert experiment_results[key]

    calibration = experiment_results["calibration"]
    svm_cal = calibration["svm_calibrated"]
    assert svm_cal["brier_score"] < 0.05

    probas = np.asarray(calibration["holdout_proba_svm_calibrated"])
    assert probas.shape == (233, 2)
    assert np.all((probas >= 0.0) & (probas <= 1.0))
    assert np.allclose(probas.sum(axis=1), 1.0, atol=1e-6)


def test_expected_artifacts_and_plots_exist(experiment_results: dict) -> None:
    assert EVALUATION_DIR == ROOT_DIR / "05 Hasil Evaluasi"

    for filename in EXPECTED_EVAL_FILES:
        file_path = EVALUATION_DIR / filename
        assert file_path.is_file(), f"File hasil tidak ditemukan: {file_path}"
        assert file_path.stat().st_size > 0

    for filename in EXPECTED_PLOT_FILES:
        plot_path = EVALUATION_DIR / filename
        assert plot_path.is_file(), f"Plot tidak ditemukan: {plot_path}"
        assert plot_path.stat().st_size > 20_000

    assert MODEL_PATH.is_file()


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

    x_phishing = vec.transform([clean_text(phishing_msg)])
    pred_phishing = int(cal_svm.predict(x_phishing)[0])
    prob_phishing = float(cal_svm.predict_proba(x_phishing)[0, 1])

    x_official = vec.transform([clean_text(official_msg)])
    pred_official = int(cal_svm.predict(x_official)[0])
    prob_official = float(cal_svm.predict_proba(x_official)[0, 1])

    assert pred_phishing == 1
    assert prob_phishing > 0.80
    assert pred_official == 0
    assert prob_official < 0.20
