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
| Dosen Pembimbing I | Novi Dian Nathasia, S.Kom., MMSI | .......................... |
| Dosen Pembimbing II | (..........................................................) | .......................... |
| Ketua Program Studi PJJ Informatika | Syahid Abdullah, S.Si, M.Kom | .......................... |
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

# BAB I PENDAHULUAN

## 1.1 Latar Belakang Masalah

Transformasi digital pada administrasi perpajakan di Indonesia telah mendorong Direktorat Jenderal Pajak (DJP) untuk memperluas pemanfaatan saluran komunikasi elektronik [1]. Inovasi layanan itu mencakup pembaruan sistem inti administrasi perpajakan (*Coretax Administration System*) pada laman `coretaxdjp.pajak.go.id` dan aplikasi bergerak *M-Pajak*. Pemerintah juga menggencarkan pemadanan Nomor Induk Kependudukan (NIK) sebagai Nomor Pokok Wajib Pajak (NPWP) serta pengiriman informasi melalui *WhatsApp Blast* resmi [2]. Saluran pesan instan tersebut mempercepat penyampaian pengingat Surat Pemberitahuan (SPT) Tahunan kepada masyarakat. Namun, celah kerawanan baru ikut terbuka.

Kepercayaan masyarakat terhadap saluran komunikasi instansi pemerintah itu dimanfaatkan oleh pelaku kejahatan siber melalui serangan rekayasa sosial (*social engineering*) pada WhatsApp [3], [4]. Kompilasi terhadap 68 dokumen pengumuman resmi DJP (`PENG-31/PJ.09/2024` hingga `PENG-50/PJ.09/2025`) dan laporan kasus Kantor Pelayanan Pajak (KPP) mengungkap dua belas kategori modus penipuan perpajakan [5]. Pelaku mengirimkan berkas berbahaya berformat *Android Package Kit* (`.apk`) berkedok aplikasi *Coretax* atau *M-Pajak* kepada calon korban. Modus lainnya menggunakan tautan situs tiruan `coretax-online.com` dan `djp.linepajak-go.com` maupun tagihan pajak palsu berformat PDF. Tujuannya adalah memicu kepanikan calon korban.

Wajib pajak awam maupun staf administrasi perusahaan sering kesulitan ketika harus membedakan pesan *WhatsApp Blast* resmi DJP dari pesan penipuan tersebut [1], [5]. Hal ini terjadi karena pelaku meniru format surat dinas yang mencantumkan nomor peraturan perpajakan secara meyakinkan. Pesan palsu itu juga memuat istilah administrasi resmi seperti kode *billing* dan *Electronic Filing Identification Number* (EFIN). Apabila sistem deteksi hanya dilatih memakai korpus spam umum tanpa penyeimbangan teks resmi perpajakan, model akan mengalami bias kata kunci (*keyword bias*). Akibatnya, pesan resmi ikut terdeteksi sebagai penipuan.

Sejumlah penelitian terdahulu telah menguji algoritma pembelajaran mesin untuk penyaringan pesan spam berbahasa Indonesia. Studi komparatif pada korpus pesan singkat (SMS) umum membuktikan bahwa *Support Vector Machine* (SVM) dan *Random Forest* menghasilkan akurasi tinggi saat dipadukan dengan pembobotan *Term Frequency-Inverse Document Frequency* (TF-IDF) maupun *Term Frequency-Relevance Frequency* (TF-RF) [6], [7], [8], [9]. Penelitian lain membahas deteksi tautan *phishing* berbasis fitur *Uniform Resource Locator* (URL) [10] dan klasifikasi *email phishing* berbahasa Inggris [11]. Kajian pada WhatsApp pun sudah mulai diterapkan untuk deteksi *phishing* berbahasa lokal Surabaya [12] serta spam bot umum [13], [14]. Objek kajiannya masih bersifat umum.

