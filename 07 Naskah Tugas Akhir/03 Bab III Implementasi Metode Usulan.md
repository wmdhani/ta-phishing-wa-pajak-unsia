# BAB III IMPLEMENTASI METODE USULAN

## 3.1 Arsitektur Implementasi Metode Usulan

Implementasi metode usulan pada penelitian ini menerjemahkan kerangka teoretis serta enam tahapan prosedur operasional pada Bab II ke dalam ekosistem perangkat lunak yang terstruktur. Seluruh pemrosesan dibangun memakai Python versi 3.11.9 dengan memisahkan modul kurasi korpus, pelatihan komparatif, serta layanan antarmuka purwarupa [40]. Pemisahan itu menjaga konsistensi teks sejak pelatihan.

Arsitektur sistem terbagi menjadi dua alur kerja utama yang terhubung melalui bundel model terserialisasi, yakni alur pelatihan luring dan alur layanan daring. Pada alur luring, seluruh bahan korpus dikurasi, dibersihkan dengan Sastrawi, diubah menjadi vektor TF-IDF tiga ribu fitur, lalu dilatih memakai `LinearSVC` dan `RandomForestClassifier` [6], [36], [37]. Alur daring memuat model terlatih ke peladen FastAPI untuk menyajikan antarmuka web *Cek Pesan Pajak* dan ekstensi *WhatsApp Web* [26].

![Arsitektur Sistem Terpadu Deteksi Phishing WhatsApp Perpajakan](Aset Gambar/Gambar 3.1 Arsitektur Sistem Terpadu.png)

Gambar 3.1 Arsitektur Sistem Terpadu Deteksi *Phishing* WhatsApp Perpajakan.

Rancangan pada Gambar 3.1 memperlihatkan bahwa seluruh logika klasifikasi, ekstraksi kata pemicu *explainable AI*, penerjemah alasan bahasa awam, serta pemeriksaan heuristik keamanan dipusatkan pada `inference.py`. Pendekatan terpusat tersebut menjaga konsistensi aturan praproses dan format respons antara web *Cek Pesan Pajak* (`web/`) dan ekstensi *Manifest V3*. Prasetel contoh pesan dan ringkasan evaluasi model turut disajikan langsung oleh peladen FastAPI yang sama.

Untuk mempermudah penelusuran antara rancangan metodologi pada Bab II dan kode program yang dibangun, setiap tahapan penelitian dipetakan secara eksplisit ke berkas sumber spesifik di dalam repositori. Struktur modular tersebut memastikan proses pengumpulan data, pelatihan model, dan layanan purwarupa dapat diuji serta dipelihara secara terpisah tanpa saling mengganggu. Pemetaan lengkap antara modul kode program, peran fungsionalnya, serta kaitannya dengan tahapan penelitian disajikan pada Tabel 3.1.

Tabel 3.1 Pemetaan Modul Kode Sumber terhadap Tahapan Metodologi Penelitian

| Berkas / Direktori Modul | Tahapan Metodologi | Peran Teknis dalam Sistem |
| :--- | :--- | :--- |
| `src/korpus_pajak.py` | Kurasi Sumber Perpajakan | Menyimpan metadata enam puluh delapan sumber, tiga puluh satu indikator penipuan DJP, dan dua ratus enam puluh teks pajak |
| `src/kurasi_dataset.py` | Konstruksi Korpus & Provenans | Membangun dataset induk 1.164 baris, korpus diperluas 2.521 baris, dan katalog provenans SHA-256 |
| `src/eksperimen_baseline.py` | Praproses & Model Dasar | Menyediakan fungsi `clean_text` Sastrawi dan uji *baseline* 80:20 `LinearSVC` serta `RandomForestClassifier` |
| `src/eksperimen_komparasi.py` | Penalaan, Kalibrasi, & Evaluasi | Menjalankan `StratifiedKFold` 10-lipatan, pencarian *grid* 36 konfigurasi, kalibrasi Platt, studi ablatif, dan ekspor `.joblib` |
| `06 Prototipe Aplikasi/inference.py` | Mesin Inferensi Terpadu | Memuat `model_phishing_pajak.joblib`, menjalankan heuristik `.apk` serta domain `pajak.go.id`, dan menyusun alasan ramah awam serta sorotan teks |
| `06 Prototipe Aplikasi/api.py` & `Jalankan Server.bat` | Layanan *Backend*, Web, & Peluncur | Menyajikan antarmuka web *Cek Pesan Pajak* (`/`) serta *endpoint* API `/health`, `/api/*`, `/predict`, dan `/predict/batch` |
| `06 Prototipe Aplikasi/web/` | Antarmuka Web Pengguna Awam | Menyediakan halaman web responsif (`index.html`, `styles.css`, `app.js`) dengan pratinjau chat WA, sorotan bahaya, panduan darurat `.apk`, dan modal evaluasi TA |
| `06 Prototipe Aplikasi/extension/` | Ekstensi Peramban *WhatsApp Web* | Memindai pesan di `web.whatsapp.com`, meneruskan lewat `background.js`, dan menampilkan lencana risiko berbahasa awam (*Manifest V3*) |
| `tests/` | Verifikasi Otomatis Sistem | Menjalankan dua puluh pengujian `pytest` untuk integritas korpus, reproduksi metrik, serta pengujian *black-box* API dan web |

