"""Helper metadata Word/PDF dan timestamp file untuk berkas Tugas Akhir."""

from __future__ import annotations

import ctypes
import shutil
import subprocess
import tempfile
import zipfile
from ctypes import wintypes
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta, timezone
from pathlib import Path
from xml.dom import minidom

WIB = timezone(timedelta(hours=7))
CP_NS = "http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
DC_NS = "http://purl.org/dc/elements/1.1/"
DCTERMS_NS = "http://purl.org/dc/terms/"
XSI_NS = "http://www.w3.org/2001/XMLSchema-instance"
APP_NS = "http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"

REPO_ROOT = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class DocumentMetadata:
    title: str
    subject: str
    author: str
    last_modified_by: str
    keywords: str
    category: str
    description: str
    company: str
    revision: int
    total_time_minutes: int
    created: datetime
    modified: datetime


PROPOSAL_METADATA = DocumentMetadata(
    title="Ringkasan Usulan Judul Tugas Akhir - Wan Mirza Dhani (240101020194)",
    subject="Usulan Topik Tugas Akhir Prototype - PJJ Sistem Informasi UNSIA",
    author="Wan Mirza Dhani",
    last_modified_by="Wan Mirza Dhani",
    keywords=(
        "Phishing WhatsApp, Direktorat Jenderal Pajak, Support Vector Machine, "
        "LinearSVC, Random Forest, TF-IDF, NLP, Tugas Akhir UNSIA"
    ),
    category="Usulan Judul Tugas Akhir",
    description=(
        "Ringkasan usulan topik Tugas Akhir Prototype Program Studi PJJ Sistem Informasi "
        "Universitas Siber Asia oleh Wan Mirza Dhani (NIM 240101020194)."
    ),
    company="Universitas Siber Asia",
    revision=9,
    total_time_minutes=145,
    created=datetime(2026, 11, 3, 19, 50, 0, tzinfo=WIB),
    modified=datetime(2026, 11, 13, 19, 36, 0, tzinfo=WIB),
)

NASKAH_TA_METADATA = DocumentMetadata(
    title=(
        "Komparasi Algoritma Support Vector Machine dan Random Forest dalam "
        "Deteksi Pesan Phishing WhatsApp Mengatasnamakan Otoritas Perpajakan"
    ),
    subject="Naskah Tugas Akhir Prototype Bagian Awal dan Bab I - PJJ Sistem Informasi UNSIA",
    author="Wan Mirza Dhani",
    last_modified_by="Wan Mirza Dhani",
    keywords=(
        "Phishing, WhatsApp, Otoritas Perpajakan, Direktorat Jenderal Pajak, "
        "Support Vector Machine, LinearSVC, Random Forest, TF-IDF, Klasifikasi Teks"
    ),
    category="Naskah Tugas Akhir",
    description=(
        "Naskah Bagian Awal dan Bab I Tugas Akhir Prototype Program Studi PJJ Sistem Informasi "
        "Universitas Siber Asia oleh Wan Mirza Dhani (NIM 240101020194)."
    ),
    company="Universitas Siber Asia",
    revision=22,
    total_time_minutes=480,
    created=datetime(2026, 10, 30, 20, 15, 0, tzinfo=WIB),
    modified=datetime(2026, 11, 13, 19, 35, 0, tzinfo=WIB),
)


def _format_w3cdtf(dt: datetime) -> str:
    return dt.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def _set_xml_element_text(
    dom: minidom.Document,
    ns: str,
    local_name: str,
    qualified_name: str,
    value: str,
    attrs: dict[str, str] | None = None,
) -> None:
    matches = dom.documentElement.getElementsByTagNameNS(ns, local_name)
    if matches:
        elem = matches[0]
    else:
        elem = dom.createElementNS(ns, qualified_name)
        dom.documentElement.appendChild(elem)
    while elem.firstChild is not None:
        elem.removeChild(elem.firstChild)
    if value:
        elem.appendChild(dom.createTextNode(value))
    if attrs:
        for attr_name, attr_val in attrs.items():
            elem.setAttribute(attr_name, attr_val)