Meskipun metode klasifikasi teks telah berkembang, kajian khusus mengenai penipuan beratasnamakan otoritas perpajakan masih sangat terbatas. Studi sebelumnya tentang penyalahgunaan data wajib pajak baru meninjau aspek hukum tanpa membangun sistem deteksi otomatis [3]. Celah penelitian (*research gap*) ini menunjukkan belum adanya komparasi *Support Vector Machine* dan *Random Forest* pada teks *phishing* perpajakan di WhatsApp. Kebaruan ilmiah (*novelty*) penelitian ini hadir melalui penyusunan 260 pesan pajak seimbang yang dipadukan dengan 904 pesan umum. Praproses teks juga dilengkapi tokenisasi pola `.apk` (`token_apk`) dan tautan (`token_url`).

Luaran (*outcome*) penelitian ini diwujudkan menjadi suatu purwarupa (*prototype*) aplikasi web interaktif berbasis bahasa pemrograman Python dan *framework* Streamlit [15], [16]. Aplikasi tersebut mengintegrasikan model klasifikasi terbaik untuk mencapai Tingkat Kesiapan Teknologi (TKT) level 6 melalui demonstrasi sistem pada lingkungan kasus yang relevan. Pengguna dapat langsung menempelkan teks pesan WhatsApp yang mencurigakan pada antarmuka aplikasi untuk memperoleh status klasifikasi beserta skor kemungkinannya. Pada tahap pengembangan selanjutnya (*future prospect development*), model ini dapat dijadikan layanan *Application Programming Interface* (API). Sistem tersebut mendukung pelindungan wajib pajak.

## 1.2 Rumusan Masalah

Berdasarkan uraian latar belakang masalah dan hasil identifikasi terhadap pola kasus penipuan perpajakan di masyarakat, rumusan masalah penelitian ini disusun dalam bentuk hubungan sebab-akibat. Pernyataan tersebut mengungkapkan kelemahan cara kerja mekanisme verifikasi manual serta keterbatasan penyaringan spam umum saat ini. Adapun tiga rumusan masalah utama yang dikaji dalam penelitian ini diuraikan sebagai berikut:

a) Kemiripan gaya bahasa kedinasan dan pemakaian istilah resmi perpajakan pada pesan penipuan (*phishing*) WhatsApp menyulitkan verifikasi manual oleh wajib pajak. Kondisi tersebut meningkatkan risiko pencurian data kredensial maupun kerugian finansial akibat pemasangan berkas `.apk` berbahaya.

b) Ketergantungan model penyaringan spam konvensional pada korpus pesan singkat umum tanpa penyeimbangan teks resmi perpajakan menyebabkan timbulnya bias kata kunci (*keyword bias*). Kelemahan ini mengakibatkan pengumuman resmi DJP berpotensi salah diklasifikasikan sebagai penipuan (*false positive*) atau pesan rekayasa sosial baru lolos dari deteksi (*false negative*).

c) Perbedaan cara kerja pemisahan ruang fitur berdimensi tinggi pada *Support Vector Machine* dan penggabungan pohon keputusan pada *Random Forest* menuntut pengujian komparatif secara empiris pada fitur TF-IDF *n-gram*. Tanpa pengujian tersebut, belum tersedia dasar terukur untuk memilih model paling optimal pada purwarupa aplikasi deteksi mandiri.

## 1.3 Batasan Masalah

Agar pembahasan dalam penelitian ini tetap terarah dan fokus pada pokok persoalan yang dikaji, diperlukan pembatasan ruang lingkup secara tegas. Batasan tersebut mengatur objek teks, sumber korpus data, metode praproses, algoritma yang diuji, hingga bentuk luaran aplikasi. Enam batasan masalah yang ditetapkan pada penelitian Tugas Akhir *Prototype* ini adalah sebagai berikut:

a) Objek penelitian dibatasi pada analisis klasifikasi biner terhadap teks pesan singkat berbahasa Indonesia. Kelas pertama adalah pesan penipuan atau rekayasa sosial (*phishing/fraud* berlabel `1`), sedangkan kelas kedua adalah pesan aman atau layanan resmi perpajakan (berlabel `0`).

