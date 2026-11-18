# Tugas Akhir UNSIA: Deteksi Phishing WhatsApp Perpajakan

**Judul:** Komparasi Algoritma Support Vector Machine dan Random Forest dalam Deteksi Pesan Phishing WhatsApp Mengatasnamakan Otoritas Perpajakan  
**Mahasiswa:** Wan Mirza Dhani (`240101020194`)  
**Program Studi:** PJJ Sistem Informasi  
**Ketua Program Studi:** Vika Febri Muliati, S.Kom., M.Kom  
**Dosen Pembimbing:** Novi Dian Nathasia, S.Kom., MMSI  

---

## Struktur Direktori (Sesuai Alur Kerja Tugas Akhir)
- `01 Administrasi/`: Pedoman resmi TA UNSIA 2024 dan daftar pembagian dosen pembimbing.
- `02 Proposal/`: Draf usulan judul dan berkas pengajuan judul (`.docx` dan `.pdf`).
- `03 Referensi/`: Catatan cek kebaruan, ekspor `.ris` Zotero, panduan SLR, `Daftar Pustaka/`, serta `Ebook Metodologi/` (diabaikan Git untuk Zotero lokal).
- `04 Dataset/`: Dokumentasi sumber data (`README Dataset.md`), korpus mentah (`01 Data Mentah/`), serta korpus terkurasi dan dataset gabungan (`02 Data Olahan/`).
- `05 Hasil Evaluasi/`: Grafik evaluasi model, *Confusion Matrix*, dan ringkasan metrik eksperimen.
- `06 Prototipe Aplikasi/`: Aplikasi web **Cek Pesan Pajak** (`web/`), layanan REST API FastAPI (`api.py`), mesin inferensi (`inference.py`), dan ekstensi Chrome WhatsApp Web (`extension/`).
- `07 Naskah Tugas Akhir/`: Bagian awal, draf Bab I sampai Bab V, dokumen Word naskah TA, serta `Aset Gambar/`.
- `src/`: Kode sumber Python terstruktur:
  - `korpus_pajak.py`: Metadata sumber otoritatif DJP dan 260 rekaman teks terkurasi.
  - `kurasi_dataset.py`: Pipeline pembuatan dataset olahan dan katalog provenans SHA-256.
  - `eksperimen_baseline.py`: Praproses Sastrawi, tokenisasi khusus, TF-IDF, dan komparasi baseline SVM vs Random Forest.
  - `eksperimen_komparasi.py`: Pipeline lengkap Stratified 10-Fold CV, GridSearchCV, kalibrasi Platt, studi ablatif, uji lintas-korpus, grafik evaluasi, dan ekspor model `.joblib`.
  - `buat_dokumen_proposal.py`: Pembangun dokumen ringkasan usulan judul `.pdf` dan `.docx`.
- `tests/`: Pengujian otomatis (`pytest`) untuk integritas korpus dan pipeline eksperimen.

---

## Lingkungan Python (Di Luar OneDrive via `uv`)
Agar file `.exe` pada virtual environment tidak diblokir OneDrive, `.venv` disimpan lokal di `%LOCALAPPDATA%\venvs\ta-phishing-pajak-unsia` dan sudah dikonfigurasi otomatis di `.vscode/settings.json` untuk terminal IDE.

```powershell
# 1. Sinkronisasi paket (bila menjalankan dari PowerShell luar IDE, set env dulu)
$env:UV_PROJECT_ENVIRONMENT = "$env:LOCALAPPDATA\venvs\ta-phishing-pajak-unsia"
uv sync

# 2. Jalankan pengujian integritas dataset & eksperimen
& "$env:LOCALAPPDATA\venvs\ta-phishing-pajak-unsia\Scripts\pytest.exe" -q

# 3. Jalankan baseline dan eksperimen komparasi lengkap SVM vs Random Forest
& "$env:LOCALAPPDATA\venvs\ta-phishing-pajak-unsia\Scripts\python.exe" src\eksperimen_baseline.py
& "$env:LOCALAPPDATA\venvs\ta-phishing-pajak-unsia\Scripts\python.exe" -m src.eksperimen_komparasi

# 4. Reproduksi seluruh dataset olahan dan katalog SHA-256
& "$env:LOCALAPPDATA\venvs\ta-phishing-pajak-unsia\Scripts\python.exe" -m src.kurasi_dataset

# 5. Jalankan aplikasi web Cek Pesan Pajak dan REST API (http://127.0.0.1:8000/)
& "$env:LOCALAPPDATA\venvs\ta-phishing-pajak-unsia\Scripts\uvicorn.exe" api:app --app-dir "06 Prototipe Aplikasi" --reload

# 6. Validasi draf naskah UNSIA dan ekspor ke Word (.docx)
& "$env:LOCALAPPDATA\venvs\ta-phishing-pajak-unsia\Scripts\python.exe" "%USERPROFILE%\.gemini\skill-vault\unsia-ta-prototype\scripts\validate_unsia.py" "07 Naskah Tugas Akhir\Naskah Bagian Awal dan Bab I TA UNSIA.md"
& "$env:LOCALAPPDATA\venvs\ta-phishing-pajak-unsia\Scripts\python.exe" "%USERPROFILE%\.gemini\skill-vault\unsia-ta-prototype\scripts\export_unsia_docx.py" "<input.md>" "<output.docx>"

# 7. Sinkronisasi referensi e-book metodologi ke Zotero lokal
& "$env:LOCALAPPDATA\venvs\ta-phishing-pajak-unsia\Scripts\python.exe" "%USERPROFILE%\.gemini\skill-vault\unsia-ta-prototype\scripts\sync_zotero_metodologi.py"

# 8. Mode Antigravity (TA / Programming)
agy-mode ta
```
