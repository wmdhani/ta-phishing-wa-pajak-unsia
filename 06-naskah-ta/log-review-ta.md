# Log Audit Bagian Awal dan Bab I Tugas Akhir

**Status:** Audit Ulang & Eksekusi Revisi Selesai (Tervalidasi Pasca-Revisi)  
**Tanggal Audit & Pemutakhiran:** 24 November 2026 (pemutakhiran dari audit awal 22 November 2026)  
**Program Studi:** S1 PJJ Sistem Informasi, Universitas Siber Asia (UNSIA)  
**Skema Tugas Akhir:** *Prototype* (Target Kesiapterapan TKT Level 6)

---

## 1. Identitas dan Ruang Lingkup Audit

Audit ini memeriksa kondisi mutakhir **Bagian Awal** dan **BAB I Pendahuluan** pada empat pilar: validitas referensi `[1]`–`[24]` beserta fakta empiris/dataset, kepatuhan terhadap Pedoman Teknis Penulisan TA UNSIA 2024, kedalaman narasi S1 Sistem Informasi serta kealamian bahasa Indonesia (*humanizer-indonesia* & bebas pola AI), dan sinkronisasi jembatan lintas bab.

**Berkas utama yang diaudit:**
1. `06-naskah-ta/md/00-bagian-awal/00-bagian-awal.md` (205 baris)
2. `06-naskah-ta/md/01-bab-1-pendahuluan/01-bab-1-pendahuluan.md` (83 baris)

**Berkas pembanding dan instrumen verifikasi:**
1. `01-administrasi/pedoman-penulisan-ta-unsia-2024.pdf` dan `01-administrasi/daftar-pembagian-dosen-pembimbing-ta.xlsx`
2. `06-naskah-ta/md/06-lampiran/06-lampiran.md` (Daftar Pustaka `[1]`–`[36]` dan Lampiran 1–5)
3. `03-referensi/catatan-kebaruan-dan-daftar-referensi.md`, `03-referensi/daftar-pustaka/`, `03-referensi/ebook-metodologi/`, dan `04-dataset/01-data-mentah/Theodorus 2021 Dokumentasi Korpus.md`
4. `04-dataset/01-data-mentah/DJP Ringkasan Scrape 68 Sumber Resmi.csv`, `04-dataset/02-data-olahan/Dataset Pajak Terkurasi 260 Baris.csv`, `04-dataset/02-data-olahan/Dataset Gabungan Utama Biner 1164 Baris.csv`, serta `05-hasil-evaluasi/json/ringkasan_eksperimen_lengkap.json` dan `ml/eksperimen_komparasi.py`
5. Skrip validator `validate_unsia.py`, skrip metrik gaya `humanizer-indonesia/scripts/metrik.py`, pustaka Zotero (`6WSLSX4K`), serta verifikasi metadata daring (`[1]`, `[17]`).

> [!NOTE]
> **Status Angka Hasil di Abstrak dan *Abstract*:** Seluruh metrik capaian pada `00-bagian-awal.md` L70 & L76 (`97,16%`, `97,74%`, `94,07%`, `95,25%`, `98,17%`, `42,22%`, `95,56%`, `95,69%`, `0,9957`, `0,02542`, `0,04214`, `2.519`, `96,03%`, `92,46%`) **tetap ditandai untuk diverifikasi ulang pada sesi Bab IV** (tidak diubah pada sesi Bagian Awal & Bab I).

---

## 2. Tujuan Bab I Terkunci dan Pemetaan Keselarasan (1.2–1.6)

Subbab 1.4 (`01-bab-1-pendahuluan.md` L47–L51) menetapkan tiga tujuan terukur berikut:

| Butir Tujuan (Subbab 1.4) | Rumusan Masalah Terkait (1.2) | Batasan Masalah (1.3) | Manfaat (1.5) | Cakupan di Metode (1.6) | Status Keselarasan |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **a)** Menyusun korpus teks perpajakan berbahasa Indonesia berimbang antara pesan *phishing* dengan pengumuman resmi, lalu memprosesnya melalui `token_apk`, `token_url`, Sastrawi, dan TF-IDF. | **a)** Peniruan surat dinas dan istilah perpajakan menyulitkan verifikasi manual wajib pajak; **b)** Penyaring berbasis SMS umum bias pada diksi kedinasan. | **a)** Klasifikasi biner teks Indonesia; **b)** `1.164` baris (`904` SMS + `260` teks pajak dari `65/68` sumber 2021–2026); **c)** Sastrawi, `token_apk`, `token_url`, TF-IDF maks. `3.000` fitur unigram-bigram. | **a)** Korpus pajak terbuka untuk praktikum NLP Prodi PJJ SI; **b)** Pemetaan 12 modus penipuan pajak. | Studi dokumentasi 68 arsip publik (`2021–2026`), kurasi 260 pesan pajak (`130` penipuan 12 modus + `130` aman 10 kategori resmi/normal) + 904 SMS (Tabel 1.1), Sastrawi, dan TF-IDF maks. 3.000 fitur. | **Selaras** (fakta L65 & atribusi `[9]`/`[10]`/`[13]` di L77 telah diluruskan). |
| **b)** Menguji dan membandingkan kinerja klasifikasi serta kalibrasi probabilitas antara `LinearSVC` berkalibrasi *Platt scaling* dengan *Random Forest*, termasuk uji kontrol tanpa korpus pajak. | **b)** Ketimpangan data latih SMS umum memicu *false positive* dan *false negative*; **c)** Ketiadaan tolok ukur komparatif terkalibrasi pada korpus pajak Indonesia menyulitkan pemilihan model peringatan dini. | **d)** Komparasi pada `1.159` teks unik pascadeduplikasi `5` baris (split terstratifikasi `927:232`); **e)** *Confusion Matrix*, 10-Fold CV, *ROC-AUC*, *PR-AUC*, *Brier Score*, dan *Log Loss*. | **a)** Bukti empiris perbandingan kinerja dan mitigasi *keyword bias*. | Validasi silang 10-fold, penyetelan hiperparameter, kalibrasi probabilitas, dan uji kontrol bias tanpa korpus pajak (L77–L83). | **Selaras** (butir `1.2 c)` telah dipertajam menjadi sebab-akibat). |
| **c)** Merancang, membangun, dan menguji purwarupa sistem deteksi terpadu berbasis REST API FastAPI, antarmuka web *Cek Pesan Pajak*, serta ekstensi *WhatsApp Web* beserta penjelas kata pemicu berbahasa awam. | **a)** Kekeliruan penilaian mendorong korban memasang `.apk` berbahaya; **c)** Absennya alat verifikasi langsung di *WhatsApp Web* memaksa pengecekan manual tanpa petunjuk risiko. | **f)** Purwarupa TKT Level 6 berbahasa Python (FastAPI, web *Cek Pesan Pajak*, ekstensi *Manifest V3*) dilengkapi penjelas kata pemicu, pemindai `.apk`, dan verifikasi `pajak.go.id`. | **b)** Rujukan mekanisme verifikasi kanal resmi; **c)** Alat verifikasi praktis sebelum warga mengeklik tautan atau memasang `.apk`. | Integrasi model terbaik berpenjelas bobot pemicu ke purwarupa TKT Level 6 pada Gambar 1.1 (L77). | **Selaras & Kuat pada Fokus S1 Sistem Informasi.** |

---

## 3. Peta Sitasi `[1]`–`[24]` Bab I

Semua nomor sitasi `[1]`–`[24]` pada `01-bab-1-pendahuluan.md` terpakai secara berurutan dari `[1]` hingga `[24]` dan terdaftar lengkap pada `06-naskah-ta/md/06-lampiran/06-lampiran.md` L3–L49.

| No | Ringkasan Sumber (Daftar Pustaka) | Berkas PDF Lokal / Bukti Sumber | Lokasi & Klaim di Bab I (Pasca-Revisi) | Status Verifikasi |
| :---: | :--- | :--- | :--- | :--- |
| `[1]` | Waluyo & N. A. Wijayanti (2026), *Perpajakan Indonesia*, ed. ke-13 | Tidak ada PDF (buku komersial Salemba Empat; terverifikasi bibliografi daring & Zotero `MR5Q3T6F`) | L5 (`coretaxdjp` & layanan digital DJP); L7 (istilah kode *billing* & EFIN) | **Sesuai.** (Edisi ke-13 tahun 2026 memuat sistem Coretax & pembayaran pajak elektronik). |
| `[2]` | DJP (Nov. 2024), PENG-32/PJ.09/2024 tentang Coretax | Ada (`02 DJP 2024 PENG-32...pdf`) | L5 (`coretaxdjp` & WA resmi); L7 (pencatutan nama layanan resmi); L33, L65 (bagian pengumuman resmi DJP dalam 68 sumber) | **Sesuai.** (`PENG-32` membahas Coretax & WA Blast resmi `+62 822-3000-9880`). |
| `[3]` | Prakoso, Ayu, & Zakaria (Jul. 2026), *JISHUP* | Ada (`03 Prakoso 2026...pdf`) | L5 (*M-Pajak*, *smishing* petugas pajak, erosi kepercayaan layanan publik); L13 (fokus aspek hukum tanpa detektor teks otomatis) | **Sesuai.** (`M-Pajak` & metode yuridis-empiris terverifikasi pada PDF hlm. 1560–1569). |
| `[4]` | Alabdan (Okt. 2020), *Future Internet* | Ada (`04 Alabdan 2020...pdf`) | L5 (penipuan berbasis pesan singkat / *smishing*) | **Sesuai.** (Membahas *smishing* dan pesan instan pada survei *phishing*). |
| `[5]` | DJP (2024–2026), PENG-31/PJ.09/2024 s.d. PENG-18/PJ.09/2026 | Ada 5 PDF (`05a`–`05e`) | L7 (`.apk`, tagihan fiktif, pencatutan nama layanan); L13 (`pajak.go.id`); L33, L65 (bagian dari 68 arsip 2021–2026) | **Sesuai.** (Modus `.apk`, tagihan/restitusi, *M-Pajak*/Coretax palsu, & `pajak.go.id` terverifikasi pada `05a`–`05e`; `coretax-online` ditarik ke temuan 68 arsip `SRC-028`). |
| `[6]` | Rahmi & Wibisono (2016), Skripsi UPI | Ada PDF parsial (`06 Rahmi...pdf`) + CSV lokal | L9 (SMS berbasis frekuensi kata); L11 (`character removal` nonhuruf merusak tautan/ekstensi); L33, L65, Tabel 1.1 (`904` SMS pascapenyisihan `239` promo) | **Sesuai.** (`1.143 - 239 = 904` baris: `335` penipuan + `569` normal). |
| `[7]` | Theodorus et al. (Apr. 2021), *IEEE EIConCIT* | Tidak ada PDF (*closed access* IEEE); ada `Theodorus 2021 Dokumentasi Korpus.md` & dataset lokal | L9 (deteksi spam SMS memakai pembobotan frekuensi kata) | **Sesuai.** (BoW 1.500 kata pada 4.125 SMS Indonesia). |
| `[8]` | Irawan et al. (Des. 2021), *Jurnal Sisfokom* | Ada (`08 Irawan 2021...pdf`) | L9 (deteksi spam SMS berbasis frekuensi kata/`CountVectorizer`) | **Sesuai.** |
| `[9]` | Al Ghofany et al. (2022), *Proc. MIMSE-I-C* | Ada (`09 Al Ghofany 2022...pdf`) | L9 (deteksi SMS dengan pembobotan kata); L77 (berakar pada *stemming* bahasa Indonesia — Nazief & Adriani) | **Sesuai.** (Telah diluruskan agar tidak diatribusikan ke pustaka Sastrawi). |
| `[10]` | Astuti et al. (Feb. 2024), *SJI* | Ada (`10 Astuti 2024...pdf`) | L9 (deteksi SMS berbasis TF-IDF); L77 (ekstraksi TF-IDF); L83 (keunggulan model linear pada teks pendek) | **Sesuai.** (Telah dipisahkan dari parameter batas `3.000` fitur). |
| `[11]` | Tampinongkol et al. (Nov. 2024), *INISTA* | Ada (`11 Tampinongkol 2024...pdf`) | L9 (komparasi SVM dan *Random Forest* pada fitur leksikal tautan *phishing*) | **Sesuai.** |
| `[12]` | Al Tawil et al. (Nov. 2024), *CMC* | Ada (`12 Al Tawil 2024...pdf`) | L9 (klasifikasi surel *phishing* dengan SVM dan RF) | **Sesuai.** |
| `[13]` | Ningtias et al. (Nov. 2026), *IKRA-ITH Informatika* | Ada (`13 Ningtias 2026...pdf`) | L9 (korpus pesan singkat publik pada studi spam); L11 (penghapusan URL saat *cleaning*); L77 (TF-IDF); L83 (keunggulan linear teks pendek) | **Sesuai.** (Diluruskan agar tidak menyebut datasetnya sebagai surel *phishing* maupun menetapkan 3.000 fitur). |
| `[14]` | Efendi et al. (Jun. 2025), *Melek IT* | Ada (`14 Efendi 2025...pdf`) | L11 (pendekatan logika *fuzzy* berbasis aturan pada WhatsApp Indonesia) | **Sesuai.** |
| `[15]` | Saputra et al. (Jan. 2026), *MISI* | Ada (`15 Saputra 2026...pdf`) | L11 (`HashingVectorizer` menghilangkan keterlacakan bobot kata); L77 (*stemming* Sastrawi) | **Sesuai.** (`Hashing Vectorizer` hlm. 6–9; Sastrawi hlm. 8; catatan metadata OJS `10.36595/misi.v9i1.1803`). |
| `[16]` | Sembiring et al. (Jun. 2026), *JSSR* | Ada (`16 Sembiring 2026...pdf`) | L11 (token tautan tanpa `.apk`/pajak; kemiripan kosakata pesan promosi resmi mengecoh penyaring kata kunci); L77 (pelestarian tautan) | **Sesuai.** (Konteks *pesan promosi resmi* sudah diperjelas di L11). |
| `[17]` | Mishra & Yadav (Sep. 2026), *IJASCA* | Tanpa PDF (*No galleys available*); abstrak OJS & Zotero `P5BS77GG` terverifikasi | L13 (penjelas kata pemicu); L77 (keterjelasan bobot pemicu); L83 (keunggulan linear pada teks pendek) | **Sesuai.** (TF-IDF unigram-bigram + `LinearSVC` + SHAP LinearExplainer). |
| `[18]` | Ismail, Nasution, & Gea (Jul. 2026), *IDEALIS* | Ada (`18 Ismail 2026...pdf`) | L13 (penjelas kata/fitur pemicu berbasis XAI dalam deteksi *phishing*) | **Sesuai.** |
| `[19]` | Suwarno et al. (Apr. 2026), *Komputa* | Ada (`19 Suwarno 2026...pdf`) | L15, L77 (ekstensi peramban untuk deteksi *phishing*) | **Sesuai.** |
| `[20]` | Hassolthine et al. (2024), *Pedoman TA UNSIA* | Ada (`01-administrasi/pedoman-penulisan-ta-unsia-2024.pdf`) | L15, L65, L77 (skema TA *Prototype* & TKT Level 6) | **Sesuai.** |
| `[21]` | Sugiyono (2023), *Metode Penelitian Kuantitatif, Kualitatif, dan R&D* | Ada (`03-referensi/ebook-metodologi/Sugiyono 2023...pdf`) | L65 (metode eksperimen kuantitatif & alur R&D) | **Sesuai.** |
| `[22]` | Darwin et al. (2021), *Metode Penelitian Pendekatan Kuantitatif* | Ada (`03-referensi/ebook-metodologi/Darwin 2021...pdf`) | L65 (pengumpulan teks memakai studi dokumentasi) | **Sesuai.** (Bab 9 hlm. 162 membahas *penelusuran data sekunder atau penelaahan dokumentasi*). |
| `[23]` | Sugiyono (2019), *Statistika untuk Penelitian* | Ada (`03-referensi/ebook-metodologi/Sugiyono 2019...pdf`, PDF pindaian) | L83 (hipotesis kerja komparatif) | **Terarsip** (PDF non-OCR, diverifikasi ulang secara visual jika dikutip rinci di Bab II). |
| `[24]` | Sinambela (2021), *Metodologi Penelitian Kuantitatif* | Ada (`03-referensi/ebook-metodologi/Sinambela 2021...pdf`) | L83 (hipotesis kerja komparatif) | **Sesuai.** |

---

## 4. Hasil Pemeriksaan Kepatuhan Pedoman UNSIA 2024 (Pasca-Revisi 24 November 2026)

1. **`validate_unsia.py`:**
   - `00-bagian-awal.md`: **`53` blok, `0 ERROR`, `0 WARNING`** (`[OK] Lulus`).
   - `01-bab-1-pendahuluan.md`: **`40` blok, sitasi unik `[1]`–`[24]` berurutan, `0 ERROR`, `0 WARNING`** (`[OK] Lulus`).
2. **Abstrak & *Abstract* (`00-bagian-awal.md` L68–L78):**
   - `ABSTRAK`: **183 kata** (batas ≤200), **1 paragraf**, 5 kata kunci urut abjad (`Deteksi Phishing, Otoritas Perpajakan, Random Forest, Support Vector Machine, TF-IDF`).
   - `ABSTRACT`: **183 kata** (batas ≤200), **1 paragraf**, 5 *keywords* urut abjad (`Phishing Detection, Random Forest, Support Vector Machine, Tax Authority, TF-IDF`).
   - Angka hasil di L70 & L76 dijaga utuh dan **ditandai untuk diverifikasi ulang pada sesi Bab IV**.
3. **Bagian Awal Lain (`00-bagian-awal.md`):**
   - Cover, Pernyataan Orisinalitas (4 kata `saya` sah sesuai templat hukum), Halaman Pengesahan, serta Kata Pengantar (`penulis`, 0 kata `saya`) telah sesuai keputusan pengguna.
   - Daftar Isi/Gambar/Tabel memuat nomor halaman statis (`i–xi`, `1–41`) yang dijadwalkan untuk sinkronisasi akhir pada kompilasi `.docx`/`.pdf` setelah Bab II–V selesai.
4. **Bab I Pendahuluan (`01-bab-1-pendahuluan.md`):**
   - `1.2 Rumusan Masalah`: Butir `a)`, `b)`, dan `c)` berbentuk pernyataan sebab-akibat/kelemahan sistem.
   - `1.4 Tujuan Penelitian`: Memakai kata kerja terukur (`Menyusun`, `Menguji dan membandingkan`, `Merancang, membangun, dan menguji`), bebas dari kata `mengetahui`, `melihat`, dan `memahami`.
   - `Tabel 1.1` & `Gambar 1.1`: Format caption, sumber olahan, serta aset gambar di `06-naskah-ta/aset-gambar/` terverifikasi ada.

---

## 5. Audit Narasi S1 Sistem Informasi dan Metrik Gaya (`humanizer-indonesia`)

