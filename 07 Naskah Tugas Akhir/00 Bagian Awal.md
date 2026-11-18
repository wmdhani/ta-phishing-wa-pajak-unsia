# TUGAS AKHIR

## KOMPARASI ALGORITMA SUPPORT VECTOR MACHINE DAN RANDOM FOREST DALAM DETEKSI PESAN PHISHING WHATSAPP MENGATASNAMAKAN OTORITAS PERPAJAKAN

## Sebagai Salah Satu Syarat untuk Memperoleh Gelar Sarjana Komputer pada Program Studi PJJ Sistem Informasi

![Logo Universitas Siber Asia](Aset Gambar/Logo UNSIA.png)

## Oleh :

## 240101020194, Wan Mirza Dhani

## PROGRAM STUDI PJJ SISTEM INFORMASI

## UNIVERSITAS SIBER ASIA

## NOVEMBER 2026

---

# HALAMAN PERNYATAAN ORISINALITAS

Saya yang bertanda-tangan di bawah ini:

| Atribut Identitas | Keterangan Mahasiswa |
| :--- | :--- |
| Nama | Wan Mirza Dhani |
| NIM | 240101020194 |
| Judul Tugas Akhir | Komparasi Algoritma Support Vector Machine dan Random Forest dalam Deteksi Pesan Phishing WhatsApp Mengatasnamakan Otoritas Perpajakan |

Menyatakan dengan sesungguhnya bahwa Tugas Akhir ini merupakan hasil penelitian, pemikiran dan pemaparan asli saya sendiri. Saya tidak mencantumkan tanpa pengakuan bahan-bahan yang telah dipublikasikan sebelumnya atau ditulis oleh orang lain, atau sebagai bahan yang pernah diajukan untuk gelar atau ijazah pada Universitas Siber Asia atau Perguruan Tinggi lainnya.

Apabila di kemudian hari terdapat penyimpangan dan ketidakbenaran dalam pernyataan ini, maka saya bersedia menerima sanksi akademik sesuai dengan peraturan yang berlaku di Universitas Siber Asia.

Demikian pernyataan ini saya buat.

| Tempat dan Tanggal | Tanda Tangan di Atas Materai Rp10.000 | Nama Lengkap Mahasiswa |
| :--- | :---: | :--- |
| Jakarta, ...... / ................ / 2026 | (materai Rp 10.000,-) | (Wan Mirza Dhani) |

---

# HALAMAN PENGESAHAN

Tugas Akhir ini diajukan oleh :

| Atribut Pengajuan | Keterangan Mahasiswa |
| :--- | :--- |
| Nama | Wan Mirza Dhani |
| NIM | 240101020194 |
| Program Studi | PJJ Sistem Informasi |
| Judul Tugas Akhir | Komparasi Algoritma Support Vector Machine dan Random Forest dalam Deteksi Pesan Phishing WhatsApp Mengatasnamakan Otoritas Perpajakan |

Telah berhasil dipertahankan di hadapan Dewan Penguji dan diterima sebagai bagian persyaratan yang diperlukan untuk memperoleh gelar Sarjana Komputer pada Program Studi PJJ Sistem Informasi Universitas Siber Asia.

| Jabatan Dewan Sidang | Nama Lengkap dan Gelar Akademik | Tanda Tangan |
| :--- | :--- | :--- |
| Ketua Sidang / Dosen Penguji I | (..........................................) | .......................... |
| Dosen Penguji II | (..........................................) | .......................... |
| Dosen Pembimbing I | (Novi Dian Nathasia, S.Kom., MMSI) | .......................... |
| Dosen Pembimbing II | (..........................................) | .......................... |
| Ketua Program Studi | (Vika Febri Muliati, S.Kom., M.Kom) | .......................... |
| Ditetapkan di | Jakarta | |
| Tanggal | ...... / ................ / 2026 | |

---

# ABSTRAK

