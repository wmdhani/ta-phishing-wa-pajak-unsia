# Dokumentasi Dataset dan Provenans Sumber Data Tugas Akhir

Dokumen ini merinci seluruh berkas data mentah (*raw data*), berkas data olahan (*processed & curated data*), metode ekstraksi (*web scraping*), serta rujukan asal sumber data untuk penelitian Tugas Akhir:

> **Judul Tugas Akhir**: Komparasi Algoritma Support Vector Machine dan Random Forest dalam Deteksi Pesan Phishing WhatsApp Mengatasnamakan Otoritas Perpajakan

Seluruh data dalam repositori ini bersumber dari publikasi resmi pemerintah, repositori ilmiah terbuka berlisensi jelas, portal cek fakta pemerintah daerah, dan media perpajakan nasional terverifikasi. Tidak ada data rahasia internal wajib pajak yang digunakan.

---

## 1. Arsitektur dan Struktur Direktori Data

```text
04 Dataset/
├── README Dataset.md                                       # Dokumentasi lengkap dataset & asal sumber data
├── 01 Data Mentah/                                         # Direktori seluruh file mentah (raw data)
│   ├── DJP Hasil Scrape 68 Sumber Resmi.json               # Teks & metadata hasil scraping 68 halaman resmi pajak
│   ├── DJP Ringkasan Scrape 68 Sumber Resmi.csv            # Tabel ringkasan metadata & SHA-256 68 halaman hasil scrape
│   ├── DJP Snapshot Scrape Mentah.json                     # Salinan mentah tangkapan HTML/teks hasil scraper
│   ├── DJP Indikator Penipuan dan Kanal Resmi.json         # Ekstraksi domain phishing, nomor WA penipu, & kanal resmi DJP
│   ├── Rahmi 2016 Korpus SMS Spam Utama v1.csv             # Korpus dasar utama (Rahmi & Wibisono, 2016 - 1.143 baris)
│   ├── Rahmi 2016 Arsip Asli SMS Spam.csv                  # Arsip asli v1.0 dataset SMS spam (UPI, 2016)
│   ├── Rahmi 2016 Catatan Korpus.txt                       # Catatan lisensi & distribusi kelas asli (Yudi Wibisono)
│   ├── Rahmi 2016 Lisensi CC BY SA.md                      # Bukti lisensi CC BY-SA 4.0 & SHA-256 korpus Rahmi (2016)
│   ├── Theodorus 2021 Korpus SMS Spam IEEE.csv             # Korpus SMS Spam IEEE EIConCIT (Theodorus dkk., 2021 - 4.125 baris)
│   ├── Theodorus 2021 Koleksi SMS Asli.xlsx                # Berkas Excel asli korpus Theodorus dkk. (2021)
│   ├── Theodorus 2021 Sitasi Resmi.cff                     # Metadata sitasi ilmiah resmi IEEE EIConCIT 2021
│   ├── Theodorus 2021 Dokumentasi Korpus.md                # Dokumentasi asli repositori Theodorus dkk. (2021)
│   ├── Kurniawan 2024 Korpus Phishing SMS dan Email Indo.csv # Korpus Phishing SMS & Email Indonesia (1.772 baris)
│   ├── Saragih 2024 Korpus SMS Spam Indo.csv               # Korpus SMS Spam Indonesia 5 kategori (690 baris)
│   └── Saragih 2024 Dataset SMS Asli.xlsx                  # Berkas Excel asli korpus Saragih (2024)
└── 02 Data Olahan/                                         # Direktori seluruh file olahan siap latih (processed data)
    ├── Dataset Pajak Terkurasi 260 Baris.csv               # Korpus domain perpajakan terkurasi (260 baris seimbang)
    ├── Dataset Gabungan Utama Biner 1164 Baris.csv         # Dataset gabungan utama biner (1.164 baris: 904 umum + 260 pajak)
    ├── Dataset Gabungan Diperluas Biner 2521 Baris.csv     # Dataset gabungan lintas korpus terdeduplikasi (2.521 baris)
    ├── Katalog Asal Sumber Data.csv                        # Katalog provenans seluruh berkas beserta hash SHA-256
    └── Katalog Asal Sumber Data.json                       # Katalog provenans format JSON
```

---

## 2. Katalog File Mentah (*Raw Data*) dan Asal Sumbernya

Tabel berikut memuat daftar berkas mentah yang dikumpulkan beserta penulis atau instansi penerbit, lisensi, jumlah rekaman, tautan sumber asli, dan nilai *checksum* SHA-256 untuk menjamin keutuhan data.

