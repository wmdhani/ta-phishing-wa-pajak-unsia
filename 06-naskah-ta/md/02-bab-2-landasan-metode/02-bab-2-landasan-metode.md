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
