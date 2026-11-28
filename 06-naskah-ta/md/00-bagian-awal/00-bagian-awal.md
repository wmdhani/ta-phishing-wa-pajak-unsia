# TUGAS AKHIR

## KOMPARASI ALGORITMA SUPPORT VECTOR MACHINE DAN RANDOM FOREST DALAM DETEKSI PESAN PHISHING WHATSAPP MENGATASNAMAKAN OTORITAS PERPAJAKAN

## Sebagai Salah Satu Syarat untuk Memperoleh Gelar Sarjana Komputer pada Program Studi PJJ Sistem Informasi

![Logo Universitas Siber Asia](../../aset-gambar/Logo UNSIA.png)

## Oleh :

## 240101020194, Wan Mirza Dhani

## PROGRAM STUDI PJJ SISTEM INFORMASI

## UNIVERSITAS SIBER ASIA

## NOVEMBER 2026

---

# HALAMAN PERNYATAAN ORISINALITAS

Saya yang bertanda tangan di bawah ini:

| Atribut Identitas | Keterangan Mahasiswa |
| :--- | :--- |
| Nama | Wan Mirza Dhani |
| NIM | 240101020194 |
| Judul Tugas Akhir | Komparasi Algoritma Support Vector Machine dan Random Forest dalam Deteksi Pesan Phishing WhatsApp Mengatasnamakan Otoritas Perpajakan |

Menyatakan dengan sesungguhnya bahwa Tugas Akhir ini merupakan hasil penelitian, pemikiran, dan pemaparan asli saya sendiri. Saya tidak mencantumkan tanpa pengakuan bahan-bahan yang telah dipublikasikan sebelumnya atau ditulis oleh orang lain, atau sebagai bahan yang pernah diajukan untuk gelar atau ijazah pada Universitas Siber Asia atau Perguruan Tinggi lainnya.

Apabila di kemudian hari terdapat penyimpangan dan ketidakbenaran dalam pernyataan ini, maka saya bersedia menerima sanksi akademik sesuai dengan peraturan yang berlaku di Universitas Siber Asia.

Demikian pernyataan ini saya buat.

| Tempat dan Tanggal | Tanda Tangan di Atas Meterai Rp10.000 | Nama Lengkap Mahasiswa |
| :--- | :---: | :--- |
| Jakarta, ...... / ................ / 2026 | (meterai Rp10.000) | (Wan Mirza Dhani) |

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
| Dosen Pembimbing | (Novi Dian Nathasia, S.Kom, MMSI.) | .......................... |
| Ketua Program Studi | (Vika Febri Muliati, S.Kom., M.Kom) | .......................... |
| Ditetapkan di | Jakarta | |
| Tanggal | ...... / ................ / 2026 | |

---

# ABSTRAK

Pelaku *phishing* di WhatsApp yang mengaku sebagai Direktorat Jenderal Pajak kerap mengirim berkas `.apk` berbahaya atau tautan *Coretax* palsu. Penelitian ini membandingkan *Support Vector Machine* (`LinearSVC`) dan *Random Forest* memakai pembobotan *Term Frequency-Inverse Document Frequency* (TF-IDF), lalu menanamkan model terbaik ke purwarupa web *Cek Pesan Pajak* serta ekstensi *WhatsApp Web*. Dataset induk kurasi berjumlah 1.164 teks (904 pesan singkat umum publik dan 260 pesan pajak berimbang), menghasilkan 1.159 teks unik pascapembersihan kata umum, *stemming* Sastrawi, serta deduplikasi. Pada validasi silang sepuluh lipatan dengan TF-IDF unigram-bigram, `LinearSVC` meraih *F1-Score* 97,16% (*Accuracy* 97,74%) mengungguli *Random Forest* 94,07% (*Accuracy* 95,25%), serta mencapai *F1-Score* 98,17% pada korpus pajak 260 baris. Uji kontrol membuktikan pelatihan pesan umum saja hanya meraih akurasi 42,22% pada subset pajak, sedangkan korpus berimbang mengangkatnya ke 95,56%. Setelah kalibrasi *Platt scaling*, akurasi *holdout* `LinearSVC` (95,69%) berbeda tidak bermakna terhadap *Random Forest* (96,55%; McNemar p = 0,7266), tetapi jauh lebih terkalibrasi (*Brier Score* 0,02542 berbanding 0,04214; *ROC-AUC* 0,9957) dan unggul pada korpus diperluas 2.519 baris (96,03% berbanding 92,46%). Integrasi model bersama penjaga `.apk` dan `pajak.go.id` ke FastAPI serta ekstensi memfasilitasi verifikasi instan dalam uji simulasi lokal.