1. **Sudut Pandang S1 Sistem Informasi:** Subbab `1.1–1.6` menyoroti ancaman pada layanan publik digital DJP (`coretaxdjp`, `M-Pajak`, siaran WhatsApp resmi), erosi kepercayaan wajib pajak, serta hambatan penyalinan manual yang melandasi perancangan purwarupa terintegrasi TKT Level 6 (FastAPI + web *Cek Pesan Pajak* + ekstensi *WhatsApp Web*) dengan penjelas kata pemicu berbahasa awam.
2. **Hasil `humanizer-indonesia/scripts/metrik.py --preset akademik`:**
   - `00-bagian-awal.md`: **9/9 LULUS** (`50` kalimat, `836` kata, rerata `16,7` kata, SD `6,6`, kalimat ≥28 kata `8,0%`, konektor `0,24/100` kata, verba ringan `0,00`, `merupakan` `1,20/1k`, *em/en-dash* `0`, pemadat `51,4/1k`).
   - `01-bab-1-pendahuluan.md`: **9/9 LULUS** (`72` kalimat, `1.357` kata, rerata `18,8` kata, SD `6,4`, kalimat ≥28 kata `9,7%`, konektor `0,15/100` kata, verba ringan `0,00`, `merupakan` `0,00`, *em/en-dash* `0`, triplet `3` / `2,21` per 1k kata, pemadat `47,9/1k`).
   - Pola kalimat penutup singkat simetris (*punchline* AI) pada L5, L7, L13, L15, dan L83 sudah dihilangkan atau dilebur ke alur argumen dengan tetap menjaga variasi panjang kalimat (`SD = 6,4`).

---

## 6. Keputusan Pengguna & Daftar Temuan Audit 24 November 2026

**Keputusan Pengguna yang Dikonfirmasi (24 November 2026):**
1. **Sapaan & Gelar Dosen Pembimbing:** Tetap menggunakan **`Bapak Novi Dian Nathasia, S.Kom., M.M.S.I.`** (usulan ubah ke `Ibu` dibatalkan; gelar dipertahankan apa adanya).
2. **Dosen Pembimbing II:** Kolom `Dosen Pembimbing II` di Halaman Pengesahan (`00-bagian-awal.md` L61) dibiarkan kosong bertitik-titik sesuai keadaan sekarang.
3. **Revisi Prosa & Sitasi Bab I:** Disetujui untuk menerapkan perbaikan **K-02, K-03, S-01 s.d. S-04, serta M-01, M-02, dan M-04** beserta penyegaran prosa S1 Sistem Informasi.

| Kode | Prioritas | Berkas & Lokasi | Temuan & Ringkasan Perbaikan | Status |
| :---: | :---: | :--- | :--- | :---: |
| `K-01` | Kritis | `00-bagian-awal.md` L94 | Usulan ubah `Bapak` menjadi `Ibu` untuk Novi Dian Nathasia, S.Kom., M.M.S.I. dibatalkan karena pengguna mengonfirmasi beliau adalah **Bapak**. | **Dibatalkan (Keputusan Pengguna)** |
| `K-02` | Kritis | `01-bab-1-pendahuluan.md` L77 | `[9]` (Al Ghofany et al., 2022) memakai *stemming* Nazief & Adriani, bukan Sastrawi. Diluruskan menjadi memakai Sastrawi mengikuti `[15]` yang berakar pada algoritma *stemming* Indonesia `[9]`. | **Selesai** |
| `K-03` | Kritis | `01-bab-1-pendahuluan.md` L5, L7 | Memisahkan atribusi `coretaxdjp`/`M-Pajak` (`[1], [2], [3]`) dan menarik contoh `coretax-online`, `kode billing`, serta `EFIN` sebagai temuan studi dokumentasi 68 arsip publik (bukan diklaim tercantum di PDF `[2], [5]`). | **Selesai** |
| `S-01` | Sedang | `01-bab-1-pendahuluan.md` L65 | Mengoreksi klaim `130 siaran resmi dari 10 layanan` menjadi `130 pesan aman pada 10 kategori siaran resmi maupun percakapan administrasi perpajakan` sesuai `Dataset Pajak Terkurasi 260 Baris.csv` (8 `Resmi_*` = 110; 2 `Normal_*` = 20). | **Selesai** |
| `S-02` | Sedang | `01-bab-1-pendahuluan.md` L9, L77 | Memisahkan `[13]` (korpus pesan singkat publik UCI 5.572 SMS) dari studi surel *phishing* `[12]`, serta memisahkan `[10], [13]` (TF-IDF umum) dari parameter desain `3.000 fitur`. | **Selesai** |
| `S-03` | Sedang | `01-bab-1-pendahuluan.md` L11 | Meluruskan deskripsi pembersihan URL dan karakter nonhuruf pada `[6], [13]` serta memperjelas bahwa `[16]` membuktikan kemiripan kosakata pada **pesan promosi resmi**. | **Selesai** |
| `S-04` | Sedang | `01-bab-1-pendahuluan.md` L5–L15, L83 | Menghilangkan lima kalimat penutup pendek bergaya *punchline* AI sembari menjaga variasi panjang kalimat (`SD 6,4`, 9/9 LULUS `metrik.py`) dan alur Sistem Informasi. | **Selesai** |
| `S-05` | Sedang | `00-bagian-awal.md` L61, L70–76, L112–203 | Pembimbing II & gelar dipertahankan; nomor halaman statis Daftar Awal dijadwalkan untuk sinkronisasi build akhir `.docx`; angka hasil Abstrak tetap bertanda **verifikasi Bab IV**. | **Terkunci / Terjadwal** |
| `M-01` | Minor | `01-bab-1-pendahuluan.md` L25 | Menajamkan Rumusan Masalah butir `c)` ke bentuk sebab-akibat langsung. | **Selesai** |
| `M-02` | Minor | `01-bab-1-pendahuluan.md` L5, L7, L11, L81 | Menyeragamkan penulisan `WhatsApp` tegak dan `*WhatsApp Web*` miring; format caption `Gambar 1.1 Tahapan Metode Penelitian.` selaras dengan `Gambar 2.1` di Bab II. | **Selesai** |
| `M-03` | Minor | `00-bagian-awal.md` L70, L76 | Catatan ejaan `ROC-AUC` di Abstrak ditinjau ulang bersama verifikasi angka hasil pada sesi Bab IV. | **Terjadwal (Sesi Bab IV)** |
| `M-04` | Minor | `03-referensi/catatan-kebaruan-dan-daftar-referensi.md` L99 | Memperbaiki `L. H. Almazaydeh` menjadi `L. Almazaydeh` agar sinkron dengan PDF `[12]` dan `06-lampiran.md` L25. | **Selesai** |
| `M-05` | Minor | `00-bagian-awal.md` L23–35 | Empat kata `saya` pada Pernyataan Orisinalitas merupakan naskah hukum baku UNSIA sehingga tetap dipertahankan. | **Diterima (Bukan Kesalahan)** |

---

## 7. Catatan Riwayat Audit Awal (22 November 2026)

Audit awal 22 November 2026 sebelumnya merapikan struktur sitasi dari `[1]`–`[31]` menjadi `[1]`–`[24]` (total Daftar Pustaka akhir `[1]`–`[36]`), menghapus 7 referensi sekunder, memindahkan angka hasil eksperimen akhir dari Subbab `1.6` ke Bab IV, serta memverifikasi kelengkapan PDF/Zotero (`35`→`36` sumber setelah penambahan `[36]` Saragih pada audit Bab II/III). Seluruh pembaruan di Bagian 1–6 di atas menjadi rujukan terkunci Bab I untuk audit Bab II–V selanjutnya.

---

# Log Audit Bab II Landasan Metode dan Lampiran Terkait

**Status:** Revisi Bab II, Lampiran 1–2, Daftar Pustaka `[1]`–`[36]`, Gambar 2.1, dan Zotero Selesai Diverifikasi  
**Tanggal Audit:** 22 November 2026  
**Program Studi:** S1 PJJ Sistem Informasi, Universitas Siber Asia (UNSIA)  
**Skema Tugas Akhir:** *Prototype* (Target Kesiapterapan TKT Level 6)

---

## 9. Ruang Lingkup Audit Bab II dan Lampiran Terkait

Audit Bab II meninjau empat aspek secara baca-saja (*read-only*): validitas referensi `[1]`–`[35]` dan Matriks Penelitian Terdahulu (`Tabel L.1`) terhadap sumber asli, kebenaran rumus dan kesesuaian konsep teknis dengan kode serta definisi operasional (`Tabel L.2`–`L.4`), kepatuhan terhadap Pedoman TA UNSIA 2024 dan perspektif S1 Sistem Informasi, serta pencatatan temuan berprioritas (`K2`, `S2`, `M2`).

**Berkas utama yang diaudit:**
1. `06-naskah-ta/md/02-bab-2-landasan-metode/02-bab-2-landasan-metode.md` (85 baris)
2. `06-naskah-ta/aset-gambar/Gambar 2.1 Bagan Alir Prosedur Eksperimen.png`
3. `06-naskah-ta/md/06-lampiran/06-lampiran.md` (Daftar Pustaka `[1]`–`[35]`, Lampiran 1 `Tabel L.1`, Lampiran 2 `Tabel L.2`–`L.4`)

**Berkas pembanding dan instrumen verifikasi:**
1. `01-administrasi/pedoman-penulisan-ta-unsia-2024.pdf` (hlm. 9–11, 23–27, 30–35)
2. Berkas PDF lokal di `03-referensi/daftar-pustaka/` (`03`, `06`, `08`, `09`, `10`, `11`, `12`, `13`, `14`, `15`, `16`, `18`, `19`, `25`, `26`, `28`, `31`, `33`, `35`), verifikasi daring (`[7]`, `[17]`, `[29]`, `[34]`), dan koleksi Zotero `6WSLSX4K` (35 item)
3. Kode sumber dan luaran eksperimen: `ml/eksperimen_baseline.py`, `ml/eksperimen_komparasi.py`, `pyproject.toml`, `04-dataset/readme-dataset.md`, `05-hasil-evaluasi/json/ringkasan_eksperimen_lengkap.json`, serta lingkungan `.venv`
4. Skrip `validate_unsia.py` dan `humanizer-indonesia/scripts/metrik.py --preset akademik`

---

## 10. Ringkasan Verifikasi Referensi dan Matriks Penelitian Terdahulu (Tabel L.1)

Pencocokan langsung naskah Bab II dan `Tabel L.1` terhadap PDF asli, metadata Zotero, serta penelusuran daring menemukan sejumlah salah atribusi, angka metrik yang kurang tepat, serta ketimpangan cakupan antara narasi dan tabel:

1. **`[8]` Irawan et al. (2021, PDF hlm. 436):** Dikelompokkan secara keliru bersama `[9]` di baris 5 Bab II untuk klaim *stemming* Nazief-Adriani, TF-IDF, 500 SMS pribadi, dan akurasi `99,52%`. Pada PDF aslinya, `[8]` memakai **5.571 SMS berbahasa Inggris** dari UCI (`4.824` *ham*, `747` *spam*) tanpa Nazief-Adriani, dan performa **SVM paling rendah (`86,5%`)** di bawah *Bagging* (`97,4%`), *Random Forest* (`96,8%`), dan *Naïve Bayes* (`96,4%`). Referensi `[8]` juga tidak masuk ke `Tabel L.1`.
2. **`[9]` Al Ghofany et al. (2022, Fig. 5 hlm. 127):** Memang meneliti 500 SMS pribadi memakai Nazief-Adriani dan TF-IDF (*Linear* SVM `99,52%`, *Sigmoid* SVM `99,60%`, TF-RF `100%`). Klaim pada baris 5 Bab II seharusnya merujuk `[9]` secara terpisah dari `[8]`.
3. **`[11]` Tampinongkol et al. (2024, PDF hlm. 130–135):** Tercantum di baris 7 Bab II dalam perbandingan TF-IDF dan SVM/RF terhadap BERT. Faktanya `[11]` mengklasifikasikan **59.899 URL *phishing*** dengan **9 fitur leksikal URL** (`Random Forest` `84,95%` mengungguli `SVM` `77,43%`), tanpa TF-IDF dan tanpa BERT.
4. **`[12]` Al Tawil et al. (2024, PDF hlm. 3404–3409):** Membandingkan TF-IDF dan *Word2Vec* dengan BERT (`1.012,66` detik vs RF `40,39` detik) pada `18.650` surel berbahasa Inggris memakai LR, DT, RF, MLP, dan BERT, tetapi **tidak menguji SVM**. Selain itu, Daftar Pustaka masih menulis inisial `L. H. Almazaydeh`, sedangkan PDF asli (hlm. 3395) menulis **`Laiali Almazaydeh`**.
5. **`[14]` Efendi et al. (2025):** Nilai rentang `0,55`–`0,83` pada `Tabel L.1` hanya berasal dari 3 pesan *phishing* yang diuji (sedangkan 2 pesan aman memperoleh skor `0,18`–`0,35`).
6. **`[15]` Saputra et al. (2026):** Kepala PDF mencetak DOI templat salah (`10.36595/misi.v5i2`), sedangkan Daftar Pustaka mencantumkan `10.36595/misi.v9i1.1803`; keaktifan DOI perlu dikonfirmasi saat tahap revisi.
7. **`[16]` Sembiring et al. (2025):** Angka `0,9859` yang tertulis di `Tabel L.1` adalah *Recall* **kelas *fraud*** (bukan *macro recall*); pada makalah aslinya, SVM mencapai Akurasi `96,98%` dan *F1-macro* `96,34%`, sementara MNB mencatat *F1-macro* tertinggi `96,93%`.
8. **`[17]` Mishra & Yadav (2026) dan `[19]` Suwarno et al. (2026):** Digabungkan pada satu baris di `Tabel L.1` tanpa angka metrik penelitiannya, padahal keduanya memiliki metrik yang jelas (`[17]`: `5.572` SMS, `LinearSVC` Akurasi `98,57%`, *F1-Score* `94,44%`, SHAP; `[19]`: `235.370`/`235.795` URL, *Logistic Regression* Akurasi `99,53%`, SUS `81%`).
9. **Ketidakcocokan jumlah `Tabel L.1` dengan narasi:** Baris 9 Bab II menyatakan terdapat **"12 studi terdahulu"** pada `Tabel L.1`, sedangkan `Tabel L.1` memuat 12 baris yang menggabungkan 13 sitasi dan tidak menyertakan `[8]` maupun `[18]` Ismail et al. (2026) yang dibahas di Subbab 2.1.
10. **Korpus tanpa sitasi (`Saragih`):** Korpus `Saragih 2024 Korpus SMS Spam Indo.csv` disebut pada baris 81 Bab II dan `Tabel L.3` baris 125 tanpa nomor sitasi `[n]` maupun entri di Daftar Pustaka.
11. **Metadata Zotero `[34]`:** Entri Permenristekdikti No. 42 Tahun 2016 (`22KIVB7F`) pada koleksi Zotero masih berjudul `(untitled)`.

---

## 11. Ringkasan Verifikasi Rumus Matematis, Konsep Teknis, dan Kesesuaian Kode

### 11.1 Persamaan Matematis (2.1)–(2.8)
1. **Inkonsistensi notasi antar-persamaan:**
   - Label kelas $y_i$ berpindah secara implisit dari $\{-1, +1\}$ (baris 15 dan Persamaan 2.1) menjadi $\{0, 1\}$ (Persamaan 2.8) tanpa penjelasan konversi label.
   - Simbol $N$ dipakai ganda untuk dua besaran berbeda (jumlah dokumen korpus pada Persamaan 2.5 vs jumlah sampel uji pada Persamaan 2.8).
   - Notasi $\mathbf{v}(d)$ pada Persamaan 2.5 belum didefinisikan; penulisan logaritma tidak seragam ($\ln$ pada Persamaan 2.5 vs $\log$ pada Persamaan 2.8); Persamaan 2.4 memakai indeks huruf Yunani $\sum_\beta$ alih-alih indeks pohon $b = 1, \dots, B$.
   - Persamaan (2.1) perlu ditegaskan sebagai formulasi *L2-regularized L2-loss* (*squared hinge*) sesuai `LinearSVC` serta mendefinisikan seluruh peubah ($\mathbf{w}, b, \mathbf{x}_i, C, i = 1, \dots, n$).
2. **Atribusi implementasi `scikit-learn` `[33]`:** Persamaan (2.4) (perataan peluang `predict_proba` pohon) dan Persamaan (2.5) (TF-IDF halus $\ln((1+N)/(1+\mathrm{df}))+1$ beserta normalisasi L2) merupakan implementasi pustaka `scikit-learn` `[33]` yang memodifikasi rancangan awal Breiman `[28]` (pemungutan suara mayoritas) dan Salton & Buckley `[29]`, sehingga `[33]` wajib disitasi pada kedua bagian tersebut.
3. **Salah atribusi optimasi Newton `[35]` dan pengelompokan metrik (baris 39):** Optimasi Newton dengan *backtracking line search* pada Lin et al. `[35]` (PDF hlm. 268–269) menaksir parameter $(A, B)$ dalam fungsi sigmoid kalibrasi Platt (**Persamaan 2.2**), bukan menghitung *Brier Score* dan *Log Loss* (**Persamaan 2.8**). Pada kalimat yang sama, *ROC-AUC* dan *PR-AUC* keliru dikelompokkan sebagai metrik kalibrasi peluang, padahal keduanya adalah metrik diskriminasi/pemeringkatan berbasis ambang batas.

### 11.2 Kesesuaian Kode (`ml/`) dan Lingkungan Aktual (`.venv`)
1. **Ruang pencarian *grid* (`Tabel L.4` baris 137 vs `ml/eksperimen_komparasi.py`):** Kode `ml/eksperimen_komparasi.py` (baris 347–358) dan `ringkasan_eksperimen_lengkap.json` (baris 133) menguji **`36` kombinasi** (`12` kombinasi `LinearSVC` + `24` kombinasi `Random Forest`). Pada `Tabel L.4` baris 137, parameter `class_weight {None, "balanced"}` untuk *Random Forest* tertinggal sehingga terbaca `12 + 12 = 24` kombinasi. Penyebutan `GridSearchCV` pada `Tabel L.2` dan `Gambar 2.1` juga kurang presisi karena implementasi aktual memakai fungsi pencarian *grid* terisolasi per lipatan (`_run_grid_over_folds`) guna mencegah kebocoran TF-IDF.
2. **Aturan praproses `clean_text` dan *stemming* Sastrawi:** Pada `ml/eksperimen_baseline.py` (baris 46–63), regex `[^a-z0-9\s_]` mempertahankan angka dan garis bawah, sementara *stemming* Sastrawi hanya diterapkan pada token alfabetis sepanjang lebih dari dua huruf (`len > 2`), sedangkan token numerik dan token `<= 2` huruf dipertahankan. Rincian ini belum tergambar akurat di baris 33 Bab II maupun `Tabel L.4` baris 133.
3. **Versi perangkat lunak (Subbab 2.5 dan `Tabel L.3` vs `.venv`):** Naskah masih mencantumkan `Python 3.11.9`, `NumPy 2.4.6`, serta tidak mencantumkan versi `SHAP` dan `FastAPI`. Versi terpasang pada `.venv` proyek adalah **`Python 3.14.7`, `Scikit-learn 1.9.1`, `Pandas 3.1.1`, `NumPy 2.5.4`, `Matplotlib 3.11.2`, `SHAP 0.54.1`, `Joblib 1.6.0`, `FastAPI 0.163.1`, `Pytest 9.2.0`, dan `Sastrawi 1.0.1`**.
4. **Jalur berkas sistem (`Tabel L.3` baris 121):** Masih menuliskan jalur lama (`api.py`, `web/`) alih-alih struktur repositori saat ini (`app/backend/api.py`, `app/frontend/`, `app/extension/`). *(Catatan titipan untuk audit Bab III: `Tabel L.5` juga terpantau masih memakai jalur lama `src/` dan `06 Prototipe Aplikasi/`.)*
5. **Pemuatan angka hasil eksperimen akhir di Bab II:** Angka hasil akhir masih muncul sebelum Bab IV pada `Tabel L.1` baris *"Penelitian Ini"* (`42,22% -> 95,56%`), `Gambar 2.1` Kotak 4 (`C = 2,0`, `100 pohon`), dan Subbab 2.5 baris 75 (`189,36` detik). Hal ini bertentangan dengan disiplin pembagian bab yang sudah ditetapkan pada revisi Bab I (`K-05`).