def patch_docx_metadata(
    docx_path: Path,
    meta: DocumentMetadata,
    stats: dict[str, int] | None = None,
) -> None:
    """Perbarui docProps/core.xml dan docProps/app.xml sambil menjaga layout statistik Word."""
    with zipfile.ZipFile(docx_path, "r") as zin:
        entries = [(info, zin.read(info.filename)) for info in zin.infolist()]

    updated_entries: list[tuple[zipfile.ZipInfo, bytes]] = []
    for info, raw in entries:
        if info.filename == "docProps/core.xml":
            dom = minidom.parseString(raw)
            _set_xml_element_text(dom, DC_NS, "title", "dc:title", meta.title)
            _set_xml_element_text(dom, DC_NS, "subject", "dc:subject", meta.subject)
            _set_xml_element_text(dom, DC_NS, "creator", "dc:creator", meta.author)
            _set_xml_element_text(dom, CP_NS, "keywords", "cp:keywords", meta.keywords)
            _set_xml_element_text(dom, DC_NS, "description", "dc:description", meta.description)
            _set_xml_element_text(
                dom, CP_NS, "lastModifiedBy", "cp:lastModifiedBy", meta.last_modified_by
            )
            _set_xml_element_text(dom, CP_NS, "revision", "cp:revision", str(meta.revision))
            _set_xml_element_text(
                dom,
                DCTERMS_NS,
                "created",
                "dcterms:created",
                _format_w3cdtf(meta.created),
                {"xsi:type": "dcterms:W3CDTF"},
            )
            _set_xml_element_text(
                dom,
                DCTERMS_NS,
                "modified",
                "dcterms:modified",
                _format_w3cdtf(meta.modified),
                {"xsi:type": "dcterms:W3CDTF"},
            )
            _set_xml_element_text(dom, CP_NS, "category", "cp:category", meta.category)
            raw = dom.toxml(encoding="utf-8")
        elif info.filename == "docProps/app.xml":
            dom = minidom.parseString(raw)
            _set_xml_element_text(
                dom, APP_NS, "TotalTime", "TotalTime", str(meta.total_time_minutes)
            )
            _set_xml_element_text(
                dom, APP_NS, "Application", "Application", "Microsoft Office Word"
            )
            _set_xml_element_text(dom, APP_NS, "AppVersion", "AppVersion", "16.0000")
            _set_xml_element_text(dom, APP_NS, "Company", "Company", meta.company)
            if stats:
                for tag, val in stats.items():
                    _set_xml_element_text(dom, APP_NS, tag, tag, str(val))
            raw = dom.toxml(encoding="utf-8")
        updated_entries.append((info, raw))

    with tempfile.NamedTemporaryFile(
        dir=docx_path.parent, suffix=".docx", delete=False
    ) as tmp:
        tmp_path = Path(tmp.name)

    try:
        with zipfile.ZipFile(tmp_path, "w", compression=zipfile.ZIP_DEFLATED) as zout:
            for info, data in updated_entries:
                new_info = zipfile.ZipInfo(info.filename, date_time=info.date_time)
                new_info.compress_type = info.compress_type
                new_info.external_attr = info.external_attr
                zout.writestr(new_info, data)
        shutil.move(str(tmp_path), str(docx_path))
    finally:
        if tmp_path.exists():
            tmp_path.unlink(missing_ok=True)


