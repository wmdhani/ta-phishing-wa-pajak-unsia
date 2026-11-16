# Glosarium Tugas Akhir (Panduan Hafalan & Sidang)

**Judul TA**: *Komparasi Algoritma Support Vector Machine dan Random Forest dalam Deteksi Pesan Phishing WhatsApp Mengatasnamakan Otoritas Perpajakan*

---

## 1. Domain Perpajakan & Rekayasa Sosial
- **Phishing**: Upaya penipuan digital dengan menyamar sebagai pihak tepercaya (seperti DJP) untuk mencuri kredensial, data pribadi, atau uang korban.
- **Smishing**: Bentuk *phishing* yang dikirim melalui pesan singkat (SMS atau aplikasi pesan seperti WhatsApp).
- **Social Engineering (Rekayasa Sosial)**: Manipulasi psikologis korban (misalnya rasa panik akan denda/pemblokiran atau iming-iming restitusi) agar mau mengklik tautan atau mengunduh berkas berbahaya.
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
- **Korpus Dasar SMS (904 baris)**: Dataset publik SMS berbahasa Indonesia (Rahmi & Wibisono: **335** penipuan, **569** normal), hasil penyaringan dari total **1.143 baris** setelah mengeksklusi **239** pesan promo/operator.
- **Korpus Spesifik Pajak (260 baris)**: Kumpulan pesan bertema perpajakan yang seimbang (**130** *phishing* dari **12 kategori modus** dan **130** pesan resmi/normal dari **10 kategori layanan**), dikurasi dari **65 dari 68 sumber publik** yang dihimpun (sebagian besar terbit 2024–2026) tanpa data rahasia internal.
- **Dataset Gabungan Utama (1.164 baris)**: Gabungan 904 korpus SMS dasar + 260 korpus spesifik pajak (**465** kelas `1` *phishing*/spam dan **699** kelas `0` aman/resmi).
- ***Stratified Train-Test Split* (80:20)**: Pembagian dataset menjadi **931 data latih** dan **233 data uji** dengan menjaga proporsi kelas tetap sama di kedua bagian.
- ***Keyword Bias* (Bias Kata Kunci)**: Kondisi saat model salah menganggap kata netral bertema pajak (misalnya *"pajak"*, *"NPWP"*, *"DJP"*) sebagai ciri penipuan karena model belum pernah melihat contoh pesan pajak resmi yang aman.
- **Uji Ablasi (*Ablation Study*)**: Eksperimen melepas/mengubah komponen data untuk mengukur dampaknya. Pada **44 data uji bertema pajak**: model korpus SMS umum hanya mencapai **40,91%**, model tanpa pesan resmi pajak seimbang mencapai **52,27%**, sedangkan model dengan korpus seimbang lengkap melonjak ke **97,73%**.
- **SHA-256 *Checksum***: Sidik jari kriptografis berkas dataset untuk menjamin integritas data tidak berubah selama riset.

---

## 3. Pra-pengolahan Teks (NLP) & Ekstraksi Fitur
- **NLP (*Natural Language Processing*)**: Cabang kecerdasan buatan agar komputer dapat memahami dan mengolah bahasa manusia (teks pesan WhatsApp).
- ***Case Folding***: Menyeragamkan seluruh huruf teks menjadi huruf kecil agar `"PAJAK"` dan `"pajak"` dianggap sama.
- **Tokenisasi Khusus (`token_apk` & `token_url`)**: Mengubah penyebutan berkas `.apk` menjadi token `token_apk` dan tautan HTTP/HTTPS menjadi `token_url` sebelum tanda baca dihapus, sehingga sinyal berbahaya tetap tertangkap model.
- **Pembersihan Karakter Nonalfanumerik**: Menghapus simbol, angka terisolasi, atau tanda baca yang tidak memberi makna klasifikasi.
- ***Stopword Removal***: Menghapus kata penghubung/umum yang terlalu sering muncul dan kurang informatif (seperti *"yang"*, *"di"*, *"dan"*).
- ***Stemming* Sastrawi**: Mengubah kata berimbuhan bahasa Indonesia ke bentuk kata dasarnya (misalnya *"pemutakhiran"* → *"mutakhir"*) menggunakan algoritma *Confix-Stripping*.
- **TF-IDF (*Term Frequency–Inverse Document Frequency*)**: Metode pembobotan kata; memberi bobot tinggi pada kata yang sering muncul di suatu pesan tetapi jarang muncul di seluruh korpus.
- ***N-gram* `(1, 2)` (Maks. 3.000 Fitur)**: Pengambilan fitur berupa 1 kata (*unigram*, misal `"efin"`) dan 2 kata berurutan (*bigram*, misal `"unduh apk"`), dibatasi maksimal 3.000 fitur terpenting.
- ***Sparse Matrix* (Matriks Jarang)**: Representasi angka hasil TF-IDF yang sebagian besar nilainya nol karena setiap pesan pendek hanya mengandung sedikit kata dari 3.000 kosakata.

