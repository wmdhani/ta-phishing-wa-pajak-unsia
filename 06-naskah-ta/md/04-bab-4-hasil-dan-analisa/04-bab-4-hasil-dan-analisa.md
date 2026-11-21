# BAB IV HASIL DAN ANALISA

## 4.1 Hasil Eksperimen Komparasi Klasifikasi dan Penyetelan Hiperparameter

Eksperimen komparatif dieksekusi oleh `src/eksperimen_komparasi.py` memakai pengacak tetap `random_state=42` selama 189,36 detik. Penyaringan duplikat Sastrawi atas 1.164 baris induk menyisakan 1.159 teks unik (`927` latih dan `232` uji) bagi `LinearSVC` serta `RandomForestClassifier` [33], [35]. Pada uji *baseline* (`n = 232`), `LinearSVC` bawaan meraih *Accuracy* 96,12%, *Precision* 97,70%, *Recall* 92,39%, dan *F1-Score* 94,97% (`TN = 138`, `FP = 2`, `FN = 7`, `TP = 85`). *Random Forest* (`n_estimators=200`) juga mencatat akurasi 96,12% dengan *F1-Score* 95,03% (`TN = 137`, `FP = 3`, `FN = 6`, `TP = 86`) [13], [32].

Evaluasi berlanjut melalui *Stratified 10-Fold Cross-Validation* terisolasi TF-IDF pada 927 data latih [38]. Sebelum penalaan, `LinearSVC` mencatat rata-rata *F1-Score* 97,04% (± 2,71%), *Accuracy* 97,63%, dan *ROC-AUC* 0,9956 dalam waktu 0,0026 detik per lipatan. Di sisi lain, *Random Forest* meraih *F1-Score* 93,68% (± 3,20%) dan akurasi 94,93% dalam waktu 0,6010 detik.

Melalui `GridSearchCV` atas 36 kandidat [40], setelan optimal `LinearSVC` pada `C=2.0` (`class_weight=None`) meraih *F1-Score* 97,16% (± 2,41%), akurasi 97,74%, dan *ROC-AUC* 0,9956 dalam 0,0027 detik per lipatan. Sebaliknya, *Random Forest* terbaik (`n_estimators=100`, `max_depth=None`, `min_samples_split=2`) mencatat *F1-Score* 94,07% (± 2,92%) dan akurasi 95,25% dalam waktu 0,2841 detik atau sekitar 106,6 kali lebih lambat [33], [35].

Pada himpunan uji tetap (`n = 232`), kalibrasi `Pipeline` *Platt scaling* menggeser akurasi `LinearSVC` ke 95,69% (`FP = 3`, `FN = 7`), sementara *Random Forest* mencatat 96,55% (`FP = 2`, `FN = 6`) [34], [42]. Selisih satu hingga dua sampel (`0,43%` sampai `0,86%`) tersebut berada di dalam simpangan baku CV (± 2,41%). Tabel 4.1 merangkum seluruh tahap evaluasi utama.

Tabel 4.1 Hasil Komparasi Kinerja Klasifikasi pada Berbagai Tahap Evaluasi

