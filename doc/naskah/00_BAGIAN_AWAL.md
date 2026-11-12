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

| Atribut Identitas | Keterangan Mahasiswa |
| :--- | :--- |
| Pernyataan | Bertanda tangan di bawah ini |
| Nama Mahasiswa | Wan Mirza Dhani |
| Nomor Induk Mahasiswa | 240101020194 (Reguler PJJ) |
| Program Studi | PJJ Informatika |
| Judul Tugas Akhir | Komparasi Algoritma Support Vector Machine dan Random Forest dalam Deteksi Pesan Phishing WhatsApp Mengatasnamakan Otoritas Perpajakan |

"Saya menyatakan dengan sesungguhnya bahwa Tugas Akhir ini adalah hasil penelitian, pemikiran, dan pemaparan asli saya sendiri dengan arahan Dosen Pembimbing. Saya tidak mencantumkan tanpa pengakuan bahan-bahan yang telah dipublikasikan sebelumnya atau ditulis oleh orang lain, atau sebagai bahan yang pernah diajukan untuk memperoleh gelar atau ijazah pada Universitas Siber Asia maupun Perguruan Tinggi lainnya. Apabila di kemudian hari terdapat penyimpangan dan ketidakbenaran dalam pernyataan ini, saya bersedia menerima sanksi akademik sesuai dengan peraturan yang berlaku di Universitas Siber Asia serta melampirkan bukti Turnitin Similarity Check maksimal 30%. Demikian pernyataan ini saya buat."

| Tempat dan Tanggal | Tanda Tangan di Atas Materai Rp10.000 | Nama Lengkap Mahasiswa |
| :--- | :---: | :--- |
| Jakarta, November 2026 | (Materai Rp10.000,-) | **Wan Mirza Dhani** |

---

# HALAMAN PENGESAHAN

| Atribut Pengajuan | Keterangan Mahasiswa |
| :--- | :--- |
| Diajukan Oleh | Mahasiswa Program Studi PJJ Informatika |
| Nama | Wan Mirza Dhani |
| NIM | 240101020194 |
| Program Studi | PJJ Informatika |
| Skema Tugas Akhir | Tugas Akhir *Prototype* |
| Judul Tugas Akhir | Komparasi Algoritma Support Vector Machine dan Random Forest dalam Deteksi Pesan Phishing WhatsApp Mengatasnamakan Otoritas Perpajakan |

Laporan Tugas Akhir ini telah berhasil dipertahankan di hadapan Dewan Penguji dan diterima sebagai bagian persyaratan yang diperlukan untuk memperoleh gelar Sarjana Komputer pada Program Studi PJJ Informatika Universitas Siber Asia. Seluruh catatan perbaikan dari tim penguji maupun dosen pembimbing telah diselesaikan oleh penulis sesuai prosedur akademik yang berlaku. Pengesahan karya ilmiah ini ditetapkan di Jakarta pada bulan November tahun dua ribu dua puluh enam.

| Jabatan Dewan Sidang | Nama Lengkap dan Gelar Akademik | Tanda Tangan |
| :--- | :--- | :--- |
| Ketua Sidang / Dosen Penguji I | (..........................................................) | .......................... |
| Dosen Penguji II | (..........................................................) | .......................... |
| Dosen Pembimbing I | Novi Dian Nathasia, S.Kom, MMSI. | .......................... |
| Dosen Pembimbing II | (..........................................................) | .......................... |
| Ketua Program Studi PJJ Informatika | Cian Ramadhona Hassolthine, S.Kom., M.Kom. | .......................... |
| Ditetapkan di Jakarta | Tanggal: ...... / ................ / 2026 | Status: Disahkan |

---

# ABSTRAK

Penipuan rekayasa sosial (*phishing*) pada WhatsApp yang mengatasnamakan Direktorat Jenderal Pajak marak terjadi melalui kiriman berkas `.apk` dan tautan tiruan *Coretax*. Penelitian ini bertujuan menguji dan membandingkan algoritma *Support Vector Machine* serta *Random Forest* berbasis pembobotan *Term Frequency-Inverse Document Frequency* (TF-IDF) untuk mendeteksi *phishing* perpajakan. Penelitian ini juga membuat *prototype* aplikasi web verifikasi mandiri. Metode eksperimental diterapkan pada 1.164 pesan berbahasa Indonesia yang memadukan 904 pesan umum dan 260 pesan pajak seimbang. Hasil pengujian membuktikan *Support Vector Machine* mencapai akurasi 98,71%, *recall* 1,00, dan *F1-Score* 0,98, mengungguli *Random Forest* berakurasi 96,57%. Model terbaik diintegrasikan ke Streamlit.

Kata Kunci: Deteksi Phishing, Otoritas Perpajakan, Random Forest, Support Vector Machine, TF-IDF.

# ABSTRACT

