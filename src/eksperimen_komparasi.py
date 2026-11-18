from __future__ import annotations

import json
import os
import re
import time
from collections.abc import Callable
from itertools import product
from pathlib import Path
from typing import Any

import joblib
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import shap
from sklearn.calibration import CalibratedClassifierCV, calibration_curve
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    brier_score_loss,
    confusion_matrix,
    f1_score,
    log_loss,
    precision_recall_curve,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.svm import LinearSVC

from src.eksperimen_baseline import STEM_WORD, STOP_WORDS, URL_PATTERN, clean_text

ROOT_DIR = Path(__file__).resolve().parent.parent
PRIMARY_CORPUS_PATH = (
    ROOT_DIR / "04 Dataset" / "02 Data Olahan" / "Dataset Gabungan Utama Biner 1164 Baris.csv"
)
EXTENDED_CORPUS_PATH = (
    ROOT_DIR / "04 Dataset" / "02 Data Olahan" / "Dataset Gabungan Diperluas Biner 2521 Baris.csv"
)
TAX_CORPUS_PATH = (
    ROOT_DIR / "04 Dataset" / "02 Data Olahan" / "Dataset Pajak Terkurasi 260 Baris.csv"
)
EVALUATION_DIR = ROOT_DIR / "05 Hasil Evaluasi"
PROTOTYPE_DIR = ROOT_DIR / "06 Prototipe Aplikasi"
MODEL_PATH = PROTOTYPE_DIR / "model_phishing_pajak.joblib"

APK_PATTERN = re.compile(r"\b[a-z0-9_.-]+\.apk\b")
RANDOM_STATE = 42
CV_SPLITS = 10

sns.set_theme(style="whitegrid", font_scale=0.95)
plt.rcParams.update(
    {
        "figure.dpi": 300,
        "savefig.dpi": 300,
        "axes.edgecolor": "#cbd5e1",
        "axes.linewidth": 0.8,
        "grid.alpha": 0.35,
    }
)


def clean_text_without_entity_tokens(text: str) -> str:
    """Praproses teks Sastrawi tanpa menyisipkan token_apk atau token_url (untuk studi ablatif)."""
    if not isinstance(text, str):
        return ""
    lowered = text.lower()
    without_url = URL_PATTERN.sub(" ", lowered)
    without_apk = APK_PATTERN.sub(" ", without_url)
    only_letters = re.sub(r"[^a-z\s]", " ", without_apk)
    tokens = [word for word in only_letters.split() if word not in STOP_WORDS]
    return " ".join(STEM_WORD(token) for token in tokens)