Kata Kunci: Deteksi Phishing, Otoritas Perpajakan, Random Forest, Support Vector Machine, TF-IDF.

# ABSTRACT

Scammers impersonating Indonesia's Directorate General of Taxes on WhatsApp frequently send malicious `.apk` files or fake *Coretax* links. This study compares *Support Vector Machine* (`LinearSVC`) and *Random Forest* classifiers using *Term Frequency-Inverse Document Frequency* (TF-IDF) features, embedding the calibrated winner into the *Cek Pesan Pajak* web prototype and a *WhatsApp Web* extension. The curated primary dataset comprises 1,164 Indonesian texts (904 public short messages and 260 balanced tax messages), yielding 1,159 unique texts after stopword removal, Sastrawi stemming, and deduplication. Under ten-fold cross-validation on unigram-bigram TF-IDF, `LinearSVC` achieved a 97.16% *F1-Score* (97.74% accuracy) over *Random Forest* at 94.07% (95.25% accuracy), while reaching 98.17% on the 260-row tax corpus. Training on general messages alone reached 42.22% accuracy on the tax subset, whereas balanced curation lifted it to 95.56%. Following Platt scaling, `LinearSVC` holdout accuracy (95.69%) did not differ significantly from *Random Forest* (96.55%; McNemar p = 0.7266), yet proved better calibrated (*Brier Score* 0.02542 versus 0.04214; *ROC-AUC* 0.9957) and led on the 2,519-row corpus (96.03% versus 92.46%). Integrating the model with `.apk` and `pajak.go.id` guards into FastAPI and the extension supports instant verification in local simulation tests.

Keywords: Phishing Detection, Random Forest, Support Vector Machine, Tax Authority, TF-IDF.

---

# KATA PENGANTAR

Puji syukur penulis panjatkan ke hadirat Tuhan Yang Maha Esa. Atas rahmat-Nya, penulis dapat menyelesaikan Tugas Akhir berjudul *"Komparasi Algoritma Support Vector Machine dan Random Forest dalam Deteksi Pesan Phishing WhatsApp Mengatasnamakan Otoritas Perpajakan"*. Tugas Akhir skema *Prototype* ini disusun sebagai syarat memperoleh gelar Sarjana Komputer pada Program Studi PJJ Sistem Informasi Universitas Siber Asia.

Topik ini dipilih karena penipuan lewat WhatsApp yang mencatut otoritas perpajakan makin sering terjadi dan merugikan masyarakat. Penyusunan laporan serta perancangan purwarupa ini tidak mungkin terlaksana tanpa bimbingan, dukungan, dan bantuan banyak pihak sejak masa perkuliahan berlangsung. Oleh karena itu, penulis menyampaikan ucapan terima kasih yang tulus kepada:

a) Bapak Jang Youn Cho, Ph.D., CPA, selaku Rektor Universitas Siber Asia. Beliau memimpin penyelenggaraan pendidikan tinggi daring sehingga proses studi penulis berjalan baik.

b) Bapak Dr. Ucuk Darusalam, S.T., M.T, selaku Wakil Rektor Bidang Akademik, Penelitian, dan Pengabdian Kepada Masyarakat Universitas Siber Asia. Dukungan beliau membantu tersedianya fasilitas belajar dan penelitian mahasiswa.

c) Ibu Vika Febri Muliati, S.Kom., M.Kom, selaku Ketua Program Studi PJJ Sistem Informasi Universitas Siber Asia. Beliau senantiasa memberikan arahan akademik selama penulis menempuh studi.

