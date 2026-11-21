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

Pelaku *phishing* di WhatsApp yang mengaku sebagai Direktorat Jenderal Pajak kerap mengirim berkas `.apk` atau tautan *Coretax* palsu kepada korban. Penelitian ini membandingkan algoritma *Support Vector Machine* (`LinearSVC`) dan *Random Forest* menggunakan fitur *Term Frequency-Inverse Document Frequency* (TF-IDF), lalu menanamkan model terbaik ke aplikasi web *Cek Pesan Pajak* serta ekstensi peramban *WhatsApp Web*. Dataset induk berjumlah 1.164 teks (904 pesan umum dan 260 pesan pajak berimbang) yang menghasilkan 1.159 teks unik pascadeduplikasi *stopword removal* dan *stemming* Sastrawi. Pada validasi silang sepuluh lipatan (*10-Fold CV*), `LinearSVC` meraih *F1-Score* 97,16% (*Accuracy* 97,74%) mengungguli *Random Forest* sebesar 94,07% (*Accuracy* 95,25%), serta mencapai *F1-Score* 98,17% pada korpus pajak 260 baris. Uji kontrol membuktikan pelatihan SMS umum saja hanya meraih akurasi 42,22% pada subset pajak, sedangkan korpus berimbang mengangkat akurasi menjadi 95,56%. Setelah kalibrasi *Platt scaling* berbasis *Pipeline*, `LinearSVC` mencatat akurasi *holdout* 95,69% (*ROC-AUC* 0,9957; *Brier Score* 0,02542) yang lebih terkalibrasi daripada *Random Forest* (*Brier Score* 0,04214), serta unggul pada korpus diperluas 2.519 baris (96,03% berbanding 92,46%). Integrasi model ke FastAPI dan ekstensi peramban bersama penjaga heuristik `.apk` serta `pajak.go.id` memampukan verifikasi langsung berbahasa awam.

Kata Kunci: Deteksi Phishing, Otoritas Perpajakan, Random Forest, Support Vector Machine, TF-IDF.

# ABSTRACT

Scammers impersonating Indonesia's Directorate General of Taxes on WhatsApp frequently send malicious `.apk` files or fake *Coretax* links. This study compares *Support Vector Machine* (`LinearSVC`) and *Random Forest* classifiers using *Term Frequency-Inverse Document Frequency* (TF-IDF) features, then embeds the calibrated model into the *Cek Pesan Pajak* web application and a *WhatsApp Web* browser extension. The primary dataset comprises 1,164 Indonesian texts (904 general messages and 260 balanced tax messages), yielding 1,159 unique texts after Sastrawi stopword removal, stemming, and deduplication. Under stratified 10-fold cross-validation, `LinearSVC` achieved a 97.16% *F1-Score* (97.74% accuracy), outperforming *Random Forest* at 94.07% (95.25% accuracy), while reaching a 98.17% *F1-Score* on the 260-row tax corpus. A control experiment showed general SMS training alone reached only 42.22% accuracy on tax messages, whereas balanced curation lifted accuracy to 95.56%. Following pipeline-isolated Platt scaling, `LinearSVC` recorded 95.69% holdout accuracy (0.9957 *ROC-AUC*, 0.02542 *Brier Score*), outperforming *Random Forest* (0.04214 *Brier Score*) and leading on the 2,519-row extended corpus (96.03% versus 92.46%). Integrating the model with `.apk` and official `pajak.go.id` guards into FastAPI and a browser extension enables instant plain-language verification.

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
| Daftar Gambar | x |
| Daftar Tabel | xi |
| Bab I Pendahuluan | 1 |
| 1.1 Latar Belakang Masalah | 1 |
| 1.2 Rumusan Masalah | 2 |
| 1.3 Batasan Masalah | 2 |
| 1.4 Tujuan Penelitian | 3 |
| 1.5 Manfaat Penelitian | 4 |
| 1.6 Metode Penelitian | 4 |
| Bab II Landasan Metode | 6 |
| 2.1 Penelitian Terdahulu dan Matriks Komparasi | 6 |
| 2.2 Landasan Teori dan Metode Khusus | 7 |
| 2.2.1 Algoritma *Support Vector Machine*, *LinearSVC*, dan Kalibrasi Platt | 7 |
| 2.2.2 Algoritma *Random Forest* | 7 |
| 2.2.3 Praproses Teks Bahasa Indonesia dan Pembobotan Fitur TF-IDF | 7 |
| 2.2.4 Validasi Silang Terstratifikasi, Metrik Evaluasi, dan Kesiapterapan Teknologi | 8 |
| 2.3 Prosedur Operasional dan Bagan Alir Penelitian | 8 |
| 2.4 Waktu dan Lokasi Penelitian | 9 |
| 2.5 Alat dan Bahan Penelitian | 10 |
| 2.6 Cara Pengumpulan dan Analisis Data | 10 |
| 2.7 Definisi Operasional Variabel dan Parameter | 10 |
| Bab III Implementasi Metode Usulan | 11 |
| 3.1 Arsitektur Implementasi Metode Usulan | 11 |
| 3.2 Implementasi Kurasi Korpus dan Praproses Teks | 12 |
| 3.3 Implementasi Pelatihan Model, Penyetelan Hiperparameter, dan Kalibrasi | 13 |
| 3.4 Implementasi Purwarupa Sistem Terpadu Tingkat Kesiapan Teknologi 6 | 14 |
| 3.5 Skenario Pengujian Sistem dan Kesiapan Evaluasi | 14 |
| Bab IV Hasil dan Analisa | 16 |
| 4.1 Hasil Eksperimen Komparasi Klasifikasi dan Penyetelan Hiperparameter | 16 |
| 4.2 Analisis Kalibrasi Probabilitas dan Studi Ablatif Fitur | 18 |
| 4.3 Analisis Ketahanan Bias Kata Kunci Pajak dan Generalisasi Lintas Korpus | 19 |
| 4.4 Analisis Interpretabilitas Fitur dan Kesalahan Prediksi | 20 |
| 4.5 Hasil Pengujian Purwarupa Sistem Terpadu dan Evaluasi Kesiapterapan Teknologi | 21 |
| Bab V Kesimpulan | 24 |
| 5.1 Kesimpulan | 24 |
| 5.2 Saran | 25 |
| Daftar Pustaka | 26 |
| Lampiran | 32 |
| Lampiran 1. Matriks Penelitian Terdahulu | 32 |
| Lampiran 2. Jadwal, Alat, Bahan, dan Definisi Operasional | 33 |
| Lampiran 3. Pemetaan Modul Kode, Kontrak API, Matriks Skenario Uji, dan Rancangan Antarmuka | 35 |
| Lampiran 4. Evaluasi ROC-PR, Studi Ablatif, Bobot Fitur, Analisis Kesalahan, dan Hasil Uji Purwarupa | 38 |
| Lampiran 5. Daftar Riwayat Hidup Penulis | 41 |

---

# DAFTAR GAMBAR

| Nomor Gambar | Judul Gambar | Halaman |
| :--- | :--- | :---: |
| Gambar 1.1 | Tahapan Metode Penelitian | 5 |
| Gambar 2.1 | Bagan Alir Prosedur Eksperimen | 9 |
| Gambar 3.1 | Arsitektur Sistem Terpadu Deteksi *Phishing* WhatsApp Perpajakan | 11 |
| Gambar 4.1 | Perbandingan *Confusion Matrix* Uji *Holdout* | 18 |
| Gambar 4.2 | Evaluasi Kalibrasi Probabilitas Model | 18 |
| Gambar 4.3 | Komparasi Generalisasi Lintas Korpus dan Subset Pajak | 20 |
| Gambar 4.4 | Analisis Interpretabilitas Model Berbasis SHAP | 20 |
| Gambar 4.5 | Tangkapan Layar Antarmuka Web *Cek Pesan Pajak* dan Respons API | 22 |
| Gambar 4.6 | Tangkapan Layar Ekstensi Chrome pada Simulasi *WhatsApp Web* | 22 |
| Gambar L.1 | Rancangan Antarmuka Web *Cek Pesan Pajak* dan Ekstensi *WhatsApp Web* | 37 |
| Gambar L.2 | Evaluasi Diskriminatif Kurva ROC dan *Precision-Recall* | 38 |
| Gambar L.3 | Analisis Interpretabilitas Fitur TF-IDF Terbaik | 39 |

---

# DAFTAR TABEL

| Nomor Tabel | Judul Tabel | Halaman |
| :--- | :--- | :---: |
| Tabel 1.1 | Komposisi Korpus Dataset Penelitian | 4 |
| Tabel 3.1 | Konfigurasi Ruang Pencarian Hiperparameter dan Parameter Terpilih | 13 |
| Tabel 4.1 | Hasil Komparasi Kinerja Klasifikasi pada Berbagai Tahap Evaluasi | 16 |
| Tabel 4.2 | Komparasi Hasil Penelitian terhadap Studi Terdahulu | 23 |
| Tabel L.1 | Matriks Penelitian Terdahulu | 32 |
| Tabel L.2 | Jadwal Pelaksanaan Penelitian | 33 |
| Tabel L.3 | Spesifikasi Alat dan Bahan Penelitian | 34 |
| Tabel L.4 | Definisi Operasional Variabel dan Parameter Penelitian | 34 |
| Tabel L.5 | Pemetaan Modul Kode Sumber terhadap Tahapan Metodologi Penelitian | 35 |
| Tabel L.6 | Spesifikasi Titik Akhir Layanan Web dan REST API FastAPI (`api.py`) | 36 |
| Tabel L.7 | Matriks Skenario Pengujian Otomatis Purwarupa dan Integritas Sistem | 36 |
| Tabel L.8 | Hasil Studi Ablatif Praproses dan Representasi Fitur TF-IDF | 38 |
| Tabel L.9 | Perbandingan Fitur Teratas `LinearSVC` dan *Random Forest* | 39 |
| Tabel L.10 | Ringkasan Analisis Kesalahan Prediksi pada Himpunan Uji *Holdout* | 39 |
| Tabel L.11 | Hasil Pengujian Fungsional Otomatis dan Latensi Inferensi Purwarupa | 40 |

---

# BAB I PENDAHULUAN

## 1.1 Latar Belakang Masalah

Direktorat Jenderal Pajak (DJP) terus memperluas layanan digital melalui portal `coretaxdjp`, aplikasi *M-Pajak*, dan siaran *WhatsApp* resmi [1], [2]. Sayangnya, perluasan kanal elektronik itu ikut dimanfaatkan pelaku penipuan berbasis pesan singkat [3], [4]. Berdasarkan 68 arsip publik tahun 2024 sampai 2026 dari pengumuman DJP, media pajak, dan pemeriksa fakta, tercatat 12 modus penipuan perpajakan. Pelaku kerap menyebarkan berkas `.apk` berbahaya, tautan palsu seperti `coretax-online`, maupun tagihan fiktif [5].

Wajib pajak awam sering kesulitan membedakan siaran resmi dari penipuan karena pelaku meniru format surat dinas beserta istilah kode *billing* dan EFIN [1], [5]. Sementara itu, filter spam yang hanya bertumpu pada SMS umum mudah mengalami bias kata kunci (*keyword bias*) sehingga pengumuman sah instansi terancam terblokir. Sejumlah penelitian memang telah menguji pembelajaran mesin pada SMS memakai TF-IDF, *Bag of Words*, dan `HashingVectorizer` [6], [7], [8], [9], [10], [11], [12], [13], [14], [15], [16], [17], [18], [19], [20], [21], [22], [23]. Kendati demikian, mayoritas riset terdahulu masih menghapus tautan dan ekstensi file saat praproses teks.

