# Laporan Hasil Eksperimen Komparasi SVM Linear dan Random Forest

Seluruh rangkaian eksperimen dijalankan secara otomatis oleh `src/eksperimen_komparasi.py` dengan total waktu komputasi **228.37 detik**.

## 1. Reproduksi Baseline (Holdout 80:20 Korpus Utama 1.164 Baris)

- **SVM Linear (Default):** Akurasi **98.28%**, Precision 97.85%, Recall 97.85%, F1-Score 97.85% (TN=138, FP=2, FN=2, TP=91).
- **Random Forest (Default `n_estimators=200`):** Akurasi **95.28%**, Precision 93.62%, Recall 94.62%, F1-Score 94.12% (TN=134, FP=6, FN=5, TP=88).

## 2. Hyperparameter Tuning & Stratified 10-Fold Cross-Validation (931 Data Latih)

- **Parameter Optimal SVM Linear:** `{"C": 5.0, "class_weight": null}` -> 10-Fold CV F1-Score **97.18% ± 2.56%**, Akurasi **97.74%**, ROC-AUC **0.9951**.
- **Parameter Optimal Random Forest:** `{"n_estimators": 200, "max_depth": null, "min_samples_split": 5, "class_weight": null}` -> 10-Fold CV F1-Score **94.19% ± 2.13%**, Akurasi **95.27%**, ROC-AUC **0.9914**.

## 3. Kalibrasi Probabilitas Platt Scaling & Evaluasi Holdout Final (n = 233)

| Model | Akurasi | Precision | Recall | F1-Score | ROC-AUC | PR-AUC | Brier Score | Log Loss |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| SVM Linear (Platt Sigmoid) | 97.42% | 95.79% | 97.85% | 96.81% | 0.9982 | 0.9975 | 0.01900 | 0.06883 |
| Random Forest (Tuned) | 96.57% | 93.81% | 97.85% | 95.79% | 0.9973 | 0.9961 | 0.03555 | 0.14426 |

## 4. Studi Ablatif Praproses dan Representasi Fitur TF-IDF

| Konfigurasi | Model | CV10 F1 Mean | CV10 Acc Mean | Holdout Acc | Holdout F1 |
| :--- | :--- | ---: | ---: | ---: | ---: |
| 1_Tanpa_Token_Entitas | SVM_Linear | 96.36% | 97.10% | 96.57% | 95.79% |
| 1_Tanpa_Token_Entitas | Random_Forest | 92.20% | 93.77% | 95.28% | 94.18% |
| 2_Tanpa_Sastrawi | SVM_Linear | 97.06% | 97.64% | 98.28% | 97.89% |
| 2_Tanpa_Sastrawi | Random_Forest | 95.28% | 96.24% | 97.42% | 96.74% |
| 3_Unigram_Saja | SVM_Linear | 95.43% | 96.35% | 97.00% | 96.30% |
| 3_Unigram_Saja | Random_Forest | 94.35% | 95.49% | 96.14% | 95.24% |
| 4_Utama_MaxFeatures_1500 | SVM_Linear | 96.24% | 96.99% | 96.57% | 95.79% |
| 4_Utama_MaxFeatures_1500 | Random_Forest | 93.71% | 94.85% | 96.14% | 95.24% |
| 5_Konfigurasi_Utama_3000 | SVM_Linear | 97.18% | 97.74% | 97.85% | 97.33% |
| 5_Konfigurasi_Utama_3000 | Random_Forest | 94.19% | 95.27% | 96.57% | 95.79% |
| 6_Utama_MaxFeatures_5000 | SVM_Linear | 95.88% | 96.67% | 97.00% | 96.30% |
| 6_Utama_MaxFeatures_5000 | Random_Forest | 93.72% | 94.95% | 95.71% | 94.74% |

## 5. Ketahanan Bias Kata Kunci Pajak & Uji Generalisasi Lintas-Korpus

- **Subset Khusus Pajak pada Holdout (n = 44):** SVM Platt mencapai Akurasi **97.73%** (F1 97.87%, FP=1, FN=0), sedangkan Random Forest mencapai Akurasi **88.64%** (F1 90.20%, FP=5, FN=0).
- **10-Fold Stratified CV Khusus Korpus Pajak (260 baris):** SVM mencapai F1 **98.17%** (Akurasi **98.08%**); Random Forest mencapai F1 **92.92%** (Akurasi **92.69%**).
- **Uji Zero-Shot Lintas-Korpus Eksternal (n = 1362 unik, dari 1362 mentah setelah menghapus 0 duplikat terhadap korpus utama):** SVM Platt mencapai Akurasi **64.17%** (F1 54.90%), sedangkan Random Forest mencapai Akurasi **60.87%** (F1 46.11%).
- **Evaluasi Korpus Diperluas 2.521 Baris (Holdout n = 505):** SVM Platt mencapai Akurasi **94.65%** (F1 91.79%) dengan 10-Fold CV F1 **91.81%**; Random Forest mencapai Akurasi **92.87%** (F1 88.82%) dengan 10-Fold CV F1 **91.53%**.

