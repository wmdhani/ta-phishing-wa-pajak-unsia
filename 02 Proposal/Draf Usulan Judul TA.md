# USULAN TOPIK DAN RANCANGAN TUGAS AKHIR

**Program Studi**: PJJ Sistem Informasi  
**Ketua Program Studi**: Vika Febri Muliati, S.Kom., M.Kom  
**Institusi**: Universitas Siber Asia (UNSIA)  
**Skema**: Tugas Akhir Prototype  

---

### Data Mahasiswa dan Pembimbing
* **Nama Mahasiswa**: Wan Mirza Dhani
* **NIM**: 240101020194
* **Dosen Pembimbing**: Novi Dian Nathasia, S.Kom., MMSI

---

### Judul Tugas Akhir
> **Komparasi Algoritma Support Vector Machine dan Random Forest dalam Deteksi Pesan Phishing WhatsApp Mengatasnamakan Otoritas Perpajakan**

---

### 1. Latar Belakang Masalah
Transformasi layanan digital perpajakan melalui sistem *Coretax* (`coretaxdjp.pajak.go.id`), aplikasi *M-Pajak*, serta *WhatsApp Blast* resmi Direktorat Jenderal Pajak (DJP) turut memicu maraknya kejahatan siber berbasis rekayasa sosial (*social engineering*) melalui WhatsApp. Pelaku mencatut identitas DJP dan Kantor Pelayanan Pajak (KPP) dengan narasi pemutakhiran data *Coretax*, pemadanan NIK-NPWP, surat tagihan tunggakan pajak, hingga pengiriman berkas berbahaya berformat *Android Package Kit* (`.apk`) dan tautan tiruan.

Wajib pajak awam kerap kesulitan membedakan pesan resmi dari pesan penipuan karena pelaku meniru format surat dinas beserta istilah perpajakan sahih seperti kode *billing* dan EFIN. Di sisi lain, penyaringan spam konvensional yang hanya dilatih pada korpus SMS umum rentan mengalami bias kata kunci (*keyword bias*), sehingga pesan resmi DJP berisiko ikut terblokir. Selain itu, pemeriksaan melalui laman web terpisah masih merepotkan karena pengguna harus menyalin dan menempelkan (*copy-paste*) isi pesan satu per satu. Oleh karena itu, diperlukan komparasi model berbasis *Natural Language Processing* (NLP) dan *Machine Learning* (*Support Vector Machine* vs *Random Forest*) pada korpus seimbang yang disajikan melalui **REST API (FastAPI)**, **Ekstensi Peramban *WhatsApp Web* (Manifest V3)** dengan penjelasan kata pemicu (*explainable detection*), serta ***dashboard* Streamlit**.

---

### 2. Rumusan Masalah
Mengacu pada ketentuan kaidah sebab-akibat Pedoman Penulisan Tugas Akhir UNSIA:
1. Kemiripan gaya bahasa kedinasan dan pemakaian istilah resmi perpajakan pada pesan penipuan (*phishing*) WhatsApp menyulitkan verifikasi manual oleh wajib pajak sehingga meningkatkan risiko pencurian kredensial dan kerugian finansial.
2. Ketergantungan model penyaringan spam konvensional pada korpus pesan singkat umum tanpa penyeimbangan teks resmi perpajakan menimbulkan bias kata kunci (*keyword bias*), yang berpotensi menghasilkan *false positive* pada pengumuman resmi DJP maupun *false negative* pada pesan penipuan baru.
3. Perbedaan mekanisme klasifikasi antara *Support Vector Machine* (*LinearSVC*) pada ruang fitur TF-IDF berdimensi tinggi dan *Random Forest Classifier* berbasis *ensemble* pohon keputusan menuntut pengujian empiris untuk menentukan model terbaik guna diintegrasikan ke dalam mekanisme verifikasi langsung tanpa salin-tempel melalui REST API (FastAPI), ekstensi peramban *WhatsApp Web* dengan penjelasan kata pemicu, serta *dashboard* Streamlit.

---

### 3. Batasan Masalah
Ruang lingkup penelitian dibatasi pada:
1. Objek penelitian adalah klasifikasi biner teks pesan singkat berbahasa Indonesia dengan kelas `1` (*phishing/fraud*) dan kelas `0` (aman/resmi perpajakan).
2. Sumber data murni memanfaatkan korpus publik terbuka tanpa data rahasia internal instansi, yaitu **1.164 baris dataset gabungan utama** yang memadukan **904 baris** korpus SMS berbahasa Indonesia (Rahmi & Wibisono, dari total 1.143 baris setelah mengeksklusi 239 pesan promo/operator) dan **260 baris** korpus spesifik perpajakan seimbang (130 pesan *phishing* dari 12 kategori modus dan 130 pesan resmi/normal dari 10 kategori layanan) yang dikurasi dari **65 dari 68 sumber publik** yang dihimpun (sebagian besar terbit periode 2024–2026).
3. Tahapan praproses teks meliputi *case folding*, transformasi pola berkas `.apk` menjadi `token_apk`, transformasi tautan menjadi `token_url`, pembersihan karakter nonalfanumerik, *stopword removal*, dan *stemming* Sastrawi, dilanjutkan pembobotan **TF-IDF *n-gram* (1, 2)** maksimal 3.000 fitur.
4. Algoritma yang dikomparasikan adalah *Support Vector Machine* (`LinearSVC`) dan *Random Forest Classifier* dengan pembagian data terstratifikasi 80:20 (931 data latih dan 233 data uji).
5. Evaluasi performa model diukur menggunakan *Confusion Matrix* (*Accuracy*, *Precision*, *Recall*, dan *F1-Score*), dengan fokus pada minimalisasi *False Negative* dan *False Positive*.
6. Luaran (*outcome*) berupa purwarupa sistem terpadu target Tingkat Kesiapan Teknologi (**TKT level 6**) yang terdiri atas layanan inferensi **REST API (FastAPI)**, **Ekstensi Peramban *WhatsApp Web* (Manifest V3)** (tombol/lencana pemeriksaan langsung pada gelembung obrolan dan menu klik kanan tanpa *copy-paste*), serta ***dashboard* Streamlit**, dilengkapi lapisan *explainable detection* (bobot kata pemicu `LinearSVC`, deteksi `.apk`/`token_apk`, dan verifikasi domain resmi `pajak.go.id`).

