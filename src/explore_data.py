import re
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC


def clean_text(text: str) -> str:
    text = str(text).lower()
    text = re.sub(r"\.apk\b", " token_apk ", text)
    text = re.sub(r"https?://\S+|www\.\S+|bit\.ly/\S+", " token_url ", text)
    text = re.sub(r"[^a-z0-9\s_]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def load_combined_dataset() -> pd.DataFrame:
    df_base = pd.read_csv("data/raw_sms_spam_v1.csv")
    df_base = df_base[df_base["label"].isin([0, 1])][["Teks", "label"]].copy()
    df_base["sumber"] = "Korpus_Umum"

    df_tax = pd.read_csv("data/dataset_pajak_curated.csv")[["Teks", "label"]].copy()
    df_tax["sumber"] = "Korpus_Pajak"

    df = pd.concat([df_base, df_tax], ignore_index=True)
    df["clean_text"] = df["Teks"].apply(clean_text)
    return df


def main() -> None:
    df = load_combined_dataset()
    print("=== STATISTIK DATASET GABUNGAN ===")
    print(f"Total baris       : {len(df)}")
    print(f"Distribusi label  :\n{df['label'].value_counts().rename({0: 'Aman (0)', 1: 'Phishing/Fraud (1)'})}")
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
        print(f"=== HASIL BASELINE: {name} ===")
        print(f"Accuracy: {accuracy_score(y_test, preds):.4f}")
        print(classification_report(y_test, preds, target_names=["Aman (0)", "Phishing (1)"]))


if __name__ == "__main__":
    main()