Sumber: Dokumentasi Rekayasa Perangkat Lunak Penelitian (2026).

## 3.2 Implementasi Kurasi Korpus dan Praproses Teks

Implementasi tahap data diawali penyusunan korpus domain perpajakan melalui berkas `src/korpus_pajak.py` dan `src/kurasi_dataset.py`. Sebanyak enam puluh delapan halaman web otoritatif dari DJP, media perpajakan, dan kanal pemeriksa fakta diambil, lalu dibersihkan dari teks navigasi berulang memakai `strip_djp_boilerplate` [2], [5]. Dari jumlah itu, tersaring enam puluh lima sumber unik menjadi dua ratus enam puluh pesan dari dua belas modus penipuan dan sepuluh layanan resmi DJP. Jumlah kedua kelas disusun seimbang.

Modul `src/kurasi_dataset.py` menggabungkan dua ratus enam puluh teks pajak tersebut dengan sembilan ratus empat SMS bahasa Indonesia dari korpus Rahmi dan Wibisono [6]. Sebanyak dua ratus tiga puluh sembilan iklan promo disisihkan terlebih dahulu. Penggabungan ini membentuk korpus induk biner sebanyak seribu seratus enam puluh empat baris, terdiri atas empat ratus enam puluh lima pesan penipuan (`1`) dan enam ratus sembilan puluh sembilan pesan normal (`0`). Keutuhan seluruh artefak korpus dijaga memakai sepuluh catatan *hash* SHA-256 pada `Katalog Asal Sumber Data.csv`.

Selain korpus induk, fungsi `build_combined_datasets` merakit korpus perluasan untuk menguji generalisasi model lintas sumber. Korpus tersebut menggabungkan himpunan induk, korpus biner Theodorus (`Label` `0` dan `2` dipetakan ke `0` dan `1`), serta korpus Saragih (`non-spam` dan `penipuan`) menjadi 4.255 baris awal [7]. Penyaringan duplikat pada `clean_text` menyisihkan 1.734 baris duplikat, terdiri atas 5 duplikat internal Rahmi dan 1.729 duplikat internal maupun lintas sumber. Himpunan akhir memuat 2.521 baris unik (822 penipuan dan 1.699 aman).

Pada jalur praproses, setiap teks masukan saat pelatihan maupun inferensi melewati fungsi `clean_text` dalam modul `src/eksperimen_baseline.py`. Kamus kata henti diambil dari `StopWordRemoverFactory`, sedangkan daftar kata dasar `StemmerFactory` diubah dari tipe daftar menjadi himpunan (`set`) berakselerasi `lru_cache` dua puluh ribu kata agar pencarian berjalan dalam waktu konstan $O(1)$ [37]. Urutan transformasi teks mengikuti enam langkah berikut:

a) Seluruh karakter diubah menjadi huruf kecil melalui metode `lower()`. Langkah ini menyeragamkan representasi kata tanpa membedakan huruf kapital di awal kalimat ataupun di tengah pesan.

b) Pola berkas Android berakhiran `.apk` (`r"\.apk\b"`) diganti lebih dahulu menjadi `token_apk` sebelum pendeteksian tautan. Urutan ini mencegah nama berkas seperti `coretax.id.apk` tertelan sebagai alamat situs web.