Kajian empiris yang khusus menyaring *phishing* berkedok otoritas pajak di Indonesia masih berfokus pada aspek hukum tanpa sistem deteksi otomatis [3]. Untuk mengisi kekosongan itu, penelitian ini menyusun 260 pesan pajak berimbang bersama 904 SMS umum dengan penyandian khusus `token_apk` dan `token_url`. Pemilihan model terbaik ditempuh lewat perbandingan langsung `LinearSVC` dan *Random Forest*, sekaligus dilengkapi penjelas kata pemicu serta daftar putih domain resmi `pajak.go.id` [24], [25].

Pemeriksaan lewat situs web terpisah masih kurang praktis karena mengharuskan penyalinan teks secara manual. Oleh karena itu, dibangun purwarupa Tingkat Kesiapan Teknologi (TKT) Level 6 berupa REST API FastAPI, aplikasi web *Cek Pesan Pajak*, dan ekstensi peramban *WhatsApp Web* [26], [27]. Sistem menampilkan vonis risiko, alasan awam, serta langkah pengamanan langsung pada jendela percakapan.

## 1.2 Rumusan Masalah

Merujuk pada kesenjangan literatur dan persoalan verifikasi pesan perpajakan di lapangan, penelitian ini menghadapi tantangan utama dari kemiripan diksi penipuan dengan pengumuman resmi. Permasalahan tersebut kemudian dirumuskan dalam tiga pernyataan sebab-akibat sebagai koridor perancangan serta pengujian sistem berikut:

a) Peniruan gaya surat dinas dan pemakaian istilah perpajakan pada pesan *phishing* menyulitkan warga memverifikasi keaslian pesan secara manual. Kekeliruan tersebut berisiko mendorong korban memasang berkas `.apk` berbahaya yang membahayakan kredensial akun serta dana pribadi.

b) Penyaring spam konvensional yang hanya dilatih memakai korpus SMS umum mudah terkena bias bobot kata. Ketimpangan data latih ini memicu salah blokir pada pengumuman resmi DJP (*false positive*) sekaligus meloloskan pesan *phishing* baru (*false negative*).

c) `LinearSVC` memisahkan kelas pada ruang fitur berdimensi tinggi secara linear, sedangkan *Random Forest* menggabungkan banyak pohon keputusan. Keduanya perlu diuji langsung pada fitur TF-IDF unigram-bigram agar perancangan purwarupa REST API, web *Cek Pesan Pajak*, dan ekstensi *WhatsApp Web* berlandaskan bukti terukur.

## 1.3 Batasan Masalah

Ruang lingkup pengerjaan Tugas Akhir *Prototype* ini dibatasi melalui enam ketentuan teknis berikut:

a) Klasifikasi berfokus secara biner pada teks pesan instan berbahasa Indonesia tanpa analisis gambar atau audio. Kelas `1` menandai indikasi penipuan, sedangkan kelas `0` menandai pesan aman atau resmi.

b) Bahan data sepenuhnya berasal dari sumber terbuka tanpa dokumen rahasia instansi mana pun. Dataset induk berjumlah 1.164 baris gabungan dari 904 SMS umum (sesudah menyisihkan 239 promo pada rilis CSV Rahmi dan Wibisono) [6] serta 260 teks pajak dari 65 di antara 68 sumber publik 2024 sampai 2026 [2], [5].

c) Tahap praproses mencakup pengecilan huruf, penyandian pola `.apk` menjadi `token_apk`, serta konversi tautan ke `token_url`. Teks selanjutnya dibersihkan dari simbol nonalfanumerik, disaring kata hentinya, distem memakai Sastrawi, dan dipetakan ke vektor TF-IDF maksimal 3.000 fitur unigram-bigram.

d) Eksperimen hanya membandingkan `LinearSVC` dan `RandomForestClassifier` pascadeduplikasi 5 teks Sastrawi identik. Sebanyak 1.159 teks unik tersebut dibagi terstratifikasi 80:20 menjadi 927 data latih dan 232 data uji.

e) Mutu prediksi diukur memakai metrik *Confusion Matrix* meliputi *Accuracy*, *Precision*, *Recall*, dan *F1-Score*. Evaluasi juga dilengkapi validasi silang sepuluh lipatan, *ROC-AUC*, *PR-AUC*, serta kalibrasi probabilitas.

f) Luaran akhir berwujud purwarupa TKT 6 berbahasa Python meliputi layanan FastAPI, antarmuka web *Cek Pesan Pajak*, serta ekstensi *WhatsApp Web* (*Manifest V3*). Fitur penjelasan kata pemicu, pemindai `.apk`, dan verifikasi domain `pajak.go.id` ikut tertanam di dalamnya.

## 1.4 Tujuan Penelitian

Selaras dengan rumusan masalah di atas, penelitian ini menetapkan tiga tujuan terukur berikut:

a) Menyusun korpus teks perpajakan berbahasa Indonesia berimbang antara pesan *phishing* dan pengumuman resmi. Data itu diproses lewat penyandian `token_apk`, `token_url`, serta ekstraksi pembobotan TF-IDF.

b) Menguji dan membandingkan keandalan `LinearSVC` berkalibrasi *Platt scaling* melawan *Random Forest* memakai metrik klasifikasi dan kalibrasi peluang. Tahap ini turut menjalankan uji kontrol tanpa korpus pajak guna membuktikan penurunan salah blokir pesan resmi.

c) Merancang purwarupa sistem deteksi terpadu berbasis REST API FastAPI, antarmuka web *Cek Pesan Pajak*, dan ekstensi *WhatsApp Web*. Sistem memuat model terbaik beserta penjelas indikator pemicu berbahasa awam.

## 1.5 Manfaat Penelitian

Pengembangan model klasifikasi berimbang serta purwarupa deteksi pesan instan ini diharapkan memberi dampak nyata pada pengajaran komputasi, edukasi publik, dan perlindungan digital masyarakat. Secara terstruktur, kontribusi yang dituju dari penelitian ini terbagi ke dalam tiga aspek berikut:

a) Manfaat Akademik dan Universitas Siber Asia (UNSIA): Memberikan bukti empiris perbandingan kinerja `LinearSVC` dan *Random Forest* beserta mitigasi *keyword bias*. Korpus pajak terbuka dan modul purwarupa ini juga bermanfaat sebagai bahan praktikum NLP Program Studi PJJ Sistem Informasi.

b) Manfaat bagi Institusi Publik: Menyediakan pemetaan 12 modus penipuan pajak serta rancangan penyaringan berbasis data lapangan. Temuan pola leksikal penipu dapat menunjang materi edukasi perlindungan wajib pajak.

c) Manfaat bagi Masyarakat: Menghadirkan alat verifikasi praktis lewat web *Cek Pesan Pajak* dan ekstensi *WhatsApp Web*. Wajib pajak dapat membaca indikasi risiko sebelum mengeklik tautan atau memasang berkas `.apk`.

## 1.6 Metode Penelitian

Penelitian ini memadukan metode eksperimen kuantitatif dengan alur *Research and Development* (R&D) sesuai pedoman Tugas Akhir *Prototype* UNSIA [27], [28]. Pengumpulan teks mengandalkan studi dokumentasi terhadap 68 arsip publik otoritatif [29], kemudian 65 sumber unik dipilih menjadi 260 pesan pajak berimbang (130 penipuan 12 modus dan 130 siaran resmi 10 layanan) [2], [5]. Penggabungannya dengan 904 SMS umum [6] membentuk dataset induk 1.164 baris pada Tabel 1.1.

Tabel 1.1 Komposisi Korpus Dataset Penelitian

| Sumber Korpus | Asal Pengumpulan | Kategori Phishing | Kategori Aman | Jumlah Total |
| :--- | :--- | :---: | :---: | :---: |
| Kumpulan SMS Publik Indonesia | Repositori Akademik UPI (Rahmi & Wibisono) [6] | 335 | 569 | 904 |
| Kumpulan Teks Khusus Perpajakan | Kurasi 65 dari 68 sumber publik [2], [5] | 130 | 130 | 260 |
| Himpunan Data Gabungan Induk | Integrasi Korpus SMS Umum serta Teks Pajak | 465 | 699 | 1.164 |

Sumber: Olahan Data Penelitian (2026).

Seluruh teks melewati praproses Sastrawi beserta penyandian `token_apk` dan `token_url` sebelum vektorisasi TF-IDF 3.000 fitur [9], [10], [11], [13], [18], [19], [22]. Sesudah validasi silang dan kalibrasi parameter, model terbaik ditanamkan ke purwarupa TKT Level 6 [24], [26] seperti tergambar pada Gambar 1.1.

![Gambar 1.1 Tahapan Metode Penelitian.](Aset Gambar/Gambar 1.1 Tahapan Metode Penelitian.png)

Gambar 1.1 Tahapan Metode Penelitian.

Karena matriks TF-IDF berdimensi tinggi bersifat jarang (*sparse*), hipotesis kerja [30], [31] memperkirakan `LinearSVC` lebih konsisten pada validasi silang dan kalibrasi peluang daripada *Random Forest* [11], [24]. Uji empiris pada 1.159 teks unik membuktikan `LinearSVC` meraih *F1-Score* 10-Fold CV 97,16% (*Accuracy* 97,74%) melampaui *Random Forest* sebesar 94,07% (`95,25%`), dengan *Brier Score* lebih kecil (`0,02542` vs `0,04214`). Penyeimbangan korpus pajak juga mendongkrak akurasi uji khusus 45 pesan pajak dari 42,22% menjadi 95,56% (`20/21` pesan resmi DJP lolos), dan mencatat *F1-Score* 98,17% pada korpus pajak 260 baris.

# BAB II LANDASAN METODE

## 2.1 Penelitian Terdahulu dan Matriks Komparasi

Perluasan kanal digital Direktorat Jenderal Pajak lewat siaran *WhatsApp Blast* Coretax sering dicatut pelaku *smishing* untuk menyebar berkas `.apk` dan tautan palsu [1], [2], [3], [4], [5]. Di Indonesia, Rahmi dan Wibisono [6] merintis korpus SMS publik memakai *Multinomial Naïve Bayes* (*Accuracy* 94,12% dan 94,56%), sementara Theodorus dkk. [7] menguji 4.125 SMS tiga kelas (*Random Forest* 94,62% vs SVM 94,38%). Penelitian Irawan dkk. [8] serta Al Ghofany dkk. [9] memadukan *stemming* Nazief-Adriani dengan TF-IDF hingga SVM Linear meraih 99,52% pada 500 SMS privat.

Pada pembandingan lintas dataset, Astuti dkk. [10], Tampinongkol dkk. [11], Al Tawil dkk. [12], dan Ningtias dkk. [13] mengevaluasi kinerja TF-IDF. Riset tersebut mengadu SVM dan *Random Forest* melawan BERT yang jauh lebih lambat dilatih. Di ranah pesan instan lokal, Efendi dkk. [14] membangun bot WhatsApp berbasis logika *fuzzy*. Saputra dkk. [15] memakai Sastrawi pada SVM berfitur `HashingVectorizer` (`95,45%`), tetapi kehilangan keterjelasan fitur. Sembiring dkk. [16] menyandikan token uang dan URL (`Recall` SVM 98,59%) tanpa mencakup `.apk`.

