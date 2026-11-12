# Tugas Akhir PJJ Informatika UNSIA (Skema Prototype)

**Judul:** Komparasi Algoritma Support Vector Machine dan Random Forest dalam Deteksi Pesan Phishing WhatsApp Mengatasnamakan Otoritas Perpajakan  
**Mahasiswa:** Wan Mirza Dhani (`240101020194`)  
**Pembimbing:** Novi Dian Nathasia, S.Kom, MMSI.

---

## Struktur Direktori
- `app/`: Aplikasi prototipe web interaktif berbasis Streamlit.
- `data/`: Dataset teks korpus umum (`raw_sms_spam_v1.csv`) dan korpus spesifik perpajakan (`dataset_pajak_curated.csv`).
- `doc/administrasi/`: Pedoman resmi TA UNSIA (`PEDOMAN_PENULISAN_TA_UNSIA_2024.pdf`) dan daftar pembagian pembimbing.
- `doc/naskah/`: Draf Bab I sampai Bab V dan lampiran naskah.
- `doc/proposal/`: Usulan judul dan dokumen proposal awal.
- `doc/referensi/`: Catatan cek kebaruan, file BIB/RIS (`referensi_metodologi_ta.ris`), panduan SLR, serta `ebook_metodologi/` (diabaikan Git untuk Zotero lokal).
- `results/`: Grafik evaluasi model, *Confusion Matrix*, dan ringkasan metrik eksperimen.
- `src/`: Skrip eksperimen ML/NLP (`explore_data.py`), pembangun dokumen proposal (`build_proposal_doc.py`), dan pipeline pelatihan.
- `tests/`: Pengujian otomatis (`pytest`).

---

## Perintah Cepat (`.venv` via `uv`)
1. **Sinkronisasi paket Python**: `uv sync`
2. **Jalankan eksperimen baseline**: `.\.venv\Scripts\python.exe src\explore_data.py`
3. **Validasi draf terhadap Pedoman UNSIA**: `.\.venv\Scripts\python.exe "%USERPROFILE%\.gemini\skill-vault\unsia-ta-prototype\scripts\validate_unsia.py" <berkas.md>`
4. **Ekspor naskah Markdown ke Word (`.docx`) UNSIA**: `.\.venv\Scripts\python.exe "%USERPROFILE%\.gemini\skill-vault\unsia-ta-prototype\scripts\export_unsia_docx.py" <input.md> <output.docx>`
5. **Mode Antigravity TA / Programming**: `agy-mode ta` / `agy-mode coding`
