# Laporan Hasil Eksperimen Komparasi SVM Linear dan Random Forest

Seluruh rangkaian eksperimen dijalankan secara otomatis oleh `src/eksperimen_komparasi.py` dengan total waktu komputasi **193.47 detik**.

## 1. Reproduksi Baseline (Holdout 80:20 Korpus Utama 1159 Baris Unik dari 1164 Mentah)

- **SVM Linear (Default):** Akurasi **96.12%**, Precision 97.70%, Recall 92.39%, F1-Score 94.97% (TN=138, FP=2, FN=7, TP=85).
- **Random Forest (Default `n_estimators=200`):** Akurasi **96.12%**, Precision 96.63%, Recall 93.48%, F1-Score 95.03% (TN=137, FP=3, FN=6, TP=86).

## 2. Hyperparameter Tuning & Stratified 10-Fold Cross-Validation (927 Data Latih)

- **Parameter Optimal SVM Linear:** `{"C": 2.0, "class_weight": null}` -> 10-Fold CV F1-Score **97.16% ± 2.41%**, Akurasi **97.74%**, ROC-AUC **0.9956**.
- **Parameter Optimal Random Forest:** `{"n_estimators": 100, "max_depth": null, "min_samples_split": 2, "class_weight": null}` -> 10-Fold CV F1-Score **94.07% ± 2.92%**, Akurasi **95.25%**, ROC-AUC **0.9901**.

## 3. Kalibrasi Probabilitas Platt Scaling & Evaluasi Holdout Final (n = 232)

| Model | Akurasi | Precision | Recall | F1-Score | ROC-AUC | PR-AUC | Brier Score | Log Loss |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| SVM Linear (Platt Sigmoid) | 95.69% | 96.59% | 92.39% | 94.44% | 0.9957 | 0.9943 | 0.02542 | 0.09186 |
| Random Forest (Tuned) | 96.55% | 97.73% | 93.48% | 95.56% | 0.9936 | 0.9909 | 0.04214 | 0.15870 |

## 4. Studi Ablatif Praproses dan Representasi Fitur TF-IDF

| Konfigurasi | Model | CV10 F1 Mean | CV10 Acc Mean | Holdout Acc | Holdout F1 |
| :--- | :--- | ---: | ---: | ---: | ---: |
| 1_Tanpa_Token_Entitas | SVM_Linear | 95.81% | 96.66% | 97.84% | 97.27% |
| 1_Tanpa_Token_Entitas | Random_Forest | 92.42% | 93.96% | 95.26% | 93.99% |
| 2_Tanpa_Sastrawi | SVM_Linear | 97.16% | 97.74% | 96.12% | 95.08% |
| 2_Tanpa_Sastrawi | Random_Forest | 94.55% | 95.69% | 96.55% | 95.60% |
| 3_Unigram_Saja | SVM_Linear | 95.94% | 96.77% | 96.12% | 95.08% |
| 3_Unigram_Saja | Random_Forest | 94.59% | 95.68% | 96.12% | 95.03% |
| 4_Utama_MaxFeatures_1500 | SVM_Linear | 96.61% | 97.30% | 96.12% | 95.03% |
| 4_Utama_MaxFeatures_1500 | Random_Forest | 94.52% | 95.58% | 96.55% | 95.56% |
| 5_Konfigurasi_Utama_3000 | SVM_Linear | 97.16% | 97.74% | 96.12% | 94.97% |
| 5_Konfigurasi_Utama_3000 | Random_Forest | 94.07% | 95.25% | 96.55% | 95.56% |
| 6_Utama_MaxFeatures_5000 | SVM_Linear | 96.79% | 97.41% | 96.98% | 96.13% |
| 6_Utama_MaxFeatures_5000 | Random_Forest | 93.34% | 94.72% | 96.55% | 95.60% |

## 5. Ketahanan Bias Kata Kunci Pajak & Uji Generalisasi Lintas-Korpus

- **Subset Khusus Pajak pada Holdout (n = 45):** SVM Platt mencapai Akurasi **95.56%** (F1 95.83%, FP=1, FN=1), sedangkan Random Forest mencapai Akurasi **95.56%** (F1 95.83%, FP=1, FN=1).
- **10-Fold Stratified CV Khusus Korpus Pajak (260 baris):** SVM mencapai F1 **98.17%** (Akurasi **98.08%**); Random Forest mencapai F1 **93.57%** (Akurasi **93.46%**).
- **Uji Zero-Shot Lintas-Korpus Eksternal (n = 1360 unik, dari 3091 mentah setelah menghapus 1483 duplikat internal dan 248 tumpang tindih dengan korpus utama):** SVM Platt mencapai Akurasi **64.19%** (F1 54.27%), sedangkan Random Forest mencapai Akurasi **62.35%** (F1 45.76%).
- **Evaluasi Korpus Diperluas 2519 Baris Unik (Holdout n = 504):** SVM Platt mencapai Akurasi **96.03%** (F1 93.71%) dengan 10-Fold CV F1 **91.81%**; Random Forest mencapai Akurasi **92.46%** (F1 87.90%) dengan 10-Fold CV F1 **91.11%**.