---

## 12. Kepatuhan Pedoman UNSIA 2024, Gaya Bahasa, dan Perspektif S1 Sistem Informasi

### 12.1 Hasil `validate_unsia.py` pada `02-bab-2-landasan-metode.md`
- **Total blok diperiksa:** `43` blok; sitasi unik terdeteksi: `[1]`–`[35]`.
- **`ERROR` (`1` positif palsu):** Skrip melaporkan belum ada Daftar Pustaka karena `02-bab-2-landasan-metode.md` diperiksa terpisah dari `06-lampiran.md`.
- **`WARNING` (`2` butir):**
  1. `[P8]` (baris 15, pengantar Persamaan 2.1): `44` kata (~3,7 baris), di bawah rentang `5–7` baris Pedoman UNSIA 4.2.d.
  2. `[P21]` (baris 41, baris persamaan terpisah): `23` kata (peringatan heuristik panjang blok rumus).
- **Catatan format Pedoman TA UNSIA 2024:** Subbab `2.4` (`50` kata) dan `2.5` (`49` kata) tergolong ringkas dan perlu diperjelas secara operasional; judul atau keterangan persamaan perlu diletakkan rata tengah di atas persamaan sesuai Pedoman 4.2.h; tautan `Gambar 2.1` di baris 65 masih memakai jalur lama `Aset Gambar/...`.

### 12.2 Hasil `humanizer-indonesia/scripts/metrik.py` (Preset `akademik`)
- **Metrik inti:** **9/9 LULUS** (`61` kalimat, `1.094` kata, rerata `17,9` kata/kalimat, simpangan baku `9,7`, kalimat $\ge 28$ kata `9,8%`, *em-dash* `0`, penghubung `0,18` per 100 kata).
- **Catatan gaya bahasa:** Kepadatan kata pemadat (*filler*/penghubung) sangat rendah (`21,0` per `1.000` kata vs pita wajar `73`–`139`) sehingga alur antar-subtopik terasa melompat; tercatat `7` pola *triplet* (`6,40` per `1.000` kata) serta sisa istilah dan kalke yang belum diselaraskan dengan Bab I (`melawan`, `mengadu`, `Mutu prediksi`, `kata henti`, `menstem`, `Penalaan parameter`).

### 12.3 Evaluasi Perspektif S1 Sistem Informasi
Bab II sudah menyajikan landasan operasional yang kuat dari sisi rekayasa pembelajaran mesin, tetapi porsi **Sistem Informasi** dan **rancangan purwarupa TA *Prototype*** (Pedoman UNSIA hlm. 27) belum seimbang:
1. Kriteria operasional **TKT Level 6** dan target kelayakan fungsional/non-fungsional purwarupa (`<100` ms latensi inferensi, verifikasi daftar putih `pajak.go.id`, penjelasan indikator pemicu berbahasa awam bagi wajib pajak) masih tertumpuk bersama definisi metrik evaluasi dan skenario uji kontrol di Subbab `2.2.4`. Pemisahan menjadi Subbab `2.2.5` akan memperjelas keterkaitan model dengan sistem verifikasi terpadu.
2. Pada Subbab `2.6` baris 79, pengecualian 3 dari 68 sumber publik (`65` terpakai; selisih `SRC-046`, `SRC-049`, `SRC-061`) belum dijelaskan alasannya, dan rentang tahun korpus pajak (`2021–2026`) belum diselaraskan dengan hasil revisi Bab I (`K-03`).

---

## 13. Daftar Temuan Berprioritas dan Usulan Revisi Konkret

| Kode | Tingkat | Lokasi | Inti Temuan & Bukti Audit | Usulan Revisi Konkret |
| :---: | :---: | :--- | :--- | :--- |
| `K2-01` | **Kritis** | Bab II L5, L7 | Salah atribusi fakta pada `[8]` (5.571 SMS Inggris, tanpa Nazief-Adriani, SVM terendah 86,5% vs Bagging 97,4%), `[11]` (59.899 URL, 9 fitur leksikal, tanpa TF-IDF/BERT), dan `[12]` (18.650 surel, tidak menguji SVM). | Pisahkan `[8]` dari klaim `[9]`; pindahkan `[11]` ke pembanding fitur leksikal URL; perbaiki uraian `[12]` agar hanya menyebut model yang benar-benar diuji (`LR`, `DT`, `RF`, `MLP`, `BERT`). |
| `K2-02` | **Kritis** | Bab II L9, L39, L79 | Salah tempat sitasi: `[17], [21]–[23]` ikut dirujuk sebagai pedoman TA/TKT di L9; optimasi Newton `[35]` (Lin et al., 2007) di L39 ditempelkan ke Pers. (2.8) serta ROC-AUC/PR-AUC disebut metrik kalibrasi; `[23], [24]` dirujuk untuk pencegahan kebocoran TF-IDF di L79. | Batasi rujukan Pedoman UNSIA & TKT ke `[20], [34]`; hubungkan `[35]` ke Pers. (2.2) kalibrasi Platt dan bedakan metrik diskriminasi vs kalibrasi; alihkan rujukan pencegahan kebocoran data TF-IDF ke `[31], [33]`. |
| `K2-03` | **Kritis** | Bab II L15–L45 (Pers. 2.1–2.8) | Label $y_i$ berubah implisit ($\{-1,+1\} \to \{0,1\}$); $N$ dipakai ganda; $\mathbf{v}(d)$ tidak didefinisikan; $\ln$ vs $\log$ campur; $\sum_\beta$ salah indeks pohon; Pers. (2.1) belum menegaskan *L2-loss*; Pers. (2.4) dan (2.5) tidak menyitasi `[33]` (`scikit-learn`). | Selaraskan notasi ($N_{\text{dok}}$ vs $N_{\text{uji}}$, indeks $b = 1 \dots B$, definisikan $\mathbf{w}, b, \mathbf{x}_i, C, \mathbf{v}(d)$); jelaskan transisi label biner untuk kalibrasi; tegaskan formulasi *L2-regularized L2-loss* dan tambahkan sitasi `[33]` pada Pers. (2.4)–(2.5). |
| `K2-04` | **Kritis** | Bab II L33, L57, L75, L81; `Tabel L.3`–`L.4` | `Tabel L.4` L137 menghilangkan `class_weight` RF (grid tertulis 24, aktual kode `36`); versi Subbab 2.5 & `Tabel L.3` (`Python 3.11.9`, `NumPy 2.4.6`) tidak cocok dengan `.venv`; korpus `Saragih` belum bersitasi `[n]`; deskripsi `clean_text`/Sastrawi belum menyebut pelestarian angka/garis bawah dan syarat `len > 2`. | Perbaiki rincian grid RF menjadi 24 kombinasi (total 36); selaraskan versi ke `.venv` aktual; tambah sitasi `[36]` Saragih (2024); jelaskan aturan `[^a-z0-9\s_]` serta *stemming* Sastrawi pada token alfabetis `len > 2`. |
| `K2-05` | **Kritis** | Bab II L9, L75; `Tabel L.1`; `Gambar 2.1` | `Tabel L.1` menyebut "12 studi" padahal 12 baris memuat 13 sitasi dan absen `[8]`, `[18]`; metrik `[14]`, `[16]`, `[17]`, `[19]` tidak akurat/kosong; hasil akhir (`42,22%->95,56%`, `C=2,0`, `100 pohon`, `189,36 detik`) muncul prematur di Bab II & `Tabel L.1`. | Lengkapi `Tabel L.1` (masukkan `[8]` & `[18]`, perbaiki metrik `[14]`, `[16]`, pisah baris `[17]` dan `[19]`) dan samakan jumlah studi di narasi L9; keluarkan seluruh angka hasil akhir serta parameter pemenang ke Bab IV. |
| `S2-01` | **Sedang** | Bab II L65; `Gambar 2.1` | Tautan gambar memakai `Aset Gambar/...`; `Gambar 2.1` menempatkan deduplikasi sebelum praproses, judul Kotak 3 mendahulukan TF-IDF sebelum *split*, serta Kotak 4 mencantumkan `GridSearchCV` dan parameter pemenang. | Ubah tautan menjadi `../../aset-gambar/Gambar 2.1 Bagan Alir Prosedur Eksperimen.png` dan buat ulang `Gambar 2.1` dengan urutan alur eksperimen aktual tanpa parameter pemenang prematur. |
| `S2-02` | **Sedang** | `Tabel L.2` L109–L110 | Baris 5 (pengujian TKT 6) berstatus `Berjalan` pada Nov 2026, padahal Baris 6 (penyusunan laporan lengkap Bab I–V) berstatus `Selesai` di bulan yang sama. | Selaraskan status dan lini masa pada `Tabel L.2` agar urutan penyelesaian kegiatan logis. |
| `S2-03` | **Sedang** | `Tabel L.3` L121 | Jalur perangkat lunak masih memakai nama lama `api.py` dan `web/`. | Perbarui ke struktur aktual `app/backend/api.py`, `app/frontend/`, dan `app/extension/` (catat juga `Tabel L.5` untuk audit Bab III). |
| `S2-04` | **Sedang** | Bab II L15, L41, L67–L75 | `validate_unsia.py` mencatat `WARNING` pada `[P8]` (44 kata) dan `[P21]` (23 kata); Subbab 2.4–2.5 singkat; penempatan judul persamaan belum mengikuti Pedoman 4.2.h (rata tengah di atas rumus). | Kembangkan `[P8]` dan Subbab 2.4–2.5 ke 5–7 baris; gabungkan baris persamaan agar tidak memecah blok pendek dan tata keterangan persamaan sesuai Pedoman 4.2.h. |
| `S2-05` | **Sedang** | Bab II Subbab 2.2.4 & 2.6 | Aspek S1 Sistem Informasi dan target operasional TKT Level 6 (`<100 ms`, daftar putih `pajak.go.id`, penjelasan awam) tenggelam di dalam 2.2.4; 3 sumber tereksklusi (`SRC-046`, `SRC-049`, `SRC-061`) di Subbab 2.6 belum dijelaskan. | Pecah kriteria prototipe & TKT Level 6 ke Subbab `2.2.5`; cantumkan alasan eksplisit eksklusi 3 dari 68 arsip publik pada Subbab 2.6. |
| `S2-06` | **Sedang** | Seluruh Bab II | `metrik.py` mencatat kepadatan kata pemadat `21,0`/1.000 kata dan `7` *triplet*, serta sisa istilah lama (`melawan`, `mengadu`, `Mutu prediksi`, `kata henti`, `menstem`, `Penalaan parameter`). | Haluskan transisi antar-alinea agar tidak teleografis, kurangi deret tiga unsur berulang, dan selaraskan istilah dengan glosarium Bab I (`terhadap`, `kualitas prediksi`, `daftar kata umum`, `pemenggalan kata dasar`, `penyetelan hiperparameter`). |
| `S2-07` | **Sedang** | DP `[12]`, `[15]`, Zotero `[34]` | Zotero `[34]` (`22KIVB7F`) berjudul `(untitled)`; DP `[12]` menulis `L. H. Almazaydeh` (PDF: `Laiali Almazaydeh`); kepala PDF `[15]` dan DP memiliki DOI berbeda. | Lengkapi judul Zotero `[34]`; perbaiki `[12]` menjadi `L. Almazaydeh`; verifikasi DOI aktif `[15]` saat tahap revisi. |
| `M2-01` | **Minor** | Bab II L15–L45 | Penulisan simbol matematika mencampur sintaks LaTeX `$...$` dengan simbol Unicode. | Seragamkan notasi matematika ke format LaTeX konsisten di seluruh Bab II. |
| `M2-02` | **Minor** | Bab II L5–L81 | Penggunaan *backtick* tidak konsisten pada angka (`95,45%`, `927`, `232`), `Recall`, dan rujukan `Tabel L.1`–`L.4`. | Hapus *backtick* pada angka metrik dan rujukan tabel lampiran; pertahankan hanya untuk pengenal kode/token teknis. |
| `M2-03` | **Minor** | Bab II & Lampiran 1–2 | Istilah asing seperti *WhatsApp*, *default*, *split*, *unigram*, *bigram*, dan *Platt scaling* belum dicetak miring merata sesuai Pedoman 4.2.b. | Terapkan huruf miring secara konsisten pada seluruh kata asing non-kode. |
| `M2-04` | **Minor** | Bab II L79 | Rentang tahun arsip publik DJP pada Subbab 2.6 belum menyebut periode `2021–2026` seperti pada Bab I (`K-03`). | Selaraskan ke `2021–2026` (didominasi periode `2024–2026`). |
| `M2-05` | **Minor** | Bab II L39 | Subbab 2.2.4 memadatkan 4 bahasan terpisah (akurasi/F1, kalibrasi, *threshold*/uji bias, TKT 6) ke dalam satu paragraf padat. | Pecah ke Subbab `2.2.4` (Metrik Evaluasi & Kalibrasi) dan `2.2.5` (Indikator Kelayakan Purwarupa TKT Level 6). |
| `M2-06` | **Minor** | `Tabel L.2`, `Gambar 2.1` | Istilah `GridSearchCV` dipakai padahal kode memakai pencarian *grid* terisolasi (`_run_grid_over_folds`). | Ganti dengan istilah `pencarian grid 10-Fold CV terisolasi` agar akurat terhadap kode. |

---

## 14. Keputusan Pengguna yang Telah Dikonfirmasi (22 November 2026)

1. **Penambahan Referensi `[36]` Saragih (2024):** Disetujui untuk ditambahkan pada tahap revisi Bab II di Daftar Pustaka (`06-lampiran.md`), sitasi Bab II (baris 81) dan `Tabel L.3` (baris 125), serta koleksi Zotero `6WSLSX4K` dengan metadata: `S. C. Saragih, "Indonesian SMS Spam Classifier Dataset," GitHub Repository, 2024. [Daring]. Tersedia: https://github.com/Sctian514/Indonesian-sms-spam-classifier (Lisensi MIT)`.
2. **Penyelarasan Lingkungan Perangkat Lunak ke `.venv` Aktual:** Disetujui untuk menyelaraskan seluruh versi perangkat lunak pada Subbab 2.5 dan `Tabel L.3` dengan paket terpasang di `.venv`: `Python 3.14.7`, `Scikit-learn 1.9.1`, `Pandas 3.1.1`, `NumPy 2.5.4`, `Matplotlib 3.11.2`, `SHAP 0.54.1`, `Joblib 1.6.0`, `FastAPI 0.163.1`, `Pytest 9.2.0`, dan `Sastrawi 1.0.1`.
3. **Batas Eksekusi Tahap Ini:** Hanya memperbarui berkas `06-naskah-ta/log-review-ta.md`. Seluruh berkas naskah (`02-bab-2-landasan-metode.md`, `06-lampiran.md`, `Gambar 2.1`) serta pembaruan entri Zotero ditunda ke sesi eksekusi revisi berikutnya.

---

## 15. Daftar Periksa Eksekusi Revisi Bab II (Panduan Sesi Lanjutan)

Urutan kerja yang direkomendasikan untuk sesi berikutnya:
1. Sunting `06-naskah-ta/md/02-bab-2-landasan-metode/02-bab-2-landasan-metode.md` untuk menyelesaikan seluruh temuan `K2-01`–`K2-05`, `S2-01`, `S2-04`–`S2-06`, serta `M2-01`–`M2-05` (termasuk pemecahan Subbab `2.2.5`, perbaikan Persamaan 2.1–2.8, pembaruan versi `.venv`, penambahan sitasi `[36]`, dan penghapusan hasil akhir prematur).
2. Buat ulang `06-naskah-ta/aset-gambar/Gambar 2.1 Bagan Alir Prosedur Eksperimen.png` sesuai urutan praproses $\to$ deduplikasi $\to$ *split* 80:20 $\to$ 10-Fold CV TF-IDF terisolasi + pencarian *grid* (`_run_grid_over_folds`), bebas angka parameter pemenang prematur (`S2-01`, `M2-06`).
3. Sunting `06-naskah-ta/md/06-lampiran/06-lampiran.md`: perbaiki Daftar Pustaka `[12]`, cek DOI `[15]`, tambahkan `[36]` Saragih (2024), lengkapi dan koreksi `Tabel L.1` (`K2-05`), perbaiki status `Tabel L.2` (`S2-02`), selaraskan versi `.venv` dan jalur aktual di `Tabel L.3` (`K2-04`, `S2-03`), serta perbarui grid RF `24` kombinasi (`36` total) dan aturan `clean_text` di `Tabel L.4` (`K2-04`).
4. Perbarui koleksi Zotero `6WSLSX4K`: isi judul item `[34]` (`22KIVB7F`) dan tambahkan entri `[36]` Saragih (2024) (`S2-07`, Keputusan 1).
5. Jalankan `validate_unsia.py`, `humanizer-indonesia/scripts/metrik.py --preset akademik`, serta pemeriksaan keutuhan sitasi `[1]`–`[36]` lintas Bab I–V dan Lampiran, lalu tambahkan **Bagian 16 (Log Eksekusi Revisi Bab II)** ke `06-naskah-ta/log-review-ta.md`.

---

## 16. Log Eksekusi Revisi Bab II dan Lampiran Terkait

**Status Akhir Tahap Ini:** Seluruh revisi Bab II (`02-bab-2-landasan-metode.md`), Daftar Pustaka (`[1]`–`[36]`) dan Lampiran 1–2 (`06-lampiran.md`), bagan alir `Gambar 2.1 Bagan Alir Prosedur Eksperimen.png`, verifikasi DOI `[15]`, serta pembaruan koleksi Zotero `6WSLSX4K` telah dijalankan dan diverifikasi pada 22 November 2026.

### 16.1 Keputusan Pengguna yang Diterapkan
1. **Penambahan Referensi `[36]` Saragih (2024):** Ditambahkan sebagai entri `[36]` pada Daftar Pustaka di `06-lampiran.md`, dirujuk di Subbab 2.6 `02-bab-2-landasan-metode.md` dan `Tabel L.3`, serta dibuatkan item baru pada koleksi Zotero `6WSLSX4K` (`key: XXVECDHC`, `itemType: dataset`, Lisensi MIT).
2. **Penyelarasan Lingkungan Perangkat Lunak ke `.venv` Aktual:** Seluruh versi perangkat lunak pada Subbab 2.5 `02-bab-2-landasan-metode.md` dan `Tabel L.3` `06-lampiran.md` diselaraskan ke paket terpasang di `.venv`: `Python 3.14.7`, `Scikit-learn 1.9.1`, `Pandas 3.1.1`, `NumPy 2.5.4`, `Matplotlib 3.11.2`, `SHAP 0.54.1`, `Joblib 1.6.0`, `FastAPI 0.163.1`, `Pytest 9.2.0`, dan `Sastrawi 1.0.1`.

