# BAB III IMPLEMENTASI METODE USULAN

## 3.1 Arsitektur Implementasi Metode Usulan

Implementasi metode usulan mewujudkan enam tahap prosedur operasional Bab II menjadi sistem perangkat lunak Python 3.11.9 [40]. Arsitekturnya memisahkan alur pelatihan luring (*offline*) dan layanan daring (*online*). Alur luring mengolah teks menjadi vektor TF-IDF 3.000 dimensi lalu melatih `LinearSVC` serta `RandomForestClassifier` [6], [36], [37]. Sementara itu, alur daring memuat bundel terkalibrasi ke FastAPI untuk melayani web dan ekstensi peramban [26], seperti pada Gambar 3.1.

![Arsitektur Sistem Terpadu Deteksi Phishing WhatsApp Perpajakan](Aset Gambar/Gambar 3.1 Arsitektur Sistem Terpadu.png)

Gambar 3.1 Arsitektur Sistem Terpadu Deteksi *Phishing* WhatsApp Perpajakan.

Logika klasifikasi, deteksi heuristik keamanan, penerjemahan alasan awam, serta sorotan bahaya dipusatkan di `06 Prototipe Aplikasi/inference.py`. Pemusatan aturan ini menjamin antarmuka web *Cek Pesan Pajak*, titik akhir REST API, dan ekstensi *WhatsApp Web* selalu menghasilkan vonis serta sorotan kata pemicu yang konsisten. Daftar lengkap pemetaan sembilan modul kode sumber terhadap tahapan riset tercantum pada Lampiran (`Tabel L.5`).

## 3.2 Implementasi Kurasi Korpus dan Praproses Teks

Tahap data dijalankan melalui `src/korpus_pajak.py` dan `src/kurasi_dataset.py`. Sebanyak 68 arsip publik disaring memakai `strip_djp_boilerplate` [2], [5] menjadi 65 sumber unik berisi 260 pesan pajak seimbang (130 *phishing* 12 modus dan 130 siaran resmi). Penggabungannya dengan 904 SMS umum [6] sesudah menyisihkan 239 iklan promo membentuk dataset induk 1.164 baris berverifikasi 10 *hash* SHA-256. Korpus induk ikut dipadukan dengan data Theodorus dkk. [7] serta Saragih dari 4.255 mentah menjadi 2.521 baris pasca-`clean_text` (membuang 1.734 duplikat).

Fungsi `clean_text` di `src/eksperimen_baseline.py` menyiapkan daftar kata dasar Sastrawi ke dalam himpunan (`set`) berkapasitas `lru_cache` 20.000 kata. Struktur himpunan ini mempercepat pencarian morfologi menjadi waktu konstan $O(1)$ saat melakukan pemrosesan massal ratusan pesan [37]. Setiap teks masukan melewati enam langkah praproses berurutan berikut:

a) Pengecilan seluruh huruf via metode `lower()` agar variasi kapitalisasi seragam.

b) Konversi pola `.apk` (`r"\.apk\b"`) menjadi `token_apk` sebelum pemindaian URL agar nama berkas tidak dianggap tautan web.

c) Pengubahan tautan `http`, `https`, `www`, `bit.ly`, atau akhiran domain `.go.id`, `.co.id`, dan `.xyz` menjadi `token_url`.

d) Penghapusan simbol nonalfanumerik selain spasi dan garis bawah memakai pola `r"[^a-z0-9\s_]"`.

e) Penyaringan *stopword* Sastrawi dengan tetap melestarikan `token_apk` dan `token_url`.

f) Pengembalian kata alfabetis lebih dari dua huruf (`tok.isalpha() and len(tok) > 2`) ke bentuk dasar lewat Sastrawi 1.0.1 [37].

Guna mendukung uji ablatif pada `src/eksperimen_komparasi.py`, dibangun pula dua varian teks pembanding di luar `teks_sastrawi`. Kolom `clean_text` menyimpan teks tanpa penyaringan kata henti dan *stemming* (`2_Tanpa_Sastrawi`), sedangkan kolom `teks_tanpa_token_entitas` menghapus pola URL dan berkas `.apk` (`1_Tanpa_Token_Entitas`).

## 3.3 Implementasi Pelatihan Model, Penyetelan Hiperparameter, dan Kalibrasi

Skrip `src/eksperimen_komparasi.py` mengunci nilai `RANDOM_STATE=42` bagi seluruh tahapan eksperimen [40]. Pada korpus induk 1.164 baris, penyaringan duplikat `teks_sastrawi` menyisihkan 5 baris sehingga tersisa 1.159 teks unik (`697` aman dan `462` penipuan). Data lalu dibagi terstratifikasi 80:20 menjadi 927 data latih dan 232 data uji. Fungsi `_precompute_tfidf_folds` membangun objek `TfidfVectorizer(ngram_range=(1, 2), max_features=3000)` secara terpisah di tiap lipatan *Stratified 10-Fold CV* agar kosakata validasi tetap terisolasi [36], [38].