Pelaku *phishing* di WhatsApp yang mengaku sebagai Direktorat Jenderal Pajak kerap mengirim berkas `.apk` atau tautan *Coretax* palsu kepada korban. Penelitian ini membandingkan algoritma *Support Vector Machine* (`LinearSVC`) dan *Random Forest* menggunakan fitur *Term Frequency-Inverse Document Frequency* (TF-IDF), lalu menanamkan model terbaik ke aplikasi web *Cek Pesan Pajak* serta ekstensi peramban *WhatsApp Web*. Dataset berjumlah 1.164 teks, terdiri atas 904 pesan umum dan 260 pesan bertema pajak berimbang yang diproses melalui *stopword removal* dan *stemming* Sastrawi. Pada uji dasar (*baseline*), `LinearSVC` mencatat akurasi 98,28% (*recall* 0,98; *F1-Score* 0,98) mengungguli *Random Forest* sebesar 95,28% (*recall* 0,95; *F1-Score* 0,94). Setelah penalaan parameter dan kalibrasi *Platt scaling*, `LinearSVC` mempertahankan akurasi uji 97,42% (*Brier Score* 0,019) serta mencapai akurasi 97,73% pada subset pesan pajak, jauh melampaui *Random Forest* sebesar 88,64%. Integrasi model terbaik ke peladen FastAPI dan ekstensi peramban berfitur alasan berbahasa awam memampukan verifikasi langsung tanpa salin-tempel manual.

Kata Kunci: Deteksi Phishing, Otoritas Perpajakan, Random Forest, Support Vector Machine, TF-IDF.

# ABSTRACT

Scammers impersonating Indonesia's Directorate General of Taxes on WhatsApp frequently send malicious `.apk` files or fake *Coretax* links. This study compares *Support Vector Machine* (`LinearSVC`) and *Random Forest* classifiers using *Term Frequency-Inverse Document Frequency* (TF-IDF) features, then embeds the superior model into the *Cek Pesan Pajak* web application and a *WhatsApp Web* browser extension. The balanced dataset contains 1,164 Indonesian texts, comprising 904 general messages and 260 tax-related messages preprocessed with Sastrawi stopword removal and stemming. On the baseline test split, `LinearSVC` achieved 98.28% accuracy (0.98 recall, 0.98 *F1-Score*), outperforming *Random Forest* at 95.28% accuracy (0.95 recall, 0.94 *F1-Score*). After hyperparameter tuning and Platt scaling calibration, `LinearSVC` maintained 97.42% holdout accuracy (0.019 *Brier Score*) and reached 97.73% accuracy on tax-specific messages, substantially exceeding *Random Forest* at 88.64%. Integrating the calibrated model into a FastAPI service and a plain-language browser extension enables immediate message verification without manual copy-pasting.

Keywords: Phishing Detection, Random Forest, Support Vector Machine, Tax Authority, TF-IDF.

---

# KATA PENGANTAR

Puji syukur penulis panjatkan kepada Tuhan Yang Maha Esa. Atas rahmat-Nya, penulis dapat menyelesaikan Tugas Akhir berjudul *"Komparasi Algoritma Support Vector Machine dan Random Forest dalam Deteksi Pesan Phishing WhatsApp Mengatasnamakan Otoritas Perpajakan"*. Tugas Akhir dengan skema *Prototype* ini disusun sebagai salah satu syarat untuk meraih gelar Sarjana Komputer pada Program Studi PJJ Sistem Informasi Universitas Siber Asia.

Topik ini penulis pilih karena semakin sering ditemukan kasus penipuan lewat WhatsApp yang mencatut nama otoritas perpajakan di Indonesia. Penelitian ini tidak mungkin selesai tanpa bantuan dan bimbingan banyak pihak, sejak masa perkuliahan hingga laporan ini tersusun. Oleh sebab itu, penulis mengucapkan terima kasih yang tulus kepada:

a) Bapak Jang Youn Cho, Ph.D., CPA, selaku Rektor Universitas Siber Asia, yang memimpin penyelenggaraan pendidikan tinggi daring sehingga proses studi penulis dapat berjalan.

b) Bapak Dr. Ucuk Darusalam, S.T., M.T., selaku Wakil Rektor Bidang Akademik, Penelitian dan Pengabdian Kepada Masyarakat Universitas Siber Asia, yang mendukung tersedianya fasilitas belajar dan penelitian bagi mahasiswa.