### 16.2 Status Penyelesaian Seluruh Temuan (`K2-01`–`K2-05`, `S2-01`–`S2-07`, `M2-01`–`M2-06`)

| Kode | Status | Ringkasan Perbaikan yang Diterapkan |
| :---: | :---: | :--- |
| `K2-01` | Selesai | Memisahkan `[8]` (5.571 SMS UCI bahasa Inggris tanpa pemenggalan kata dasar; SVM 86,5% di bawah *Bagging* 97,4%, RF 96,8%, NB 96,4%) dari `[9]`; memindahkan `[11]` (59.899 URL, 9 fitur leksikal, tanpa TF-IDF/BERT); meluruskan `[12]` (`LR`, `DT`, `RF`, `MLP`, `BERT` tanpa SVM); menegaskan angka 98,59% `[16]` sebagai *Recall* kelas *fraud* SVM. |
| `K2-02` | Selesai | Membatasi rujukan pedoman TA & TKT di 2.1 ke `[20], [34]`; menghubungkan optimasi Newton *backtracking line search* `[35]` ke Persamaan (2.2) kalibrasi Platt; memisahkan metrik diskriminasi (*ROC-AUC*, *PR-AUC* `[32]`) dari kalibrasi (*Brier Score*, *Log Loss* Persamaan 2.8 `[32], [33]`); mengalihkan pencegahan kebocoran data TF-IDF di 2.6 ke `[31], [33]`. |
| `K2-03` | Selesai | Menjelaskan konversi label $\{-1,+1\} \to \{0,1\}$ sebelum Persamaan (2.2); membedakan $N_{\text{dok}}$ (Persamaan 2.5) vs $N_{\text{uji}}$ (Persamaan 2.8); mengganti $\sum_\beta$ menjadi indeks $b=1,\dots,B$; menyeragamkan logaritma ke $\ln$; mendefinisikan semua peubah ($\mathbf{w}, b, \mathbf{x}_i, C, \mathbf{v}(d)$); menegaskan formulasi *L2-regularized L2-loss* pada Persamaan (2.1) dan menambahkan sitasi `[33]` pada Persamaan (2.4)–(2.5). |
| `K2-04` | Selesai | Melengkapi parameter *Random Forest* di `Tabel L.4` dengan `class_weight {None, "balanced"}` (`24` konfigurasi RF + `12` konfigurasi `LinearSVC` = `36` kandidat); menyelaraskan versi perangkat lunak Bab II & `Tabel L.3` ke `.venv`; menambahkan `[36]` Saragih (2024); mendeskripsikan aturan `clean_text` (`[^a-z0-9\s_]` serta Sastrawi `len > 2` untuk token alfabetis). |
| `K2-05` | Selesai | Melengkapi `Tabel L.1` menjadi 15 studi terdahulu (`[3]`, `[6]`–`[19]`) + baris Penelitian Ini (menambah `[8]`, `[18]`, memisahkan `[17]` & `[19]`, memperbaiki `[14]` & `[16]`); menyamakan narasi Subbab 2.1 ke 15 studi; menghapus seluruh angka hasil akhir dan parameter pemenang prematur (`189,36` detik, `C=2,0`, `100 pohon`, `42,22%->95,56%`) dari Bab II, `Tabel L.1`, dan `Gambar 2.1`. |
| `S2-01` | Selesai | Memperbarui tautan gambar di 2.3 ke `../../aset-gambar/Gambar 2.1 Bagan Alir Prosedur Eksperimen.png` dan membuat ulang `Gambar 2.1` (`2160 x 990` piksel) sesuai urutan aktual (kurasi $\to$ praproses & deduplikasi $\to$ *split* 80:20 & TF-IDF terisolasi $\to$ penyetelan *grid* 10-Fold CV + kalibrasi Platt $\to$ evaluasi & lintas-korpus $\to$ ekspor purwarupa TKT 6). |
| `S2-02` | Selesai | Menyelaraskan status baris 5 `Tabel L.2` (*Perancangan arsitektur purwarupa TKT 6 dan pengujian sistem*) menjadi `Berjalan` pada Oktober 2026 dan `Selesai` pada November 2026. |
| `S2-03` | Selesai | Memperbarui jalur komponen purwarupa pada `Tabel L.3` menjadi `app/backend/api.py`, `app/frontend/`, dan `app/extension/`. |
| `S2-04` | Selesai | Mengembangkan alinea pengantar 2.2.1, 2.4, dan 2.5 ke rentang 5–7 baris Pedoman UNSIA 4.2.d serta meletakkan judul Persamaan (2.1)–(2.8) di atas blok `$$...$$` sehingga `validate_unsia.py` mencatat `0 WARNING`. |
| `S2-05` | Selesai | Memecah target operasional TKT Level 6 (`<100` ms, daftar putih `pajak.go.id`, penjelasan awam berbasis bobot fitur & SHAP) ke Subbab baru `2.2.5`, dan menambahkan alasan eksplisit pengecualian `SRC-046`, `SRC-049`, dan `SRC-061` di Subbab 2.6 (artikel sekunder DDTC News/Ortax yang merangkum pengumuman primer DJP dari `pajak.go.id`). |
| `S2-06` | Selesai | Menghaluskan transisi antar-kalimat, menghilangkan kalke/istilah lama (`melawan`, `mengadu`, `Mutu prediksi`, `kata henti`, `menstem`, `Penalaan parameter`), menurunkan *triplet* prosa menjadi `0` (`1` positif palsu pada baris rumus Persamaan 2.6), serta menjaga `9/9` metrik gaya lulus. |
| `S2-07` | Selesai | Mengubah `22KIVB7F` (`[34]`) di Zotero ke `itemType: report` berjudulkan lengkap (`version: 52`, `numChildren: 1`); memperbaiki penulis kedua `[12]` menjadi `L. Almazaydeh` di DP dan `Laiali Almazaydeh` pada `TDNR9QKL` di Zotero (`version: 54`); memverifikasi DOI aktif `[15]`. |
| `M2-01`–`M2-06` | Selesai | Menyeragamkan seluruh notasi rumus Bab II ke LaTeX; menghapus *backtick* pada angka metrik dan rujukan `Tabel L.1`–`L.4`; menyeragamkan cetak miring istilah asing non-kode di Bab II dan Lampiran 1–2; menyelaraskan rentang arsip `2021–2026` di 2.6 dan `Tabel L.3`; mengganti istilah `GridSearchCV` dengan `pencarian grid 10-Fold CV terisolasi` pada Subbab 2.3, `Tabel L.2`, `Tabel L.4`, dan `Gambar 2.1`. |

### 16.3 Pembaruan Referensi, Verifikasi DOI `[15]`, dan Koleksi Zotero (`[1]`–`[36]`)
1. **Verifikasi DOI `[15]` (Saputra dkk., 2026):** Pemeriksaan langsung ke `https://doi.org/api/handles/10.36595/misi.v9i1.1803` dan `https://api.crossref.org/works/10.36595/misi.v9i1.1803` mengembalikan status `200 OK` yang mengarah aktif ke artikel `http://e-journal.stmiklombok.ac.id/index.php/misi/article/view/1803` terbitan STMIK Lombok (sedangkan `10.36595/misi.v5i2` pada kepala PDF terbukti DOI templat isu tahun 2023). Daftar Pustaka `[15]` tetap memakai `10.36595/misi.v9i1.1803`.
2. **Pembaruan Item `[12]` & `[34]` dan Penambahan `[36]` di Zotero (`6WSLSX4K`):**
   - Item `[34]` (`22KIVB7F`): diperbarui dari `statute` tidak berjudul menjadi `report` berjudul lengkap (*Peraturan Menteri Riset, Teknologi, dan Pendidikan Tinggi Nomor 42 Tahun 2016 tentang Pengukuran dan Penetapan Tingkat Kesiapterapan Teknologi*), penulis `Menteri Riset, Teknologi, dan Pendidikan Tinggi Republik Indonesia`, `version: 52`, lampiran anak tetap `numChildren: 1`.
   - Item `[12]` (`TDNR9QKL`): nama penulis kedua disesuaikan dari `L. H. Almazaydeh` menjadi `Laiali Almazaydeh` (`version: 54`) sesuai halaman 3395 PDF asli.
   - Item `[36]` (`XXVECDHC`): dibuat sebagai item `dataset` baru untuk `S. C. Saragih (2024)` (*Indonesian SMS Spam Classifier Dataset*, GitHub, Lisensi MIT).
   - Total koleksi `6WSLSX4K` kini tepat **36 item** (`totalResults = 36`, `libraryVersion = 54`) tanpa entri duplikat maupun item tanpa judul.

### 16.4 Hasil Verifikasi Final (22 November 2026)
1. **`validate_unsia.py`:**
   - `02-bab-2-landasan-metode.md` (mandiri): **58 blok, sitasi unik `[1]`–`[36]`, `0 WARNING`**, dan `1 ERROR` positif palsu karena berkas bab mandiri tidak memuat Daftar Pustaka.
   - Gabungan `02-bab-2-landasan-metode.md` + blok `# DAFTAR PUSTAKA` (`bab2_plus_dp.md`): **95 blok, sitasi unik `[1]`–`[36]`, `0 ERROR`, `0 WARNING`** (`[OK] Lulus`).
   - `06-lampiran.md` (mandiri): **84 blok, `0 WARNING`** (hanya `1 ERROR` positif palsu urutan sitasi karena berkas lampiran tidak memuat Bab I).
2. **`humanizer-indonesia/scripts/metrik.py --preset akademik` pada `02-bab-2-landasan-metode.md`:**
   - **9/9 LULUS** (`109` kalimat, `1.837` kata, rerata `16,9` kata, simpangan baku `7,3`, kalimat $\ge 28$ kata `7,3%`, koordinasi `0,25`, konektor `0,05` per 100 kata, verba ringan `0,00`, enumerasi `0,00`, `merupakan` `0,54` per 1.000 kata, *em-dash* & *en-dash* `0`).
   - Diagnostik tambahan: kalimat pendek lepas `0`, deret sejajar `0`, penyangkalan antisipatif `0`, seluruh 11 diagnostik kaidah & wacana `0`, kepadatan pemadat `48,4` per 1.000 kata, dan *triplet* `1` (`0` pada prosa; `1` positif palsu pada baris rumus Persamaan 2.6).
3. **Keutuhan Sitasi `[1]`–`[36]` Lintas Bab dan Integritas Gambar:**
   - Daftar Pustaka pada `06-lampiran.md` berjumlah tepat **36 entri kontinu `[1]`–`[36]`**.
   - Pemeriksaan lintas `00-bagian-awal.md` hingga `06-lampiran.md`: seluruh `[1]`–`[36]` terpakai (`Unused = []`, `Missing from DP = []`, `OutOfRange = []`).
   - Tautan gambar di Bab II (`../../aset-gambar/Gambar 2.1 Bagan Alir Prosedur Eksperimen.png`) terverifikasi ada di disk (`exists = True`, resolusi `2160 x 990` piksel), bebas parameter pemenang dan `GridSearchCV`.


---

## 17. Audit Bab III, Lampiran 3, Validitas Dataset, dan Sinkronisasi Kode Implementasi

**Status Tahap Ini:** Tahap Audit Selesai (Belum Ada Penyuntingan pada Naskah Bab III / Lampiran 3 maupun Kode)  
**Tanggal Audit:** 22 November 2026

### 17.1 Identitas & Ruang Lingkup Audit
1. **Berkas utama yang diaudit:**
   - `06-naskah-ta/md/03-bab-3-implementasi-metode/03-bab-3-implementasi-metode.md` (58 baris, 753 kata).
   - Lampiran 3 pada `06-naskah-ta/md/06-lampiran/06-lampiran.md` (baris 149–199: `Tabel L.5`, `Tabel L.6`, `Tabel L.7`, dan `Gambar L.1`).
2. **Sumber pembuktian teknis yang diperiksa langsung:**
   - Dokumentasi & data: `04-dataset/readme-dataset.md`, `04-dataset/01-data-mentah/`, `04-dataset/02-data-olahan/`.
   - Skrip ML: `ml/korpus_pajak.py`, `ml/kurasi_dataset.py`, `ml/eksperimen_baseline.py`, `ml/eksperimen_komparasi.py`.
   - Purwarupa & pengujian: `app/backend/inference.py`, `app/backend/api.py`, `app/frontend/index.html`, `app/extension/manifest.json`, `app/extension/content.js`, `app/extension/background.js`, serta `tests/` (29 skenario `pytest`).

### 17.2 Angka Dataset Terverifikasi (Hasil Pemeriksaan Python Langsung)

#### A. Ringkasan Sumber Mentah (`04-dataset/01-data-mentah/`)
| Berkas Mentah | Total Baris | Distribusi Kelas Asli | Subset Biner Dipakai | Keterangan |
| :--- | :---: | :--- | :---: | :--- |
| `Rahmi 2016 Korpus SMS Spam Utama v1.csv` | 1.143 | `0` Normal: 569; `1` Penipuan: 335; `2` Promo: 239 | 904 | Menyisihkan 239 iklan promo |
| `Theodorus 2021 Korpus SMS Spam IEEE.csv` | 4.125 | `0` Ham: 2.323; `1` Promo: 1.382; `2` Spam: 420 | 2.743 | Menyisihkan 1.382 promo |
| `Saragih 2024 Korpus SMS Spam Indo.csv` | 690 | `non-spam`: 201; `penipuan`: 147; `promo`: 200; `kta`: 71; `judi`: 71 | 348 | Menyisihkan promo, KTA, dan judi |
| `Kurniawan 2024 Korpus Phishing SMS dan Email Indo.csv` | 1.772 | — | — | Arsip pembanding (tidak digabung) |
| `DJP Ringkasan Scrape 68 Sumber Resmi.csv` | 68 | — | 65 sumber | `SRC-046`, `SRC-049`, `SRC-061` tereksklusi |
| **Total Pra-Deduplikasi Korpus Diperluas** | — | `904 + 260 + 2.743 + 348` | **4.255** | Sebelum deduplikasi `clean_text` |

#### B. Integritas Berkas Olahan (`04-dataset/02-data-olahan/`)
| Berkas CSV Olahan | Baris Mentah CSV | Unik Pasca-Sastrawi (`teks_sastrawi`) | Distribusi Kelas Terverifikasi | Null / Kosong / Duplikat Tersisa |
| :--- | :---: | :---: | :--- | :--- |
| `Dataset Pajak Terkurasi 260 Baris.csv` | 260 | 260 (0 dibuang) | `1` (*Phishing*): 130; `0` (Resmi/Normal): 130 | Null: 0; `Teks` kosong: 0; Sastrawi kosong: 0; duplikat tersisa: 0 (`65` `id_sumber`, `22` `kategori_modus`) |
| `Dataset Gabungan Utama Biner 1164 Baris.csv` | 1.164 (`0`: 699; `1`: 465) | 1.159 (5 dibuang) | `0` (Aman/Normal): 697; `1` (*Phishing*/*Fraud*): 462 | Null: 0; `Teks` kosong: 0; Sastrawi kosong: 0; 5 duplikat Sastrawi berasal dari `Korpus_Umum_Rahmi2016` (1 duplikat teks persis + 4 variasi tanda baca/kapitalisasi) |
| `Dataset Gabungan Diperluas Biner 2521 Baris.csv` | 2.521 (`0`: 1.699; `1`: 822; hasil dedup `clean_text` dari 4.255 baris) | 2.519 (2 dibuang) | `0` (Aman/Normal): 1.697; `1` (*Phishing*/*Fraud*): 822 | Null: 0; `Teks` kosong: 0; `clean_text` duplikat: 0; **2 baris dari `Theodorus 2021` (`idx=1610` `'anda'` dan `idx=2074` `'Ok'`, label `0`) menjadi string kosong pasca-Sastrawi** sehingga 1 baris kosong tersisa di korpus 2.519 (`68` `id_sumber`, `28` `kategori_modus`) |

#### C. Konsistensi Katalog SHA-256, Audit Kebocoran Data (*Data Leakage*), dan `pytest`
1. **Katalog SHA-256 (`Katalog Asal Sumber Data.csv` & `.json`):** Seluruh **10/10** berkas (`FILE-RAW-01` s.d. `FILE-RAW-07`, `FILE-PROC-01` s.d. `FILE-PROC-03`) tersedia di disk dan **10/10 cocok persis** dengan *checksum* SHA-256 (`0` ketidakcocokan).
2. **Audit Kebocoran Data (*Data Leakage*):**
   - **Pembagian *Holdout* 80:20 (`random_state=42`, terstratifikasi):** Data latih `927` baris (`557` aman `0`, `370` penipuan `1`) dan data uji `232` baris (`140` aman `0`, `92` penipuan `1`); irisan `teks_sastrawi` = **`0`**.
   - ***Stratified 10-Fold CV* internal (`927` latih):** Irisan `teks_sastrawi` antar-lipatan pada kesepuluh lipatan = **`[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]`**; TF-IDF dibangun terisolasi di tiap lipatan oleh `_precompute_tfidf_folds`.
   - **Uji Kontrol 45 Pesan Pajak (`Korpus_Pajak_Terverifikasi` pada *holdout* `232`):** Subset pajak uji = **`45`** baris (`24` *phishing* `1`, `21` resmi `0`) vs subset latih SMS umum = **`712`** baris (`448` aman `0`, `264` penipuan `1`); irisan terhadap latih SMS-umum = **`0`** dan terhadap latih penuh `927` = **`0`**.
   - **Uji Eksternal *Zero-Shot* (`Stage 4B`):** **`1.360`** teks eksternal unik (`1.000` aman `0`, `360` penipuan `1`) di luar korpus induk `1.159` memiliki irisan = **`0`**.
3. **Status `pytest`:** **`29 passed` dalam `27,68` detik** (`test_eksperimen_baseline.py`: 2; `test_eksperimen_komparasi.py`: 5; `test_integritas_dataset.py`: 6; `test_prototipe_api.py`: 16).

### 17.3 Hasil Pemeriksaan `validate_unsia.py`, `metrik.py`, dan Perspektif S1 Sistem Informasi
1. **`validate_unsia.py` pada `03-bab-3-implementasi-metode.md`:** `28` blok diperiksa; sitasi unik terdeteksi `[2, 5, 6, 7, 17, 18, 19, 26, 27, 29, 30, 31, 33, 34, 35]`; `1 ERROR` positif palsu (berkas bab mandiri tanpa Daftar Pustaka); **`3 WARNING`** alinea lebih pendek dari ketentuan 5–7 baris (~55–85 kata, Pedoman UNSIA 4.2.d):
   - `[P9]` baris 17: `43` kata (~3,6 baris)
   - `[P16]` baris 31: `36` kata (~3,0 baris)
   - `[P19]` baris 37: `39` kata (~3,2 baris)