def load_datasets() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Muat korpus utama (1.164), diperluas (2.521), dan pajak (260) beserta kolom Sastrawi."""
    df_primary = pd.read_csv(PRIMARY_CORPUS_PATH)
    df_primary["teks_sastrawi"] = df_primary["Teks"].fillna("").astype(str).apply(clean_text)
    df_primary["teks_tanpa_token_entitas"] = (
        df_primary["Teks"].fillna("").astype(str).apply(clean_text_without_entity_tokens)
    )

    df_extended = pd.read_csv(EXTENDED_CORPUS_PATH)
    df_extended["teks_sastrawi"] = df_extended["Teks"].fillna("").astype(str).apply(clean_text)

    df_tax = pd.read_csv(TAX_CORPUS_PATH)
    df_tax["teks_sastrawi"] = df_tax["Teks"].fillna("").astype(str).apply(clean_text)
    return df_primary, df_extended, df_tax


def _compute_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_prob: np.ndarray | None = None,
    y_score: np.ndarray | None = None,
) -> dict[str, Any]:
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    metrics: dict[str, Any] = {
        "n_samples": len(y_true),
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision": float(precision_score(y_true, y_pred, zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, zero_division=0)),
        "f1": float(f1_score(y_true, y_pred, zero_division=0)),
        "f1_macro": float(f1_score(y_true, y_pred, average="macro", zero_division=0)),
        "tn": int(tn),
        "fp": int(fp),
        "fn": int(fn),
        "tp": int(tp),
        "roc_auc": None,
        "pr_auc": None,
        "brier_score": None,
        "log_loss": None,
    }

    has_both_classes = len(np.unique(y_true)) == 2
    if y_prob is not None:
        if has_both_classes:
            metrics["roc_auc"] = float(roc_auc_score(y_true, y_prob))
            metrics["pr_auc"] = float(average_precision_score(y_true, y_prob))
        metrics["brier_score"] = float(brier_score_loss(y_true, y_prob))
        metrics["log_loss"] = float(log_loss(y_true, np.clip(y_prob, 1e-15, 1 - 1e-15), labels=[0, 1]))
    elif y_score is not None and has_both_classes:
        metrics["roc_auc"] = float(roc_auc_score(y_true, y_score))
        metrics["pr_auc"] = float(average_precision_score(y_true, y_score))

    return metrics


def _precompute_tfidf_folds(
    texts: pd.Series,
    labels: np.ndarray,
    cv: StratifiedKFold,
    ngram_range: tuple[int, int] = (1, 2),
    max_features: int = 3000,
) -> list[tuple[Any, np.ndarray, Any, np.ndarray]]:
    """Bangun matriks TF-IDF terisolasi per fold di memori untuk mencegah kebocoran data."""
    y_arr = np.asarray(labels)
    folds = []
    for tr_idx, val_idx in cv.split(texts, y_arr):
        vec = TfidfVectorizer(ngram_range=ngram_range, max_features=max_features)
        x_tr_tf = vec.fit_transform(texts.iloc[tr_idx])
        x_val_tf = vec.transform(texts.iloc[val_idx])
        folds.append((x_tr_tf, y_arr[tr_idx], x_val_tf, y_arr[val_idx]))
    return folds


def _evaluate_cv_folds(
    folds: list[tuple[Any, np.ndarray, Any, np.ndarray]],
    clf_factory: Callable[[], Any],
    return_train_f1: bool = False,
) -> dict[str, float]:
    """Evaluasi model pada daftar fold TF-IDF yang sudah diprakomputasi di memori."""
    acc_scores: list[float] = []
    prec_scores: list[float] = []
    rec_scores: list[float] = []
    f1_scores: list[float] = []
    f1_macro_scores: list[float] = []
    auc_scores: list[float] = []
    train_f1_scores: list[float] = []
    fit_times: list[float] = []

    for x_tr_tf, y_tr, x_val_tf, y_val in folds:
        t0 = time.perf_counter()
        clf = clf_factory()
        clf.fit(x_tr_tf, y_tr)
        fit_times.append(time.perf_counter() - t0)

        y_pred = clf.predict(x_val_tf)
        y_score = (
            clf.predict_proba(x_val_tf)[:, 1]
            if hasattr(clf, "predict_proba")
            else clf.decision_function(x_val_tf)
        )

        acc_scores.append(float(accuracy_score(y_val, y_pred)))
        prec_scores.append(float(precision_score(y_val, y_pred, zero_division=0)))
        rec_scores.append(float(recall_score(y_val, y_pred, zero_division=0)))
        f1_scores.append(float(f1_score(y_val, y_pred, zero_division=0)))
        f1_macro_scores.append(float(f1_score(y_val, y_pred, average="macro", zero_division=0)))
        if len(np.unique(y_val)) == 2:
            auc_scores.append(float(roc_auc_score(y_val, y_score)))
        if return_train_f1:
            train_pred = clf.predict(x_tr_tf)
            train_f1_scores.append(float(f1_score(y_tr, train_pred, zero_division=0)))

    ddof = 1 if len(acc_scores) > 1 else 0
    return {
        "accuracy_mean": float(np.mean(acc_scores)),
        "accuracy_std": float(np.std(acc_scores, ddof=ddof)),
        "precision_mean": float(np.mean(prec_scores)),
        "precision_std": float(np.std(prec_scores, ddof=ddof)),
        "recall_mean": float(np.mean(rec_scores)),
        "recall_std": float(np.std(rec_scores, ddof=ddof)),
        "f1_mean": float(np.mean(f1_scores)),
        "f1_std": float(np.std(f1_scores, ddof=ddof)),
        "f1_macro_mean": float(np.mean(f1_macro_scores)),
        "f1_macro_std": float(np.std(f1_macro_scores, ddof=ddof)),
        "roc_auc_mean": float(np.mean(auc_scores)) if auc_scores else 0.0,
        "roc_auc_std": float(np.std(auc_scores, ddof=ddof)) if len(auc_scores) > 1 else 0.0,
        "mean_train_f1": float(np.mean(train_f1_scores)) if train_f1_scores else 0.0,
        "mean_fit_time_sec": float(np.mean(fit_times)),
    }


def _run_grid_over_folds(
    folds: list[tuple[Any, np.ndarray, Any, np.ndarray]],
    model_label: str,
    param_grid: dict[str, list[Any]],
    clf_builder: Callable[[dict[str, Any]], Any],
) -> tuple[dict[str, Any], dict[str, float], pd.DataFrame]:
    """Lakukan pencarian grid pada fold terpraproses dan urutkan berdasarkan F1 rata-rata."""
    param_names = list(param_grid.keys())
    candidates: list[dict[str, Any]] = []
    for combo in product(*param_grid.values()):
        params = dict(zip(param_names, combo, strict=True))
        cv_summary = _evaluate_cv_folds(
            folds, lambda p=params: clf_builder(p), return_train_f1=True
        )
        candidates.append({"params": params, "summary": cv_summary})

    candidates.sort(
        key=lambda item: (
            item["summary"]["f1_mean"],
            item["summary"]["accuracy_mean"],
            item["summary"]["roc_auc_mean"],
        ),
        reverse=True,
    )

    rows = []
    for rank, item in enumerate(candidates, start=1):
        s = item["summary"]
        rows.append(
            {
                "model": model_label,
                "rank_test_f1": rank,
                "params": json.dumps(item["params"], sort_keys=True),
                "mean_test_f1": s["f1_mean"],
                "std_test_f1": s["f1_std"],
                "mean_test_accuracy": s["accuracy_mean"],
                "std_test_accuracy": s["accuracy_std"],
                "mean_test_precision": s["precision_mean"],
                "mean_test_recall": s["recall_mean"],
                "mean_test_f1_macro": s["f1_macro_mean"],
                "mean_test_roc_auc": s["roc_auc_mean"],
                "mean_train_f1": s["mean_train_f1"],
                "mean_fit_time_sec": s["mean_fit_time_sec"],
            }
        )

    best_candidate = candidates[0]
    return best_candidate["params"], best_candidate["summary"], pd.DataFrame(rows)


def _run_stage1_baseline(
    df_primary: pd.DataFrame,
    idx_train: np.ndarray,
    idx_test: np.ndarray,
    folds_train: list[tuple[Any, np.ndarray, Any, np.ndarray]],
) -> dict[str, Any]:
    """Reproduksi baseline holdout 80:20 dan evaluasi 10-Fold Stratified CV default."""
    x_train = df_primary.loc[idx_train, "teks_sastrawi"]
    x_test = df_primary.loc[idx_test, "teks_sastrawi"]
    y_train = df_primary.loc[idx_train, "label"].to_numpy()
    y_test = df_primary.loc[idx_test, "label"].to_numpy()

    vec = TfidfVectorizer(ngram_range=(1, 2), max_features=3000)
    x_train_tf = vec.fit_transform(x_train)
    x_test_tf = vec.transform(x_test)

    svm_base = LinearSVC(random_state=RANDOM_STATE)
    svm_base.fit(x_train_tf, y_train)
    svm_pred = svm_base.predict(x_test_tf)
    svm_score = svm_base.decision_function(x_test_tf)

    rf_base = RandomForestClassifier(n_estimators=200, random_state=RANDOM_STATE)
    rf_base.fit(x_train_tf, y_train)
    rf_pred = rf_base.predict(x_test_tf)
    rf_prob = rf_base.predict_proba(x_test_tf)[:, 1]

    svm_cv = _evaluate_cv_folds(folds_train, lambda: LinearSVC(random_state=RANDOM_STATE))
    rf_cv = _evaluate_cv_folds(
        folds_train, lambda: RandomForestClassifier(n_estimators=200, random_state=RANDOM_STATE)
    )

    return {
        "svm_linear": _compute_metrics(y_test, svm_pred, y_score=svm_score),
        "random_forest": _compute_metrics(y_test, rf_pred, y_prob=rf_prob),
        "cv_10fold_default": {"svm_linear": svm_cv, "random_forest": rf_cv},
        "holdout_pred_svm_baseline": svm_pred,
    }


def _run_stage2_and_3_tuning_calibration(
    df_primary: pd.DataFrame,
    idx_train: np.ndarray,
    idx_test: np.ndarray,
    folds_train: list[tuple[Any, np.ndarray, Any, np.ndarray]],
) -> dict[str, Any]:
    """Jalankan GridSearch 10-Fold pada 931 data latih dan kalibrasi Platt pada LinearSVC."""
    x_train = df_primary.loc[idx_train, "teks_sastrawi"]
    x_test = df_primary.loc[idx_test, "teks_sastrawi"]
    y_train = df_primary.loc[idx_train, "label"].to_numpy()
    y_test = df_primary.loc[idx_test, "label"].to_numpy()

    svm_best_params, svm_cv_summary, svm_grid_df = _run_grid_over_folds(
        folds_train,
        "SVM_Linear",
        {"C": [0.1, 0.25, 0.5, 1.0, 2.0, 5.0], "class_weight": [None, "balanced"]},
        lambda p: LinearSVC(random_state=RANDOM_STATE, max_iter=5000, **p),
    )
    rf_best_params, rf_cv_summary, rf_grid_df = _run_grid_over_folds(
        folds_train,
        "Random_Forest",
        {
            "n_estimators": [100, 200, 300],
            "max_depth": [None, 30],
            "min_samples_split": [2, 5],
            "class_weight": [None, "balanced"],
        },
        lambda p: RandomForestClassifier(random_state=RANDOM_STATE, **p),
    )
    grid_df = pd.concat([svm_grid_df, rf_grid_df], ignore_index=True)

    vec_main = TfidfVectorizer(ngram_range=(1, 2), max_features=3000)
    x_train_tf = vec_main.fit_transform(x_train)
    x_test_tf = vec_main.transform(x_test)

    svm_tuned = LinearSVC(random_state=RANDOM_STATE, max_iter=5000, **svm_best_params)
    svm_tuned.fit(x_train_tf, y_train)
    svm_tuned_pred = svm_tuned.predict(x_test_tf)
    svm_tuned_score = svm_tuned.decision_function(x_test_tf)

    svm_calibrated = CalibratedClassifierCV(
        estimator=LinearSVC(random_state=RANDOM_STATE, max_iter=5000, **svm_best_params),
        method="sigmoid",
        cv=5,
    )
    svm_calibrated.fit(x_train_tf, y_train)
    cal_pred = svm_calibrated.predict(x_test_tf)
    cal_proba_all = svm_calibrated.predict_proba(x_test_tf)
    cal_proba = cal_proba_all[:, 1]

    rf_tuned = RandomForestClassifier(random_state=RANDOM_STATE, **rf_best_params)
    rf_tuned.fit(x_train_tf, y_train)
    rf_tuned_pred = rf_tuned.predict(x_test_tf)
    rf_tuned_proba = rf_tuned.predict_proba(x_test_tf)[:, 1]

    return {
        "best_params": {"svm_linear": svm_best_params, "random_forest": rf_best_params},
        "cv_10fold_tuned": {"svm_linear": svm_cv_summary, "random_forest": rf_cv_summary},
        "holdout_tuned": {
            "svm_linear": _compute_metrics(y_test, svm_tuned_pred, y_score=svm_tuned_score),
            "svm_calibrated": _compute_metrics(y_test, cal_pred, y_prob=cal_proba),
            "random_forest": _compute_metrics(y_test, rf_tuned_pred, y_prob=rf_tuned_proba),
        },
        "grid_df": grid_df,
        "models_holdout": {
            "vectorizer": vec_main,
            "svm_tuned": svm_tuned,
            "svm_calibrated": svm_calibrated,
            "rf_tuned": rf_tuned,
            "x_train_tf": x_train_tf,
            "x_test_tf": x_test_tf,
        },
        "holdout_arrays": {
            "y_test": y_test,
            "pred_svm_calibrated": cal_pred,
            "proba_svm_calibrated_matrix": cal_proba_all,
            "proba_svm_calibrated": cal_proba,
            "pred_rf_tuned": rf_tuned_pred,
            "proba_rf_tuned": rf_tuned_proba,
        },
    }


def _run_ablation_study(
    df_primary: pd.DataFrame,
    idx_train: np.ndarray,
    idx_test: np.ndarray,
    svm_best_params: dict[str, Any],
    rf_best_params: dict[str, Any],
) -> pd.DataFrame:
    """Bandingkan 6 skenario praproses dan TF-IDF secara adil pada 10-Fold CV dan holdout."""
    configs = [
        ("1_Tanpa_Token_Entitas", "teks_tanpa_token_entitas", (1, 2), 3000),
        ("2_Tanpa_Sastrawi", "clean_text", (1, 2), 3000),
        ("3_Unigram_Saja", "teks_sastrawi", (1, 1), 3000),
        ("4_Utama_MaxFeatures_1500", "teks_sastrawi", (1, 2), 1500),
        ("5_Konfigurasi_Utama_3000", "teks_sastrawi", (1, 2), 3000),
        ("6_Utama_MaxFeatures_5000", "teks_sastrawi", (1, 2), 5000),
    ]

    cv = StratifiedKFold(n_splits=CV_SPLITS, shuffle=True, random_state=RANDOM_STATE)
    y_train = df_primary.loc[idx_train, "label"].to_numpy()
    y_test = df_primary.loc[idx_test, "label"].to_numpy()
    rows = []

    for config_name, col_name, ngram_range, max_features in configs:
        x_train = df_primary.loc[idx_train, col_name].fillna("").astype(str)
        x_test = df_primary.loc[idx_test, col_name].fillna("").astype(str)

        folds_cfg = _precompute_tfidf_folds(
            x_train, y_train, cv, ngram_range=ngram_range, max_features=max_features
        )
        vec = TfidfVectorizer(ngram_range=ngram_range, max_features=max_features)
        x_train_tf = vec.fit_transform(x_train)
        x_test_tf = vec.transform(x_test)
        actual_vocab = len(vec.vocabulary_)

        for model_name, clf_factory in (
            (
                "SVM_Linear",
                lambda: LinearSVC(random_state=RANDOM_STATE, max_iter=5000, **svm_best_params),
            ),
            (
                "Random_Forest",
                lambda: RandomForestClassifier(random_state=RANDOM_STATE, **rf_best_params),
            ),
        ):
            cv_res = _evaluate_cv_folds(folds_cfg, clf_factory)
            model = clf_factory()
            model.fit(x_train_tf, y_train)
            y_pred = model.predict(x_test_tf)
            holdout_m = _compute_metrics(y_test, y_pred)

            rows.append(
                {
                    "konfigurasi": config_name,
                    "kolom_teks": col_name,
                    "ngram_range": str(ngram_range),
                    "max_features": max_features,
                    "vocab_aktual": actual_vocab,
                    "model": model_name,
                    "cv10_accuracy_mean": cv_res["accuracy_mean"],
                    "cv10_f1_mean": cv_res["f1_mean"],
                    "cv10_f1_std": cv_res["f1_std"],
                    "holdout_accuracy": holdout_m["accuracy"],
                    "holdout_precision": holdout_m["precision"],
                    "holdout_recall": holdout_m["recall"],
                    "holdout_f1": holdout_m["f1"],
                    "holdout_f1_macro": holdout_m["f1_macro"],
                }
            )

    return pd.DataFrame(rows)


def _run_stage4_domain_and_cross_corpus(
    df_primary: pd.DataFrame,
    df_extended: pd.DataFrame,
    df_tax: pd.DataFrame,
    idx_test: np.ndarray,
    stage2_3: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Evaluasi bias kata kunci pajak, zero-shot eksternal, dan korpus diperluas 2.521 baris."""
    svm_best_params = stage2_3["best_params"]["svm_linear"]
    rf_best_params = stage2_3["best_params"]["random_forest"]
    holdout_arr = stage2_3["holdout_arrays"]

    # Stage 4A: Subset Korpus_Pajak_Terverifikasi pada holdout 233 + CV 10-fold pada 260 baris pajak
    df_test = df_primary.loc[idx_test].copy()
    tax_mask = (df_test["sumber"] == "Korpus_Pajak_Terverifikasi").to_numpy()
    y_test_tax = holdout_arr["y_test"][tax_mask]

    tax_holdout_svm = _compute_metrics(
        y_test_tax,
        holdout_arr["pred_svm_calibrated"][tax_mask],
        y_prob=holdout_arr["proba_svm_calibrated"][tax_mask],
    )
    tax_holdout_rf = _compute_metrics(
        y_test_tax,
        holdout_arr["pred_rf_tuned"][tax_mask],
        y_prob=holdout_arr["proba_rf_tuned"][tax_mask],
    )

    cv = StratifiedKFold(n_splits=CV_SPLITS, shuffle=True, random_state=RANDOM_STATE)
    x_tax = df_tax["teks_sastrawi"]
    y_tax = df_tax["label"].to_numpy()
    tax_folds = _precompute_tfidf_folds(x_tax, y_tax, cv, ngram_range=(1, 2), max_features=3000)

    tax_cv_svm = _evaluate_cv_folds(
        tax_folds, lambda: LinearSVC(random_state=RANDOM_STATE, max_iter=5000, **svm_best_params)
    )
    tax_cv_rf = _evaluate_cv_folds(
        tax_folds, lambda: RandomForestClassifier(random_state=RANDOM_STATE, **rf_best_params)
    )

    # Fit model produksi pada seluruh 1.164 baris korpus utama (untuk Stage 4B & ekspor joblib)
    vec_full = TfidfVectorizer(ngram_range=(1, 2), max_features=3000)
    x_full_tf = vec_full.fit_transform(df_primary["teks_sastrawi"])
    y_full = df_primary["label"].to_numpy()

    svm_full_linear = LinearSVC(random_state=RANDOM_STATE, max_iter=5000, **svm_best_params)
    svm_full_linear.fit(x_full_tf, y_full)

    svm_full_cal = CalibratedClassifierCV(
        estimator=LinearSVC(random_state=RANDOM_STATE, max_iter=5000, **svm_best_params),
        method="sigmoid",
        cv=5,
    )
    svm_full_cal.fit(x_full_tf, y_full)

    rf_full = RandomForestClassifier(random_state=RANDOM_STATE, **rf_best_params)
    rf_full.fit(x_full_tf, y_full)

    # Stage 4B: Uji zero-shot pada sumber eksternal yang belum pernah dilihat model
    external_sources = {"Korpus_Umum_Theodorus2021_IEEE", "Korpus_Umum_Saragih2024"}
    df_ext_raw = df_extended[df_extended["sumber"].isin(external_sources)].copy()
    primary_seen_texts = set(df_primary["teks_sastrawi"])
    df_ext_unseen = df_ext_raw[~df_ext_raw["teks_sastrawi"].isin(primary_seen_texts)].copy()
    overlap_removed = int(len(df_ext_raw) - len(df_ext_unseen))

    x_ext_tf = vec_full.transform(df_ext_unseen["teks_sastrawi"])
    y_ext = df_ext_unseen["label"].to_numpy()

    ext_svm_pred = svm_full_cal.predict(x_ext_tf)
    ext_svm_prob = svm_full_cal.predict_proba(x_ext_tf)[:, 1]
    ext_rf_pred = rf_full.predict(x_ext_tf)
    ext_rf_prob = rf_full.predict_proba(x_ext_tf)[:, 1]

    per_source_ext: dict[str, Any] = {}
    for src_name in sorted(external_sources):
        mask = (df_ext_unseen["sumber"] == src_name).to_numpy()
        per_source_ext[src_name] = {
            "svm_calibrated": _compute_metrics(y_ext[mask], ext_svm_pred[mask], y_prob=ext_svm_prob[mask]),
            "random_forest": _compute_metrics(y_ext[mask], ext_rf_pred[mask], y_prob=ext_rf_prob[mask]),
        }

    # Stage 4C: Evaluasi penuh korpus diperluas 2.521 baris (Holdout 80:20 + 10-Fold CV)
    x_2521 = df_extended["teks_sastrawi"]
    y_2521 = df_extended["label"].to_numpy()
    idx_tr_2521, idx_te_2521 = train_test_split(
        df_extended.index.to_numpy(),
        test_size=0.2,
        random_state=RANDOM_STATE,
        stratify=y_2521,
    )
    vec_2521 = TfidfVectorizer(ngram_range=(1, 2), max_features=3000)
    x_tr_2521_tf = vec_2521.fit_transform(x_2521.loc[idx_tr_2521])
    x_te_2521_tf = vec_2521.transform(x_2521.loc[idx_te_2521])

    svm_2521_cal = CalibratedClassifierCV(
        estimator=LinearSVC(random_state=RANDOM_STATE, max_iter=5000, **svm_best_params),
        method="sigmoid",
        cv=5,
    )
    svm_2521_cal.fit(x_tr_2521_tf, y_2521[idx_tr_2521])
    rf_2521 = RandomForestClassifier(random_state=RANDOM_STATE, **rf_best_params)
    rf_2521.fit(x_tr_2521_tf, y_2521[idx_tr_2521])

    holdout_2521_svm = _compute_metrics(
        y_2521[idx_te_2521],
        svm_2521_cal.predict(x_te_2521_tf),
        y_prob=svm_2521_cal.predict_proba(x_te_2521_tf)[:, 1],
    )
    holdout_2521_rf = _compute_metrics(
        y_2521[idx_te_2521],
        rf_2521.predict(x_te_2521_tf),
        y_prob=rf_2521.predict_proba(x_te_2521_tf)[:, 1],
    )

    ext_folds = _precompute_tfidf_folds(x_2521, y_2521, cv, ngram_range=(1, 2), max_features=3000)
    cv_2521_svm = _evaluate_cv_folds(
        ext_folds, lambda: LinearSVC(random_state=RANDOM_STATE, max_iter=5000, **svm_best_params)
    )
    cv_2521_rf = _evaluate_cv_folds(
        ext_folds, lambda: RandomForestClassifier(random_state=RANDOM_STATE, **rf_best_params)
    )

    stage4_summary = {
        "tax_subset": {
            "holdout_tax_rows": int(tax_mask.sum()),
            "holdout_svm_calibrated": tax_holdout_svm,
            "holdout_random_forest": tax_holdout_rf,
            "cv_10fold_tax_260_svm": tax_cv_svm,
            "cv_10fold_tax_260_rf": tax_cv_rf,
        },
        "external_cross_corpus": {
            "raw_external_rows": len(df_ext_raw),
            "overlap_with_primary_removed": overlap_removed,
            "unseen_external_rows": len(df_ext_unseen),
            "combined_svm_calibrated": _compute_metrics(y_ext, ext_svm_pred, y_prob=ext_svm_prob),
            "combined_random_forest": _compute_metrics(y_ext, ext_rf_pred, y_prob=ext_rf_prob),
            "per_source": per_source_ext,
        },
        "extended_2521": {
            "n_train": len(idx_tr_2521),
            "n_test": len(idx_te_2521),
            "holdout_svm_calibrated": holdout_2521_svm,
            "holdout_random_forest": holdout_2521_rf,
            "cv_10fold_svm": cv_2521_svm,
            "cv_10fold_rf": cv_2521_rf,
        },
    }
    full_models = {
        "vectorizer": vec_full,
        "svm_linear": svm_full_linear,
        "svm_calibrated": svm_full_cal,
        "random_forest": rf_full,
    }
    return stage4_summary, full_models