Studi lain menelaah klasifikasi SMS dan surel [17], [18], [19], [20], komparasi *phishing* [21], [22], serta penipuan di media sosial X [23]. Kajian mutakhir merancang kerangka `LinearSVC` terjelaskan [24], penerapan XAI [25], dan ekstensi peramban [26]. Matriks lengkap 12 studi terdahulu termuat pada Lampiran (`Tabel L.1`). Pemetaan ini menyingkap empat celah: ketiadaan korpus pajak berimbang, terbuangnya `.apk` atau URL saat praproses, absennya uji kontrol *keyword bias*, dan minimnya ekstensi berkalibrasi Platt. Kerangka kerja ini mengacu pedoman TA *Prototype* UNSIA [27], [28], [29], [30], [31].

## 2.2 Landasan Teori dan Metode Khusus

### 2.2.1 Algoritma Support Vector Machine, LinearSVC, dan Kalibrasi Platt

*Support Vector Machine* bekerja mencari *hyperplane* berjarak *margin* terbesar di ruang fitur berdimensi tinggi [32]. Untuk matriks TF-IDF ribuan dimensi yang bersifat jarang, implementasi `LinearSVC` memakai pustaka LIBLINEAR. Pustaka tersebut mengoptimalkan fungsi objektif pada Persamaan (2.1) dengan target kelas $y_i \in \{-1, +1\}$ [33].

**Persamaan (2.1)** *LinearSVC*: min (1/2)||w||² + C ∑ᵢ max(0, 1 - yᵢ(wᵀxᵢ + b))²

Keluaran mentah *f*(*x*) = *w*ᵀ*x* + *b* masih berupa jarak pemisah sehingga belum langsung menunjukkan peluang pasti. Oleh sebab itu, regresi logistik *Platt scaling* [34] memetakan jarak tersebut ke rentang probabilitas nol sampai satu melalui Persamaan (2.2). Sementara itu, bobot *w*ⱼ tiap token memberi transparansi kontribusi kata.

**Persamaan (2.2)** *Platt Scaling*: P(y=1|f(x)) = 1 / (1 + exp(A·f(x) + B))

### 2.2.2 Algoritma Random Forest

*Random Forest* membentuk banyak pohon keputusan independen melalui mekanisme *bootstrap aggregating* (*bagging*) dan pencuplikan acak subset fitur [35]. Titik pemecah terbaik ditentukan lewat penurunan nilai impuritas Gini pada Persamaan (2.3). Selanjutnya, peluang prediksi ansambel diperoleh dari rata-rata suara seluruh *B* pohon melalui Persamaan (2.4). Pada teks pendek yang jarang fiturnya, pemecahan satu kata per simpul sering menyisakan peluang pada wilayah keraguan.

**Persamaan (2.3)** Impuritas Gini: Gini(t) = 1 - ∑ₖ p(k|t)²

**Persamaan (2.4)** *Random Forest*: P(y=1|x) = (1/B) ∑ᵦ Pᵦ(y=1|x)

### 2.2.3 Praproses Teks Bahasa Indonesia dan Pembobotan Fitur TF-IDF

Pembobotan TF-IDF menilai kepentingan kata dari kekerapan lokalnya dikalikan kelangkaan dokumen di seluruh korpus. Hasil pembobotan dinormalisasi memakai norma Euclidean L2 pada Persamaan (2.5) agar panjang pesan tidak mendistorsi skor [36]. Sebelum diekstrak menjadi fitur *unigram* dan *bigram*, huruf teks diseragamkan menjadi kecil. Pola `.apk` lalu disandikan ke `token_apk` dan URL ke `token_url`, diikuti penghapusan simbol, *stopword removal*, serta *stemming* Sastrawi pada kata lebih dari dua huruf [37].

**Persamaan (2.5)** w(t,d) = [tf(t,d)·(ln((1+N)/(1+df(t)))+1)]/||v(d)||₂

### 2.2.4 Validasi Silang Terstratifikasi, Metrik Evaluasi, dan Kesiapterapan Teknologi

Validasi silang terstratifikasi 10 lipatan mempertahankan proporsi kelas pada tiap partisi [38]. Mutu prediksi dihitung dari matriks konfusi (*TP*, *TN*, *FP*, *FN*) ke dalam *Accuracy*, *Precision*, *Recall*, serta *F1-Score* via Scikit-learn pada Persamaan (2.6) dan (2.7) [39], [40]. Kelayakan purwarupa mengacu TKT Level 6 Permenristekdikti Nomor 42 Tahun 2016 [41]. Adapun kalibrasi probabilitas dinilai lewat *ROC-AUC*, *PR-AUC*, *Brier Score*, dan *Log Loss* dengan optimasi Newton pada Persamaan (2.8) [42].

**Persamaan (2.6)** Acc = (TP + TN) / (TP + TN + FP + FN) ; Prec = TP / (TP + FP)

**Persamaan (2.7)** Rec = TP / (TP + FN) ; F1 = 2·(Prec·Rec) / (Prec + Rec)

**Persamaan (2.8)** BS = (1/N) ∑ᵢ (pᵢ - yᵢ)² ; LL = -(1/N) ∑ᵢ [yᵢlog(pᵢ) + (1-yᵢ)log(1-pᵢ)]

## 2.3 Prosedur Operasional dan Bagan Alir Penelitian

Prosedur operasional memadukan eksperimen kuantitatif dan R&D dari hulu data hingga uji antarmuka pengguna [27], [28]. Setiap eksperimen mengunci pengacak `random_state=42` guna menjaga keterulangan seluruh metrik [40]. Pemodelan hanya memproses vektor TF-IDF teks tanpa menguraikan gambar maupun file biner `.apk`. Alur kerjanya terbagi menjadi enam tahap berikut:

a) Kurasi 260 pesan pajak berimbang dari 65 sumber publik dipadukan bersama 904 SMS umum menjadi korpus induk 1.164 baris dan korpus perluasan 2.521 baris terverifikasi SHA-256 [2], [5], [6].

b) Praproses teks menyeragamkan huruf kecil, menyandikan `token_apk` dan `token_url`, menghapus simbol nonalfanumerik, menyaring kata henti, lalu menstem dengan Sastrawi [37].

c) Deduplikasi 5 teks Sastrawi identik menyisakan 1.159 baris unik. Data dibagi terstratifikasi 80:20 (`927` latih dan `232` uji) sebelum vektorisasi TF-IDF 3.000 fitur [36].

d) Penalaan parameter menguji 36 kandidat pada 10-Fold CV terisolasi. Setelah itu, `LinearSVC` terbaik dikalibrasi memakai `Pipeline` *Platt scaling* lima lipatan [33], [38], [42].

e) Evaluasi lanjutan menjalankan 6 skenario ablatif dan uji kontrol tanpa korpus pajak vs korpus seimbang (`n = 45`). Pengujian berlanjut ke 1.360 pesan eksternal unik, korpus 2.519 baris, dan SHAP [24], [25], [39].

f) Pengemasan model `.joblib` ke dalam FastAPI, aplikasi web *Cek Pesan Pajak*, dan ekstensi *WhatsApp Web* memenuhi target TKT Level 6 [26], [41].

Keterkaitan keenam tahapan prosedur operasional eksperimen tersebut diperlihatkan pada Gambar 2.1.

![Gambar 2.1 Bagan Alir Prosedur Eksperimen.](Aset Gambar/Gambar 2.1 Bagan Alir Prosedur Eksperimen.png)

Gambar 2.1 Bagan Alir Prosedur Eksperimen.

## 2.4 Waktu dan Lokasi Penelitian

Penelitian berlangsung empat bulan mulai Agustus hingga November 2026 mengikuti kalender akademik PJJ Sistem Informasi UNSIA [27]. Eksekusi komputasi dilakukan secara luring di Jakarta Selatan. Seluruh kegiatan memakai data terbuka tanpa menyentuh sistem internal otoritas pajak [2], [5]. Jadwal rinci enam tahapan kegiatan penelitian tercantum pada Lampiran (`Tabel L.2`).

## 2.5 Alat dan Bahan Penelitian

Eksperimen dijalankan pada laptop berprosesor Intel Core i5-12450H, RAM 16 GB, dan Windows 11 Pro 64-bit dalam waktu 189,36 detik. Perangkat lunak memakai Python 3.11.9 bersama Scikit-learn 1.9.1 [40], Sastrawi 1.0.1 [37], SHAP, Joblib 1.6.0, FastAPI, dan Pytest 9.2.0. Spesifikasi lengkap perangkat keras, perangkat lunak, dan berkas korpus termuat pada Lampiran (`Tabel L.3`).

## 2.6 Cara Pengumpulan dan Analisis Data

Pengumpulan bahan perpajakan menerapkan dokumentasi terhadap 68 arsip publik otoritatif [29]. Seleksi menyisihkan 3 sumber berulang serta 239 SMS promosi Rahmi dan Wibisono. Hasil seleksi membentuk 130 pesan *phishing* dari 12 modus dan 130 siaran resmi DJP pada korpus induk 1.164 baris [2], [5], [6]. Selama 10-Fold CV, vektorizer TF-IDF selalu dibangun terpisah pada tiap lipatan latih untuk mencegah kebocoran data [30], [31], [38].

Untuk menguji Rumusan Masalah (b) secara terkontrol, model turut dilatih hanya memakai 712 SMS umum partisi latih lalu diuji ke 45 pesan pajak *holdout*. Hasil kontrol itu kemudian disandingkan dengan model berimbang 1.159 baris. Pengujian lintas korpus juga dijalankan pada 1.360 pesan unik Theodorus dkk. [7] dan Saragih guna mengukur daya generalisasi eksternal.

## 2.7 Definisi Operasional Variabel dan Parameter

Variabel bebas berupa teks pesan berbahasa Indonesia yang dipetakan menjadi vektor TF-IDF `(1, 2)` maksimal 3.000 fitur. Adapun variabel terikat berupa label biner kelas `1` (*phishing*) dan kelas `0` (resmi/normal) [29], [30]. Pengukuran parameter mencakup regulasi `C` `LinearSVC`, jumlah pohon *Random Forest*, kalibrasi Platt [33], [35], [42], serta indikator kelayakan TKT 6 [39], [41]. Matriks definisi operasional lengkap tercantum pada Lampiran (`Tabel L.4`).

# BAB III IMPLEMENTASI METODE USULAN

## 3.1 Arsitektur Implementasi Metode Usulan

Implementasi metode usulan mewujudkan enam tahap prosedur operasional Bab II menjadi sistem perangkat lunak Python 3.11.9 [40]. Arsitekturnya memisahkan alur pelatihan luring (*offline*) dan layanan daring (*online*). Alur luring mengolah teks menjadi vektor TF-IDF 3.000 dimensi lalu melatih `LinearSVC` serta `RandomForestClassifier` [6], [36], [37]. Sementara itu, alur daring memuat bundel terkalibrasi ke FastAPI untuk melayani web dan ekstensi peramban [26], seperti pada Gambar 3.1.