b) Sumber data penelitian menggunakan korpus publik terbuka tanpa memakai data rahasia internal wajib pajak. Dataset gabungan utama berjumlah 1.164 baris yang terdiri atas 904 baris korpus dasar SMS berbahasa Indonesia [6] dan 260 baris korpus spesifik perpajakan terkurasi seimbang dari 68 publikasi resmi periode 2024 sampai 2026 [2], [5].

c) Tahapan praproses teks (*text preprocessing*) meliputi pembersihan karakter nonalfanumerik, penyeragaman huruf kecil (*case folding*), serta pengubahan pola berkas `.apk` menjadi `token_apk` dan tautan menjadi `token_url`. Proses tersebut dilanjutkan dengan penghapusan kata henti (*stopword removal*), *stemming* Sastrawi, dan pembobotan TF-IDF *n-gram* $(1, 2)$ maksimal 3.000 fitur.

d) Algoritma klasifikasi pembelajaran mesin yang dibandingkan dalam eksperimen ini dibatasi pada metode *Support Vector Machine* (*LinearSVC*) dan *Random Forest Classifier*. Pembagian himpunan data latih terhadap data uji dilakukan secara terstratifikasi (*stratified train-test split*) dengan proporsi 80:20, yaitu 931 data latih dan 233 data uji.

e) Evaluasi kinerja model diukur memakai matriks evaluasi *Confusion Matrix* yang mencakup nilai *Accuracy*, *Precision*, *Recall*, dan *F1-Score*. Analisis kesalahan difokuskan pada kemampuan kedua algoritma dalam menekan jumlah *False Negative* maupun *False Positive* pada pesan perpajakan.

f) Luaran (*outcome*) penelitian berupa purwarupa (*prototype*) aplikasi web interaktif berbasis bahasa pemrograman Python dengan *framework* Streamlit pada Tingkat Kesiapan Teknologi (TKT) level 6. Aplikasi ini menerima masukan teks pesan WhatsApp dari pengguna dan menampilkan hasil klasifikasi beserta indikator risikonya.

## 1.4 Tujuan Penelitian

Sejalan dengan rumusan dan batasan masalah yang telah ditetapkan sebelumnya, penelitian ini dirancang untuk mencapai peningkatan akurasi deteksi sekaligus menghasilkan purwarupa sistem yang terukur. Setiap capaian dirumuskan memakai kata kerja operasional yang dapat diuji secara empiris pada tahap eksperimen. Adapun tiga tujuan utama yang hendak dicapai dalam penelitian ini adalah sebagai berikut:

a) Menyusun korpus teks berbahasa Indonesia bertema perpajakan yang seimbang antara kelas penipuan dan kelas layanan resmi. Tahap ini juga menerapkan konsep praproses teks serta pembobotan fitur *Term Frequency-Inverse Document Frequency* (TF-IDF) untuk mengenali karakteristik pesan *phishing* WhatsApp mengatasnamakan otoritas perpajakan.

b) Menguji, menghitung, dan menganalisis perbandingan kinerja algoritma *Support Vector Machine* terhadap *Random Forest* berdasarkan metrik *Accuracy*, *Precision*, *Recall*, serta *F1-Score*. Pengujian ini bertujuan membuktikan ketangguhan model dalam mendeteksi pesan *phishing* perpajakan tanpa menimbulkan bias kata kunci pada pesan resmi.

c) Membuat *prototype* aplikasi web deteksi pesan *phishing* yang interaktif menggunakan *framework* Streamlit dengan mengintegrasikan model klasifikasi terbaik. Purwarupa ini disiapkan sebagai sarana verifikasi mandiri yang praktis bagi masyarakat dan wajib pajak.

## 1.5 Manfaat Penelitian