Melalui fungsi `_run_grid_over_folds`, pencarian *grid* mengevaluasi seluruh 36 kandidat kombinasi parameter (12 kandidat `LinearSVC` dan 24 kandidat *Random Forest*) berdasarkan nilai rata-rata *F1-Score* sepuluh lipatan. Rincian ruang pencarian serta parameter optimal terpilih dari evaluasi tersebut disajikan pada Tabel 3.1.

Tabel 3.1 Konfigurasi Ruang Pencarian Hiperparameter dan Parameter Terpilih

| Algoritma Klasifikasi | Ruang Pencarian Parameter (`_run_grid_over_folds`) | Konfigurasi Terpilih |
| :--- | :--- | :--- |
| `LinearSVC` | `C`: `0.1, 0.25, 0.5, 1.0, 2.0, 5.0`; `class_weight`: `None, balanced`; `max_iter=5000` | `C=2.0`, `class_weight=None` |
| `RandomForestClassifier` | `n_estimators`: `100, 200, 300`; `max_depth`: `None, 30`; `min_samples_split`: `2, 5`; `class_weight`: `None, balanced` | `n_estimators=100`, `max_depth=None`, `min_samples_split=2`, `class_weight=None` |

Sumber: Implementasi Penalaan Parameter pada `src/eksperimen_komparasi.py` (2026).

Keluaran mentah `LinearSVC` masih berbentuk jarak *hyperplane* sehingga perlu dikalibrasi menjadi peluang [33], [34], [42]. Fungsi `_make_calibrated_svm_pipeline` membungkus vektorizer dan `LinearSVC` dalam `Pipeline` sebelum dikalibrasi lewat `CalibratedClassifierCV(method="sigmoid", cv=5)`. Berikutnya, `_run_stage4_domain_and_cross_corpus` menguji skenario kontrol 712 SMS umum vs korpus seimbang (`n = 45`) dan CV 260 teks pajak (`Stage 4A`). Tahap akhir mengevaluasi 1.360 teks eksternal unik (`Stage 4B`) serta korpus diperluas 2.519 baris pasca-Sastrawi (`Stage 4C`) [7], mengekspor `model_phishing_pajak.joblib`, dan menghitung SHAP (`n = 232`) [24], [25].

## 3.4 Implementasi Purwarupa Sistem Terpadu Tingkat Kesiapan Teknologi 6

Berkas `inference.py` memuat bundel `model_phishing_pajak.joblib` memakai `lru_cache(maxsize=1)` serta menormalisasi masukan memakai `clean_text` yang sama dengan pelatihan [41]. Di samping menghitung peluang `svm_prob`, modul menerapkan dua lapisan heuristik perpajakan. Pola `APK_PATTERN` (`r"\b[a-z0-9_.-]+\.apk\b"`) memindai berkas `.apk` dan langsung menaikkan status ke `TINGGI`. Adapun `URL_PATTERN` mensyaratkan TLD alfabetis supaya angka jam (`17.00`) dan nominal (`Rp1.500.000`) aman, sementara `is_official_djp_domain` hanya meloloskan host `pajak.go.id` atau `.pajak.go.id`. Hasil perkalian fitur TF-IDF dan `coef_` diterjemahkan oleh `_extract_top_triggers` menjadi alasan awam [24].

Layanan REST API di `api.py` dibangun di atas FastAPI Uvicorn beserta pengaturan CORS `allow_private_network=True`, *security headers*, dan pembatas laju permintaan (spesifikasi pada `Tabel L.6`). Antarmuka web *Cek Pesan Pajak* di `web/` memiliki tiga tab (**Cek Pesan**, **Web Resmi & Ciri Scam**, **Darurat .apk**), kotak **Cek Chat WhatsApp**, tombol **Cek Sekarang**, tiga prasetel (**File .apk Palsu**, **Link Pajak Palsu**, **Chat Resmi DJP**), serta info akademik di *footer*. Ekstensi *Manifest V3* di `extension/` [26] memindai gelembung obrolan minimal 8 karakter dan kartu `.apk` di *WhatsApp Web*, sesuai Lampiran `Gambar L.1`.

## 3.5 Skenario Pengujian Sistem dan Kesiapan Evaluasi

Integritas sistem diuji otomatis memakai Pytest 9.2.0 terhadap 23 skenario uji pada empat berkas di `tests/`. Modul `test_integritas_dataset.py` (6 kasus) dan suite eksperimen (7 kasus) mengunci keutuhan 10 *hash* SHA-256, deduplikasi Sastrawi, isolasi Platt, arah SHAP, `.joblib`, serta keunggulan akurasi atas kontrol SMS umum. Pada sisi layanan aplikasi, `tests/test_prototipe_api.py` mengeksekusi 10 skenario *black-box* (`UJI-01` s.d. `UJI-09` pada Lampiran `Tabel L.7`) mencakup kesiapan layanan, deteksi `.apk`/domain tiruan, pengecoh `pajak.go.id.evil.com`, penjagaan jam dan nominal, tolak spasi kosong (`422`), `POST /predict/batch` (3 masukan campuran berstatus `total=3` dengan spasi menghasilkan `"error"` serta tolak teks >5.000 karakter `422`), halaman web, dan *security headers*.
