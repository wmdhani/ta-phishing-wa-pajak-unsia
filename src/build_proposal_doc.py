from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
import docx
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH


def build_docs() -> None:
    pdf_path = "doc/proposal/Usulan_Judul_TA_Wan_Mirza_Dhani_240101020194.pdf"
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        topMargin=2.2 * cm,
        bottomMargin=2.2 * cm,
        leftMargin=2.8 * cm,
        rightMargin=2.5 * cm,
    )
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Heading1"],
        fontName="Times-Roman",
        fontSize=13,
        leading=16,
        alignment=TA_CENTER,
        spaceAfter=4,
    )
    subtitle_style = ParagraphStyle(
        "DocSub",
        parent=styles["Normal"],
        fontName="Times-Roman",
        fontSize=11,
        leading=14,
        alignment=TA_CENTER,
        spaceAfter=14,
    )
    h2_style = ParagraphStyle(
        "H2",
        parent=styles["Heading2"],
        fontName="Times-Bold",
        fontSize=11,
        leading=14,
        spaceBefore=9,
        spaceAfter=4,
    )
    body_style = ParagraphStyle(
        "Body",
        parent=styles["Normal"],
        fontName="Times-Roman",
        fontSize=10.5,
        leading=15,
        alignment=TA_JUSTIFY,
        spaceAfter=5,
    )
    box_style = ParagraphStyle(
        "Box",
        parent=styles["Normal"],
        fontName="Times-Bold",
        fontSize=11,
        leading=15,
        alignment=TA_CENTER,
    )

    story = [
        Paragraph("<b>RINGKASAN USULAN TOPIK TUGAS AKHIR</b>", title_style),
        Paragraph("Program Studi PJJ Informatika – Universitas Siber Asia (UNSIA)", subtitle_style),
    ]

    meta_data = [
        ["Nama Mahasiswa", ": Wan Mirza Dhani"],
        ["NIM", ": 240101020194"],
        ["Dosen Pembimbing", ": Novi Dian Nathasia, S.Kom, MMSI."],
        ["Skema Tugas Akhir", ": Tugas Akhir Prototype"],
    ]
    t = Table(meta_data, colWidths=[4.2 * cm, 11 * cm], hAlign="LEFT")
    t.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (-1, -1), "Times-Roman"),
                ("FONTSIZE", (0, 0), (-1, -1), 10.5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
            ]
        )
    )
    story.append(t)
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Usulan Judul Tugas Akhir:</b>", h2_style))
    judul_text = (
        "Komparasi Algoritma Support Vector Machine dan Random Forest dalam "
        "Deteksi Pesan Phishing WhatsApp Mengatasnamakan Otoritas Perpajakan"
    )
    jt = Table([[Paragraph(f'<b>"{judul_text}"</b>', box_style)]], colWidths=[15.5 * cm])
    jt.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F4F6F8")),
                ("BOX", (0, 0), (-1, -1), 0.75, colors.HexColor("#B0BEC5")),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ]
        )
    )
    story.append(jt)

    story.append(Paragraph("<b>1. Latar Belakang &amp; Urgensi Masalah</b>", h2_style))
    story.append(
        Paragraph(
            "Maraknya penipuan berbasis rekayasa sosial (<i>social engineering</i>) melalui WhatsApp yang "
            "mengatasnamakan Direktorat Jenderal Pajak (DJP)—seperti modus pemutakhiran data Coretax, surat "
            "tagihan pajak kurang bayar, pemadanan NIK-NPWP, hingga pengiriman file berbahaya berformat "
            "<i>.apk</i>—sering mengecoh masyarakat karena menggunakan gaya bahasa menyerupai surat dinas resmi. "
            "Diperlukan sistem deteksi otomatis berbasis <i>Natural Language Processing</i> (NLP) untuk membantu "
            "pengguna memverifikasi indikasi penipuan dari teks pesan yang diterima.",
            body_style,
        )
    )

    story.append(Paragraph("<b>2. Rumusan Masalah</b>", h2_style))
    story.append(
        Paragraph(
            "1) Pesan penipuan (<i>phishing</i>) WhatsApp bertema perpajakan memiliki pola kalimat persuasif yang "
            "sulit dibedakan oleh wajib pajak awam sehingga berisiko menimbulkan kerugian finansial dan pencurian data.<br/>"
            "2) Diperlukan pengujian empiris untuk membandingkan kinerja algoritma <i>Support Vector Machine</i> (SVM) "
            "dan <i>Random Forest</i> (RF) dalam mengklasifikasikan teks pesan berbahasa Indonesia bertema perpajakan.",
            body_style,
        )
    )

    story.append(Paragraph("<b>3. Sumber Data &amp; Kesiapan Dataset (Data Publik Terbuka)</b>", h2_style))
    story.append(
        Paragraph(
            "Penelitian ini <b>tidak menggunakan data internal/rahasia instansi</b>, melainkan murni memanfaatkan "
            "data publik terbuka yang telah mulai dikumpulkan (saat ini telah siap <b>944 baris data awal</b>):<br/>"
            "• <b>Korpus Dasar Publik (904 baris)</b>: Dataset <i>benchmark</i> SMS/pesan penipuan vs pesan normal berbahasa Indonesia.<br/>"
            "• <b>Korpus Spesifik Perpajakan (40 baris awal, akan diperluas ke 150–300 baris)</b>: Sampel teks modus "
            "penipuan pajak dari rilis imbauan publik resmi DJP (<i>pajak.go.id</i> / media massa) disandingkan dengan "
            "format notifikasi resmi publik DJP agar model tidak mengalami <i>bias</i> kata kunci.",
            body_style,
        )
    )

    story.append(Paragraph("<b>4. Metode &amp; Rencana Luaran Prototype</b>", h2_style))
    story.append(
        Paragraph(
            "• <b>Tahapan NLP</b>: <i>Text Preprocessing</i> (<i>Cleaning, Case Folding, Normalisasi, Stopword Removal, "
            "Stemming Sastrawi</i>) dan ekstraksi fitur menggunakan <b>TF-IDF</b>.<br/>"
            "• <b>Komparasi Model</b>: Membandingkan <b>Support Vector Machine (SVM)</b> dan <b>Random Forest</b> "
            "menggunakan <i>Confusion Matrix</i> (<i>Accuracy, Precision, Recall,</i> dan <i>F1-Score</i>).<br/>"
            "• <b>Bentuk Prototype</b>: Aplikasi web interaktif berbasis Python (<b>Streamlit</b>) tempat pengguna "
            "menempelkan teks pesan WhatsApp mencurigakan dan langsung memperoleh status analisis (<i>Aman</i> / "
            "<i>Indikasi Phishing</i>) beserta skor probabilitasnya.",
            body_style,
        )
    )

    doc.build(story)
    print("PDF created:", pdf_path)

    wdoc = docx.Document()
    for section in wdoc.sections:
        section.top_margin = Cm(2.5)
        section.bottom_margin = Cm(2.5)
        section.left_margin = Cm(3.0)
        section.right_margin = Cm(2.5)

    p_title = wdoc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("RINGKASAN USULAN TOPIK TUGAS AKHIR\n")
    r_title.bold = True
    r_title.font.size = Pt(13)
    r_sub = p_title.add_run("Program Studi PJJ Informatika – Universitas Siber Asia (UNSIA)")
    r_sub.font.size = Pt(11)

    p_meta = wdoc.add_paragraph()
    p_meta.add_run("Nama Mahasiswa\t: Wan Mirza Dhani\n")
    p_meta.add_run("NIM\t\t\t: 240101020194\n")
    p_meta.add_run("Dosen Pembimbing\t: Novi Dian Nathasia, S.Kom, MMSI.\n")
    p_meta.add_run("Skema Tugas Akhir\t: Tugas Akhir Prototype")

    wdoc.add_heading("Usulan Judul Tugas Akhir", level=2)
    p_j = wdoc.add_paragraph()
    r_j = p_j.add_run(f'"{judul_text}"')
    r_j.bold = True

    sections_content = [
        (
            "1. Latar Belakang & Urgensi Masalah",
            "Maraknya penipuan berbasis rekayasa sosial (social engineering) melalui WhatsApp yang mengatasnamakan "
            "Direktorat Jenderal Pajak (DJP)—seperti modus pemutakhiran data Coretax, surat tagihan pajak kurang bayar, "
            "pemadanan NIK-NPWP, hingga pengiriman file berbahaya berformat .apk—sering mengecoh masyarakat karena "
            "menggunakan gaya bahasa menyerupai surat dinas resmi. Diperlukan sistem deteksi otomatis berbasis Natural "
            "Language Processing (NLP) untuk membantu pengguna memverifikasi indikasi penipuan dari teks pesan yang diterima.",
        ),
        (
            "2. Rumusan Masalah",
            "1) Pesan penipuan (phishing) WhatsApp bertema perpajakan memiliki pola kalimat persuasif yang sulit "
            "dibedakan oleh wajib pajak awam sehingga berisiko menimbulkan kerugian finansial dan pencurian data.\n"
            "2) Diperlukan pengujian empiris untuk membandingkan kinerja algoritma Support Vector Machine (SVM) dan "
            "Random Forest (RF) dalam mengklasifikasikan teks pesan berbahasa Indonesia bertema perpajakan.",
        ),
        (
            "3. Sumber Data & Kesiapan Dataset",
            "Penelitian ini tidak menggunakan data internal/rahasia instansi, melainkan murni memanfaatkan data publik "
            "terbuka yang telah mulai dikumpulkan (saat ini terkumpul 944 baris data awal):\n"
            "- Korpus Dasar Publik (904 baris): Dataset benchmark SMS/pesan penipuan vs pesan normal berbahasa Indonesia.\n"
            "- Korpus Spesifik Perpajakan (40 baris awal, akan diperluas ke 150-300 baris): Sampel teks modus penipuan "
            "pajak dari imbauan publik resmi DJP (pajak.go.id / media massa) disandingkan dengan format notifikasi resmi publik DJP.",
        ),
        (
            "4. Metode & Rencana Luaran Prototype",
            "- Tahapan NLP: Text Preprocessing (Cleaning, Case Folding, Normalisasi, Stopword Removal, Stemming Sastrawi) "
            "dan pembobotan fitur kata menggunakan TF-IDF.\n"
            "- Komparasi Model: Membandingkan Support Vector Machine (SVM) dan Random Forest menggunakan Confusion Matrix "
            "(Accuracy, Precision, Recall, dan F1-Score).\n"
            "- Bentuk Prototype: Aplikasi web interaktif berbasis Python (Streamlit) tempat pengguna menempelkan teks "
            "pesan WhatsApp mencurigakan dan langsung memperoleh status analisis (Aman / Indikasi Phishing) beserta skor probabilitasnya.",
        ),
    ]

    for sec_title, sec_body in sections_content:
        wdoc.add_heading(sec_title, level=2)
        wdoc.add_paragraph(sec_body)

    docx_path = "doc/proposal/Usulan_Judul_TA_Wan_Mirza_Dhani_240101020194.docx"
    wdoc.save(docx_path)
    print("DOCX created:", docx_path)


if __name__ == "__main__":
    build_docs()
