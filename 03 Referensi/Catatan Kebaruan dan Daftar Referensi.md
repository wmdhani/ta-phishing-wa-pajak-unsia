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
| 11 | Sembiring et al. (2026) | Klasifikasi Pesan Penipuan Digital Indonesia | XGBoost + Bayesian Optimization + SMOTE | Berfokus pada penipuan digital lintas topik tanpa pengkhususan tema perpajakan maupun perbandingan dengan SVM dan Random Forest. |

---

## 3. Daftar Pustaka Format IEEE (Siap Pakai untuk Laporan UNSIA)

Berikut referensi terverifikasi yang dapat langsung disalin ke Bab I, Bab II, dan Daftar Pustaka (urutan penomoran `[1]`, `[2]`, dst. disesuaikan nanti dengan kemunculan pertama di naskah):

[1] D. Irawan, Hamidah, E. B. Perkasa, Yurindra, D. Wahyuningsih, and E. Helmud, “Perbandingan klassifikasi SMS berbasis Support Vector Machine, Naive Bayes Classifier, Random Forest dan Bagging Classifier,” *Jurnal Sisfokom (Sistem Informasi dan Komputer)*, vol. 10, no. 3, pp. 432-437, Dec. 2021, doi: [10.32736/sisfokom.v10i3.1302](https://doi.org/10.32736/sisfokom.v10i3.1302).

[2] A. Theodorus, T. K. Prasetyo, R. Hartono, and D. Suhartono, “Short Message Service (SMS) spam filtering using machine learning in Bahasa Indonesia,” in *Proc. 3rd East Indonesia Conf. Comput. Inf. Technol. (EIConCIT)*, Apr. 2021, pp. 199-203, doi: [10.1109/EIConCIT50028.2021.9431859](https://doi.org/10.1109/EIConCIT50028.2021.9431859).

[3] M. S. Al Ghofany, R. Dwiyansaputra, F. Bimantoro, and Khairunnas, “Indonesian SMS spam detection using TF-RF feature weighting method and Support Vector Machine classifier,” in *Proc. First Mandalika Int. Multi-Conf. Sci. Eng. (MIMSE-I-C)*, 2022, pp. 117-129, doi: [10.2991/978-94-6463-084-8_12](https://doi.org/10.2991/978-94-6463-084-8_12).

[4] E. Z. Astuti, C. A. Sari, E. H. Rachmawanto, and R. R. Ali, “Comparative study of machine learning algorithms for performing ham or spam classification in SMS,” *Scientific Journal of Informatics*, vol. 11, no. 1, pp. 177-186, Feb. 2024, doi: [10.15294/sji.v11i1.47364](https://doi.org/10.15294/sji.v11i1.47364).

[5] F. F. Tampinongkol, A. R. Kamila, A. C. Wardhana, A. W. C. Kusuma, and D. Revaldo, “Implementation of Random Forest classification and Support Vector Machine algorithms for phishing link detection,” *Journal of Informatics Information System Software Engineering and Applications (INISTA)*, vol. 7, no. 1, pp. 127-137, Nov. 2024, doi: [10.20895/inista.v7i1.1588](https://doi.org/10.20895/inista.v7i1.1588).

[6] A. Al Tawil, L. H. Almazaydeh, D. Qawasmeh, B. Qawasmeh, M. Alshinwan, and K. Elleithy, “Comparative analysis of machine learning algorithms for email phishing detection using TF-IDF, Word2Vec, and BERT,” *Computers, Materials & Continua*, vol. 81, no. 2, pp. 3395-3412, Nov. 2024, doi: [10.32604/cmc.2024.057279](https://doi.org/10.32604/cmc.2024.057279).

[7] F. M. Efendi, A. K. Adisusilo, and S. Budiprayitno, “Pengembangan sistem deteksi phishing pada WhatsApp berbasis AI dengan integrasi bahasa lokal Surabaya,” *Melek IT Information Technology Journal*, vol. 11, no. 1, pp. 101-112, Jun. 2025, doi: [10.30742/melekitjournal.v11i1.417](https://doi.org/10.30742/melekitjournal.v11i1.417).

[8] R. B. Saputra, M. Azwar, L. Widyawati, Husain, and K. A. Latif, “Implementasi algoritma SVM pada bot WhatsApp untuk deteksi pesan spam,” *Jurnal Manajemen Informatika dan Sistem Informasi*, vol. 9, no. 1, pp. 39-51, Jan. 2026, doi: [10.36595/misi.v9i1.1803](https://doi.org/10.36595/misi.v9i1.1803).

[9] A. A. Ningtias, N. Anwar, A. Ichwani, and R. T. Iswahyudi, “Komparasi kinerja Support Vector Machine dan Random Forest untuk deteksi spam email berbasis TF-IDF teks,” *IKRA-ITH Informatika: Jurnal Komputer dan Informatika*, vol. 10, no. 3, pp. 45-51, Nov. 2026.

[10] M. A. Sembiring, M. F. L. Sibuea, and Anjani, “Optimasi model klasifikasi pesan penipuan digital berbahasa Indonesia menggunakan XGBoost dengan Bayesian Optimization dan SMOTE,” *Journal of Science and Social Research*, vol. 9, no. 3, pp. 5329-5336, Jun. 2026, doi: [10.54314/jssr.v9i3.7212](https://doi.org/10.54314/jssr.v9i3.7212).

[11] N. B. Prakoso, H. Ayu, and H. Zakaria, “Misuse of taxpayer data for phising scams,” *Journal of International Islamic Law, Human Rights, and Public Policy*, vol. 4, no. 3, pp. 1560-1569, Jul. 2026, doi: [10.5281/zenodo.21853029](https://doi.org/10.5281/zenodo.21853029).

[12] R. Alabdan, “Phishing attacks survey: Types, vectors, and technical approaches,” *Future Internet*, vol. 12, no. 10, p. 168, Oct. 2020, doi: [10.3390/fi12100168](https://doi.org/10.3390/fi12100168).
