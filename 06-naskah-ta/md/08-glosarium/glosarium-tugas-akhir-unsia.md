# Glosarium Tugas Akhir (Panduan Hafalan & Sidang)

**Judul TA**: *Komparasi Algoritma Support Vector Machine dan Random Forest dalam Deteksi Pesan Phishing WhatsApp Mengatasnamakan Otoritas Perpajakan*

---

## 1. Domain Perpajakan & Rekayasa Sosial
- **Phishing**: Upaya penipuan digital dengan menyamar sebagai pihak tepercaya (seperti DJP) untuk mencuri kredensial, data pribadi, atau uang korban.
- **Smishing**: Bentuk *phishing* yang dikirim melalui pesan singkat (SMS atau aplikasi pesan seperti WhatsApp).
- **Social Engineering (Rekayasa Sosial)**: Manipulasi psikologis korban (misalnya rasa panik akan denda/pemblokiran atau iming-iming restitusi) agar mau mengeklik tautan atau mengunduh berkas berbahaya.
- **DJP & KPP / KP2KP**: Direktorat Jenderal Pajak dan unit vertikalnya (Kantor Pelayanan Pajak / Kantor Pelayanan, Penyuluhan, dan Konsultasi Perpajakan) yang namanya sering dicatut pelaku.
- **Coretax (`coretaxdjp.pajak.go.id`)**: Sistem inti administrasi perpajakan DJP yang sering dijadikan narasi palsu ("pemutakhiran data Coretax").
- **M-Pajak**: Aplikasi resmi DJP untuk layanan pajak di ponsel; kerap ditiru dengan mengirim berkas `.apk` palsu via WhatsApp.
- **WhatsApp Blast Resmi DJP**: Layanan pengiriman pesan informasi/edukasi resmi DJP melalui WhatsApp yang sahih, sehingga tidak boleh salah diblokir oleh model deteksi.
- **EFIN (*Electronic Filing Identification Number*)**: Nomor identitas resmi terbitan DJP untuk layanan pajak elektronik; istilah ini sering dipakai penipu agar pesan tampak resmi.
- **Kode *Billing***: Kode identifikasi pembayaran pajak resmi; penipu kerap memalsukan narasi tagihan/kurang bayar memakai istilah ini.
- **Pemadanan NIK–NPWP**: Kebijakan integrasi Nomor Induk Kependudukan sebagai NPWP yang sering dijadikan umpan penipuan.
- **Berkas `.apk` (*Android Package Kit*)**: Format berkas instalasi aplikasi Android. Dalam kasus penipuan pajak, pelaku mengirim `.apk` palsu (misalnya berkedok surat tagihan) untuk mencuri OTP/akses perbankan.
- **Verifikasi Domain `pajak.go.id`**: Pengecekan apakah tautan di dalam pesan benar-benar mengarah ke domain resmi pemerintah Indonesia (`*.pajak.go.id`) atau domain tiruan.

---