| ID Katalog | Lokasi Berkas | Jumlah Rekaman | Penulis / Instansi Sumber | Lisensi | Tautan Asal Sumber / DOI | Checksum SHA-256 (16 Karakter Awal) |
| :--- | :--- | :---: | :--- | :--- | :--- | :--- |
| `FILE-RAW-01` | `04 Dataset/01 Data Mentah/Rahmi 2016 Korpus SMS Spam Utama v1.csv` | 1.143 baris | Ferdila Rahmi & Yudi Wibisono (Universitas Pendidikan Indonesia, 2016) | CC BY-SA 4.0 | https://repository.upi.edu/26936/ | `865d3ea178bc8545` |
| `FILE-RAW-02` | `04 Dataset/01 Data Mentah/Rahmi 2016 Arsip Asli SMS Spam.csv` | 1.143 baris | Ferdila Rahmi & Yudi Wibisono (Arsip Asli v1.0 Agustus 2018) | CC BY-SA 4.0 | https://yudiwbs.wordpress.com/2018/08/05/dataset-klasifikasi-bahasa-indonesia-sms-spam-klasifikasi-teks-dengan-scikit-learn/ | `49001313b7180f02` |
| `FILE-RAW-03` | `04 Dataset/01 Data Mentah/Theodorus 2021 Korpus SMS Spam IEEE.csv` | 4.125 baris | Agustinus Theodorus, Tio K. Prasetyo, Reynaldi Hartono, Derwin Suhartono (BINUS University, IEEE EIConCIT 2021) | CC BY-SA 4.0 | https://doi.org/10.1109/EIConCIT50028.2021.9431859 | `14c6e56a5f39a841` |
| `FILE-RAW-04` | `04 Dataset/01 Data Mentah/Kurniawan 2024 Korpus Phishing SMS dan Email Indo.csv` | 1.772 baris | Rasen Kurniawan (2024), kompilasi korpus Kaggle & Gist Yudi Wibisono | Open Source | https://github.com/rasen-kurniawan/phishing-detection-eda | `b94131b9bc67b4b1` |
| `FILE-RAW-05` | `04 Dataset/01 Data Mentah/Saragih 2024 Korpus SMS Spam Indo.csv` | 690 baris | Samuel Cristian Saragih (2024) | MIT License | https://github.com/Sctian514/Indonesian-sms-spam-classifier | `ebaf0f849001ae31` |
| `FILE-RAW-06` | `04 Dataset/01 Data Mentah/DJP Hasil Scrape 68 Sumber Resmi.json` | 68 artikel | Direktorat Jenderal Pajak (`pajak.go.id`), DDTC News, Ortax, Jalahoaks DKI Jakarta, BCA, Antara, DetikFinance | Informasi Publik | https://www.pajak.go.id/id/pengumuman | `60b571cc67630a5b` |
| `FILE-RAW-07` | `04 Dataset/01 Data Mentah/DJP Indikator Penipuan dan Kanal Resmi.json` | 31 indikator | Direktorat Jenderal Pajak (`PENG-31/PJ.09/2024` s.d. `PENG-50/PJ.09/2025`) | Informasi Publik | https://www.pajak.go.id/id/pengumuman/waspada-penipuan-yang-mengatasnamakan-direktorat-jenderal-pajak | `e7883bd235c40700` |

### Rincian Korpus Akademik Terbuka
1. **Korpus Rahmi & Wibisono (2016)**: Berisi 1.143 pesan singkat berbahasa Indonesia yang terbagi ke dalam tiga label asli: `0` = SMS Normal (569 pesan), `1` = Penipuan/Fraud (335 pesan), dan `2` = Promo/Iklan (239 pesan). Data pribadi pada korpus ini telah dianonimkan oleh penyusun aslinya menggunakan penanda `nama1`.
2. **Korpus Theodorus dkk. (2021) - IEEE EIConCIT**: Merupakan dataset pendamping makalah ilmiah yang telah menjadi referensi utama nomor `[2]` pada proposal penelitian ini (*Short Message Service (SMS) Spam Filtering using Machine Learning in Bahasa Indonesia*, DOI: `10.1109/EIConCIT50028.2021.9431859`). Berisi 4.125 pesan (`0` = *ham*/normal sebanyak 2.323 baris, `1` = *promo* sebanyak 1.382 baris, dan `2` = *spam*/penipuan sebanyak 420 baris).
3. **Korpus Kurniawan (2024) & Saragih (2024)**: Digunakan sebagai korpus pembanding dan pengayaan lintas sumber (*cross-corpus validation*), mencakup pesan *phishing* dan penipuan pinjaman ilegal, undian palsu, serta pesan normal berbahasa Indonesia.

---

## 3. Katalog File Olahan (*Processed & Curated Data*)