## 6. Interpretabilitas Fitur Teratas & Analisis Kesalahan (n = 232)

- **Indikator Phishing Terkuat SVM Linear (+):** `no` (2.241), `sms` (1.694), `rekening` (1.508), `info` (1.405), `segera` (1.378), `pin` (1.373), `token_apk` (1.358), `token_url` (1.355)
- **Indikator Resmi/Normal Terkuat SVM Linear (-):** `nama1` (-1.272), `aku` (-1.221), `resmi` (-1.071), `maupun` (-0.963), `terimakasih` (-0.913), `yg` (-0.894), `nya` (-0.874), `pernah` (-0.842)
- **Fitur Terpenting Random Forest (Gini):** `no` (0.0424), `hub` (0.0349), `info` (0.0319), `sms` (0.0227), `token_url` (0.0226), `hadiah` (0.0200), `pin` (0.0175), `rekening` (0.0174)
- **Top-8 Fitur SHAP SVM Linear (Holdout):** `no` (0.0677, Phishing), `aku` (0.0575, Resmi/Normal), `token_url` (0.0461, Phishing), `info` (0.0440, Phishing), `pin` (0.0395, Phishing), `nama1` (0.0395, Resmi/Normal), `yg` (0.0388, Resmi/Normal), `resmi` (0.0341, Resmi/Normal)
- **Top-8 Fitur SHAP Random Forest (Holdout):** `info` (0.0323, Phishing), `no` (0.0323, Phishing), `hub` (0.0260, Phishing), `token_url` (0.0242, Phishing), `sms` (0.0212, Phishing), `segera` (0.0155, Phishing), `pin` (0.0147, Phishing), `klik` (0.0142, Phishing)
- **Jumlah Sampel Salah Prediksi (gabungan SVM/RF pada holdout):** 13 baris (rincian lengkap tersedia di `analisis_kesalahan_prediksi.csv`).

- `idx=118` | `Korpus_Umum_Rahmi2016` | `SMS_Penipuan_Umum` | Aktual=1, SVM=1 (p=0.566), RF=0 (p=0.420) | `Maaf…! saya bu RATNA meganai RUMAH saya Sudah liat, soalnya saya lagi di bandara silahkan hubungi suami saya H`
- `idx=50` | `Korpus_Umum_Rahmi2016` | `SMS_Penipuan_Umum` | Aktual=1, SVM=0 (p=0.218), RF=1 (p=0.750) | `Gratis 120 menit Nelpon ke Sesama Indosat, 120 SMS ke Sesama Indosat&12 MB Internet slma 12 JAM tiap Isi Ulang`
- `idx=491` | `Korpus_Umum_Rahmi2016` | `SMS_Normal_Umum` | Aktual=0, SVM=1 (p=0.543), RF=0 (p=0.170) | `Dimulai dari angka 0`
- `idx=898` | `Korpus_Umum_Rahmi2016` | `SMS_Normal_Umum` | Aktual=0, SVM=1 (p=0.608), RF=1 (p=0.640) | `No bri atas nama kamu mana`
- `idx=960` | `Korpus_Pajak_Terverifikasi` | `Phishing_APK_MPajak` | Aktual=1, SVM=0 (p=0.424), RF=1 (p=0.730) | `Pemberitahuan Direktorat Jenderal Pajak: Untuk mengaktifkan fitur pembuatan kode billing dan pengecekan KSWP t`
- `idx=293` | `Korpus_Umum_Rahmi2016` | `SMS_Penipuan_Umum` | Aktual=1, SVM=0 (p=0.347), RF=0 (p=0.250) | `Terima kasih telah melakukan isi ulang di sunny15.Trx Sukses sbsar 10.000 SN:1790103904.BYR PLNTELKOM BISA.Kam`
- `idx=1003` | `Korpus_Pajak_Terverifikasi` | `Phishing_Link_NIK_NPWP_Pemutakhiran` | Aktual=1, SVM=1 (p=0.787), RF=0 (p=0.340) | `PERINGATAN PEMUTAKHIRAN DATA: Sesuai instruksi Direktorat Jenderal Pajak, wajib pajak yang menerima pesan What`
- `idx=52` | `Korpus_Umum_Rahmi2016` | `SMS_Penipuan_Umum` | Aktual=1, SVM=1 (p=0.819), RF=0 (p=0.350) | `GRATIS internetan 5MB berlaku utk 7 hari hanya dg isi ulang AXISmu hari ini Rp5.000. Ayo isi ulang sekarang ju`
- `idx=228` | `Korpus_Umum_Rahmi2016` | `SMS_Penipuan_Umum` | Aktual=1, SVM=0 (p=0.494), RF=1 (p=0.610) | `Sayang sekali kamu kalah cepat. Tapi jangan khawatir! Ayo coba lagi di sesi berikutnya! * Pastikan kamu membac`
- `idx=314` | `Korpus_Umum_Rahmi2016` | `SMS_Penipuan_Umum` | Aktual=1, SVM=0 (p=0.033), RF=0 (p=0.230) | `Transfer ke Mandiri aja, a/n Resti Amanda norek 9000007701999`
- `idx=102` | `Korpus_Umum_Rahmi2016` | `SMS_Penipuan_Umum` | Aktual=1, SVM=0 (p=0.392), RF=0 (p=0.470) | `Kirim ke MANDIRI aja, a/n ARYA. rek: 131-000-7252-937. klo sudah kabarin ya!`
- `idx=1082` | `Korpus_Pajak_Terverifikasi` | `Resmi_WA_Blast_Pemadanan_NIK_NPWP` | Aktual=0, SVM=1 (p=0.551), RF=1 (p=0.600) | `Selamat siang Wajib Pajak, untuk mengecek apakah NIK Anda sudah berstatus Valid sebagai NPWP 16 digit, silakan`
- `idx=165` | `Korpus_Umum_Rahmi2016` | `SMS_Penipuan_Umum` | Aktual=1, SVM=0 (p=0.493), RF=1 (p=0.550) | `pembayaran anda sudah jatuh tempo silahkan melapor/M-HUB ke Kantor 082327327705 terima kasih`