2. **`humanizer-indonesia/scripts/metrik.py --preset akademik`:** **9/9 LULUS** (`44` kalimat, `753` kata, rerata `17,1` kata/kalimat, simpangan baku `7,2`, kalimat $\ge 28$ kata `4,5%`, konektor `0,13`/100 kata, verba ringan `0,13`/100 kata, *em-dash* `0`). Catatan diagnostik: kepadatan kata pemadat sangat rendah (`14,6` per 1.000 kata vs rentang korpus `73–139`), `3` *triplet*, `1` kalimat pendek lepas (`Tahap data dijalankan melalui ...`), serta `1` verba ringan (`melakukan pemrosesan`).
3. **Evaluasi Narasi S1 Sistem Informasi:** Secara struktur alur sudah runtut (arsitektur $\to$ data & praproses $\to$ pelatihan & kalibrasi $\to$ purwarupa $\to$ pengujian), tetapi naskah masih terlalu tipis (58 baris, 753 kata) dan terbaca seperti daftar simbol kode Python. Perspektif rekayasa Sistem Informasi—seperti diagram/uraian kontrak data antara `content.js`–`background.js`–FastAPI, alasan bisnis/pengguna atas pemisahan skema keputusan `TINGGI`/`SEDANG`/`RENDAH`, pembagian peran komponen sistem, dan ketertelusuran kebutuhan fungsional/non-fungsional terhadap 29 kasus uji—belum dijelaskan utuh bagi pembaca bisnis/sistem.

### 17.4 Daftar Temuan Prioritas Bab III & Lampiran 3

| Kode | Tingkat | Lokasi | Inti Temuan & Bukti Kode/Data | Usulan Perbaikan Konkret |
| :---: | :---: | :--- | :--- | :--- |
| `K3-01` | **Kritis** | Bab III L7, L11, L15, L17, L31, L35, L46, L54; Lampiran 3 `Tabel L.5`–`L.6`, `Gambar L.1` | Seluruh jalur berkas/direktori memakai nama lama: `src/` (aktual `ml/`), `06 Prototipe Aplikasi/` (aktual `app/backend/`), `web/` (aktual `app/frontend/`), `extension/` (aktual `app/extension/`), dan `Aset Gambar/` (aktual `../../aset-gambar/`). | Perbarui seluruh jalur di Bab III, `Tabel L.5`, `Tabel L.6`, dan tautan `Gambar 3.1` / `Gambar L.1` agar cocok 100% dengan struktur repositori aktual. |
| `K3-02` | **Kritis** | Bab III L5, L58; Lampiran 3 `Tabel L.5` L158, L163, `Tabel L.7` L192 | (1) Bab III L5 mencantumkan `Python 3.11.9` (aktual `.venv`: `Python 3.14.7`). (2) Bab III L58 & `Tabel L.5` L163 masih menyebut `23 skenario uji` (`10` API + `13` data/model), sedangkan `tests/` aktual memiliki **`29` pengujian `pytest` lulus** (`16` pada `test_prototipe_api.py` + `6` `test_integritas_dataset.py` + `2` `test_eksperimen_baseline.py` + `5` `test_eksperimen_komparasi.py`). (3) `Tabel L.5` L158 masih menyebut `GridSearchCV`, padahal `ml/eksperimen_komparasi.py` memakai `_run_grid_over_folds`. | Samakan versi Python ke `3.14.7`, perbarui hitungan pengujian menjadi `29` kasus (`16` API + `13` data & eksperimen), dan ganti `GridSearchCV` pada `Tabel L.5` dengan pencarian *grid* terisolasi (`_run_grid_over_folds`). |
| `K3-03` | **Kritis** | Bab III L15, L23, L39–46, L52 | (1) L52 menyebut `lru_cache(maxsize=1)`, padahal `app/backend/inference.py` L189 memakai `@functools.lru_cache(maxsize=4)`. (2) L23 hanya menyebut 3 TLD (`.go.id`, `.co.id`, `.xyz`), padahal `ml/eksperimen_baseline.py` L26 memakai 9 akhiran (`go.id|co.id|my.id|com|net|org|xyz|id|cc`), sedangkan `inference.py` L23–34 memakai `_BARE_TLD_LIST` (64+ TLD), lookbehind `(?<!@)`, dan `re.IGNORECASE`. (3) L52 belum menyebut `re.IGNORECASE` pada `APK_PATTERN` serta eskalasi `has_apk -> label=1, TINGGI` dan ambang risiko `0,75`/`0,50`. (4) `Tabel 3.1` L39–46 memuat kolom `Konfigurasi Terpilih` (`C=2.0`, `100` pohon) secara prematur sebelum Bab IV (melanggar disiplin batas bab `K-05`/`K2-05`). (5) L15 menyebut `Saragih` tanpa sitasi `[36]`. | Perbaiki `maxsize=4`, jelaskan perbedaan cakupan `URL_PATTERN` pelatihan vs inferensi serta aturan ambang risiko (`>=0,75` `TINGGI`, `>=0,50` atau domain curiga `SEDANG`, eskalasi `.apk`), pindahkan nilai parameter pemenang dari `Tabel 3.1` ke Bab IV, dan tambahkan sitasi `[36]`. |
| `S3-01` | **Sedang** | Bab III L54; `Tabel L.6` L167–177 | (1) `Tabel L.6` belum mencantumkan `GET /simulasi-wa` (`api.py` L361), batas total 100.000 karakter per *batch* (`_MAX_BATCH_TOTAL_CHARS`), *weighted rate limit* batch (`RATE_LIMIT_PER_MIN=60`), dan respons error `503` saat model absen. (2) Narasi L54 tentang ekstensi *Manifest V3* belum menjelaskan alur pesan aktual: `content.js` (`MutationObserver` 150 ms + interval 1.500 ms + penyaring pesan keluar `TAX_SELF_TEST_RE` vs pesan masuk $\ge 8$ karakter/sinyal `.apk` atau URL) $\to$ `chrome.runtime.sendMessage` (`WA_PAJAK_PREDICT`) $\to$ `background.js` (Service Worker) $\to$ `POST /predict`. | Lengkapi `Tabel L.6` dengan endpoint `/simulasi-wa`, batasan batch 100.000 karakter, *rate limiting*, dan kode `503`; uraikan alur komunikasi *content script*–*service worker*–FastAPI di Subbab 3.4 secara runtut. |
| `S3-02` | **Sedang** | Bab III L15, L17, L31, L37 | `validate_unsia.py` mencatat `3 WARNING` alinea pendek (`[P9]`, `[P16]`, `[P19]`); `metrik.py` mencatat kepadatan pemadat `14,6`/1.000 kata, `1` kalimat pendek lepas (`Tahap data dijalankan melalui ...`), dan `1` verba ringan (`melakukan pemrosesan`). | Kembangkan `[P9]`, `[P16]`, dan `[P19]` menjadi 5–7 baris (~55–85 kata) beserta alasan desain sistemnya, gabungkan kalimat pendek lepas di L15, dan haluskan transisi antar-kalimat. |
| `S3-03` | **Sedang** | Seluruh Bab III (`03-bab-3-implementasi-metode.md`) | Narasi masih terlalu singkat (58 baris, 753 kata) dan berorientasi rincian kode Python tanpa menjembatani pemahaman pembaca bisnis/sistem informasi (alur keputusan risiko bagi wajib pajak, kontrak pertukaran data, tata kelola keamanan *privacy-preserving*, serta keterkaitan skenario uji dengan kebutuhan fungsional/non-fungsional). | Perkaya narasi operasional di setiap subbab dari sudut pandang arsitektur sistem informasi, alur layanan pengguna, dan matriks keterlacakan pengujian. |
| `M3-01` | **Minor** | Bab III L35, L54, L58 | Penggunaan *backtick* tidak konsisten pada angka (`697`, `462`, `422`) dan rujukan `Tabel L.5`–`L.7` / `Gambar L.1`. | Hapus *backtick* pada angka biasa serta rujukan tabel/gambar lampiran; sisakan untuk pengenal kode/endpoint/header teknis. |
| `M3-02` | **Minor** | Bab III L31, L46; `Tabel L.5` L158 | Masih terdapat istilah lama `"kata henti"` (L31) dan `"Penalaan"` (L46, `Tabel L.5` L158) yang belum seragam dengan revisi Bab I–II. | Seragamkan ke `"daftar kata umum"` / *stopword* dan `"Penyetelan Hiperparameter"`. |
| `M3-03` | **Minor** | Bab III L48, L52, L54 | Penempatan sitasi kurang pas: L48 kurang `[36]` pada korpus 2.519; L52 menempelkan `[34]` di kalimat detail `lru_cache`/`clean_text`; L54 menempelkan `[19]` langsung pada rincian ekstensi *WhatsApp Web* milik penulis. | Tambahkan `[36]` di L48 dan geser `[34]`/`[19]` agar merujuk pada konteks konsep TKT 6 dan ekstensi peramban secara akurat. |
| `M3-04` | **Minor** | Bab III L15, L48; `readme-dataset.md` | Dua baris sangat pendek dari `Theodorus 2021` (`'anda'` dan `'Ok'`, label `0`) tereduksi menjadi *string* kosong setelah *stopword removal* & *stemming* Sastrawi pada korpus diperluas 2.521 (menyisakan 1 baris kosong di korpus 2.519), meski korpus induk 1.159 dan pajak 260 bersih (0 baris kosong). | Catat fenomena 2 baris kosong pasca-Sastrawi pada korpus diperluas 2.521/2.519 secara transparan pada penjelasan data agar tidak membingungkan pembaca/penguji. |


---

## 18. Log Eksekusi Revisi Bab III, Lampiran 3, Aset Gambar, dan Dokumentasi Dataset

**Status Tahap Ini:** Seluruh revisi Bab III (`03-bab-3-implementasi-metode.md`), Lampiran 3 (`06-lampiran.md`), Daftar Tabel (`00-bagian-awal.md`), aset visual (`Gambar 3.1` dan `Gambar L.1`), serta dokumentasi dataset (`04-dataset/readme-dataset.md`) telah dijalankan dan diverifikasi pada 22 November 2026.

### 18.1 Ringkasan Penyelesaian Temuan Audit (`K3-01`–`K3-03`, `S3-01`–`S3-03`, `M3-01`–`M3-04`)

| Kode / Area | Status | Ringkasan Perbaikan yang Diterapkan |
| :--- | :---: | :--- |
| `K3-01` | Selesai | Memperbarui seluruh jalur kode dan gambar pada Bab III serta Lampiran 3 (`Tabel L.5`–`L.6`, `Gambar 3.1`, `Gambar L.1`) ke struktur aktual `ml/`, `app/backend/`, `app/frontend/`, `app/extension/`, dan `../../aset-gambar/`. |
| `K3-02` | Selesai | Menyelaraskan versi lingkungan ke `Python 3.14.7`, memperbarui hitungan pengujian menjadi `29` kasus (`13` data/model + `16` API & keamanan pada `tests/`), dan mengganti istilah `GridSearchCV` pada `Tabel L.5` menjadi pencarian *grid* terisolasi (`_run_grid_over_folds`). |
| `K3-03` | Selesai | Memperbaiki `lru_cache(maxsize=4)` (`app/backend/inference.py`), menyinkronkan cakupan `URL_PATTERN` pelatihan (9 akhiran domain) dan inferensi (`_BARE_TLD_LIST` 64+ TLD, `(?<!@)`, `re.IGNORECASE`), menguraikan eskalasi `.apk` (`label=1`, `TINGGI`) serta ambang risiko `0,75`/`0,50`, membuang parameter pemenang prematur dari `Tabel 3.1`, dan menyematkan sitasi `[36]` untuk Saragih. |
| `S3-01` | Selesai | Melengkapi `Tabel L.6` dengan `GET /simulasi-wa`, batas 100.000 karakter *batch*, pembatas laju berbobot (`60`/menit), serta galat `503`; menambahkan `UJI-11` s.d. `UJI-16` di `Tabel L.7`; menguraikan alur `content.js` (`MutationObserver`, filter pesan masuk/keluar) $\to$ `chrome.runtime.sendMessage` $\to$ `background.js` $\to$ `POST /predict`. |
| `S3-02` | Selesai | Mengembangkan alinea pendek serta memecah kalimat terlalu panjang sehingga `validate_unsia.py` mencatat **`0 WARNING`** dan `metrik.py --preset akademik` lulus **9/9 metrik** (`rerata 18,9`, `kalimat panjang 8,6%`, `0` kalimat pendek lepas, `0` verba ringan). |
| `S3-03` | Selesai | Memperkuat narasi Sistem Informasi di Bab III (`1.099` kata): menjelaskan tata kelola privasi (pemrosesan sementara tanpa simpan isi pesan), aturan bisnis verifikasi perpajakan, label antarmuka web aktual dari `app/frontend/index.html` (`Periksa Chat WhatsApp`, `Tempel & Periksa`, `Periksa Pesan`, `Info Akademik (TA UNSIA)`), serta ketertelusuran 29 skenario uji. |
| `M3-01`–`M3-04` | Selesai | Menyeragamkan pemakaian *backtick* (tanpa *backtick* pada angka dan rujukan tabel/gambar), menyelaraskan istilah `"daftar kata umum (*stopword*)"` dan `"Penyetelan Hiperparameter"`, memperbaiki penempatan sitasi `[19]`, `[34]`, `[36]`, dan mencatat 2 pesan singkat (`'anda'`, `'Ok'`) yang menjadi *string* kosong pasca-Sastrawi pada korpus diperluas `2.519`. |
| **Perbaikan Tambahan** | Selesai | Merender ulang `Gambar 3.1 Arsitektur Sistem Terpadu.png` (bebas parameter pemenang `C=2.0`, memakai jalur aktual `app/*` dan `maxsize=4`) serta `Gambar L.1 Rancangan Antarmuka Purwarupa dan Ekstensi.png` (menyesuaikan label UI aktual `app/frontend/index.html`); menyinkronkan judul `Tabel 3.1` dan `Tabel L.6` pada `00-bagian-awal.md`; serta memperbarui jalur `04-dataset/`, `ml/`, dan angka uji `232` baris di `04-dataset/readme-dataset.md`. |

### 18.2 Hasil Verifikasi Final (22 November 2026)
1. **`validate_unsia.py`:**
   - `03-bab-3-implementasi-metode.md` (mandiri): **32 blok, sitasi unik `[2, 5, 6, 7, 17, 18, 19, 26, 27, 29, 30, 31, 33, 34, 35, 36]`, `0 WARNING`**, `1 ERROR` positif palsu (berkas mandiri tanpa Daftar Pustaka).
   - Gabungan Bab III + blok `# DAFTAR PUSTAKA` (`bab3_plus_dp.md`): **70 blok, `0 ERROR`, `0 WARNING`** (`[OK] Dokumen lulus seluruh pemeriksaan kepatuhan Pedoman TA UNSIA & Humanizer-ID`).
2. **`humanizer-indonesia/scripts/metrik.py --preset akademik` (`03-bab-3-implementasi-metode.md`):**
   - **9/9 LULUS** (`58` kalimat, `1.099` kata, rerata `18,9` kata, simpangan baku `6,5`, kalimat $\ge 28$ kata `8,6%`, koordinasi `0,40`, konektor `0,18`/100 kata, verba ringan `0,00`, enumerasi `0,00`, `merupakan` `0,00`, *em-dash* `0`, kalimat pendek lepas `0`, seluruh 11 kaidah & wacana `0`).
3. **Keutuhan Sitasi & Tautan Gambar:**
   - Daftar Pustaka `[1]`–`[36]` lintas `00-bagian-awal.md` s.d. `06-lampiran.md`: **`DP count = 36`, `Unused = []`, `Missing from DP = []`**.
   - Tautan gambar di Bab III (`../../aset-gambar/Gambar 3.1 Arsitektur Sistem Terpadu.png`) dan Lampiran 3 (`../../aset-gambar/Gambar L.1 Rancangan Antarmuka Purwarupa dan Ekstensi.png`) terverifikasi ada (`exists = True`). *(Catatan untuk audit Bab IV/Lampiran 4 berikutnya: `Gambar L.2` dan `Gambar L.3` pada Lampiran 4 masih memakai jalur lama `Aset Gambar/...` dan belum disentuh pada tahap ini.)*
4. **`pytest -q`:** **`29 passed` dalam `5,63` detik** (`exit code 0`).

---

## 19. Audit Ulang & Eksekusi Revisi Bab II, Lampiran 1–2, Gambar 2.1, Daftar Pustaka `[1]`–`[36]`, & Zotero (24 November 2026)

**Status Tahap Ini:** Seluruh temuan audit Bab II pasca-penguncian Bab I (`K-01`–`K-05`, `S-01`–`S-06`, `M-01`–`M-03`) telah disetujui dan dieksekusi penuh terhadap `02-bab-2-landasan-metode.md`, `06-lampiran.md`, `00-bagian-awal.md`, `Gambar 2.1 Bagan Alir Prosedur Eksperimen.png`, `03-bab-3-implementasi-metode.md`, `04-bab-4-hasil-dan-analisa.md`, `03-referensi/catatan-kebaruan-dan-daftar-referensi.md`, serta dua item Zotero (`ZK3YRJSC`, `8EJRWUJ3`).

### 19.1 Ringkasan Penyelesaian Temuan Audit