d) Bapak Novi Dian Nathasia, S.Kom, MMSI., selaku Dosen Pembimbing Tugas Akhir. Beliau meluangkan waktu dan pikiran untuk membimbing penulis hingga penelitian ini selesai.

e) Seluruh dosen pengajar Program Studi PJJ Sistem Informasi Universitas Siber Asia. Ilmu sistem informasi yang dibagikan sangat bermanfaat bagi penyusunan penelitian ini.

f) Orang tua dan keluarga penulis yang selalu mendoakan penulis. Dukungan moral serta materi dari keluarga menjadi kekuatan utama selama masa studi.

g) Rekan-rekan mahasiswa Program Studi PJJ Sistem Informasi serta seluruh pihak yang membantu penulis. Diskusi selama penyusunan karya ilmiah ini amat menolong penyelesaian purwarupa sistem.

Penulis menyadari laporan Tugas Akhir ini masih memiliki sejumlah keterbatasan yang perlu disempurnakan di masa mendatang. Oleh sebab itu, kritik dan saran yang membangun sangat penulis harapkan demi perbaikan sistem deteksi ini bagi masyarakat. Akhir kata, semoga Tuhan Yang Maha Esa membalas kebaikan seluruh pihak yang membantu dan karya ilmiah ini membawa manfaat.

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
| Daftar Gambar | x |
| Daftar Tabel | xi |
| Bab I Pendahuluan | 1 |
| 1.1 Latar Belakang Masalah | 1 |
| 1.2 Rumusan Masalah | 2 |
| 1.3 Batasan Masalah | 3 |
| 1.4 Tujuan Penelitian | 4 |
| 1.5 Manfaat Penelitian | 4 |
| 1.6 Metode Penelitian | 5 |
| Bab II Landasan Metode | 7 |
| 2.1 Penelitian Terdahulu dan Matriks Komparasi | 7 |
| 2.2 Landasan Teori dan Metode Khusus | 8 |
| 2.2.1 Algoritma *Support Vector Machine*, *LinearSVC*, dan Kalibrasi Platt | 8 |
| 2.2.2 Algoritma *Random Forest* | 9 |
| 2.2.3 Praproses Teks Bahasa Indonesia dan Pembobotan Fitur TF-IDF | 9 |
| 2.2.4 Validasi Silang Terstratifikasi, Metrik Evaluasi, dan Kalibrasi Probabilitas | 10 |
| 2.2.5 Indikator Kelayakan Purwarupa dan Kesiapterapan Teknologi (TKT Level 6) | 11 |
| 2.3 Prosedur Operasional dan Bagan Alir Penelitian | 11 |
| 2.4 Waktu dan Lokasi Penelitian | 13 |
| 2.5 Alat dan Bahan Penelitian | 13 |
| 2.6 Cara Pengumpulan dan Analisis Data | 14 |
| 2.7 Definisi Operasional Variabel dan Parameter | 14 |
| Bab III Implementasi Metode Usulan | 15 |
| 3.1 Arsitektur Implementasi Metode Usulan | 15 |
| 3.2 Implementasi Kurasi Korpus dan Praproses Teks | 16 |
| 3.3 Implementasi Pelatihan Model, Penyetelan Hiperparameter, dan Kalibrasi | 17 |
| 3.4 Implementasi Purwarupa Sistem Terpadu Tingkat Kesiapan Teknologi 6 | 19 |
| 3.5 Skenario Pengujian Sistem dan Kesiapan Evaluasi | 20 |
| Bab IV Hasil dan Analisa | 22 |
| 4.1 Hasil Eksperimen Komparasi Klasifikasi dan Penyetelan Hiperparameter | 22 |
| 4.2 Analisis Kalibrasi Probabilitas dan Studi Ablatif Fitur | 24 |
| 4.3 Analisis Ketahanan Bias Kata Kunci Pajak dan Generalisasi Lintas Korpus | 25 |
| 4.4 Analisis Interpretabilitas Fitur dan Kesalahan Prediksi | 26 |
| 4.5 Hasil Pengujian Purwarupa Sistem Terpadu dan Evaluasi Kesiapterapan Teknologi | 26 |
| Bab V Kesimpulan | 29 |
| 5.1 Kesimpulan | 29 |
| 5.2 Saran | 30 |
| Daftar Pustaka | 31 |
| Lampiran | 36 |
| Lampiran 1. Matriks Penelitian Terdahulu | 36 |
| Lampiran 2. Jadwal, Alat, Bahan, dan Definisi Operasional | 37 |
| Lampiran 3. Pemetaan Modul Kode, Kontrak API, Matriks Skenario Uji, dan Rancangan Antarmuka | 39 |
| Lampiran 4. Evaluasi ROC-PR, Studi Ablatif, Bobot Fitur, Analisis Kesalahan, dan Hasil Uji Purwarupa | 42 |
| Lampiran 5. Daftar Riwayat Hidup Penulis | 48 |

