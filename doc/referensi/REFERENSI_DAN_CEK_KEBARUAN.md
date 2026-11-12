# Daftar Referensi Jurnal & Hasil Cross-Check Kebaruan Judul

**Judul yang Diuji:**
> *"Komparasi Algoritma Support Vector Machine dan Random Forest dalam Deteksi Pesan Phishing WhatsApp Mengatasnamakan Otoritas Perpajakan"*

---

## 1. Kesimpulan Cross-Check Kebaruan (*Novelty / Research Gap*)

Berdasarkan penelusuran literatur ilmiah melalui indeks **OpenAlex** dan jurnal nasional/internasional hingga tahun 2026:
**Belum ditemukan penelitian yang identik secara utuh** menggabungkan seluruh elemen berikut:
1. Komparasi algoritma **Support Vector Machine (SVM)** dan **Random Forest (RF)** berbasis fitur **TF-IDF**,
2. Fokus pada platform pesan instan **WhatsApp** berbahasa Indonesia,
3. Domain spesifik **rekayasa sosial (*phishing*) mengatasnamakan otoritas perpajakan** (modus `.apk`, Coretax, pemadanan NIK-NPWP, tagihan pajak palsu), dan
4. Luaran **prototipe web deteksi mandiri**.

Penelitian yang sudah ada baru mencakup **irisan parsial** (masih membahas SMS umum, email berbahasa Inggris, fokus fitur URL saja, atau membahas penipuan pajak hanya dari sudut pandang hukum dan sosialisasi non-teknis).

---

## 2. Matriks Posisi Penelitian Terdahulu (Untuk Bab II Landasan Metode)

| No | Peneliti & Tahun | Fokus / Domain | Metode / Algoritma | Pembeda dengan Penelitian Ini (*Research Gap*) |
| :-: | :--- | :--- | :--- | :--- |
| 1 | Irawan et al. (2021) | Klasifikasi SMS Spam Umum (Indonesia) | SVM, Naive Bayes, Random Forest, Bagging | Fokus pada SMS promo/spam umum era lama; belum menyasar pola rekayasa sosial WhatsApp maupun modus perpajakan. |
| 2 | Theodorus et al. (2021) | Filtering SMS Spam Bahasa Indonesia | Machine Learning (SVM, NB, dll.) | Menggunakan data SMS umum tanpa memodelkan pola kalimat kedinasan formal seperti instansi pajak dan belum berwujud prototipe web. |
| 3 | Al Ghofany et al. (2022) | Deteksi SMS Spam Bahasa Indonesia | TF-RF + Support Vector Machine | Hanya menguji satu algoritma (SVM) dengan pembobotan TF-RF pada korpus SMS umum; tidak melakukan komparasi dengan Random Forest. |
| 4 | Astuti et al. (2024) | Klasifikasi Ham/Spam SMS | Komparasi Algoritma ML | Menggunakan korpus SMS umum, belum menargetkan pesan WhatsApp spesifik otoritas perpajakan. |
| 5 | Tampinongkol et al. (2024) | Deteksi Link Phishing | Random Forest & SVM | Menganalisis fitur leksikal URL tautan, bukan analisis konteks teks pesan WhatsApp. |
| 6 | Al Tawil et al. (2024) | Deteksi Email Phishing | TF-IDF, Word2Vec, BERT + ML | Fokus pada email berbahasa Inggris, bukan pesan singkat WhatsApp berbahasa Indonesia. |
| 7 | Efendi et al. (2025) | Deteksi Phishing WhatsApp | AI + Integrasi Bahasa Lokal Surabaya | Berfokus pada dialek lokal Surabaya, tidak membahas modus penipuan perpajakan maupun komparasi SVM vs Random Forest. |
| 8 | Saputra et al. (2026) | Deteksi Pesan Spam Bot WhatsApp | Support Vector Machine (SVM) | Berfokus pada integrasi bot spam umum dan hanya menguji SVM tanpa komparasi Random Forest serta bukan domain perpajakan. |
| 9 | Ningtias et al. (2026) | Deteksi Spam Email | TF-IDF + SVM dan Random Forest | Komparasi metodenya serupa, namun objek datanya adalah email spam umum, bukan pesan phishing WhatsApp bertema perpajakan. |
| 10 | Prakoso et al. (2026) | Penyalahgunaan Data Wajib Pajak untuk Phishing | Kajian Hukum / Regulasi | Membahas aspek hukum perlindungan data wajib pajak; tidak membangun model Machine Learning maupun sistem deteksi otomatis. |

---

## 3. Daftar Pustaka Format IEEE (Siap Pakai untuk Laporan UNSIA)