Hasil pelaksanaan penelitian dan pengembangan purwarupa sistem deteksi pesan *phishing* ini diharapkan dapat memberikan dampak positif yang nyata bagi berbagai pemangku kepentingan. Manfaat utama dari karya ilmiah Tugas Akhir ini meliputi kontribusi pada pengembangan ilmu pengetahuan, dukungan bagi instansi terkait, serta pelindungan masyarakat umum. Rincian manfaat penelitian tersebut diuraikan sebagai berikut:

a) Manfaat bagi Bidang Ilmu Pengetahuan dan Teknologi (IPTEKS): Menyumbangkan rujukan ilmiah dan bukti empiris mengenai perbandingan kinerja algoritma *Support Vector Machine* terhadap *Random Forest* berbasis TF-IDF *n-gram*. Korpus terkurasi yang disusun dalam penelitian ini juga dapat dipakai kembali untuk pengembangan pemrosesan bahasa alami (*Natural Language Processing*) bahasa Indonesia.

b) Manfaat bagi Instansi dan Pengambil Kebijakan: Memberikan masukan teknis beserta model purwarupa yang dapat dijadikan bahan pertimbangan oleh otoritas perpajakan maupun pengelola keamanan siber. Hasil analisis terhadap dua belas kategori modus penipuan pajak ini dapat mendukung penyusunan strategi edukasi pelindungan wajib pajak yang berbasis data.

c) Manfaat bagi Masyarakat dan Wajib Pajak: Menyediakan alat bantu verifikasi mandiri berbasis web yang mudah diakses kapan saja melalui perangkat pengguna. Masyarakat dapat memeriksa keaslian teks pesan WhatsApp yang mengatasnamakan Direktorat Jenderal Pajak sebelum mengakses tautan mencurigakan atau mengunduh lampiran `.apk`.

## 1.6 Metode Penelitian

Penelitian ini menggunakan pendekatan kuantitatif eksperimental yang dipadukan dengan metode perancangan teknik atau *Research and Development* (R&D) sesuai skema Tugas Akhir *Prototype* di Universitas Siber Asia [15], [16]. Pengumpulan data dilakukan melalui studi dokumentasi dan ekstraksi otomatis (*web scraping*) pada 68 sumber informasi publik yang otoritatif [17]. Sumber tersebut meliputi pengumuman resmi Direktorat Jenderal Pajak (`pajak.go.id`), siaran pers unit kerja KPP, portal cek fakta pemerintah daerah, serta berita perpajakan nasional terverifikasi [2], [5]. Seluruh data yang dihimpun merupakan informasi publik terbuka sehingga tidak melanggar kerahasiaan data wajib pajak.

Data spesifik perpajakan yang terkumpul sebanyak 260 baris tersebut dikurasi secara seimbang menjadi 130 pesan *phishing* dari 12 kategori modus dan 130 pesan resmi dari 10 kategori layanan. Penyeimbangan proporsi kelas ini dilakukan agar model klasifikasi tidak mengalami bias kata kunci terhadap istilah administrasi perpajakan. Korpus perpajakan itu kemudian digabungkan dengan 904 baris korpus dasar SMS berbahasa Indonesia berlisensi terbuka sehingga membentuk dataset gabungan utama sebanyak 1.164 baris [6], [7]. Rincian komposisi datanya tampak pada Tabel 1.1.

Tabel 1.1 Komposisi Korpus Dataset Penelitian

| Nama Korpus Data | Sumber Rujukan Utama | Kelas Phishing (Baris) | Kelas Aman (Baris) | Total Rekaman (Baris) |
| :--- | :--- | :---: | :---: | :---: |
| Korpus Dasar SMS Indonesia | Repositori Publik UPI & IEEE EIConCIT [6], [7] | 335 | 569 | 904 |
| Korpus Spesifik Perpajakan | Kurasi 68 Sumber Resmi DJP & Cek Fakta [2], [5] | 130 | 130 | 260 |
| Dataset Gabungan Utama | Penggabungan Biner Terverifikasi SHA-256 | 465 | 699 | 1.164 |