## 2. Dataset, Kurasi & *Keyword Bias*
- **Korpus (*Corpus*)**: Kumpulan teks terstruktur yang digunakan untuk melatih dan menguji model NLP.
- **Korpus Dasar SMS (904 baris)**: Dataset publik SMS berbahasa Indonesia (Rahmi & Wibisono: **335** penipuan, **569** normal), hasil penyaringan dari total **1.143 baris CSV** setelah mengeksklusi **239** pesan promo/operator.
- **Korpus Spesifik Pajak (260 baris)**: Kumpulan pesan bertema perpajakan yang seimbang (**130** *phishing* dari **12 kategori modus** dan **130** pesan resmi/normal dari **10 kategori layanan**), dikurasi dari **65 dari 68 sumber publik** (2024–2026) tanpa data rahasia internal.
- **Dataset Gabungan Utama (1.164 mentah / 1.159 teks unik)**: Gabungan 904 korpus SMS dasar + 260 korpus spesifik pajak (`465` penipuan, `699` normal; setelah deduplikasi `5` baris Sastrawi identik tersisa **1.159** teks unik: `462` penipuan, `697` aman).
- ***Stratified Train-Test Split* (80:20)**: Pembagian 1.159 teks unik menjadi **927 data latih** dan **232 data uji** dengan menjaga proporsi kelas tetap sama di kedua bagian.
- ***Keyword Bias* (Bias Kata Kunci)**: Kondisi saat model salah menganggap kata netral bertema pajak (misalnya *"pajak"*, *"NPWP"*, *"DJP"*) sebagai ciri penipuan karena model belum pernah melihat contoh pesan pajak resmi yang aman.
- **Uji Kontrol & Studi Ablasi (*Ablation Study*)**: Pada **45 pesan uji pajak (`n = 45`)**: pelatihan kontrol hanya dengan `712` SMS umum mencatat akurasi **42,22%** (`LinearSVC`, `11/21` pesan DJP salah terblokir) dan **33,33%** (*Random Forest*), sedangkan korpus seimbang melonjakkan kedua model ke **95,56%** (`20/21` resmi DJP lolos; `ROC-AUC 0,9960` pada `LinearSVC`). Pada studi ablatif 10-Fold CV, penghapusan `token_apk`/`token_url` menurunkan *F1-Score* `LinearSVC` **1,35 poin** (`97,16%` ke `95,81%`), sedangkan unigram saja menurunkan **1,22 poin** (`95,94%`).
- **Uji Lintas-Korpus (`1.360` eksternal & `2.519` diperluas)**: Uji *zero-shot* pada `1.360` pesan unik eksternal (Theodorus & Saragih) mencatat *Recall* `80,28%` pada `LinearSVC`, lalu akurasi pulih ke **96,03%** vs **92,46%** saat dilatih ulang pada `2.519` baris diperluas.
- **SHA-256 *Checksum***: Sidik jari kriptografis 10 berkas dataset pada `Katalog Asal Sumber Data.csv` untuk menjamin integritas data tidak berubah selama riset.

---

## 3. Pra-pengolahan Teks (NLP) & Ekstraksi Fitur
- **NLP (*Natural Language Processing*)**: Cabang kecerdasan buatan agar komputer dapat memahami dan mengolah bahasa manusia (teks pesan WhatsApp).
- ***Case Folding***: Menyeragamkan seluruh huruf teks menjadi huruf kecil agar `"PAJAK"` dan `"pajak"` dianggap sama.
- **Tokenisasi Khusus (`token_apk` & `token_url`)**: Mengubah penyebutan berkas `.apk` menjadi token `token_apk` dan tautan web menjadi `token_url` sebelum tanda baca dihapus, sehingga sinyal berbahaya tetap tertangkap model.
- **Pembersihan Karakter Nonalfanumerik**: Menghapus simbol atau tanda baca selain alfanumerik, spasi, dan garis bawah (`r"[^a-z0-9\s_]"`).
- ***Stopword Removal***: Menghapus kata penghubung/umum yang terlalu sering muncul berdasarkan Sastrawi sambil mengecualikan `token_apk` dan `token_url`.
- ***Stemming* Sastrawi**: Mengubah kata alfabetis lebih dari dua huruf ke bentuk dasarnya (misalnya *"pemutakhiran"* menjadi *"mutakhir"*) memakai algoritma *Confix-Stripping*.
- **TF-IDF (*Term Frequency–Inverse Document Frequency*)**: Metode pembobotan kata ternormalisasi L2; memberi bobot tinggi pada istilah spesifik penciri *phishing*.
- ***N-gram* `(1, 2)` (Maks. 3.000 Fitur)**: Pengambilan fitur 1 kata (*unigram*) dan 2 kata berurutan (*bigram*), dibatasi maksimal 3.000 fitur terpenting pada lipatan latih.
- ***Sparse Matrix* (Matriks Jarang)**: Representasi vektor TF-IDF yang sebagian besar nilainya nol karena tiap pesan pendek hanya memuat sebagian kecil dari 3.000 kosakata.

---

