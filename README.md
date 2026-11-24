# Tugas Akhir UNSIA: Deteksi Phishing WhatsApp Perpajakan

**Judul:** Komparasi Algoritma Support Vector Machine dan Random Forest dalam Deteksi Pesan Phishing WhatsApp Mengatasnamakan Otoritas Perpajakan  
**Mahasiswa:** Wan Mirza Dhani (`240101020194`)  
**Program Studi:** PJJ Sistem Informasi  
**Ketua Program Studi:** Vika Febri Muliati, S.Kom., M.Kom  
**Dosen Pembimbing:** Novi Dian Nathasia, S.Kom., MMSI  

---

## Struktur Direktori (Sesuai Alur Kerja Tugas Akhir)
- `01-administrasi/`: Pedoman resmi TA UNSIA 2024 dan daftar pembagian dosen pembimbing.
- `02-proposal/`: Draf usulan judul dan berkas pengajuan judul (`.docx` dan `.pdf`).
- `03-referensi/`: Catatan cek kebaruan, daftar pustaka (`daftar-pustaka/`), serta buku metodologi (`ebook-metodologi/`).
- `04-dataset/`: Dokumentasi sumber data (`readme-dataset.md`), korpus mentah (`01-data-mentah/`), serta korpus terkurasi dan dataset gabungan (`02-data-olahan/`).
- `05-hasil-evaluasi/`: Grafik evaluasi model (`gambar/`), tabel CSV (`csv/`), ringkasan JSON (`json/`), dan laporan (`laporan/`).
- `app/`: Aplikasi web **Cek Pesan Pajak** (`app/frontend/`), layanan REST API FastAPI & mesin inferensi (`app/backend/api.py`, `app/backend/inference.py`), serta ekstensi Chrome WhatsApp Web (`app/extension/`).
- `06-naskah-ta/`: Naskah modular per bab (`md/`), dokumen Word (`docx/`), PDF (`pdf/`), aset gambar (`aset-gambar/`), dan log audit (`log-review-ta.md`).
- `ml/`: Kode sumber modul eksperimen dan kurasi Python:
  - `ml/korpus_pajak.py`: Metadata sumber otoritatif DJP dan 260 rekaman teks terkurasi.
  - `ml/kurasi_dataset.py`: Pipeline pembuatan dataset olahan dan katalog provenans SHA-256.
  - `ml/eksperimen_baseline.py`: Praproses Sastrawi, tokenisasi khusus, TF-IDF, dan komparasi baseline SVM vs Random Forest.
  - `ml/eksperimen_komparasi.py`: Pipeline lengkap Stratified 10-Fold CV, GridSearchCV, kalibrasi Platt, studi ablatif, uji lintas-korpus, grafik evaluasi, dan ekspor model `.joblib`.
  - `ml/benchmark_purwarupa.py`: Pengukuran latensi `TestClient`, penangkapan tangkapan layar web/ekstensi, dan salin aset gambar evaluasi.
- `scripts/`: Pembangun dokumen proposal dan penyuntik metadata/PDF Word (`buat_dokumen_proposal.py`, `terapkan_metadata_dokumen.py`).
- `tests/`: Pengujian otomatis (`pytest`) untuk integritas korpus, pipeline eksperimen, dan purwarupa API/ekstensi.

---

## Lingkungan Python (Di Luar OneDrive via `uv`)
Agar file `.exe` pada virtual environment tidak diblokir OneDrive, `.venv` disimpan lokal di `%LOCALAPPDATA%\venvs\ta-phishing-pajak-unsia` dan sudah dikonfigurasi otomatis di `.vscode/settings.json` untuk terminal IDE.

```powershell
# 1. Sinkronisasi paket (bila menjalankan dari PowerShell luar IDE, set env dulu)
$env:UV_PROJECT_ENVIRONMENT = "$env:LOCALAPPDATA\venvs\ta-phishing-pajak-unsia"
uv sync

# 2. Jalankan pengujian integritas dataset, eksperimen, & API
& "$env:LOCALAPPDATA\venvs\ta-phishing-pajak-unsia\Scripts\pytest.exe" -q

# 3. Jalankan baseline, eksperimen komparasi lengkap, & benchmark purwarupa
& "$env:LOCALAPPDATA\venvs\ta-phishing-pajak-unsia\Scripts\python.exe" -m ml.eksperimen_baseline
& "$env:LOCALAPPDATA\venvs\ta-phishing-pajak-unsia\Scripts\python.exe" -m ml.eksperimen_komparasi
& "$env:LOCALAPPDATA\venvs\ta-phishing-pajak-unsia\Scripts\python.exe" -m ml.benchmark_purwarupa

# 4. Reproduksi seluruh dataset olahan dan katalog SHA-256
& "$env:LOCALAPPDATA\venvs\ta-phishing-pajak-unsia\Scripts\python.exe" -m ml.kurasi_dataset

# 5. Jalankan aplikasi web Cek Pesan Pajak dan REST API (http://127.0.0.1:8000/)
& "$env:LOCALAPPDATA\venvs\ta-phishing-pajak-unsia\Scripts\uvicorn.exe" api:app --app-dir "app/backend" --reload

# 6. Validasi draf naskah UNSIA dan ekspor ke Word (.docx)
& "$env:LOCALAPPDATA\venvs\ta-phishing-pajak-unsia\Scripts\python.exe" "%USERPROFILE%\.gemini\skill-vault\unsia-ta-prototype\scripts\validate_unsia.py" "06-naskah-ta\md\07-naskah-lengkap\naskah-lengkap-tugas-akhir-ta-unsia.md"
& "$env:LOCALAPPDATA\venvs\ta-phishing-pajak-unsia\Scripts\python.exe" "%USERPROFILE%\.gemini\skill-vault\unsia-ta-prototype\scripts\export_unsia_docx.py" "<input.md>" "<output.docx>"
```