| ID Katalog | Lokasi Berkas | Jumlah Baris | Distribusi Kelas Biner | Keterangan Pengolahan | Checksum SHA-256 (16 Karakter Awal) |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `FILE-PROC-01` | `04 Dataset/02 Data Olahan/Dataset Pajak Terkurasi 260 Baris.csv` | 260 baris | `1` (Phishing Pajak): 130<br>`0` (Aman/Resmi Pajak): 130 | Kurasi seimbang 50:50 dari 68 sumber resmi, dilengkapi kolom `Teks`, `label`, `kategori_modus`, `sumber_referensi`, `id_sumber`, dan `url_sumber`. | `4cdcf6da8748d89b` |
| `FILE-PROC-02` | `04 Dataset/02 Data Olahan/Dataset Gabungan Utama Biner 1164 Baris.csv` | 1.164 baris | `1` (Phishing/Fraud): 465<br>`0` (Aman/Normal): 699 | Penggabungan subset biner `Rahmi 2016 Korpus SMS Spam Utama v1.csv` (904 baris) dan `Dataset Pajak Terkurasi 260 Baris.csv` (260 baris), dilengkapi kolom `clean_text`, `ada_token_apk`, `ada_token_url`, `jumlah_kata`, dan `jumlah_karakter`. | `1f203f93683009d6` |
| `FILE-PROC-03` | `04 Dataset/02 Data Olahan/Dataset Gabungan Diperluas Biner 2521 Baris.csv` | 2.521 baris | `1` (Phishing/Fraud): 822<br>`0` (Aman/Normal): 1.699 | Penggabungan terdeduplikasi berdasarkan `clean_text` dari korpus Rahmi (2016), Theodorus (2021), Saragih (2024), dan korpus pajak terkurasi (260 baris). | `dc58b5484e58cbbf` |

### Distribusi 22 Kategori Modus pada `Dataset Pajak Terkurasi 260 Baris.csv` (260 Baris)

Penyeimbangan kelas `1` (130 baris) dan kelas `0` (130 baris) pada domain perpajakan dirancang agar algoritma Support Vector Machine (SVM) dan Random Forest tidak mengalami bias kata kunci (*keyword bias*). Apabila kosakata seperti `pajak`, `NPWP`, `Coretax`, `SPT`, `EFIN`, `M-Pajak`, atau `billing` hanya muncul pada kelas penipuan, model akan salah mengklasifikasikan pesan WhatsApp Blast resmi DJP sebagai *phishing*.

#### A. Kelas `1` - Pesan *Phishing* Mengatasnamakan Otoritas Perpajakan (130 Baris)
| No. | Kode `kategori_modus` | Jumlah | Rujukan Kasus Resmi DJP / KPP / Cek Fakta |
| :---: | :--- | :---: | :--- |
| 1 | `Phishing_APK_Coretax` | 15 | `PENG-4/PJ.09/2025`, `PENG-1/PJ.09/2025`, Artikel DJP (`SRC-014`), DDTC (`SRC-048`), Kemkomdigi (`SRC-067`) |
| 2 | `Phishing_APK_MPajak` | 15 | `PENG-31/PJ.09/2024`, KPP Madya Bandar Lampung (`SRC-022`), KP2KP Enrekang (`SRC-034`), KP2KP Mempawah (`SRC-027`) |
| 3 | `Phishing_APK_Tagihan_SKP_SP2DK` | 15 | `SP-12/2024` (`SRC-008`), KPP Rantau Prapat (`SRC-029`), KP2KP Sinjai (`SRC-026`), Jalahoaks DKI (`SRC-062`) |
| 4 | `Phishing_APK_eBilling_eFaktur` | 10 | `PENG-32/PJ.09/2024` (`SRC-002`), DDTC News (`SRC-047`), Kanwil DJP Banten (`SRC-012`) |
| 5 | `Phishing_Link_Coretax` | 15 | Kasus Korban KP2KP Kuala Kurun `coretax-online.com` (`SRC-028`), Artikel DJP `coretaxdjp-pajak-id.com` (`SRC-014`) |
| 6 | `Phishing_Link_NIK_NPWP_Pemutakhiran` | 12 | `PENG-31/PJ.09/2024` (`djp.linepajak-go.com`, `pajak.xzgo.cc`), KP2KP Takalar (`SRC-019`, `SRC-020`), Jalahoaks (`SRC-063`) |
| 7 | `Phishing_Link_EFIN_OTP_Passphrase` | 10 | Pengumuman Email Palsu DJP (`SRC-006`), Kanwil DJP Banten (`SRC-012`), KP2KP Mempawah (`SRC-027`) |
| 8 | `Phishing_PDF_Surat_Palsu_KUP` | 10 | Kasus Pos Kolonodale / KPP Poso "Layanan Coretax Online" PDF + sanksi KUP (`SRC-017`), KP2KP Bandarjaya (`SRC-018`) |
| 9 | `Phishing_Transfer_Meterai_Rekening_Pribadi` | 10 | `SP-17/WPJ.18/2024` Kanwil DJP Bali (`SRC-009`), KP2KP Kuala Kurun (`SRC-028`), KP2KP Sambas (`SRC-023`), KP2KP Kutacane (`SRC-024`) |
| 10 | `Phishing_Restitusi_Pengembalian_Pajak` | 8 | Kasus Restitusi WA KP2KP Takalar (`SRC-031`), KPP Pratama Palopo (`SRC-030`), Artikel DJP (`SRC-014`) |
| 11 | `Phishing_VideoCall_ShareScreen_PetugasPalsu` | 5 | Kasus Video Call KP2KP Pinrang (`SRC-021`), Share Screen KPP Palopo (`SRC-030`), Profil AI KP2KP Sambas (`SRC-023`) |
| 12 | `Phishing_Lelang_Sitaan_BiayaAdmin` | 5 | Lelang Fiktif & Rekrutmen Palsu DJP (`SRC-001`, `SRC-005`, `SRC-013`, `SRC-014`) |
| **Total** | **12 Kategori Modus Phishing** | **130** | **100% tertaut ke `id_sumber` dan `url_sumber`** |

