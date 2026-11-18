# Catatan Penjelasan Aplikasi Cek Pesan Pajak untuk Bimbingan TA UNSIA

**Penulis:** Wan Mirza Dhani (240101020194)  
**Dosen Pembimbing:** Bapak Novi Dian Nathasia, S.Kom., MMSI  
**Tautan Live (Utama - Railway):** https://cek-pesan-pajak-production.up.railway.app  
**Tautan Cadangan (Render):** https://cek-pesan-pajak.onrender.com  
**Repositori GitHub:** https://github.com/wmdhani/ta-phishing-wa-pajak-unsia  

---

## 1. Kalimat Pembuka (Gambaran Besar dalam 15 Detik)

> *"Pak, aplikasi **Cek Pesan Pajak** ini saya rancang dengan dua sisi. Sisi depan saya buat sesimpel mungkin untuk masyarakat awam supaya mereka tinggal paste chat WA, langsung tahu bahaya atau aman beserta alasannya. Di balik layar, sistemnya ditenagai model **LinearSVC** yang digabung dengan aturan keamanan khusus pajak (cek file `.apk` dan domain `pajak.go.id`), plus ruang khusus **Info Akademik** di pojok bawah kanan untuk melihat pembuktian riset dan komparasi model."*

---

## 2. Penjelasan Tiap Komponen

### A. Tampilan Web Pengguna (`06 Prototipe Aplikasi/web/`)
- **Berkas:** `index.html`, `app.js`, `styles.css`.
- **Kenapa dipisah jadi 3 tab?** Supaya orang awam tidak bingung. Tab **Cek Pesan** untuk periksa chat, **Web Resmi & Ciri Scam** untuk edukasi cek domain DJP, dan **Darurat .apk** khusus panduan pertolongan pertama kalau user telanjur *install* file berbahaya.
- **Tampilan hasil dibuat to-the-point:** Begitu chat dicek, muncul status tegas (`BAHAYA / SCAM`, `WASPADA`, atau `AMAN`), pratinjau chat yang otomatis menandai warna pada file `.apk` atau link, lalu dua kotak singkat: **Kenapa?** dan **Solusi**. Tersedia juga tombol **Copy Alert** / **Share WA** supaya warga bisa langsung memperingatkan grup keluarga.
- **Sisi keamanan frontend:** Teks yang dikirim user tidak disimpan di database mana pun. Seluruh teks ditampilkan memakai `textContent`, bukan HTML mentah, supaya aman dari serangan *Cross-Site Scripting* (XSS).
- **Bagian khusus dosen (Modal Info Akademik):** Disembunyikan di tombol footer kanan bawah agar tidak mengganggu orang awam, berisi 3 sub-tab:
  1. **Summary:** ringkasan dataset (1.164 chat), akurasi utama (`97,42%` *holdout*; `97,73%` khusus chat pajak), dan 6 baris inti perbandingan `LinearSVC` vs `Random Forest` (bisa dibuka semua 19 baris lewat tombol `Show All 19 Rows`).
  2. **Live XAI Check:** membedah chat yang baru dicek, membandingkan skor `LinearSVC` vs `Random Forest` secara langsung, lengkap dengan 6 kata pemicu terkuat dan hasil pemotongan kata Sastrawi.
  3. **Demo WA Extension:** simulasi cara kerja ekstensi *WhatsApp Web* langsung di dalam modal (plus mode layar penuh di `/simulasi-wa`).

### B. "Otak" Pembersih Teks & Prediksi (`src/eksperimen_baseline.py`, `inference.py`, `model_phishing_pajak.joblib`)
- **Pembersihan teks yang konsisten:** Chat yang masuk dibersihkan dulu memakai fungsi yang persis sama seperti waktu melatih model. Kata berimbuhan dipotong ke kata dasar memakai Sastrawi, sedangkan `.apk` dan link website diganti jadi penanda khusus (`token_apk` dan `token_url`). File `.apk` diproses duluan sebelum link supaya file seperti `coretax.id.apk` tidak salah dianggap website.
- **Model yang dipakai:** File `model_phishing_pajak.joblib` (sekitar 1,19 MB) berisi kamus TF-IDF 3.000 kata/frasa dan dua model: **LinearSVC terkalibrasi Platt** sebagai model utama, serta **Random Forest** sebagai pembanding. Model dimuat satu kali ke memori (`cache`), jadi setiap cek pesan hanya butuh hitungan belasan milidetik di lokal (sekitar `66 ms` di Railway).
- **Hybrid AI + Aturan Pajak:**
  1. **Aturan `.apk`:** Jika ada lampiran `.apk`, risiko otomatis dipaksa menjadi **BAHAYA / SCAM**, karena DJP tidak pernah mengirim aplikasi lewat WhatsApp.
  2. **Aturan domain resmi `pajak.go.id`:** Sistem hanya mengakui domain yang persis `pajak.go.id` atau berakhiran `.pajak.go.id`. Jebakan seperti `pajak.go.id.verifikasi.xyz` tetap ditandai mencurigakan. Angka jam (`17.00`) atau nominal uang (`Rp1.500.000`) dijaga agar tidak salah dianggap alamat web.