def _build_feature_and_error_tables(
    df_primary: pd.DataFrame,
    idx_test: np.ndarray,
    stage1: dict[str, Any],
    stage2_3: dict[str, Any],
) -> tuple[pd.DataFrame, pd.DataFrame]:
    models = stage2_3["models_holdout"]
    vec: TfidfVectorizer = models["vectorizer"]
    svm_tuned: LinearSVC = models["svm_tuned"]
    rf_tuned: RandomForestClassifier = models["rf_tuned"]

    feature_names = vec.get_feature_names_out()
    coefs = svm_tuned.coef_.ravel()
    pos_idx = np.argsort(coefs)[::-1][:25]
    neg_idx = np.argsort(coefs)[:25]
    rf_imp = rf_tuned.feature_importances_
    rf_idx = np.argsort(rf_imp)[::-1][:25]

    feature_rows = []
    for rank, i in enumerate(pos_idx, start=1):
        feature_rows.append(
            {"model_kelompok": "SVM_Positif_Phishing", "rank": rank, "fitur": str(feature_names[i]), "skor": float(coefs[i])}
        )
    for rank, i in enumerate(neg_idx, start=1):
        feature_rows.append(
            {"model_kelompok": "SVM_Negatif_Resmi", "rank": rank, "fitur": str(feature_names[i]), "skor": float(coefs[i])}
        )
    for rank, i in enumerate(rf_idx, start=1):
        feature_rows.append(
            {"model_kelompok": "RF_Importance", "rank": rank, "fitur": str(feature_names[i]), "skor": float(rf_imp[i])}
        )
    df_features = pd.DataFrame(feature_rows)

    arr = stage2_3["holdout_arrays"]
    y_test = arr["y_test"]
    pred_svm_base = stage1["holdout_pred_svm_baseline"]
    pred_svm_cal = arr["pred_svm_calibrated"]
    prob_svm_cal = arr["proba_svm_calibrated"]
    pred_rf = arr["pred_rf_tuned"]
    prob_rf = arr["proba_rf_tuned"]

    df_test = df_primary.loc[idx_test].copy()
    df_test["indeks_korpus"] = idx_test
    df_test["label_aktual"] = y_test
    df_test["pred_svm_baseline"] = pred_svm_base
    df_test["pred_svm_calibrated"] = pred_svm_cal
    df_test["prob_svm_calibrated"] = np.round(prob_svm_cal, 6)
    df_test["pred_rf_tuned"] = pred_rf
    df_test["prob_rf_tuned"] = np.round(prob_rf, 6)

    err_svm = df_test["pred_svm_calibrated"] != df_test["label_aktual"]
    err_rf = df_test["pred_rf_tuned"] != df_test["label_aktual"]
    err_base = df_test["pred_svm_baseline"] != df_test["label_aktual"]
    df_err = df_test[err_svm | err_rf | err_base].copy()

    def _label_error_source(row: pd.Series) -> str:
        s_err = row["pred_svm_calibrated"] != row["label_aktual"]
        r_err = row["pred_rf_tuned"] != row["label_aktual"]
        if s_err and r_err:
            return "Keduanya"
        if s_err:
            return "SVM_Terkalibrasi_Saja"
        if r_err:
            return "RF_Tuned_Saja"
        return "SVM_Baseline_Saja"

    df_err["kesalahan_pada"] = df_err.apply(_label_error_source, axis=1)
    cols = [
        "indeks_korpus",
        "sumber",
        "kategori_modus",
        "label_aktual",
        "pred_svm_baseline",
        "pred_svm_calibrated",
        "prob_svm_calibrated",
        "pred_rf_tuned",
        "prob_rf_tuned",
        "kesalahan_pada",
        "Teks",
        "teks_sastrawi",
    ]
    return df_features, df_err[cols].reset_index(drop=True)