![Arsitektur Sistem Terpadu Deteksi Phishing WhatsApp Perpajakan](Aset Gambar/Gambar 3.1 Arsitektur Sistem Terpadu.png)

Gambar 3.1 Arsitektur Sistem Terpadu Deteksi *Phishing* WhatsApp Perpajakan.

Logika klasifikasi, deteksi heuristik keamanan, penerjemahan alasan awam, serta sorotan bahaya dipusatkan di `06 Prototipe Aplikasi/inference.py`. Pemusatan aturan ini menjamin antarmuka web *Cek Pesan Pajak*, titik akhir REST API, dan ekstensi *WhatsApp Web* selalu menghasilkan vonis serta sorotan kata pemicu yang konsisten. Daftar lengkap pemetaan sembilan modul kode sumber terhadap tahapan riset tercantum pada Lampiran (`Tabel L.5`).

## 3.2 Implementasi Kurasi Korpus dan Praproses Teks

Tahap data dijalankan melalui `src/korpus_pajak.py` dan `src/kurasi_dataset.py`. Sebanyak 68 arsip publik disaring memakai `strip_djp_boilerplate` [2], [5] menjadi 65 sumber unik berisi 260 pesan pajak seimbang (130 *phishing* 12 modus dan 130 siaran resmi). Penggabungannya dengan 904 SMS umum [6] sesudah menyisihkan 239 iklan promo membentuk dataset induk 1.164 baris berverifikasi 10 *hash* SHA-256. Korpus induk ikut dipadukan dengan data Theodorus dkk. [7] serta Saragih dari 4.255 mentah menjadi 2.521 baris pasca-`clean_text` (membuang 1.734 duplikat).

Fungsi `clean_text` di `src/eksperimen_baseline.py` menyiapkan daftar kata dasar Sastrawi ke dalam himpunan (`set`) berkapasitas `lru_cache` 20.000 kata. Struktur himpunan ini mempercepat pencarian morfologi menjadi waktu konstan $O(1)$ saat melakukan pemrosesan massal ratusan pesan [37]. Setiap teks masukan melewati enam langkah praproses berurutan berikut:

a) Pengecilan seluruh huruf via metode `lower()` agar variasi kapitalisasi seragam.

b) Konversi pola `.apk` (`r"\.apk\b"`) menjadi `token_apk` sebelum pemindaian URL agar nama berkas tidak dianggap tautan web.

c) Pengubahan tautan `http`, `https`, `www`, `bit.ly`, atau akhiran domain `.go.id`, `.co.id`, dan `.xyz` menjadi `token_url`.

d) Penghapusan simbol nonalfanumerik selain spasi dan garis bawah memakai pola `r"[^a-z0-9\s_]"`.

e) Penyaringan *stopword* Sastrawi dengan tetap melestarikan `token_apk` dan `token_url`.

f) Pengembalian kata alfabetis lebih dari dua huruf (`tok.isalpha() and len(tok) > 2`) ke bentuk dasar lewat Sastrawi 1.0.1 [37].

Guna mendukung uji ablatif pada `src/eksperimen_komparasi.py`, dibangun pula dua varian teks pembanding di luar `teks_sastrawi`. Kolom `clean_text` menyimpan teks tanpa penyaringan kata henti dan *stemming* (`2_Tanpa_Sastrawi`), sedangkan kolom `teks_tanpa_token_entitas` menghapus pola URL dan berkas `.apk` (`1_Tanpa_Token_Entitas`).

## 3.3 Implementasi Pelatihan Model, Penyetelan Hiperparameter, dan Kalibrasi

Skrip `src/eksperimen_komparasi.py` mengunci nilai `RANDOM_STATE=42` bagi seluruh tahapan eksperimen [40]. Pada korpus induk 1.164 baris, penyaringan duplikat `teks_sastrawi` menyisihkan 5 baris sehingga tersisa 1.159 teks unik (`697` aman dan `462` penipuan). Data lalu dibagi terstratifikasi 80:20 menjadi 927 data latih dan 232 data uji. Fungsi `_precompute_tfidf_folds` membangun objek `TfidfVectorizer(ngram_range=(1, 2), max_features=3000)` secara terpisah di tiap lipatan *Stratified 10-Fold CV* agar kosakata validasi tetap terisolasi [36], [38].

Melalui fungsi `_run_grid_over_folds`, pencarian *grid* mengevaluasi seluruh 36 kandidat kombinasi parameter (12 kandidat `LinearSVC` dan 24 kandidat *Random Forest*) berdasarkan nilai rata-rata *F1-Score* sepuluh lipatan. Rincian ruang pencarian serta parameter optimal terpilih dari evaluasi tersebut disajikan pada Tabel 3.1.

Tabel 3.1 Konfigurasi Ruang Pencarian Hiperparameter dan Parameter Terpilih

| Algoritma Klasifikasi | Ruang Pencarian Parameter (`_run_grid_over_folds`) | Konfigurasi Terpilih |
| :--- | :--- | :--- |
| `LinearSVC` | `C`: `0.1, 0.25, 0.5, 1.0, 2.0, 5.0`; `class_weight`: `None, balanced`; `max_iter=5000` | `C=2.0`, `class_weight=None` |
| `RandomForestClassifier` | `n_estimators`: `100, 200, 300`; `max_depth`: `None, 30`; `min_samples_split`: `2, 5`; `class_weight`: `None, balanced` | `n_estimators=100`, `max_depth=None`, `min_samples_split=2`, `class_weight=None` |

Sumber: Implementasi Penalaan Parameter pada `src/eksperimen_komparasi.py` (2026).

Keluaran mentah `LinearSVC` masih berbentuk jarak *hyperplane* sehingga perlu dikalibrasi menjadi peluang [33], [34], [42]. Fungsi `_make_calibrated_svm_pipeline` membungkus vektorizer dan `LinearSVC` dalam `Pipeline` sebelum dikalibrasi lewat `CalibratedClassifierCV(method="sigmoid", cv=5)`. Berikutnya, `_run_stage4_domain_and_cross_corpus` menguji skenario kontrol 712 SMS umum vs korpus seimbang (`n = 45`) dan CV 260 teks pajak (`Stage 4A`). Tahap akhir mengevaluasi 1.360 teks eksternal unik (`Stage 4B`) serta korpus diperluas 2.519 baris pasca-Sastrawi (`Stage 4C`) [7], mengekspor `model_phishing_pajak.joblib`, dan menghitung SHAP (`n = 232`) [24], [25].

## 3.4 Implementasi Purwarupa Sistem Terpadu Tingkat Kesiapan Teknologi 6

Berkas `inference.py` memuat bundel `model_phishing_pajak.joblib` memakai `lru_cache(maxsize=1)` serta menormalisasi masukan memakai `clean_text` yang sama dengan pelatihan [41]. Di samping menghitung peluang `svm_prob`, modul menerapkan dua lapisan heuristik perpajakan. Pola `APK_PATTERN` (`r"\b[a-z0-9_.-]+\.apk\b"`) memindai berkas `.apk` dan langsung menaikkan status ke `TINGGI`. Adapun `URL_PATTERN` mensyaratkan TLD alfabetis supaya angka jam (`17.00`) dan nominal (`Rp1.500.000`) aman, sementara `is_official_djp_domain` hanya meloloskan host `pajak.go.id` atau `.pajak.go.id`. Hasil perkalian fitur TF-IDF dan `coef_` diterjemahkan oleh `_extract_top_triggers` menjadi alasan awam [24].

Layanan REST API di `api.py` dibangun di atas FastAPI Uvicorn beserta pengaturan CORS `allow_private_network=True`, *security headers*, dan pembatas laju permintaan (spesifikasi pada `Tabel L.6`). Antarmuka web *Cek Pesan Pajak* di `web/` memiliki tiga tab (**Cek Pesan**, **Web Resmi & Ciri Scam**, **Darurat .apk**), kotak **Cek Chat WhatsApp**, tombol **Cek Sekarang**, tiga prasetel (**File .apk Palsu**, **Link Pajak Palsu**, **Chat Resmi DJP**), serta info akademik di *footer*. Ekstensi *Manifest V3* di `extension/` [26] memindai gelembung obrolan minimal 8 karakter dan kartu `.apk` di *WhatsApp Web*, sesuai Lampiran `Gambar L.1`.

## 3.5 Skenario Pengujian Sistem dan Kesiapan Evaluasi

Integritas sistem diuji otomatis memakai Pytest 9.2.0 terhadap 23 skenario uji pada empat berkas di `tests/`. Modul `test_integritas_dataset.py` (6 kasus) dan suite eksperimen (7 kasus) mengunci keutuhan 10 *hash* SHA-256, deduplikasi Sastrawi, isolasi Platt, arah SHAP, `.joblib`, serta keunggulan akurasi atas kontrol SMS umum. Pada sisi layanan aplikasi, `tests/test_prototipe_api.py` mengeksekusi 10 skenario *black-box* (`UJI-01` s.d. `UJI-09` pada Lampiran `Tabel L.7`) mencakup kesiapan layanan, deteksi `.apk`/domain tiruan, pengecoh `pajak.go.id.evil.com`, penjagaan jam dan nominal, tolak spasi kosong (`422`), `POST /predict/batch` (3 masukan campuran berstatus `total=3` dengan spasi menghasilkan `"error"` serta tolak teks >5.000 karakter `422`), halaman web, dan *security headers*.

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

# BAB V KESIMPULAN

## 5.1 Kesimpulan

Berdasarkan rangkaian kurasi data, pemodelan komparatif, pengujian ketahanan bias, dan validasi purwarupa sistem terpadu, diperoleh tiga kesimpulan yang menjawab tujuan penelitian sebagai berikut:

a) Penggabungan 260 pesan pajak berimbang dari 65 arsip publik bersama 904 SMS umum menghasilkan korpus induk 1.164 baris. Penyaringan duplikat Sastrawi lalu menyisakan 1.159 teks unik. Pelestarian `token_apk` serta `token_url` dalam ekstraksi TF-IDF `(1, 2)` 3.000 fitur terbukti esensial. Penghapusan token entitas memangkas *F1-Score* 10-Fold CV `LinearSVC` sebesar 1,35 poin (`97,16%` ke `95,81%`), sedangkan pembatasan unigram menurunkannya 1,22 poin (`95,94%`).

b) Model `LinearSVC` Platt (`C=2,0`) mengungguli *Random Forest* (`n_estimators=100`) pada 10-Fold CV (*F1-Score* `97,16% ± 2,41%` vs `94,07% ± 2,92%`) dan *ROC-AUC* (`0,9957` vs `0,9936`). Model ini mencatat *Brier Score* `0,02542` dan *Log Loss* `0,09186` (turun `39,68%` dan `42,12%`). Pelatihannya berjalan 106,6 kali lebih cepat serta unggul pada korpus 2.519 baris (`96,03%` vs `92,46%`). Pada uji kontrol 45 pesan pajak, model SMS umum (`712` latih) hanya meraih akurasi `42,22%` untuk `LinearSVC` (`11/21` pesan DJP terblokir) dan `33,33%` bagi *Random Forest*. Sebaliknya, penyeimbangan korpus mengangkat keduanya ke akurasi `95,56%` (`20/21` pesan resmi lolos) dengan *F1-Score* CV 260 pajak `98,17%`.

