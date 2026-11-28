"""Pembangun 4 bagan Tugas Akhir UNSIA (HTML/SVG) dan konversi PNG resolusi tinggi."""

from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
ASSET_DIR = ROOT_DIR / "06-naskah-ta" / "aset-gambar"
CHROME_CANDIDATES = (
    Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
    Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
)

SVG_SHELL = """<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8" />
  <title>{title}</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: #ffffff;
      font-family: "Segoe UI", "Inter", -apple-system, BlinkMacSystemFont, sans-serif;
    }}
    svg {{ display: block; width: {vb_w}px; height: {vb_h}px; background: #ffffff; }}
  </style>
</head>
<body>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {vb_w} {vb_h}" width="{vb_w}" height="{vb_h}" role="img" aria-labelledby="t1 d1">
  <title id="t1">{title}</title>
  <desc id="d1">{desc}</desc>
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 1 1.5 L 9 5 L 1 8.5 z" fill="#475569" />
    </marker>
    <marker id="arrow-link" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 1 1.5 L 9 5 L 1 8.5 z" fill="#1d4ed8" />
    </marker>
    <marker id="arrow-accent" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 1 1.5 L 9 5 L 1 8.5 z" fill="#c2410c" />
    </marker>
  </defs>
  <rect x="0" y="0" width="{vb_w}" height="{vb_h}" fill="#ffffff" />
{body}
</svg>
</body>
</html>
"""


def _diagram_1_1_body() -> str:
    # 3x2 zig-zag grid: 1 -> 2 -> 3 -> down to 4 -> 5 -> 6
    # viewBox 800 x 336, all coords on 4px grid
    return """  <!-- Baris atas konektor: 1->2, 2->3, 3->4 -->
  <line x1="248" y1="80" x2="276" y2="80" stroke="#475569" stroke-width="2" marker-end="url(#arrow)" />
  <line x1="516" y1="80" x2="544" y2="80" stroke="#475569" stroke-width="2" marker-end="url(#arrow)" />
  <line x1="664" y1="144" x2="664" y2="188" stroke="#475569" stroke-width="2" marker-end="url(#arrow)" />
  <!-- Baris bawah konektor: 4->5, 5->6 -->
  <line x1="544" y1="256" x2="516" y2="256" stroke="#475569" stroke-width="2" marker-end="url(#arrow)" />
  <line x1="276" y1="256" x2="248" y2="256" stroke="#c2410c" stroke-width="2.2" marker-end="url(#arrow-accent)" />

  <!-- Kotak 1 -->
  <rect x="16" y="16" width="232" height="128" rx="8" fill="#ffffff" stroke="#1e293b" stroke-width="1.6" />
  <rect x="16" y="16" width="232" height="32" rx="8" fill="#0f3d75" />
  <rect x="16" y="40" width="232" height="8" fill="#0f3d75" />
  <text x="132" y="37" text-anchor="middle" fill="#ffffff" font-size="13.5" font-weight="700">1. Kurasi Korpus Publik</text>
  <text x="132" y="76" text-anchor="middle" fill="#1e293b" font-size="12.5">904 SMS Umum &amp; 260 Pajak</text>
  <text x="132" y="96" text-anchor="middle" fill="#475569" font-size="12">(65 dari 68 arsip 2021–2026)</text>
  <text x="132" y="118" text-anchor="middle" fill="#1d4ed8" font-size="12" font-weight="600">Total Induk: 1.164 baris</text>

  <!-- Kotak 2 -->
  <rect x="280" y="16" width="236" height="128" rx="8" fill="#ffffff" stroke="#1e293b" stroke-width="1.6" />
  <rect x="280" y="16" width="236" height="32" rx="8" fill="#0f3d75" />
  <rect x="280" y="40" width="236" height="8" fill="#0f3d75" />
  <text x="398" y="37" text-anchor="middle" fill="#ffffff" font-size="13.5" font-weight="700">2. Praproses Teks</text>
  <text x="398" y="76" text-anchor="middle" fill="#1e293b" font-size="12.5">Case folding &amp; token entitas</text>
  <text x="398" y="96" text-anchor="middle" fill="#475569" font-size="12">(token_apk &amp; token_url)</text>
  <text x="398" y="118" text-anchor="middle" fill="#475569" font-size="12">Stopword &amp; Stemming Sastrawi</text>

  <!-- Kotak 3 -->
  <rect x="548" y="16" width="236" height="128" rx="8" fill="#ffffff" stroke="#1e293b" stroke-width="1.6" />
  <rect x="548" y="16" width="236" height="32" rx="8" fill="#0f3d75" />
  <rect x="548" y="40" width="236" height="8" fill="#0f3d75" />
  <text x="666" y="37" text-anchor="middle" fill="#ffffff" font-size="13.5" font-weight="700">3. TF-IDF &amp; Partisi Data</text>
  <text x="666" y="76" text-anchor="middle" fill="#1e293b" font-size="12.5">Deduplikasi: 1.159 teks unik</text>
  <text x="666" y="96" text-anchor="middle" fill="#475569" font-size="12">TF-IDF (1, 2) maks. 3.000 fitur</text>
  <text x="666" y="118" text-anchor="middle" fill="#1d4ed8" font-size="12" font-weight="600">Split 80:20 (927 latih : 232 uji)</text>

  <!-- Kotak 4 -->
  <rect x="548" y="192" width="236" height="128" rx="8" fill="#ffffff" stroke="#1e293b" stroke-width="1.6" />
  <rect x="548" y="192" width="236" height="32" rx="8" fill="#0f3d75" />
  <rect x="548" y="216" width="236" height="8" fill="#0f3d75" />
  <text x="666" y="213" text-anchor="middle" fill="#ffffff" font-size="13.5" font-weight="700">4. Pelatihan &amp; Penalaan</text>
  <text x="666" y="252" text-anchor="middle" fill="#1e293b" font-size="12.5">LinearSVC (C=2,0) &amp; Platt</text>
  <text x="666" y="272" text-anchor="middle" fill="#475569" font-size="12">vs Random Forest (100 pohon)</text>
  <text x="666" y="294" text-anchor="middle" fill="#475569" font-size="12">GridSearch 36 kandidat 10-Fold CV</text>

  <!-- Kotak 5 -->
  <rect x="280" y="192" width="236" height="128" rx="8" fill="#ffffff" stroke="#1e293b" stroke-width="1.6" />
  <rect x="280" y="192" width="236" height="32" rx="8" fill="#0f3d75" />
  <rect x="280" y="216" width="236" height="8" fill="#0f3d75" />
  <text x="398" y="213" text-anchor="middle" fill="#ffffff" font-size="13.5" font-weight="700">5. Evaluasi Komparatif</text>
  <text x="398" y="252" text-anchor="middle" fill="#1e293b" font-size="12.5">Matriks Konfusi, ROC/PR, Brier</text>
  <text x="398" y="272" text-anchor="middle" fill="#475569" font-size="12">6 Uji Ablasi &amp; Kontrol (n=45)</text>
  <text x="398" y="294" text-anchor="middle" fill="#475569" font-size="12">Uji Eksternal &amp; Analisis SHAP</text>

  <!-- Kotak 6 (Focal Accent) -->
  <rect x="16" y="192" width="232" height="128" rx="8" fill="rgba(194,65,12,0.06)" stroke="#c2410c" stroke-width="1.8" />
  <rect x="16" y="192" width="232" height="32" rx="8" fill="#c2410c" />
  <rect x="16" y="216" width="232" height="8" fill="#c2410c" />
  <text x="132" y="213" text-anchor="middle" fill="#ffffff" font-size="13.5" font-weight="700">6. Purwarupa TKT Level 6</text>
  <text x="132" y="252" text-anchor="middle" fill="#1e293b" font-size="12.5">REST API &amp; Web Cek Pesan Pajak</text>
  <text x="132" y="272" text-anchor="middle" fill="#475569" font-size="12">Ekstensi WhatsApp Web (MV3)</text>
  <text x="132" y="294" text-anchor="middle" fill="#c2410c" font-size="12" font-weight="600">Daftar Putih DJP &amp; Alasan Awam</text>"""


