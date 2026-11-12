# Dokumentasi Dataset Penelitian

## 1. Struktur Data
Dataset disusun dalam dua komponen agar model mampu membedakan pola pesan normal, penipuan umum, dan penipuan spesifik otoritas perpajakan tanpa mengalami *bias* kata kunci:

1. **`raw_sms_spam_v1.csv`** (Korpus Dasar Publik)
   - **Sumber**: Repositori terbuka *Indonesian SMS Spam Dataset* (adaptasi korpus Yudi Wibisono / Rahmi).
   - **Jumlah**: 1.143 baris pesan berbahasa Indonesia.
   - **Label asli**: `0` = Normal (569), `1` = Penipuan/Fraud (335), `2` = Promo/Spam Iklan (239).
   - **Fungsi**: Memberikan fondasi struktur kalimat sehari-hari bahasa Indonesia dan pola penipuan umum (*smishing*).

2. **`dataset_pajak_curated.csv`** (Korpus Domain Perpajakan)
   - **Sumber**: Kurasi publik berdasarkan rilis imbauan resmi waspada penipuan Direktorat Jenderal Pajak (`pajak.go.id`), pemberitaan media nasional (`ddtc.co.id`, `pajakku.com`), serta format resmi komunikasi publik DJP (WA Blast resmi, Kring Pajak 1500200, dan percakapan normal bertema pajak).
   - **Jumlah Awal**: 40 baris (20 *Phishing* Perpajakan, 20 Resmi/Aman bertema pajak).
   - **Label**: `0` = Aman/Resmi, `1` = Phishing/Penipuan.
   - **Fungsi**: Mencegah model bias terhadap kata kunci domain (seperti "pajak", "NPWP", "Coretax", "SPT"). Dengan menyeimbangkan contoh pesan *phishing* dan pesan resmi yang sama-sama mengandung kata "pajak", model dipaksa mempelajari pola manipulasi (`.apk`, desakan waktu, tautan non-`pajak.go.id`, permintaan OTP/transfer).

---

## 2. Rencana Ekspansi Data (Tahap Lanjutan)
Untuk kebutuhan pelatihan model final Tugas Akhir:
- Menambah variasi korpus spesifik perpajakan hingga 150–300 baris dari arsip laporan penipuan publik (media sosial `@kring_pajak`, `@DitjenPajakRI`, portal aduan publik).
- Menggabungkan kelas `0` (Normal) dan `1` (Fraud/Phishing) dari korpus dasar + korpus domain perpajakan untuk skenario klasifikasi biner (*Aman* vs *Phishing*).
