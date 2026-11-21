# BAB V KESIMPULAN

## 5.1 Kesimpulan

Berdasarkan rangkaian kurasi data, pemodelan komparatif, pengujian ketahanan bias, dan validasi purwarupa sistem terpadu, diperoleh tiga kesimpulan yang menjawab tujuan penelitian sebagai berikut:

a) Penggabungan 260 pesan pajak berimbang dari 65 arsip publik bersama 904 SMS umum menghasilkan korpus induk 1.164 baris. Penyaringan duplikat Sastrawi lalu menyisakan 1.159 teks unik. Pelestarian `token_apk` serta `token_url` dalam ekstraksi TF-IDF `(1, 2)` 3.000 fitur terbukti esensial. Penghapusan token entitas memangkas *F1-Score* 10-Fold CV `LinearSVC` sebesar 1,35 poin (`97,16%` ke `95,81%`), sedangkan pembatasan unigram menurunkannya 1,22 poin (`95,94%`).

b) Model `LinearSVC` Platt (`C=2,0`) mengungguli *Random Forest* (`n_estimators=100`) pada 10-Fold CV (*F1-Score* `97,16% ± 2,41%` vs `94,07% ± 2,92%`) dan *ROC-AUC* (`0,9957` vs `0,9936`). Model ini mencatat *Brier Score* `0,02542` dan *Log Loss* `0,09186` (turun `39,68%` dan `42,12%`). Pelatihannya berjalan 106,6 kali lebih cepat serta unggul pada korpus 2.519 baris (`96,03%` vs `92,46%`). Pada uji kontrol 45 pesan pajak, model SMS umum (`712` latih) hanya meraih akurasi `42,22%` untuk `LinearSVC` (`11/21` pesan DJP terblokir) dan `33,33%` bagi *Random Forest*. Sebaliknya, penyeimbangan korpus mengangkat keduanya ke akurasi `95,56%` (`20/21` pesan resmi lolos) dengan *F1-Score* CV 260 pajak `98,17%`.

c) Purwarupa terpadu menyatukan `LinearSVC` Platt bersama penjaga `.apk` dan daftar putih `pajak.go.id` ke dalam FastAPI, web *Cek Pesan Pajak*, serta ekstensi *WhatsApp Web* (*Manifest V3*). Integrasi tersebut menutup kelemahan TF-IDF murni pada kasus `idx=960` dan `idx=1082`. Seluruh 23 pengujian Pytest lulus dalam 21,51 detik dengan latensi `POST /predict` rata-rata `34,991` ms (*P95* `48,082` ms) sehingga memenuhi kriteria TKT Level 6.

## 5.2 Saran

Untuk pengembangan riset dan adopsi sistem lebih lanjut, diajukan tiga rekomendasi terarah berikut:

a) Korpus latih perlu diperbarui secara berkala memakai pesan layanan Coretax DJP mutakhir agar penurunan presisi lintas periode (`Stage 4B`: `40,99%`, `FP = 416`) dapat ditekan. Langkah ini sebaiknya dipadukan dengan normalisasi entitas *Named Entity Recognition* (NER) guna menghilangkan artefak korpus lama seperti `nama1` dan `2016`.

b) Fitur deteksi multi-sinyal di luar batas teks saat ini layak dieksplorasi pada riset berikutnya. Peneliti selanjutnya dapat menambahkan ekstraksi *Optical Character Recognition* (OCR) atas tangkapan layar surat palsu dan pemeriksaan reputasi domain WHOIS. Evaluasi model bahasa terkuantisasi seperti IndoBERT juga relevan untuk mendeteksi penipuan transfer super singkat tanpa tautan (`idx=314` dan `idx=102`).

c) Evaluasi *User Acceptance Testing* (UAT) bersama wajib pajak secara terbatas disarankan untuk menguji keterbacaan alasan awam di lapangan. Pemeliharaan berkala selektor DOM pada `content.js` ekstensi *Manifest V3* juga dibutuhkan mengikuti pembaruan antarmuka *WhatsApp Web*.
