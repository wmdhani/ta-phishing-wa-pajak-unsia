from src.eksperimen_baseline import clean_text, load_combined_dataset


def test_clean_text_preserves_tokens_and_stems() -> None:
    sample = "Segera unduh Surat_Tagihan.apk melalui https://coretax-online.com agar pemblokiran dibatalkan"
    cleaned = clean_text(sample)
    tokens = cleaned.split()
    assert "token_apk" in tokens
    assert "token_url" in tokens
    assert "blokir" in tokens
    assert "batal" in tokens
    assert "melalui" not in tokens


def test_load_combined_dataset_shape() -> None:
    df_raw = load_combined_dataset(deduplicate=False)
    assert len(df_raw) == 1164
    assert (df_raw["label"] == 1).sum() == 465
    assert (df_raw["label"] == 0).sum() == 699

    df = load_combined_dataset()
    assert len(df) == 1159
    assert (df["label"] == 1).sum() == 462
    assert (df["label"] == 0).sum() == 697
    assert not df["clean_text"].duplicated().any()
    assert (df["clean_text"].str.len() > 0).all()