Berikut referensi terverifikasi yang dapat langsung disalin ke Bab I, Bab II, dan Daftar Pustaka (urutan penomoran `[1]`, `[2]`, dst. disesuaikan nanti dengan kemunculan pertama di naskah):

[1] D. Irawan, E. B. Perkasa, and Y. Yurindra, “Perbandingan Klassifikasi SMS Berbasis Support Vector Machine, Naive Bayes Classifier, Random Forest dan Bagging Classifier,” *Jurnal Sisfokom (Sistem Informasi dan Komputer)*, vol. 10, no. 3, 2021, doi: [10.32736/sisfokom.v10i3.1302](https://doi.org/10.32736/sisfokom.v10i3.1302).

[2] A. Theodorus, T. K. Prasetyo, R. Hartono, *et al.*, “Short Message Service (SMS) Spam Filtering using Machine Learning in Bahasa Indonesia,” in *East Indonesia Conference on Computer and Information Technology (EIConCIT)*, 2021, doi: [10.1109/eiconcit50028.2021.9431859](https://doi.org/10.1109/eiconcit50028.2021.9431859).

[3] M. S. Al Ghofany, R. Dwiyansaputra, F. Bimantoro, *et al.*, “Indonesian SMS Spam Detection Using TF-RF Feature Weighting Method and Support Vector Machine Classifier,” 2022, doi: [10.2991/978-94-6463-084-8_12](https://doi.org/10.2991/978-94-6463-084-8_12).

[4] E. Z. Astuti, C. A. Sari, E. H. Rachmawanto, *et al.*, “Comparative Study of Machine Learning Algorithms for Performing Ham or Spam Classification in SMS,” *Scientific Journal of Informatics*, vol. 11, no. 1, 2024, doi: [10.15294/sji.v11i1.47364](https://doi.org/10.15294/sji.v11i1.47364).

[5] F. F. Tampinongkol, A. R. Kamila, and A. C. Wardhana, “Implementation of Random Forest Classification and Support Vector Machine Algorithms for Phishing Link Detection,” *Journal of Informatics Information System Software Engineering and Applications (INISTA)*, vol. 7, no. 1, 2024, doi: [10.20895/inista.v7i1.1588](https://doi.org/10.20895/inista.v7i1.1588).

[6] A. Al Tawil, L. H. Almazaydeh, D. Qawasmeh, *et al.*, “Comparative Analysis of Machine Learning Algorithms for Email Phishing Detection Using TF-IDF, Word2Vec, and BERT,” *Computers, Materials & Continua*, 2024, doi: [10.32604/cmc.2024.057279](https://doi.org/10.32604/cmc.2024.057279).

[7] F. M. Efendi, A. K. Adisusilo, and S. Budiprayitno, “Pengembangan Sistem Deteksi Phishing pada WhatsApp Berbasis AI dengan Integrasi Bahasa Lokal Surabaya,” *Melek IT Information Technology Journal*, vol. 11, no. 1, 2025, doi: [10.30742/melekitjournal.v11i1.417](https://doi.org/10.30742/melekitjournal.v11i1.417).

[8] R. B. Saputra, M. Azwar, and L. Widyawati, “Implementasi Algoritma SVM pada Bot WhatsApp untuk Deteksi Pesan Spam,” *Jurnal Manajemen Informatika dan Sistem Informasi*, vol. 9, no. 1, 2026, doi: [10.36595/misi.v9i1.1803](https://doi.org/10.36595/misi.v9i1.1803).

[9] A. A. Ningtias, N. Anwar, and A. Ichwani, “Komparasi Kinerja Support Vector Machine dan Random Forest untuk Deteksi Spam Email Berbasis TF-IDF Teks,” *IKRA-ITH Informatika: Jurnal Komputer dan Informatika*, 2026.

[10] M. A. Sembiring, M. F. L. Sibuea, and A. Anjani, “Optimasi Model Klasifikasi Pesan Penipuan Digital Berbahasa Indonesia Menggunakan XGBoost dengan Bayesian Optimization dan SMOTE,” *Journal of Science and Social Research*, vol. 9, no. 3, 2026, doi: [10.54314/jssr.v9i3.7212](https://doi.org/10.54314/jssr.v9i3.7212).

[11] N. B. Prakoso, H. Ayu, and H. Zakaria, “Misuse of Taxpayer Data for Phising Scams,” *Journal of International Islamic Law, Human Right and Public Policy*, 2026, doi: [10.5281/zenodo.21853028](https://doi.org/10.5281/zenodo.21853028).

[12] R. Alabdan, “Phishing Attacks Survey: Types, Vectors, and Technical Approaches,” *Future Internet*, vol. 12, no. 10, p. 168, 2020, doi: [10.3390/fi12100168](https://doi.org/10.3390/fi12100168).