def _extract_positive_shap(raw_values: Any) -> np.ndarray:
    """Normalisasi keluaran SHAP biner menjadi matriks 2D untuk kelas positif (Phishing = 1)."""
    if isinstance(raw_values, list):
        return np.asarray(raw_values[1], dtype=float)
    arr = np.asarray(raw_values, dtype=float)
    if arr.ndim == 3:
        return arr[:, :, 1]
    return arr


def _compute_shap_table(stage2_3: dict[str, Any], top_n: int = 20) -> pd.DataFrame:
    """Hitung kontribusi SHAP global pada data holdout untuk SVM Linear dan Random Forest."""
    models = stage2_3["models_holdout"]
    feature_names = models["vectorizer"].get_feature_names_out()
    x_train_tf = models["x_train_tf"]
    x_test_tf = models["x_test_tf"]
    x_test_dense = x_test_tf.toarray()

    svm_masker = shap.maskers.Independent(x_train_tf, max_samples=x_train_tf.shape[0])
    svm_shap = _extract_positive_shap(
        shap.LinearExplainer(models["svm_tuned"], svm_masker).shap_values(x_test_tf)
    )
    rf_background = shap.sample(x_train_tf.toarray(), 100, random_state=RANDOM_STATE)
    rf_shap = _extract_positive_shap(
        shap.TreeExplainer(
            models["rf_tuned"],
            data=rf_background,
            feature_perturbation="interventional",
        ).shap_values(x_test_dense)
    )

    rows: list[dict[str, Any]] = []
    for model_label, shap_matrix in (
        ("SVM_Linear_SHAP", svm_shap),
        ("Random_Forest_SHAP", rf_shap),
    ):
        mean_abs = np.abs(shap_matrix).mean(axis=0)
        mean_signed = shap_matrix.mean(axis=0)
        top_idx = np.argsort(mean_abs)[::-1][:top_n]
        for rank, idx in enumerate(top_idx, start=1):
            signed_val = float(mean_signed[idx])
            rows.append(
                {
                    "model": model_label,
                    "rank": rank,
                    "fitur": str(feature_names[idx]),
                    "mean_abs_shap": float(mean_abs[idx]),
                    "mean_shap_signed": signed_val,
                    "arah_dominan": "Phishing" if signed_val >= 0 else "Resmi/Normal",
                }
            )
    return pd.DataFrame(rows)