c) Purwarupa terpadu menyatukan `LinearSVC` Platt bersama penjaga `.apk` dan daftar putih `pajak.go.id` ke dalam FastAPI, web *Cek Pesan Pajak*, serta ekstensi *WhatsApp Web* (*Manifest V3*). Integrasi tersebut menutup kelemahan TF-IDF murni pada kasus `idx=960` dan `idx=1082`. Seluruh 23 pengujian Pytest lulus dalam 21,51 detik dengan latensi `POST /predict` rata-rata `34,991` ms (*P95* `48,082` ms) sehingga memenuhi kriteria TKT Level 6.

## 5.2 Saran

Untuk pengembangan riset dan adopsi sistem lebih lanjut, diajukan tiga rekomendasi terarah berikut:

a) Korpus latih perlu diperbarui secara berkala memakai pesan layanan Coretax DJP mutakhir agar penurunan presisi lintas periode (`Stage 4B`: `40,99%`, `FP = 416`) dapat ditekan. Langkah ini sebaiknya dipadukan dengan normalisasi entitas *Named Entity Recognition* (NER) guna menghilangkan artefak korpus lama seperti `nama1` dan `2016`.

b) Fitur deteksi multi-sinyal di luar batas teks saat ini layak dieksplorasi pada riset berikutnya. Peneliti selanjutnya dapat menambahkan ekstraksi *Optical Character Recognition* (OCR) atas tangkapan layar surat palsu dan pemeriksaan reputasi domain WHOIS. Evaluasi model bahasa terkuantisasi seperti IndoBERT juga relevan untuk mendeteksi penipuan transfer super singkat tanpa tautan (`idx=314` dan `idx=102`).

c) Evaluasi *User Acceptance Testing* (UAT) bersama wajib pajak secara terbatas disarankan untuk menguji keterbacaan alasan awam di lapangan. Pemeliharaan berkala selektor DOM pada `content.js` ekstensi *Manifest V3* juga dibutuhkan mengikuti pembaruan antarmuka *WhatsApp Web*.

# DAFTAR PUSTAKA

[1] Waluyo, *Perpajakan Indonesia*, ed. ke-13. Jakarta: Salemba Empat, 2020.

[2] Direktorat Jenderal Pajak, “Penyebarluasan Informasi Mengenai Coretax (Pengumuman Nomor PENG-32/PJ.09/2024),” *Portal Resmi Direktorat Jenderal Pajak Kementerian Keuangan Republik Indonesia*, Nov. 2024. [Online]. Available: https://pajak.go.id/id/pengumuman/penyebarluasan-informasi-mengenai-coretax

[3] N. B. Prakoso, H. Ayu, and H. Zakaria, “Misuse of taxpayer data for phising scams,” *Journal of International Islamic Law, Human Rights, and Public Policy*, vol. 4, no. 3, pp. 1560-1569, Jul. 2026, doi: 10.5281/zenodo.21853029.

[4] R. Alabdan, “Phishing attacks survey: Types, vectors, and technical approaches,” *Future Internet*, vol. 12, no. 10, p. 168, Oct. 2020, doi: 10.3390/fi12100168.

[5] Direktorat Jenderal Pajak, “Waspada penipuan yang mengatasnamakan Direktorat Jenderal Pajak (Pengumuman Nomor PENG-31/PJ.09/2024 s.d. PENG-18/PJ.09/2026),” *Portal Resmi Direktorat Jenderal Pajak Kementerian Keuangan Republik Indonesia*, 2026. [Online]. Available: https://www.pajak.go.id/id/pengumuman/waspada-penipuan-yang-mengatasnamakan-direktorat-jenderal-pajak

[6] F. Rahmi and Y. Wibisono, “Aplikasi SMS spam filtering pada Android menggunakan algoritma Naïve Bayes,” Skripsi, Dept. Pendidikan Ilmu Komputer, Universitas Pendidikan Indonesia, Bandung, 2016. [Online]. Available: https://repository.upi.edu/26936/

[7] A. Theodorus, T. K. Prasetyo, R. Hartono, and D. Suhartono, “Short Message Service (SMS) spam filtering using machine learning in Bahasa Indonesia,” in *Proc. 3rd East Indonesia Conf. Comput. Inf. Technol. (EIConCIT)*, Apr. 2021, pp. 199-203, doi: 10.1109/EIConCIT50028.2021.9431859.

[8] D. Irawan, Hamidah, E. B. Perkasa, Yurindra, D. Wahyuningsih, and E. Helmud, “Perbandingan klassifikasi SMS berbasis Support Vector Machine, Naive Bayes Classifier, Random Forest dan Bagging Classifier,” *Jurnal Sisfokom (Sistem Informasi dan Komputer)*, vol. 10, no. 3, pp. 432-437, Dec. 2021, doi: 10.32736/sisfokom.v10i3.1302.

[9] M. S. Al Ghofany, R. Dwiyansaputra, F. Bimantoro, and Khairunnas, “Indonesian SMS spam detection using TF-RF feature weighting method and Support Vector Machine classifier,” in *Proc. First Mandalika Int. Multi-Conf. Sci. Eng. (MIMSE-I-C)*, 2022, pp. 117-129, doi: 10.2991/978-94-6463-084-8_12.

[10] E. Z. Astuti, C. A. Sari, E. H. Rachmawanto, and R. R. Ali, “Comparative study of machine learning algorithms for performing ham or spam classification in SMS,” *Scientific Journal of Informatics*, vol. 11, no. 1, pp. 177-186, Feb. 2024, doi: 10.15294/sji.v11i1.47364.

[11] F. F. Tampinongkol, A. R. Kamila, A. C. Wardhana, A. W. C. Kusuma, and D. Revaldo, “Implementation of Random Forest classification and Support Vector Machine algorithms for phishing link detection,” *Journal of Informatics Information System Software Engineering and Applications (INISTA)*, vol. 7, no. 1, pp. 127-137, Nov. 2024, doi: 10.20895/inista.v7i1.1588.

[12] A. Al Tawil, L. H. Almazaydeh, D. Qawasmeh, B. Qawasmeh, M. Alshinwan, and K. Elleithy, “Comparative analysis of machine learning algorithms for email phishing detection using TF-IDF, Word2Vec, and BERT,” *Computers, Materials & Continua*, vol. 81, no. 2, pp. 3395-3412, Nov. 2024, doi: 10.32604/cmc.2024.057279.

[13] A. A. Ningtias, N. Anwar, A. Ichwani, and R. T. Iswahyudi, “Komparasi kinerja Support Vector Machine dan Random Forest untuk deteksi spam email berbasis TF-IDF teks,” *IKRA-ITH Informatika: Jurnal Komputer dan Informatika*, vol. 10, no. 3, pp. 45-51, Nov. 2026.

[14] F. M. Efendi, A. K. Adisusilo, and S. Budiprayitno, “Pengembangan sistem deteksi phishing pada WhatsApp berbasis AI dengan integrasi bahasa lokal Surabaya,” *Melek IT Information Technology Journal*, vol. 11, no. 1, pp. 101-112, Jun. 2025, doi: 10.30742/melekitjournal.v11i1.417.

[15] R. B. Saputra, M. Azwar, L. Widyawati, Husain, and K. A. Latif, “Implementasi algoritma SVM pada bot WhatsApp untuk deteksi pesan spam,” *Jurnal Manajemen Informatika dan Sistem Informasi*, vol. 9, no. 1, pp. 39-51, Jan. 2026, doi: 10.36595/misi.v9i1.1803.

[16] M. A. Sembiring, M. F. L. Sibuea, and Anjani, “Optimasi model klasifikasi pesan penipuan digital berbahasa Indonesia menggunakan XGBoost dengan Bayesian Optimization dan SMOTE,” *Journal of Science and Social Research*, vol. 9, no. 3, pp. 5329-5336, Jun. 2026, doi: 10.54314/jssr.v9i3.7212.

[17] A. Setiyono and H. F. Pardede, “Klasifikasi SMS spam menggunakan Support Vector Machine,” *Jurnal Pilar Nusa Mandiri*, vol. 15, no. 2, pp. 275-280, Sep. 2019, doi: 10.33480/pilar.v15i2.693.

[18] N. J. Saputra, “Analysis of SMS spam detection using TF-IDF: A study on SMS Spam Collection dataset,” *Jurnal Sosial Teknologi*, vol. 4, no. 4, pp. 213-217, Apr. 2024, doi: 10.59188/jurnalsostech.v4i4.1214.

[19] H. Ahammad, M. Samsuzzaman, M. H. Rashid, and M. A. Masud, “Comparative analysis of machine learning algorithms for spam SMS classification using TF-IDF vectorization,” in *Proc. IEEE Int. Conf. Future Mach. Learn. Data Sci. (FMLDS)*, Nov. 2025, pp. 736-741, doi: 10.1109/fmlds67896.2025.00123.

[20] S. K. Birthriya, P. Ahlawat, and A. K. Jain, “Machine learning-based smishing detection using fuzzy logic and TF-IDF feature engineering,” *Franklin Open*, vol. 14, p. 100506, Mar. 2026, doi: 10.1016/j.fraope.2026.100506.

[21] R. Fauzan, A. V. Vitianingsih, D. Cahyono, A. L. Maukar, and Y. A. B. Suprio, “Penerapan algoritma klasifikasi pada machine learning untuk deteksi phishing,” *MALCOM: Indonesian Journal of Machine Learning and Computer Science*, vol. 5, no. 2, pp. 531-540, Mar. 2025, doi: 10.57152/malcom.v5i2.1968.

[22] I. P. Sari, O. K. Sulaiman, D. Apdilah, and P. Simanjuntak, “Analisis komparatif Support Vector Machine dan Random Forest untuk deteksi email phishing,” *Applied Information Technology and Computer Science (AICOMS)*, vol. 4, no. 2, pp. 18-27, Nov. 2025, doi: 10.58466/aicoms.v4i2.1806.

[23] I. K. Izzah, I. Riadi, and A. Fadlil, “Analisis kinerja machine learning untuk deteksi konten penipuan berbahasa Indonesia di Twitter,” *Rabit: Jurnal Teknologi dan Sistem Informasi Univrab*, vol. 11, no. 1, pp. 725-742, Jan. 2026, doi: 10.36341/rabit.v11i1.7124.

[24] P. Mishra and A. Yadav, “An explainable and reproducible lightweight machine learning framework for SMS spam detection using TF-IDF and Linear Support Vector Classification,” *International Journal of Advanced Science and Computer Applications*, vol. 5, no. 2, Sep. 2026, doi: 10.47679/ijasca.v5i2.269.

[25] J. Ismail, R. A. Nasution, and M. N. Gea, “Deteksi phishing URL menggunakan XGBoost dengan Explainable AI pada Web Page Phishing Detection dataset,” *IDEALIS: InDonEsiA journaL Information System*, vol. 9, no. 2, pp. 268-277, Jul. 2026, doi: 10.36080/idealis.v9i2.3810.

[26] Suwarno, V. Capricornness, and Y. Christian, “Implementasi machine learning berbasis browser extension untuk deteksi URL phishing menggunakan Logistic Regression classification,” *Komputa: Jurnal Ilmiah Komputer dan Informatika*, vol. 15, no. 1, May 2026, doi: 10.34010/komputa.v15i1.18882.