c) Ibu Vika Febri Muliati, S.Kom., M.Kom, selaku Ketua Program Studi PJJ Sistem Informasi Universitas Siber Asia, yang memberikan arahan akademik selama penulis menempuh studi.

d) Bapak Novi Dian Nathasia, S.Kom., MMSI, selaku Dosen Pembimbing Tugas Akhir, yang meluangkan waktu dan pikiran untuk membimbing penulis hingga penelitian ini selesai.

e) Seluruh dosen pengajar Program Studi PJJ Sistem Informasi Universitas Siber Asia, yang telah membekali penulis dengan ilmu komputasi yang sangat berguna.

f) Orang tua dan keluarga penulis, yang tidak pernah berhenti mendoakan. Dukungan moral dan materi dari keluarga menjadi sumber kekuatan utama bagi penulis.

g) Rekan-rekan mahasiswa Program Studi PJJ Sistem Informasi dan semua pihak yang telah membantu penulis. Diskusi selama penyusunan karya ilmiah ini sangat menolong penyelesaian purwarupa sistem.

Penulis menyadari laporan Tugas Akhir ini masih memiliki keterbatasan yang dapat diperbaiki pada penelitian selanjutnya. Karena itu, kritik dan saran yang membangun dari pembaca sangat penulis harapkan untuk menyempurnakan sistem deteksi ini ke depan. Akhir kata, semoga Tuhan Yang Maha Esa membalas kebaikan semua pihak yang telah membantu, dan semoga Tugas Akhir ini bermanfaat bagi pengembangan ilmu pengetahuan.

| Tempat dan Waktu Penyusunan | Identitas Penyusun |
| :--- | :---: |
| Jakarta, November 2026 | **Penulis** |

---

# DAFTAR ISI

| Bagian / Bab / Subbab | Halaman |
| :--- | :---: |
| Halaman Judul | i |
| Halaman Pernyataan Orisinalitas | ii |
| Halaman Pengesahan | iii |
| Halaman Abstrak dan *Abstract* | iv |
| Kata Pengantar | v |
| Daftar Isi | vii |
| Daftar Gambar | ix |
| Daftar Tabel | x |
| Bab I Pendahuluan | 1 |
| 1.1 Latar Belakang Masalah | 1 |
| 1.2 Rumusan Masalah | 2 |
| 1.3 Batasan Masalah | 3 |
| 1.4 Tujuan Penelitian | 4 |
| 1.5 Manfaat Penelitian | 5 |
| 1.6 Metode Penelitian | 6 |
| Bab II Landasan Metode | 8 |
| 2.1 Penelitian Terdahulu dan Matriks Komparasi | 8 |
| 2.2 Landasan Teori dan Metode Khusus | 11 |
| 2.2.1 Algoritma *Support Vector Machine*, *LinearSVC*, dan Kalibrasi Platt | 11 |
| 2.2.2 Algoritma *Random Forest* | 11 |
| 2.2.3 Praproses Teks Bahasa Indonesia dan Pembobotan Fitur TF-IDF | 12 |
| 2.2.4 Validasi Silang Terstratifikasi, Metrik Evaluasi, dan Kesiapterapan Teknologi | 13 |
| 2.3 Prosedur Operasional dan Bagan Alir Penelitian | 13 |
| 2.4 Waktu dan Lokasi Penelitian | 15 |
| 2.5 Alat dan Bahan Penelitian | 16 |
| 2.6 Cara Pengumpulan dan Analisis Data | 17 |
| 2.7 Definisi Operasional Variabel dan Parameter | 18 |
| Bab III Implementasi Metode Usulan | 20 |
| 3.1 Arsitektur Implementasi Metode Usulan | 20 |
| 3.2 Implementasi Kurasi Korpus dan Praproses Teks | 22 |
| 3.3 Implementasi Pelatihan Model, Penyetelan Hiperparameter, dan Kalibrasi | 24 |
| 3.4 Implementasi Purwarupa Sistem Terpadu Tingkat Kesiapan Teknologi 6 | 26 |
| 3.5 Skenario Pengujian Sistem dan Kesiapan Evaluasi | 29 |
| Bab IV Hasil dan Analisa | 31 |
| 4.1 Hasil Eksperimen Komparasi Klasifikasi dan Penyetelan Hiperparameter | 31 |
| 4.2 Analisis Kalibrasi Probabilitas dan Studi Ablatif Fitur | 34 |
| 4.3 Analisis Ketahanan Bias Kata Kunci Pajak dan Generalisasi Lintas Korpus | 36 |
| 4.4 Analisis Interpretabilitas Fitur dan Kesalahan Prediksi | 37 |
| 4.5 Hasil Pengujian Purwarupa Sistem Terpadu dan Evaluasi Kesiapterapan Teknologi | 42 |
| Daftar Pustaka | 47 |