---

## 4. Algoritma *Machine Learning* yang Dikomparasikan
- ***Supervised Learning* (Pembelajaran Terawasi)**: Pelatihan model menggunakan data yang sudah diberi label (`1` = *phishing/fraud*, `0` = aman/resmi).
- **SVM (*Support Vector Machine* — `LinearSVC`)**: Algoritma yang mencari garis/bidang pemisah (*hyperplane*) dengan jarak paling lebar (*maximum margin*) antar kelas; sangat unggul pada data teks TF-IDF berdimensi tinggi. Hasil *baseline*: akurasi **98,28%** (`Recall` `0,98`; `F1-Score` `0,98`).
- ***Platt Scaling* (Kalibrasi Probabilitas)**: Teknik mengubah nilai jarak (*decision function*) dari `LinearSVC` menjadi skor probabilitas (0%–100%) agar mudah dibaca pengguna.
- ***Random Forest Classifier***: Algoritma *ensemble* yang menggabungkan banyak pohon keputusan (*decision trees*, `n_estimators=200` pada *baseline*) melalui pemungutan suara mayoritas (*bagging*). Hasil *baseline*: akurasi **95,28%** (`Recall` `0,95`; `F1-Score` `0,94`).

---

## 5. Metrik Evaluasi & Validasi
- ***Confusion Matrix***: Tabel 2×2 pencocokan prediksi vs label asli:
  - **TP (*True Positive*)**: *Phishing* terdeteksi benar sebagai *phishing*.
  - **TN (*True Negative*)**: Pesan resmi/aman terdeteksi benar sebagai aman.
  - **FP (*False Positive*)**: Pesan resmi DJP salah dituduh *phishing* (bahaya: informasi penting terblokir).
  - **FN (*False Negative*)**: Pesan *phishing* lolos dianggap aman (bahaya paling fatal: wajib pajak tertipu).
- ***Accuracy* (Akurasi)**: Persentase seluruh prediksi benar dari total data uji (`LinearSVC` **98,28%** vs `Random Forest` **95,28%**).
- ***Precision* (Presisi)**: Dari seluruh pesan yang diprediksi *phishing*, berapa persen yang benar-benar *phishing* (mengukur minimnya *False Positive*).
- ***Recall* (Sensitivitas)**: Dari seluruh pesan *phishing* yang sebenarnya, berapa persen yang berhasil ditangkap model (mengukur minimnya *False Negative*).
- ***F1-Score***: Rata-rata harmonik antara *Precision* dan *Recall* (metrik penting saat distribusi kelas tidak persis 50:50).
- ***10-Fold Cross-Validation***: Membagi data menjadi 10 lipatan dan menguji model 10 kali secara bergantian untuk memastikan performa konsisten (**97,31%** default / **97,74%** tuned untuk `LinearSVC` vs **95,06%** / **95,27%** untuk `Random Forest`).
- **ROC-AUC & PR-AUC**: Luas area di bawah kurva ROC dan *Precision–Recall*; mengukur kemampuan pemisahan kelas di berbagai ambang batas skor (mendekati `1,0` berarti sangat baik).

---

## 6. Arsitektur Purwarupa & Kesiapan Teknologi
- **TKT Level 6 (*Tingkat Kesiapan Teknologi*)**: Purwarupa sistem telah diintegrasikan dan diuji fungsionalnya pada lingkungan operasional yang relevan (bukan sekadar teori/skrip lokal).
- **REST API (`FastAPI`)**: Layanan *backend* cepat berbasis Python yang menerima teks pesan WhatsApp via HTTP dan mengembalikan hasil prediksi, probabilitas, serta penjelasan fitur.
- **Ekstensi Peramban *WhatsApp Web* (`Manifest V3`)**: Pengaya Chrome/Edge yang menyuntikkan tombol/lencana pemeriksaan langsung ke gelembung obrolan dan menu klik kanan di *WhatsApp Web* agar pengguna tidak perlu *copy-paste*.
- ***Dashboard* `Streamlit`**: Antarmuka web interaktif untuk pengujian manual, demonstrasi model, dan inspeksi metrik evaluasi.
- ***Explainable Detection* (XAI)**: Kemampuan sistem menjelaskan *mengapa* suatu pesan dicurigai—menampilkan kata/frasa pemicu dari bobot `LinearSVC`, peringatan `token_apk`, dan status domain `pajak.go.id`.
- **`Joblib`**: Pustaka Python untuk menyimpan dan memuat ulang model `LinearSVC` beserta *vectorizer* TF-IDF yang sudah dilatih (`model_phishing_pajak.joblib`).
