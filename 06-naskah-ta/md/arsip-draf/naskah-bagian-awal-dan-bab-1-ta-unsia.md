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