[27] C. R. Hassolthine, U. Darusalam, and M. Ikhwani, *Pedoman Teknis Penulisan Tugas Akhir Mahasiswa Universitas Siber Asia (SK Rektor Nomor 01 Tahun 2024)*. Jakarta: Universitas Siber Asia, 2024.

[28] Sugiyono, *Metode Penelitian Kuantitatif, Kualitatif, dan R&D*, ed. ke-2. Bandung: Alfabeta, 2023.

[29] M. Darwin, M. R. Mamondol, S. A. Sormin, and Y. Nurhayati, *Metode Penelitian Pendekatan Kuantitatif*. Bandung: Media Sains Indonesia, 2021.

[30] Sugiyono, *Statistika untuk Penelitian*. Bandung: Alfabeta, 2019.

[31] L. P. Sinambela, *Metodologi Penelitian Kuantitatif: Teoretik dan Praktik*. Depok: Rajawali Pers, 2021.

[32] C. Cortes and V. Vapnik, “Support-vector networks,” *Machine Learning*, vol. 20, no. 3, pp. 273-297, Sep. 1995, doi: 10.1007/BF00994018.

[33] R.-E. Fan, K.-W. Chang, C.-J. Hsieh, X.-R. Wang, and C.-J. Lin, “LIBLINEAR: A library for large linear classification,” *Journal of Machine Learning Research*, vol. 9, pp. 1871-1874, Aug. 2008. [Online]. Available: https://jmlr.org/papers/v9/fan08a.html

[34] J. C. Platt, “Probabilistic outputs for support vector machines and comparisons to regularized likelihood methods,” in *Advances in Large Margin Classifiers*, A. J. Smola, P. Bartlett, B. Schölkopf, and D. Schuurmans, Eds. Cambridge, MA, USA: MIT Press, 2000, pp. 61-74.

[35] L. Breiman, “Random forests,” *Machine Learning*, vol. 45, no. 1, pp. 5-32, Oct. 2001, doi: 10.1023/A:1010933404324.

[36] G. Salton and C. Buckley, “Term-weighting approaches in automatic text retrieval,” *Information Processing & Management*, vol. 24, no. 5, pp. 513-523, 1988, doi: 10.1016/0306-4573(88)90021-0.

[37] M. Adriani, J. Asian, B. A. A. Nazief, S. M. M. Tahaghoghi, and H. E. Williams, “Stemming Indonesian: A confix-stripping approach,” *ACM Transactions on Asian Language Information Processing*, vol. 6, no. 4, pp. 1-33, Dec. 2007, doi: 10.1145/1316457.1316459.

[38] R. Kohavi, “A study of cross-validation and bootstrap for accuracy estimation and model selection,” in *Proc. 14th Int. Joint Conf. Artif. Intell. (IJCAI)*, Montreal, QC, Canada, Aug. 1995, vol. 2, pp. 1137-1143. [Online]. Available: https://www.ijcai.org/Proceedings/95-2/Papers/016.pdf

[39] M. Sokolova and G. Lapalme, “A systematic analysis of performance measures for classification tasks,” *Information Processing & Management*, vol. 45, no. 4, pp. 427-437, Jul. 2009, doi: 10.1016/j.ipm.2009.03.002.

[40] F. Pedregosa *et al.*, “Scikit-learn: Machine Learning in Python,” *Journal of Machine Learning Research*, vol. 12, pp. 2825-2830, Oct. 2011. [Online]. Available: https://jmlr.org/papers/v12/pedregosa11a.html

[41] Menteri Riset, Teknologi, dan Pendidikan Tinggi Republik Indonesia, *Peraturan Menteri Riset, Teknologi, dan Pendidikan Tinggi Nomor 42 Tahun 2016 tentang Pengukuran dan Penetapan Tingkat Kesiapterapan Teknologi* (Berita Negara Republik Indonesia Tahun 2016 Nomor 1010). Jakarta: Kementerian Ristekdikti, Jul. 2016.

[42] H.-T. Lin, C.-J. Lin, and R. C. Weng, “A note on Platt's probabilistic outputs for support vector machines,” *Machine Learning*, vol. 68, no. 3, pp. 267-276, Aug. 2007, doi: 10.1007/s10994-007-5018-6.

---

# LAMPIRAN

## Lampiran 1. Matriks Penelitian Terdahulu

Tabel L.1 Matriks Penelitian Terdahulu

| Peneliti dan Tahun                                   | Objek dan Fitur                                                                          | Algoritma dan Kinerja                                                                                 | Keunggulan serta Kelemahan                                                           |
| :--------------------------------------------------- | :--------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------- |
| Prakoso dkk. (2026) [3]                              | Kajian yuridis-empiris penipuan data wajib pajak Coretax, NPWP, dan PKP di Indonesia     | Analisis kualitatif normatif tanpa eksperimen model klasifikasi ataupun metrik uji kuantitatif        | Memetakan eksploitasi data pajak, tetapi belum membangun detektor teks otomatis      |
| Rahmi dan Wibisono (2016) [6]                        | Korpus SMS Indonesia (1.140 naskah; 1.143 CSV) memakai *Term Frequency* (10-CV)          | *Multinomial Naïve Bayes* meraih *Accuracy* 94,12% (*spam* vs normal) dan 94,56% (*fraud* vs *promo*) | Merintis korpus publik Indonesia, namun menghapus URL/`.apk` dan tanpa domain pajak  |
| Theodorus dkk. (2021) [7]                            | Korpus 4.125 SMS Indonesia tiga kelas memakai *Bag of Words* 1.500 kata                  | *Random Forest* (*Acc* 94,62%), *LogReg* (94,57%), XGBoost (94,52%), SVM (94,38%)                     | Memperluas korpus pesan Indonesia tanpa fokus *phishing* perpajakan                  |
| Al Ghofany dkk. (2022) [9]                           | 500 SMS privat Indonesia memakai *stemming* Nazief-Adriani serta TF-IDF dan TF-RF        | SVM Sigmoid (*Acc* 99,60%) dan SVM Linear (99,52%) pada 10-*fold* CV                                  | Membuktikan efektivitas *stemming* Indonesia, tetapi belum membandingkan RF          |
| Astuti dkk. (2024) [10]                              | 5.574 SMS Inggris memakai pembobotan TF-IDF (pembagian 70:30)                            | SVC Sigmoid (*Acc* 97,93%; *F1* 95%) unggul atas *Random Forest* (*F1* 94%)                           | Menyajikan komparasi metrik lengkap, tetapi tanpa praproses Indonesia                |
| Tampinongkol dkk. (2024) [11]                        | 59.899 URL *phishing* dengan 9 fitur leksikal tautan (pembagian 80:20)                   | *Random Forest* (*Acc* 84,95%) vs SVM default (77,43%)                                                | Membandingkan RF dan SVM pada tautan, bukan isi rekayasa sosial                      |
| Al Tawil dkk. (2024) [12]                            | 18.650 surel *phishing* Inggris membandingkan TF-IDF, *Word2Vec*, dan BERT               | RF TF-IDF (*F1* 0,98; latih 40,39 dtk) vs BERT (*F1* 0,99; latih 1.012,66 dtk)                        | Mengukur efisiensi waktu TF-IDF, namun tidak menguji SVM                             |
| Ningtias dkk. (2026) [13]                            | 5.572 pesan SMS Inggris memakai TF-IDF dan optimasi `GridSearchCV`                       | Linear SVM (*Acc* 98,39%; *F1* 0,9371) vs *Random Forest* (95,96%; *F1* 0,8421)                       | Membuktikan keunggulan Linear SVM pascapenalaan, tetapi menghapus URL                |
| Efendi dkk. (2025) [14]                              | Bot WhatsApp bahasa Indonesia, Jawa, & Surabaya berbasis 3 fitur heuristik (uji 5 pesan) | Logika *fuzzy* Mamdani dan TSK (keyakinan 0,55 s.d. 0,83)                                             | Mendukung dialek daerah WhatsApp, namun tanpa pembelajaran terawasi terukur          |
| Saputra dkk. (2026) [15]                             | 1.320 pesan WA dan SMS Indonesia memakai Sastrawi dan `HashingVectorizer` 5.000 fitur    | Linear SVM (*Acc* 95,45%; *Macro F1* 0,95 pada split 80:20)                                           | Menerapkan Sastrawi pada WA, tetapi *hashing* menghilangkan fitur XAI                |
| Sembiring dkk. (2026) [16]                           | 2.320 pesan penipuan Indonesia dengan token entitas dan TF-IDF kata/karakter             | Linear SVM (*Recall* 0,9859) dan XGBoost (*Accuracy* 96,34%)                                          | Melestarikan URL/nominal, namun belum menyandikan `.apk` dan ekstensi WA             |
| Mishra & Yadav (2026) [24]; Suwarno dkk. (2026) [26] | SMS TF-IDF [24] serta ekstensi URL *phishing* [26]                                       | `LinearSVC` terjelaskan [24]; Ekstensi *LogReg* [26]                                                  | Menunjukkan `LinearSVC` *explainable* dan ekstensi peramban, belum terpadu WA pajak  |
| Penelitian Ini (2026)                                | Dataset induk 1.164 (1.159 unik) & korpus diperluas 2.519 baris unik                     | `LinearSVC` Platt vs *Random Forest* pada TF-IDF `(1, 2)` + `token_apk`/`token_url`                   | Mengatasi *keyword bias* (kontrol 42,22%->95,56%), XAI, dan purwarupa ekstensi TKT 6 |

Sumber: Hasil Kajian Pustaka (2026).

## Lampiran 2. Jadwal, Alat, Bahan, dan Definisi Operasional

Tabel L.2 Jadwal Pelaksanaan Penelitian

| Tahap Kegiatan Penelitian                                   | Agustus 2026 | September 2026 | Oktober 2026 | November 2026 |
| :---------------------------------------------------------- | :----------: | :------------: | :----------: | :-----------: |
| Studi literatur, cek kebaruan, dan perumusan proposal       |   Berjalan   |    Selesai     |              |               |
| Pengumpulan sumber DJP serta kurasi dataset terverifikasi   |              |    Berjalan    |   Selesai    |               |
| Implementasi skrip praproses, TF-IDF, dan eksperimen model  |              |                |   Berjalan   |    Selesai    |
| Penalaan *GridSearchCV*, kalibrasi Platt, dan uji ablatif   |              |                |   Berjalan   |    Selesai    |
| Perancangan arsitektur purwarupa TKT 6 dan pengujian sistem |              |                |              |   Berjalan    |
| Penyusunan laporan lengkap Bab I hingga Bab V dan Lampiran  |              |                |   Berjalan   |    Selesai    |

Sumber: Rencana Kerja Penelitian (2026).

Tabel L.3 Spesifikasi Alat dan Bahan Penelitian