def _generate_plots(
    stage2_3: dict[str, Any],
    stage4: dict[str, Any],
    df_features: pd.DataFrame,
    df_shap: pd.DataFrame,
    out_dir: Path,
) -> None:
    arr = stage2_3["holdout_arrays"]
    y_test = arr["y_test"]
    pred_svm = arr["pred_svm_calibrated"]
    prob_svm = arr["proba_svm_calibrated"]
    pred_rf = arr["pred_rf_tuned"]
    prob_rf = arr["proba_rf_tuned"]

    cal_metrics = stage2_3["holdout_tuned"]
    svm_m = cal_metrics["svm_calibrated"]
    rf_m = cal_metrics["random_forest"]

    # Gambar 1: Confusion Matrix Komparasi (Holdout n=233)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.6))
    class_labels = ["Normal / Resmi (0)", "Phishing / Penipuan (1)"]
    for ax, title, y_pred, cmap in (
        (axes[0], f"SVM Linear (Platt) - Akurasi {svm_m['accuracy'] * 100:.2f}%", pred_svm, "Blues"),
        (axes[1], f"Random Forest (Tuned) - Akurasi {rf_m['accuracy'] * 100:.2f}%", pred_rf, "Greens"),
    ):
        cm = confusion_matrix(y_test, y_pred, labels=[0, 1])
        cm_pct = cm / cm.sum(axis=1, keepdims=True) * 100
        annots = np.array([[f"{cm[r, c]}\n({cm_pct[r, c]:.1f}%)" for c in range(2)] for r in range(2)])
        sns.heatmap(
            cm,
            annot=annots,
            fmt="",
            cmap=cmap,
            cbar=False,
            xticklabels=class_labels,
            yticklabels=class_labels,
            annot_kws={"size": 11, "weight": "bold"},
            ax=ax,
        )
        ax.set_title(title, fontsize=11, fontweight="bold", pad=10)
        ax.set_xlabel("Label Prediksi", fontsize=10)
        ax.set_ylabel("Label Aktual", fontsize=10)
    fig.suptitle("Perbandingan Confusion Matrix Uji Holdout (n = 233)", fontsize=12.5, fontweight="bold", y=1.02)
    fig.tight_layout()
    fig.savefig(out_dir / "Gambar_Evaluasi_1_Confusion_Matrix_Komparasi.png", bbox_inches="tight")
    plt.close(fig)

    # Gambar 2: Kurva ROC dan Precision-Recall
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.8))
    fpr_s, tpr_s, _ = roc_curve(y_test, prob_svm)
    fpr_r, tpr_r, _ = roc_curve(y_test, prob_rf)
    axes[0].plot(fpr_s, tpr_s, lw=2.2, color="#1d4ed8", label=f"SVM Linear (AUC = {svm_m['roc_auc']:.4f})")
    axes[0].plot(fpr_r, tpr_r, lw=2.2, color="#059669", linestyle="--", label=f"Random Forest (AUC = {rf_m['roc_auc']:.4f})")
    axes[0].plot([0, 1], [0, 1], lw=1.2, color="#94a3b8", linestyle=":", label="Garis Acak (AUC = 0.5000)")
    axes[0].set_title("Kurva ROC (Receiver Operating Characteristic)", fontsize=11, fontweight="bold")
    axes[0].set_xlabel("False Positive Rate (1 - Spesifisitas)")
    axes[0].set_ylabel("True Positive Rate (Recall)")
    axes[0].legend(loc="lower right")

    prec_s, rec_s, _ = precision_recall_curve(y_test, prob_svm)
    prec_r, rec_r, _ = precision_recall_curve(y_test, prob_rf)
    axes[1].plot(rec_s, prec_s, lw=2.2, color="#1d4ed8", label=f"SVM Linear (PR-AUC = {svm_m['pr_auc']:.4f})")
    axes[1].plot(rec_r, prec_r, lw=2.2, color="#059669", linestyle="--", label=f"Random Forest (PR-AUC = {rf_m['pr_auc']:.4f})")
    axes[1].set_title("Kurva Precision-Recall (Kelas Phishing)", fontsize=11, fontweight="bold")
    axes[1].set_xlabel("Recall (Sensitivitas)")
    axes[1].set_ylabel("Precision (Presisi)")
    axes[1].set_ylim(0.5, 1.03)
    axes[1].legend(loc="lower left")

    fig.suptitle("Evaluasi Diskriminatif Kurva ROC dan Precision-Recall (n = 233)", fontsize=12.5, fontweight="bold", y=1.02)
    fig.tight_layout()
    fig.savefig(out_dir / "Gambar_Evaluasi_2_Kurva_ROC_dan_PR.png", bbox_inches="tight")
    plt.close(fig)

    # Gambar 3: Kalibrasi Probabilitas Platt (Reliability Diagram + Distribusi)
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.8))
    prob_true_s, prob_pred_s = calibration_curve(y_test, prob_svm, n_bins=10, strategy="uniform")
    prob_true_r, prob_pred_r = calibration_curve(y_test, prob_rf, n_bins=10, strategy="uniform")

    axes[0].plot([0, 1], [0, 1], "k:", lw=1.3, label="Kalibrasi Sempurna")
    axes[0].plot(
        prob_pred_s,
        prob_true_s,
        "s-",
        lw=2,
        color="#1d4ed8",
        label=f"SVM Platt (Brier={svm_m['brier_score']:.4f}, LogLoss={svm_m['log_loss']:.4f})",
    )
    axes[0].plot(
        prob_pred_r,
        prob_true_r,
        "o--",
        lw=2,
        color="#059669",
        label=f"RF Tuned (Brier={rf_m['brier_score']:.4f}, LogLoss={rf_m['log_loss']:.4f})",
    )
    axes[0].set_title("Kurva Reliabilitas Probabilitas (10 Bin)", fontsize=11, fontweight="bold")
    axes[0].set_xlabel("Rata-rata Probabilitas Prediksi")
    axes[0].set_ylabel("Proporsi Positif Aktual")
    axes[0].legend(loc="upper left", fontsize=8.5)

    axes[1].hist(prob_svm, bins=15, alpha=0.55, color="#1d4ed8", label="SVM Linear (Platt)", edgecolor="white")
    axes[1].hist(prob_rf, bins=15, alpha=0.55, color="#059669", label="Random Forest (Tuned)", edgecolor="white")
    axes[1].set_title("Distribusi Probabilitas Prediksi (n = 233)", fontsize=11, fontweight="bold")
    axes[1].set_xlabel("Probabilitas Kelas Phishing (P = 1)")
    axes[1].set_ylabel("Jumlah Pesan")
    axes[1].legend(loc="upper center", fontsize=9)

    fig.suptitle("Evaluasi Kalibrasi Probabilitas Model (Platt Scaling vs Random Forest)", fontsize=12.5, fontweight="bold", y=1.02)
    fig.tight_layout()
    fig.savefig(out_dir / "Gambar_Evaluasi_3_Kalibrasi_Probabilitas_Platt.png", bbox_inches="tight")
    plt.close(fig)

    # Gambar 4: Top Fitur SVM vs Random Forest
    top_pos = df_features[df_features["model_kelompok"] == "SVM_Positif_Phishing"].head(12)
    top_neg = df_features[df_features["model_kelompok"] == "SVM_Negatif_Resmi"].head(12)
    svm_plot_df = pd.concat([top_pos, top_neg], ignore_index=True).sort_values("skor")
    rf_plot_df = df_features[df_features["model_kelompok"] == "RF_Importance"].head(15).sort_values("skor")

    fig, axes = plt.subplots(1, 2, figsize=(13, 6.2))
    svm_colors = ["#dc2626" if val > 0 else "#2563eb" for val in svm_plot_df["skor"]]
    axes[0].barh(svm_plot_df["fitur"], svm_plot_df["skor"], color=svm_colors)
    axes[0].axvline(0, color="#334155", lw=1.0)
    axes[0].set_title("Top Bobot Koefisien LinearSVC\n(Merah = Phishing, Biru = Resmi/Normal)", fontsize=10.5, fontweight="bold")
    axes[0].set_xlabel("Koefisien Hyperplane")

    axes[1].barh(rf_plot_df["fitur"], rf_plot_df["skor"], color="#059669")
    axes[1].set_title("Top-15 Kepentingan Fitur Random Forest\n(Mean Decrease in Impurity)", fontsize=10.5, fontweight="bold")
    axes[1].set_xlabel("Skor Gini Importance")

    fig.suptitle("Analisis Interpretabilitas Fitur TF-IDF Terbaik", fontsize=12.5, fontweight="bold", y=1.01)
    fig.tight_layout()
    fig.savefig(out_dir / "Gambar_Evaluasi_4_Bobot_Fitur_Teratas.png", bbox_inches="tight")
    plt.close(fig)

    # Gambar 5: Komparasi Lintas Korpus (Accuracy & F1-Score)
    ext_n = stage4["external_cross_corpus"]["unseen_external_rows"]
    tax_n = stage4["tax_subset"]["holdout_tax_rows"]
    regimes = [
        f"Holdout Utama\n(n={svm_m['n_samples']})",
        f"Subset Pajak\n(n={tax_n})",
        f"Zero-Shot Eksternal\n(n={ext_n})",
        f"Korpus 2.521\n(Holdout n={stage4['extended_2521']['n_test']})",
    ]
    svm_acc = [
        svm_m["accuracy"] * 100,
        stage4["tax_subset"]["holdout_svm_calibrated"]["accuracy"] * 100,
        stage4["external_cross_corpus"]["combined_svm_calibrated"]["accuracy"] * 100,
        stage4["extended_2521"]["holdout_svm_calibrated"]["accuracy"] * 100,
    ]
    rf_acc = [
        rf_m["accuracy"] * 100,
        stage4["tax_subset"]["holdout_random_forest"]["accuracy"] * 100,
        stage4["external_cross_corpus"]["combined_random_forest"]["accuracy"] * 100,
        stage4["extended_2521"]["holdout_random_forest"]["accuracy"] * 100,
    ]
    svm_f1 = [
        svm_m["f1"] * 100,
        stage4["tax_subset"]["holdout_svm_calibrated"]["f1"] * 100,
        stage4["external_cross_corpus"]["combined_svm_calibrated"]["f1"] * 100,
        stage4["extended_2521"]["holdout_svm_calibrated"]["f1"] * 100,
    ]
    rf_f1 = [
        rf_m["f1"] * 100,
        stage4["tax_subset"]["holdout_random_forest"]["f1"] * 100,
        stage4["external_cross_corpus"]["combined_random_forest"]["f1"] * 100,
        stage4["extended_2521"]["holdout_random_forest"]["f1"] * 100,
    ]

    x_pos = np.arange(len(regimes))
    width = 0.35
    fig, axes = plt.subplots(1, 2, figsize=(12.5, 4.9))
    for ax, metric_label, vals_s, vals_r in (
        (axes[0], "Akurasi (%)", svm_acc, rf_acc),
        (axes[1], "F1-Score (%)", svm_f1, rf_f1),
    ):
        b1 = ax.bar(x_pos - width / 2, vals_s, width, label="SVM Linear (Platt)", color="#1d4ed8")
        b2 = ax.bar(x_pos + width / 2, vals_r, width, label="Random Forest (Tuned)", color="#059669")
        for bars in (b1, b2):
            for bar in bars:
                h = bar.get_height()
                ax.annotate(
                    f"{h:.1f}%",
                    xy=(bar.get_x() + bar.get_width() / 2, h),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha="center",
                    va="bottom",
                    fontsize=8,
                )
        ax.set_xticks(x_pos)
        ax.set_xticklabels(regimes, fontsize=9)
        ax.set_ylim(0, 112)
        ax.set_ylabel(metric_label)
        ax.set_title(f"Perbandingan {metric_label} Lintas Skenario", fontsize=11, fontweight="bold")
        ax.legend(loc="lower left")

    fig.suptitle("Generalisasi Model: Uji Holdout, Domain Pajak, dan Lintas-Korpus", fontsize=12.5, fontweight="bold", y=1.02)
    fig.tight_layout()
    fig.savefig(out_dir / "Gambar_Evaluasi_5_Komparasi_Lintas_Korpus.png", bbox_inches="tight")
    plt.close(fig)

    # Gambar 6: Komparasi SHAP Global (SVM Linear vs Random Forest)
    fig, axes = plt.subplots(1, 2, figsize=(13, 6.0))
    for ax, model_key, title in (
        (axes[0], "SVM_Linear_SHAP", "Top-15 Fitur SHAP: SVM Linear\n(Merah = Mendorong Phishing, Biru = Resmi/Normal)"),
        (axes[1], "Random_Forest_SHAP", "Top-15 Fitur SHAP: Random Forest\n(Merah = Mendorong Phishing, Biru = Resmi/Normal)"),
    ):
        sub = df_shap[df_shap["model"] == model_key].head(15).sort_values("mean_abs_shap")
        colors = ["#dc2626" if val >= 0 else "#2563eb" for val in sub["mean_shap_signed"]]
        ax.barh(sub["fitur"], sub["mean_abs_shap"], color=colors)
        ax.set_title(title, fontsize=10.5, fontweight="bold")
        ax.set_xlabel("Rata-rata |Nilai SHAP| (Dampak Prediksi Holdout)")

    fig.suptitle("Interpretabilitas Model Berbasis SHAP (Holdout n = 233)", fontsize=12.5, fontweight="bold", y=1.01)
    fig.tight_layout()
    fig.savefig(out_dir / "Gambar_Evaluasi_6_SHAP_Komparasi.png", bbox_inches="tight")
    plt.close(fig)


