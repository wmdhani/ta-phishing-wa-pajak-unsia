import re
from functools import lru_cache
from pathlib import Path

import pandas as pd
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
)
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC

SPECIAL_TOKENS = frozenset({"token_apk", "token_url"})
URL_PATTERN = re.compile(
    r"https?://\S+|www\.\S+|bit\.ly/\S+|\b[a-z0-9.-]+\.(?:go\.id|co\.id|my\.id|com|net|org|xyz|id|cc)\S*"
)


def _build_sastrawi_tools() -> tuple[set[str], callable]:
    stop_words = set(StopWordRemoverFactory().get_stop_words())
    stemmer = StemmerFactory().create_stemmer()
    inner = getattr(
        stemmer, "delegatedStemmer", getattr(stemmer, "delegated_stemmer", stemmer)
    )
    # PySastrawi stores dictionary words in a list; converting to set gives O(1) lookup.
    if hasattr(inner, "dictionary"):
        inner.dictionary.words = set(inner.dictionary.words)
    cached_stem = lru_cache(maxsize=20000)(stemmer.stem)
    return stop_words, cached_stem


STOP_WORDS, STEM_WORD = _build_sastrawi_tools()


def clean_text(text: str) -> str:
    text = str(text).lower()
    text = re.sub(r"\.apk\b", " token_apk ", text)
    text = URL_PATTERN.sub(" token_url ", text)
    text = re.sub(r"[^a-z0-9\s_]", " ", text)

    processed = []
    for tok in text.split():
        if tok in SPECIAL_TOKENS:
            processed.append(tok)
            continue
        if tok in STOP_WORDS:
            continue
        if tok.isalpha() and len(tok) > 2:
            processed.append(STEM_WORD(tok))
        else:
            processed.append(tok)
    return " ".join(processed)


def load_combined_dataset() -> pd.DataFrame:
    dataset_dir = Path(__file__).resolve().parent.parent / "04 Dataset"
    df_base = pd.read_csv(
        dataset_dir / "01 Data Mentah" / "Rahmi 2016 Korpus SMS Spam Utama v1.csv"
    )
    df_base = df_base[df_base["label"].isin([0, 1])][["Teks", "label"]].copy()
    df_base["sumber"] = "Korpus_Umum"

    df_tax = pd.read_csv(
        dataset_dir / "02 Data Olahan" / "Dataset Pajak Terkurasi 260 Baris.csv"
    )[["Teks", "label"]].copy()
    df_tax["sumber"] = "Korpus_Pajak"

    df = pd.concat([df_base, df_tax], ignore_index=True)
    df["clean_text"] = df["Teks"].apply(clean_text)
    return df


def main() -> None:
    df = load_combined_dataset()
    print("=== STATISTIK DATASET GABUNGAN ===")
    print(f"Total baris       : {len(df)}")
    print(
        f"Distribusi label  :\n{df['label'].value_counts().rename({0: 'Aman (0)', 1: 'Phishing/Fraud (1)'})}"
    )
    print(f"\nDistribusi sumber :\n{df['sumber'].value_counts()}\n")

    X_train, X_test, y_train, y_test = train_test_split(
        df["clean_text"],
        df["label"],
        test_size=0.2,
        random_state=42,
        stratify=df["label"],
    )

    vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=3000)
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    models = {
        "Support Vector Machine (LinearSVC)": LinearSVC(random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=200, random_state=42),
    }

    for name, model in models.items():
        model.fit(X_train_vec, y_train)
        preds = model.predict(X_test_vec)
        cm = confusion_matrix(y_test, preds)
        print(f"=== HASIL BASELINE: {name} ===")
        print(f"Accuracy      : {accuracy_score(y_test, preds):.4f}")
        print(f"F1-Score Macro: {f1_score(y_test, preds, average='macro'):.4f}")
        print(f"Confusion Mat : TN={cm[0,0]}, FP={cm[0,1]}, FN={cm[1,0]}, TP={cm[1,1]}")
        print(classification_report(y_test, preds, target_names=["Aman (0)", "Phishing (1)"]))


if __name__ == "__main__":
    main()