#### B. Kelas `0` - Pesan Resmi DJP dan Percakapan Normal Perpajakan (130 Baris)
| No. | Kode `kategori_modus` | Jumlah | Rujukan Pengumuman / Layanan Resmi DJP |
| :---: | :--- | :---: | :--- |
| 1 | `Resmi_WA_Blast_Coretax` | 15 | Pengumuman Resmi WA Blast Coretax `+62 822-3000-9880` (`SRC-007`, `SRC-045`, `SRC-054`) |
| 2 | `Resmi_WA_Blast_SPT_Tahunan` | 15 | Kutipan WA Blast Resmi KPP Pratama Denpasar Barat (`SRC-036`) & KP2KP Negara (`SRC-042`) |
| 3 | `Resmi_WA_Blast_Pemadanan_NIK_NPWP` | 14 | WA Blast Resmi KPP Pratama Singaraja (`SRC-035`), KP2KP Mukomuko (`SRC-037`), KPP Batam Utara (`SRC-038`) |
| 4 | `Resmi_Notifikasi_BPE_Billing_MPN` | 14 | Prosedur Resmi Pembayaran MPN G3 Kanwil DJP Kalselteng (`SRC-010`) & Artikel M-Pajak (`SRC-016`) |
| 5 | `Resmi_Layanan_KringPajak_EFIN_MPajak` | 14 | Layanan Resmi Kring Pajak 1500200, `kunjung.pajak.go.id` (`SRC-040`), EFIN KPP Watampone (`SRC-039`) |
| 6 | `Resmi_Layanan_WA_KPP_KP2KP_Terverifikasi` | 14 | WA Terverifikasi KPP Jatinegara (`SRC-043`), KPP Poso (`SRC-017`), Kanwil Papabrama (`SRC-011`), KP2KP Pinrang (`SRC-021`) |
| 7 | `Resmi_Edukasi_Waspada_Penipuan_DJP` | 14 | Rilis Resmi Imbauan Waspada Penipuan `PENG-31/PJ.09/2024` s.d. `PENG-50/PJ.09/2025` (`SRC-001` s.d. `SRC-013`) |
| 8 | `Resmi_Kelas_Pajak_dan_Survei_DJP` | 10 | WA Blast Resmi Survei Kepuasan DJP (`SRC-057`), Kelas Pajak KPP Poso (`SRC-032`), IG Live KPP Palopo (`SRC-030`) |
| 9 | `Normal_Percakapan_Pajak_Kantor_WP` | 12 | Percakapan wajar staf keuangan/wajib pajak merujuk layanan resmi (`SRC-015`, `SRC-017`, `SRC-021`, `SRC-040`) |
| 10 | `Normal_Diskusi_Administrasi_Perpajakan` | 8 | Diskusi internal administrasi e-Faktur, e-Bupot, TER PPh 21, dan NTPN (`SRC-010`, `SRC-016`, `SRC-045`) |
| **Total** | **10 Kategori Resmi / Normal** | **130** | **100% tertaut ke `id_sumber` dan `url_sumber`** |

---

## 4. Indikator Kompromi (*Indicators of Compromise*) & Kanal Resmi dari Rilis DJP

Dari hasil *scraping* dokumen pengumuman resmi DJP (`04 Dataset/01 Data Mentah/DJP Indikator Penipuan dan Kanal Resmi.json`), berikut adalah indikator teknis yang tercatat secara eksplisit dalam rilis resmi pemerintah:

