# BAB V KESIMPULAN

## 5.1 Kesimpulan

Penelitian ini menjawab tiga tujuan bernomor pada Subbab 1.4 berdasarkan eksperimen dengan pengacak tetap `random_state=42`. Seluruh temuan bersumber dari korpus kurasi campuran (77,66% SMS umum tahun 2016 serta 22,34% pesan pajak rekonstruksi) dan validasi purwarupa sistem pada simulasi lokal. Rincian keempat simpulan beserta padanan kondisi nyatanya tersaji pada butir berikut:

a) Tujuan pertama (butir 1) tercapai lewat penyusunan 260 pesan pajak berimbang dari 65 sumber publik 2021–2026 (130 *phishing* 12 modus, 130 aman) bersama 904 SMS umum menjadi 1.159 teks unik. Uji ablatif menetapkan setelan utama menurut CV `LinearSVC` (97,16%, turun ke 95,81% tanpa token entitas; Sastrawi bergeser 0,0006%). Kebutuhan daftar putih domain di lapangan pun menjustifikasi pelestarian `token_apk` dan `token_url`.

b) Tujuan kedua (butir 2) menempatkan `LinearSVC` (`C=2.0`) sebagai model utama dengan *F1-Score* 10-*Fold* CV 97,16% (± 2,41%) versus 94,07% (± 2,92%) pada *Random Forest*, latih 79,36 kali lebih cepat, serta akurasi korpus diperluas 96,03% melawan 92,46%. Pada *holdout* (`n = 232`), selisih akurasi tidak bermakna (95,69% vs 96,55%; McNemar p = 0,7266). Namun, `LinearSVC` unggul kalibrasi (*Brier* 0,02542 vs 0,04214; zona ragu 9,48% vs 25,43%) dan menangkap kasus `idx=1003` yang luput di *Random Forest*.

c) Uji kontrol dalam Tujuan kedua (butir 2) membuktikan peran korpus pajak berimbang dalam menekan bias kata kunci lapangan. Pelatihan 712 SMS umum saja hanya memberi akurasi 42,22% untuk `LinearSVC` pada 45 pesan pajak *holdout* (11 dari 21 pesan aman/resmi terblokir) dan 33,33% untuk *Random Forest*. Penambahan korpus pajak lalu mengangkat keduanya ke 95,56% (20 dari 21 pesan aman lolos), sedangkan pada *zero-shot* 1.360 pesan eksternal *Recall* `LinearSVC` mencapai 80,28% dengan presisi 40,99% (`FP=416`).

d) Tujuan ketiga (butir 3) terwujud lewat purwarupa terpadu yang memadukan bundel `LinearSVC` Platt, aturan `.apk`, serta daftar putih `pajak.go.id` pada FastAPI, web *Cek Pesan Pajak*, dan ekstensi *WhatsApp Web* (*Manifest V3*). Sebanyak 29 uji Pytest lulus dalam 7,88 detik dengan rerata `POST /predict` 35,651 ms (*P95* 52,524 ms; maks. 62,120 ms). Aturan `.apk` menaikkan `idx=960` ke `TINGGI`, sedangkan `idx=1082` turun ke 0,109 di bundel produksi, memenuhi TKT Level 6 pada simulasi.

## 5.2 Saran

Rekomendasi berikut diturunkan langsung dari keterbatasan nyata pada Bab IV. Keterbatasan tersebut meliputi penurunan presisi lintas korpus, kegagalan fitur leksikal tanpa tautan, serta batas verifikasi pada simulasi lokal. Saran ini ditujukan bagi peneliti lanjutan dan pengelola layanan publik perpajakan. Usulan pengembangan selanjutnya mencakup butir berikut:

a) Pada uji *zero-shot* Tahap 4B, presisi `LinearSVC` turun ke 40,99% (`FP = 416`) akibat pergeseran gaya bahasa antarkorpus dan antarperiode. Korpus latih perlu diperbarui berkala memakai siaran resmi Coretax mutakhir serta pesan penipuan asli aduan warga. Himpunan uji pajak juga perlu diperluas melampaui 45 pesan, disertai normalisasi artefak seperti `nama1` dan `2016`.

b) Galat `idx=314` dan `idx=102` memperlihatkan batas fitur leksikal TF-IDF pada permintaan transfer tanpa tautan maupun `.apk`. Studi lanjutan dapat menguji model kontekstual seperti IndoBERT sambil menjaga latensi di bawah 50 ms. Ambang peluang 0,50 sampai 0,74 juga perlu ditinjau ulang agar kasus `idx=1082` tidak menerima peringatan, di samping menelaah lampiran gambar pada Subbab 1.3.

c) Latensi baru diukur lewat `TestClient` *in-process*, sedangkan ekstensi baru berjalan pada simulasi DOM `/simulasi-wa`. Tahap berikutnya perlu mengukur latensi jaringan nyata, menguji ekstensi pada `web.whatsapp.com`, serta memelihara selektor DOM `content.js`. *User Acceptance Testing* bersama wajib pajak turut dibutuhkan untuk menguji keterbacaan alasan awam menuju TKT Level 7.