c) Pola alamat tautan web, baik berawalan `http`, `https`, `www`, penyingkat `bit.ly`, maupun domain umum berakhiran `.go.id`, `.co.id`, serta `.xyz`, dikonversi menjadi token khusus `token_url`.

d) Karakter selain huruf alfabet kecil, angka, spasi, dan garis bawah dihapus dengan ekspresi reguler `r"[^a-z0-9\s_]"` sehingga tanda baca terbuang sementara penanda `token_apk` dan `token_url` tetap utuh.

e) Seluruh token diperiksa terhadap himpunan `SPECIAL_TOKENS` (`token_apk` dan `token_url`) agar langsung dipertahankan, sedangkan token biasa yang tercatat di dalam kamus `STOP_WORDS` Sastrawi dibuang dari rangkaian kata.

f) Setiap kata alfabetis sepanjang lebih dari dua huruf (`tok.isalpha() and len(tok) > 2`) dikembalikan ke bentuk kata dasar memakai algoritma Nazief-Adriani pada Sastrawi 1.0.1 [37]. Token kemudian disatukan kembali menjadi string bersih.

Guna mendukung studi ablatif pada tahap evaluasi, modul `src/eksperimen_komparasi.py` turut menyiapkan dua varian praproses teks pembanding di samping kolom utama `teks_sastrawi`. Kolom `clean_text` dari `src/kurasi_dataset.py` merepresentasikan praproses tanpa penghapusan *stopword* dan tanpa *stemming* Sastrawi untuk skenario `2_Tanpa_Sastrawi`. Sementara itu, fungsi `clean_text_without_entity_tokens` menghasilkan kolom `teks_tanpa_token_entitas` dengan menghapus pola URL serta berkas `.apk` menjadi spasi kosong untuk skenario `1_Tanpa_Token_Entitas`.

## 3.3 Implementasi Pelatihan Model, Penyetelan Hiperparameter, dan Kalibrasi

Tahap pelatihan dan evaluasi komparatif diimplementasikan dalam berkas `src/eksperimen_komparasi.py` dengan menstandarkan `RANDOM_STATE` sebesar empat puluh dua demi keterulangan hasil [40]. Data induk sebanyak 1.164 baris dipisahkan terstratifikasi 80:20 menjadi 931 data latih dan 233 data uji. Pada tahap *baseline*, `LinearSVC` bawaan dan `RandomForestClassifier` dua ratus pohon dilatih pada vektor TF-IDF unigram-bigram maksimal tiga ribu fitur data latih [36].

Untuk mencegah kebocoran informasi pembobotan kata selama validasi silang sepuluh lipatan (`StratifiedKFold` dengan `shuffle=True` dan `random_state=42`), diimplementasikan fungsi `_precompute_tfidf_folds` [38]. Fungsi tersebut membangun objek `TfidfVectorizer(ngram_range=(1, 2), max_features=3000)` yang terpisah di dalam setiap lipatan latih sebelum mengubah data validasi lipatan bersangkutan. Selanjutnya, fungsi `_run_grid_over_folds` mengevaluasi seluruh kombinasi hiperparameter secara menyeluruh di atas sepuluh lipatan yang sudah terisolasi tersebut lalu mengurutkan kandidat berdasarkan nilai rata-rata *F1-Score*, akurasi, dan *ROC-AUC*.

Sebanyak tiga puluh enam konfigurasi parameter diuji dalam pencarian *grid*, terdiri atas dua belas kombinasi untuk `LinearSVC` (`max_iter=5000`) dan dua puluh empat kombinasi untuk `RandomForestClassifier`. Pencarian *grid* tersebut memilih `C=5.0` tanpa pembobotan kelas seimbang pada `LinearSVC`, serta dua ratus pohon tanpa batas kedalaman maksimum dengan syarat pemecahan simpul minimum lima sampel pada `RandomForestClassifier`. Rincian lengkap ruang pencarian dan parameter terpilih tercantum pada Tabel 3.2.

Tabel 3.2 Konfigurasi Ruang Pencarian Hiperparameter dan Parameter Terpilih