1. **Domain *Phishing* yang Diumumkan Resmi oleh DJP**:
   - `djp[.]linepajak-go[.]com` (Sumber: `PENG-31/PJ.09/2024` / `SRC-001`)
   - `pajak[.]xzgo[.]cc` (Sumber: `PENG-31/PJ.09/2024` / `SRC-001`)
   - `coretaxdjp-pajak-id[.]com` (Sumber: Artikel Edukasi Pajak Digital DJP / `SRC-014`)
   - `coretax-online[.]com` (Sumber: Laporan Kasus Korban KP2KP Kuala Kurun / `SRC-028`)
   - `pajak-id[.]co[.]id` (Sumber: Artikel Edukasi Pajak Digital DJP / `SRC-014`)
   - `pajak-go[.]id` (Sumber: Rilis DJP & DDTC News / `SRC-055`)
2. **Nomor WhatsApp Penipu yang Diumumkan dalam `PENG-31/PJ.09/2024` (`SRC-001`)**:
   - `+6282118339033`, `+6289518182603`, `+6282258192334`, `+6283183738739`, `+6281367728313`, `+6281318762817`, `+6285361994929`.
3. **Alamat *Email Spoofing* yang Diumumkan DJP (`SRC-006`)**:
   - `djponline_pajak@yahoo.com`, `efiling@pajakk.go.id`.
4. **Nomor WhatsApp dan Kanal Resmi Terverifikasi DJP**:
   - WhatsApp Blast Resmi Edukasi Coretax DJP: `+62 822-3000-9880` (`SRC-007`, `SRC-054`)
   - Portal Utama dan Coretax DJP: `https://www.pajak.go.id` dan `https://coretaxdjp.pajak.go.id` (`SRC-014`, `SRC-028`)
   - Kring Pajak & Pengaduan Resmi: `1500200`, `https://pengaduan.pajak.go.id`, `pengaduan@pajak.go.id`, `@kring_pajak` (`SRC-001`)
   - WhatsApp Terverifikasi Unit Kerja: KPP Pratama Jakarta Jatinegara (`0895-8018-76969` / `SRC-043`), KPP Pratama Poso (`0851-8681-2833`, `0851-5666-2318` / `SRC-017`), Kanwil DJP Papabrama (`+62-813-4471-4177` / `SRC-011`), KP2KP Pinrang (`0421-921566` / `SRC-021`), KP2KP Sinjai (`0812-2018-2008` / `SRC-026`), KP2KP Perdagangan (`0813-6203-6060` / `SRC-044`).

---

## 5. Daftar Lengkap 68 Sumber Web Resmi Hasil Scraping (`DJP Hasil Scrape 68 Sumber Resmi.json`)

Seluruh teks bersih hasil *scraping* tersimpan di dalam `04 Dataset/01 Data Mentah/DJP Hasil Scrape 68 Sumber Resmi.json` dan ringkasannya di `04 Dataset/01 Data Mentah/DJP Ringkasan Scrape 68 Sumber Resmi.csv`.