- **Alasan otomatis (XAI):** Sistem melihat bobot tiap kata di `LinearSVC`, membuang kata pajak netral (seperti *pajak* atau *NPWP*), lalu mengambil kata pemicu bernada mendesak atau ancaman (seperti *segera*, *denda*, *unduh*) untuk dijelaskan ke user dengan bahasa awam.

### C. Peladen / Jembatan Backend (`06 Prototipe Aplikasi/api.py`)
- Backend dibangun memakai **FastAPI** sebagai jembatan antara web/ekstensi dan model Python.
- **Startup cepat:** Begitu server menyala (`lifespan`), model dan kamus Sastrawi langsung dipanaskan di memori supaya pengguna pertama tidak menunggu lama.
- **Pengaman API:** Input dibatasi maksimal 5.000 karakter, setiap IP dibatasi maksimal 60 kali cek per menit supaya server tidak mudah di-spam (*rate limit*), dan respons dilengkapi *security header* standar web (`X-Content-Type-Options: nosniff`, `X-Frame-Options: SAMEORIGIN`, `Referrer-Policy`, `Permissions-Policy`).

### D. Ekstensi Chrome WhatsApp Web (`06 Prototipe Aplikasi/extension/`)
- Berkas: `manifest.json`, `content.js`, `background.js`, `popup.html`, `popup.js`, `styles.css`, dan `simulasi_whatsapp_web.html`.
- `content.js` memantau gelembung chat baru yang muncul di `web.whatsapp.com` (mengabaikan daftar chat di samping dan teks kutipan/reply), lalu menempelkan tombol **Cek Pesan Pajak** tepat di dalam chat.
- Saat tombol diklik, `background.js` mengirim teks ke API dan hasilnya langsung muncul sebagai lencana merah/kuning/hijau di bawah chat, tanpa user perlu copy-paste.

### E. Deployment Cloud & Pengujian (`Dockerfile`, `railway.json`, `render.yaml`, `tests/test_prototipe_api.py`)
- **Dockerfile** memakai `python:3.11-slim`, hanya menginstal 8 library inti produksi dari `requirements-deploy.txt`, berjalan sebagai user non-root `appuser`, dan tidak membutuhkan `pandas` saat inferensi sehingga container ringan dan cepat dibangun.
- **Pengujian Otomatis:** Seluruh fungsi API, deteksi `.apk`, anti-spoofing domain, penjagaan angka jam `17.00`, *rate limiter*, *security header*, dan halaman web terverifikasi lulus lewat **21 skenario `pytest`**.

---

## 3. Contekan Tanya-Jawab Bimbingan

| Pertanyaan yang Mungkin Muncul | Jawaban Singkat |
| :--- | :--- |
| *"Kenapa pakai LinearSVC, tidak Random Forest saja?"* | *"Pada teks pendek berbahasa Indonesia dengan 3.000 fitur TF-IDF yang banyak nilai nolnya, LinearSVC jauh lebih presisi memisahkan imbauan resmi pajak (`97,73%`) daripada Random Forest (`88,64%`). Random Forest sering salah menuduh chat resmi yang punya link `pajak.go.id`. LinearSVC juga ratusan kali lebih cepat dilatih dan bobot katanya transparan untuk XAI."* |
| *"Kalau penipu pakai domain mirip seperti `pajak.go.id.verifikasi.xyz` bagaimana?"* | *"Sistem mengecek bagian akhiran host yang benar-benar persis `pajak.go.id` atau `.pajak.go.id`. Karena akhiran domain di contoh itu `.xyz`, sistem langsung menandainya sebagai domain mencurigakan."* |
| *"Apakah angka jam seperti `17.00` atau uang `Rp1.500.000` bisa salah dianggap link?"* | *"Sudah dicegah, Pak. Pola regex link kami mensyaratkan akhiran huruf domain asli (seperti `.com`, `.id`, `.xyz`), jadi angka dengan titik seperti jam atau rupiah tidak akan terdeteksi sebagai URL."* |
| *"Apa keterbatasan aplikasi yang sekarang?"* | *"Dua hal, Pak: pertama, ekstensi Chrome saat ini masih diarahkan ke server lokal (`localhost:8000`) sedangkan aplikasi webnya sudah online di Railway; kedua, pembatas spam (*rate limiter*) masih disimpan di memori satu server, jadi kalau suatu saat sistem diperbesar ke banyak server sekaligus, penghitungnya perlu dipindah ke Redis."* |