| Kategori Komponen               | Nama Komponen / Berkas                            | Spesifikasi dan Peran dalam Penelitian                                                                                         |
| :------------------------------ | :------------------------------------------------ | :----------------------------------------------------------------------------------------------------------------------------- |
| Perangkat Keras                 | Komputer Jinjing Komputasi                        | Prosesor Intel Core i5-12450H, RAM 16 GB, Windows 11 Pro 64-bit                                                                |
| Perangkat Lunak Inti            | Python, Scikit-learn, Sastrawi                    | Python 3.11.9, Scikit-learn 1.9.1 (`LinearSVC`, `RandomForestClassifier`, `CalibratedClassifierCV`), Sastrawi 1.0.1 [37], [40] |
| Perangkat Lunak Pendukung       | Pandas, NumPy, Matplotlib, SHAP, Joblib, Pytest   | Pandas 3.1.1, NumPy 2.4.6, Matplotlib 3.11.2, SHAP, Joblib 1.6.0, Pytest 9.2.0                                                 |
| Rancangan Purwarupa             | FastAPI, Web Kustom, Ekstensi Manifest V3         | REST API (`api.py`), Web *Cek Pesan Pajak* (`web/`), dan Ekstensi *WhatsApp Web* TKT 6 [26], [41]                              |
| Bahan Korpus SMS Publik         | `Rahmi 2016 Korpus SMS Spam Utama v1.csv`         | 904 SMS Indonesia (335 penipuan, 569 normal); 239 promo disisihkan [6]                                                         |
| Bahan Korpus Pajak              | `Dataset Pajak Terkurasi 260 Baris.csv`           | 260 teks pajak seimbang (130 *phishing*, 130 resmi) dari 65/68 sumber publik [2], [5]                                          |
| Bahan Gabungan Induk            | `Dataset Gabungan Utama Biner 1164 Baris.csv`     | Gabungan 904 SMS + 260 teks pajak (1.159 baris unik pasca-Sastrawi), verifikasi SHA-256                                        |
| Bahan Diperluas & Uji Eksternal | `Dataset Gabungan Diperluas Biner 2521 Baris.csv` | 2.521 baris (2.519 unik), plus 1.360 eksternal unik Theodorus [7] & Saragih                                                    |

Sumber: Dokumentasi Lingkungan Penelitian (2026).

Tabel L.4 Definisi Operasional Variabel dan Parameter Penelitian

| Nama Variabel / Parameter                    | Jenis / Kategori                | Definisi Operasional dan Nilai dalam Eksperimen                                                                       |
| :------------------------------------------- | :------------------------------ | :-------------------------------------------------------------------------------------------------------------------- |
| Teks Pesan Instan (`Teks` / `teks_sastrawi`) | Variabel Bebas (Masukan)        | String pesan bahasa Indonesia dipraproses menjadi huruf kecil, `token_apk`, `token_url`, dan kata dasar Sastrawi [37] |
| Label Klasifikasi (`label`)                  | Variabel Terikat (Target Biner) | Kategori biner `1` untuk indikasi *phishing* dan `0` untuk pesan aman/resmi                                           |
| Parameter Ekstraksi TF-IDF                   | Parameter Representasi Fitur    | Pembobotan TF-IDF `ngram_range` `(1, 2)` dengan `max_features` `3.000` (ablatif `1.500` dan `5.000`) [36]             |
| Parameter `LinearSVC`                        | *Hyperparameter* SVM Linear     | Pencarian `C` `{0,1; 0,25; 0,5; 1,0; 2,0; 5,0}`, `class_weight` `{None, "balanced"}`, `max_iter=5000` [33], [40]      |
| Parameter *Random Forest*                    | *Hyperparameter* Ansambel       | Pencarian `n_estimators` `{100, 200, 300}`, `max_depth` `{None, 30}`, `min_samples_split` `{2, 5}` [35]               |
| Parameter Kalibrasi *Platt*                  | Parameter Kalibrasi             | `CalibratedClassifierCV` dengan `method="sigmoid"`, `cv=5` berbasis `Pipeline` [34], [42]                             |
| Metrik Evaluasi                              | Variabel Kinerja Utama          | *Accuracy*, *Precision*, *Recall*, *F1-Score*, *ROC-AUC*, *PR-AUC*, *Brier Score*, dan *Log Loss* [38], [39]          |
| Indikator Kesiapan Teknologi                 | Variabel Kelayakan              | Capaian TKT 6 lewat `.joblib` pada REST API, web *Cek Pesan Pajak*, dan ekstensi *WhatsApp Web* [41]                  |

Sumber: Sintesis Metodologi Penelitian (2026).

## Lampiran 3. Pemetaan Modul Kode, Kontrak API, Matriks Skenario Uji, dan Rancangan Antarmuka

Tabel L.5 Pemetaan Modul Kode Sumber terhadap Tahapan Metodologi Penelitian

| Berkas / Direktori Modul                  | Tahapan Metodologi            | Peran Teknis dalam Sistem                                                                 |
| :---------------------------------------- | :---------------------------- | :---------------------------------------------------------------------------------------- |
| `src/korpus_pajak.py`                     | Kurasi Sumber Perpajakan      | Menyimpan 68 sumber publik, 31 indikator DJP, dan 260 teks pajak                          |
| `src/kurasi_dataset.py`                   | Konstruksi & Provenans        | Membangun dataset induk 1.164, korpus diperluas 2.521, dan katalog SHA-256                |
| `src/eksperimen_baseline.py`              | Praproses & Baseline          | Menyediakan `clean_text` Sastrawi dan uji *baseline* 80:20                                |
| `src/eksperimen_komparasi.py`             | Penalaan, Kalibrasi, Evaluasi | Menjalankan 10-Fold CV, `GridSearchCV`, Platt, ablatif, kontrol bias, SHAP, dan `.joblib` |
| `06 Prototipe Aplikasi/inference.py`      | Mesin Inferensi Terpadu       | Memuat `.joblib`, menjalankan heuristik `.apk`/`pajak.go.id`, dan menyusun alasan awam    |
| `06 Prototipe Aplikasi/api.py` & peluncur | Layanan Backend & Web         | Menyajikan web (`/`) serta *endpoint* `/health`, `/api/*`, `/predict`, `/predict/batch`   |
| `06 Prototipe Aplikasi/web/`              | Antarmuka Web Pengguna        | Halaman web responsif (`index.html`, `styles.css`, `app.js`) dan modal evaluasi TA        |
| `06 Prototipe Aplikasi/extension/`        | Ekstensi *WhatsApp Web*       | Ekstensi *Manifest V3* pada `web.whatsapp.com` untuk lencana risiko langsung              |
| `tests/`                                  | Verifikasi Otomatis Sistem    | Menjalankan 23 pengujian `pytest` atas data, model, API, dan keamanan                     |

Sumber: Dokumentasi Rekayasa Perangkat Lunak Penelitian (2026).

Tabel L.6 Spesifikasi Titik Akhir Layanan Web dan REST API FastAPI (`api.py`)

| Metode & Jalur                               | Skema Masukan                                   | Struktur Keluaran Utama                                             | Peran dalam Arsitektur                       |
| :------------------------------------------- | :---------------------------------------------- | :------------------------------------------------------------------ | :------------------------------------------- |
| `GET /`                                      | Tanpa badan permintaan                          | Berkas HTML web *Cek Pesan Pajak*                                   | Menyajikan aplikasi web utama                |
| `GET /health`                                | Tanpa badan permintaan                          | Status `ok`, `models_loaded`, dan `metadata`                        | Pemeriksaan kesiapan layanan web/ekstensi    |
| `GET /api/presets` & `/api/academic-summary` | Tanpa badan permintaan                          | Prasetel uji, metadata model, dan baris `tabel_komparasi_utama.csv` | Mengisi tombol contoh cepat dan modal sidang |
| `POST /predict`                              | JSON `text` (1-5.000 karakter) & `top_k` (1-20) | Label, `risk_level`, `plain_reasons`, `highlights`, `trigger_words` | Inferensi tunggal web dan ekstensi           |
| `POST /predict/batch`                        | JSON daftar `texts` (1-200 pesan) & `top_k`     | Total baris dan hasil per indeks                                    | Pemrosesan pesan massal                      |

Sumber: Implementasi Layanan API pada `06 Prototipe Aplikasi/api.py` (2026).

Tabel L.7 Matriks Skenario Pengujian Otomatis Purwarupa dan Integritas Sistem

| Kode Uji | Berkas / Subjek Pengujian                          | Skenario Masukan & Kondisi Uji                                       | Keluaran yang Diharapkan                                         |
| :------- | :------------------------------------------------- | :------------------------------------------------------------------- | :--------------------------------------------------------------- |
| `UJI-01` | `test_prototipe_api.py` (`GET /health`)            | Permintaan kesiapan peladen API                                      | HTTP 200 dengan `LinearSVC+Platt` aktif                          |
| `UJI-02` | `test_prototipe_api.py` (`POST /predict`)          | Pesan berkas `Coretax_DJP_Update.apk`                                | Label `1`, `has_apk=True`, risiko `TINGGI`                       |
| `UJI-03` | `test_prototipe_api.py` (`POST /predict`)          | Tautan palsu `pajak-djp-verifikasi.xyz`                              | Label `1`, `suspicious_domains` tanpa jam `17.00`                |
| `UJI-04` | `test_prototipe_api.py` (`POST /predict`)          | Pengumuman resmi `djponline.pajak.go.id`                             | Label `0`, risiko `RENDAH`, `official_domains` terisi            |
| `UJI-05` | `test_prototipe_api.py` (`is_official_djp_domain`) | Uji pengecoh `pajak.go.id.evil.com` vs sah                           | Mengembalikan `False` tiruan, `True` domain sah                  |
| `UJI-06` | `test_prototipe_api.py` (`POST /predict`)          | Teks spasi kosong                                                    | Ditolak dengan status HTTP 422                                   |
| `UJI-07` | `test_prototipe_api.py` (`POST /predict/batch`)    | Tiga masukan campuran (`.apk`, spasi, resmi) + teks `5.001` karakter | HTTP 200 `total=3` (`results[1]` error) & HTTP 422 teks berlebih |
| `UJI-08` | `test_prototipe_api.py` (penjaga angka)            | Pesan resmi memuat jam `16.00` dan `Rp1.500.000`                     | `suspicious_domains` kosong, status `RENDAH`                     |
| `UJI-09` | `test_prototipe_api.py` (`GET /` & `/api/*`)       | Permintaan halaman web, simulasi WA, prasetel, & ringkasan TA        | HTTP 200 beserta header keamanan aktif                           |
| `UJI-10` | `test_integritas_dataset.py` & eksperimen          | Validasi 5 korpus, SHA-256, deduplikasi, Platt, & kontrol            | Seluruh 13 pengujian data dan model lulus                        |

Sumber: Implementasi Pengujian Otomatis `pytest` pada Direktori `tests/` (2026).

![Rancangan Antarmuka Web Cek Pesan Pajak dan Ekstensi WhatsApp Web](Aset Gambar/Gambar L.1 Rancangan Antarmuka Purwarupa dan Ekstensi.png)

Gambar L.1 Rancangan Antarmuka Web *Cek Pesan Pajak* dan Ekstensi *WhatsApp Web*.

## Lampiran 4. Evaluasi ROC-PR, Studi Ablatif, Bobot Fitur, Analisis Kesalahan, dan Hasil Uji Purwarupa

![Gambar L.2 Evaluasi Diskriminatif Kurva ROC dan Precision-Recall.](Aset Gambar/Gambar L.2 Evaluasi Diskriminatif Kurva ROC dan Precision-Recall.png)