| ID Sumber | Kategori Sumber | Instansi Penerbit | Nomor Dokumen / Rujukan | Tautan URL Resmi |
| :--- | :--- | :--- | :--- | :--- |
| `SRC-001` | Pengumuman Resmi DJP | Direktorat Jenderal Pajak | `PENG-31/PJ.09/2024` | https://pajak.go.id/id/pengumuman/waspada-penipuan-mengatasnamakan-direktorat-jenderal-pajak |
| `SRC-002` | Pengumuman Resmi DJP | Direktorat Jenderal Pajak | `PENG-32/PJ.09/2024` | https://pajak.go.id/id/pengumuman/waspada-penipuan-mengatasnamakan-direktorat-jenderal-pajak-0 |
| `SRC-003` | Pengumuman Resmi DJP | Direktorat Jenderal Pajak | `PENG-1/PJ.09/2025` | https://www.pajak.go.id/id/pengumuman/waspada-penipuan-mengatasnamakan-direktorat-jenderal-pajak-1 |
| `SRC-004` | Pengumuman Resmi DJP | Direktorat Jenderal Pajak | `PENG-4/PJ.09/2025` | https://pajak.go.id/id/pengumuman/waspada-penipuan-yang-mengatasnamakan-djp |
| `SRC-005` | Pengumuman Resmi DJP | Direktorat Jenderal Pajak | `PENG-50/PJ.09/2025` | https://pajak.go.id/id/pengumuman/imbauan-kewaspadaan-terhadap-modus-penipuan-mengatasnamakan-pejabatpegawai-direktorat |
| `SRC-006` | Pengumuman Resmi DJP | Direktorat Jenderal Pajak | Pengumuman Email Palsu | https://pajak.go.id/id/pengumuman/waspada-penipuan-mengatasnamakan-djp |
| `SRC-007` | Pengumuman Resmi DJP | Direktorat Jenderal Pajak | Pengumuman WA Blast Coretax | https://www.pajak.go.id/id/pengumuman/pengiriman-whatsapp-blast-dalam-rangka-edukasi-coretax-djp |
| `SRC-008` | Siaran Pers DJP | Direktorat Jenderal Pajak | `SP-12/2024` | https://www.pajak.go.id/id/siaran-pers/modus-penipuan-mengatasnamakan-djp |
| `SRC-009` | Siaran Pers DJP | Kanwil DJP Bali | `SP-17/WPJ.18/2024` | https://www.pajak.go.id/id/siaran-pers/waspada-marak-beredar-penipuan-mengatasnamakan-djp-melalui-media-whatsapp-dan-email |
| `SRC-010` | Siaran Pers DJP | Kanwil DJP Kalselteng | Siaran Pers Kalselteng | https://www.pajak.go.id/id/siaran-pers/kanwil-djp-kalselteng-ingatkan-waspada-email-palsu-tagihan-pajak-mengatasnamakan-djp |
| `SRC-011` | Siaran Pers DJP | Kanwil DJP Papabrama | Siaran Pers Papabrama | https://www.pajak.go.id/id/siaran-pers/waspada-penipuan-terbaru-yang-mengatasnamakan-direktorat-jenderal-pajak |
| `SRC-012` | Siaran Pers DJP | Kanwil DJP Banten | Siaran Pers Banten | https://www.pajak.go.id/id/siaran-pers/waspada-penipuan-yang-mengatasnamakan-direktorat-jenderal-pajak |
| `SRC-013` | Siaran Pers DJP | Kanwil DJP Kalselteng | Siaran Pers DJP 2026 | https://pajak.go.id/id/siaran-pers/djp-imbau-kembali-agar-masyarakat-waspadai-penipuan |
| `SRC-014` | Artikel Edukasi DJP | Direktorat Jenderal Pajak | Artikel 5 Modus Penipuan | https://pajak.go.id/id/artikel/stop-klik-waspada-5-modus-penipuan-pajak-digital-yang-mengintai-wajib-pajak |
| `SRC-015` | Artikel Edukasi DJP | Direktorat Jenderal Pajak | Artikel WA Setelah SPT | https://www.pajak.go.id/id/artikel/waspada-pesan-whatsapp-pemutakhiran-data-setelah-lapor-spt |
| `SRC-016` | Artikel Edukasi DJP | Direktorat Jenderal Pajak | Artikel Resmi M-Pajak | https://www.pajak.go.id/id/artikel/m-pajak-layanan-pajak-mudah-dalam-genggaman |
| `SRC-017` | Berita Kasus KPP/KP2KP | Pos Kolonodale / KPP Poso | Laporan WA PDF Coretax | https://www.pajak.go.id/id/berita/terima-whatsapp-mencurigakan-wajib-pajak-konfirmasi-ke-pos-kolonodale |
| `SRC-018` | Berita Kasus KPP/KP2KP | KP2KP Bandarjaya | Laporan WA PDF WP Badan | https://pajak.go.id/id/berita/tetap-waspada-wajib-pajak-laporkan-penipuan-ke-pajak-bandarjaya |
| `SRC-019` | Berita Kasus KPP/KP2KP | KP2KP Takalar | Edukasi Phishing WA | https://www.pajak.go.id/id/berita/marak-penipuan-whatsapp-kp2kp-takalar-awas-phising |
| `SRC-020` | Berita Kasus KPP/KP2KP | KP2KP Takalar | Aduan Konfirmasi Data WA | https://pajak.go.id/id/berita/penipuan-mengatasnamakan-djp-kp2kp-takalar-ingatkan-wajib-pajak-tetap-waspada |
| `SRC-021` | Berita Kasus KPP/KP2KP | KP2KP Pinrang | Kasus Video Call & Rp10rb | https://pajak.go.id/id/berita/penipuan-mengatasnamakan-djp-pajak-pinrang-tegaskan-semua-pelayanan-gratis |
| `SRC-022` | Berita Kasus KPP/KP2KP | KPP Madya Bandar Lampung | Kasus APK M-Pajak via WA | https://pajak.go.id/id/berita/marak-penipuan-mengatasnamakan-djp-pajak-madya-bandar-lampung-imbau-masyarakat-waspada |
| `SRC-023` | Berita Kasus KPP/KP2KP | KP2KP Sambas | Kasus Profil AI & APK WA | https://www.pajak.go.id/id/berita/waspada-modus-penipuan-mengatasnamakan-djp-pajak-sambas-sebarkan-brosur |
| `SRC-024` | Berita Kasus KPP/KP2KP | KP2KP Kutacane | Kasus Hapus Data & Biaya | https://www.pajak.go.id/id/berita/pajak-kutacane-imbau-wajib-pajak-untuk-waspada-penipuan |
| `SRC-025` | Berita Kasus KPP/KP2KP | KP2KP Unaaha | Kasus Telepon Kantor Pusat | https://www.pajak.go.id/id/berita/jangan-percaya-tangkal-penipuan-dengan-konfirmasi |
| `SRC-026` | Berita Kasus KPP/KP2KP | KP2KP Sinjai | Kasus Chat Verifikasi NPWP | https://pajak.go.id/id/berita/verifikasi-data-melalui-chat-mencurigakan-kp2kp-sinjai-modus-penipuan |
| `SRC-027` | Berita Kasus KPP/KP2KP | KP2KP Mempawah | Kasus APK, Meterai & OTP | https://www.pajak.go.id/id/berita/wajib-pajak-nyaris-jadi-korban-penipuan-berkedok-pajak-kp2kp-mempawah-berikan-edukasi-kanal |
| `SRC-028` | Berita Kasus KPP/KP2KP | KP2KP Kuala Kurun | Kasus `coretax-online.com` | https://www.pajak.go.id/id/berita/kp2kp-kuala-kurun-datangi-korban-penipuan-atas-namakan-djp |
| `SRC-029` | Berita Kasus KPP/KP2KP | KPP Pratama Rantau Prapat | WA Blast Waspada APK SKP | https://www.pajak.go.id/id/berita/pajak-rantau-prapat-minta-wajib-pajak-waspada-penipuan |
| `SRC-030` | Berita Kasus KPP/KP2KP | KPP Pratama Palopo | Edukasi Scam & Share Screen | https://www.pajak.go.id/id/berita/jelaskan-modus-penipuan-berkedok-djp-dan-langkah-hadapinya-kpp-pratama-palopo-gelar |
| `SRC-031` | Berita Kasus KPP/KP2KP | KP2KP Takalar | Kasus Janji Restitusi WA | https://pajak.go.id/id/berita/kp2kp-takalar-edukasi-wajib-pajak-waspadai-modus-penipuan-atas-namakan-djp |
| `SRC-032` | Berita Kasus KPP/KP2KP | KPP Pratama Poso | Kasus Meterai Palsu Morowali | https://www.pajak.go.id/id/berita/marak-penipuan-pajak-poso-minta-masyarakat-waspada |
| `SRC-033` | Berita Kasus KPP/KP2KP | KP2KP Kepahiang | Edukasi Anti-Phishing ASN | https://www.pajak.go.id/id/berita/cegah-penipuan-pajak-kepahiang-kunjungi-instansi-pemerintah-dan-perbankan |
| `SRC-034` | Berita Kasus KPP/KP2KP | KP2KP Enrekang | Kasus Aplikasi Tiruan M-Pajak | https://pajak.go.id/id/berita/marak-penipuan-berkedok-m-pajak-kp2kp-enrekang-imbau-masyarakat-waspada |
| `SRC-035` | Berita Layanan Resmi | KPP Pratama Singaraja | WA Blast Pemadanan NIK-NPWP | https://www.pajak.go.id/id/berita/gaungkan-pemadanan-nik-npwp-pajak-singaraja-kirim-whatsapp-blast |
| `SRC-036` | Berita Layanan Resmi | KPP Pratama Denpasar Barat | WA Blast Resmi SPT Tahunan | https://www.pajak.go.id/id/berita/tingkatkan-kepatuhan-spt-tahunan-kpp-denbar-kirimkan-whatsapp-blast |
| `SRC-037` | Berita Layanan Resmi | KP2KP Mukomuko | WA Blast Pemadanan NIK-NPWP | https://www.pajak.go.id/id/berita/pajak-mukomuko-imbau-wajib-pajak-lakukan-pemadanan-nik-npwp |
| `SRC-038` | Berita Layanan Resmi | KPP Pratama Batam Utara | WA Blast Pengingat NIK-NPWP | https://www.pajak.go.id/id/berita/kpp-batam-utara-kirim-pesan-pengingat-nik-npwp-melalui-whatsapp-blast |
| `SRC-039` | Berita Layanan Resmi | KPP Pratama Watampone | Layanan EFIN & Billing WA | https://www.pajak.go.id/id/berita/mudahnya-mengajukan-permintaan-kode-efin-dan-kode-billing-melalui-layanan-whatsapp-kpp |
| `SRC-040` | Berita Layanan Resmi | KPP Pratama Tolitoli | Antrean Online & WA KPP | https://pajak.go.id/id/berita/daftar-antrean-online-kpp-pratama-tolitoli-siap-melayani-lewat-whatsapp |
| `SRC-041` | Berita Layanan Resmi | KPP Pratama Kupang | Satu Nomor Layanan WA KPP | https://www.pajak.go.id/id/berita/permudah-wajib-pajak-kpp-kupang-luncurkan-satu-nomor-layanan-whatsapp |
| `SRC-042` | Berita Layanan Resmi | KP2KP Negara | Asistensi SPT via WA | https://www.pajak.go.id/id/berita/kp2kp-negara-berikan-asistensi-pelaporan-spt-tahunan-via-whatsapp |
| `SRC-043` | Berita Layanan Resmi | KPP Pratama Jakarta Jatinegara | Inovasi WA Terverifikasi | https://www.pajak.go.id/id/berita/kpp-jatinegara-luncurkan-inovasi-layanan-whatsapp-terverifikasi |
| `SRC-044` | Berita Layanan Resmi | KP2KP Perdagangan | Layanan Billing via WA | https://www.pajak.go.id/id/berita/kp2kp-perdagangan-bantu-wajib-pajak-buat-kode-billing-lewat-whatsapp |
| `SRC-045` | Berita Layanan Resmi | Direktorat Jenderal Pajak | Portal Reformasi Coretax | https://pajak.go.id/id/reformdjp/coretax |
| `SRC-046` s.d. `SRC-058` | Portal Berita Pajak | DDTC News | 13 Artikel Rilis Resmi DJP (`SP-12/2024`, `SP-30/2024`, `PENG-31`, `PENG-1`, `PENG-4`, `PENG-50`, WA Blast Coretax & Survei) | `https://news.ddtc.co.id` (tautan spesifik per artikel di `DJP Ringkasan Scrape 68 Sumber Resmi.csv`) |
| `SRC-059` s.d. `SRC-061` | Portal Berita Pajak | Ortax | 3 Artikel Kajian Modus Penipuan Pejabat DJP & Coretax | `https://ortax.org` (tautan spesifik di `DJP Ringkasan Scrape 68 Sumber Resmi.csv`) |
| `SRC-062` s.d. `SRC-064` | Portal Cek Fakta | Jalahoaks Pemprov DKI Jakarta | 3 Klarifikasi Hoaks WA Surat Tagihan Pajak, Pemadanan NPWP, & Pembaruan Data DJP | `https://jalahoaks.jakarta.go.id` (tautan spesifik di `DJP Ringkasan Scrape 68 Sumber Resmi.csv`) |
| `SRC-065` | Edukasi Keamanan Bank | PT Bank Central Asia Tbk (BCA) | Awas Modus Penipuan Pajak Mengatasnamakan DJP | https://www.bca.co.id/id/informasi/awas-modus/2024/10/01/08/21/awas-modus-penipuan-pajak-mengatasnamakan-djp |
| `SRC-066` s.d. `SRC-067` | Kantor Berita Nasional | LKBN Antara | Imbauan DJP & Peringatan Kemkomdigi soal Phishing Coretax DJP | `https://www.antaranews.com` (tautan spesifik di `DJP Ringkasan Scrape 68 Sumber Resmi.csv`) |
| `SRC-068` s.d. `SRC-069` | Media Ekonomi Nasional | DetikFinance | Daftar Modus Penipuan Terbaru Catut Nama DJP | `https://finance.detik.com` (tautan spesifik di `DJP Ringkasan Scrape 68 Sumber Resmi.csv`) |