Social engineering (*phishing*) scams on WhatsApp impersonating the Directorate General of Taxes have proliferated via malicious `.apk` files and fake *Coretax* links. This study aims to test and compare *Support Vector Machine* and *Random Forest* algorithms using *Term Frequency-Inverse Document Frequency* (TF-IDF) features to detect tax *phishing* messages. This research also builds a web prototype for independent verification. An experimental method is applied to 1,164 Indonesian messages combining 904 general texts and 260 balanced tax messages. Results prove *Support Vector Machine* achieves 98.71% accuracy, 1.00 recall, and 0.98 *F1-Score*, outperforming *Random Forest* (96.57%). The model powers Streamlit.

Keywords: Phishing Detection, Random Forest, Support Vector Machine, Tax Authority, TF-IDF.

---

# KATA PENGANTAR

Puji syukur penulis panjatkan ke hadirat Tuhan Yang Maha Esa karena atas rahmat-Nya, penulis dapat menyelesaikan Tugas Akhir ini dengan baik. Tugas Akhir ini berjudul *"Komparasi Algoritma Support Vector Machine dan Random Forest dalam Deteksi Pesan Phishing WhatsApp Mengatasnamakan Otoritas Perpajakan"*. Penulisan karya ilmiah dengan skema *Prototype* ini disusun untuk memenuhi salah satu syarat memperoleh gelar Sarjana Komputer pada Program Studi PJJ Informatika Universitas Siber Asia.

Ketertarikan penulis terhadap permasalahan dalam Tugas Akhir ini berangkat dari maraknya kasus penipuan digital melalui WhatsApp yang mencatut identitas otoritas perpajakan di Indonesia. Penulis menyadari bahwa tanpa bantuan dan bimbingan dari berbagai pihak, dari masa perkuliahan sampai pada penyusunan laporan ini, sangatlah sulit bagi penulis untuk menyelesaikan penelitian ini. Karena itu, penulis menyampaikan ucapan terima kasih yang tulus kepada:

a) Bapak Dr. Ucuk Darusalam, S.T., M.T., selaku Wakil Rektor Bidang Akademik Universitas Siber Asia. Beliau telah mendukung penyediaan fasilitas pembelajaran daring yang memadai bagi mahasiswa.

b) Bapak Cian Ramadhona Hassolthine, S.Kom., M.Kom., selaku Ketua Program Studi PJJ Informatika Universitas Siber Asia. Beliau telah memberikan arahan kebijakan akademik selama masa studi penulis.

c) Ibu Novi Dian Nathasia, S.Kom, MMSI., selaku Dosen Pembimbing Tugas Akhir. Beliau telah menyediakan waktu dan pikiran untuk membimbing penulis dalam menyelesaikan penelitian ini.

d) Seluruh dosen pengajar Program Studi PJJ Informatika Universitas Siber Asia. Para pengajar telah membekali penulis dengan ilmu pengetahuan komputasi yang sangat bermanfaat.

e) Orang tua dan keluarga penulis yang selalu memberikan doa setiap waktu. Dukungan moral serta material dari keluarga menjadi penguat utama bagi penulis.

f) Rekan-rekan mahasiswa Program Studi PJJ Informatika beserta semua pihak yang telah membantu penulis. Diskusi selama penyusunan karya ilmiah ini sangat membantu penyelesaian purwarupa sistem.

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
| Daftar Isi | vi |
| Daftar Tabel | vii |
| Daftar Gambar | viii |
| Bab I Pendahuluan | 1 |
| 1.1 Latar Belakang Masalah | 1 |
| 1.2 Rumusan Masalah | 3 |
| 1.3 Batasan Masalah | 4 |
| 1.4 Tujuan Penelitian | 5 |
| 1.5 Manfaat Penelitian | 5 |
| 1.6 Metode Penelitian | 6 |
| Bab II Landasan Metode | 8 |
| Bab III Implementasi Metode Usulan | 14 |
| Bab IV Hasil dan Analisa | 20 |
| Bab V Kesimpulan | 26 |
| Daftar Pustaka | 28 |
| Lampiran | 30 |

---

# DAFTAR TABEL

| Nomor Tabel | Judul Tabel | Halaman |
| :--- | :--- | :---: |
| Tabel 1.1 | Komposisi Korpus Dataset Penelitian | 6 |
| Tabel 2.1 | Matriks Penelitian Terdahulu | 10 |
| Tabel 2.2 | Definisi Operasional Variabel dan Parameter | 13 |
| Tabel 3.1 | Spesifikasi Lingkungan Pengembangan Prototipe | 15 |
| Tabel 4.1 | Hasil Komparasi Kinerja Model pada Data Uji | 21 |
| Tabel 4.2 | Evaluasi Tingkat Kesiapan Teknologi (TKT) Sistem | 25 |

---

# DAFTAR GAMBAR

| Nomor Gambar | Judul Gambar | Halaman |
| :--- | :--- | :---: |
| Gambar 1.1 | Tahapan Metode Penelitian | 7 |
| Gambar 2.1 | Bagan Alir Prosedur Operasional Penelitian | 11 |
| Gambar 3.1 | Arsitektur Sistem dan Antarmuka Purwarupa Streamlit | 18 |
| Gambar 4.1 | Perbandingan *Confusion Matrix* Algoritma SVM dan *Random Forest* | 22 |
| Gambar 4.2 | Pengujian Fungsional Deteksi Pesan pada Aplikasi Web | 24 |

---