Tahap analisis data diawali praproses teks bahasa Indonesia yang meliputi pembersihan karakter, *case folding*, tokenisasi `token_apk` dan `token_url`, penghapusan kata henti, serta *stemming* Sastrawi. Teks bersih itu diubah menjadi matriks numerik dengan pembobotan TF-IDF *n-gram* $(1, 2)$ maksimal 3.000 fitur, lalu dibagi terstratifikasi sebesar 80:20 [18], [19]. Selanjutnya, dilakukan pelatihan dan penalaan parameter pada *Support Vector Machine* (*LinearSVC*) serta *Random Forest Classifier*. Kinerja kedua model diukur memakai *Confusion Matrix* dan diintegrasikan ke aplikasi Streamlit pada TKT level 6. Urutan tahapan itu tampak pada Gambar 1.1.

![Gambar 1.1 Tahapan Metode Penelitian.](assets/gambar_1_1_tahapan_penelitian.png)

Gambar 1.1 Tahapan Metode Penelitian.

Berdasarkan karakteristik matriks fitur TF-IDF yang berdimensi tinggi dan bersifat renggang (*sparse matrix*), penelitian ini merumuskan hipotesis kerja untuk diuji secara empiris pada tahap eksperimen [18], [19]. Hipotesis penelitian ini menyatakan bahwa terdapat perbedaan kinerja klasifikasi yang terukur antara kedua algoritma, dan algoritma *Support Vector Machine* (*LinearSVC*) menghasilkan nilai *Recall* serta *F1-Score* deteksi pesan *phishing* perpajakan yang lebih unggul dibandingkan *Random Forest*. Hasil eksperimen pendahuluan (*baseline*) pada 233 data uji mendukung hipotesis tersebut karena *Support Vector Machine* mampu mencapai akurasi 98,71% dan *Recall* 1,00. Capaian itu melampaui algoritma *Random Forest* yang memperoleh akurasi 96,57% serta *Recall* 0,95.

---

# DAFTAR PUSTAKA

[1] Waluyo, *Perpajakan Indonesia*, ed. ke-13. Jakarta: Salemba Empat, 2020.

[2] Direktorat Jenderal Pajak, “Pengiriman WhatsApp Blast dalam rangka edukasi Coretax DJP,” *Portal Resmi Direktorat Jenderal Pajak Kementerian Keuangan Republik Indonesia*, 2024. [Online]. Available: https://www.pajak.go.id/id/pengumuman/pengiriman-whatsapp-blast-dalam-rangka-edukasi-coretax-djp

[3] N. B. Prakoso, H. Ayu, and H. Zakaria, “Misuse of taxpayer data for phising scams,” *Journal of International Islamic Law, Human Right and Public Policy*, 2026, doi: 10.5281/zenodo.21853028.

[4] R. Alabdan, “Phishing attacks survey: Types, vectors, and technical approaches,” *Future Internet*, vol. 12, no. 10, p. 168, Oct. 2020, doi: 10.3390/fi12100168.

[5] Direktorat Jenderal Pajak, “Waspada penipuan yang mengatasnamakan Direktorat Jenderal Pajak (Pengumuman Nomor PENG-31/PJ.09/2024 s.d. PENG-50/PJ.09/2025),” *Portal Resmi Direktorat Jenderal Pajak Kementerian Keuangan Republik Indonesia*, 2025. [Online]. Available: https://www.pajak.go.id/id/pengumuman/waspada-penipuan-yang-mengatasnamakan-direktorat-jenderal-pajak

[6] F. Rahmi and Y. Wibisono, “Dataset klasifikasi bahasa Indonesia SMS spam,” *Repositori Universitas Pendidikan Indonesia*, Bandung, 2016. [Online]. Available: https://repository.upi.edu/26936/