| Algoritma Klasifikasi | Ruang Pencarian Parameter (`_run_grid_over_folds`) | Konfigurasi Terpilih |
| :--- | :--- | :--- |
| `LinearSVC` | `C`: `0.1, 0.25, 0.5, 1.0, 2.0, 5.0`; `class_weight`: `None, balanced`; `max_iter=5000` | `C=5.0`, `class_weight=None` |
| `RandomForestClassifier` | `n_estimators`: `100, 200, 300`; `max_depth`: `None, 30`; `min_samples_split`: `2, 5`; `class_weight`: `None, balanced` | `n_estimators=200`, `max_depth=None`, `min_samples_split=5`, `class_weight=None` |

Sumber: Implementasi Penalaan Parameter pada `src/eksperimen_komparasi.py` (2026).

Oleh karena keluaran fungsi keputusan `LinearSVC` berupa jarak terhadap bidang pemisah dan belum berwujud peluang probabilitas, diterapkan kalibrasi sigmoid Platt memakai `CalibratedClassifierCV(method="sigmoid", cv=5)` [33], [34], [42]. Kalibrasi lima lipatan tersebut mengubah nilai margin linear menjadi probabilitas kelas penipuan pada rentang nol hingga satu sehingga setara untuk dibandingkan dengan `predict_proba` milik *Random Forest*. Mutu kesesuaian peluang selanjutnya dinilai melalui perhitungan *Brier Score* dan *Log Loss* pada himpunan uji dua ratus tiga puluh tiga pesan [39].

Setelah penalaan dan kalibrasi selesai, fungsi `_run_stage4_domain_and_cross_corpus` menjalankan tiga uji ketahanan tambahan. Pertama, kinerja model diukur pada empat puluh empat sampel pajak di data uji serta validasi silang sepuluh lipatan atas dua ratus enam puluh teks pajak (`Stage 4A`). Kedua, model produksi pada 1.164 baris diuji secara *zero-shot* pada 1.362 pesan eksternal (`Stage 4B`). Pengujian kemudian diulang pada korpus diperluas 2.521 baris (`Stage 4C`) [7].

Pada tahap akhir jalur luring, vektorizer TF-IDF, `LinearSVC` linear murni, `LinearSVC` terkalibrasi Platt, dan `RandomForestClassifier` yang telah dilatih penuh pada 1.164 baris dikemas ke satu kamus Python lalu disimpan memakai Joblib 1.6.0 (`compress=3`) ke `06 Prototipe Aplikasi/model_phishing_pajak.joblib`. Selanjutnya, fungsi `_build_feature_and_error_tables` dan `_compute_shap_table` mengekstrak koefisien fitur teratas, merangkum sampel salah prediksi, serta menghitung nilai SHAP (`LinearExplainer` dan `TreeExplainer`) pada 233 data uji [24], [25].

## 3.4 Implementasi Purwarupa Sistem Terpadu Tingkat Kesiapan Teknologi 6

Seluruh subsistem aplikasi purwarupa ditempatkan pada direktori `06 Prototipe Aplikasi/` guna memenuhi kriteria demonstrasi dalam lingkungan simulasi yang relevan sesuai Tingkat Kesiapan Teknologi enam [41]. Lapisan inti inferensi pada berkas `inference.py` memuat bundel `model_phishing_pajak.joblib` secara efisien ke memori menggunakan mekanisme `lru_cache(maxsize=1)`. Setiap pesan teks yang masuk dibersihkan memakai fungsi `clean_text` yang sama dengan jalur pelatihan, diubah menjadi matriks TF-IDF, lalu dihitung peluang *phishing*-nya oleh model `svm_calibrated` maupun pembanding `random_forest`.

Di samping inferensi pembelajaran mesin, fungsi `analyze_urls_and_apk` dan `predict_message` pada `inference.py` menjalankan dua lapisan aturan heuristik perpajakan. Lapisan pertama memindai teks mentah memakai `APK_PATTERN` (`r"\b[a-z0-9_.-]+\.apk\b"`) guna menangkap lampiran aplikasi berbahaya. Lapisan kedua mengekstrak tautan melalui `URL_PATTERN` bersyarat akhiran *top-level domain* alfabetis pada tautan tanpa awalan `http` atau `www` sehingga angka jam `17.00` maupun nominal `Rp1.500.000` tidak ikut tertandai.

Setiap domain hasil ekstraksi terlebih dahulu diproses oleh fungsi `_extract_domain` memakai `urlparse` agar tautan tanpa awalan `http://` tetap terbaca nama hostnya secara konsisten. Selanjutnya, fungsi `is_official_djp_domain` hanya mengembalikan nilai benar apabila nama host tepat sama dengan `pajak.go.id` atau berakhiran `.pajak.go.id`. Dengan aturan ketat tersebut, teknik pengecohan domain tiruan seperti `pajak.go.id.evil.com` tetap tertandai sebagai domain eksternal mencurigakan di antarmuka pengguna.