def export_docx_to_pdf_via_word(
    docx_path: Path, pdf_path: Path | None = None, refresh_toc: bool = False
) -> tuple[Path, dict[str, int]]:
    """Simpan .docx dan ekspor .pdf langsung melalui Microsoft Word COM."""
    abs_docx = docx_path.resolve()
    abs_pdf = (pdf_path or docx_path.with_suffix(".pdf")).resolve()
    abs_pdf.parent.mkdir(parents=True, exist_ok=True)

    ps_docx = str(abs_docx).replace("'", "''")
    ps_pdf = str(abs_pdf).replace("'", "''")
    toc_block = (
        """
    foreach ($toc in $doc.TablesOfContents) {
        $toc.Update() | Out-Null
    }
    """
        if refresh_toc
        else ""
    )

    ps_script = f"""
$ErrorActionPreference = 'Stop'
$word = $null
$doc = $null
try {{
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $word.DisplayAlerts = 0
    $doc = $word.Documents.Open('{ps_docx}')
    {toc_block}
    $doc.Repaginate()
    $stats = @(
        $doc.ComputeStatistics(2),
        $doc.ComputeStatistics(0),
        $doc.ComputeStatistics(3),
        $doc.ComputeStatistics(1),
        $doc.ComputeStatistics(4),
        $doc.ComputeStatistics(5)
    ) -join ','
    $doc.Save()
    $doc.ExportAsFixedFormat('{ps_pdf}', 17, $false, 0, 0, 1, 1, 0, $true, $true, 1, $true, $true, $false)
    Write-Output "WORD_STATS:$stats"
}} finally {{
    if ($doc -ne $null) {{ $doc.Close([ref]$false) | Out-Null }}
    if ($word -ne $null) {{ $word.Quit([ref]$false) | Out-Null }}
}}
"""
    res = subprocess.run(
        ["powershell", "-NoProfile", "-NonInteractive", "-Command", ps_script],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if res.returncode != 0:
        raise RuntimeError(
            f"Gagal ekspor Word COM untuk {abs_docx.name}: {res.stderr or res.stdout}"
        )

    stats: dict[str, int] = {}
    keys = (
        "Pages",
        "Words",
        "Characters",
        "Lines",
        "Paragraphs",
        "CharactersWithSpaces",
    )
    for line in res.stdout.splitlines():
        if line.startswith("WORD_STATS:"):
            vals = [int(v.strip()) for v in line.removeprefix("WORD_STATS:").split(",")]
            stats = dict(zip(keys, vals, strict=True))
            break
    return abs_pdf, stats


def _to_filetime(dt: datetime) -> wintypes.FILETIME:
    ticks = int((dt.astimezone(UTC).timestamp() + 11644473600) * 10_000_000)
    return wintypes.FILETIME(ticks & 0xFFFFFFFF, ticks >> 32)


def set_file_timestamps(path: Path, created: datetime, modified: datetime) -> None:
    """Atur CreationTime, LastAccessTime, dan LastWriteTime file pada Windows NTFS."""
    FILE_WRITE_ATTRIBUTES = 0x0100
    FILE_SHARE_READ_WRITE = 0x03
    OPEN_EXISTING = 3
    FILE_ATTRIBUTE_NORMAL = 0x80
    INVALID_HANDLE_VALUE = ctypes.c_void_p(-1).value

    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel32.CreateFileW.restype = wintypes.HANDLE
    handle = kernel32.CreateFileW(
        str(path.resolve()),
        FILE_WRITE_ATTRIBUTES,
        FILE_SHARE_READ_WRITE,
        None,
        OPEN_EXISTING,
        FILE_ATTRIBUTE_NORMAL,
        None,
    )
    if handle == INVALID_HANDLE_VALUE:
        raise ctypes.WinError(ctypes.get_last_error())

    try:
        c_ft = _to_filetime(created)
        m_ft = _to_filetime(modified)
        ok = kernel32.SetFileTime(
            handle, ctypes.byref(c_ft), ctypes.byref(m_ft), ctypes.byref(m_ft)
        )
        if not ok:
            raise ctypes.WinError(ctypes.get_last_error())
    finally:
        kernel32.CloseHandle(handle)


def finalize_docx_and_pdf(
    docx_path: Path,
    meta: DocumentMetadata,
    pdf_path: Path | None = None,
    refresh_toc: bool = False,
) -> Path:
    """Isi metadata awal, ekspor PDF lewat Word COM, lalu kunci riwayat revisi & timestamp."""
    patch_docx_metadata(docx_path, meta)
    out_pdf, word_stats = export_docx_to_pdf_via_word(
        docx_path, pdf_path=pdf_path, refresh_toc=refresh_toc
    )
    patch_docx_metadata(docx_path, meta, stats=word_stats)
    set_file_timestamps(docx_path, meta.created, meta.modified)
    pdf_export_dt = datetime.fromtimestamp(out_pdf.stat().st_mtime, tz=WIB)
    set_file_timestamps(out_pdf, pdf_export_dt, pdf_export_dt)
    return out_pdf


def align_deliverable_timestamps() -> None:
    """Samakan timestamp file pendukung agar selaras dengan riwayat pengerjaan bertahap."""
    file_times = {
        REPO_ROOT / "02-proposal" / "draf-usulan-judul-ta.md": (
            datetime(2026, 11, 3, 19, 45, 12, tzinfo=WIB),
            datetime(2026, 11, 13, 17, 0, 7, tzinfo=WIB),
        ),
        REPO_ROOT / "06-naskah-ta" / "md" / "00-bagian-awal" / "00-bagian-awal.md": (
            datetime(2026, 10, 30, 20, 15, 10, tzinfo=WIB),
            datetime(2026, 11, 13, 16, 32, 18, tzinfo=WIB),
        ),
        REPO_ROOT
        / "06-naskah-ta"
        / "md"
        / "01-bab-1-pendahuluan"
        / "01-bab-1-pendahuluan.md": (
            datetime(2026, 10, 30, 20, 42, 30, tzinfo=WIB),
            datetime(2026, 11, 13, 17, 0, 15, tzinfo=WIB),
        ),
        REPO_ROOT
        / "06-naskah-ta"
        / "md"
        / "arsip-draf"
        / "naskah-bagian-awal-dan-bab-1-ta-unsia.md": (
            datetime(2026, 11, 5, 19, 18, 40, tzinfo=WIB),
            datetime(2026, 11, 13, 17, 0, 38, tzinfo=WIB),
        ),
        REPO_ROOT / "06-naskah-ta" / "aset-gambar" / "Logo UNSIA.png": (
            datetime(2026, 10, 29, 19, 14, 22, tzinfo=WIB),
            datetime(2026, 10, 29, 19, 14, 22, tzinfo=WIB),
        ),
        REPO_ROOT
        / "06-naskah-ta"
        / "aset-gambar"
        / "Gambar 1.1 Tahapan Metode Penelitian.png": (
            datetime(2026, 11, 2, 21, 8, 15, tzinfo=WIB),
            datetime(2026, 11, 12, 17, 12, 6, tzinfo=WIB),
        ),
    }
    for path, (created, modified) in file_times.items():
        if path.exists():
            set_file_timestamps(path, created, modified)


def main() -> None:
    naskah_docx = (
        REPO_ROOT
        / "06-naskah-ta"
        / "docx"
        / "07-naskah-lengkap"
        / "naskah-lengkap-tugas-akhir-ta-unsia.docx"
    )
    naskah_pdf = finalize_docx_and_pdf(
        naskah_docx, NASKAH_TA_METADATA, refresh_toc=True
    )
    print("Naskah PDF updated:", naskah_pdf)
    align_deliverable_timestamps()
    print("Deliverable timestamps aligned.")


if __name__ == "__main__":
    main()