---

### 4. Tujuan Penelitian
1. Menyusun korpus teks berbahasa Indonesia bertema perpajakan yang seimbang antara kelas penipuan dan kelas layanan resmi serta menerapkan praproses Sastrawi, tokenisasi khusus, dan pembobotan TF-IDF.
2. Menguji, menghitung, dan menganalisis perbandingan performa *Accuracy*, *Precision*, *Recall*, dan *F1-Score* antara algoritma *Support Vector Machine* (`LinearSVC`) dan *Random Forest Classifier*.
3. Mengembangkan *prototype* deteksi pesan *phishing* terintegrasi berbasis **REST API (FastAPI)**, **Ekstensi Peramban *WhatsApp Web* (Manifest V3)**, dan ***dashboard* Streamlit** menggunakan model terbaik dengan fitur penjelasan kata pemicu agar pengguna dapat memeriksa pesan langsung di *WhatsApp Web* tanpa *copy-paste*.

---

### 5. Manfaat Penelitian
1. **Bagi IPTEKS & Universitas Siber Asia (UNSIA)**: Memberikan kontribusi empiris komparasi SVM dan Random Forest berbasis TF-IDF *n-gram* dengan mitigasi bias kata kunci, sekaligus menyediakan korpus terbuka dan modul purwarupa sebagai aset praktikum/pembelajaran NLP di Prodi PJJ Sistem Informasi UNSIA serta penguat literasi keamanan siber bagi ekosistem kampus daring UNSIA.
2. **Bagi Instansi & Pengambil Kebijakan**: Memberikan masukan teknis dan pemetaan 12 kategori modus penipuan pajak untuk mendukung strategi edukasi pelindungan wajib pajak.
3. **Bagi Masyarakat / Wajib Pajak**: Menyediakan sarana verifikasi praktis langsung di *WhatsApp Web* melalui ekstensi peramban maupun *dashboard* Streamlit—lengkap dengan penjelasan kata pemicu—sehingga masyarakat tidak perlu *copy-paste* sebelum memutuskan mengklik tautan atau mengunduh berkas `.apk`.

---

### 6. Metodologi Penelitian & Kesiapan Saat Ini
Alur pelaksanaan penelitian menggabungkan pendekatan kuantitatif eksperimental dan *Research and Development* (R&D):
1. **Pengumpulan & Kurasi Data (Selesai)**: Kompilasi 65 dari 68 sumber publik yang dihimpun (sebagian besar terbit 2024–2026: DJP `pajak.go.id`, KPP/KP2KP, DDTC, Ortax, Jalahoaks, BCA, Antara, DetikFinance) menjadi 260 pesan pajak seimbang, lalu digabung dengan 904 pesan SMS publik (dari 1.143 baris pascaeksklusi 239 pesan promo/operator) menjadi 1.164 baris dataset gabungan utama beserta katalog *checksum* SHA-256.
2. **Pra-pengolahan Teks (*Preprocessing*)**: *Case folding*, tokenisasi khusus `token_apk` dan `token_url`, pembersihan karakter nonalfanumerik, *stopword removal*, serta *stemming* bahasa Indonesia menggunakan **Sastrawi**.
3. **Ekstraksi Fitur & Pembagian Data**: Pembobotan fitur menggunakan **TF-IDF *n-gram* (1, 2)** maksimal 3.000 fitur dan pembagian *stratified train-test split* 80:20 (931 latih, 233 uji).
4. **Pelatihan, Evaluasi & Uji Ablasi Bias Kata Kunci**: Komparasi `LinearSVC` vs `RandomForestClassifier` (*n_estimators=200*) menggunakan *Confusion Matrix*. Pada skenario *baseline*, `LinearSVC` meraih **akurasi 98,28%** (*Recall* 0,98; *F1-Score* 0,98; hanya 2 *False Negative* dan 2 *False Positive*), mengungguli `Random Forest` (**akurasi 95,28%**, *Recall* 0,95; *F1-Score* 0,94; 5 *False Negative* dan 6 *False Positive*). Uji ablasi pada 44 data uji bertema pajak membuktikan pelibatan korpus pajak seimbang menaikkan akurasi subset pajak dari **40,91%** (korpus SMS umum saja) dan **52,27%** (tanpa pesan resmi pajak seimbang) menjadi **97,73%**.
5. **Pengembangan Sistem Terintegrasi (Tahap Berikutnya)**: Penalaan parameter lanjutan, analisis bobot fitur pemicu (*explainable detection*), serta integrasi model terbaik ke **REST API (FastAPI)**, **Ekstensi Peramban *WhatsApp Web* (Manifest V3)**, dan ***dashboard* Streamlit** hingga pengujian fungsional (TKT level 6).
