# TUGAS AKHIR

## KOMPARASI ALGORITMA SUPPORT VECTOR MACHINE DAN RANDOM FOREST DALAM DETEKSI PESAN PHISHING WHATSAPP MENGATASNAMAKAN OTORITAS PERPAJAKAN

## Sebagai Salah Satu Syarat untuk Memperoleh Gelar Sarjana Komputer pada Program Studi PJJ Informatika

![Logo Universitas Siber Asia](assets/logo_unsia.png)

## Oleh :

## 240101020194, Wan Mirza Dhani

## PROGRAM STUDI PJJ INFORMATIKA

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
| Program Studi | PJJ Informatika |
| Judul Tugas Akhir | Komparasi Algoritma Support Vector Machine dan Random Forest dalam Deteksi Pesan Phishing WhatsApp Mengatasnamakan Otoritas Perpajakan |

Telah berhasil dipertahankan di hadapan Dewan Penguji dan diterima sebagai bagian persyaratan yang diperlukan untuk memperoleh gelar Sarjana Komputer pada Program Studi PJJ Informatika Universitas Siber Asia.

| Jabatan Dewan Sidang | Nama Lengkap dan Gelar Akademik | Tanda Tangan |
| :--- | :--- | :--- |
| Ketua Sidang / Dosen Penguji I | (..........................................) | .......................... |
| Dosen Penguji II | (..........................................) | .......................... |
| Dosen Pembimbing I | (Novi Dian Nathasia, S.Kom., MMSI) | .......................... |
| Dosen Pembimbing II | (..........................................) | .......................... |
| Ketua Program Studi | (Syahid Abdullah, S.Si, M.Kom) | .......................... |
| Ditetapkan di | Jakarta | |
| Tanggal | ...... / ................ / 2026 | |

---

# ABSTRAK

Penipuan *phishing* pada WhatsApp berkedok Direktorat Jenderal Pajak kerap memanfaatkan berkas `.apk` serta tautan *Coretax* palsu. Penelitian ini membandingkan *Support Vector Machine* dan *Random Forest* berbasis pembobotan *Term Frequency-Inverse Document Frequency* (TF-IDF) sekaligus membangun *prototype* web verifikasi mandiri. Uji eksperimental memadukan 904 pesan umum dan 260 pesan pajak seimbang melalui *stopword removal* serta *stemming* Sastrawi menjadi 1.164 data teks. Hasil membuktikan *Support Vector Machine* meraih akurasi 98,28%, *recall* 0,98, dan *F1-Score* 0,98, mengungguli *Random Forest* berakurasi 95,28% (*recall* 0,95; *F1-Score* 0,94). Integrasi model terbaik pada Streamlit memudahkan verifikasi pesan secara cepat.

Kata Kunci: Deteksi Phishing, Otoritas Perpajakan, Random Forest, Support Vector Machine, TF-IDF.

# ABSTRACT

WhatsApp *phishing* scams impersonating the Directorate General of Taxes frequently distribute malicious `.apk` files and fake *Coretax* links. This study compares *Support Vector Machine* and *Random Forest* with *Term Frequency-Inverse Document Frequency* (TF-IDF) weighting while building a self-verification web prototype. Experimental testing combines 904 general texts and 260 balanced tax messages processed via Sastrawi stopword removal and stemming into 1,164 records. Results prove *Support Vector Machine* achieves 98.28% accuracy, 0.98 recall, and 0.98 *F1-Score*, outperforming *Random Forest* at 95.28% accuracy (0.95 recall; 0.94 *F1-Score*). Integrating the best model into Streamlit enables rapid message verification.

Keywords: Phishing Detection, Random Forest, Support Vector Machine, Tax Authority, TF-IDF.

---

# KATA PENGANTAR