| Kode | Status | Ringkasan Eksekusi & Bukti Verifikasi |
| :---: | :---: | :--- |
| `K-01` | Selesai | Menata ulang penomoran sitasi IEEE `[25]`–`[36]` berurutan mengikuti kemunculan pertama pada naskah terpadu Bab I + Bab II (`[34]->[25]`, `[25]->[26]`, `[26]->[27]`, `[33]->[28]`, `[27]->[29]`, `[35]->[30]`, `[28]->[31]`, `[30]->[32]`, `[29]->[33]`, `[31]->[34]`, `[32]->[35]`, `[36]->[36]`) serta menyinkronkannya di Daftar Pustaka `06-lampiran.md`, Bab III, Bab IV, dan `catatan-kebaruan-dan-daftar-referensi.md`. |
| `K-02` | Selesai | Menyelaraskan fakta dan metrik sumber primer di Bab II & `Tabel L.1`: `[9]` Al Ghofany dkk. (`TF-RF + stemming`: SVM Linear `100%`, SVM *Sigmoid* `99,96%`, serta catatan `10-fold CV × 15 iterasi`); `[3]` Prakoso dkk. (Coretax, NIK, NPWP, DJP Online, M-Pajak, SPT tanpa PKP); `[19]` Suwarno dkk. (`235.370` total URL bersih: `134.850` sah + `100.520` *phishing*); `[11]` & `[18]` pemisahan cacah total dua kelas; `[10]` Astuti dkk. (+RF `Acc 97,28%`, *Macro F1*, dan catatan *support* 1.839). |
| `K-03` | Selesai | Menyeragamkan komposisi `Dataset Pajak Terkurasi 260 Baris.csv` pada Subbab `2.3`, `2.6`, `Tabel L.3`, dan `Gambar 2.1` menjadi `130 phishing` dan `130 aman (110 siaran resmi DJP + 20 pesan pajak normal)` selaras dengan Bab I. |
| `K-04` | Selesai | Memperbarui Daftar Pustaka `[22]` (`M. Darwin *et al.*`, Editor `T. S. Tambunan`, `CV. Media Sains Indonesia`) dan `[24]` Sinambela (`2014`, `Graha Ilmu` Yogyakarta mengikuti kolofon PDF terlampir), serta memperbarui item Zotero `ZK3YRJSC` (`version 55`, `Salman Alparis Sormin` + 9 penulis lain + editor) dan `8EJRWUJ3` (`version 56`, edisi `2014`). |
| `K-05` | Selesai | Mempertegas cakupan teknis rumus & praproses: penyaringan token 1 karakter di `TfidfVectorizer` standar (`2.2.3`, `Tabel L.4`); margin fungsional $f(\mathbf{x})/\|\mathbf{w}\|_2$, target probabilitas teratur $t_i$ Lin dkk. `[30]`, dan perataan peluang 5 submodel `(TF-IDF + LinearSVC + Sigmoid)` pada `CalibratedClassifierCV(cv=5)` (`2.2.1`); augmentasi bias $b$ ke regularisasi L2 LIBLINEAR (`2.2.1`); serta jumlah berbobot impuritas Gini anak simpul menurut CART/`scikit-learn` `[28]` (`2.2.2`). |
| `S-01` | Selesai | Memperbaiki judul `2.2.4` dan menambahkan entri subbab `2.2.5 Indikator Kelayakan Purwarupa dan Kesiapterapan Teknologi (TKT Level 6)` pada Daftar Isi `00-bagian-awal.md`. |
| `S-02` | Selesai | Melengkapi rincian 5 surat DJP `2024–2026` (termasuk `PENG-1/PJ.09/2025`) di `[5]`, menambah `pp. 1-39, Sep. 2020` pada `[4]`, menambahkan koma jurnal pada `[11]`, menyematkan DOI terbitan `10.37817/ikraith-informatika.v10i3` pada `[13]`, dan mengubah judul `[28]` (`Pedregosa`) ke *sentence case*. |
| `S-03` | Selesai | Memisahkan sitasi `[2]` (.apk) dari `[1], [3], [4], [5]` (tautan palsu) di `2.1`, menambahkan catatan kandidat daftar putih `t.kemenkeu.go.id` dari `PENG-50/PJ.09/2025` `[5]` di `2.2.5`, menyertakan `[7], [36]` di `2.3` tahap `a)`, `[28]` di `2.3` tahap `d)`, serta memisahkan peran Kohavi `[34]` (*10-Fold CV*) dari `scikit-learn` `[28]` (isolasi kosakata TF-IDF) di `2.6`. |
| `S-04` | Selesai | Merancang ulang `Gambar 2.1 Bagan Alir Prosedur Eksperimen.png` memakai alur 3-zona HTML+SVG (memisahkan `Partisi 80:20` dari `TF-IDF 10-Fold CV terisolasi`, menambahkan cabang kontrol `712 SMS -> n=45` dan jalur `232 / 1.360 / 2.519`, memperbaiki label `110 resmi, 20 normal`, dan membersihkan pengenal internal kode). |
| `S-05` | Selesai | Menambahkan `Seaborn 0.13.2` dan `Uvicorn 0.54.0` pada `2.5` & `Tabel L.3`, memperjelas komposisi `1.159 + 1.360 = 2.519`, menambahkan `[2], [5], [6]` di `Tabel L.3`, serta melengkapi `2.7` & `Tabel L.4` dengan skala pengukuran, variabel perlakuan uji kontrol (`712` vs `927`), kliping $\epsilon = 10^{-15}$, dan ambang risiko `TINGGI`/`SEDANG`/`RENDAH`. |
| `S-06` & `M-01`–`M-03` | Selesai | Menghapus seluruh 8 kalimat penutup *punchline* simetris, memperbaiki rujukan kohesi Subbab `2.4`, menstandarkan cetak miring (*Coretax*, *Sigmoid*, *bot*, *Euclidean*, *dataset*, *Log Loss*), menghapus *backtick* non-kode, menghindari `[0, 1]` dan *en-dash* agar bebas salah deteksi sitasi/gaya, menjabarkan komponen $v_t(d)$ & vektor nol pada Persamaan (2.5), mengganti indeks pohon `Persamaan (2.4)` ke $m=1,\dots,T$, serta menstabilkan panjang seluruh paragraf Bab II ke `5–7` baris (`~55–85` kata). |

### 19.2 Hasil Verifikasi Pasca-Revisi (24 November 2026)

1. **`Gambar 2.1 Bagan Alir Prosedur Eksperimen.png` (`diagram-design`):**
   - `self_check.py`: **`OK`** (tanpa pelanggaran kontras, teks melebihi kotak, maupun `viewBox`).
   - `verify_geometry.py`: **`Summary: 1 file(s) checked, 0 finding(s).`**
   - Render *headless Chromium* skala `2x`: **`2000×1568` piksel** (`297.512` byte; `exists = True`), telah diperiksa secara visual agar bebas tumpukan garis maupun label terpotong.
2. **`validate_unsia.py`:**
   - `02-bab-2-landasan-metode.md` (mandiri): **`60` blok, `0 WARNING`**, `1 ERROR` semu (berkas mandiri tanpa Daftar Pustaka).
   - Gabungan `Bab I + Bab II + Daftar Pustaka`: **`137` blok, `0 ERROR`, `0 WARNING`** (`[OK] Dokumen lulus seluruh pemeriksaan kepatuhan Pedoman TA UNSIA & Humanizer-ID`), urutan sitasi **`[1]`–`[36]` tepat sekuensial**.
   - Gabungan `Bab I..V + Daftar Pustaka`: **`221` blok, `0 ERROR`**, `[1]`–`[36]` utuh (`3 WARNING` berada di luar Bab I–II, yaitu pada Bab IV `[P166]`, `[P168]`, `[P176]`).
3. **`humanizer-indonesia/scripts/metrik.py --preset akademik` (`02-bab-2-landasan-metode.md`):**
   - **9/9 LULUS:** `101` kalimat, `1.775` kata, rerata `17,6` kata/kalimat, simpangan baku `6,4`, kalimat $\ge 28$ kata `6,9%`, koordinasi `0,43`, konektor `0,17`/100 kata, verba ringan `0,00`/100 kata, enumerasi `0,00`, `merupakan` `0,00`, *em/en-dash* `0`, kalimat pendek lepas `0`, dan seluruh `11` diagnostik kaidah & wacana bernilai `0`. *(Catatan: kepadatan pemadat `27,6`/1.000 kata tetap dipantau pada sifat ringkas penulisan rumus dan parameter.)*
4. **Integritas Lintas Berkas:** `DP entries = 36 contiguous 1..36`, `Unused = []`, `Missing = []`; Zotero `ZK3YRJSC` (`v55`) dan `8EJRWUJ3` (`v56`) terverifikasi. *(Catatan lanjutan: peninjauan & sinkronisasi Bab IV–V beserta kompilasi akhir `.docx` via `export_unsia_docx.py` dijadwalkan pada sesi berikutnya.)*


---

## 20. Audit Ulang Mendalam & Eksekusi Revisi Bab III, Lampiran 3, Aset Visual, Dataset, dan Kode (24 November 2026)

**Status Tahap Ini:** Seluruh temuan audit pasca-penguncian Bab I–II (`K3R-01`–`K3R-05`, `S3R-01`–`S3R-06`, `M3R-01`–`M3R-05`) telah disetujui dan dieksekusi penuh terhadap `03-bab-3-implementasi-metode.md`, Lampiran 3 pada `06-lampiran.md`, `Gambar 3.1 Arsitektur Sistem Terpadu.png`, `Gambar L.1 Rancangan Antarmuka Purwarupa dan Ekstensi.png`, `04-dataset/readme-dataset.md`, serta perbaikan minor pada `ml/korpus_pajak.py`, `ml/eksperimen_komparasi.py`, `app/backend/model_phishing_pajak.joblib` (metadata `preprocessing`), `app/backend/api.py`, `app/frontend/app.js`, dan `tests/test_prototipe_api.py`.

### 20.1 Angka Dataset Terverifikasi Mutakhir (Audit Python Langsung 24 November 2026)

1. **Korpus Mentah (`.csv`, `.xlsx`, `.json`) di `04-dataset/01-data-mentah/`:**
   - `Rahmi 2016 Korpus SMS Spam Utama v1.csv` & `Rahmi 2016 Arsip Asli SMS Spam.csv`: masing-masing `1.143` baris, `0` null (`0`: `569`, `1`: `335`, `2`: `239`; subset biner `904`).
   - `Theodorus 2021 Korpus SMS Spam IEEE.csv`: `4.125` baris, `0` null (`0`: `2.323`, `1`: `1.382`, `2`: `420`; subset biner `2.743`); `Theodorus 2021 Koleksi SMS Asli.xlsx` memiliki 8 *sheet* dengan *sheet* utama `Training Data` berjumlah `4.125` baris data (`4.126` termasuk *header*).
   - `Saragih 2024 Korpus SMS Spam Indo.csv`: `690` baris, `0` null (`Non-spam`: `201`, `Promo`: `200`, `Penipuan`: `147`, `KTA`: `71`, `Judi`: `71`; subset biner `348`); `Saragih 2024 Dataset SMS Asli.xlsx` (`Sheet1`) berjumlah `690` baris data (`691` termasuk *header*).
   - `Kurniawan 2024 Korpus Phishing SMS dan Email Indo.csv`: `1.772` baris, `0` null (`1`: `1.069`, `0`: `703`; `email`: `1.234`, `sms`: `538`; arsip pembanding, tidak digabung).
   - `DJP Hasil Scrape 68 Sumber Resmi.json` & `DJP Ringkasan Scrape 68 Sumber Resmi.csv`: `68` artikel (`http_status=200`, `0` null, tanggal `2021-09-09` s.d. `2026-09-22`; `45` domain `pajak.go.id`/`www.pajak.go.id` + `23` berita/cek fakta). Terpakai di korpus pajak 260: `65` sumber (`45` kanal resmi `pajak.go.id` + `20` berita/cek fakta; mengecualikan `SRC-046`, `SRC-049`, `SRC-061`).
   - `DJP Indikator Penipuan dan Kanal Resmi.json`: `31` butir dalam 5 daftar (`6` sumber otoritatif, `6` domain *phishing*, `2` *email spoofing*, `7` nomor WA penipu, `10` kanal resmi).
2. **Korpus Olahan (`04-dataset/02-data-olahan/`) dan Pelurusan Mekanisme Deduplikasi:**
   - `Dataset Pajak Terkurasi 260 Baris.csv`: `260` → `260` unik pasca-Sastrawi (`1`: `130` lintas 12 modus; `0`: `130` = `110` `Resmi_*` + `20` `Normal_*`; `0` null/kosong/duplikat).
   - `Dataset Gabungan Utama Biner 1164 Baris.csv`: `1.164` (`0`: `699`, `1`: `465`) → `1.159` unik pasca-Sastrawi (`0`: `697`, `1`: `462`; `5` baris duplikat asal `Korpus_Umum_Rahmi2016` dibuang: `idx 419/440`, `516/692` label `0` dan `idx 64/65`, `161/162`, `189/190` label `1`; `0` null/kosong).
   - `Dataset Gabungan Diperluas Biner 2521 Baris.csv`: `4.255` mentah → `2.521` pasca-`clean_text` (`0`: `1.699`, `1`: `822`) → `2.519` unik pasca-Sastrawi (`0`: `1.697`, `1`: `822`; `2` baris label `0` dari Theodorus dkk. gugur: `1` baris `idx=2074` `'Ok'` luruh ke `""` bertumbukan dengan `idx=1610` `'anda'` yang tersisa sebagai 1 baris kosong di `2.519`, dan `1` baris `idx=1230` bertumbukan dengan `idx=1229` sesudah *stopword* `'akan'` terbuang).
3. **SHA-256 & Kebocoran Data:**
   - Katalog SHA-256 (`Katalog Asal Sumber Data.csv` & `.json`): `10/10` berkas cocok persis (`0` hilang, `0` tidak cocok, `0` beda CSV vs JSON).
   - *Data leakage*: irisan `0` pada *holdout* 80:20 (`927:232`, `random_state=42`), 10-*Fold* CV (`[0]*10`), uji kontrol `45` pesan pajak (`24` *phishing*, `21` resmi) vs `712` SMS latih maupun `927` latih penuh, serta uji eksternal *zero-shot* `1.360` (`1.000` aman, `360` *phishing*; dari `3.091` mentah `-1.483` dup internal `-248` irisan induk) vs `1.159` induk.

### 20.2 Ringkasan Penyelesaian Temuan Audit (`K3R-01`–`K3R-05`, `S3R-01`–`S3R-06`, `M3R-01`–`M3R-05`)

| Kode | Status | Ringkasan Eksekusi & Perbaikan |
| :---: | :---: | :--- |
| `K3R-01` | Selesai | Meluruskan Bab III Subbab 3.4 menjadi `FastAPI 0.163.1` dan `Uvicorn 0.54.0` dengan versi kontrak API `2.1.0` (selaras Bab II & `Tabel L.3`). |
| `K3R-02` | Selesai | Memisahkan peran `_assemble_prediction` (penetapan `label` & `risk_level` `TINGGI`/`SEDANG`/`RENDAH`), `_extract_top_triggers` (skor kontribusi fitur `tfidf * coef`), dan `_build_plain_reasons`/`_extract_highlights_and_triggers` (alasan awam & sorotan). |
| `K3R-03` | Selesai | Memperbaiki sitasi Bab III Subbab 3.1 dari `[6], [32], [33]` menjadi `[27], [28], [31], [33]` (LIBLINEAR, `scikit-learn`, Breiman, Salton & Buckley). |
| `K3R-04` | Selesai | Menyelaraskan komposisi 260 pesan pajak di 3.2 menjadi `130 phishing` (12 modus) dan `130 aman (110 siaran resmi DJP + 20 percakapan administrasi pajak normal)` serta memisahkan peran `strip_djp_boilerplate` dari kurasi manual 65 sumber (`45` domain `pajak.go.id` + `20` berita/cek fakta). |
| `K3R-05` | Selesai | Memecah `UJI-09` pada `Tabel L.7` menjadi `UJI-09a` dan `UJI-09b` sehingga `16` fungsi `pytest` pada `tests/test_prototipe_api.py` terpetakan 1-ke-1 ke `16` kode uji (`UJI-01`–`UJI-09a`, `UJI-09b`, `UJI-11`–`UJI-16`) ditambah `UJI-10` (13 uji data/model) = 29 total. |
| `S3R-01`–`S3R-02` | Selesai | Menjelaskan mekanisme penyusutan `2.521 -> 2.519` (`'anda'`/`'Ok'` + duplikat *stopword* `'akan'`) di Bab III & `readme-dataset.md`; membedakan eksplisit `clean_text` kurasi 4 langkah (`ml/kurasi_dataset.py`) dari `clean_text` pelatihan/inferensi 6 langkah (`ml/eksperimen_baseline.py`) serta perilaku `clean_text_without_entity_tokens` (`[^a-z\s]`). |
| `S3R-03`–`S3R-04` | Selesai | Memperbarui daftar TLD ke `79 akhiran domain` pada Bab III & `Gambar 3.1`; merender ulang `Gambar 3.1` (`2080×1520`, alur `content.js & popup.html -> background.js`, bebas tabrakan panah-label) dan `Gambar L.1` (`2320×1440`, DOM aktual `index.html` dengan `Siap` di `popup.html`), keduanya lulus `self_check.py = OK` dan `verify_geometry.py = 0 finding(s)`. |
| `S3R-05`–`S3R-06` | Selesai | Menambahkan catatan kandidat `t.kemenkeu.go.id`, kondisi `label=0, risk_level=SEDANG` (`Perlu Verifikasi / Waspada`), kondisi tombol pesan keluar ekstensi + `top_k=5` + *fallback* `/simulasi-wa`, serta memecah paragraf panjang agar alur Sistem Informasi runtut dan memenuhi rentang 5–7 baris Pedoman UNSIA 4.2.d. |
| `M3R-01`–`M3R-05` | Selesai | Menghapus entri cadangan tak terpakai `SRC-069` di `ml/korpus_pajak.py` (`len(SOURCE_METADATA) = 68`); memperbarui metadata `"preprocessing": "ml.eksperimen_baseline.clean_text"` pada `ml/eksperimen_komparasi.py` & `app/backend/model_phishing_pajak.joblib` serta docstring L338 (`927` data latih); menyeragamkan `M.M.S.I.` pada `api.py`, `app.js`, & `test_prototipe_api.py`; melengkapi `Tabel L.5`–`L.6` (`simulasi_wa.js`, *default* `top_k`, bidang respons) serta keseragaman `WhatsApp` tegak. |

### 20.3 Hasil Verifikasi Pasca-Revisi (24 November 2026)
- **`pytest -q`:** **`29 passed`** (`exit code 0`), **`ruff check ml app tests`:** **`All checks passed!`**
- **`validate_unsia.py`:** `03-bab-3-implementasi-metode.md` (mandiri) `36` blok, **`0 WARNING`**; gabungan `Bab III + Daftar Pustaka` **`0 ERROR, 0 WARNING`** (`[OK] Lulus`); lintas `Bab I..V + Daftar Pustaka` sitasi `[1]`–`[36]` utuh (`Unused = []`, `Missing = []`).
- **`humanizer-indonesia/scripts/metrik.py --preset akademik`:** **`9/9 LULUS`** (`71` kalimat, `1.395` kata, rerata `19,6`, SD `6,8`, kalimat $\ge 28$ kata `11,3%`, konektor `0,22`/100 kata, verba ringan `0,00`, `merupakan` `0,00`, *em/en-dash* `0`, seluruh 11 diagnostik kaidah & wacana `0`).
- **Aset Visual (`diagram-design`):** `Gambar 3.1` (`2080×1520`) dan `Gambar L.1` (`2320×1440`) lulus `self_check.py = OK` dan `verify_geometry.py = 0 finding(s)` serta terverifikasi visual bebas tumpang tindih.


---

## 21. Audit dan Eksekusi Revisi Bab IV, Lampiran 4, Aset Gambar, dan Benchmark Purwarupa (24 November 2026)

Reviu mendalam dan verifikasi ulang numerik penuh terhadap **BAB IV (`04-bab-4-hasil-dan-analisa.md`)**, **Lampiran 4 (`06-lampiran.md`)**, seluruh CSV/JSON hasil evaluasi di `05-hasil-evaluasi/`, skrip `ml/benchmark_purwarupa.py`, serta tangkapan layar UI purwarupa telah dilaksanakan dan diselesaikan (dengan catatan penyelarasan Bab V ditunda ke sesi berikutnya).

### 21.1 Angka Final Terverifikasi (Hasil Hitung Ulang CSV/JSON & Benchmark Baru)