| Tahap Evaluasi dan Himpunan Uji | Model Klasifikasi | *Accuracy* | *Precision* | *Recall* | *F1-Score* | *ROC-AUC* |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| *Baseline Holdout* (`n = 232`) | `LinearSVC` / RF (Default) | 96,12% / 96,12% | 97,70% / 96,63% | 92,39% / 93,48% | 94,97% / 95,03% | 0,9955 / 0,9939 |
| *10-Fold CV* Default (`n = 927`) | `LinearSVC` / RF (Default) | 97,63% / 94,93% | 97,37% / 93,69% | 96,76% / 93,78% | 97,04% / 93,68% | 0,9956 / 0,9905 |
| *10-Fold CV Tuned* (`n = 927`) | `LinearSVC` (`C=2.0`) / RF | 97,74% / 95,25% | 97,61% / 94,46% | 96,76% / 93,78% | 97,16% / 94,07% | 0,9956 / 0,9901 |
| *Holdout* Final (`n = 232`) | `LinearSVC` Platt / RF Tuned | 95,69% / 96,55% | 96,59% / 97,73% | 92,39% / 93,48% | 94,44% / 95,56% | 0,9957 / 0,9936 |
| Kontrol Tanpa Korpus Pajak (`n = 45`) | `LinearSVC` Platt / RF Tuned | 42,22% / 33,33% | 45,00% / 31,25% | 37,50% / 20,83% | 40,91% / 25,00% | 0,3571 / 0,3502 |
| Subset Pajak Seimbang (`n = 45`) | `LinearSVC` Platt / RF Tuned | 95,56% / 95,56% | 95,83% / 95,83% | 95,83% / 95,83% | 95,83% / 95,83% | 0,9960 / 0,9752 |
| *10-Fold CV* Korpus Pajak (`n = 260`) | `LinearSVC` (`C=2.0`) / RF | 98,08% / 93,46% | 96,52% / 92,99% | 100,00% / 94,62% | 98,17% / 93,57% | 0,9947 / 0,9905 |
| *Zero-Shot* Eksternal (`n = 1.360`) | `LinearSVC` Platt / RF Tuned | 64,19% / 62,35% | 40,99% / 36,99% | 80,28% / 60,00% | 54,27% / 45,76% | 0,7875 / 0,6978 |
| *Holdout* Korpus Diperluas (`n = 504`) | `LinearSVC` Platt / RF Tuned | 96,03% / 92,46% | 96,75% / 92,00% | 90,85% / 84,15% | 93,71% / 87,90% | 0,9883 / 0,9771 |

Sumber: Pengolahan Hasil Eksperimen `05 Hasil Evaluasi/tabel_komparasi_utama.csv` (2026).

Sebaran empat kuadran *Confusion Matrix* pada himpunan uji `n = 232` tampak pada Gambar 4.1. Grafik kurva ROC dan *Precision-Recall* terlampir pada `Gambar L.2` dengan *ROC-AUC* 0,9957 vs 0,9936 serta *PR-AUC* 0,9943 vs 0,9909 [39]. Pergeseran satu sampel pada `LinearSVC` Platt muncul di `idx=1082` (`p = 0,5506`) akibat perataan lima submodel `CalibratedClassifierCV`. Selisih satu sampel tersebut setara 0,43%.

![Gambar 4.1 Perbandingan Confusion Matrix Uji Holdout.](Aset Gambar/Gambar 4.1 Perbandingan Confusion Matrix Uji Holdout.png)

Gambar 4.1 Perbandingan *Confusion Matrix* Uji *Holdout*.

## 4.2 Analisis Kalibrasi Probabilitas dan Studi Ablatif Fitur

Penyajian skor risiko membutuhkan probabilitas yang selaras dengan frekuensi kejadian nyata [34], [42]. Pada `n = 232`, *Platt scaling* berbasis `Pipeline` pada `LinearSVC` mencatat *Brier Score* 0,02542 dan *Log Loss* 0,09186. Angka galat tersebut jauh di bawah *Random Forest* yang mencatat *Brier Score* 0,04214 serta *Log Loss* 0,15870. Kalibrasi `LinearSVC` menekan *Brier Score* sebesar 39,68% dan memangkas *Log Loss* sebesar 42,12%. Seperti terlihat pada Gambar 4.2, sebaran skor `LinearSVC` memisah tegas mendekati nol dan satu, berlawanan dengan *Random Forest* yang menyebar di wilayah keraguan 0,2 sampai 0,8 [35].

![Gambar 4.2 Evaluasi Kalibrasi Probabilitas Model.](Aset Gambar/Gambar 4.2 Evaluasi Kalibrasi Probabilitas Model.png)

Gambar 4.2 Evaluasi Kalibrasi Probabilitas Model.