def _diagram_2_1_body() -> str:
    # 3-zone vertical experimental flowchart, viewBox 800 x 564, all coords on 4px grid
    return """  <!-- Zona 1 -->
  <rect x="16" y="16" width="768" height="148" rx="8" fill="rgba(15,23,42,0.025)" stroke="rgba(15,23,42,0.14)" stroke-width="1" />
  <text x="28" y="36" fill="#475569" font-size="10.5" font-weight="700" letter-spacing="1.0" font-family="'Consolas','Courier New',monospace">ZONA 1 · KURASI DATA, PRAPROSES TEKS, &amp; PARTISI TERSTRATIFIKASI</text>

  <!-- Zona 2 -->
  <rect x="16" y="200" width="676" height="144" rx="8" fill="rgba(29,78,216,0.035)" stroke="rgba(29,78,216,0.18)" stroke-width="1" />

  <!-- Zona 3 -->
  <rect x="16" y="376" width="768" height="148" rx="8" fill="rgba(194,65,12,0.03)" stroke="rgba(194,65,12,0.18)" stroke-width="1" />

  <!-- Konektor Zona 1 -->
  <line x1="252" y1="96" x2="280" y2="96" stroke="#475569" stroke-width="1.8" marker-end="url(#arrow)" />
  <line x1="516" y1="96" x2="544" y2="96" stroke="#475569" stroke-width="1.8" marker-end="url(#arrow)" />

  <!-- Tahap C -> Tahap D (927 latih) -->
  <path d="M 596 144 V 164 Q 596 172 588 172 H 204 Q 196 172 196 180 V 232" fill="none" stroke="#475569" stroke-width="1.8" marker-end="url(#arrow)" />
  <!-- Tahap C -> Jalur Kontrol (712 SMS) -->
  <path d="M 652 144 V 184 Q 652 192 644 192 H 532 Q 524 192 524 200 V 232" fill="none" stroke="#1d4ed8" stroke-width="1.6" stroke-dasharray="5 3" marker-end="url(#arrow-link)" />
  <!-- Tahap C -> Tahap E (232 uji & eksternal via kanan) -->
  <path d="M 732 144 V 440 Q 732 448 724 448 H 676" fill="none" stroke="#1d4ed8" stroke-width="1.6" stroke-dasharray="5 3" marker-end="url(#arrow-link)" />

  <!-- Tahap D -> Tahap E -->
  <line x1="196" y1="324" x2="196" y2="404" stroke="#475569" stroke-width="1.8" marker-end="url(#arrow)" />
  <!-- Jalur Kontrol -> Tahap E -->
  <line x1="524" y1="324" x2="524" y2="404" stroke="#1d4ed8" stroke-width="1.6" stroke-dasharray="5 3" marker-end="url(#arrow-link)" />
  <!-- Tahap E -> Tahap F -->
  <line x1="392" y1="456" x2="432" y2="456" stroke="#c2410c" stroke-width="2" marker-end="url(#arrow-accent)" />

  <!-- Label Zona dengan Mask agar tidak tertabrak garis panah -->
  <rect x="24" y="208" width="380" height="14" rx="2" fill="#f7f9fd" />
  <text x="28" y="220" fill="#1d4ed8" font-size="10.5" font-weight="700" letter-spacing="1.0" font-family="'Consolas','Courier New',monospace">ZONA 2 · PENYETELAN MODEL &amp; JALUR KONTROL BIAS</text>

  <rect x="24" y="384" width="440" height="14" rx="2" fill="#fdf8f6" />
  <text x="28" y="396" fill="#c2410c" font-size="10.5" font-weight="700" letter-spacing="1.0" font-family="'Consolas','Courier New',monospace">ZONA 3 · EVALUASI MULTI-SKENARIO &amp; PURWARUPA TKT LEVEL 6</text>

  <!-- Label Konektor dengan Mask Putih -->
  <rect x="336" y="164" width="96" height="14" rx="2" fill="#ffffff" />
  <text x="384" y="175" text-anchor="middle" fill="#475569" font-size="10.5" font-weight="700" font-family="'Consolas','Courier New',monospace">927 LATIH</text>

  <rect x="548" y="184" width="108" height="14" rx="2" fill="#ffffff" />
  <text x="602" y="195" text-anchor="middle" fill="#1d4ed8" font-size="10.5" font-weight="700" font-family="'Consolas','Courier New',monospace">712 SMS UMUM</text>

  <rect x="676" y="276" width="104" height="14" rx="2" fill="#ffffff" />
  <text x="728" y="287" text-anchor="middle" fill="#1d4ed8" font-size="10.5" font-weight="700" font-family="'Consolas','Courier New',monospace">232 UJI &amp; EKS.</text>

  <rect x="136" y="352" width="120" height="14" rx="2" fill="#ffffff" />
  <text x="196" y="363" text-anchor="middle" fill="#475569" font-size="10.5" font-weight="700" font-family="'Consolas','Courier New',monospace">MODEL PLATT</text>

  <rect x="468" y="352" width="112" height="14" rx="2" fill="#ffffff" />
  <text x="524" y="363" text-anchor="middle" fill="#1d4ed8" font-size="10.5" font-weight="700" font-family="'Consolas','Courier New',monospace">MODEL KONTROL</text>

  <!-- Kotak A -->
  <rect x="28" y="48" width="224" height="96" rx="6" fill="#ffffff" stroke="#1e293b" stroke-width="1.4" />
  <text x="40" y="70" fill="#475569" font-size="10.5" font-weight="700" font-family="'Consolas','Courier New',monospace">TAHAP A · KORPUS</text>
  <text x="40" y="92" fill="#0f172a" font-size="14" font-weight="700">Himpun Korpus Seimbang</text>
  <text x="40" y="112" fill="#334155" font-size="12">260 pajak + 904 SMS = 1.164</text>
  <text x="40" y="130" fill="#475569" font-size="11.5">+1.360 eksternal = 2.521 baris</text>

  <!-- Kotak B -->
  <rect x="284" y="48" width="232" height="96" rx="6" fill="#ffffff" stroke="#1e293b" stroke-width="1.4" />
  <text x="296" y="70" fill="#475569" font-size="10.5" font-weight="700" font-family="'Consolas','Courier New',monospace">TAHAP B · PRAPROSES</text>
  <text x="296" y="92" fill="#0f172a" font-size="14" font-weight="700">Normalisasi Teks Lokal</text>
  <text x="296" y="112" fill="#334155" font-size="12">Sandi token_apk &amp; token_url</text>
  <text x="296" y="130" fill="#475569" font-size="11.5">Stopword &amp; Stemming Sastrawi</text>

  <!-- Kotak C -->
  <rect x="548" y="48" width="224" height="96" rx="6" fill="#ffffff" stroke="#1e293b" stroke-width="1.4" />
  <text x="560" y="70" fill="#475569" font-size="10.5" font-weight="700" font-family="'Consolas','Courier New',monospace">TAHAP C · SPLIT 80:20</text>
  <text x="560" y="92" fill="#0f172a" font-size="14" font-weight="700">Deduplikasi &amp; Partisi</text>
  <text x="560" y="112" fill="#334155" font-size="12">1.159 unik (927 : 232)</text>
  <text x="560" y="130" fill="#475569" font-size="11.5">Korpus perluasan = 2.519 unik</text>

  <!-- Kotak D -->
  <rect x="28" y="236" width="336" height="88" rx="6" fill="#ffffff" stroke="#1e293b" stroke-width="1.4" />
  <text x="40" y="256" fill="#1d4ed8" font-size="10.5" font-weight="700" font-family="'Consolas','Courier New',monospace">TAHAP D · PENYETELAN &amp; KALIBRASI</text>
  <text x="40" y="278" fill="#0f172a" font-size="14" font-weight="700">GridSearch 10-Fold CV + Platt</text>
  <text x="40" y="298" fill="#334155" font-size="12">TF-IDF (1, 2) maks. 3.000; 36 kandidat model</text>
  <text x="40" y="314" fill="#475569" font-size="11.5">Kalibrasi sigmoid 5-lipatan (LinearSVC C=2,0)</text>

  <!-- Kotak Kontrol -->
  <rect x="388" y="236" width="288" height="88" rx="6" fill="#ffffff" stroke="#1d4ed8" stroke-width="1.4" />
  <text x="400" y="256" fill="#1d4ed8" font-size="10.5" font-weight="700" font-family="'Consolas','Courier New',monospace">JALUR KONTROL · RUMUSAN (b)</text>
  <text x="400" y="278" fill="#0f172a" font-size="14" font-weight="700">Latih Tanpa Korpus Pajak</text>
  <text x="400" y="298" fill="#334155" font-size="12">Dilatih hanya 712 SMS umum</text>
  <text x="400" y="314" fill="#475569" font-size="11.5">Pembanding bias di n = 45 pajak</text>

  <!-- Kotak E -->
  <rect x="28" y="408" width="364" height="96" rx="6" fill="#ffffff" stroke="#1e293b" stroke-width="1.4" />
  <text x="40" y="428" fill="#475569" font-size="10.5" font-weight="700" font-family="'Consolas','Courier New',monospace">TAHAP E · EVALUASI &amp; XAI</text>
  <text x="40" y="450" fill="#0f172a" font-size="14" font-weight="700">Uji Holdout, Ablasi, &amp; Lintas Korpus</text>
  <text x="40" y="470" fill="#334155" font-size="12">Accuracy, F1, ROC/PR, Brier, &amp; 6 ablatif</text>
  <text x="40" y="488" fill="#475569" font-size="11.5">Kontrol bias, 1.360 eksternal, bobot &amp; SHAP</text>

  <!-- Kotak F (Focal) -->
  <rect x="436" y="408" width="240" height="96" rx="6" fill="rgba(194,65,12,0.06)" stroke="#c2410c" stroke-width="1.8" />
  <text x="448" y="428" fill="#c2410c" font-size="10.5" font-weight="700" font-family="'Consolas','Courier New',monospace">TAHAP F · PURWARUPA TKT 6</text>
  <text x="448" y="450" fill="#0f172a" font-size="14" font-weight="700">Layanan Web &amp; Ekstensi</text>
  <text x="448" y="470" fill="#334155" font-size="12">Bundel .joblib + API (&lt;100 ms)</text>
  <text x="448" y="488" fill="#c2410c" font-size="11.5" font-weight="600">Daftar putih DJP &amp; alasan awam</text>

  <!-- Legenda -->
  <line x1="16" y1="536" x2="784" y2="536" stroke="#cbd5e1" stroke-width="1" />
  <text x="16" y="554" fill="#475569" font-size="11" font-weight="700">LEGENDA:</text>
  <line x1="92" y1="550" x2="128" y2="550" stroke="#475569" stroke-width="1.8" marker-end="url(#arrow)" />
  <text x="136" y="554" fill="#334155" font-size="11.5">Alur utama eksperimen</text>
  <line x1="308" y1="550" x2="344" y2="550" stroke="#1d4ed8" stroke-width="1.6" stroke-dasharray="5 3" marker-end="url(#arrow-link)" />
  <text x="352" y="554" fill="#334155" font-size="11.5">Jalur kontrol &amp; partisi data uji</text>
  <line x1="564" y1="550" x2="600" y2="550" stroke="#c2410c" stroke-width="2" marker-end="url(#arrow-accent)" />
  <text x="608" y="554" fill="#334155" font-size="11.5">Keluaran model ke TKT 6</text>"""