| Domain Evaluasi | Sumber Artefak | Angka Final Terverifikasi |
| :--- | :--- | :--- |
| **Eksekusi & Split Induk** | `ml/eksperimen_komparasi.py`, `ringkasan_eksperimen_lengkap.json` | `random_state=42`, durasi `189,36` detik; `1.164 -> 1.159` unik (`927` latih / `232` uji). |
| ***Baseline Holdout* (`n=232`)** | `tabel_komparasi_utama.csv` | `LinearSVC` bawaan: *Acc* `96,12%`, *Prec* `97,70%`, *Rec* `92,39%`, *F1* `94,97%` (`TN=138, FP=2, FN=7, TP=85`); RF (`n_estimators=200`): *Acc* `96,12%`, *F1* `95,03%` (`TN=137, FP=3, FN=6, TP=86`). |
| **10-*Fold* CV Default (`n=927`)** | `ringkasan_eksperimen_lengkap.json` | `LinearSVC`: *F1* `97,04% (± 2,71%)`, *Acc* `97,63% (± 2,20%)`, *ROC-AUC* `0,9956`, `0,002645` s/lipatan; RF: *F1* `93,68% (± 3,20%)`, *Acc* `94,93% (± 2,59%)`, *ROC-AUC* `0,9905`, `0,535709` s/lipatan (rasio **`202,57`**x). |
| **10-*Fold* CV Tuned (`36` komb.)** | `hasil_gridsearch_10fold.csv`, `ringkasan_eksperimen_lengkap.json` | `LinearSVC` (`C=2.0`, `class_weight=None`): *F1* `97,16% (± 2,41%)`, *Acc* `97,74% (± 1,93%)`, *ROC-AUC* `0,9956`, `0,003900` s/lipatan; RF (`n_estimators=100`, `max_depth=None`, `min_samples_split=2`, `class_weight=None`): *F1* `94,07% (± 2,92%)`, *Acc* `95,25% (± 2,39%)`, *ROC-AUC* `0,9901`, `0,309561` s/lipatan (rasio **`79,36`**x). |
| ***Holdout* Terkalibrasi Platt (`n=232`)** | `tabel_komparasi_utama.csv`, `ringkasan_eksperimen_lengkap.json` | `LinearSVC` Platt: *Acc* `95,69%` (`TN=137, FP=3, FN=7, TP=85`), *ROC-AUC* `0,995730` (`0,9957`), *PR-AUC* `0,994296` (`0,9943`), *Brier* `0,02541712` (`0,02542`), *Log Loss* `0,09185649` (`0,09186`), zona abu `[0,2..0,8]` = `22/232` (`9,48%`). RF Platt: *Acc* `96,55%` (`FP=2, FN=6`), *ROC-AUC* `0,9936`, *PR-AUC* `0,9909`, *Brier* `0,04214`, *Log Loss* `0,15870`. Reduksi `LinearSVC` vs RF: *Brier* `-39,68%`, *Log Loss* `-42,12%`. |
| **McNemar & Bootstrap 95% CI** | `holdout_proba_svm_calibrated` (`ringkasan_eksperimen_lengkap.json`) | McNemar eksak dua sisi (`n=232`): `both_ok=219`, `svm_only_ok=3`, `rf_only_ok=5`, `both_err=5`, `p = 0,7266`. Bootstrap 95% CI `LinearSVC` Platt: *Acc* `[93,10%, 98,28%]`, *F1* `[90,80%, 97,67%]`, *ROC-AUC* `[0,9896, 0,9995]`, *Brier* `[0,01428, 0,03869]`. |
| **Studi Ablatif (`6` skenario)** | `studi_ablatif_fitur.csv` | Utama (`teks_sastrawi`, `(1, 2)`, `3.000` fitur): CV *F1* `97,16%` (`97,1596%`); tanpa `token_apk`/`token_url`: turun `1,35` poin (`1,3512`) ke `95,81%` (RF `92,42%`), *holdout* `97,84%`; *unigram* saja: turun `1,22` poin (`1,2186`) ke `95,94%`; selisih CV dengan vs tanpa Sastrawi = `0,0006%` (`0,000627%`; `97,1596%` vs `97,1589%`). |
| **Bias Keyword Pajak (Tahap 4A)** | `tabel_komparasi_utama.csv` | Subset uji pajak `45` pesan (`21` resmi DJP + `24` *phishing*): kontrol `712` SMS umum -> `LinearSVC` *Acc* `42,22%`, *F1* `40,91%`, *ROC-AUC* `0,3571` (`FP=11`, spesifisitas `47,62%`, `FN=15`), RF *Acc* `33,33%`, *F1* `25,00%` (`FP=11, FN=19`). Korpus seimbang -> `LinearSVC` & RF *Acc* `95,56%`, *F1* `95,83%` (`FP=1, FN=1`), `LinearSVC` *ROC-AUC* `0,9960`, *Brier* `0,03289` (vs RF `0,9752` / `0,10914`). CV `260` baris pajak: `LinearSVC` *F1* `98,17% (± 2,56%)`, *Rec* `100,00%` vs RF *F1* `93,57% (± 3,03%)`. |
| **Lintas Korpus (Tahap 4B & 4C)** | `tabel_komparasi_utama.csv` | Tahap 4B (*zero-shot* `1.360` unik: `1.266` Theodorus + `94` Saragih `90:4`): `LinearSVC` *Rec* `80,28%`, *F1* `54,27%`, *Prec* `40,99%` (`FP=416`, spesifisitas Theodorus `58,40%`) vs RF *Rec* `60,00%`, *F1* `45,76%`. Tahap 4C (`2.519` unik, *holdout* `n=504`): `LinearSVC` *Acc* `96,03%` vs RF `92,46%`; 10-*Fold* CV `LinearSVC` `91,81% (± 2,19%)` vs RF `91,11% (± 2,58%)`. |
| **SHAP & Error (`n=232`)** | `fitur_teratas_svm_vs_rf.csv`, `shap_fitur_teratas_svm_vs_rf.csv`, `analisis_kesalahan_prediksi.csv` | Pemicu positif `LinearSVC`: `no` (`+2,2405`), `sms` (`+1,6940`), `rekening` (`+1,5083`), `info` (`+1,4054`), `segera` (`+1,3778`), `pin` (`+1,3729`), `token_apk` (`+1,3582`), `token_url` (`+1,3550`). Penahan negatif `LinearSVC`: `nama1` (`-1,2720`, `\|SHAP\| 0,0395`), `aku` (`-1,2206`, `\|SHAP\| 0,0575`), `resmi` (`-1,0706`, `\|SHAP\| 0,0341`), `yg` (`-0,8942`, `\|SHAP\| 0,0388`), `2016` (`-0,6664`). Galat gabungan `13` baris (`10` `LinearSVC` Platt, `8` RF, `5` irisan): `idx=1082` (`p=0,5506` tertahan `WASPADA` oleh rentang `0,50..0,74`, bundel produksi `1.159` -> `0,109`); `idx=960` (`p=0,424`, diekalasi `has_apk` ke `TINGGI`); `idx=314`/`102` (bobot `mandiri` `-0,7612`). |
| **Purwarupa & Latensi (Baru)** | `benchmark_latensi_purwarupa.json`, `tabel_pengujian_purwarupa.csv` | `pytest`: **`29/29 PASSED`** (`7,65` s: `16` uji API `UJI-01`–`UJI-09a`, `UJI-09b`, `UJI-11`–`UJI-16` + `13` uji data/model `UJI-10`). *Cold load* bundel: `118,166` ms; `predict_message` (`n=232`): *Mean* `13,763` ms (*Std* `1,261`, *P50* `13,537`, *P95* `15,919`, *P99* `18,400`, *Max* `19,898` ms); `POST /predict` (`n=232`): *Mean* `28,916` ms (*Std* `10,528`, *P50* `26,974`, *P95* `47,775`, *P99* `56,908`, *Max* `103,16` ms); `POST /predict/batch` (`50` pesan): `49,263` ms (`0,985` ms/pesan). |

### 21.2 Ringkasan Penyelesaian Temuan (`K4-01`–`K4-05`, `S4-01`–`S4-06`, `M4-01`–`M4-05`)

- **`K4-01`–`K4-05` (Kritis):** Menyinkronkan `ml/benchmark_purwarupa.py`, `tabel_pengujian_purwarupa.csv`, `Tabel L.11`, dan Bab IV Subbab 4.5 ke suite lengkap `29/29` uji (`7,65` s) + latensi terbaru; meluruskan mekanisme aktual `idx=1082` di `inference.py` (`is_official_djp_domain` melindungi `suspicious_domains`, bukan menimpa probabilitas `0,50..0,74`, tertahan di `WASPADA`); memperbaiki tautan gambar Lampiran 4 ke `../../aset-gambar/`; memulihkan rincian CV `2.519` (`91,81%` vs `91,11%`) dan catatan ketimpangan Saragih `90:4`; serta meluruskan definisi SHAP aktif *TreeExplainer* vs *LinearExplainer* (`Gambar 4.4`).
- **`S4-01`–`S4-06` (Sedang):** Meregenerasi `Gambar 4.5` (`1600×920`, API `v2.1.0`, `Scam 92%` / `0,9249`) dan `Gambar 4.6` (`1520×880`, simulasi MV3 dari `/simulasi-wa`, `Scam 84%`, `djponline.pajak.go.id` `Pola Chat Resmi / Normal` `0,1023`) tanpa menimpa `Gambar 1.1`/`2.1`/`3.1`/`L.1`; melengkapi uji McNemar (`p=0,7266`), Bootstrap 95% CI, waktu latih CV `0,0026`/`0,5357` s (`202,57`x) dan `0,0039`/`0,3096` s (`79,36`x), selisih ablatif `0,0006%`, implikasi sistem informasi (FP memblokir pengumuman resmi DJP vs FN meloloskan penipuan), serta batasan TKT Level 6 (`TestClient` *in-process*, DOM simulasi `/simulasi-wa`, belum UAT wajib pajak).
- **`M4-01`–`M4-05` (Minor):** Menyeragamkan gaya penulisan UNSIA (`di mana` dihapus, `linier -> linear`, paragraf berada di rentang 5–7 baris / 45–98 kata), memadankan istilah dan ejaan lintas `04-bab-4` & `06-lampiran.md` (`Tabel L.8`–`L.11`), serta memeriksa visual seluruh 6 PNG evaluasi + 2 PNG tangkapan layar purwarupa.

### 21.3 Hasil Verifikasi Akhir Bab IV & Lampiran 4

- **Kode & Uji Otomatis:** `ruff check ml app tests` lulus; `pytest -q` lulus `29 passed`; `ml/benchmark_purwarupa.py` selesai (`exit code 0`, regenerasi `benchmark_latensi_purwarupa.json`, `tabel_pengujian_purwarupa.csv`, `Gambar 4.5`, dan `Gambar 4.6`).
- **Pedoman UNSIA (`validate_unsia.py`):** `04-bab-4-hasil-dan-analisa.md` mandiri **`0 WARNING`**; `06-lampiran.md` mandiri **`0 WARNING`**; gabungan `Bab I..V + Lampiran` **`0 ERROR`** (`[1]`–`[36]` utuh) dan **`0 WARNING`** pada Bab I–IV & Lampiran (tersisa `[P186]` pada Bab V).
- **Humanisasi (`metrik.py --preset akademik` pada Bab IV):** Lulus **`9/9`** metrik utama beserta seluruh diagnostik kaidah & wacana.
- **Tindak Lanjut Sesi Berikutnya (Bab V & Ekspor Final `.docx`):**
  1. Sinkronkan `05-bab-5-kesimpulan/05-bab-5-kesimpulan.md` terhadap angka final Bab IV: rasio waktu latih CV `79,36` kali, `29` fungsi uji `pytest` dalam `7,65` detik, latensi `POST /predict` `28,916` ms (*P95* `47,775` ms), pelurusan mekanisme `idx=1082` (`is_official_djp_domain` tidak menimpa label pada probabilitas `0,50..0,74`, tertahan `WASPADA`), serta pemecahan/perluasan paragraf `[P186]` (`23` kata) hingga Bab V lulus `validate_unsia.py` (`0 ERROR, 0 WARNING`) dan `metrik.py --preset akademik`.
  2. Ekspor dan verifikasi berkas Word terpadu via `export_unsia_docx.py`.

---

## 22. Audit Akhir Sesi 5: Bab V, Daftar Pustaka, Sinkronisasi Lintas Naskah (≤ 30 Halaman), dan Ekspor Final DOCX (24 November 2026)

**Status Tahap Ini:** Seluruh rekomendasi audit Sesi 5 telah disetujui pengguna (*"Ringkas ke ≤ 30 halaman dan kerjakan semua yang anda rekomendasikan"*) dan selesai dieksekusi pada `00-bagian-awal.md`, `02-bab-2-landasan-metode.md`, `04-bab-4-hasil-dan-analisa.md`, `05-bab-5-kesimpulan.md`, `06-lampiran.md`, `glosarium-tugas-akhir-unsia.md`, `naskah-lengkap-tugas-akhir-ta-unsia.md`, serta seluruh berkas `.docx` terkait.

### 22.1 Ringkasan Perbaikan yang Dieksekusi

1. **Bab V (`05-bab-5-kesimpulan.md`):**
   - Menyelaraskan butir `5.1 a)`–`d)` ke Tujuan `1.4 a)`–`c)` dengan angka terkunci Sesi 4 (`random_state=42`, rasio latih `79,36` kali, *holdout* `95,69%` vs `96,55%` dengan McNemar `p = 0,7266`, *Brier Score* `0,02542` / *Log Loss* `0,09186`, `29` uji Pytest dalam `7,65` detik, latensi `POST /predict` rata-rata `28,916` ms dan *P95* `47,775` ms, TKT Level 6 pada simulasi, serta mekanisme aktual `idx=960` naik ke `TINGGI` dan `idx=1082` tertahan `WASPADA`).
   - Menurunkan Saran `5.2 a)`–`c)` langsung dari keterbatasan nyata Bab IV (penurunan presisi Tahap 4B `40,99%` / `FP=416`, galat `idx=314`/`idx=102`/`idx=1082`, dan batas verifikasi simulasi menuju TKT Level 7).
2. **Peringkasan Naskah Utama Bab I–V ke ≤ 30 Halaman & Pemolesan Lintas Bab:**
   - Memindahkan `Gambar 4.3` (Komparasi Lintas Korpus → `Gambar L.4`), `Gambar 4.4` (SHAP → `Gambar L.5`), `Gambar 4.6` (Ekstensi Chrome → `Gambar L.6`), serta `Tabel 4.2` (Komparasi Studi Terdahulu → `Tabel L.12`, dengan perbaikan `L-06`: CV *Acc* `97,74%` pada model non-Platt) ke Lampiran 4 (`06-lampiran.md`), dan menomori ulang tangkapan layar Web *Cek Pesan Pajak* di Bab IV menjadi `Gambar 4.3`.
   - Memperbaiki `L-02` (atribusi selisih *Brier Score* `39,68%` & *Log Loss* `42,12%` antarmodel), menghapus 12 kalimat penutup pendek (*punchline*, `L-04`), memperbaiki `L-05` (register formal pada `has_apk`), serta memadatkan Bab II dari `9` menjadi `8` halaman tanpa mengubah urutan sitasi `[1]`–`[36]` maupun Persamaan `(2.1)`–`(2.8)`.
   - Memperbarui `ABSTRAK` & `ABSTRACT` pada `00-bagian-awal.md` dengan hasil uji McNemar (`p = 0,7266`, tetap di bawah 200 kata), menyinkronkan `DAFTAR ISI`, `DAFTAR GAMBAR`, dan `DAFTAR TABEL` terhadap penomoran halaman Word aktual, serta memperbarui `glosarium-tugas-akhir-unsia.md` (`L-08`: `29/29` uji dalam `7,65` detik; latensi `28,916` ms / *P95* `47,775` ms).

### 22.2 Hasil Verifikasi Akhir Pasca-Sinkronisasi (24 November 2026)

- **Sitasi & Daftar Pustaka (`cek_konsistensi.py` + MCP `zoteus`):** Urutan kemunculan pertama `[1]`–`[36]` berurutan tanpa loncatan (`Bab I [1]–[24]`, `Bab II [25]–[36]`), yatim `0`, hilang `0`, `36/36` cocok terhadap koleksi Zotero `6WSLSX4K`, seluruh `15` tabel dan `12` gambar terindeks sinkron (`Jumlah temuan: 0`).
- **Kepatuhan Pedoman UNSIA (`validate_unsia.py`):**
  - `00-bagian-awal.md`: **`0 ERROR, 0 WARNING`**.
  - `05-bab-5-kesimpulan.md`: **`0 ERROR, 0 WARNING`**.
  - `naskah-lengkap-tugas-akhir-ta-unsia.md` (`328` blok, sitasi `[1]`–`[36]`): **`0 ERROR, 0 WARNING`** (`[OK] Lulus`).
- **Metrik Bahasa (`humanizer-indonesia/scripts/metrik.py --preset akademik`):** `00-bagian-awal.md`, `02-bab-2-landasan-metode.md`, `04-bab-4-hasil-dan-analisa.md`, dan `05-bab-5-kesimpulan.md` masing-masing **`9/9 LULUS`**.
- **Jumlah Halaman Word (`.docx` Terpadu):** Total dokumen `61` halaman; bagian isi **Bab I–V tepat `30` halaman** (Bab I hlm. `1–6`, Bab II hlm. `7–14`, Bab III hlm. `15–21`, Bab IV hlm. `22–28`, Bab V hlm. `29–30`; Daftar Pustaka hlm. `31–35`; Lampiran hlm. `36–50`), memenuhi rentang resmi UNSIA `10–30` halaman.

---

## 23. Revisi Pasca-Bimbingan Bab I–III & Penguatan Pembahasan Bab IV (28 November 2026)

**Status Tahap Ini:** Seluruh empat catatan bimbingan dosen untuk Bab I–III beserta penguatan pembahasan Bab IV telah diterapkan pada naskah `.md`, dikompilasi ke `.docx` serta `.pdf`, dan diverifikasi.

### 23.1 Ringkasan Perubahan Berdasarkan Masukan Bimbingan

1. **Batas 30 Halaman untuk Bab I–V:** Naskah terpadu (`naskah-lengkap-tugas-akhir-ta-unsia.docx` dan `.pdf`, total `61` halaman) terkonfirmasi menempatkan **Bab I–V tepat `30` halaman** (Bab I hlm. `1–6`, Bab II hlm. `7–14`, Bab III hlm. `15–21`, Bab IV hlm. `22–28`, Bab V hlm. `29–30`; Daftar Pustaka mulai hlm. `31`, Lampiran hlm. `36–50`).
2. **Halaman Pengesahan Satu Dosen Pembimbing (`00-bagian-awal.md`):** Menghapus baris `Dosen Pembimbing II` dan mengubah `Dosen Pembimbing I` menjadi `Dosen Pembimbing` untuk `(Novi Dian Nathasia, S.Kom., M.M.S.I.)` (tetap memakai ejaan gelar EYD V yang seragam dengan Kata Pengantar, Kaprodi `S.Kom., M.Kom.`, `api.py`, `app.js`, dan `test_prototipe_api.py`).
3. **Penomoran `1.4 Tujuan Penelitian` & Keselarasan dengan `1.2 Rumusan Masalah` (`01-bab-1-pendahuluan.md`):** Mengubah perincian Subbab `1.4` menjadi penomoran `1.`, `2.`, `3.` dengan kata kerja terukur (`Menyusun`, `Menguji dan membandingkan`, `Merancang, membangun, dan menguji`) yang dipetakan 1-ke-1 dengan Subbab `1.2` butir `a)`, `b)`, `c)`.
4. **Penguatan Pembahasan Perbandingan vs Kondisi Nyata di Bab IV (`04-bab-4-hasil-dan-analisa.md` & `05-bab-5-kesimpulan.md`):**
   - Menjelaskan implikasi lapangan pada Subbab `4.1–4.5`: responsivitas latih ulang `79,36×` saat modus *Coretax* berubah, dampak `FN=7` (risiko `.apk` lolos) vs `FP=3` (hambatan siaran DJP), risiko *alert fatigue* dari zona ragu *Random Forest* (`25,43%` vs `9,48%`), serta perbandingan kasus pesan nyata (`idx=1003` tertangkap `LinearSVC` `0,787` vs *Random Forest* `0,340`; `idx=960` `.apk` dieskalasi aturan `has_apk`; `idx=1082` dilindungi `is_official_djp_domain`; batas leksikal pada `idx=314`/`102`).
   - Menambahkan **`Tabel 4.2 Perbandingan Hasil Pengujian Penelitian terhadap Kondisi Nyata Operasional`** pada Subbab `4.5` (hlm. `27`) serta memperbarui `DAFTAR ISI`, `DAFTAR GAMBAR`, dan `DAFTAR TABEL` di `00-bagian-awal.md`.