Enam skenario ablatif dijalankan pada `05 Hasil Evaluasi/studi_ablatif_fitur.csv` (rincian penuh pada Lampiran `Tabel L.8`) [36], [37]. Konfigurasi utama (`teks_sastrawi`, bigram `(1, 2)`, 3.000 fitur) meraih *F1-Score* 10-Fold CV `LinearSVC` tertinggi (`97,16%`). Peniadaan token entitas menurunkan skor CV tersebut sebesar 1,35 poin ke 95,81% dan menjatuhkan *Random Forest* ke 92,42% [16]. Pembatasan unigram saja turut memangkas skor `LinearSVC` sebesar 1,22 poin ke 95,94%.

Dua temuan tambahan muncul dari uji ablatif. Selisih CV antara memakai dan meniadakan Sastrawi hanya 0,0007%, menandakan Sastrawi terutama berfungsi menyeragamkan variasi imbuhan kata [9], [37]. Di samping itu, lonjakan akurasi *holdout* `1_Tanpa_Token_Entitas` (97,84%) dipicu penyatuan tautan resmi dan palsu ke token `token_url` sebelum daftar putih domain bekerja. Oleh sebab itu, daftar putih domain perlu terpisah.

## 4.3 Analisis Ketahanan Bias Kata Kunci Pajak dan Generalisasi Lintas Korpus

Pengujian `Tahap 4A` menjawab langsung Rumusan Masalah (b) lewat perbandingan model kontrol tanpa korpus pajak terhadap model berimbang pada 45 pesan pajak (`21` resmi DJP dan `24` *phishing*). Ketika `LinearSVC` Platt hanya dilatih memakai 712 SMS umum, akurasinya jatuh ke 42,22% (*F1-Score* 40,91%; *ROC-AUC* 0,3571). Sebanyak 11 pengumuman resmi DJP ikut terblokir (`FP = 11`) dan 15 pesan penipuan lolos (`FN = 15`). *Random Forest* pada kondisi kontrol serupa mencatat akurasi 33,33% dan *F1-Score* 25,00% (`FP = 11`, `FN = 19`).

Begitu korpus pajak berimbang masuk ke data latih utama (`1.159` baris), kedua model melonjak ke *Accuracy* 95,56% dan *F1-Score* 95,83% (`FP = 1`, `FN = 1`). Dua puluh dari 21 siaran resmi DJP lolos aman [2], [5]. Di atas subset tersebut, `LinearSVC` Platt meraih *ROC-AUC* 0,9960 (*Brier Score* 0,03289) mengungguli *Random Forest* (`0,9752`; `0,10914`). Pada 10-Fold CV 260 baris pajak, `LinearSVC` unggul jauh dengan *F1-Score* 98,17% (*Recall* 100,00%) dibanding *Random Forest* sebesar 93,57%.

Pada uji *zero-shot* lintas korpus `Tahap 4B` terhadap 1.360 pesan unik Theodorus dkk. [7] dan Saragih, `LinearSVC` mempertahankan *Recall* 80,28% (*F1-Score* 54,27%) melampaui *Random Forest* (`60,00%`; `45,76%`). Presisi turun ke 40,99% (`FP = 416`) akibat *domain shift* kosakata SMS normal lintas periode dan ketimpangan 94 baris sisa Saragih (`90:4`). Saat korpus diperluas ke 2.519 baris unik pada `Tahap 4C`, akurasi *holdout* (`n = 504`) `LinearSVC` pulih ke 96,03% berbanding 92,46% pada *Random Forest*. Tren lintas domain tervisualisasi pada Gambar 4.3, yang menegaskan pentingnya pembaruan kosakata berkala.

![Gambar 4.3 Komparasi Generalisasi Lintas Korpus dan Subset Pajak.](Aset Gambar/Gambar 4.3 Komparasi Generalisasi Lintas Korpus dan Subset Pajak.png)

Gambar 4.3 Komparasi Generalisasi Lintas Korpus dan Subset Pajak.

## 4.4 Analisis Interpretabilitas Fitur dan Kesalahan Prediksi