Penetapan status akhir dan tingkat risiko pada `predict_message` menggabungkan peluang kalibrasi `svm_prob` dengan temuan heuristik secara deterministik. Pada kondisi dasar, pesan diberi label `1` apabila `svm_prob >= 0.5`. Namun, jika `has_apk` bernilai benar meskipun `svm_prob < 0.75`, sistem melakukan eskalasi otomatis menjadi `label = 1` dan risiko `TINGGI`. Tanpa berkas `.apk`, risiko ditetapkan `TINGGI` jika `svm_prob >= 0.75`, `SEDANG` jika `svm_prob >= 0.50` atau ada `suspicious_domains`, dan `RENDAH` jika aman.

Guna menyajikan penjelasan yang ramah bagi masyarakat umum, fungsi `_extract_top_triggers` menghitung kontribusi tiap kata atau frasa dari hasil kali bobot TF-IDF dan koefisien `svm_linear.coef_` [24]. Kontribusi tersebut lalu dipetakan ke kelompok kata pemicu, yakni desakan waktu, ancaman denda, serta ajakan verifikasi. Dari pemetaan itu, sistem menyusun satu vonis risiko utama, sorotan khusus pada berkas `.apk` atau tautan, serta daftar alasan dan langkah pencegahan berbahasa sehari-hari.

Layanan *backend* dan peladen web pada berkas `api.py` dibangun di atas kerangka kerja FastAPI dengan peladen ASGI Uvicorn, dilengkapi skrip pintas `Jalankan Server.bat` untuk memudahkan pengaktifan lokal. Kebijakan *Cross-Origin Resource Sharing* mengatur `allow_private_network=True` agar permintaan `GET`, `POST`, dan `OPTIONS` dari peramban lokal, halaman publik `https://web.whatsapp.com`, maupun ekstensi `chrome-extension://*` tetap diterima secara aman. Rincian kontrak layanan API tersaji pada Tabel 3.3.

Tabel 3.3 Spesifikasi Titik Akhir Layanan Web dan REST API FastAPI (`api.py`)

| Metode & Jalur | Skema Masukan | Struktur Keluaran Utama | Peran dalam Arsitektur |
| :--- | :--- | :--- | :--- |
| `GET /` | Tanpa badan permintaan | Berkas HTML antarmuka web *Cek Pesan Pajak* | Menyajikan aplikasi web utama bagi masyarakat awam |
| `GET /health` | Tanpa badan permintaan | Status `ok`, `models_loaded`, dan `metadata` korpus latih | Pemeriksaan kesiapan layanan oleh halaman web dan popup ekstensi |
| `GET /api/presets` & `/api/academic-summary` | Tanpa badan permintaan | Daftar prasetel pesan uji, metadata model, dan baris `tabel_komparasi_utama.csv` | Mengisi tombol contoh siap uji serta modal info akademik di footer |
| `POST /predict` | JSON `text` (1 sampai 5.000 karakter) dan `top_k` (1 sampai 20) | Label, `risk_level`, `risk_title`, `plain_reasons`, `highlights`, `trigger_words`, dan `action_steps` | Titik akhir inferensi tunggal bagi web *Cek Pesan Pajak* dan ekstensi |
| `POST /predict/batch` | JSON daftar `texts` (1 sampai 200 pesan) dan `top_k` | Jumlah total dan daftar hasil prediksi terindeks per baris | Titik akhir pemrosesan pesan massal terstruktur |

Sumber: Implementasi Layanan API pada `06 Prototipe Aplikasi/api.py` (2026).

Antarmuka web *Cek Pesan Pajak* pada `06 Prototipe Aplikasi/web/` (`index.html`, `styles.css`, `app.js`) dirancang memakai bahasa Indonesia sehari-hari untuk masyarakat awam. Elemen teknis yang tidak dibutuhkan pengguna umum, meliputi pengaturan URL *endpoint*, metadata model, unggah CSV massal, probabilitas ganda, dan tabel koefisien TF-IDF, dihapus dari layar utama. Sebagai gantinya, ringkasan evaluasi tersebut diletakkan di balik tautan *Info Akademik dan Evaluasi Model* pada bagian *footer* untuk keperluan demo sidang.