---

# DAFTAR GAMBAR

| Nomor Gambar | Judul Gambar | Halaman |
| :--- | :--- | :---: |
| Gambar 1.1 | Tahapan Metode Penelitian | 7 |
| Gambar 2.1 | Bagan Alir Prosedur Eksperimen | 15 |
| Gambar 3.1 | Arsitektur Sistem Terpadu Deteksi *Phishing* WhatsApp Perpajakan | 20 |
| Gambar 3.2 | Rancangan Antarmuka Web *Cek Pesan Pajak* dan Ekstensi *WhatsApp Web* | 28 |
| Gambar 4.1 | Perbandingan *Confusion Matrix* Uji *Holdout* | 33 |
| Gambar 4.2 | Evaluasi Diskriminatif Kurva ROC dan *Precision-Recall* | 33 |
| Gambar 4.3 | Evaluasi Kalibrasi Probabilitas Model | 34 |
| Gambar 4.4 | Analisis Interpretabilitas Fitur TF-IDF Terbaik | 38 |
| Gambar 4.5 | Komparasi Generalisasi Lintas Korpus dan Subset Pajak | 37 |
| Gambar 4.6 | Tangkapan Layar Antarmuka Web *Cek Pesan Pajak* dan Respons API | 44 |
| Gambar 4.7 | Tangkapan Layar Ekstensi Chrome pada Simulasi *WhatsApp Web* | 45 |
| Gambar 4.8 | Analisis Interpretabilitas Model Berbasis SHAP | 40 |

---

# DAFTAR TABEL

| Nomor Tabel | Judul Tabel | Halaman |
| :--- | :--- | :---: |
| Tabel 1.1 | Komposisi Korpus Dataset Penelitian | 6 |
| Tabel 2.1 | Matriks Penelitian Terdahulu | 9 |
| Tabel 2.2 | Jadwal Pelaksanaan Penelitian | 15 |
| Tabel 2.3 | Spesifikasi Alat dan Bahan Penelitian | 16 |
| Tabel 2.4 | Definisi Operasional Variabel dan Parameter Penelitian | 19 |
| Tabel 3.1 | Pemetaan Modul Kode Sumber terhadap Tahapan Metodologi Penelitian | 21 |
| Tabel 3.2 | Konfigurasi Ruang Pencarian Hiperparameter dan Parameter Terpilih | 25 |
| Tabel 3.3 | Spesifikasi Titik Akhir Layanan Web dan REST API FastAPI (`api.py`) | 27 |
| Tabel 3.4 | Matriks Skenario Pengujian Otomatis Purwarupa dan Integritas Sistem | 29 |
| Tabel 4.1 | Hasil Komparasi Kinerja Klasifikasi pada Berbagai Tahap Evaluasi | 32 |
| Tabel 4.2 | Hasil Studi Ablatif Praproses dan Representasi Fitur TF-IDF | 35 |
| Tabel 4.3 | Perbandingan Fitur Teratas `LinearSVC` dan *Random Forest* | 38 |
| Tabel 4.4 | Ringkasan Analisis Kesalahan Prediksi pada Himpunan Uji *Holdout* | 41 |
| Tabel 4.5 | Hasil Pengujian Fungsional Otomatis dan Latensi Inferensi Purwarupa | 42 |
| Tabel 4.6 | Komparasi Hasil Penelitian terhadap Studi Terdahulu | 45 |

---