Gambar L.2 Evaluasi Diskriminatif Kurva ROC dan *Precision-Recall*.

Tabel L.8 Hasil Studi Ablatif Praproses dan Representasi Fitur TF-IDF

| Skenario Konfigurasi       | Model            | CV10 *Accuracy* | CV10 *F1-Score* | *Holdout Accuracy* | *Holdout F1-Score* |
| :------------------------- | :--------------- | :-------------: | :-------------: | :----------------: | :----------------: |
| `1_Tanpa_Token_Entitas`    | `LinearSVC` / RF | 96,66% / 93,96% | 95,81% / 92,42% |  97,84% / 95,26%   |  97,27% / 93,99%   |
| `2_Tanpa_Sastrawi`         | `LinearSVC` / RF | 97,74% / 95,69% | 97,16% / 94,55% |  96,12% / 96,55%   |  95,08% / 95,60%   |
| `3_Unigram_Saja`           | `LinearSVC` / RF | 96,77% / 95,68% | 95,94% / 94,59% |  96,12% / 96,12%   |  95,08% / 95,03%   |
| `4_Utama_MaxFeatures_1500` | `LinearSVC` / RF | 97,30% / 95,58% | 96,61% / 94,52% |  96,12% / 96,55%   |  95,03% / 95,56%   |
| `5_Konfigurasi_Utama_3000` | `LinearSVC` / RF | 97,74% / 95,25% | 97,16% / 94,07% |  96,12% / 96,55%   |  94,97% / 95,56%   |
| `6_Utama_MaxFeatures_5000` | `LinearSVC` / RF | 97,41% / 94,72% | 96,79% / 93,34% |  96,98% / 96,55%   |  96,13% / 95,60%   |

Sumber: Hasil Studi Ablatif `05 Hasil Evaluasi/studi_ablatif_fitur.csv` (2026).

![Gambar L.3 Analisis Interpretabilitas Fitur TF-IDF Terbaik.](Aset Gambar/Gambar L.3 Analisis Interpretabilitas Fitur TF-IDF Terbaik.png)

Gambar L.3 Analisis Interpretabilitas Fitur TF-IDF Terbaik.

Tabel L.9 Perbandingan Fitur Teratas `LinearSVC` dan *Random Forest*

| Peringkat | Fitur Positif (`LinearSVC`) | Bobot *w* (+) | Fitur Penahan Resmi/Normal (`LinearSVC`) | Bobot *w* (-) | Fitur Terpenting *Random Forest* | Skor Gini |
| :-------: | :-------------------------- | :-----------: | :--------------------------------------- | :-----------: | :------------------------------- | :-------: |
|     1     | `no`                        |    +2,2405    | `nama1`                                  |    -1,2720    | `no`                             |  0,0424   |
|     2     | `sms`                       |    +1,6940    | `aku`                                    |    -1,2206    | `hub`                            |  0,0349   |
|     3     | `rekening`                  |    +1,5083    | `resmi`                                  |    -1,0706    | `info`                           |  0,0319   |
|     4     | `info`                      |    +1,4054    | `maupun`                                 |    -0,9633    | `sms`                            |  0,0227   |
|     5     | `segera`                    |    +1,3778    | `terimakasih`                            |    -0,9134    | `token_url`                      |  0,0226   |
|     6     | `pin`                       |    +1,3729    | `yg`                                     |    -0,8942    | `hadiah`                         |  0,0200   |
|     7     | `token_apk`                 |    +1,3582    | `nya`                                    |    -0,8738    | `pin`                            |  0,0175   |
|     8     | `token_url`                 |    +1,3550    | `pernah`                                 |    -0,8417    | `rekening`                       |  0,0174   |

Sumber: Ekstraksi Bobot Model `05 Hasil Evaluasi/fitur_teratas_svm_vs_rf.csv` (2026).

Tabel L.10 Ringkasan Analisis Kesalahan Prediksi pada Himpunan Uji *Holdout*

| Indeks | Sumber dan Kategori              | Aktual | Prob. SVM | Prob. RF | Lokasi Galat              | Ringkasan Konten dan Penyebab Leksikal                                    |
| :----: | :------------------------------- | :----: | :-------: | :------: | :------------------------ | :------------------------------------------------------------------------ |
|  118   | Rahmi (Penipuan)                 |   1    |   0,566   |  0,420   | RF Saja (FN)              | Modus jual rumah mengajak hubungi nomor seluler tanpa kata `hadiah`       |
|   50   | Rahmi (Penipuan)                 |   1    |   0,218   |  0,750   | SVM Baseline & Platt (FN) | Tawaran gratis kuota operator dengan banyak angka satuan                  |
|  491   | Rahmi (Normal)                   |   0    |   0,543   |  0,170   | SVM Baseline & Platt (FP) | Teks amat pendek "Dimulai dari angka 0" tanpa konteks normal              |
|  898   | Rahmi (Normal)                   |   0    |   0,608   |  0,640   | Keduanya (FP)             | Pertanyaan singkat "No bri atas nama kamu mana" bermuatan kata `no`       |
|  960   | Pajak (`Phishing_APK_MPajak`)    |   1    |   0,424   |  0,730   | SVM Baseline & Platt (FN) | Gaya surat DJP mengirim `MPajak_Aktivasi_KSWP.apk` tanpa kata spam umum   |
|  293   | Rahmi (Penipuan)                 |   1    |   0,347   |  0,250   | Keduanya (FN)             | Notifikasi isi ulang pulsa palsu mirip struk transaksi resmi              |
|  1003  | Pajak (`Phishing_Link_NIK_NPWP`) |   1    |   0,787   |  0,340   | RF Saja (FN)              | Tautan palsu `form-wajibpajak-djp.com` lolos di RF tapi tertangkap SVM    |
|   52   | Rahmi (Penipuan)                 |   1    |   0,819   |  0,350   | RF Saja (FN)              | Iming-iming bonus internet 5MB bergaya informal                           |
|  228   | Rahmi (Penipuan)                 |   1    |   0,494   |  0,610   | SVM Baseline & Platt (FN) | Undian *event* bergaya percakapan santai mendekati ambang 0,5             |
|  314   | Rahmi (Penipuan)                 |   1    |   0,033   |  0,230   | Keduanya (FN)             | Instruksi singkat transfer rekening Mandiri tanpa tautan maupun ancaman   |
|  102   | Rahmi (Penipuan)                 |   1    |   0,392   |  0,470   | Keduanya (FN)             | Permintaan transfer Mandiri pendek menyerupai pesan keluarga              |
|  1082  | Pajak (Pemadanan NIK Resmi)      |   0    |   0,551   |  0,600   | Keduanya (FP)             | Imbauan resmi ke `www.pajak.go.id` terseret bobot `token_url` dan `login` |
|  165   | Rahmi (Penipuan)                 |   1    |   0,493   |  0,550   | SVM Baseline & Platt (FN) | Tagihan jatuh tempo mengarahkan ke nomor ponsel (`p = 0,493`)             |

Sumber: Analisis Kesalahan `05 Hasil Evaluasi/analisis_kesalahan_prediksi.csv` (2026).

Tabel L.11 Hasil Pengujian Fungsional Otomatis dan Latensi Inferensi Purwarupa

| Kode / Metrik | Subjek dan Kondisi Uji                                           | Jumlah Uji / Sampel |             Hasil / Waktu Terukur             |       Status       |
| :------------ | :--------------------------------------------------------------- | :-----------------: | :-------------------------------------------: | :----------------: |
| `UJI-01`      | `GET /health` kesiapan FastAPI & model                           |          1          |         HTTP 200 (`LinearSVC+Platt`)          |   Lulus (220 ms)   |
| `UJI-02`      | `POST /predict` berkas `Coretax_DJP_Update.apk`                  |          1          |      Label `1`, `has_apk=True`, `TINGGI`      |   Lulus (230 ms)   |
| `UJI-03`      | `POST /predict` domain `pajak-djp-verifikasi.xyz`                |          1          |        Label `1`, tanpa angka `17.00`         |   Lulus (40 ms)    |
| `UJI-04`      | `POST /predict` pengumuman `djponline.pajak.go.id`               |          1          |     Label `0`, `official_domains` terisi      |   Lulus (40 ms)    |
| `UJI-05`      | `is_official_djp_domain` atas `pajak.go.id.evil.com`             |          1          |             `False` untuk tiruan              |   Lulus (<1 ms)    |
| `UJI-06`      | `POST /predict` masukan spasi kosong                             |          1          |            Ditolak status HTTP 422            |   Lulus (20 ms)    |
| `UJI-07`      | `POST /predict/batch` 3 masukan campuran & teks >5.000 karakter  |          1          | HTTP 200 `total=3` (`results[1]` error) & 422 |   Lulus (90 ms)    |
| `UJI-08`      | Guard pukul `16.00` dan nominal `Rp1.500.000`                    |          1          |     `suspicious_domains` kosong, `RENDAH`     |   Lulus (50 ms)    |
| `UJI-09`      | `GET /`, `/simulasi-wa`, `/api/presets`, `/api/academic-summary` |          1          |       HTTP 200 beserta header keamanan        |   Lulus (750 ms)   |
| `UJI-10`      | Suite integritas 5 korpus, SHA-256, Platt, dan `.joblib`         |         13          |          Seluruh 13 pengujian lulus           |  Lulus (2.100 ms)  |
| `LAT-01`      | Latensi lokal `inference.py::predict_message` (*Mean* / *P95*)   |         232         |      20,746 ms/pesan (*P95* = 27,447 ms)      | Memenuhi (<100 ms) |
| `LAT-02`      | Latensi REST API `FastAPI POST /predict` (*Mean* / *P95*)        |         232         |      34,991 ms/pesan (*P95* = 48,082 ms)      | Memenuhi (<100 ms) |
| `LAT-03`      | Latensi massal `FastAPI POST /predict/batch` (50 pesan)          |         50          |     1.315,652 ms total (26,313 ms/pesan)      | Memenuhi (<100 ms) |

Sumber: Eksekusi `src/benchmark_purwarupa.py` dan `05 Hasil Evaluasi/tabel_pengujian_purwarupa.csv` (2026).

## Lampiran 5. Daftar Riwayat Hidup Penulis

| Atribut Biodata             | Keterangan Mahasiswa                                                                                                                                  |
| :-------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------- |
| Nama Lengkap                | Wan Mirza Dhani                                                                                                                                       |
| Nomor Induk Mahasiswa (NIM) | 240101020194                                                                                                                                          |
| Program Studi               | PJJ Sistem Informasi                                                                                                                                  |
| Fakultas / Universitas      | Universitas Siber Asia (UNSIA)                                                                                                                        |
| Tempat, Tanggal Lahir       | Medan, 22 Maret 1996                                                                                                                                  |
| Domisili                    | Medan, Sumatera Utara                                                                                                                                 |
| Surel Akademik              | wm.dhani@gmail.com                                                                                                                                    |
| Riwayat Pendidikan          | SD Wahidin, SMP Wahidin, SMA Shafiyyatul Amaliyyah, D1 Perpajakan STAN, D3 Perpajakan Universitas Terbuka, S1 Sistem Informasi Universitas Siber Asia |
| Bidang Minat                | Rekayasa Perangkat Lunak, Keamanan Informasi, dan *Natural Language Processing*                                                                       |