---

## 6. Reproduksi Pipeline dan Hasil Evaluasi Baseline

Untuk mereproduksi seluruh berkas data olahan dan katalog provenans dari berkas mentah, jalankan:

```powershell
& "$env:LOCALAPPDATA\venvs\ta-phishing-pajak-unsia\Scripts\python.exe" -m src.kurasi_dataset
```

Untuk menjalankan evaluasi komparasi *baseline* Support Vector Machine (`LinearSVC`) dan `RandomForestClassifier` (pembagian *stratified train-test split* 80:20, TF-IDF *n-gram* `(1, 2)` dengan 3.000 fitur, praproses *stopword removal* dan *stemming* Sastrawi, serta tokenisasi khusus `token_apk` dan `token_url`):

```powershell
& "$env:LOCALAPPDATA\venvs\ta-phishing-pajak-unsia\Scripts\python.exe" src\eksperimen_baseline.py
```

### Ringkasan Performa Baseline pada Dataset Gabungan Utama (1.164 Baris; Data Uji = 233 Baris)

| Algoritma | Accuracy | Precision (Phishing `1`) | Recall (Phishing `1`) | F1-Score (Phishing `1`) | F1-Score Macro |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Support Vector Machine (`LinearSVC`)** | **98,28%** | **0,98** | **0,98** | **0,98** | **0,98** |
| **Random Forest (`n_estimators=200`)** | **95,28%** | 0,94 | 0,95 | 0,94 | 0,95 |
