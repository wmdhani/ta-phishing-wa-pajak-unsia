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