Tata letak *Cek Pesan Pajak* memakai navigasi tab ringkas (*Cek Pesan*, *Kanal Resmi dan Ciri Scam*, serta *Darurat .apk*) agar layar utama tetap lega. Setelah pesan dipindai lewat kotak tempel atau tiga contoh cepat, pratinjau chat menyorot berkas `.apk` dan tautan disertai chip kata pemicu di bawahnya. Hasil dilengkapi alasan singkat, saran aman, tombol bagikan ke WhatsApp, panduan darurat `.apk`, daftar situs `pajak.go.id`, serta empat ciri penipuan.

![Rancangan Antarmuka Web Cek Pesan Pajak dan Ekstensi WhatsApp Web](Aset Gambar/Gambar 3.2 Rancangan Antarmuka Purwarupa dan Ekstensi.png)

Gambar 3.2 Rancangan Antarmuka Web *Cek Pesan Pajak* dan Ekstensi *WhatsApp Web*.

Integrasi langsung pada peramban diwujudkan melalui ekstensi Chrome berarsitektur *Manifest V3* di folder `extension/` yang tersusun atas enam berkas, yaitu `manifest.json`, `background.js`, `content.js`, `styles.css`, `popup.html`, dan `popup.js` [26]. Skrip `content.js` memakai `MutationObserver` untuk memindai gelembung pesan masuk minimal delapan karakter, kartu lampiran berkas `.apk`, maupun tautan pendek, serta mendukung uji mandiri pada pesan keluar bertema pajak. Saat tombol *Cek Pesan Pajak* ditekan, permintaan dikirim lewat *service worker* `background.js` ke `http://127.0.0.1:8000/predict` agar lencana risiko berbahasa awam tampil seperti pada Gambar 3.2.

## 3.5 Skenario Pengujian Sistem dan Kesiapan Evaluasi

Keandalan seluruh jalur data, eksperimen pemodelan, dan antarmuka purwarupa diverifikasi otomatis memakai kerangka kerja Pytest 9.2.0 lewat dua puluh kasus uji pada empat berkas terpisah guna mencegah regresi kode. Berkas `test_integritas_dataset.py` menguji jumlah baris lima korpus mentah, validitas enam puluh delapan hasil *scraping*, serta keseimbangan dua ratus enam puluh data pajak. Pengujian juga memastikan kecocokan gabungan biner 1.164 maupun 2.521 baris serta sepuluh *hash* SHA-256.

Pengujian pipeline pembelajaran mesin diwakili dua kasus uji dalam `test_eksperimen_baseline.py` dan empat kasus uji dalam `test_eksperimen_komparasi.py`. Pengujian itu memvalidasi pelestarian `token_apk` serta `token_url` pada `clean_text` dan mengunci reproduksi metrik dasar `LinearSVC` maupun `RandomForestClassifier`. Skrip turut memastikan kelayakan *Brier Score* di bawah `0.05`, sifat penjumlahan probabilitas Platt, serta keandalan bundel `model_phishing_pajak.joblib` memprediksi penipuan pajak. Peluang prediksinya disyaratkan melebihi delapan puluh persen.

Khusus lapisan purwarupa TKT 6, berkas `tests/test_prototipe_api.py` menjalankan sembilan pengujian *black-box* memakai `TestClient` FastAPI. Skenario tersebut mencakup uji kesehatan layanan, deteksi `.apk`, identifikasi domain tiruan, validasi domain `pajak.go.id`, serta penolakan domain pengecoh. Pengujian turut memeriksa penjagaan pola angka jam maupun nominal, penolakan masukan kosong, pemrosesan *batch*, serta ketersediaan antarmuka web. Matriks pengujian lengkapnya tercantum pada Tabel 3.4.

Tabel 3.4 Matriks Skenario Pengujian Otomatis Purwarupa dan Integritas Sistem