---

# DAFTAR GAMBAR

| Nomor Gambar | Judul Gambar | Halaman |
| :--- | :--- | :---: |
| Gambar 1.1 | Tahapan Metode Penelitian | 6 |
| Gambar 2.1 | Bagan Alir Prosedur Eksperimen | 13 |
| Gambar 3.1 | Arsitektur Sistem Terpadu Deteksi *Phishing* WhatsApp Perpajakan | 15 |
| Gambar 4.1 | Perbandingan *Confusion Matrix* Uji *Holdout* | 24 |
| Gambar 4.2 | Evaluasi Kalibrasi Probabilitas Model | 25 |
| Gambar 4.3 | Tangkapan Layar Antarmuka Web *Cek Pesan Pajak* dan Respons API | 27 |
| Gambar L.1 | Rancangan Antarmuka Web *Cek Pesan Pajak* dan Ekstensi *WhatsApp Web* | 41 |
| Gambar L.2 | Evaluasi Diskriminatif Kurva ROC dan *Precision-Recall* | 42 |
| Gambar L.3 | Analisis Interpretabilitas Fitur TF-IDF Terbaik | 43 |
| Gambar L.4 | Komparasi Generalisasi Lintas Korpus dan Subset Pajak | 46 |
| Gambar L.5 | Analisis Interpretabilitas Model Berbasis SHAP | 46 |
| Gambar L.6 | Tangkapan Layar Ekstensi Chrome pada Simulasi *WhatsApp Web* | 47 |

---

# DAFTAR TABEL

| Nomor Tabel | Judul Tabel | Halaman |
| :--- | :--- | :---: |
| Tabel 1.1 | Komposisi Korpus Dataset Penelitian | 5 |
| Tabel 3.1 | Konfigurasi Ruang Pencarian Hiperparameter pada Penyetelan 10-Fold CV | 18 |
| Tabel 4.1 | Hasil Komparasi Kinerja Klasifikasi pada Berbagai Tahap Evaluasi | 23 |
| Tabel 4.2 | Perbandingan Hasil Pengujian Penelitian terhadap Kondisi Nyata Operasional | 28 |
| Tabel L.1 | Matriks Penelitian Terdahulu | 36 |
| Tabel L.2 | Jadwal Pelaksanaan Penelitian | 37 |
| Tabel L.3 | Spesifikasi Alat dan Bahan Penelitian | 37 |
| Tabel L.4 | Definisi Operasional Variabel dan Parameter Penelitian | 38 |
| Tabel L.5 | Pemetaan Modul Kode Sumber terhadap Tahapan Metodologi Penelitian | 39 |
| Tabel L.6 | Spesifikasi Titik Akhir Layanan Web dan REST API FastAPI | 39 |
| Tabel L.7 | Matriks Skenario Pengujian Otomatis Purwarupa dan Integritas Sistem | 40 |
| Tabel L.8 | Hasil Studi Ablatif Praproses dan Representasi Fitur TF-IDF | 42 |
| Tabel L.9 | Perbandingan Fitur Teratas `LinearSVC` dan *Random Forest* | 43 |
| Tabel L.10 | Ringkasan Analisis Kesalahan Prediksi pada Himpunan Uji *Holdout* | 43 |
| Tabel L.11 | Hasil Pengujian Fungsional Otomatis dan Latensi Inferensi Purwarupa | 44 |
| Tabel L.12 | Komparasi Hasil Penelitian terhadap Studi Terdahulu | 47 |

---