def _build_main_comparison_table(stage1: dict[str, Any], stage2_3: dict[str, Any], stage4: dict[str, Any]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []

    def _add_holdout_row(tahap: str, model_label: str, m: dict[str, Any]) -> None:
        rows.append(
            {
                "tahap_evaluasi": tahap,
                "model": model_label,
                "n_sampel": m["n_samples"],
                "accuracy": round(m["accuracy"], 4),
                "precision": round(m["precision"], 4),
                "recall": round(m["recall"], 4),
                "f1": round(m["f1"], 4),
                "f1_macro": round(m["f1_macro"], 4),
                "roc_auc": round(m["roc_auc"], 4) if m["roc_auc"] is not None else None,
                "pr_auc": round(m["pr_auc"], 4) if m["pr_auc"] is not None else None,
                "brier_score": round(m["brier_score"], 5) if m["brier_score"] is not None else None,
                "log_loss": round(m["log_loss"], 5) if m["log_loss"] is not None else None,
                "tn": m["tn"],
                "fp": m["fp"],
                "fn": m["fn"],
                "tp": m["tp"],
            }
        )

    def _add_cv_row(tahap: str, model_label: str, n_samples: int, cv_m: dict[str, float]) -> None:
        rows.append(
            {
                "tahap_evaluasi": tahap,
                "model": model_label,
                "n_sampel": n_samples,
                "accuracy": round(cv_m["accuracy_mean"], 4),
                "precision": round(cv_m["precision_mean"], 4),
                "recall": round(cv_m["recall_mean"], 4),
                "f1": round(cv_m["f1_mean"], 4),
                "f1_macro": round(cv_m["f1_macro_mean"], 4),
                "roc_auc": round(cv_m["roc_auc_mean"], 4),
                "pr_auc": None,
                "brier_score": None,
                "log_loss": None,
                "tn": None,
                "fp": None,
                "fn": None,
                "tp": None,
            }
        )

    _add_holdout_row("Tahap 1: Baseline Holdout 80:20", "SVM Linear (Default)", stage1["svm_linear"])
    _add_holdout_row("Tahap 1: Baseline Holdout 80:20", "Random Forest (Default n=200)", stage1["random_forest"])
    _add_cv_row("Tahap 1: 10-Fold CV Default (Latih)", "SVM Linear (Default)", 931, stage1["cv_10fold_default"]["svm_linear"])
    _add_cv_row("Tahap 1: 10-Fold CV Default (Latih)", "Random Forest (Default n=200)", 931, stage1["cv_10fold_default"]["random_forest"])

    _add_cv_row("Tahap 2: 10-Fold CV Tuned (Latih)", "SVM Linear (Tuned)", 931, stage2_3["cv_10fold_tuned"]["svm_linear"])
    _add_cv_row("Tahap 2: 10-Fold CV Tuned (Latih)", "Random Forest (Tuned)", 931, stage2_3["cv_10fold_tuned"]["random_forest"])
    _add_holdout_row("Tahap 3: Holdout Tuned & Kalibrasi", "SVM Linear (Tuned)", stage2_3["holdout_tuned"]["svm_linear"])
    _add_holdout_row("Tahap 3: Holdout Tuned & Kalibrasi", "SVM Linear (Platt Sigmoid)", stage2_3["holdout_tuned"]["svm_calibrated"])
    _add_holdout_row("Tahap 3: Holdout Tuned & Kalibrasi", "Random Forest (Tuned)", stage2_3["holdout_tuned"]["random_forest"])

    _add_holdout_row("Tahap 4A: Subset Pajak Holdout", "SVM Linear (Platt Sigmoid)", stage4["tax_subset"]["holdout_svm_calibrated"])
    _add_holdout_row("Tahap 4A: Subset Pajak Holdout", "Random Forest (Tuned)", stage4["tax_subset"]["holdout_random_forest"])
    _add_cv_row("Tahap 4A: 10-Fold CV Korpus Pajak 260", "SVM Linear (Tuned)", 260, stage4["tax_subset"]["cv_10fold_tax_260_svm"])
    _add_cv_row("Tahap 4A: 10-Fold CV Korpus Pajak 260", "Random Forest (Tuned)", 260, stage4["tax_subset"]["cv_10fold_tax_260_rf"])

    _add_holdout_row("Tahap 4B: Zero-Shot Eksternal (Unseen)", "SVM Linear (Platt Sigmoid)", stage4["external_cross_corpus"]["combined_svm_calibrated"])
    _add_holdout_row("Tahap 4B: Zero-Shot Eksternal (Unseen)", "Random Forest (Tuned)", stage4["external_cross_corpus"]["combined_random_forest"])

    _add_holdout_row("Tahap 4C: Holdout Korpus 2.521 (80:20)", "SVM Linear (Platt Sigmoid)", stage4["extended_2521"]["holdout_svm_calibrated"])
    _add_holdout_row("Tahap 4C: Holdout Korpus 2.521 (80:20)", "Random Forest (Tuned)", stage4["extended_2521"]["holdout_random_forest"])
    _add_cv_row("Tahap 4C: 10-Fold CV Korpus 2.521", "SVM Linear (Tuned)", 2521, stage4["extended_2521"]["cv_10fold_svm"])
    _add_cv_row("Tahap 4C: 10-Fold CV Korpus 2.521", "Random Forest (Tuned)", 2521, stage4["extended_2521"]["cv_10fold_rf"])

    return pd.DataFrame(rows)


def _format_pct(val: float | None) -> str:
    return f"{val * 100:.2f}%" if val is not None else "-"


def _build_markdown_report(
    stage1: dict[str, Any],
    stage2_3: dict[str, Any],
    df_ablation: pd.DataFrame,
    stage4: dict[str, Any],
    df_features: pd.DataFrame,
    df_shap: pd.DataFrame,
    df_errors: pd.DataFrame,
    runtime_sec: float,
) -> str:
    b_svm = stage1["svm_linear"]
    b_rf = stage1["random_forest"]
    t_cv_svm = stage2_3["cv_10fold_tuned"]["svm_linear"]
    t_cv_rf = stage2_3["cv_10fold_tuned"]["random_forest"]
    h_svm = stage2_3["holdout_tuned"]["svm_calibrated"]
    h_rf = stage2_3["holdout_tuned"]["random_forest"]
    tax_s = stage4["tax_subset"]
    ext_s = stage4["external_cross_corpus"]
    e2521 = stage4["extended_2521"]

    svm_params_str = json.dumps(stage2_3["best_params"]["svm_linear"])
    rf_params_str = json.dumps(stage2_3["best_params"]["random_forest"])

    ablation_lines = [
        "| Konfigurasi | Model | CV10 F1 Mean | CV10 Acc Mean | Holdout Acc | Holdout F1 |",
        "| :--- | :--- | ---: | ---: | ---: | ---: |",
    ]
    for _, row in df_ablation.iterrows():
        ablation_lines.append(
            f"| {row['konfigurasi']} | {row['model']} | {row['cv10_f1_mean'] * 100:.2f}% | "
            f"{row['cv10_accuracy_mean'] * 100:.2f}% | {row['holdout_accuracy'] * 100:.2f}% | {row['holdout_f1'] * 100:.2f}% |"
        )

    top_pos = ", ".join(
        f"`{r['fitur']}` ({r['skor']:.3f})"
        for _, r in df_features[df_features["model_kelompok"] == "SVM_Positif_Phishing"].head(8).iterrows()
    )
    top_neg = ", ".join(
        f"`{r['fitur']}` ({r['skor']:.3f})"
        for _, r in df_features[df_features["model_kelompok"] == "SVM_Negatif_Resmi"].head(8).iterrows()
    )
    top_rf = ", ".join(
        f"`{r['fitur']}` ({r['skor']:.4f})"
        for _, r in df_features[df_features["model_kelompok"] == "RF_Importance"].head(8).iterrows()
    )
    top_shap_svm = ", ".join(
        f"`{r['fitur']}` ({r['mean_abs_shap']:.4f}, {r['arah_dominan']})"
        for _, r in df_shap[df_shap["model"] == "SVM_Linear_SHAP"].head(8).iterrows()
    )
    top_shap_rf = ", ".join(
        f"`{r['fitur']}` ({r['mean_abs_shap']:.4f}, {r['arah_dominan']})"
        for _, r in df_shap[df_shap["model"] == "Random_Forest_SHAP"].head(8).iterrows()
    )

    err_lines = []
    for _, r in df_errors.head(12).iterrows():
        snippet = str(r["Teks"]).replace("\n", " ").replace("|", "/")[:110]
        err_lines.append(
            f"- `idx={r['indeks_korpus']}` | `{r['sumber']}` | `{r['kategori_modus']}` | "
            f"Aktual={r['label_aktual']}, SVM={r['pred_svm_calibrated']} (p={r['prob_svm_calibrated']:.3f}), "
            f"RF={r['pred_rf_tuned']} (p={r['prob_rf_tuned']:.3f}) | `{snippet}`"
        )
    if not err_lines:
        err_lines.append("- Tidak ada kesalahan prediksi pada kedua model di himpunan uji.")

    return "\n".join(
        [
            "# Laporan Hasil Eksperimen Komparasi SVM Linear dan Random Forest",
            "",
            f"Seluruh rangkaian eksperimen dijalankan secara otomatis oleh `src/eksperimen_komparasi.py` dengan total waktu komputasi **{runtime_sec:.2f} detik**.",
            "",
            "## 1. Reproduksi Baseline (Holdout 80:20 Korpus Utama 1.164 Baris)",
            "",
            f"- **SVM Linear (Default):** Akurasi **{_format_pct(b_svm['accuracy'])}**, Precision {_format_pct(b_svm['precision'])}, Recall {_format_pct(b_svm['recall'])}, F1-Score {_format_pct(b_svm['f1'])} (TN={b_svm['tn']}, FP={b_svm['fp']}, FN={b_svm['fn']}, TP={b_svm['tp']}).",
            f"- **Random Forest (Default `n_estimators=200`):** Akurasi **{_format_pct(b_rf['accuracy'])}**, Precision {_format_pct(b_rf['precision'])}, Recall {_format_pct(b_rf['recall'])}, F1-Score {_format_pct(b_rf['f1'])} (TN={b_rf['tn']}, FP={b_rf['fp']}, FN={b_rf['fn']}, TP={b_rf['tp']}).",
            "",
            "## 2. Hyperparameter Tuning & Stratified 10-Fold Cross-Validation (931 Data Latih)",
            "",
            f"- **Parameter Optimal SVM Linear:** `{svm_params_str}` -> 10-Fold CV F1-Score **{t_cv_svm['f1_mean'] * 100:.2f}% ± {t_cv_svm['f1_std'] * 100:.2f}%**, Akurasi **{t_cv_svm['accuracy_mean'] * 100:.2f}%**, ROC-AUC **{t_cv_svm['roc_auc_mean']:.4f}**.",
            f"- **Parameter Optimal Random Forest:** `{rf_params_str}` -> 10-Fold CV F1-Score **{t_cv_rf['f1_mean'] * 100:.2f}% ± {t_cv_rf['f1_std'] * 100:.2f}%**, Akurasi **{t_cv_rf['accuracy_mean'] * 100:.2f}%**, ROC-AUC **{t_cv_rf['roc_auc_mean']:.4f}**.",
            "",
            "## 3. Kalibrasi Probabilitas Platt Scaling & Evaluasi Holdout Final (n = 233)",
            "",
            "| Model | Akurasi | Precision | Recall | F1-Score | ROC-AUC | PR-AUC | Brier Score | Log Loss |",
            "| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
            f"| SVM Linear (Platt Sigmoid) | {_format_pct(h_svm['accuracy'])} | {_format_pct(h_svm['precision'])} | {_format_pct(h_svm['recall'])} | {_format_pct(h_svm['f1'])} | {h_svm['roc_auc']:.4f} | {h_svm['pr_auc']:.4f} | {h_svm['brier_score']:.5f} | {h_svm['log_loss']:.5f} |",
            f"| Random Forest (Tuned) | {_format_pct(h_rf['accuracy'])} | {_format_pct(h_rf['precision'])} | {_format_pct(h_rf['recall'])} | {_format_pct(h_rf['f1'])} | {h_rf['roc_auc']:.4f} | {h_rf['pr_auc']:.4f} | {h_rf['brier_score']:.5f} | {h_rf['log_loss']:.5f} |",
            "",
            "## 4. Studi Ablatif Praproses dan Representasi Fitur TF-IDF",
            "",
            *ablation_lines,
            "",
            "## 5. Ketahanan Bias Kata Kunci Pajak & Uji Generalisasi Lintas-Korpus",
            "",
            f"- **Subset Khusus Pajak pada Holdout (n = {tax_s['holdout_tax_rows']}):** SVM Platt mencapai Akurasi **{_format_pct(tax_s['holdout_svm_calibrated']['accuracy'])}** (F1 {_format_pct(tax_s['holdout_svm_calibrated']['f1'])}, FP={tax_s['holdout_svm_calibrated']['fp']}, FN={tax_s['holdout_svm_calibrated']['fn']}), sedangkan Random Forest mencapai Akurasi **{_format_pct(tax_s['holdout_random_forest']['accuracy'])}** (F1 {_format_pct(tax_s['holdout_random_forest']['f1'])}, FP={tax_s['holdout_random_forest']['fp']}, FN={tax_s['holdout_random_forest']['fn']}).",
            f"- **10-Fold Stratified CV Khusus Korpus Pajak (260 baris):** SVM mencapai F1 **{tax_s['cv_10fold_tax_260_svm']['f1_mean'] * 100:.2f}%** (Akurasi **{tax_s['cv_10fold_tax_260_svm']['accuracy_mean'] * 100:.2f}%**); Random Forest mencapai F1 **{tax_s['cv_10fold_tax_260_rf']['f1_mean'] * 100:.2f}%** (Akurasi **{tax_s['cv_10fold_tax_260_rf']['accuracy_mean'] * 100:.2f}%**).",
            f"- **Uji Zero-Shot Lintas-Korpus Eksternal (n = {ext_s['unseen_external_rows']} unik, dari {ext_s['raw_external_rows']} mentah setelah menghapus {ext_s['overlap_with_primary_removed']} duplikat terhadap korpus utama):** SVM Platt mencapai Akurasi **{_format_pct(ext_s['combined_svm_calibrated']['accuracy'])}** (F1 {_format_pct(ext_s['combined_svm_calibrated']['f1'])}), sedangkan Random Forest mencapai Akurasi **{_format_pct(ext_s['combined_random_forest']['accuracy'])}** (F1 {_format_pct(ext_s['combined_random_forest']['f1'])}).",
            f"- **Evaluasi Korpus Diperluas 2.521 Baris (Holdout n = {e2521['n_test']}):** SVM Platt mencapai Akurasi **{_format_pct(e2521['holdout_svm_calibrated']['accuracy'])}** (F1 {_format_pct(e2521['holdout_svm_calibrated']['f1'])}) dengan 10-Fold CV F1 **{e2521['cv_10fold_svm']['f1_mean'] * 100:.2f}%**; Random Forest mencapai Akurasi **{_format_pct(e2521['holdout_random_forest']['accuracy'])}** (F1 {_format_pct(e2521['holdout_random_forest']['f1'])}) dengan 10-Fold CV F1 **{e2521['cv_10fold_rf']['f1_mean'] * 100:.2f}%**.",
            "",
            "## 6. Interpretabilitas Fitur Teratas & Analisis Kesalahan (n = 233)",
            "",
            f"- **Indikator Phishing Terkuat SVM Linear (+):** {top_pos}",
            f"- **Indikator Resmi/Normal Terkuat SVM Linear (-):** {top_neg}",
            f"- **Fitur Terpenting Random Forest (Gini):** {top_rf}",
            f"- **Top-8 Fitur SHAP SVM Linear (Holdout):** {top_shap_svm}",
            f"- **Top-8 Fitur SHAP Random Forest (Holdout):** {top_shap_rf}",
            f"- **Jumlah Sampel Salah Prediksi (gabungan SVM/RF pada holdout):** {len(df_errors)} baris (rincian lengkap tersedia di `analisis_kesalahan_prediksi.csv`).",
            "",
            *err_lines,
            "",
        ]
    )


def run_all_experiments(save_outputs: bool = True) -> dict[str, Any]:
    """Jalankan seluruh pipeline eksperimen Tahap 1-4 dan simpan artefak evaluasi."""
    t_start = time.perf_counter()
    df_primary, df_extended, df_tax = load_datasets()

    idx_train, idx_test = train_test_split(
        df_primary.index.to_numpy(),
        test_size=0.2,
        random_state=RANDOM_STATE,
        stratify=df_primary["label"].to_numpy(),
    )

    cv = StratifiedKFold(n_splits=CV_SPLITS, shuffle=True, random_state=RANDOM_STATE)
    folds_train = _precompute_tfidf_folds(
        df_primary.loc[idx_train, "teks_sastrawi"],
        df_primary.loc[idx_train, "label"].to_numpy(),
        cv,
        ngram_range=(1, 2),
        max_features=3000,
    )

    stage1 = _run_stage1_baseline(df_primary, idx_train, idx_test, folds_train)
    stage2_3 = _run_stage2_and_3_tuning_calibration(df_primary, idx_train, idx_test, folds_train)
    df_ablation = _run_ablation_study(
        df_primary,
        idx_train,
        idx_test,
        stage2_3["best_params"]["svm_linear"],
        stage2_3["best_params"]["random_forest"],
    )
    stage4, full_models = _run_stage4_domain_and_cross_corpus(
        df_primary, df_extended, df_tax, idx_test, stage2_3
    )
    df_features, df_errors = _build_feature_and_error_tables(
        df_primary, idx_test, stage1, stage2_3
    )
    df_shap = _compute_shap_table(stage2_3, top_n=20)
    df_main_table = _build_main_comparison_table(stage1, stage2_3, stage4)
    runtime_sec = float(time.perf_counter() - t_start)

    summary = {
        "metadata": {
            "random_state": RANDOM_STATE,
            "cv_splits": CV_SPLITS,
            "primary_rows": len(df_primary),
            "train_rows": len(idx_train),
            "test_rows": len(idx_test),
            "extended_rows": len(df_extended),
            "tax_rows": len(df_tax),
            "runtime_seconds": round(runtime_sec, 2),
        },
        "baseline": {
            "svm_linear": stage1["svm_linear"],
            "random_forest": stage1["random_forest"],
        },
        "cv_10fold": {
            "default": stage1["cv_10fold_default"],
            "tuned": stage2_3["cv_10fold_tuned"],
        },
        "tuning": {
            "best_params": stage2_3["best_params"],
            "grid_total_configs": len(stage2_3["grid_df"]),
        },
        "calibration": {
            "svm_linear_uncalibrated": stage2_3["holdout_tuned"]["svm_linear"],
            "svm_calibrated": stage2_3["holdout_tuned"]["svm_calibrated"],
            "random_forest": stage2_3["holdout_tuned"]["random_forest"],
            "holdout_proba_svm_calibrated": stage2_3["holdout_arrays"]["proba_svm_calibrated_matrix"].tolist(),
        },
        "ablation": df_ablation.to_dict(orient="records"),
        "tax_subset": stage4["tax_subset"],
        "external_cross_corpus": stage4["external_cross_corpus"],
        "extended_2521": stage4["extended_2521"],
        "shap_top_features": {
            "svm_linear": df_shap[df_shap["model"] == "SVM_Linear_SHAP"].head(10).to_dict(orient="records"),
            "random_forest": df_shap[df_shap["model"] == "Random_Forest_SHAP"].head(10).to_dict(orient="records"),
        },
        "error_analysis_count": len(df_errors),
        "runtime_seconds": round(runtime_sec, 2),
    }

    if save_outputs:
        os.makedirs(EVALUATION_DIR, exist_ok=True)
        os.makedirs(PROTOTYPE_DIR, exist_ok=True)

        df_main_table.to_csv(EVALUATION_DIR / "tabel_komparasi_utama.csv", index=False)
        stage2_3["grid_df"].to_csv(EVALUATION_DIR / "hasil_gridsearch_10fold.csv", index=False)
        df_ablation.to_csv(EVALUATION_DIR / "studi_ablatif_fitur.csv", index=False)
        df_features.to_csv(EVALUATION_DIR / "fitur_teratas_svm_vs_rf.csv", index=False)
        df_shap.to_csv(EVALUATION_DIR / "shap_fitur_teratas_svm_vs_rf.csv", index=False)
        df_errors.to_csv(EVALUATION_DIR / "analisis_kesalahan_prediksi.csv", index=False)

        _generate_plots(stage2_3, stage4, df_features, df_shap, EVALUATION_DIR)

        report_md = _build_markdown_report(
            stage1, stage2_3, df_ablation, stage4, df_features, df_shap, df_errors, runtime_sec
        )
        (EVALUATION_DIR / "Laporan Hasil Eksperimen Komparasi.md").write_text(
            report_md, encoding="utf-8"
        )

        (EVALUATION_DIR / "ringkasan_eksperimen_lengkap.json").write_text(
            json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
        )

        bundle = {
            **full_models,
            "metadata": {
                "trained_on": "Dataset Gabungan Utama Biner 1164 Baris.csv",
                "n_samples": len(df_primary),
                "preprocessing": "src.eksperimen_baseline.clean_text",
                "svm_best_params": stage2_3["best_params"]["svm_linear"],
                "rf_best_params": stage2_3["best_params"]["random_forest"],
                "holdout_accuracy_svm": stage2_3["holdout_tuned"]["svm_calibrated"]["accuracy"],
                "holdout_brier_svm_calibrated": stage2_3["holdout_tuned"]["svm_calibrated"]["brier_score"],
                "holdout_accuracy_rf": stage2_3["holdout_tuned"]["random_forest"]["accuracy"],
            },
        }
        joblib.dump(bundle, MODEL_PATH, compress=3)

    return summary


if __name__ == "__main__":
    results = run_all_experiments(save_outputs=True)
    print(f"Eksperimen komparasi selesai dalam {results['runtime_seconds']:.2f} detik.")
    print(
        f"Baseline Holdout -> SVM: {results['baseline']['svm_linear']['accuracy']:.4f} | "
        f"RF: {results['baseline']['random_forest']['accuracy']:.4f}"
    )
    print(f"Best Params -> SVM: {results['tuning']['best_params']['svm_linear']} | RF: {results['tuning']['best_params']['random_forest']}")
    print(
        f"Holdout Final -> SVM Platt Acc: {results['calibration']['svm_calibrated']['accuracy']:.4f} "
        f"(Brier={results['calibration']['svm_calibrated']['brier_score']:.5f}) | "
        f"RF Acc: {results['calibration']['random_forest']['accuracy']:.4f} "
        f"(Brier={results['calibration']['random_forest']['brier_score']:.5f})"
    )
