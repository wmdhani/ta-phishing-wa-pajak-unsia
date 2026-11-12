# USULAN TOPIK DAN RANCANGAN TUGAS AKHIR

**Program Studi**: PJJ Informatika  
**Institusi**: Universitas Siber Asia (UNSIA)  
**Skema**: Tugas Akhir Prototype  

---

### Data Mahasiswa dan Pembimbing
* **Nama Mahasiswa**: Wan Mirza Dhani
* **NIM**: 240101020194
* **Dosen Pembimbing**: Novi Dian Nathasia, S.Kom, MMSI.

---

### Judul Tugas Akhir
> **Komparasi Algoritma Support Vector Machine dan Random Forest dalam Deteksi Pesan Phishing WhatsApp Mengatasnamakan Otoritas Perpajakan**

---

### 1. Latar Belakang Masalah
Peningkatan pemanfaatan saluran komunikasi digital seperti WhatsApp sebagai media layanan informasi publik diiringi oleh maraknya kejahatan siber berbasis rekayasa sosial (*social engineering*). Salah satu modus yang paling sering terjadi di Indonesia adalah pengiriman pesan penipuan (*phishing*) yang mengatasnamakan otoritas perpajakan (Direktorat Jenderal Pajak). Pelaku memanipulasi kepanikan wajib pajak melalui narasi tagihan tunggakan pajak, surat imbauan klarifikasi, pembekuan rekening/NPWP, serta lampiran berkas berbahaya berformat Android Package Kit (`.apk`).

Masyarakat awam kerap kesulitan membedakan pesan resmi dari otoritas perpajakan dengan pesan manipulatif tersebut karena pesan penipuan disusun menyerupai format kedinasan resmi. Upaya sosialisasi yang dilakukan otoritas terkait belum sepenuhnya mampu menghentikan laju korban. Oleh karena itu, diperlukan suatu sistem deteksi cerdas berbasis *Natural Language Processing* (NLP) dan *Machine Learning* yang mampu mengenali pola teks serta karakteristik pesan *phishing* secara otomatis dan memberikan peringatan dini kepada masyarakat secara cepat.

---

### 2. Rumusan Masalah
Mengacu pada ketentuan kaidah sebab-akibat pedoman penulisan Tugas Akhir UNSIA:
1. Maraknya pesan penipuan (*phishing*) WhatsApp bertema perpajakan dengan teknik rekayasa sosial dan lampiran file `.apk` berbahaya yang mengecoh masyarakat sehingga berpotensi menimbulkan kerugian finansial serta kebocoran data pribadi wajib pajak.
2. Belum tersedianya alat bantu deteksi otomatis berbasis teks lokal berbahasa Indonesia yang membandingkan keandalan algoritma klasifikasi (*Support Vector Machine* vs *Random Forest*) secara spesifik untuk kasus penipuan perpajakan.

---

### 3. Batasan Masalah
Ruang lingkup penelitian dibatasi pada:
1. Objek penelitian berfokus pada data teks pesan berbahasa Indonesia bertema perpajakan (pesan resmi notifikasi layanan vs pesan penipuan/phishing).
2. Data diperoleh dari kompilasi tangkapan layar publik/edukasi resmi otoritas perpajakan serta korpus publik penipuan SMS/WhatsApp berbahasa Indonesia di ranah publik (tanpa menggunakan data rahasia instansi).
3. Metode ekstraksi fitur teks yang digunakan adalah *Term Frequency-Inverse Document Frequency* (TF-IDF) dengan tahapan *text preprocessing* (pembersihan teks, *case folding*, *stopword removal*, dan *stemming*).
4. Algoritma klasifikasi yang dikomparasikan dibatasi pada *Support Vector Machine* (SVM) dan *Random Forest* (RF).
5. Evaluasi performa model diukur menggunakan *Confusion Matrix* dengan metrik *Accuracy*, *Precision*, *Recall*, dan *F1-Score*.
6. Luaran (*outcome*) berupa prototipe aplikasi web interaktif berbasis Python (Streamlit) yang memungkinkan pengguna menempelkan teks pesan dan memperoleh hasil klasifikasi (*Phishing* atau *Aman*) beserta skor probabilitasnya.

---

### 4. Tujuan Penelitian
1. Mengembangkan model klasifikasi teks berbasis *Natural Language Processing* untuk mendeteksi pesan penipuan perpajakan pada WhatsApp.
2. Membandingkan performa akurasi, presisi, *recall*, dan *f1-score* antara algoritma *Support Vector Machine* (SVM) dan *Random Forest* (RF).
3. Membangun prototipe aplikasi web deteksi pesan *phishing* berbasis Streamlit sebagai sarana verifikasi mandiri bagi masyarakat.

---

### 5. Manfaat Penelitian
1. **Bagi Akademik**: Memberikan kontribusi empiris mengenai performa komparasi algoritma SVM dan Random Forest pada korpus spesifik kejahatan siber berbahasa Indonesia.
2. **Bagi Masyarakat / Pengguna Layanan**: Menyediakan alat verifikasi mandiri yang mudah diakses untuk memeriksa keaslian pesan yang mengatasnamakan otoritas pajak sebelum membuka tautan atau mengunduh lampiran.
3. **Bagi Pengembang Sistem**: Menjadi rujukan implementasi filter otomatis pada sistem komunikasi digital.

---

### 6. Metodologi Penelitian
Alur pelaksanaan penelitian dirancang sistematis:
1. **Pengumpulan Data**: Pengumpulan korpus teks pesan *phishing* perpajakan dan pesan notifikasi resmi publik.
2. **Pra-pengolahan Teks (*Preprocessing*)**: *Cleaning* (menghapus URL, tanda baca, angka), *Case Folding*, *Stopwords Removal*, dan *Stemming* bahasa Indonesia.
3. **Ekstraksi Fitur**: Pembobotan kata menggunakan TF-IDF *vectorizer*.
4. **Pelatihan Model (*Model Training*)**:
   - Algoritma 1: *Support Vector Machine* (analisis *hyperparameter tuning* kernel Linear/RBF).
   - Algoritma 2: *Random Forest* (penalaan parameter *n_estimators* dan *max_depth*).
5. **Evaluasi & Komparasi Model**: Pengujian data uji (*test set*) menggunakan *Confusion Matrix* (menitikberatkan pada minimalisasi *False Negative*).
6. **Pengembangan Prototipe Web**: Integrasi model terbaik ke antarmuka web interaktif menggunakan framework Streamlit.
