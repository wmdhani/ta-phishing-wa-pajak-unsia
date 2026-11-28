"""Generator ringkasan usulan topik Tugas Akhir (.docx dan .pdf via Word COM)."""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

import docx
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
from docx.shared import Cm, Pt, RGBColor

try:
    from scripts.terapkan_metadata_dokumen import export_docx_to_pdf_via_word
except ImportError:
    from terapkan_metadata_dokumen import export_docx_to_pdf_via_word

FONT_NAME = "Times New Roman"
DEFAULT_TEXT_COLOR = RGBColor(0x11, 0x11, 0x11)

JUDUL_TEXT = (
    "Komparasi Algoritma Support Vector Machine dan Random Forest dalam "
    "Deteksi Pesan Phishing WhatsApp Mengatasnamakan Otoritas Perpajakan"
)


def _set_run_font(
    run: docx.text.run.Run,
    size_pt: float,
    bold: bool = False,
    italic: bool = False,
    color: RGBColor = DEFAULT_TEXT_COLOR,
) -> None:
    run.font.name = FONT_NAME
    run.font.size = Pt(size_pt)
    run.bold = bold
    run.italic = italic
    run.font.color.rgb = color
    r_pr = run._r.get_or_add_rPr()
    r_fonts = r_pr.find(qn("w:rFonts"))
    if r_fonts is None:
        r_fonts = OxmlElement("w:rFonts")
        r_pr.insert(0, r_fonts)
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        r_fonts.set(qn(attr), FONT_NAME)


def _add_styled_runs(
    paragraph: docx.text.paragraph.Paragraph,
    segments: Iterable[tuple[str, bool, bool]],
    size_pt: float = 10.0,
) -> None:
    for text, bold, italic in segments:
        run = paragraph.add_run(text)
        _set_run_font(run, size_pt=size_pt, bold=bold, italic=italic)


def _set_cell_padding(
    cell: docx.table._Cell, top: int, bottom: int, left: int, right: int
) -> None:
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_mar = OxmlElement("w:tcMar")
    for side, val in (("top", top), ("bottom", bottom), ("left", left), ("right", right)):
        node = OxmlElement(f"w:{side}")
        node.set(qn("w:w"), str(val))
        node.set(qn("w:type"), "dxa")
        tc_mar.append(node)
    tc_pr.append(tc_mar)


def _remove_table_borders(table: docx.table.Table) -> None:
    tbl_pr = table._tbl.tblPr
    borders = parse_xml(
        f"<w:tblBorders {nsdecls('w')}>"
        '<w:top w:val="none"/><w:left w:val="none"/>'
        '<w:bottom w:val="none"/><w:right w:val="none"/>'
        '<w:insideH w:val="none"/><w:insideV w:val="none"/>'
        "</w:tblBorders>"
    )
    tbl_pr.append(borders)


def _style_callout_cell(cell: docx.table._Cell) -> None:
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_pr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="F4F6F8"/>'))
    tc_pr.append(
        parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            '<w:top w:val="single" w:sz="6" w:space="0" w:color="B0BEC5"/>'
            '<w:left w:val="single" w:sz="6" w:space="0" w:color="B0BEC5"/>'
            '<w:bottom w:val="single" w:sz="6" w:space="0" w:color="B0BEC5"/>'
            '<w:right w:val="single" w:sz="6" w:space="0" w:color="B0BEC5"/>'
            "</w:tcBorders>"
        )
    )
    _set_cell_padding(cell, top=110, bottom=110, left=150, right=150)


def _add_section_heading(doc: docx.Document, title: str) -> None:
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(5.5)
    p.paragraph_format.space_after = Pt(1.5)
    p.paragraph_format.line_spacing = 1.1
    p.paragraph_format.keep_with_next = True
    _set_run_font(p.add_run(title), size_pt=10.5, bold=True)


def _add_body_paragraph(
    doc: docx.Document,
    segments: Iterable[tuple[str, bool, bool]],
    indent_cm: float = 0.0,
    first_line_cm: float = 0.0,
    space_after_pt: float = 2.0,
) -> None:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf = p.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(space_after_pt)
    pf.line_spacing = 1.12
    if indent_cm:
        pf.left_indent = Cm(indent_cm)
    if first_line_cm:
        pf.first_line_indent = Cm(first_line_cm)
    _add_styled_runs(p, segments, size_pt=10.0)