## 4. Algoritma *Machine Learning* yang Dikomparasikan
- ***Supervised Learning* (Pembelajaran Terawasi)**: Pelatihan model menggunakan data berlabel biner (`1` = *phishing*, `0` = aman/resmi).
- **SVM (*Support Vector Machine* — `LinearSVC`)**: Algoritma pencari *hyperplane* dengan *margin* maksimum pada ruang fitur berdimensi tinggi. Hasil optimal (`C=2.0`): *10-Fold CV* **F1 97,16% ± 2,41%** (*Accuracy* **97,74%**), *holdout* Platt **95,69%** (*ROC-AUC* **0,9957**; *PR-AUC* **0,9943**; *Brier Score* **0,02542**; *Log Loss* **0,09186**), serta *F1-Score* **98,17%** pada CV 260 korpus pajak.
- ***Platt Scaling* (Kalibrasi Probabilitas)**: Teknik regresi logistik (`CalibratedClassifierCV`, `method="sigmoid"`, `cv=5`) dalam `Pipeline` terisolasi untuk mengubah jarak *hyperplane* `LinearSVC` menjadi peluang 0%–100%.
- ***Random Forest Classifier***: Algoritma *ensemble* dari banyak pohon keputusan (*bagging*). Setelan terbaik (`n_estimators=100`, `max_depth=None`, `min_samples_split=2`): *10-Fold CV* **F1 94,07% ± 2,92%** (*Accuracy* **95,25%**), *holdout* **96,55%** (*ROC-AUC* **0,9936**; *Brier Score* **0,04214**; *Log Loss* **0,15870**), dan **92,46%** di korpus diperluas 2.519 baris.

---

## 5. Metrik Evaluasi & Validasi
- ***Confusion Matrix***: Tabel 2×2 pencocokan prediksi vs label asli (`TP`, `TN`, `FP`, `FN`). *False Negative* paling krusial diwaspadai karena meloloskan pesan *phishing*, sedangkan *False Positive* memblokir pesan resmi DJP.
- ***Accuracy*, *Precision*, *Recall*, *F1-Score***: Empat metrik dasar klasifikasi biner; di holdout `n = 232` selisih diskrit 1–2 sampel antara `LinearSVC` Platt (`95,69%`) dan *Random Forest* (`96,55%`) masih di dalam simpangan baku CV (`± 2,41%`).
- ***10-Fold Stratified Cross-Validation***: Validasi silang 10 lipatan dengan TF-IDF terisolasi di tiap lipatan untuk mencegah kebocoran data (*data leakage*).
- **ROC-AUC, PR-AUC, *Brier Score*, & *Log Loss***: Mengukur daya pisah peringkat probabilitas dan seberapa akurat nilai peluang terkalibrasi terhadap kejadian nyata (`LinearSVC` Platt menekan *Brier Score* `39,68%` lebih rendah daripada *Random Forest*).

---

## 6. Arsitektur Purwarupa & Kesiapan Teknologi
- **TKT Level 6 (*Tingkat Kesiapan Teknologi*)**: Purwarupa sistem terpadu yang telah didemonstrasikan pada lingkungan simulasi relevan (*Permenristekdikti No. 42 Tahun 2016*), lulus `23/23` pengujian Pytest dalam `21,51` detik.
- **REST API (`FastAPI` & `Jalankan Server.bat`)**: Layanan *backend* (`allow_private_network=True`, *security headers*, *rate limiter*) berlatensi rata-rata **34,991 ms/pesan** (*P95* **48,082 ms**) pada `POST /predict` dan **26,313 ms/pesan** pada *batch* 50 pesan.
- **Ekstensi Peramban *WhatsApp Web* (`Manifest V3`)**: Pengaya Chrome/Edge (`background.js`, `content.js`, `popup.html`) yang memindai gelembung pesan (`>= 8` karakter) dan lampiran `.apk` secara langsung tanpa salin-tempel.
- **Antarmuka Web *Cek Pesan Pajak* (`web/`)**: Aplikasi web tiga tab (*Cek Pesan*, *Web Resmi & Ciri Scam*, *Darurat .apk*) berprasetel cepat (*File .apk Palsu*, *Link Pajak Palsu*, *Chat Resmi DJP*), sorotan bahaya interaktif, dan modal info akademik di *footer*.
- ***Explainable Detection* (XAI & SHAP)**: Penjelasan pemicu bahaya berbahasa awam berdasarkan perkalian TF-IDF dan `coef_` `LinearSVC`, divalidasi global melalui `LinearExplainer` dan `TreeExplainer` SHAP pada `n = 232`.
- **`Joblib`**: Pustaka Python untuk menyerialisasi bundel model dan vektorizer TF-IDF terkalibrasi (`model_phishing_pajak.joblib`).