## 6. Interpretabilitas Fitur Teratas & Analisis Kesalahan (n = 233)

- **Indikator Phishing Terkuat SVM Linear (+):** `no` (2.338), `sms` (1.876), `hub` (1.774), `token_apk` (1.764), `info` (1.604), `rekening` (1.575), `klik` (1.562), `hp` (1.507)
- **Indikator Resmi/Normal Terkuat SVM Linear (-):** `nama1` (-1.431), `aku` (-1.167), `terimakasih` (-1.093), `maupun` (-1.085), `resmi` (-1.067), `guna` (-0.999), `kalau` (-0.971), `lanjut` (-0.962)
- **Fitur Terpenting Random Forest (Gini):** `info` (0.0362), `no` (0.0350), `token_url` (0.0318), `hadiah` (0.0248), `sms` (0.0241), `pin` (0.0232), `hub` (0.0228), `klik` (0.0193)
- **Jumlah Sampel Salah Prediksi (gabungan SVM/RF pada holdout):** 13 baris (rincian lengkap tersedia di `analisis_kesalahan_prediksi.csv`).

- `idx=334` | `Korpus_Umum_Rahmi2016` | `SMS_Penipuan_Umum` | Aktual=1, SVM=1 (p=0.718), RF=0 (p=0.425) | `Yuk Ikuti akun dakwah, caranya: ketik IKUT [spasi] AkuCintaIslam kirim ke 082110001021.`
- `idx=839` | `Korpus_Umum_Rahmi2016` | `SMS_Normal_Umum` | Aktual=0, SVM=1 (p=0.523), RF=0 (p=0.249) | `Terima kasih atas konfirmasinya. Orderan sedang kami proses.`
- `idx=495` | `Korpus_Umum_Rahmi2016` | `SMS_Normal_Umum` | Aktual=0, SVM=1 (p=0.743), RF=0 (p=0.136) | `Dimulai dari angka 0`
- `idx=50` | `Korpus_Umum_Rahmi2016` | `SMS_Penipuan_Umum` | Aktual=1, SVM=0 (p=0.208), RF=1 (p=0.772) | `Gratis 120 menit Nelpon ke Sesama Indosat, 120 SMS ke Sesama Indosat&12 MB Internet slma 12 JAM tiap Isi Ulang`
- `idx=97` | `Korpus_Umum_Rahmi2016` | `SMS_Penipuan_Umum` | Aktual=1, SVM=0 (p=0.394), RF=1 (p=0.522) | `Kemudahan dan Keamanan bisnis TOGEL kini Berbentuk online, Bergabung dan raih keberuntungan anda di www.brotog`
- `idx=753` | `Korpus_Umum_Rahmi2016` | `SMS_Normal_Umum` | Aktual=0, SVM=0 (p=0.370), RF=1 (p=0.502) | `Pemakaian internet kamu sdh mencapai batasFUP,kecepatan akan disesuaikan.Lebih EKSIS dgnINTERNETGaul Bulanan C`
- `idx=1126` | `Korpus_Pajak_Terverifikasi` | `Resmi_Layanan_WA_KPP_KP2KP_Terverifikasi` | Aktual=0, SVM=0 (p=0.408), RF=1 (p=0.590) | `Apresiasi KP2KP Bandarjaya: Terima kasih kepada Wajib Pajak yang telah proaktif melaporkan pesan PDF mencuriga`
- `idx=1122` | `Korpus_Pajak_Terverifikasi` | `Resmi_Layanan_WA_KPP_KP2KP_Terverifikasi` | Aktual=0, SVM=0 (p=0.065), RF=1 (p=0.529) | `Apabila mendapat informasi mencurigakan yang mengatasnamakan DJP atau KP2KP Sinjai, Wajib Pajak dapat melakuka`
- `idx=1087` | `Korpus_Pajak_Terverifikasi` | `Resmi_WA_Blast_Pemadanan_NIK_NPWP` | Aktual=0, SVM=1 (p=0.712), RF=1 (p=0.637) | `Selamat siang Wajib Pajak, untuk mengecek apakah NIK Anda sudah berstatus Valid sebagai NPWP 16 digit, silakan`
- `idx=943` | `Korpus_Pajak_Terverifikasi` | `Resmi_Layanan_KringPajak_EFIN_MPajak` | Aktual=0, SVM=0 (p=0.103), RF=1 (p=0.515) | `Terima kasih telah memanfaatkan layanan konsultasi resmi KPP. Apabila terdapat kendala lebih lanjut silakan hu`
- `idx=463` | `Korpus_Umum_Rahmi2016` | `SMS_Normal_Umum` | Aktual=0, SVM=1 (p=0.529), RF=0 (p=0.084) | `Cara panggil na localhost/SistemRumahSakit/gerbang/rawatdarurat`
- `idx=1065` | `Korpus_Pajak_Terverifikasi` | `Resmi_WA_Blast_Coretax` | Aktual=0, SVM=0 (p=0.070), RF=1 (p=0.516) | `Yth. Wajib Pajak, pastikan Anda hanya merujuk pada pengumuman resmi di laman www.pajak.go.id dan media sosial `