Transparansi model dikaji lewat vektor koefisien `LinearSVC` (Lampiran `Gambar L.3` dan `Tabel L.9`) serta nilai SHAP terkondisi fitur aktif pada `n = 232` menggunakan `LinearExplainer` dan `TreeExplainer` [24], [25] di Gambar 4.4. Token pemicu *phishing* terkuat `LinearSVC` meliputi `no` (+2,241), `sms` (+1,694), `rekening` (+1,508), `info` (+1,405), `segera` (+1,378), `pin` (+1,373), `token_apk` (+1,358), serta `token_url` (+1,355). Posisi `token_apk` dan `token_url` membuktikan fitur teknis ini menangkap sinyal penipuan secara kuat.

![Gambar 4.4 Analisis Interpretabilitas Model Berbasis SHAP.](Aset Gambar/Gambar 4.4 Analisis Interpretabilitas Model Berbasis SHAP.png)

Gambar 4.4 Analisis Interpretabilitas Model Berbasis SHAP.

Di sisi penahan kelas aman pada `LinearSVC`, dorongan terkuat berasal dari `resmi` (-1,071; SHAP 0,0341), `laman`, `kp2kp`, serta `pratama`, selain token percakapan `nama1` (-1,272; SHAP 0,0395), `yg` (-0,894), dan pronomina orang pertama informal (SHAP 0,0575; `Tabel L.9`). Token `nama1` dan `2016` (-0,666) berasal dari anonimisasi korpus Rahmi [6] sehingga disaring dari antarmuka pengguna. Pada *Random Forest*, sepuluh fitur SHAP teratas didominasi kata pemicu *phishing* seperti `info` (0,0323) dan `no` (0,0323).

Penelusuran galat pada 232 data uji menemukan 13 sampel salah prediksi gabungan (`10` pada `LinearSVC` Platt dan `8` pada *Random Forest*, rinci di Lampiran `Tabel L.10`). Kasus `idx=960` (*phishing* `MPajak_Aktivasi_KSWP.apk` bergaya dinas) lolos dari model linear (`p = 0,424`) namun tertangkap oleh aturan `has_apk`. Sebaliknya, `idx=1082` (imbauan sah bermuatan `www.pajak.go.id`) sempat terkena positif palsu (`p = 0,551`) akibat `token_url`, lalu terselamatkan daftar putih `is_official_djp_domain`. Dua kesalahan pesan transfer tanpa tautan (`idx=314` dan `idx=102`) menunjukkan batas fitur leksikal murni.

## 4.5 Hasil Pengujian Purwarupa Sistem Terpadu dan Evaluasi Kesiapterapan Teknologi

Pengujian otomatis melalui Pytest 9.2.0 dan `src/benchmark_purwarupa.py` meluluskan seluruh 23 kasus uji dalam 21,51 detik (rincian `UJI-01` s.d. `UJI-10` dan `LAT-01` s.d. `LAT-05` di Lampiran `Tabel L.11`). Setelah `.joblib` dimuat ke `lru_cache` dalam 122,655 ms, `inference.py::predict_message` pada `n = 232` berjalan rata-rata 20,746 ms (*P95* 27,447 ms), sedangkan REST API `POST /predict` mencatat rata-rata 34,991 ms (*median* 31,812 ms; *P95* 48,082 ms) dan batch 50 pesan tuntas dalam 1.315,652 ms (26,313 ms/pesan). Pada `UJI-07`, `POST /predict/batch` mengembalikan `total=3` atas tiga masukan campuran serta menolak teks >5.000 karakter berstatus 422.

Demonstrasi web *Cek Pesan Pajak* dan respons JSON API tampak pada Gambar 4.5. Prasetel `Pembaruan_Coretax_DJP.apk` memunculkan lencana `BAHAYA / SCAM` (`Scam 92%`; `svm_probability = 0,9249`), menyorot `.apk` di pratinjau chat, serta menampilkan empat chip awal (*segera*, *unduh*, *instal*, *verifikasi*) dari lima kata pemicu JSON. Simulasi ekstensi *Manifest V3* pada Gambar 4.6 mendeteksi `djp-coretax-verifikasi.xyz` sebagai bahaya (`Scam 84%`), meloloskan `djponline.pajak.go.id` (`Aman 90%`), serta menjaga jam `17.00`. Atas integrasi penuh dan latensi *P95* di bawah 50 ms tersebut, sistem memenuhi **TKT Level 6** sesuai Permenristekdikti Nomor 42 Tahun 2016 [41].