def _diagram_3_1_body() -> str:
    # Architecture diagram: viewBox 800 x 540, all coords on 4px grid
    return """  <!-- Zona 1 -->
  <rect x="16" y="16" width="768" height="148" rx="8" fill="rgba(15,23,42,0.025)" stroke="rgba(15,23,42,0.14)" stroke-width="1" />
  <text x="28" y="36" fill="#475569" font-size="10.5" font-weight="700" letter-spacing="1.0" font-family="'Consolas','Courier New',monospace">ZONA 1 · KANAL PENGGUNA (TANPA PENYIMPANAN TEKS)</text>

  <!-- Zona 2 -->
  <rect x="16" y="196" width="768" height="224" rx="8" fill="rgba(29,78,216,0.035)" stroke="rgba(29,78,216,0.18)" stroke-width="1" />

  <!-- Zona 3 -->
  <rect x="16" y="452" width="768" height="72" rx="8" fill="rgba(194,65,12,0.03)" stroke="rgba(194,65,12,0.18)" stroke-width="1" />

  <!-- Konektor -->
  <line x1="208" y1="148" x2="208" y2="224" stroke="#1d4ed8" stroke-width="1.8" marker-end="url(#arrow-link)" />
  <rect x="128" y="172" width="160" height="14" rx="2" fill="#ffffff" />
  <text x="208" y="183" text-anchor="middle" fill="#1d4ed8" font-size="10.5" font-weight="700" font-family="'Consolas','Courier New',monospace">GET / &amp; POST /predict</text>

  <line x1="592" y1="148" x2="592" y2="224" stroke="#1d4ed8" stroke-width="1.8" marker-end="url(#arrow-link)" />
  <rect x="500" y="172" width="184" height="14" rx="2" fill="#ffffff" />
  <text x="592" y="183" text-anchor="middle" fill="#1d4ed8" font-size="10.5" font-weight="700" font-family="'Consolas','Courier New',monospace">Service Worker POST /predict</text>

  <!-- API -> 3 Modul Inferensi -->
  <line x1="400" y1="296" x2="400" y2="324" stroke="#475569" stroke-width="1.8" marker-end="url(#arrow)" />
  <path d="M 400 308 H 152 Q 144 308 144 316 V 324" fill="none" stroke="#475569" stroke-width="1.6" marker-end="url(#arrow)" />
  <path d="M 400 308 H 648 Q 656 308 656 316 V 324" fill="none" stroke="#475569" stroke-width="1.6" marker-end="url(#arrow)" />
  <rect x="336" y="302" width="128" height="12" rx="2" fill="#ffffff" />
  <text x="400" y="311" text-anchor="middle" fill="#1e293b" font-size="10" font-weight="700" font-family="'Consolas','Courier New',monospace">INFERENCE.PY</text>

  <!-- Model -> Modul 2 -->
  <line x1="400" y1="476" x2="400" y2="412" stroke="#c2410c" stroke-width="1.8" marker-end="url(#arrow-accent)" />
  <rect x="316" y="428" width="168" height="14" rx="2" fill="#ffffff" />
  <text x="400" y="439" text-anchor="middle" fill="#c2410c" font-size="10.5" font-weight="700" font-family="'Consolas','Courier New',monospace">MUAT MODEL JOBLIB</text>

  <rect x="24" y="204" width="408" height="14" rx="2" fill="#f7f9fd" />
  <text x="28" y="216" fill="#1d4ed8" font-size="10.5" font-weight="700" letter-spacing="1.0" font-family="'Consolas','Courier New',monospace">ZONA 2 · PELADEN REST API &amp; MESIN INFERENSI TERPUSAT</text>

  <rect x="24" y="458" width="352" height="14" rx="2" fill="#fdf8f6" />
  <text x="28" y="470" fill="#c2410c" font-size="10.5" font-weight="700" letter-spacing="1.0" font-family="'Consolas','Courier New',monospace">ZONA 3 · ARTEFAK MODEL LURING (DIREKTORI ML/)</text>

  <!-- Node 1a: Web -->
  <rect x="28" y="48" width="360" height="100" rx="6" fill="#ffffff" stroke="#1e293b" stroke-width="1.4" />
  <text x="44" y="68" fill="#1d4ed8" font-size="10.5" font-weight="700" font-family="'Consolas','Courier New',monospace">APLIKASI WEB · APP/FRONTEND/</text>
  <text x="44" y="90" fill="#0f172a" font-size="14.5" font-weight="700">Antarmuka Web Cek Pesan Pajak</text>
  <text x="44" y="112" fill="#334155" font-size="12">Panel periksa pesan, sorotan bahaya interaktif,</text>
  <text x="44" y="132" fill="#475569" font-size="11.5">tab Web Resmi, Darurat .apk, &amp; Info Akademik</text>

  <!-- Node 1b: Ekstensi -->
  <rect x="412" y="48" width="360" height="100" rx="6" fill="#ffffff" stroke="#1e293b" stroke-width="1.4" />
  <text x="428" y="68" fill="#1d4ed8" font-size="10.5" font-weight="700" font-family="'Consolas','Courier New',monospace">EKSTENSI CHROME · MANIFEST V3 (V1.2.0)</text>
  <text x="428" y="90" fill="#0f172a" font-size="14.5" font-weight="700">Pelindung WhatsApp Web &amp; Popup</text>
  <text x="428" y="112" fill="#334155" font-size="12">Pemindai DOM pesan (&ge;8 kar., .apk, atau tautan)</text>
  <text x="428" y="132" fill="#475569" font-size="11.5">Menampilkan lencana risiko langsung di obrolan</text>

  <!-- Node 2: FastAPI -->
  <rect x="28" y="228" width="744" height="68" rx="6" fill="#ffffff" stroke="#1d4ed8" stroke-width="1.5" />
  <text x="44" y="248" fill="#1d4ed8" font-size="10.5" font-weight="700" font-family="'Consolas','Courier New',monospace">REST API · FASTAPI 0.163.1 &amp; UVICORN 0.54.0 (KONTRAK V2.1.0)</text>
  <text x="44" y="268" fill="#0f172a" font-size="14.5" font-weight="700">Layanan Terpadu (app/backend/api.py)</text>
  <text x="44" y="286" fill="#334155" font-size="11.5">Endpoint: /predict, /predict/batch, /health, /simulasi-wa · Pengaman: CORS, CSP, Rate Limit 60/mnt</text>

  <!-- Modul 1 -->
  <rect x="28" y="328" width="232" height="80" rx="6" fill="#ffffff" stroke="#1e293b" stroke-width="1.4" />
  <text x="40" y="348" fill="#475569" font-size="10" font-weight="700" font-family="'Consolas','Courier New',monospace">MODUL 1 · PRAPROSES</text>
  <text x="40" y="368" fill="#0f172a" font-size="13.5" font-weight="700">Normalisasi &amp; TF-IDF</text>
  <text x="40" y="388" fill="#334155" font-size="11.5">Stemming Sastrawi (cache 20rb)</text>
  <text x="40" y="402" fill="#475569" font-size="11.5">Sandi token_apk &amp; token_url</text>

  <!-- Modul 2 -->
  <rect x="280" y="328" width="240" height="80" rx="6" fill="#ffffff" stroke="#1e293b" stroke-width="1.4" />
  <text x="292" y="348" fill="#475569" font-size="10" font-weight="700" font-family="'Consolas','Courier New',monospace">MODUL 2 · KLASIFIKASI &amp; XAI</text>
  <text x="292" y="368" fill="#0f172a" font-size="13.5" font-weight="700">Skor Platt &amp; Alasan Awam</text>
  <text x="292" y="388" fill="#334155" font-size="11.5">Tingkat TINGGI / SEDANG / RENDAH</text>
  <text x="292" y="402" fill="#475569" font-size="11.5">Ekstraksi kata pemicu &amp; sorotan</text>

  <!-- Modul 3 (Focal) -->
  <rect x="540" y="328" width="232" height="80" rx="6" fill="rgba(194,65,12,0.06)" stroke="#c2410c" stroke-width="1.8" />
  <text x="552" y="348" fill="#c2410c" font-size="10" font-weight="700" font-family="'Consolas','Courier New',monospace">MODUL 3 · ATURAN DJP</text>
  <text x="552" y="368" fill="#0f172a" font-size="13">Aturan .apk &amp; Daftar Putih</text>
  <text x="552" y="388" fill="#334155" font-size="11.5">Deteksi .apk (eskalasi TINGGI)</text>
  <text x="552" y="402" fill="#c2410c" font-size="11.5" font-weight="600">79 TLD &amp; domain sah pajak.go.id</text>

  <!-- Node 3: Joblib -->
  <rect x="28" y="476" width="744" height="40" rx="6" fill="#ffffff" stroke="#c2410c" stroke-width="1.5" />
  <text x="400" y="501" text-anchor="middle" fill="#0f172a" font-size="13" font-weight="700">Bundel Model Terlatih (model_phishing_pajak.joblib) · TF-IDF 3.000 + LinearSVC Platt + RF</text>"""