| Kode Uji | Berkas / Subjek Pengujian | Skenario Masukan & Kondisi Uji | Keluaran yang Diharapkan |
| :--- | :--- | :--- | :--- |
| `UJI-01` | `test_prototipe_api.py` (`GET /health`) | Permintaan cek kesiapan peladen API | Status HTTP 200 dengan `LinearSVC+Platt` aktif |
| `UJI-02` | `test_prototipe_api.py` (`POST /predict`) | Pesan memuat berkas `Coretax_DJP_Update.apk` | Label `1`, `has_apk=True`, risiko `TINGGI`, alasan awam & sorotan `.apk` terisi |
| `UJI-03` | `test_prototipe_api.py` (`POST /predict`) | Pesan tautan palsu `pajak-djp-verifikasi.xyz` | Label `1`, domain tercatat di `suspicious_domains` tanpa angka `17.00` |
| `UJI-04` | `test_prototipe_api.py` (`POST /predict`) | Pengumuman resmi `djponline.pajak.go.id` | Label `0`, risiko `RENDAH`, domain di `official_domains` tanpa domain curiga |
| `UJI-05` | `test_prototipe_api.py` (`is_official_djp_domain`) | Uji pengecohan `pajak.go.id.evil.com` vs domain sah | Mengembalikan `False` untuk domain tiruan, `True` untuk sah |
| `UJI-06` | `test_prototipe_api.py` (`POST /predict`) | Pengiriman teks berisi spasi kosong | Ditolak dengan kode status HTTP 422 (*Unprocessable Entity*) |
| `UJI-07` | `test_prototipe_api.py` (`POST /predict/batch`) | Pengiriman dua teks campuran *phishing* dan resmi | Status HTTP 200 dengan `total=2` dan dua objek hasil |
| `UJI-08` | `test_prototipe_api.py` (penjagaan pola angka) | Pesan resmi memuat pukul `16.00` dan `Rp1.500.000` | `suspicious_domains` kosong dan status tetap `RENDAH` |
| `UJI-09` | `test_prototipe_api.py` (`GET /` & `/api/*`) | Permintaan halaman web utama, prasetel, dan ringkasan TA | Status HTTP 200 menyajikan *Cek Pesan Pajak*, 3 prasetel, dan tabel evaluasi |
| `UJI-10` | `test_integritas_dataset.py` & eksperimen | Validasi lima dataset mentah, SHA-256, dan metrik `.joblib` | Seluruh sebelas pengujian data dan model lulus tanpa galat |

Sumber: Implementasi Pengujian Otomatis `pytest` pada Direktori `tests/` (2026).

Bersamaan dengan verifikasi fungsional, skrip `eksperimen_komparasi.py` menjalankan enam konfigurasi studi ablatif untuk mengisolasi pengaruh fitur, mencakup `1_Tanpa_Token_Entitas`, `2_Tanpa_Sastrawi`, `3_Unigram_Saja`, `4_Utama_MaxFeatures_1500`, `5_Konfigurasi_Utama_3000`, dan `6_Utama_MaxFeatures_5000`. Seluruh artefak keluaran tersimpan terstruktur pada direktori `05 Hasil Evaluasi/` berupa enam grafik beresolusi tinggi, tujuh berkas tabel CSV, dan laporan JSON lengkap. Analisis hasilnya dibahas pada Bab IV.

---

# DAFTAR PUSTAKA

[2] Direktorat Jenderal Pajak, “Penyebarluasan Informasi Mengenai Coretax (Pengumuman Nomor PENG-32/PJ.09/2024),” *Portal Resmi Direktorat Jenderal Pajak Kementerian Keuangan Republik Indonesia*, Nov. 2024. [Online]. Available: https://pajak.go.id/id/pengumuman/penyebarluasan-informasi-mengenai-coretax

[5] Direktorat Jenderal Pajak, “Waspada penipuan yang mengatasnamakan Direktorat Jenderal Pajak (Pengumuman Nomor PENG-31/PJ.09/2024 s.d. PENG-18/PJ.09/2026),” *Portal Resmi Direktorat Jenderal Pajak Kementerian Keuangan Republik Indonesia*, 2026. [Online]. Available: https://www.pajak.go.id/id/pengumuman/waspada-penipuan-yang-mengatasnamakan-direktorat-jenderal-pajak

[6] F. Rahmi and Y. Wibisono, “Aplikasi SMS spam filtering pada Android menggunakan algoritma Naïve Bayes,” Skripsi, Dept. Pendidikan Ilmu Komputer, Universitas Pendidikan Indonesia, Bandung, 2016. [Online]. Available: https://repository.upi.edu/26936/