### 23.2 Hasil Verifikasi Pasca-Revisi (28 November 2026)

- **`validate_unsia.py` (`naskah-lengkap-tugas-akhir-ta-unsia.md`):** `326` blok diperiksa, sitasi `[1]`–`[36]` berurutan utuh, **`0 ERROR, 0 WARNING`** (`[OK] Lulus`).
- **`humanizer-indonesia/scripts/metrik.py --preset akademik`:** `00-bagian-awal.md`, `01-bab-1-pendahuluan.md`, `04-bab-4-hasil-dan-analisa.md`, dan `05-bab-5-kesimpulan.md` masing-masing **`9/9 LULUS`** (Bab IV: rerata `18,4`, SD `6,9`, kalimat $\ge 28$ kata `5,9%`, *em/en-dash* `0`).
- **Verifikasi XML & Ekspor `.docx`/`.pdf`:** `Dosen Pembimbing II` terkonfirmasi absen, `Dosen Pembimbing` (`Novi Dian Nathasia, S.Kom., M.M.S.I.`) hadir, `1.4` bernomor `1.`, `2.`, `3.`, `Tabel 4.2` muncul `1` kali, serta `00-bagian-awal.pdf` (`10` hlm.), `01-bab-1-pendahuluan.pdf` (`13` hlm.), `04-bab-4-hasil-dan-analisa.pdf` (`7` hlm.), `05-bab-5-kesimpulan.pdf` (`3` hlm.), dan `naskah-lengkap-tugas-akhir-ta-unsia.pdf` (`61` hlm.) berhasil diekspor ulang. *(Catatan: berkas `Wan Mirza Dhani_Tugas Akir_Progress 26112026.docx` tidak disentuh karena sedang terbuka/terkunci oleh pengguna.)*

---

## 24. Perombakan Total Format Word Native, Eliminasi Artefak OneDrive, dan Audit Visual Penuh (28 November 2026)

**Status Tahap Ini:** Seluruh berkas `.docx` dan `.pdf` TA dibangun ulang dari nol memakai modul lokal [scripts/ekspor_naskah_unsia.py](../scripts/ekspor_naskah_unsia.py) melalui tahapan *staging* non-OneDrive (`%TEMP%\unsia_docx_build\<uuid>`) agar bebas konflik sinkronisasi OneDrive/Office Cache, memanfaatkan penuh fitur native Microsoft Word, serta diaudit menyeluruh secara OOXML dan visual halaman demi halaman.

### 24.1 Akar Masalah Sebelumnya & Perbaikan Pipeline Ekspor

1. **Eliminasi Konflik OneDrive Office File Cache:** Pembuatan serta otomasi Word COM (`$word.Documents.Open`, pembaruan daftar isi/gambar/tabel, repaginasi, dan ekspor PDF) sebelumnya menyentuh langsung folder tersinkronisasi OneDrive sehingga memicu *three-way auto-merge* (2 logo UNSIA di sampul, gambar menumpuk, dan duplikasi bab/paragraf). Pipeline baru merender, memproses Word COM, dan menambal metadata di direktori sementara lokal `%TEMP%`, lalu menyalin secara atomik ke `06-naskah-ta/`.
2. **Pemanfaatan Penuh Fitur Native Microsoft Word (`scripts/ekspor_naskah_unsia.py`):**
   - **Persamaan Matematika OMML Native:** Konverter rekursif LaTeX ke MathML lalu transformasi `MML2OMML.XSL` ke blok `<m:oMathPara>` / `<m:oMath>` berbahasa *Cambria Math* dengan penomoran kanan `(2.1)`–`(2.8)` (`8` persamaan tampilan + `42` ekspresi sebaris pada Bab II; total `50` `<m:oMath>` pada naskah terpadu).
   - **Daftar Native (`word/numbering.xml`):** Seluruh daftar huruf (`a)`, `b)`), angka (`1.`, `2.`, `3.`), dan butir memakai definisi abstrak/penomoran asli Word (`41` blok `<w:numPr>` pada naskah terpadu), bukan teks polos.
   - **Struktur Navigasi, Caption, dan Daftar Otomatis:** Menggunakan gaya bawaan `Heading 1`/`2`/`3` untuk *Navigation Pane*, gaya `Caption` / `Caption Tabel` dengan field `{ SEQ Gambar }` (`12` buah) dan `{ SEQ Tabel }` (`16` buah), serta field dinamis `{ TOC \o "1-3" \f C \h \z \u }` (`DAFTAR ISI`), `{ TOC \h \z \c "Gambar" }` (`DAFTAR GAMBAR`), dan `{ TOC \h \z \c "Tabel" }` (`DAFTAR TABEL`) dengan pembaruan gaya bawaan `toc 1`–`3` dan `table of figures` (`RightIndent = 1,35 cm`, *dot leader*, spasi seragam).
   - **Tabel Akademik & Bibliografi Rapi:** Grid lebar kolom tetap `14,0 cm` (`<w:tblHeader/>` berulang di tiap halaman sambungan, `<w:cantSplit/>` agar baris tidak terpotong antarhalaman, perataan kiri untuk tabel 2 kolom biodata, serta peluasan kolom pengenal garis bawah pada tabel ablatif `Tabel L.8`), dan daftar pustaka `[1]`–`[36]` IEEE rata gantung bertabulasi `\t`.
   - **Kompatibilitas, Bahasa Pemeriksa, & Metadata Autentik:** Mode kompatibilitas Word 2013+ (`compatibilityMode=15`), bahasa pemeriksa `id-ID` (`en-US` khusus `ABSTRACT`), nomor halaman `12 pt` pada seluruh bagian (`BAB I–V`, `DAFTAR PUSTAKA`, `LAMPIRAN`), Halaman Pengesahan 4 posisi dengan satu `Dosen Pembimbing` (`Novi Dian Nathasia, S.Kom., M.M.S.I.`), serta metadata `Application=Microsoft Office Word` (`16.0000`) dan `creator=Wan Mirza Dhani`.
   - **Perbaikan Format Glosarium (`glosarium-tugas-akhir-unsia.md`):** Memisahkan penanda tebal dan miring pada butir `Kode Billing`, `SHA-256 Checksum`, serta `ROC-AUC, PR-AUC, Brier Score, & Log Loss` agar tidak ada tanda `*` mentah yang bocor ke PDF.

### 24.2 Ringkasan Halaman & Verifikasi Akhir (28 November 2026)

- **Jumlah Halaman Final (`--all --print-page-map`):**
  - `00-bagian-awal.pdf`: `11` hlm. (`1.616` kata) | `01-bab-1-pendahuluan.pdf`: `6` hlm. (`1.499` kata) | `02-bab-2-landasan-metode.pdf`: `8` hlm. (`1.885` kata) | `03-bab-3-implementasi-metode.pdf`: `7` hlm. (`1.592` kata) | `04-bab-4-hasil-dan-analisa.pdf`: `7` hlm. (`1.545` kata) | `05-bab-5-kesimpulan.pdf`: `2` hlm. (`541` kata) | `06-lampiran.pdf`: `19` hlm. (`4.488` kata) | `glosarium-tugas-akhir-unsia.pdf`: `5` hlm. | `naskah-lengkap-tugas-akhir-ta-unsia.pdf`: **`60` hlm. (`13.163` kata)** dengan rincian **Bab I–V tepat `30` halaman** (`Bab I` hlm. `1–6`, `Bab II` hlm. `7–14`, `Bab III` hlm. `15–21`, `Bab IV` hlm. `22–28`, `Bab V` hlm. `29–30`; `DAFTAR PUSTAKA` hlm. `31–35`; `LAMPIRAN` hlm. `36–49`).
- **Audit OOXML (`.docx` `00`–`07`):** `0` token LaTeX mentah, `0` sisa Markdown bocor, `0` pesan kesalahan TOC/TOF, `0` `Dosen Pembimbing II`, tepat `1` logo sampul pada `00` dan `naskah-lengkap`, serta `WINWORD_COUNT=0` (tidak ada proses Word menggantung).
- **Kepatuhan, Bahasa, Lint, & Unit Test:** `validate_unsia.py` pada `naskah-lengkap-tugas-akhir-ta-unsia.md` lulus **`0 ERROR, 0 WARNING`** (`326` blok, `[1]`–`[36]` utuh); `metrik.py --preset akademik` pada `00-bagian-awal.md` lulus **`9/9 LULUS`**; `ruff check scripts/ekspor_naskah_unsia.py` lulus; `pytest -q` lulus **`29 passed`**.
- **Inspeksi Visual PDF & Berkas Terjaga:** Pemeriksaan visual atas seluruh PDF (`00` s.d. `08`, termasuk `naskah-lengkap-tugas-akhir-ta-unsia.pdf` hlm. `1–60`) memastikan `1` logo sampul, OMML utuh, `DAFTAR ISI`/`DAFTAR GAMBAR`/`DAFTAR TABEL` rapi tanpa tabrakan nomor halaman, `Tabel L.8` dan `Lampiran 5` (NIM rata kiri) bersih, serta berkas arsip/bimbingan pengguna (`Wan Mirza Dhani_Tugas Akir_Progress 26112026.docx`, `Tugas Akhir_Bab 3.pdf`, `Panduan-Bimbingan-TA-UNSIA.pdf`, dan `arsip-draf/*`) tetap utuh tidak tersentuh.


---

## 25. Penyelarasan Nama/Gelar Excel serta Revisi Total Tabel, Grafik, dan Bagan TA (28 November 2026)

**Status Tahap Ini:** Seluruh penamaan nama dan gelar telah diselaraskan terhadap berkas administrasi `01-administrasi/daftar-pembagian-dosen-pembimbing-ta.xlsx`, seluruh 16 tabel akademik (+ Lampiran 5) diperbarui menjadi ringkas (*to the point*) dengan tata letak Word profesional, seluruh 6 grafik Matplotlib (`ml/eksperimen_komparasi.py --plots-only`), 4 bagan (`scripts/buat_bagan_ta.py`), dan 2 tangkapan layar purwarupa (`ml/benchmark_purwarupa.py --screenshots-only`) dibangun ulang agar tajam dan terbaca jelas di kertas A4.

### 25.1 Penyelarasan Nama & Gelar Sesuai Excel Pembimbing
- **Dosen Pembimbing:** `Novi Dian Nathasia, S.Kom, MMSI.` (sapaan `Bapak` di Kata Pengantar & kode dipertahankan sesuai keputusan pengguna pada Bagian 6 / `K-01`).
- **Ketua Program Studi:** `Vika Febri Muliati, S.Kom., M.Kom`.
- **Wakil Rektor:** `Dr. Ucuk Darusalam, S.T., M.T`.
- Diterapkan konsisten pada `00-bagian-awal.md` (Halaman Pengesahan & Kata Pengantar), `app/backend/api.py`, `app/frontend/app.js`, `tests/test_prototipe_api.py`, `README.md`, `app/backend/catatan-penjelasan-aplikasi.md`, `02-proposal/draf-usulan-judul-ta.md`, dan `scripts/buat_dokumen_proposal.py`.

### 25.2 Revisi Mesin Render & Konten 16 Tabel Tugas Akhir
- **`scripts/ekspor_naskah_unsia.py`:** Menambahkan warna latar header `#EAEFF5`, garis pemisah sel tegas (`#B8C2CC`/`#CBD5E1`), sorotan penanda jadwal `✓` (`#E2E8F0`), penggabungan vertikal otomatis (*vertical merge*) untuk pasangan model pada `Tabel 4.1` dan `Tabel L.8` beserta penjagaan baris awal agar `Tabel 4.1` tidak terpotong baris yatim, perbaikan rata tengah kolom `:---:`, perluasan lebar kolom untuk nama berkas `.py`, dan perbesaran lebar gambar cetak ke `14,0 cm` (tinggi maks. `12,2 cm`).
- **Perampingan 16 Tabel (`Tabel 1.1`, `3.1`, `4.1`, `4.2`, `L.1`–`L.12`):** Menghapus tanda `/` ganda dua model per sel pada `Tabel 4.1` dan `Tabel L.8` menjadi pasangan baris bersih, menghapus `snake_case` dan pengulangan nama berkas uji di `Tabel L.7`, memadatkan seluruh deskripsi ke poin inti 1–3 baris tanpa pemenggalan kata/URL, serta menyinkronkan nomor halaman statis `DAFTAR ISI`, `DAFTAR GAMBAR`, dan `DAFTAR TABEL` pada `00-bagian-awal.md` (total naskah terpadu `59` halaman; **Bab I–V tetap tepat `30` halaman**).

### 25.3 Pembaruan 6 Grafik, 4 Bagan, & 2 Tangkapan Layar
- **6 Grafik Evaluasi (`ml/eksperimen_komparasi.py --plots-only`):** Dirancang khusus untuk lebar cetak `14,0 cm` (`figsize` `7,6–8,4` inci, `300 dpi`), latar putih bersih tanpa *top/right spines*, tanpa `suptitle` duplikat, desimal koma Indonesia, legenda gabungan di atas pada `Gambar 4.3`, anotasi zona ragu pada `Gambar 4.2`, serta tick sumbu-x rapi `0,01` pada `Gambar L.5`.
- **4 Bagan (`scripts/buat_bagan_ta.py`, `2400 px` lebar, `scale=3`):** `Gambar 1.1`, `Gambar 2.1`, `Gambar 3.1`, dan `Gambar L.1` dibangun ulang pada `viewBox` kompak `800 px` dengan latar putih bersih dan lulus `4/4 self_check.py = OK` serta `4/4 verify_geometry.py = 0 finding(s)`.
- **2 Tangkapan Layar (`ml/benchmark_purwarupa.py --screenshots-only`):** `Gambar 4.5` (`1360×900`, `2×`) dan `Gambar 4.6` (`1440×870`, `2×`) dirapatkan agar teks antarmuka, respons JSON, dan lencana hijau simulasi terbaca utuh.

---

## 26. Perapian Penamaan Berkas, Pembaruan Proposal, Pembersihan .venv/Arsip, dan Sinkronisasi Repositori

**Status Tahap Ini:** Seluruh penamaan berkas gambar, administrasi, referensi, serta video demo telah dirapikan, berkas proposal dan naskah terdampak dibangun ulang, lingkungan `.venv` beserta cache Python dan draf usang dihapus dari folder OneDrive, lalu seluruh pembaruan disinkronkan lewat *commit* atomik ke `origin/main`.

### 26.1 Perapian Penamaan & Pemindahan Berkas
- **Aset Gambar Naskah (`06-naskah-ta/aset-gambar/`):** Menyelaraskan 4 nama berkas gambar terhadap nomor keterangan di naskah: `Gambar 4.5 ... Web Cek Pesan Pajak ...` → `Gambar 4.3 ...`, `Gambar 4.3 ... Lintas Korpus ...` → `Gambar L.4 ...`, `Gambar 4.4 ... SHAP ...` → `Gambar L.5 ...`, dan `Gambar 4.6 ... Ekstensi Chrome ...` → `Gambar L.6 ...`, serta memperbarui rujukan di `04-bab-4-hasil-dan-analisa.md`, `06-lampiran.md`, `naskah-lengkap-tugas-akhir-ta-unsia.md`, dan `ml/benchmark_purwarupa.py`.
- **Administrasi, Daftar Pustaka, & Akar Proyek:** Memindahkan dan merapikan `Panduan-Bimbingan-TA-UNSIA.pdf` menjadi `01-administrasi/panduan-bimbingan-ta-unsia.pdf`; mengganti `Indeks Daftar Pustaka Bab I.md` menjadi `03-referensi/daftar-pustaka/indeks-daftar-pustaka.md` beserta menyelaraskan 6 awalan nomor PDF lokal (`26`, `27`, `28`, `30`, `31`, `34`); serta mengganti `Demo Website.mp4` menjadi `demo-website.mp4`.
- **Skrip & Dokumentasi:** Menghapus rujukan `arsip-draf` pada `scripts/terapkan_metadata_dokumen.py`, mengunci `UV_PROJECT_ENVIRONMENT` serta menghapus fallback `.venv` lokal pada `app/backend/jalankan-server.bat`, dan memutakhirkan struktur direktori serta perintah ekspor pada `README.md`.

### 26.2 Pembaruan Proposal, Ekspor Naskah Terdampak, & Pembersihan Workspace
- **Regenerasi Proposal & Naskah:** Membangun ulang `02-proposal/usulan-judul-ta-wan-mirza-dhani-240101020194.docx` dan `.pdf` (`2` hlm., `606` kata; gelar pembimbing sesuai Excel `Novi Dian Nathasia, S.Kom, MMSI.`) serta mengekspor ulang `04-bab-4` (`7` hlm.), `06-lampiran` (`18` hlm.), dan `07-naskah-lengkap` (`59` hlm., **Bab I–V tetap tepat `30` hlm.**) lewat `scripts/ekspor_naskah_unsia.py`.
- **Pembersihan Berkas Tak Terpakai & Bebas Sync OneDrive:** Menghapus permanen folder `.venv` (`376,09 MB` / `11.765` berkas; lingkungan kerja menggunakan `%LOCALAPPDATA%\venvs\ta-phishing-pajak-unsia`), `.pytest_cache`, `.ruff_cache`, seluruh `**/__pycache__`, `06-naskah-ta/docx/arsip-draf/`, `Wan Mirza Dhani_Tugas Akir_Progress 26112026.docx`, serta `Tugas Akhir_Bab 3.pdf`.
- **Verifikasi Akhir:** `validate_unsia.py` (`0 ERROR, 0 WARNING`, sitasi `[1]`–`[36]` lengkap), `ruff check --no-cache` (`All checks passed!`), `pytest -q` (`29 passed`), audit rujukan gambar Markdown (`26/26` valid), audit rujukan PDF indeks (`31/31` valid), audit OOXML proposal dan naskah lengkap (`13` media tertanam, bebas galat TOC dan `M.M.S.I.`), serta kebersihan folder (`VENV_EXISTS=False`, `DIRTY_DIRS=0`, `DIRTY_FILES=0`, `WINWORD_COUNT=0`).