def build_proposal_docx(docx_path: Path) -> None:
    doc = docx.Document()
    normal = doc.styles["Normal"]
    normal.font.name = FONT_NAME
    normal.font.size = Pt(10)

    sec = doc.sections[0]
    sec.page_width = Cm(21.0)
    sec.page_height = Cm(29.7)
    sec.top_margin = Cm(1.5)
    sec.bottom_margin = Cm(1.4)
    sec.left_margin = Cm(2.3)
    sec.right_margin = Cm(2.1)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(1.5)
    _set_run_font(p_title.add_run("RINGKASAN USULAN TOPIK TUGAS AKHIR"), size_pt=12.5, bold=True)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(6)
    _set_run_font(
        p_sub.add_run("Program Studi PJJ Sistem Informasi \u2013 Universitas Siber Asia (UNSIA)"),
        size_pt=10.5,
    )

    meta_rows = [
        ("Nama Mahasiswa", ": Wan Mirza Dhani"),
        ("NIM", ": 240101020194"),
        ("Program Studi", ": PJJ Sistem Informasi"),
        ("Ketua Program Studi", ": Vika Febri Muliati, S.Kom., M.Kom"),
        ("Dosen Pembimbing", ": Novi Dian Nathasia, S.Kom, MMSI."),
        ("Skema Tugas Akhir", ": Tugas Akhir Prototype (Target TKT Level 6)"),
    ]
    meta_table = doc.add_table(rows=len(meta_rows), cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.LEFT
    meta_table.autofit = False
    _remove_table_borders(meta_table)
    for row_idx, (label, val) in enumerate(meta_rows):
        row = meta_table.rows[row_idx]
        for col_idx, width, text in ((0, Cm(4.2), label), (1, Cm(12.2), val)):
            cell = row.cells[col_idx]
            cell.width = width
            _set_cell_padding(cell, top=18, bottom=18, left=0, right=40)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.08
            _set_run_font(p.add_run(text), size_pt=10.0)

    _add_section_heading(doc, "Usulan Judul Tugas Akhir:")
    callout = doc.add_table(rows=1, cols=1)
    callout.alignment = WD_TABLE_ALIGNMENT.CENTER
    callout.autofit = False
    box_cell = callout.cell(0, 0)
    box_cell.width = Cm(16.4)
    _style_callout_cell(box_cell)
    p_box = box_cell.paragraphs[0]
    p_box.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_box.paragraph_format.space_before = Pt(0)
    p_box.paragraph_format.space_after = Pt(0)
    p_box.paragraph_format.line_spacing = 1.15
    _set_run_font(p_box.add_run(f'"{JUDUL_TEXT}"'), size_pt=10.5, bold=True)

    _add_section_heading(doc, "1. Latar Belakang & Urgensi Masalah")
    _add_body_paragraph(
        doc,
        [
            ("Maraknya penipuan berbasis rekayasa sosial (", False, False),
            ("social engineering", False, True),
            (
                (
                    ") melalui WhatsApp yang mengatasnamakan Direktorat Jenderal Pajak (DJP)"
                    "\u2014seperti modus pemutakhiran data Coretax, surat tagihan pajak kurang bayar, "
                    "pemadanan NIK-NPWP, hingga pengiriman file berbahaya berformat "
                ),
                False,
                False,
            ),
            (".apk", False, True),
            (
                (
                    "\u2014sering mengecoh masyarakat karena meniru gaya bahasa surat dinas resmi. "
                    "Di sisi lain, penyaring spam umum rentan mengalami bias kata kunci terhadap pesan resmi DJP, "
                    "sedangkan pemeriksaan web manual mengharuskan pengguna menyalin-tempel pesan satu per satu. "
                    "Diperlukan sistem deteksi otomatis berbasis "
                ),
                False,
                False,
            ),
            ("Natural Language Processing", False, True),
            (
                    (
                        " (NLP) yang terintegrasi ke REST API, ekstensi peramban WhatsApp Web dengan penjelasan "
                        "indikator risiko berbahasa awam, dan "
                    ),
                    False,
                    False,
                ),
                ("antarmuka web Cek Pesan Pajak", False, True),
                (".", False, False),
            ],
        )

    _add_section_heading(doc, "2. Rumusan Masalah")
    for item in (
        [
            ("1) Kemiripan bahasa kedinasan dan istilah perpajakan sahih pada pesan ", False, False),
            ("phishing", False, True),
            (
                (
                    " WhatsApp menyulitkan verifikasi manual oleh wajib pajak sehingga berisiko "
                    "menimbulkan kerugian finansial dan pencurian kredensial."
                ),
                False,
                False,
            ),
        ],
        [
            (
                (
                    "2) Penyaringan spam konvensional tanpa penyeimbangan korpus resmi perpajakan "
                    "menimbulkan bias kata kunci ("
                ),
                False,
                False,
            ),
            ("keyword bias", False, True),
            ("), yang memicu salah blokir pesan resmi DJP (", False, False),
            ("false positive", False, True),
            (") maupun lolosnya pesan penipuan (", False, False),
            ("false negative", False, True),
            (").", False, False),
        ],
        [
            ("3) Diperlukan pengujian empiris untuk membandingkan kinerja ", False, False),
            ("Support Vector Machine", False, True),
            (" (", False, False),
            ("LinearSVC", False, True),
            (") dan ", False, False),
            ("Random Forest Classifier", False, True),
            (" pada fitur TF-IDF ", False, False),
            ("n-gram", False, True),
            (
                (
                    " guna diintegrasikan ke sistem verifikasi langsung tanpa salin-tempel melalui REST API (FastAPI), "
                    "ekstensi peramban WhatsApp Web dengan penjelasan indikator risiko berbahasa awam, serta "
                ),
                False,
                False,
            ),
            ("antarmuka web Cek Pesan Pajak", False, True),
            (".", False, False),
        ],
    ):
        _add_body_paragraph(doc, item, indent_cm=0.42, first_line_cm=-0.42, space_after_pt=1.5)

    _add_section_heading(doc, "3. Sumber Data & Kesiapan Dataset (Data Publik Terbuka)")
    _add_body_paragraph(
        doc,
        [
            ("Penelitian ini ", False, False),
            ("tidak menggunakan data internal/rahasia instansi", True, False),
            (
                (
                    ", melainkan murni memanfaatkan data publik terbuka yang telah selesai dihimpun, "
                    "dikurasi, dan dicatat integritas SHA-256-nya ("
                ),
                False,
                False,
            ),
            ("1.164 baris dataset gabungan utama", True, False),
            ("):", False, False),
        ],
        space_after_pt=1.5,
    )
    for bullet in (
        [
            ("\u2022 ", False, False),
            ("Korpus Dasar Publik (904 baris)", True, False),
            (": Dataset ", False, False),
            ("benchmark", False, True),
            (
                " SMS/pesan penipuan vs pesan normal berbahasa Indonesia (335 penipuan dan 569 normal, dari 1.143 baris pascaeksklusi 239 pesan promo/operator).",
                False,
                False,
            ),
        ],
        [
            ("\u2022 ", False, False),
            ("Korpus Spesifik Perpajakan (260 baris seimbang)", True, False),
            (": Kurasi dari ", False, False),
            ("65 dari 68 sumber publik", True, False),
            (" yang dihimpun (sebagian besar terbit 2024\u20132026: ", False, False),
            ("pajak.go.id", False, True),
            (
                (
                    ", KPP/KP2KP, portal cek fakta, dan media pajak terverifikasi) terdiri atas 130 pesan modus "
                    "penipuan pajak (12 kategori) dan 130 pesan resmi/normal (10 kategori) untuk mencegah bias kata kunci."
                ),
                False,
                False,
            ),
        ],
    ):
        _add_body_paragraph(doc, bullet, indent_cm=0.35, first_line_cm=-0.28, space_after_pt=1.5)

    _add_section_heading(doc, "4. Metode, Hasil Uji Ablasi & Rencana Luaran Prototype")
    for bullet in (
        [
            ("\u2022 ", False, False),
            ("Tahapan NLP", True, False),
            (": ", False, False),
            ("Case Folding", False, True),
            (", tokenisasi khusus berkas ", False, False),
            (".apk", False, True),
            (" (", False, False),
            ("token_apk", False, True),
            (") dan tautan (", False, False),
            ("token_url", False, True),
            ("), pembersihan karakter nonalfanumerik, ", False, False),
            ("Stopword Removal", False, True),
            (", ", False, False),
            ("Stemming Sastrawi", False, True),
            (", serta pembobotan ", False, False),
            ("TF-IDF n-gram (1, 2)", True, False),
            (" maksimal 3.000 fitur.", False, False),
        ],
        [
            ("\u2022 ", False, False),
            ("Komparasi Model & Uji Ablasi", True, False),
            (": Deduplikasi Sastrawi (1.159 unik) dan pembagian terstratifikasi 80:20 (927 latih; 232 uji) membandingkan ", False, False),
            ("Support Vector Machine (LinearSVC)", True, False),
            (" dan ", False, False),
            ("Random Forest Classifier", True, False),
            (" via ", False, False),
            ("Confusion Matrix", False, True),
            (" & ", False, False),
            ("10-Fold CV", False, True),
            (". Pada ", False, False),
            ("10-Fold CV", False, True),
            (", LinearSVC meraih F1-Score ", False, False),
            ("97,16%", True, False),
            (" (Accuracy ", False, False),
            ("97,74%", True, False),
            (") vs Random Forest ", False, False),
            ("94,07%", True, False),
            (", serta ", False, False),
            ("Brier Score 0,02542", True, False),
            (" pada holdout. Pada uji ketahanan domain pajak, subset uji pajak (n = 45) meraih Accuracy ", False, False),
            ("95,56%", True, False),
            (" (ROC-AUC ", False, False),
            ("0,9960", True, False),
            ("; 20/21 pesan resmi lolos) dan ", False, False),
            ("98,17% F1-Score", True, False),
            (" pada 10-Fold CV 260 baris.", False, False),
        ],
        [
            ("\u2022 ", False, False),
            ("Arsitektur Prototype (TKT 6)", True, False),
            (": Sistem terpadu berbasis ", False, False),
            ("REST API (FastAPI)", True, False),
            (", ", False, False),
            ("Ekstensi Peramban WhatsApp Web (Manifest V3)", True, False),
            (" (tombol pemeriksaan langsung ", False, False),
            ("Cek Pesan Pajak", False, True),
            (" pada gelembung obrolan dan jendela ", False, False),
            ("popup", False, True),
            (" tanpa ", False, False),
            ("copy-paste", False, True),
            ("), serta ", False, False),
            ("Antarmuka Web Cek Pesan Pajak", True, False),
            (", dilengkapi lapisan ", False, False),
            ("explainable detection", False, True),
            (" (bobot kata pemicu ", False, False),
            ("LinearSVC", False, True),
            (", deteksi ", False, False),
            (".apk/token_apk", False, True),
            (", dan verifikasi domain ", False, False),
            ("pajak.go.id", False, True),
            (").", False, False),
        ],
        [
            ("\u2022 ", False, False),
            ("Manfaat bagi Masyarakat & UNSIA", True, False),
            (
                (
                    ": Memudahkan wajib pajak memeriksa pesan langsung di WhatsApp Web serta menyediakan korpus "
                    "terbuka dan modul purwarupa sebagai aset praktikum/pembelajaran NLP Prodi PJJ Sistem Informasi "
                ),
                False,
                False,
            ),
            ("Universitas Siber Asia (UNSIA)", True, False),
            (" dan penguat literasi keamanan siber ekosistem kampus daring.", False, False),
        ],
    ):
        _add_body_paragraph(doc, bullet, indent_cm=0.35, first_line_cm=-0.28, space_after_pt=1.5)

    doc.save(str(docx_path))


def build_docs() -> None:
    proposal_dir = Path(__file__).resolve().parent.parent / "02-proposal"
    proposal_dir.mkdir(parents=True, exist_ok=True)
    docx_path = proposal_dir / "usulan-judul-ta-wan-mirza-dhani-240101020194.docx"
    pdf_path = proposal_dir / "usulan-judul-ta-wan-mirza-dhani-240101020194.pdf"

    build_proposal_docx(docx_path)
    out_pdf, pdf_info = export_docx_to_pdf_via_word(docx_path, pdf_path=pdf_path)
    print("DOCX updated:", docx_path)
    print("PDF exported via Word COM:", out_pdf, pdf_info)


if __name__ == "__main__":
    build_docs()