[7] A. Theodorus, T. K. Prasetyo, R. Hartono, and D. Suhartono, “Short Message Service (SMS) spam filtering using machine learning in Bahasa Indonesia,” in *Proc. 3rd East Indonesia Conf. Comput. Inf. Technol. (EIConCIT)*, Apr. 2021, pp. 199-203, doi: 10.1109/EIConCIT50028.2021.9431859.

[24] P. Mishra and A. Yadav, “An explainable and reproducible lightweight machine learning framework for SMS spam detection using TF-IDF and Linear Support Vector Classification,” *International Journal of Advanced Science and Computer Applications*, vol. 5, no. 2, Sep. 2026, doi: 10.47679/ijasca.v5i2.269.

[25] J. Ismail, R. A. Nasution, and M. N. Gea, “Deteksi phishing URL menggunakan XGBoost dengan Explainable AI pada Web Page Phishing Detection dataset,” *IDEALIS: InDonEsiA journaL Information System*, vol. 9, no. 2, pp. 268-277, Jul. 2026, doi: 10.36080/idealis.v9i2.3810.

[26] Suwarno, V. Capricornness, and Y. Christian, “Implementasi machine learning berbasis browser extension untuk deteksi URL phishing menggunakan Logistic Regression classification,” *Komputa: Jurnal Ilmiah Komputer dan Informatika*, vol. 15, no. 1, May 2026, doi: 10.34010/komputa.v15i1.18882.

[33] R.-E. Fan, K.-W. Chang, C.-J. Hsieh, X.-R. Wang, and C.-J. Lin, “LIBLINEAR: A library for large linear classification,” *Journal of Machine Learning Research*, vol. 9, pp. 1871-1874, Aug. 2008. [Online]. Available: https://jmlr.org/papers/v9/fan08a.html

[34] J. C. Platt, “Probabilistic outputs for support vector machines and comparisons to regularized likelihood methods,” in *Advances in Large Margin Classifiers*, A. J. Smola, P. Bartlett, B. Schölkopf, and D. Schuurmans, Eds. Cambridge, MA, USA: MIT Press, 2000, pp. 61-74.

[36] G. Salton and C. Buckley, “Term-weighting approaches in automatic text retrieval,” *Information Processing & Management*, vol. 24, no. 5, pp. 513-523, 1988, doi: 10.1016/0306-4573(88)90021-0.

[37] M. Adriani, J. Asian, B. A. A. Nazief, S. M. M. Tahaghoghi, and H. E. Williams, “Stemming Indonesian: A confix-stripping approach,” *ACM Transactions on Asian Language Information Processing*, vol. 6, no. 4, pp. 1-33, Dec. 2007, doi: 10.1145/1316457.1316459.

[38] R. Kohavi, “A study of cross-validation and bootstrap for accuracy estimation and model selection,” in *Proc. 14th Int. Joint Conf. Artif. Intell. (IJCAI)*, Montreal, QC, Canada, Aug. 1995, vol. 2, pp. 1137-1143. [Online]. Available: https://www.ijcai.org/Proceedings/95-2/Papers/016.pdf

[39] M. Sokolova and G. Lapalme, “A systematic analysis of performance measures for classification tasks,” *Information Processing & Management*, vol. 45, no. 4, pp. 427-437, Jul. 2009, doi: 10.1016/j.ipm.2009.03.002.

[40] F. Pedregosa *et al.*, “Scikit-learn: Machine Learning in Python,” *Journal of Machine Learning Research*, vol. 12, pp. 2825-2830, Oct. 2011. [Online]. Available: https://jmlr.org/papers/v12/pedregosa11a.html

[41] Menteri Riset, Teknologi, dan Pendidikan Tinggi Republik Indonesia, *Peraturan Menteri Riset, Teknologi, dan Pendidikan Tinggi Nomor 42 Tahun 2016 tentang Pengukuran dan Penetapan Tingkat Kesiapterapan Teknologi* (Berita Negara Republik Indonesia Tahun 2016 Nomor 1010). Jakarta: Kementerian Ristekdikti, Jul. 2016.

[42] H.-T. Lin, C.-J. Lin, and R. C. Weng, “A note on Platt's probabilistic outputs for support vector machines,” *Machine Learning*, vol. 68, no. 3, pp. 267-276, Aug. 2007, doi: 10.1007/s10994-007-5018-6.