Puji syukur penulis panjatkan ke hadirat Tuhan Yang Maha Esa karena atas rahmat-Nya, penulis dapat menyelesaikan Tugas Akhir ini dengan baik. Tugas Akhir ini berjudul *"Komparasi Algoritma Support Vector Machine dan Random Forest dalam Deteksi Pesan Phishing WhatsApp Mengatasnamakan Otoritas Perpajakan"*. Penulisan karya ilmiah dengan skema *Prototype* ini disusun untuk memenuhi salah satu syarat memperoleh gelar Sarjana Komputer pada Program Studi PJJ Informatika Universitas Siber Asia.

Ketertarikan penulis terhadap permasalahan dalam Tugas Akhir ini berangkat dari maraknya kasus penipuan digital melalui WhatsApp yang mencatut identitas otoritas perpajakan di Indonesia. Penulis menyadari bahwa tanpa bantuan dan bimbingan dari berbagai pihak, dari masa perkuliahan sampai pada penyusunan laporan ini, sangatlah sulit bagi penulis untuk menyelesaikan penelitian ini. Karena itu, penulis menyampaikan ucapan terima kasih yang tulus kepada:

a) Bapak Jang Youn Cho, Ph.D., CPA, selaku Rektor Universitas Siber Asia. Beliau telah memimpin penyelenggaraan pendidikan tinggi berbasis pembelajaran daring yang mendukung proses studi penulis.

b) Bapak Dr. Ucuk Darusalam, S.T., M.T., selaku Wakil Rektor Bidang Akademik, Penelitian dan Pengabdian Kepada Masyarakat Universitas Siber Asia. Beliau telah mendukung penyediaan fasilitas pembelajaran dan penelitian yang memadai bagi mahasiswa.

c) Bapak Syahid Abdullah, S.Si, M.Kom, selaku Ketua Program Studi PJJ Informatika Universitas Siber Asia. Beliau telah memberikan arahan kebijakan akademik selama masa studi penulis.

d) Bapak Novi Dian Nathasia, S.Kom., MMSI, selaku Dosen Pembimbing Tugas Akhir. Beliau telah menyediakan waktu dan pikiran untuk membimbing penulis dalam menyelesaikan penelitian ini.

e) Seluruh dosen pengajar Program Studi PJJ Informatika Universitas Siber Asia. Para pengajar telah membekali penulis dengan ilmu pengetahuan komputasi yang sangat bermanfaat.

f) Orang tua dan keluarga penulis yang selalu memberikan doa setiap waktu. Dukungan moral serta material dari keluarga menjadi penguat utama bagi penulis.

g) Rekan-rekan mahasiswa Program Studi PJJ Informatika beserta semua pihak yang telah membantu penulis. Diskusi selama penyusunan karya ilmiah ini sangat membantu penyelesaian purwarupa sistem.

Penulis menyadari bahwa laporan Tugas Akhir ini masih memiliki keterbatasan yang dapat dikembangkan lebih lanjut pada penelitian berikutnya. Karena itu, penulis mengharapkan saran dan kritik yang membangun dari para pembaca demi penyempurnaan sistem deteksi ini di masa mendatang. Akhir kata, penulis berharap Tuhan Yang Maha Esa berkenan membalas segala kebaikan semua pihak yang telah membantu. Semoga Tugas Akhir ini membawa manfaat nyata bagi pengembangan ilmu pengetahuan.

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
| Daftar Gambar | viii |
| Daftar Tabel | ix |
| Bab I Pendahuluan | 1 |
| 1.1 Latar Belakang Masalah | 1 |
| 1.2 Rumusan Masalah | 2 |
| 1.3 Batasan Masalah | 3 |
| 1.4 Tujuan Penelitian | 4 |
| 1.5 Manfaat Penelitian | 5 |
| 1.6 Metode Penelitian | 6 |
| Daftar Pustaka | 8 |

---

# DAFTAR GAMBAR

| Nomor Gambar | Judul Gambar | Halaman |
| :--- | :--- | :---: |
| Gambar 1.1 | Tahapan Metode Penelitian | 7 |

---

# DAFTAR TABEL

| Nomor Tabel | Judul Tabel | Halaman |
| :--- | :--- | :---: |
| Tabel 1.1 | Komposisi Korpus Dataset Penelitian | 6 |

---