def _diagram_l_1_body() -> str:
    # Clean schematic UI wireframe for Web & Extension: viewBox 800 x 476, coords on 4px grid
    return """  <!-- Panel A: Web Cek Pesan Pajak -->
  <rect x="16" y="16" width="492" height="444" rx="8" fill="#f8fafc" stroke="#1e293b" stroke-width="1.5" />
  <text x="32" y="40" fill="#1d4ed8" font-size="11" font-weight="700" letter-spacing="0.8" font-family="'Consolas','Courier New',monospace">A. ANTARMUKA WEB (APP/FRONTEND/INDEX.HTML)</text>

  <!-- Header Web -->
  <rect x="28" y="52" width="468" height="44" rx="6" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2" />
  <text x="44" y="79" fill="#0f3d75" font-size="14" font-weight="700">Cek Pesan Pajak</text>
  <rect x="240" y="62" width="76" height="24" rx="4" fill="#eff6ff" stroke="#1d4ed8" stroke-width="1.2" />
  <text x="278" y="78" text-anchor="middle" fill="#1d4ed8" font-size="11" font-weight="700">Cek Pesan</text>
  <rect x="324" y="62" width="92" height="24" rx="4" fill="#ffffff" stroke="#cbd5e1" stroke-width="1" />
  <text x="370" y="78" text-anchor="middle" fill="#475569" font-size="10.5">Web Resmi</text>
  <rect x="424" y="62" width="64" height="24" rx="4" fill="#fef2f2" stroke="#c2410c" stroke-width="1" />
  <text x="456" y="78" text-anchor="middle" fill="#c2410c" font-size="10.5" font-weight="700">.apk</text>

  <!-- Kolom Input Kiri -->
  <rect x="28" y="108" width="224" height="288" rx="6" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2" />
  <text x="42" y="130" fill="#0f172a" font-size="13" font-weight="700">Periksa Chat WhatsApp</text>
  <rect x="42" y="142" width="112" height="24" rx="4" fill="#f1f5f9" stroke="#94a3b8" stroke-width="1" />
  <text x="98" y="158" text-anchor="middle" fill="#1e293b" font-size="11" font-weight="600">Tempel &amp; Periksa</text>
  <rect x="42" y="176" width="196" height="96" rx="4" fill="#f8fafc" stroke="#94a3b8" stroke-width="1" />
  <text x="52" y="198" fill="#334155" font-size="11">Yth. Wajib Pajak, unduh</text>
  <text x="52" y="216" fill="#c2410c" font-size="11" font-weight="700">Pembaruan_Coretax_DJP.apk</text>
  <text x="52" y="234" fill="#334155" font-size="11">untuk verifikasi NPWP...</text>
  <text x="52" y="258" fill="#64748b" font-size="10">137 / 5.000 karakter</text>
  <rect x="42" y="284" width="196" height="32" rx="6" fill="#0f3d75" />
  <text x="140" y="305" text-anchor="middle" fill="#ffffff" font-size="12.5" font-weight="700">Periksa Pesan</text>
  <text x="42" y="336" fill="#475569" font-size="11" font-weight="600">Contoh Uji Cepat:</text>
  <rect x="42" y="346" width="94" height="34" rx="4" fill="#fef2f2" stroke="#c2410c" stroke-width="1" />
  <text x="89" y="367" text-anchor="middle" fill="#9a3412" font-size="10.5" font-weight="600">File .apk</text>
  <rect x="144" y="346" width="94" height="34" rx="4" fill="#f0fdf4" stroke="#15803d" stroke-width="1" />
  <text x="191" y="367" text-anchor="middle" fill="#166534" font-size="10.5" font-weight="600">Resmi DJP</text>

  <!-- Kolom Hasil Kanan -->
  <rect x="264" y="108" width="232" height="288" rx="6" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2" />
  <rect x="276" y="120" width="208" height="68" rx="6" fill="#fef2f2" stroke="#c2410c" stroke-width="1.5" />
  <text x="288" y="140" fill="#c2410c" font-size="10.5" font-weight="700">RISIKO TINGGI · SCAM 92%</text>
  <text x="288" y="160" fill="#7f1d1d" font-size="12" font-weight="700">Jangan Klik atau Download!</text>
  <text x="288" y="178" fill="#991b1b" font-size="10.5">Ada file .apk berbahaya.</text>

  <text x="276" y="210" fill="#0f172a" font-size="12" font-weight="700">Sorotan &amp; Kata Pemicu</text>
  <text x="276" y="228" fill="#475569" font-size="11">segera · unduh · instal</text>
  <text x="276" y="256" fill="#0f172a" font-size="12" font-weight="700">Alasan Deteksi (Awam)</text>
  <text x="276" y="274" fill="#334155" font-size="11">&bull; Lampiran .apk pencuri OTP</text>
  <text x="276" y="290" fill="#334155" font-size="11">&bull; Nada memaksa / ancam denda</text>
  <text x="276" y="316" fill="#0f172a" font-size="12" font-weight="700">Langkah Aman</text>
  <text x="276" y="334" fill="#334155" font-size="11">&bull; Jangan pasang .apk &amp; blokir</text>
  <text x="276" y="350" fill="#334155" font-size="11">&bull; Cek resmi di pajak.go.id</text>
  <rect x="276" y="362" width="100" height="22" rx="4" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1" />
  <text x="326" y="377" text-anchor="middle" fill="#1e293b" font-size="10.5">Salin Peringatan</text>
  <rect x="384" y="362" width="100" height="22" rx="4" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1" />
  <text x="434" y="377" text-anchor="middle" fill="#1e293b" font-size="10.5">Bagikan ke WA</text>

  <!-- Footer Web -->
  <rect x="28" y="408" width="468" height="40" rx="6" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2" />
  <text x="44" y="432" fill="#475569" font-size="11">Purwarupa TA UNSIA (TKT 6)</text>
  <rect x="348" y="416" width="136" height="24" rx="4" fill="#eff6ff" stroke="#1d4ed8" stroke-width="1.2" />
  <text x="416" y="432" text-anchor="middle" fill="#1d4ed8" font-size="11" font-weight="700">Info Akademik</text>

  <!-- Panel B: Ekstensi WhatsApp Web -->
  <rect x="524" y="16" width="260" height="444" rx="8" fill="#f8fafc" stroke="#1e293b" stroke-width="1.5" />
  <text x="538" y="40" fill="#1d4ed8" font-size="11" font-weight="700" letter-spacing="0.8" font-family="'Consolas','Courier New',monospace">B. EKSTENSI MANIFEST V3</text>

  <!-- Bubble Phishing -->
  <rect x="536" y="52" width="236" height="128" rx="6" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2" />
  <text x="548" y="72" fill="#0f172a" font-size="12" font-weight="700">Pesan Masuk (+62 857-xxxx)</text>
  <text x="548" y="92" fill="#334155" font-size="11">Login djp-coretax-verifikasi.xyz</text>
  <text x="548" y="108" fill="#334155" font-size="11">sebelum pukul 17.00 WIB.</text>
  <rect x="548" y="122" width="212" height="44" rx="4" fill="#fef2f2" stroke="#c2410c" stroke-width="1.4" />
  <text x="558" y="140" fill="#9a3412" font-size="11" font-weight="700">TINGGI · Jangan Klik!</text>
  <text x="558" y="156" fill="#b91c1c" font-size="10.5">Link luar DJP (Scam 84%)</text>

  <!-- Bubble Resmi -->
  <rect x="536" y="192" width="236" height="124" rx="6" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2" />
  <text x="548" y="212" fill="#0f172a" font-size="12" font-weight="700">Pesan Masuk (Info Resmi DJP)</text>
  <text x="548" y="232" fill="#334155" font-size="11">SPT via djponline.pajak.go.id</text>
  <text x="548" y="248" fill="#334155" font-size="11">atau hubungi Kring Pajak 1500200.</text>
  <rect x="548" y="262" width="212" height="42" rx="4" fill="#f0fdf4" stroke="#15803d" stroke-width="1.4" />
  <text x="558" y="280" fill="#166534" font-size="11" font-weight="700">RENDAH · Pola Resmi</text>
  <text x="558" y="295" fill="#15803d" font-size="10.5">Domain sah djponline.pajak.go.id</text>

  <!-- Popup Ekstensi -->
  <rect x="536" y="328" width="236" height="120" rx="6" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2" />
  <text x="548" y="348" fill="#0f3d75" font-size="12" font-weight="700">Popup Ekstensi (popup.html)</text>
  <rect x="720" y="334" width="40" height="20" rx="4" fill="#f0fdf4" stroke="#15803d" stroke-width="1" />
  <text x="740" y="348" text-anchor="middle" fill="#166534" font-size="10.5" font-weight="700">Siap</text>
  <text x="548" y="372" fill="#334155" font-size="11">Tempel teks WA untuk diperiksa</text>
  <text x="548" y="388" fill="#475569" font-size="10.5">melalui POST /predict (top_k=5)</text>
  <rect x="548" y="404" width="212" height="30" rx="5" fill="#0f3d75" />
  <text x="654" y="423" text-anchor="middle" fill="#ffffff" font-size="12" font-weight="700">Cek Pesan Sekarang</text>"""


