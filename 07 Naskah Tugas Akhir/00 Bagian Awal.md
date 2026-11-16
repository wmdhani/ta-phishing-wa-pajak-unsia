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

Pelaku *phishing* di WhatsApp yang mengaku sebagai Direktorat Jenderal Pajak biasanya mengirim berkas `.apk` atau tautan *Coretax* palsu kepada korbannya. Penelitian ini menguji dua algoritma, yaitu *Support Vector Machine* dan *Random Forest*, dengan fitur berbobot *Term Frequency-Inverse Document Frequency* (TF-IDF), lalu menanamkan model terbaik ke *prototype* layanan web dan ekstensi peramban *WhatsApp Web* agar pengguna dapat memeriksa pesan secara langsung. Data yang dipakai berjumlah 1.164 teks, terdiri atas 904 pesan umum dan 260 pesan bertema pajak dengan komposisi seimbang, yang diproses melalui *stopword removal* dan *stemming* Sastrawi. *Support Vector Machine* mencatat akurasi 98,28%, *recall* 0,98, dan *F1-Score* 0,98, sedangkan *Random Forest* memperoleh akurasi 95,28% dengan *recall* 0,95 dan *F1-Score* 0,94. Integrasi model terbaik pada *backend* FastAPI, *dashboard* Streamlit, dan ekstensi peramban berfitur penjelasan kata pemicu memudahkan verifikasi pesan tanpa salin-tempel manual.

Kata Kunci: Deteksi Phishing, Otoritas Perpajakan, Random Forest, Support Vector Machine, TF-IDF.

# ABSTRACT

Scammers who pose as the Directorate General of Taxes on WhatsApp often send malicious `.apk` files or fake *Coretax* links. This study evaluates *Support Vector Machine* and *Random Forest* classifiers using *Term Frequency-Inverse Document Frequency* (TF-IDF) weighting, and embeds the better model into a web service and *WhatsApp Web* browser extension prototype for direct message verification. The dataset contains 1,164 texts, made up of 904 general messages and 260 balanced tax-related messages, processed with Sastrawi stopword removal and stemming. *Support Vector Machine* reached 98.28% accuracy, 0.98 recall, and 0.98 *F1-Score*, while *Random Forest* scored 95.28% accuracy with 0.95 recall and 0.94 *F1-Score*. Integrating the best model into a FastAPI backend, Streamlit dashboard, and explainable browser extension enables rapid message inspection without manual copy-pasting.

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
| 1.2 Rumusan Masalah | 3 |
| 1.3 Batasan Masalah | 3 |
| 1.4 Tujuan Penelitian | 5 |
| 1.5 Manfaat Penelitian | 5 |
| 1.6 Metode Penelitian | 6 |
| Bab II Landasan Metode | 9 |
| 2.1 Penelitian Terdahulu dan Matriks Komparasi | 9 |
| 2.2 Landasan Teori dan Metode Khusus | 12 |
| 2.2.1 Algoritma *Support Vector Machine*, *LinearSVC*, dan Kalibrasi Platt | 12 |
| 2.2.2 Algoritma *Random Forest* | 13 |
| 2.2.3 Praproses Teks Bahasa Indonesia dan Pembobotan Fitur TF-IDF | 13 |
| 2.2.4 Validasi Silang Terstratifikasi, Metrik Evaluasi, dan Kesiapterapan Teknologi | 14 |
| 2.3 Prosedur Operasional dan Bagan Alir Penelitian | 15 |
| 2.4 Waktu dan Lokasi Penelitian | 16 |
| 2.5 Alat dan Bahan Penelitian | 17 |
| 2.6 Cara Pengumpulan dan Analisis Data | 19 |
| 2.7 Definisi Operasional Variabel dan Parameter | 19 |
| Daftar Pustaka | 22 |

---

# DAFTAR GAMBAR

| Nomor Gambar | Judul Gambar | Halaman |
| :--- | :--- | :---: |
| Gambar 1.1 | Tahapan Metode Penelitian | 8 |
| Gambar 2.1 | Bagan Alir Prosedur Eksperimen | 16 |

---

# DAFTAR TABEL

| Nomor Tabel | Judul Tabel | Halaman |
| :--- | :--- | :---: |
| Tabel 1.1 | Komposisi Korpus Dataset Penelitian | 7 |
| Tabel 2.1 | Matriks Penelitian Terdahulu | 10 |
| Tabel 2.2 | Jadwal Pelaksanaan Penelitian | 17 |
| Tabel 2.3 | Spesifikasi Alat dan Bahan Penelitian | 18 |
| Tabel 2.4 | Definisi Operasional Variabel dan Parameter Penelitian | 21 |

---
