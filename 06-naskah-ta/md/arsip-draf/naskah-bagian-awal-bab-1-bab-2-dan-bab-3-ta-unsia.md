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

---

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

---

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