def _find_browser() -> Path:
    for cand in CHROME_CANDIDATES:
        if cand.exists():
            return cand
    raise FileNotFoundError("Microsoft Edge atau Google Chrome tidak ditemukan.")


def _render_html_to_png(
    html_text: str, out_png: Path, width: int, height: int, scale: int = 3
) -> Path:
    browser = _find_browser()
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".html", encoding="utf-8", delete=False
    ) as tmp:
        tmp.write(html_text)
        tmp_html = Path(tmp.name)

    url = tmp_html.resolve().as_uri()
    cmd = [
        str(browser),
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        f"--force-device-scale-factor={scale}",
        f"--window-size={width},{height}",
        f"--screenshot={out_png.resolve()}",
        url,
    ]
    res = subprocess.run(cmd, check=False, capture_output=True, text=True, timeout=30)
    if res.returncode != 0 or not out_png.exists():
        tmp_html.unlink(missing_ok=True)
        raise RuntimeError(f"Gagal render {out_png.name}: {res.stderr or res.stdout}")
    return tmp_html


def build_all_diagrams(verify_dir: Path | None = None) -> list[Path]:
    specs = (
        (
            "Gambar 1.1 Tahapan Metode Penelitian",
            "Diagram alir enam tahapan metode penelitian dari kurasi korpus hingga purwarupa TKT 6.",
            800,
            336,
            _diagram_1_1_body(),
            ASSET_DIR / "Gambar 1.1 Tahapan Metode Penelitian.png",
        ),
        (
            "Gambar 2.1 Bagan Alir Prosedur Eksperimen",
            "Diagram alir tiga zona eksperimen LinearSVC Platt vs Random Forest beserta jalur kontrol bias.",
            800,
            564,
            _diagram_2_1_body(),
            ASSET_DIR / "Gambar 2.1 Bagan Alir Prosedur Eksperimen.png",
        ),
        (
            "Gambar 3.1 Arsitektur Sistem Terpadu",
            "Arsitektur tiga zona meliputi web, ekstensi Manifest V3, FastAPI, inferensi, dan bundel model.",
            800,
            540,
            _diagram_3_1_body(),
            ASSET_DIR / "Gambar 3.1 Arsitektur Sistem Terpadu.png",
        ),
        (
            "Gambar L.1 Rancangan Antarmuka Purwarupa dan Ekstensi",
            "Wireframe antarmuka web Cek Pesan Pajak dan ekstensi WhatsApp Web Manifest V3.",
            800,
            476,
            _diagram_l_1_body(),
            ASSET_DIR / "Gambar L.1 Rancangan Antarmuka Purwarupa dan Ekstensi.png",
        ),
    )

    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    if verify_dir is not None:
        verify_dir.mkdir(parents=True, exist_ok=True)

    html_files: list[Path] = []
    for title, desc, w, h, body, out_png in specs:
        html_doc = SVG_SHELL.format(title=title, desc=desc, vb_w=w, vb_h=h, body=body)
        tmp_html = _render_html_to_png(html_doc, out_png, width=w, height=h, scale=3)
        if verify_dir is not None:
            saved_html = verify_dir / f"{out_png.stem}.html"
            saved_html.write_text(html_doc, encoding="utf-8")
            html_files.append(saved_html)
        tmp_html.unlink(missing_ok=True)
        print(f"[OK] {out_png.name} ({w*3}x{h*3})")
    return html_files


def main() -> None:
    parser = argparse.ArgumentParser(description="Bangun ulang 4 bagan TA UNSIA resolusi tinggi.")
    parser.add_argument(
        "--save-html-dir",
        type=Path,
        default=None,
        help="Simpan berkas HTML sumber sementara untuk audit self_check & verify_geometry.",
    )
    args = parser.parse_args()
    html_files = build_all_diagrams(verify_dir=args.save_html_dir)
    if args.save_html_dir is not None:
        skill_scripts = Path(r"C:\Users\Lenovo\.gemini\config\skills\diagram-design\scripts")
        for hf in html_files:
            for checker in ("self_check.py", "verify_geometry.py"):
                cmd = [sys.executable, str(skill_scripts / checker)]
                if checker == "self_check.py":
                    cmd.append("--offline")
                cmd.append(str(hf))
                res = subprocess.run(cmd, capture_output=True, text=True, check=False)
                print(f"[{checker} :: {hf.name}] rc={res.returncode}")
                if res.stdout.strip():
                    print(" ", res.stdout.strip().replace("\n", " | "))
                if res.returncode != 0 and res.stderr.strip():
                    print("  ERR:", res.stderr.strip())


if __name__ == "__main__":
    main()