![Gambar 4.5 Tangkapan Layar Antarmuka Web Cek Pesan Pajak dan Respons API.](Aset Gambar/Gambar 4.5 Tangkapan Layar Antarmuka Web Cek Pesan Pajak dan Respons API.png)

Gambar 4.5 Tangkapan Layar Antarmuka Web *Cek Pesan Pajak* dan Respons API.

![Gambar 4.6 Tangkapan Layar Ekstensi Chrome pada Simulasi WhatsApp Web.](Aset Gambar/Gambar 4.6 Tangkapan Layar Ekstensi Chrome pada Simulasi WhatsApp Web.png)

Gambar 4.6 Tangkapan Layar Ekstensi Chrome pada Simulasi *WhatsApp Web*.

Perbandingan akhir terhadap studi terdahulu [6], [7], [9], [10], [11], [13], [15], [16], [24], [26] terangkum pada Tabel 4.2. Pembandingan ini merangkum kebaruan penelitian dalam memadukan korpus pajak berimbang, uji kontrol *keyword bias*, kalibrasi probabilitas *Platt scaling*, interpretabilitas SHAP, serta ekstensi *WhatsApp Web* berlatensi rendah pada TKT Level 6.

Tabel 4.2 Komparasi Hasil Penelitian terhadap Studi Terdahulu

| Peneliti (Tahun) | Korpus & Fitur | Model Terbaik & Kinerja | Kebaruan pada Penelitian Ini |
| :--- | :--- | :--- | :--- |
| Rahmi & Wibisono (2016) [6]; Theodorus dkk. (2021) [7] | 1.140 SMS (TF) & 4.125 SMS Indo (BoW) | MNB (*Acc* 94,56%); RF (*Acc* 94,62% vs SVM 94,38%) | Menambahkan korpus pajak seimbang, pelestarian `.apk`/URL, & uji bias |
| Al Ghofany dkk. (2022) [9]; Astuti dkk. (2024) [10] | 500 SMS Indo & 5.574 SMS Inggris (TF-IDF) | SVM Sigmoid (99,60%); SVC (97,93%) > RF | Menguji Sastrawi pada korpus pajak publik + kalibrasi Platt + SHAP |
| Tampinongkol dkk. (2024) [11]; Ningtias dkk. (2026) [13] | 59.899 URL & 5.572 SMS Inggris (TF-IDF) | RF (84,95%); Linear SVM (98,39%) > RF (95,96%) | Memproses teks rekayasa sosial WA pajak + menyimpan sinyal `.apk`/URL |
| Saputra dkk. (2026) [15]; Sembiring dkk. (2026) [16] | 1.320 pesan WA & 2.320 pesan Indo | SVM (*Acc* 95,45%); XGBoost (96,34%), SVM (*Rec* 98,59%) | Menghindari *hashing* agar XAI tetap terbaca + menyandikan `.apk` + ekstensi |
| Mishra & Yadav (2026) [24]; Suwarno dkk. (2026) [26] | SMS TF-IDF [24]; Ekstensi URL *LogReg* [26] | `LinearSVC` XAI [24]; Ekstensi peramban [26] | Memadukan XAI, penjaga `pajak.go.id`, web, & ekstensi WA pajak TKT 6 |
| **Penelitian Ini (2026)** | **1.159 unik (induk) & 2.519 diperluas, TF-IDF `(1, 2)` + Sastrawi** | **`LinearSVC` Platt (*CV* 97,74%, *F1* pajak 98,17%, *Brier* 0,02542)** | **Kontrol bias 42,22%->95,56%, SHAP, *guard* `.apk`/domain sah, TKT 6 (34,99 ms)** |

Sumber: Sintesis Perbandingan Eksperimen dan Literatur (2026).