## 7. Catatan Metodologis dan Batas Interpretasi

- **Stabilitas Lintas-Lipatan vs Varians Holdout Tunggal:** SVM Linear unggul konsisten pada seluruh skenario 10-Fold CV (korpus utama `97.16%` vs `94.07%`, korpus pajak `98.17%` vs `93.57%`, korpus diperluas `91.81%` vs `91.11%`), holdout korpus diperluas (`96.03%` vs `92.46%`), zero-shot eksternal (F1 `54.27%` vs `45.76%`), ROC-AUC/PR-AUC (`0.9957`/`0.9943` vs `0.9936`/`0.9909`), serta Brier Score (`0.02542` vs `0.04214`). Selisih 1–2 sampel pada ambang diskrit `0.5` di holdout utama (`n = 232`) berada dalam rentang simpangan baku CV (`±2.41%`).
- **Interpretasi Studi Ablatif & Token Generik `token_url`:** Konfigurasi utama (`teks_sastrawi`, bigram `(1, 2)`, `3.000` fitur) dipilih karena meraih rata-rata F1 10-Fold CV tertinggi pada SVM (`97.16%`), mengungguli skenario tanpa token entitas (`95.81%`) dan unigram saja (`95.94%`). Variasi pada holdout tunggal (`1_Tanpa_Token_Entitas` `97.84%`) dipengaruhi ukuran uji (`1` sampel = `0.43%`) serta penyamaran domain resmi `pajak.go.id` dan tautan penipu ke satu token generik `token_url`.
- **Justifikasi Empiris Lapisan Heuristik Purwarupa (`idx=960` & `idx=1082`):** Kasus `idx=960` (pesan `.apk` bergaya birokratis formal dengan `p_svm = 0.424`) dan `idx=1082` (siaran resmi pemadanan NIK bermuatan `www.pajak.go.id` dengan `p_svm = 0.551`) membuktikan keterbatasan TF-IDF murni dan menjustifikasi aturan hibrida `has_apk` serta `is_official_djp_domain` pada `06 Prototipe Aplikasi/inference.py`.
- **Rincian Zero-Shot Lintas-Korpus & Ketimpangan Subset Saragih:** Pada `1360` pesan eksternal unik, SVM mempertahankan Recall `80.28%` namun mengalami penurunan spesifisitas (`58.40%`, `FP = 416`) akibat *domain shift* kosakata SMS normal lintas-periode (2016 vs 2021–2024). Khusus subset `Korpus_Umum_Saragih2024` (`n = 94` pascadeduplikasi 248 baris Rahmi), komposisi kelas sangat timpang (`90` penipuan : `4` normal), sehingga `f1_macro` dan `roc_auc` subset tersebut tidak diinterpretasikan secara terpisah.
- **Skala SHAP & Artefak Anonimisasi Korpus Dasar:** Nilai `LinearExplainer` bekerja pada satuan margin hyperplane sedangkan `TreeExplainer` bekerja pada satuan probabilitas, sehingga perbandingan lintas model mengacu pada peringkat fitur dan `arah_dominan` saat fitur aktif (`x_test > 0`). Munculnya `nama1` (`-1.272`) dan `2016` (`-0.666`) merupakan artefak anonimisasi korpus SMS Rahmi 2016, sedangkan ketahanan terhadap kosakata pajak dibuktikan melalui evaluasi terpisah pada 260 baris korpus pajak seimbang.