[7] A. Theodorus, T. K. Prasetyo, R. Hartono, and D. Suhartono, “Short Message Service (SMS) spam filtering using machine learning in Bahasa Indonesia,” in *Proc. East Indonesia Conf. Comput. Inf. Technol. (EIConCIT)*, Apr. 2021, pp. 199-203, doi: 10.1109/EIConCIT50028.2021.9431859.

[8] D. Irawan, E. B. Perkasa, and Y. Yurindra, “Perbandingan klassifikasi SMS berbasis Support Vector Machine, Naive Bayes Classifier, Random Forest dan Bagging Classifier,” *Jurnal Sisfokom (Sistem Informasi dan Komputer)*, vol. 10, no. 3, pp. 432-437, Dec. 2021, doi: 10.32736/sisfokom.v10i3.1302.

[9] M. S. Al Ghofany, R. Dwiyansaputra, F. Bimantoro, and A. Aranta, “Indonesian SMS spam detection using TF-RF feature weighting method and Support Vector Machine classifier,” in *Proc. Int. Conf. Intell. Cybern. Technol. Appl. (ICICyTA)*, 2022, pp. 112-119, doi: 10.2991/978-94-6463-084-8_12.

[10] F. F. Tampinongkol, A. R. Kamila, and A. C. Wardhana, “Implementation of Random Forest classification and Support Vector Machine algorithms for phishing link detection,” *Journal of Informatics Information System Software Engineering and Applications (INISTA)*, vol. 7, no. 1, pp. 1-10, Nov. 2024, doi: 10.20895/inista.v7i1.1588.

[11] A. Al Tawil, L. H. Almazaydeh, D. Qawasmeh, B. Qawasmeh, M. Alshinwan, and K. Elleithy, “Comparative analysis of machine learning algorithms for email phishing detection using TF-IDF, Word2Vec, and BERT,” *Computers, Materials & Continua*, vol. 81, no. 2, pp. 3395-3412, Nov. 2024, doi: 10.32604/cmc.2024.057279.

[12] F. M. Efendi, A. K. Adisusilo, and S. Budiprayitno, “Pengembangan sistem deteksi phishing pada WhatsApp berbasis AI dengan integrasi bahasa lokal Surabaya,” *Melek IT Information Technology Journal*, vol. 11, no. 1, pp. 45-54, 2025, doi: 10.30742/melekitjournal.v11i1.417.

[13] R. B. Saputra, M. Azwar, and L. Widyawati, “Implementasi algoritma SVM pada bot WhatsApp untuk deteksi pesan spam,” *Jurnal Manajemen Informatika dan Sistem Informasi*, vol. 9, no. 1, pp. 12-21, Jan. 2026, doi: 10.36595/misi.v9i1.1803.

[14] A. A. Ningtias, N. Anwar, and A. Ichwani, “Komparasi kinerja Support Vector Machine dan Random Forest untuk deteksi spam email berbasis TF-IDF teks,” *IKRA-ITH Informatika: Jurnal Komputer dan Informatika*, vol. 10, no. 1, pp. 55-64, 2026.

[15] C. R. Hassolthine, U. Darusalam, and M. Ikhwani, *Pedoman Teknis Penulisan Tugas Akhir Mahasiswa Universitas Siber Asia (SK Rektor Nomor 01 Tahun 2024)*. Jakarta: Universitas Siber Asia, 2024.

[16] Sugiyono, *Metode Penelitian Kuantitatif, Kualitatif, dan R&D*, ed. ke-2. Bandung: Alfabeta, 2023.

[17] M. Darwin, M. R. Mamondol, S. A. Sormin, and Y. Nurhayati, *Metode Penelitian Pendekatan Kuantitatif*. Bandung: Media Sains Indonesia, 2021.

[18] Sugiyono, *Statistika untuk Penelitian*. Bandung: Alfabeta, 2019.

[19] L. P. Sinambela, *Metodologi Penelitian Kuantitatif: Teoretik dan Praktik*. Depok: Rajawali Pers, 2021.
