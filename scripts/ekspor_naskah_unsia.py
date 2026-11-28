"""Eksporter naskah Tugas Akhir UNSIA ke DOCX/PDF dengan fitur asli Microsoft Word."""

from __future__ import annotations

import argparse
import json
import math
import re
import shutil
import subprocess
import sys
import tempfile
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from uuid import uuid4

import docx
from docx.enum.section import WD_SECTION
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.table import WD_ALIGN_VERTICAL, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
from docx.shared import Cm, Pt, RGBColor
from lxml import etree

try:
    from PIL import Image
except ImportError:
    Image = None

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from terapkan_metadata_dokumen import (
    REPO_ROOT,
    WIB,
    DocumentMetadata,
    patch_docx_metadata,
    set_file_timestamps,
)

MML2OMML_XSL_PATH = Path(r"C:\Program Files\Microsoft Office\root\Office16\MML2OMML.XSL")
MML_NS = "http://www.w3.org/1998/Math/MathML"
OMML_NS = "http://schemas.openxmlformats.org/officeDocument/2006/math"
W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"

PRINTABLE_WIDTH_CM = 14.0
PRINTABLE_WIDTH_DXA = 7938
COVER_LOGO_WIDTH_CM = 4.0
MAX_IMAGE_WIDTH_CM = 14.0
MAX_IMAGE_HEIGHT_CM = 12.2

IMG_LINE_RE = re.compile(r"^!\[(.*?)\]\((.+?)\)\s*$")
IMG_REF_TITLE_RE = re.compile(r'^<?(.+?)>?(?:\s+"[^"]*")?$')
GAMBAR_CAPTION_RE = re.compile(r"^Gambar\s+((?:\d+|L))\.(\d+)\s+(.+)$")
TABEL_CAPTION_RE = re.compile(r"^Tabel\s+((?:\d+|L))\.(\d+)\s+(.+)$")
PERSAMAAN_CAPTION_RE = re.compile(r"^(?:\*\*)?Persamaan\s+\(\d+\.\d+\)(?:\*\*)?")
BIB_ITEM_RE = re.compile(r"^(\[\d+\])\s+(.+)$")
LIST_ITEM_RE = re.compile(r"^(?:([a-z])\)|(\d+)\.|[-*]\s)\s*(.+)$")

BORDERLESS_META_SECTIONS = {
    "HALAMAN PERNYATAAN ORISINALITAS",
    "HALAMAN PENGESAHAN",
    "KATA PENGANTAR",
}
TOC_SECTIONS = {"DAFTAR ISI", "DAFTAR GAMBAR", "DAFTAR TABEL"}

_XSLT_CACHE: etree.XSLT | None = None


def _get_mml2omml_xslt() -> etree.XSLT:
    global _XSLT_CACHE
    if _XSLT_CACHE is None:
        if not MML2OMML_XSL_PATH.is_file():
            raise FileNotFoundError(
                f"Berkas XSLT Office tidak ditemukan: {MML2OMML_XSL_PATH}"
            )
        _XSLT_CACHE = etree.XSLT(etree.parse(str(MML2OMML_XSL_PATH)))
    return _XSLT_CACHE


# ---------------------------------------------------------------------------
# LaTeX -> MathML -> Word OMML converter
# ---------------------------------------------------------------------------

LATEX_TOKEN_RE = re.compile(
    r"""
    (\\[A-Za-z]+)
    | (\\[{}\\|])
    | (\s+)
    | ([0-9]+(?:\{,\}[0-9]+|,[0-9]+)?)
    | ([A-Za-z]+)
    | (.)
    """,
    re.VERBOSE,
)

LATEX_SYMBOLS = {
    r"\|": "\u2016",
    r"\{": "{",
    r"\}": "}",
    r"\mid": "|",
    r"\cdot": "\u00B7",
    r"\top": "\u22A4",
    r"\in": "\u2208",
    r"\le": "\u2264",
    r"\ge": "\u2265",
    r"\dots": "\u2026",
    r"\epsilon": "\u03B5",
    r"\quad": "\u2003",
    r"\qquad": "\u2003\u2003",
}

UPRIGHT_FUNCS = {r"\ln", r"\exp"}
NARY_OR_LIMIT_OPS = {r"\sum": "\u2211", r"\min": "min", r"\max": "max"}


def _mml(tag: str, text: str | None = None, **attrs: str) -> etree._Element:
    el = etree.Element(f"{{{MML_NS}}}{tag}", **attrs)
    if text is not None:
        el.text = text
    return el


def _wrap_mrow(nodes: list[etree._Element]) -> etree._Element:
    if len(nodes) == 1:
        return nodes[0]
    row = _mml("mrow")
    row.extend(nodes)
    return row


class _LatexMathMLParser:
    """Recursive-descent LaTeX math parser emitting Presentation MathML."""

    def __init__(self, tex: str) -> None:
        normalized = tex.strip().replace("{,}", ",")
        self.tokens: list[str] = []
        for m in LATEX_TOKEN_RE.finditer(normalized):
            tok = m.group(0)
            if tok.isspace():
                continue
            self.tokens.append(tok)
        self.pos = 0

    def peek(self, offset: int = 0) -> str | None:
        idx = self.pos + offset
        return self.tokens[idx] if 0 <= idx < len(self.tokens) else None

    def pop(self) -> str:
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    def parse(self) -> etree._Element:
        root = _mml("math")
        nodes = self._parse_seq(stop_tokens=set())
        root.extend(nodes)
        return root

    def _parse_seq(
        self, stop_tokens: set[str], stop_on_norm_close: bool = False
    ) -> list[etree._Element]:
        out: list[etree._Element] = []
        while (tok := self.peek()) is not None:
            if tok in stop_tokens:
                break
            if stop_on_norm_close and tok == r"\|":
                break
            out.append(self._parse_scripted())
        return out

    def _parse_group_nodes(self) -> list[etree._Element]:
        if self.peek() == "{":
            self.pop()
            nodes = self._parse_seq(stop_tokens={"}"})
            if self.peek() == "}":
                self.pop()
            return nodes
        return [self._parse_atom()]

    def _parse_group_as_node(self) -> etree._Element:
        return _wrap_mrow(self._parse_group_nodes())

    def _parse_scripted(self) -> etree._Element:
        base = self._parse_atom()
        sub: etree._Element | None = None
        sup: etree._Element | None = None
        while (nxt := self.peek()) in ("_", "^"):
            self.pop()
            arg = self._parse_group_as_node()
            if nxt == "_":
                sub = arg
            else:
                sup = arg

        if sub is None and sup is None:
            return base

        is_sum = base.tag == f"{{{MML_NS}}}mo" and base.text == "\u2211"
        is_lim_op = base.tag in {f"{{{MML_NS}}}mi", f"{{{MML_NS}}}mo"} and base.text in {
            "min",
            "max",
        }

        if is_sum and sub is not None and sup is not None:
            el = _mml("munderover")
            el.extend([base, sub, sup])
            return el
        if (is_sum or is_lim_op) and sub is not None and sup is None:
            el = _mml("munder")
            el.extend([base, sub])
            return el
        if sub is not None and sup is not None:
            el = _mml("msubsup")
            el.extend([base, sub, sup])
            return el
        if sub is not None:
            el = _mml("msub")
            el.extend([base, sub])
            return el
        el = _mml("msup")
        el.extend([base, sup])
        return el

    def _extract_brace_text(self) -> str:
        if self.peek() != "{":
            return self.pop() if self.peek() is not None else ""
        self.pop()
        parts: list[str] = []
        depth = 1
        while (tok := self.peek()) is not None:
            self.pop()
            if tok == "{":
                depth += 1
            elif tok == "}":
                depth -= 1
                if depth == 0:
                    break
            else:
                parts.append(tok)
        return "".join(parts)

    def _parse_atom(self) -> etree._Element:
        tok = self.pop()

        if tok == "{":
            nodes = self._parse_seq(stop_tokens={"}"})
            if self.peek() == "}":
                self.pop()
            return _wrap_mrow(nodes)

        if tok == r"\frac":
            num = self._parse_group_as_node()
            den = self._parse_group_as_node()
            el = _mml("mfrac")
            el.extend([num, den])
            return el

        if tok == r"\left":
            left_delim = self.pop() if self.peek() is not None else "("
            left_txt = LATEX_SYMBOLS.get(left_delim, left_delim)
            inner = self._parse_seq(stop_tokens={r"\right"})
            right_txt = ")"
            if self.peek() == r"\right":
                self.pop()
                rd = self.pop() if self.peek() is not None else ")"
                right_txt = LATEX_SYMBOLS.get(rd, rd)
            row = _mml("mrow")
            row.append(_mml("mo", left_txt))
            row.extend(inner)
            row.append(_mml("mo", right_txt))
            return row

        if tok == r"\|":
            inner = self._parse_seq(stop_tokens={"}", r"\right"}, stop_on_norm_close=True)
            if self.peek() == r"\|":
                self.pop()
                row = _mml("mrow")
                row.append(_mml("mo", "\u2016"))
                row.extend(inner)
                row.append(_mml("mo", "\u2016"))
                return row
            return _mml("mo", "\u2016")

        if tok == r"\mathbf":
            inner_nodes = self._parse_group_nodes()
            for node in inner_nodes:
                if node.tag == f"{{{MML_NS}}}mi":
                    node.set("mathvariant", "bold")
            return _wrap_mrow(inner_nodes)

        if tok in (r"\mathrm", r"\text"):
            txt = self._extract_brace_text()
            return _mml("mi", txt, mathvariant="normal")

        if tok in UPRIGHT_FUNCS:
            return _mml("mi", tok[1:], mathvariant="normal")

        if tok in NARY_OR_LIMIT_OPS:
            if tok == r"\sum":
                return _mml("mo", "\u2211")
            return _mml("mi", tok[1:], mathvariant="normal")

        if tok in LATEX_SYMBOLS:
            ch = LATEX_SYMBOLS[tok]
            if tok == r"\top":
                return _mml("mi", ch, mathvariant="normal")
            if tok == r"\epsilon":
                return _mml("mi", ch)
            if tok in (r"\quad", r"\qquad"):
                return _mml("mtext", ch)
            return _mml("mo", ch)

        if tok[0].isdigit():
            return _mml("mn", tok)

        if tok.isalpha():
            return _mml("mi", tok)

        return _mml("mo", tok)


def _style_omml_runs(omath_el: etree._Element, size_pt: int) -> None:
    sz_val = str(size_pt * 2)
    for nary_pr in omath_el.findall(f".//{{{OMML_NS}}}naryPr"):
        if nary_pr.find(f"{{{OMML_NS}}}limLoc") is None:
            lim = etree.Element(f"{{{OMML_NS}}}limLoc")
            lim.set(f"{{{OMML_NS}}}val", "undOvr")
            chr_el = nary_pr.find(f"{{{OMML_NS}}}chr")
            if chr_el is not None:
                chr_el.addnext(lim)
            else:
                nary_pr.insert(0, lim)

    for r_el in omath_el.findall(f".//{{{OMML_NS}}}r"):
        w_rpr = r_el.find(f"{{{W_NS}}}rPr")
        if w_rpr is None:
            w_rpr = etree.Element(f"{{{W_NS}}}rPr")
            m_rpr = r_el.find(f"{{{OMML_NS}}}rPr")
            if m_rpr is not None:
                m_rpr.addnext(w_rpr)
            else:
                r_el.insert(0, w_rpr)
        for old in list(w_rpr):
            if old.tag in {f"{{{W_NS}}}rFonts", f"{{{W_NS}}}sz", f"{{{W_NS}}}szCs"}:
                w_rpr.remove(old)
        rfonts = etree.SubElement(w_rpr, f"{{{W_NS}}}rFonts")
        for attr in ("ascii", "hAnsi", "cs"):
            rfonts.set(f"{{{W_NS}}}{attr}", "Cambria Math")
        sz = etree.SubElement(w_rpr, f"{{{W_NS}}}sz")
        sz.set(f"{{{W_NS}}}val", sz_val)
        sz_cs = etree.SubElement(w_rpr, f"{{{W_NS}}}szCs")
        sz_cs.set(f"{{{W_NS}}}val", sz_val)


def latex_to_omml(tex: str, font_size: int = 12, display: bool = False) -> etree._Element:
    """Convert a LaTeX math expression into an Office Math (OMML) XML element."""
    mml_root = _LatexMathMLParser(tex).parse()
    transformed = _get_mml2omml_xslt()(mml_root)
    omath = transformed.getroot()
    if omath is None or not omath.tag.endswith("}oMath"):
        raise ValueError(f"Konversi MML2OMML tidak menghasilkan <m:oMath> untuk: {tex}")
    _style_omml_runs(omath, font_size)
    if display:
        para = etree.Element(f"{{{OMML_NS}}}oMathPara")
        para_pr = etree.SubElement(para, f"{{{OMML_NS}}}oMathParaPr")
        jc = etree.SubElement(para_pr, f"{{{OMML_NS}}}jc")
        jc.set(f"{{{OMML_NS}}}val", "center")
        para.append(omath)
        return para
    return omath


def _append_omml_inline(
    p: docx.text.paragraph.Paragraph, tex: str, font_size: int = 12
) -> None:
    omml_el = latex_to_omml(tex, font_size=font_size, display=False)
    p._p.append(omml_el)


# ---------------------------------------------------------------------------
# Recursive inline Markdown + inline math parser
# ---------------------------------------------------------------------------


def _style_run(
    run: docx.text.run.Run,
    font_size: int,
    bold: bool | None,
    italic: bool | None,
    lang: str | None = None,
) -> None:
    if bold is not None:
        run.bold = bold
    if italic is not None:
        run.italic = italic
    run.font.name = "Times New Roman"
    run.font.size = Pt(font_size)
    run.font.color.rgb = RGBColor(0, 0, 0)
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.insert(0, rfonts)
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rfonts.set(qn(attr), "Times New Roman")
    if lang:
        lang_el = rpr.find(qn("w:lang"))
        if lang_el is None:
            lang_el = OxmlElement("w:lang")
            rpr.append(lang_el)
        lang_el.set(qn("w:val"), lang)


def _find_closing_delim(text: str, start: int, delim: str) -> int:
    pos = start
    while True:
        idx = text.find(delim, pos)
        if idx == -1:
            return -1
        if idx > 0 and text[idx - 1] == "\\":
            pos = idx + len(delim)
            continue
        if delim == "*" and text[idx : idx + 2] == "**":
            pos = idx + 2
            continue
        return idx


def _emit_inline_nodes(
    p: docx.text.paragraph.Paragraph,
    text: str,
    font_size: int,
    bold: bool | None,
    italic: bool | None,
    lang: str | None,
) -> None:
    i = 0
    n = len(text)
    buf: list[str] = []

    def flush() -> None:
        if buf:
            run = p.add_run("".join(buf))
            _style_run(run, font_size, bold, italic, lang=lang)
            buf.clear()

    while i < n:
        ch = text[i]

        if ch == "\\" and i + 1 < n and text[i + 1] in ("*", "`", "$", "|", "[", "]"):
            buf.append(text[i + 1])
            i += 2
            continue

        if ch == "$":
            end = text.find("$", i + 1)
            if end != -1 and "\n" not in text[i + 1 : end]:
                flush()
                _append_omml_inline(p, text[i + 1 : end], font_size=font_size)
                i = end + 1
                continue

        if text.startswith("***", i):
            end = _find_closing_delim(text, i + 3, "***")
            if end != -1:
                flush()
                _emit_inline_nodes(p, text[i + 3 : end], font_size, True, True, lang)
                i = end + 3
                continue

        if text.startswith("**", i):
            end = _find_closing_delim(text, i + 2, "**")
            if end != -1:
                flush()
                _emit_inline_nodes(p, text[i + 2 : end], font_size, True, italic, lang)
                i = end + 2
                continue

        if ch == "`":
            end = text.find("`", i + 1)
            if end != -1:
                flush()
                run = p.add_run(text[i + 1 : end])
                _style_run(run, font_size, bold, italic, lang=lang)
                i = end + 1
                continue

        if ch == "*":
            end = _find_closing_delim(text, i + 1, "*")
            if end != -1:
                flush()
                _emit_inline_nodes(p, text[i + 1 : end], font_size, bold, True, lang)
                i = end + 1
                continue

        if ch == "[":
            close_br = text.find("]", i + 1)
            if close_br != -1 and close_br + 1 < n and text[close_br + 1] == "(":
                close_par = text.find(")", close_br + 2)
                if close_par != -1:
                    flush()
                    _emit_inline_nodes(
                        p, text[i + 1 : close_br], font_size, bold, italic, lang
                    )
                    i = close_par + 1
                    continue

        buf.append(ch)
        i += 1

    flush()


def add_formatted_runs(
    p: docx.text.paragraph.Paragraph,
    text: str,
    font_size: int = 12,
    bold_default: bool | None = False,
    italic_default: bool | None = False,
    lang: str | None = None,
) -> None:
    _emit_inline_nodes(p, text, font_size, bold_default, italic_default, lang)


def strip_markdown_plain(text: str) -> str:
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    s = s.replace(r"\|", "|").replace("***", "").replace("**", "").replace("`", "")
    s = s.replace("*", "").replace("$", "")
    return s.strip()


# ---------------------------------------------------------------------------
# Document configuration, native numbering, fields, captions, sections
# ---------------------------------------------------------------------------


def _set_unsia_margins(section: docx.section.Section) -> None:
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(3.0)
    section.bottom_margin = Cm(3.0)
    section.left_margin = Cm(4.0)
    section.right_margin = Cm(3.0)


def _set_style_font(
    style,
    size_pt: int = 12,
    bold: bool | None = False,
    italic: bool | None = False,
    lang: str | None = "id-ID",
) -> None:
    style.font.name = "Times New Roman"
    style.font.size = Pt(size_pt)
    if bold is not None:
        style.font.bold = bold
    if italic is not None:
        style.font.italic = italic
    style.font.color.rgb = RGBColor(0, 0, 0)
    rpr = style._element.get_or_add_rPr()
    for tag in ("w:rFonts", "w:lang"):
        for old in rpr.findall(qn(tag)):
            rpr.remove(old)
    rfonts = OxmlElement("w:rFonts")
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rfonts.set(qn(attr), "Times New Roman")
    rpr.append(rfonts)
    if lang:
        lang_el = OxmlElement("w:lang")
        lang_el.set(qn("w:val"), lang)
        lang_el.set(qn("w:eastAsia"), "en-US")
        rpr.append(lang_el)


def _get_or_add_paragraph_style(
    doc: docx.Document, name: str, base_style: str | None = "Normal"
):
    try:
        return doc.styles[name]
    except KeyError:
        st = doc.styles.add_style(name, WD_STYLE_TYPE.PARAGRAPH)
        if base_style and base_style in doc.styles:
            st.base_style = doc.styles[base_style]
        return st


def _configure_settings_xml(doc: docx.Document) -> None:
    settings = doc.settings.element
    if settings.find(qn("w:updateFields")) is None:
        upd = OxmlElement("w:updateFields")
        upd.set(qn("w:val"), "true")
        settings.append(upd)

    compat = settings.find(qn("w:compat"))
    if compat is None:
        compat = OxmlElement("w:compat")
        settings.append(compat)
    has_compat_mode = False
    for child in compat.findall(qn("w:compatSetting")):
        if child.get(qn("w:name")) == "compatibilityMode":
            child.set(qn("w:val"), "15")
            has_compat_mode = True
    if not has_compat_mode:
        cs = OxmlElement("w:compatSetting")
        cs.set(qn("w:name"), "compatibilityMode")
        cs.set(qn("w:uri"), "http://schemas.microsoft.com/office/word")
        cs.set(qn("w:val"), "15")
        compat.append(cs)


def _set_doc_defaults_language(doc: docx.Document, lang: str = "id-ID") -> None:
    styles_el = doc.styles.element
    doc_defaults = styles_el.find(qn("w:docDefaults"))
    if doc_defaults is None:
        return
    rpr_def = doc_defaults.find(qn("w:rPrDefault"))
    if rpr_def is None:
        rpr_def = OxmlElement("w:rPrDefault")
        doc_defaults.insert(0, rpr_def)
    rpr = rpr_def.find(qn("w:rPr"))
    if rpr is None:
        rpr = OxmlElement("w:rPr")
        rpr_def.append(rpr)
    for tag in ("w:rFonts", "w:sz", "w:szCs", "w:lang"):
        for old in rpr.findall(qn(tag)):
            rpr.remove(old)
    rfonts = OxmlElement("w:rFonts")
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rfonts.set(qn(attr), "Times New Roman")
    rpr.append(rfonts)
    for sz_tag in ("w:sz", "w:szCs"):
        sz = OxmlElement(sz_tag)
        sz.set(qn("w:val"), "24")
        rpr.append(sz)
    lang_el = OxmlElement("w:lang")
    lang_el.set(qn("w:val"), lang)
    lang_el.set(qn("w:eastAsia"), "en-US")
    rpr.append(lang_el)


def _setup_native_numbering(doc: docx.Document) -> dict[str, int]:
    """Ensure numbering.xml exists and register native lowerLetter, decimal, bullet specs."""
    tmp = doc.add_paragraph(style="List Number")
    tmp._element.getparent().remove(tmp._element)

    numbering_root = doc.part.numbering_part.numbering_definitions._numbering
    existing_abs = [
        int(el.get(qn("w:abstractNumId")))
        for el in numbering_root.findall(qn("w:abstractNum"))
        if el.get(qn("w:abstractNumId")) is not None
    ]
    next_abs_id = (max(existing_abs) + 1) if existing_abs else 100

    specs = (
        ("lowerLetter", "lowerLetter", "%1)", "Times New Roman"),
        ("decimal", "decimal", "%1.", "Times New Roman"),
        ("bullet", "bullet", "\u2022", "Symbol"),
    )
    abstract_ids: dict[str, int] = {}
    first_num = numbering_root.find(qn("w:num"))

    for kind, num_fmt, lvl_text, font_name in specs:
        abs_id = next_abs_id
        next_abs_id += 1
        abstract_ids[kind] = abs_id
        abs_xml = parse_xml(
            f'<w:abstractNum {nsdecls("w")} w:abstractNumId="{abs_id}">'
            '  <w:multiLevelType w:val="singleLevel"/>'
            '  <w:lvl w:ilvl="0">'
            '    <w:start w:val="1"/>'
            f'    <w:numFmt w:val="{num_fmt}"/>'
            f'    <w:lvlText w:val="{lvl_text}"/>'
            '    <w:lvlJc w:val="left"/>'
            '    <w:pPr><w:ind w:left="425" w:hanging="312"/></w:pPr>'
            '    <w:rPr>'
            f'      <w:rFonts w:ascii="{font_name}" w:hAnsi="{font_name}" w:cs="Times New Roman"/>'
            '      <w:color w:val="000000"/>'
            '      <w:sz w:val="24"/>'
            '      <w:szCs w:val="24"/>'
            '    </w:rPr>'
            '  </w:lvl>'
            '</w:abstractNum>'
        )
        if first_num is not None:
            first_num.addprevious(abs_xml)
        else:
            numbering_root.append(abs_xml)

    return abstract_ids


def _allocate_list_num_id(doc: docx.Document, abstract_id: int) -> int:
    numbering_root = doc.part.numbering_part.numbering_definitions._numbering
    existing_nums = [
        int(el.get(qn("w:numId")))
        for el in numbering_root.findall(qn("w:num"))
        if el.get(qn("w:numId")) is not None
    ]
    new_id = (max(existing_nums) + 1) if existing_nums else 1
    num_xml = parse_xml(
        f'<w:num {nsdecls("w")} w:numId="{new_id}">'
        f'  <w:abstractNumId w:val="{abstract_id}"/>'
        '  <w:lvlOverride w:ilvl="0"><w:startOverride w:val="1"/></w:lvlOverride>'
        '</w:num>'
    )
    numbering_root.append(num_xml)
    return new_id


def _attach_num_pr(p: docx.text.paragraph.Paragraph, num_id: int, ilvl: int = 0) -> None:
    ppr = p._p.get_or_add_pPr()
    for old in ppr.findall(qn("w:numPr")):
        ppr.remove(old)
    num_pr = OxmlElement("w:numPr")
    ilvl_el = OxmlElement("w:ilvl")
    ilvl_el.set(qn("w:val"), str(ilvl))
    num_id_el = OxmlElement("w:numId")
    num_id_el.set(qn("w:val"), str(num_id))
    num_pr.append(ilvl_el)
    num_pr.append(num_id_el)
    ppr.append(num_pr)


def configure_unsia_document(doc: docx.Document) -> dict[str, int]:
    for section in doc.sections:
        _set_unsia_margins(section)

    _configure_settings_xml(doc)
    _set_doc_defaults_language(doc, "id-ID")

    normal = doc.styles["Normal"]
    _set_style_font(normal, size_pt=12, bold=False, italic=False, lang="id-ID")
    normal.paragraph_format.line_spacing = 1.5
    normal.paragraph_format.space_before = Pt(0)
    normal.paragraph_format.space_after = Pt(0)
    normal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    normal.paragraph_format.widow_control = True

    for lvl, align, sb, sa in (
        ("Heading 1", WD_ALIGN_PARAGRAPH.CENTER, 0, 12),
        ("Heading 2", WD_ALIGN_PARAGRAPH.LEFT, 12, 6),
        ("Heading 3", WD_ALIGN_PARAGRAPH.LEFT, 8, 4),
    ):
        st = _get_or_add_paragraph_style(doc, lvl, base_style="Normal")
        _set_style_font(st, size_pt=12, bold=True, italic=False, lang="id-ID")
        st.paragraph_format.alignment = align
        st.paragraph_format.line_spacing = 1.5
        st.paragraph_format.first_line_indent = Cm(0)
        st.paragraph_format.left_indent = Cm(0)
        st.paragraph_format.space_before = Pt(sb)
        st.paragraph_format.space_after = Pt(sa)
        st.paragraph_format.keep_with_next = True
        st.paragraph_format.widow_control = True

    fig_cap = _get_or_add_paragraph_style(doc, "Caption", base_style="Normal")
    _set_style_font(fig_cap, size_pt=12, bold=True, italic=False, lang="id-ID")
    fig_cap.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    fig_cap.paragraph_format.line_spacing = 1.15
    fig_cap.paragraph_format.first_line_indent = Cm(0)
    fig_cap.paragraph_format.space_before = Pt(4)
    fig_cap.paragraph_format.space_after = Pt(8)
    fig_cap.paragraph_format.keep_with_next = False
    fig_cap.paragraph_format.widow_control = True

    tbl_cap = _get_or_add_paragraph_style(doc, "Caption Tabel", base_style="Normal")
    _set_style_font(tbl_cap, size_pt=12, bold=False, italic=False, lang="id-ID")
    tbl_cap.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    tbl_cap.paragraph_format.line_spacing = 1.15
    tbl_cap.paragraph_format.first_line_indent = Cm(0)
    tbl_cap.paragraph_format.space_before = Pt(8)
    tbl_cap.paragraph_format.space_after = Pt(4)
    tbl_cap.paragraph_format.keep_with_next = True
    tbl_cap.paragraph_format.widow_control = True

    for toc_name, indent_cm in (
        ("TOC 1", 0.0),
        ("TOC 2", 0.75),
        ("TOC 3", 1.5),
        ("Table of Figures", 0.0),
    ):
        tst = _get_or_add_paragraph_style(doc, toc_name, base_style="Normal")
        _set_style_font(tst, size_pt=12, bold=False, italic=False, lang="id-ID")
        tst.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
        tst.paragraph_format.line_spacing = 1.5
        tst.paragraph_format.left_indent = Cm(indent_cm)
        tst.paragraph_format.right_indent = Cm(1.35)
        tst.paragraph_format.first_line_indent = Cm(0)
        tst.paragraph_format.space_before = Pt(0)
        tst.paragraph_format.space_after = Pt(2)
        tst.paragraph_format.widow_control = True
        tst.paragraph_format.tab_stops.clear_all()
        tst.paragraph_format.tab_stops.add_tab_stop(
            Cm(PRINTABLE_WIDTH_CM), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS
        )

    return _setup_native_numbering(doc)


def _set_page_number_format(
    section: docx.section.Section, fmt: str, start: int | None = None
) -> None:
    sect_pr = section._sectPr
    for existing in sect_pr.findall(qn("w:pgNumType")):
        sect_pr.remove(existing)
    pg_num = OxmlElement("w:pgNumType")
    pg_num.set(qn("w:fmt"), fmt)
    if start is not None:
        pg_num.set(qn("w:start"), str(start))
    sect_pr.append(pg_num)


def _add_page_number_footer(
    footer: docx.section._Footer, alignment: WD_ALIGN_PARAGRAPH
) -> None:
    footer.is_linked_to_previous = False
    p = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
    p.text = ""
    p.alignment = alignment
    p.paragraph_format.first_line_indent = Cm(0)
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)

    def _make_rpr() -> OxmlElement:
        rpr = OxmlElement("w:rPr")
        rfonts = OxmlElement("w:rFonts")
        for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
            rfonts.set(qn(attr), "Times New Roman")
        rpr.append(rfonts)
        for sz_tag in ("w:sz", "w:szCs"):
            sz = OxmlElement(sz_tag)
            sz.set(qn("w:val"), "24")
            rpr.append(sz)
        color = OxmlElement("w:color")
        color.set(qn("w:val"), "000000")
        rpr.append(color)
        return rpr

    for kind in ("begin", "instr", "separate", "end"):
        r = OxmlElement("w:r")
        r.append(_make_rpr())
        if kind == "instr":
            instr = OxmlElement("w:instrText")
            instr.set(qn("xml:space"), "preserve")
            instr.text = " PAGE "
            r.append(instr)
        else:
            fld = OxmlElement("w:fldChar")
            fld.set(qn("w:fldCharType"), kind)
            r.append(fld)
        p._p.append(r)


def _append_complex_field(
    p: docx.text.paragraph.Paragraph,
    instr_text: str,
    cached_text: str,
    font_size: int = 12,
    bold: bool | None = None,
) -> None:
    def _make_r(text: str | None = None, fld_type: str | None = None) -> None:
        r = OxmlElement("w:r")
        rpr = OxmlElement("w:rPr")
        rfonts = OxmlElement("w:rFonts")
        for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
            rfonts.set(qn(attr), "Times New Roman")
        rpr.append(rfonts)
        if bold is True:
            rpr.append(OxmlElement("w:b"))
        for sz_tag in ("w:sz", "w:szCs"):
            sz = OxmlElement(sz_tag)
            sz.set(qn("w:val"), str(font_size * 2))
            rpr.append(sz)
        color = OxmlElement("w:color")
        color.set(qn("w:val"), "000000")
        rpr.append(color)
        r.append(rpr)
        if fld_type is not None:
            fc = OxmlElement("w:fldChar")
            fc.set(qn("w:fldCharType"), fld_type)
            r.append(fc)
        elif text is not None:
            el = OxmlElement("w:instrText")
            el.set(qn("xml:space"), "preserve")
            el.text = text
            r.append(el)
        p._p.append(r)

    _make_r(fld_type="begin")
    _make_r(text=f" {instr_text.strip()} ")
    _make_r(fld_type="separate")
    run = p.add_run(cached_text)
    _style_run(run, font_size, bold, False)
    _make_r(fld_type="end")


def _add_tc_field(
    p: docx.text.paragraph.Paragraph, label: str, flag: str, level: str = "1"
) -> None:
    clean = label.replace('"', "'").strip()

    def _rpr() -> OxmlElement:
        rpr = OxmlElement("w:rPr")
        rfonts = OxmlElement("w:rFonts")
        for attr in ("w:ascii", "w:hAnsi", "w:cs"):
            rfonts.set(qn(attr), "Times New Roman")
        rpr.append(rfonts)
        return rpr

    for kind, text in (
        ("begin", None),
        ("instr", f' TC "{clean}" \\f {flag} \\l {level} '),
        ("end", None),
    ):
        r = OxmlElement("w:r")
        r.append(_rpr())
        if text is not None:
            instr = OxmlElement("w:instrText")
            instr.set(qn("xml:space"), "preserve")
            instr.text = text
            r.append(instr)
        else:
            fc = OxmlElement("w:fldChar")
            fc.set(qn("w:fldCharType"), kind)
            r.append(fc)
        p._p.append(r)


def _add_toc_field(doc: docx.Document, instr_text: str) -> None:
    sdt = parse_xml(
        f'<w:sdt {nsdecls("w")}>'
        '  <w:sdtPr>'
        '    <w:docPartObj>'
        '      <w:docPartGallery w:val="Table of Contents"/>'
        '      <w:docPartUnique/>'
        '    </w:docPartObj>'
        '  </w:sdtPr>'
        '  <w:sdtContent>'
        '    <w:p>'
        '      <w:pPr>'
        '        <w:ind w:firstLine="0"/>'
        '        <w:tabs><w:tab w:val="right" w:leader="dot" w:pos="7938"/></w:tabs>'
        '      </w:pPr>'
        '      <w:r><w:fldChar w:fldCharType="begin" w:dirty="true"/></w:r>'
        f'      <w:r><w:instrText xml:space="preserve"> {instr_text} </w:instrText></w:r>'
        '      <w:r><w:fldChar w:fldCharType="separate"/></w:r>'
        '      <w:r>'
        '        <w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="24"/></w:rPr>'
        '        <w:t>Klik kanan lalu pilih Update Field untuk memperbarui daftar.</w:t>'
        '      </w:r>'
        '      <w:r><w:fldChar w:fldCharType="end"/></w:r>'
        '    </w:p>'
        '  </w:sdtContent>'
        '</w:sdt>'
    )
    body = doc._body._body
    sect_pr = body.find(qn("w:sectPr"))
    if sect_pr is not None:
        sect_pr.addprevious(sdt)
    else:
        body.append(sdt)


def _add_seq_caption(
    doc: docx.Document,
    seq_name: str,
    label_word: str,
    prefix: str,
    num: str,
    title_md: str,
    style_name: str,
    inherit_style_bold: bool,
    ensure_trailing_dot: bool,
) -> docx.text.paragraph.Paragraph:
    p = doc.add_paragraph(style=style_name)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.first_line_indent = Cm(0)
    p.paragraph_format.widow_control = True

    bold_val: bool | None = None if inherit_style_bold else False
    lead_run = p.add_run(f"{label_word} {prefix}.")
    _style_run(lead_run, 12, bold_val, False)

    reset_flag = " \\r 1" if int(num) == 1 else ""
    _append_complex_field(
        p,
        f"SEQ {seq_name}{reset_flag} \\* ARABIC",
        num,
        font_size=12,
        bold=bold_val,
    )

    sp_run = p.add_run(" ")
    _style_run(sp_run, 12, bold_val, False)

    clean_title = title_md.strip()
    if ensure_trailing_dot and not clean_title.endswith("."):
        clean_title += "."
    elif not ensure_trailing_dot:
        clean_title = clean_title.rstrip(".")

    add_formatted_runs(
        p,
        clean_title,
        font_size=12,
        bold_default=bold_val,
        italic_default=False,
    )
    return p


def _add_centered_label(
    doc: docx.Document,
    text: str,
    bold_default: bool,
    space_before: int,
    space_after: int,
    keep_with_next: bool = False,
) -> docx.text.paragraph.Paragraph:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.first_line_indent = Cm(0)
    p.paragraph_format.keep_with_next = keep_with_next
    p.paragraph_format.widow_control = True
    add_formatted_runs(p, text, font_size=12, bold_default=bold_default)
    return p


def _strip_outer_bold_caption(text: str) -> str:
    s = text.strip()
    if s.startswith("**") and s.endswith("**") and len(s) > 4:
        return s[2:-2].strip()
    return s


def _has_following_gambar_caption(lines: list[str], next_idx: int) -> bool:
    j = next_idx
    while j < len(lines):
        nxt = lines[j].strip()
        if not nxt or nxt == "---":
            j += 1
            continue
        return bool(GAMBAR_CAPTION_RE.match(_strip_outer_bold_caption(nxt)))
    return False


def _resolve_image_path(img_ref: str, md_dir: Path) -> Path | None:
    m = IMG_REF_TITLE_RE.match(img_ref.strip())
    clean_ref = m.group(1).strip() if m else img_ref.strip()
    for candidate in (md_dir / clean_ref, Path(clean_ref)):
        resolved = candidate.resolve()
        if resolved.is_file():
            return resolved
    return None


def _compute_fit_size_cm(
    img_path: Path,
    max_width_cm: float = MAX_IMAGE_WIDTH_CM,
    max_height_cm: float | None = MAX_IMAGE_HEIGHT_CM,
) -> float:
    if Image is None:
        return max_width_cm
    try:
        with Image.open(img_path) as im:
            px_w, px_h = im.size
            dpi_raw = im.info.get("dpi", (96, 96))
    except OSError:
        return max_width_cm

    if isinstance(dpi_raw, (tuple, list)) and dpi_raw and dpi_raw[0] > 0:
        dpi_x = float(dpi_raw[0])
        dpi_y = float(dpi_raw[1]) if len(dpi_raw) > 1 and dpi_raw[1] > 0 else dpi_x
    elif isinstance(dpi_raw, (int, float)) and dpi_raw > 0:
        dpi_x = dpi_y = float(dpi_raw)
    else:
        dpi_x = dpi_y = 96.0

    nat_w = (px_w / dpi_x) * 2.54
    nat_h = (px_h / dpi_y) * 2.54
    width_cm = min(nat_w, max_width_cm) if nat_w > 0 else max_width_cm
    if max_height_cm and nat_w > 0 and nat_h > 0:
        proj_h = width_cm * (nat_h / nat_w)
        if proj_h > max_height_cm:
            width_cm = max_height_cm * (nat_w / nat_h)
    return round(width_cm, 2)


def _add_image_block(
    doc: docx.Document,
    img_match: re.Match[str],
    md_dir: Path,
    has_explicit_caption: bool,
    max_width_cm: float = MAX_IMAGE_WIDTH_CM,
    max_height_cm: float | None = MAX_IMAGE_HEIGHT_CM,
    suppress_caption: bool = False,
    space_before: int = 8,
    space_after: int = 2,
) -> None:
    alt_text = img_match.group(1).strip()
    img_ref = img_match.group(2).strip()
    resolved = _resolve_image_path(img_ref, md_dir)
    if resolved is None:
        _add_centered_label(doc, f"[Gambar tidak ditemukan: {img_ref}]", False, 8, 8)
        return

    img_p = doc.add_paragraph()
    img_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    img_p.paragraph_format.space_before = Pt(space_before)
    img_p.paragraph_format.space_after = Pt(space_after)
    img_p.paragraph_format.first_line_indent = Cm(0)
    img_p.paragraph_format.keep_with_next = (not suppress_caption) and (
        has_explicit_caption or bool(alt_text)
    )

    width_cm = _compute_fit_size_cm(
        resolved, max_width_cm=max_width_cm, max_height_cm=max_height_cm
    )
    run = img_p.add_run()
    run.add_picture(str(resolved), width=Cm(width_cm))

    if not suppress_caption and not has_explicit_caption and alt_text:
        m = GAMBAR_CAPTION_RE.match(alt_text)
        if m:
            _add_seq_caption(
                doc,
                "Gambar",
                "Gambar",
                m.group(1),
                m.group(2),
                m.group(3),
                "Caption",
                inherit_style_bold=True,
                ensure_trailing_dot=True,
            )


# ---------------------------------------------------------------------------
# Display equations + Table helpers
# ---------------------------------------------------------------------------


def _set_table_fixed_grid(tbl: docx.table.Table, widths_cm: list[float]) -> None:
    tbl.autofit = False
    tbl_pr = tbl._tbl.tblPr
    for tag in ("w:tblW", "w:tblLayout"):
        for old in tbl_pr.findall(qn(tag)):
            tbl_pr.remove(old)

    dxa_widths = [max(180, round(w * 567)) for w in widths_cm]
    total_dxa = sum(dxa_widths)
    tbl_w = OxmlElement("w:tblW")
    tbl_w.set(qn("w:w"), str(total_dxa))
    tbl_w.set(qn("w:type"), "dxa")
    tbl_pr.append(tbl_w)

    layout = OxmlElement("w:tblLayout")
    layout.set(qn("w:type"), "fixed")
    tbl_pr.append(layout)

    old_grid = tbl._tbl.find(qn("w:tblGrid"))
    if old_grid is not None:
        tbl._tbl.remove(old_grid)
    tbl_grid = OxmlElement("w:tblGrid")
    for w_dxa in dxa_widths:
        gc = OxmlElement("w:gridCol")
        gc.set(qn("w:w"), str(w_dxa))
        tbl_grid.append(gc)
    tbl_pr.addnext(tbl_grid)

    for row in tbl.rows:
        for idx, w_dxa in enumerate(dxa_widths):
            if idx < len(row.cells):
                tc_pr = row.cells[idx]._tc.get_or_add_tcPr()
                for old in tc_pr.findall(qn("w:tcW")):
                    tc_pr.remove(old)
                tc_w = OxmlElement("w:tcW")
                tc_w.set(qn("w:w"), str(w_dxa))
                tc_w.set(qn("w:type"), "dxa")
                tc_pr.append(tc_w)


def _set_row_props(
    row: docx.table._Row, cant_split: bool = True, is_header: bool = False
) -> None:
    tr_pr = row._tr.get_or_add_trPr()
    for tag in ("w:cantSplit", "w:tblHeader"):
        for old in tr_pr.findall(qn(tag)):
            tr_pr.remove(old)
    if cant_split:
        tr_pr.append(OxmlElement("w:cantSplit"))
    if is_header:
        tr_pr.append(OxmlElement("w:tblHeader"))


def _set_cell_margins(
    cell: docx.table._Cell, top: int = 45, bottom: int = 45, left: int = 65, right: int = 65
) -> None:
    tc_pr = cell._tc.get_or_add_tcPr()
    for existing in tc_pr.findall(qn("w:tcMar")):
        tc_pr.remove(existing)
    mar = OxmlElement("w:tcMar")
    for side, val in (("top", top), ("bottom", bottom), ("left", left), ("right", right)):
        node = OxmlElement(f"w:{side}")
        node.set(qn("w:w"), str(val))
        node.set(qn("w:type"), "dxa")
        mar.append(node)
    tc_pr.append(mar)


def _set_cell_shading(cell: docx.table._Cell, fill_hex: str) -> None:
    tc_pr = cell._tc.get_or_add_tcPr()
    for existing in tc_pr.findall(qn("w:shd")):
        tc_pr.remove(existing)
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill_hex)
    tc_pr.append(shd)


def _set_cell_border_edges(cell: docx.table._Cell, **edges: tuple[str, str, str]) -> None:
    tc_pr = cell._tc.get_or_add_tcPr()
    for existing in tc_pr.findall(qn("w:tcBorders")):
        tc_pr.remove(existing)
    tc_borders = OxmlElement("w:tcBorders")
    for edge in ("top", "left", "bottom", "right"):
        b = OxmlElement(f"w:{edge}")
        if edge in edges:
            val, sz, color = edges[edge]
            b.set(qn("w:val"), val)
            b.set(qn("w:sz"), sz)
            b.set(qn("w:space"), "0")
            b.set(qn("w:color"), color)
        else:
            b.set(qn("w:val"), "none")
        tc_borders.append(b)
    tc_pr.append(tc_borders)


def _clear_table_borders(tbl: docx.table.Table) -> None:
    tbl_pr = tbl._tbl.tblPr
    for existing in tbl_pr.findall(qn("w:tblBorders")):
        tbl_pr.remove(existing)
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        b = OxmlElement(f"w:{edge}")
        b.set(qn("w:val"), "none")
        borders.append(b)
    tbl_pr.append(borders)


def _set_academic_table_borders(
    tbl: docx.table.Table,
    row_fills: list[str | None] | None = None,
    summary_rows: set[int] | None = None,
    pair_bottom_rows: set[int] | None = None,
    cols: int = 0,
) -> None:
    _clear_table_borders(tbl)
    heavy = ("single", "8", "000000")
    med_rule = ("single", "6", "475569")
    row_rule = ("single", "4", "B8C2CC")
    col_rule = ("single", "4", "CBD5E1")
    hdr_col_rule = ("single", "4", "94A3B8")
    last_row = len(tbl.rows) - 1
    num_cols = cols or (len(tbl.rows[0].cells) if tbl.rows else 0)
    lr_pad = 55 if num_cols >= 7 else 75

    for r_idx, row in enumerate(tbl.rows):
        _set_row_props(row, cant_split=True, is_header=(r_idx == 0))
        fill_hex = row_fills[r_idx] if row_fills and r_idx < len(row_fills) else None
        for c_idx, cell in enumerate(row.cells):
            cell_edges: dict[str, tuple[str, str, str]] = {}
            if r_idx == 0:
                cell_edges["top"] = heavy
                cell_edges["bottom"] = heavy
                if 0 < c_idx < num_cols:
                    cell_edges["left"] = hdr_col_rule
                if c_idx < num_cols - 1:
                    cell_edges["right"] = hdr_col_rule
                _set_cell_shading(cell, "EAEFF5")
            else:
                if summary_rows and r_idx in summary_rows:
                    cell_edges["top"] = ("single", "6", "000000")
                elif pair_bottom_rows and (r_idx - 1) in pair_bottom_rows:
                    cell_edges["top"] = med_rule
                else:
                    cell_edges["top"] = row_rule

                if r_idx == last_row:
                    cell_edges["bottom"] = heavy
                elif pair_bottom_rows and r_idx in pair_bottom_rows:
                    cell_edges["bottom"] = med_rule
                else:
                    cell_edges["bottom"] = row_rule

                if c_idx > 0:
                    cell_edges["left"] = col_rule
                if c_idx < num_cols - 1:
                    cell_edges["right"] = col_rule
                if fill_hex:
                    _set_cell_shading(cell, fill_hex)

            _set_cell_border_edges(cell, **cell_edges)
            _set_cell_margins(cell, top=55, bottom=55, left=lr_pad, right=lr_pad)


def _render_display_equation(doc: docx.Document, raw_block: str) -> None:
    eq_num = ""
    tex = raw_block.strip()
    m = re.search(r"\\qquad\s*\((\d+\.\d+)\)\s*$", tex)
    if m:
        eq_num = f"({m.group(1)})"
        tex = tex[: m.start()].strip()

    size_pt = 11 if len(tex) > 95 else 12
    omath_para = latex_to_omml(tex, font_size=size_pt, display=True)

    tbl = doc.add_table(rows=1, cols=3)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    _clear_table_borders(tbl)
    _set_row_props(tbl.rows[0], cant_split=True, is_header=False)

    for c_idx in range(3):
        cell = tbl.cell(0, c_idx)
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        _set_cell_margins(cell, top=30, bottom=55, left=0, right=0)

    mid_p = tbl.cell(0, 1).paragraphs[0]
    mid_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    mid_p.paragraph_format.first_line_indent = Cm(0)
    mid_p.paragraph_format.line_spacing = 1.0
    mid_p.paragraph_format.space_before = Pt(0)
    mid_p.paragraph_format.space_after = Pt(0)
    mid_p._p.append(omath_para)

    num_p = tbl.cell(0, 2).paragraphs[0]
    num_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    num_p.paragraph_format.first_line_indent = Cm(0)
    num_p.paragraph_format.line_spacing = 1.0
    num_p.paragraph_format.space_before = Pt(0)
    num_p.paragraph_format.space_after = Pt(0)
    if eq_num:
        run = num_p.add_run(eq_num)
        _style_run(run, 12, False, False)

    _set_table_fixed_grid(tbl, [0.4, 12.3, 1.3])


def _split_markdown_table_row(row_str: str) -> list[str]:
    inner = row_str.strip()
    inner = inner.removeprefix("|")
    if inner.endswith("|") and not inner.endswith(r"\|"):
        inner = inner[:-1]
    parts = re.split(r"(?<!\\)\|", inner)
    return [p.replace(r"\|", "|").strip() for p in parts]


def _parse_col_alignments(sep_row: str) -> list[WD_ALIGN_PARAGRAPH | None]:
    aligns: list[WD_ALIGN_PARAGRAPH | None] = []
    for cell in _split_markdown_table_row(sep_row):
        c = cell.strip()
        if c.startswith(":") and c.endswith(":"):
            aligns.append(WD_ALIGN_PARAGRAPH.CENTER)
        elif c.endswith(":"):
            aligns.append(WD_ALIGN_PARAGRAPH.RIGHT)
        elif c.startswith(":"):
            aligns.append(WD_ALIGN_PARAGRAPH.LEFT)
        else:
            aligns.append(None)
    return aligns


def _compute_smart_column_widths(rows: list[list[str]], cols: int) -> list[float]:
    if cols <= 1:
        return [PRINTABLE_WIDTH_CM]

    min_cm: list[float] = []
    weight: list[float] = []
    max_tok_cap = 26 if cols <= 4 else 18
    for c_idx in range(cols):
        lengths: list[int] = []
        max_word_len = 3
        for r_idx, row in enumerate(rows):
            plain = strip_markdown_plain(row[c_idx]) if c_idx < len(row) else ""
            lengths.append(len(plain))
            for tok in re.split(r"[\s]+", plain):
                clean_tok = tok.strip(".,:;[]\"'()")
                is_snake_token = "_" in clean_tok and len(clean_tok) <= 24 and cols >= 5
                if (
                    2 <= len(clean_tok) <= max_tok_cap
                    or (r_idx == 0 and len(clean_tok) <= 18)
                    or is_snake_token
                ):
                    max_word_len = max(max_word_len, len(clean_tok))
        lengths.sort()
        p85 = lengths[min(len(lengths) - 1, int(0.85 * len(lengths)))]
        head_len = len(strip_markdown_plain(rows[0][c_idx])) if c_idx < len(rows[0]) else 4
        eff_len = max(head_len, p85, 3)
        weight.append(math.sqrt(eff_len))
        max_req_cm = 4.2 if cols <= 4 else 3.2
        req_cm = max(0.95, min(max_req_cm, max_word_len * 0.175 + 0.28))
        min_cm.append(req_cm)

    min_sum = sum(min_cm)
    if min_sum >= PRINTABLE_WIDTH_CM:
        scale = PRINTABLE_WIDTH_CM / min_sum
        widths = [round(w * scale, 3) for w in min_cm]
    else:
        rem = PRINTABLE_WIDTH_CM - min_sum
        w_sum = sum(weight) or 1.0
        widths = [round(m + rem * (wt / w_sum), 3) for m, wt in zip(min_cm, weight)]

    diff = round(PRINTABLE_WIDTH_CM - sum(widths), 3)
    max_idx = max(range(cols), key=lambda k: widths[k])
    widths[max_idx] = round(widths[max_idx] + diff, 3)
    return widths


def _render_borderless_keyvalue_table(
    doc: docx.Document,
    rows: list[list[str]],
    first_col_cm: float = 4.2,
    left_indent_cm: float = 0.0,
) -> None:
    tbl = doc.add_table(rows=len(rows), cols=3)
    tbl.alignment = WD_TABLE_ALIGNMENT.LEFT
    _clear_table_borders(tbl)
    if left_indent_cm > 0:
        tbl_pr = tbl._tbl.tblPr
        for old in tbl_pr.findall(qn("w:tblInd")):
            tbl_pr.remove(old)
        ind = OxmlElement("w:tblInd")
        ind.set(qn("w:w"), str(round(left_indent_cm * 567)))
        ind.set(qn("w:type"), "dxa")
        tbl_pr.append(ind)
    val_cm = round(PRINTABLE_WIDTH_CM - left_indent_cm - first_col_cm - 0.4, 2)
    for r_idx, row_data in enumerate(rows):
        _set_row_props(tbl.rows[r_idx], cant_split=True)
        key = row_data[0]
        val = row_data[1] if len(row_data) > 1 else ""
        for c_idx, txt in enumerate((key, ":", val)):
            cell = tbl.cell(r_idx, c_idx)
            _set_cell_margins(cell, top=22, bottom=22, left=15, right=15)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.line_spacing = 1.4
            p.paragraph_format.first_line_indent = Cm(0)
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(1)
            add_formatted_runs(p, txt, font_size=12, bold_default=False)
    _set_table_fixed_grid(tbl, [first_col_cm, 0.4, val_cm])


def _render_orisinalitas_signature(doc: docx.Document, row: list[str]) -> None:
    date_txt = row[0] if len(row) > 0 else ""
    materai_txt = row[1] if len(row) > 1 else "(meterai Rp10.000)"
    name_txt = row[2] if len(row) > 2 else ""

    for txt, sb, sa, left_ind in (
        (date_txt, 14, 2, 0.0),
        ("Yang membuat pernyataan,", 0, 12, 0.0),
        (materai_txt, 14, 18, 0.8),
        (name_txt, 8, 0, 0.0),
    ):
        if not txt:
            continue
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.left_indent = Cm(left_ind)
        p.paragraph_format.first_line_indent = Cm(0)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_before = Pt(sb)
        p.paragraph_format.space_after = Pt(sa)
        add_formatted_runs(p, txt, font_size=12, bold_default=False)


def _render_pengesahan_signatures(doc: docx.Document, data_rows: list[list[str]]) -> None:
    """Render Halaman Pengesahan grid per Lampiran 3 (single advisor centered above Kaprodi)."""
    slots: list[tuple[str, str]] = []
    footer_rows: list[list[str]] = []
    for row in data_rows:
        role = row[0] if len(row) > 0 else ""
        person = row[1] if len(row) > 1 else ""
        low = role.lower()
        if low.startswith(("ditetapkan", "tanggal")):
            footer_rows.append([role, person])
        else:
            slots.append((role, person))

    def _fill_sig_cell(cell: docx.table._Cell, role_txt: str, person_txt: str) -> None:
        _set_cell_margins(cell, top=42, bottom=42, left=30, right=30)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.first_line_indent = Cm(0)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        add_formatted_runs(p, role_txt, font_size=12, bold_default=False)

        sp = cell.add_paragraph()
        sp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        sp.paragraph_format.first_line_indent = Cm(0)
        sp.paragraph_format.space_before = Pt(28)
        sp.paragraph_format.space_after = Pt(10)
        sp.paragraph_format.line_spacing = 1.0
        add_formatted_runs(sp, person_txt, font_size=12, bold_default=False)

    if slots:
        pair_count = 1 if len(slots) >= 2 else 0
        rem = slots[2:] if len(slots) >= 2 else slots
        total_rows = pair_count + len(rem)
        tbl = doc.add_table(rows=total_rows, cols=2)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        _clear_table_borders(tbl)
        _set_table_fixed_grid(tbl, [7.0, 7.0])

        for row in tbl.rows:
            _set_row_props(row, cant_split=True)

        if pair_count == 1:
            for c_idx in range(2):
                _fill_sig_cell(tbl.cell(0, c_idx), slots[c_idx][0], slots[c_idx][1])

        for offset, (role_txt, person_txt) in enumerate(rem):
            r_idx = pair_count + offset
            merged = tbl.cell(r_idx, 0).merge(tbl.cell(r_idx, 1))
            tc_pr = merged._tc.get_or_add_tcPr()
            for old in tc_pr.findall(qn("w:tcW")):
                tc_pr.remove(old)
            tc_w = OxmlElement("w:tcW")
            tc_w.set(qn("w:w"), str(PRINTABLE_WIDTH_DXA))
            tc_w.set(qn("w:type"), "dxa")
            tc_pr.append(tc_w)
            _fill_sig_cell(merged, role_txt, person_txt)

    if footer_rows:
        sp_p = doc.add_paragraph()
        sp_p.paragraph_format.first_line_indent = Cm(0)
        sp_p.paragraph_format.space_before = Pt(4)
        sp_p.paragraph_format.space_after = Pt(0)
        sp_p.paragraph_format.line_spacing = 1.0
        _render_borderless_keyvalue_table(doc, footer_rows, first_col_cm=2.8, left_indent_cm=0.0)


def _render_kata_pengantar_closing(doc: docx.Document, row: list[str]) -> None:
    date_txt = row[0] if len(row) > 0 else ""
    author_txt = row[1] if len(row) > 1 else "**Penulis**"
    tbl = doc.add_table(rows=1, cols=2)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    _clear_table_borders(tbl)
    _set_row_props(tbl.rows[0], cant_split=True)
    cell = tbl.cell(0, 1)
    _set_cell_margins(cell, top=120, bottom=40, left=40, right=40)
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.first_line_indent = Cm(0)
    p.paragraph_format.line_spacing = 1.3
    p.paragraph_format.space_after = Pt(28)
    add_formatted_runs(p, date_txt, font_size=12, bold_default=False)

    p2 = cell.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p2.paragraph_format.first_line_indent = Cm(0)
    p2.paragraph_format.line_spacing = 1.0
    add_formatted_runs(p2, author_txt, font_size=12, bold_default=False)
    _set_table_fixed_grid(tbl, [8.5, 5.5])


def _render_static_toc_paragraphs(
    doc: docx.Document, table_lines: list[list[str]], current_h1: str
) -> None:
    """Render static dot-leader entries for standalone 00-bagian-awal.docx."""
    data_rows = table_lines[1:] if len(table_lines) > 1 else table_lines
    for row in data_rows:
        if current_h1 == "DAFTAR ISI":
            label = row[0] if len(row) > 0 else ""
            page = row[1] if len(row) > 1 else ""
            plain_lbl = strip_markdown_plain(label)
            if re.match(r"^\d+\.\d+\.\d+\s+", plain_lbl):
                style = "TOC 3"
            elif re.match(r"^(\d+\.\d+|Lampiran\s+\d+)\s*", plain_lbl):
                style = "TOC 2"
            else:
                style = "TOC 1"
        else:
            num_lbl = row[0] if len(row) > 0 else ""
            title_lbl = row[1] if len(row) > 1 else ""
            page = row[2] if len(row) > 2 else ""
            label = f"{num_lbl} {title_lbl}".strip()
            style = "Table of Figures"

        p = doc.add_paragraph(style=style)
        p.paragraph_format.first_line_indent = Cm(0)
        add_formatted_runs(p, label, font_size=12, bold_default=False)
        tab_run = p.add_run(f"\t{page.strip()}")
        _style_run(tab_run, 12, False, False)


def _render_academic_table(
    doc: docx.Document,
    table_lines: list[list[str]],
    col_aligns: list[WD_ALIGN_PARAGRAPH | None] | None = None,
) -> None:
    cols = max(len(r) for r in table_lines)
    tbl = doc.add_table(rows=len(table_lines), cols=cols)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    compact_table = len(table_lines) <= 6

    merge_pairs: list[int] = []
    for r_idx in range(2, len(table_lines)):
        prev_c0 = strip_markdown_plain(table_lines[r_idx - 1][0]).strip()
        cur_c0 = strip_markdown_plain(table_lines[r_idx][0]).strip()
        if cols >= 5 and prev_c0 and not cur_c0:
            merge_pairs.append(r_idx)

    pair_set = set(merge_pairs)
    pair_bottom_rows = set(merge_pairs)
    summary_rows: set[int] = set()
    row_fills: list[str | None] = [None] * len(table_lines)
    pair_idx = 0

    for r_idx, row_data in enumerate(table_lines):
        first_raw = row_data[0].strip() if row_data else ""
        if r_idx >= 1 and first_raw.startswith(("**Total", "**Penelitian Ini")):
            summary_rows.add(r_idx)
            row_fills[r_idx] = "F1F5F9"
        elif merge_pairs and r_idx >= 1:
            if r_idx in pair_set:
                row_fills[r_idx] = row_fills[r_idx - 1]
            else:
                row_fills[r_idx] = "F8FAFC" if (pair_idx % 2 == 1) else "FFFFFF"
                pair_idx += 1
        elif r_idx >= 2 and r_idx % 2 == 0 and len(table_lines) >= 8:
            row_fills[r_idx] = "FAFBFD"

    for r_idx, row_data in enumerate(table_lines):
        for c_idx in range(cols):
            val = row_data[c_idx] if c_idx < len(row_data) else ""
            cell = tbl.cell(r_idx, c_idx)
            if r_idx == 0 or (r_idx in pair_set and c_idx == 0):
                cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.0
            p.paragraph_format.first_line_indent = Cm(0)
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.widow_control = True
            if (
                r_idx == 0
                or (compact_table and r_idx < len(table_lines) - 1)
                or ((r_idx + 1) in pair_set)
                or (merge_pairs and len(table_lines) <= 22 and r_idx < min(len(table_lines) - 1, 5))
            ):
                p.paragraph_format.keep_with_next = True

            plain_val = strip_markdown_plain(val).strip()
            explicit_align = (
                col_aligns[c_idx] if col_aligns and c_idx < len(col_aligns) else None
            )
            if r_idx == 0:
                p.alignment = (
                    explicit_align
                    if explicit_align is not None
                    else WD_ALIGN_PARAGRAPH.LEFT
                )
            elif explicit_align == WD_ALIGN_PARAGRAPH.CENTER and len(plain_val) <= 28:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            elif explicit_align == WD_ALIGN_PARAGRAPH.RIGHT:
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            elif cols >= 3 and c_idx >= 1 and re.match(r"^[\d.,+%±<>=\-\s/()✓]+$", plain_val):
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT

            if r_idx in pair_set and c_idx == 0:
                continue
            add_formatted_runs(p, val, font_size=10, bold_default=(r_idx == 0))

    _set_academic_table_borders(
        tbl,
        row_fills=row_fills,
        summary_rows=summary_rows,
        pair_bottom_rows=pair_bottom_rows,
        cols=cols,
    )
    for r_idx, row_data in enumerate(table_lines):
        if r_idx >= 1:
            for c_idx in range(cols):
                if c_idx < len(row_data) and row_data[c_idx].strip() == "✓":
                    tbl.cell(r_idx, c_idx).vertical_alignment = WD_ALIGN_VERTICAL.CENTER
                    _set_cell_shading(tbl.cell(r_idx, c_idx), "E2E8F0")

    widths_cm = _compute_smart_column_widths(table_lines, cols)
    _set_table_fixed_grid(tbl, widths_cm)

    for r_idx in merge_pairs:
        merged = tbl.cell(r_idx - 1, 0).merge(tbl.cell(r_idx, 0))
        merged.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        _set_cell_border_edges(
            merged,
            top=("single", "6", "475569") if (r_idx - 2) in pair_set else ("single", "4", "B8C2CC"),
            bottom=("single", "8", "000000") if r_idx == len(table_lines) - 1 else ("single", "6", "475569"),
            right=("single", "4", "CBD5E1"),
        )


def _render_cover_section(
    doc: docx.Document, cover_lines: list[str], md_dir: Path
) -> None:
    sec0 = doc.sections[0]
    sec0.different_first_page_header_footer = True
    _set_page_number_format(sec0, "lowerRoman", start=1)

    h2_idx = 0
    h2_total = sum(1 for ln in cover_lines if ln.strip().startswith("## "))

    for raw_ln in cover_lines:
        raw = raw_ln.strip()
        if not raw or raw == "---":
            continue
        if raw.startswith("# "):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.first_line_indent = Cm(0)
            p.paragraph_format.line_spacing = 1.0
            p.paragraph_format.space_before = Pt(12)
            p.paragraph_format.space_after = Pt(24)
            add_formatted_runs(p, raw[2:].strip().upper(), font_size=16, bold_default=True)
            _add_tc_field(p, "HALAMAN JUDUL", "C", "1")
            continue

        img_match = IMG_LINE_RE.match(raw)
        if img_match:
            _add_image_block(
                doc,
                img_match,
                md_dir,
                has_explicit_caption=False,
                max_width_cm=COVER_LOGO_WIDTH_CM,
                max_height_cm=None,
                suppress_caption=True,
                space_before=16,
                space_after=24,
            )
            continue

        if raw.startswith("## "):
            txt = raw[3:].strip()
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.first_line_indent = Cm(0)
            if h2_idx == 0:
                p.paragraph_format.line_spacing = 1.15
                p.paragraph_format.space_after = Pt(42)
                add_formatted_runs(p, txt, font_size=16, bold_default=True)
            elif h2_idx == 1:
                p.paragraph_format.line_spacing = 1.5
                p.paragraph_format.space_after = Pt(20)
                add_formatted_runs(p, txt, font_size=14, bold_default=False)
            elif txt.lower().startswith("oleh"):
                p.paragraph_format.line_spacing = 1.5
                p.paragraph_format.space_before = Pt(8)
                p.paragraph_format.space_after = Pt(2)
                add_formatted_runs(p, txt, font_size=12, bold_default=True)
            elif h2_idx == h2_total - 4 or re.match(r"^\d{6,}", txt):
                p.paragraph_format.line_spacing = 1.5
                p.paragraph_format.space_after = Pt(42)
                add_formatted_runs(p, txt, font_size=12, bold_default=True)
            else:
                p.paragraph_format.line_spacing = 1.0
                p.paragraph_format.space_before = Pt(0)
                p.paragraph_format.space_after = Pt(2)
                add_formatted_runs(p, txt, font_size=14, bold_default=True)
            h2_idx += 1


# ---------------------------------------------------------------------------
# Main Markdown -> Native UNSIA DOCX converter
# ---------------------------------------------------------------------------


def build_unsia_docx_only(md_path: Path, out_docx: Path) -> None:
    """Build native Microsoft Word .docx cleanly from Markdown without COM side-effects."""
    doc = docx.Document()
    numbering_abs = configure_unsia_document(doc)

    md_dir = md_path.resolve().parent
    lines = md_path.read_text(encoding="utf-8").splitlines()
    has_body_chapters = any(ln.strip().upper().startswith("# BAB ") for ln in lines)

    i = 0
    if lines and lines[0].strip().upper() == "# TUGAS AKHIR":
        cover_block: list[str] = []
        while i < len(lines) and lines[i].strip() != "---":
            cover_block.append(lines[i])
            i += 1
        _render_cover_section(doc, cover_block, md_dir)
        if i < len(lines) and lines[i].strip() == "---":
            i += 1

        front_sec = doc.add_section(WD_SECTION.NEW_PAGE)
        _set_unsia_margins(front_sec)
        front_sec.different_first_page_header_footer = False
        _set_page_number_format(front_sec, "lowerRoman", start=2)
        _add_page_number_footer(front_sec.footer, WD_ALIGN_PARAGRAPH.CENTER)
        has_started_front_heading = False
    else:
        sec0 = doc.sections[0]
        sec0.different_first_page_header_footer = True
        _set_page_number_format(sec0, "decimal", start=1)
        _add_page_number_footer(sec0.first_page_footer, WD_ALIGN_PARAGRAPH.CENTER)
        _add_page_number_footer(sec0.footer, WD_ALIGN_PARAGRAPH.RIGHT)
        has_started_front_heading = True

    in_abstrak = False
    in_abstract_en = False
    in_bibliography = False
    in_body_chapters = False
    has_started_main_section = False
    current_h1 = ""

    active_list_kind: str | None = None
    active_list_num_id: int | None = None

    while i < len(lines):
        raw = lines[i].strip()
        if not raw or raw == "---":
            i += 1
            continue

        # Multi-line or single-line display equation $$...$$
        if raw.startswith("$$"):
            active_list_kind = None
            active_list_num_id = None
            eq_parts = [raw[2:]]
            if raw.endswith("$$") and len(raw) > 4:
                eq_body = raw[2:-2]
            else:
                i += 1
                while i < len(lines):
                    ln = lines[i].strip()
                    if ln.endswith("$$"):
                        eq_parts.append(ln[:-2])
                        break
                    eq_parts.append(ln)
                    i += 1
                eq_body = " ".join(eq_parts)
            _render_display_equation(doc, eq_body)
            i += 1
            continue

        if raw.startswith("# "):
            active_list_kind = None
            active_list_num_id = None
            title_txt = raw[2:].strip().upper()
            current_h1 = title_txt
            is_bab = title_txt.startswith("BAB ")
            is_bib = title_txt == "DAFTAR PUSTAKA"
            is_lampiran = title_txt == "LAMPIRAN"
            is_abstract_en_h = title_txt == "ABSTRACT"

            if is_bab or is_bib or is_lampiran:
                in_body_chapters = True
                in_bibliography = is_bib
                in_abstrak = False
                in_abstract_en = False
                if doc.paragraphs or has_started_main_section:
                    chap_sec = doc.add_section(WD_SECTION.NEW_PAGE)
                    _set_unsia_margins(chap_sec)
                    chap_sec.different_first_page_header_footer = True
                    _set_page_number_format(
                        chap_sec,
                        "decimal",
                        start=1 if not has_started_main_section else None,
                    )
                    _add_page_number_footer(
                        chap_sec.first_page_footer, WD_ALIGN_PARAGRAPH.CENTER
                    )
                    _add_page_number_footer(chap_sec.footer, WD_ALIGN_PARAGRAPH.RIGHT)
                has_started_main_section = True
                p = doc.add_paragraph(style="Heading 1")
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p.paragraph_format.space_before = Pt(28)
                p.paragraph_format.space_after = Pt(12)
                p.paragraph_format.first_line_indent = Cm(0)
                add_formatted_runs(p, title_txt, font_size=12, bold_default=True)
            else:
                if is_abstract_en_h:
                    p = doc.add_paragraph()
                    in_abstrak = True
                    in_abstract_en = True
                    p.paragraph_format.page_break_before = False
                    p.paragraph_format.space_before = Pt(14)
                    p.paragraph_format.space_after = Pt(6)
                    p.paragraph_format.keep_with_next = True
                else:
                    p = doc.add_paragraph(style="Heading 1")
                    in_abstract_en = False
                    if title_txt == "ABSTRAK":
                        in_abstrak = True
                        p.paragraph_format.page_break_before = has_started_front_heading
                        p.paragraph_format.space_before = Pt(0)
                        p.paragraph_format.space_after = Pt(6)
                    else:
                        in_abstrak = False
                        p.paragraph_format.page_break_before = (
                            has_started_front_heading or in_body_chapters
                        )
                        p.paragraph_format.space_before = Pt(0)
                        p.paragraph_format.space_after = Pt(12)
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p.paragraph_format.first_line_indent = Cm(0)
                if not in_body_chapters:
                    has_started_front_heading = True
                add_formatted_runs(
                    p,
                    title_txt,
                    font_size=12,
                    bold_default=True,
                    lang="en-US" if is_abstract_en_h else None,
                )

                if title_txt in TOC_SECTIONS:
                    hp = doc.add_paragraph()
                    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                    hp.paragraph_format.first_line_indent = Cm(0)
                    hp.paragraph_format.line_spacing = 1.5
                    hp.paragraph_format.space_before = Pt(0)
                    hp.paragraph_format.space_after = Pt(4)
                    add_formatted_runs(hp, "Halaman", font_size=12, bold_default=False)
                    if has_body_chapters:
                        if title_txt == "DAFTAR ISI":
                            _add_toc_field(doc, 'TOC \\o "1-3" \\f C \\h \\z \\u')
                        elif title_txt == "DAFTAR GAMBAR":
                            _add_toc_field(doc, 'TOC \\h \\z \\c "Gambar"')
                        elif title_txt == "DAFTAR TABEL":
                            _add_toc_field(doc, 'TOC \\h \\z \\c "Tabel"')

            i += 1
            continue

        if raw.startswith("## "):
            active_list_kind = None
            active_list_num_id = None
            sub_txt = raw[3:].strip().rstrip(".")
            p = doc.add_paragraph(style="Heading 2")
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(12)
            p.paragraph_format.space_after = Pt(6)
            p.paragraph_format.first_line_indent = Cm(0)
            p.paragraph_format.keep_with_next = True
            add_formatted_runs(p, sub_txt, font_size=12, bold_default=True)
            in_abstrak = False
            in_abstract_en = False
            i += 1
            continue

        if raw.startswith("### "):
            active_list_kind = None
            active_list_num_id = None
            subsub_txt = raw[4:].strip().rstrip(".")
            p = doc.add_paragraph(style="Heading 3")
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(8)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.first_line_indent = Cm(0)
            p.paragraph_format.keep_with_next = True
            add_formatted_runs(p, subsub_txt, font_size=12, bold_default=True)
            i += 1
            continue

        img_match = IMG_LINE_RE.match(raw)
        if img_match:
            active_list_kind = None
            active_list_num_id = None
            has_caption = _has_following_gambar_caption(lines, i + 1)
            _add_image_block(doc, img_match, md_dir, has_caption)
            i += 1
            continue

        tbl_cap_m = TABEL_CAPTION_RE.match(raw)
        if tbl_cap_m:
            active_list_kind = None
            active_list_num_id = None
            _add_seq_caption(
                doc,
                "Tabel",
                "Tabel",
                tbl_cap_m.group(1),
                tbl_cap_m.group(2),
                tbl_cap_m.group(3),
                "Caption Tabel",
                inherit_style_bold=False,
                ensure_trailing_dot=False,
            )
            i += 1
            continue

        unbolded_raw = _strip_outer_bold_caption(raw)
        fig_cap_m = GAMBAR_CAPTION_RE.match(unbolded_raw)
        if fig_cap_m:
            active_list_kind = None
            active_list_num_id = None
            _add_seq_caption(
                doc,
                "Gambar",
                "Gambar",
                fig_cap_m.group(1),
                fig_cap_m.group(2),
                fig_cap_m.group(3),
                "Caption",
                inherit_style_bold=True,
                ensure_trailing_dot=True,
            )
            i += 1
            continue

        if PERSAMAAN_CAPTION_RE.match(raw):
            active_list_kind = None
            active_list_num_id = None
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.first_line_indent = Cm(0)
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.keep_with_next = True
            p.paragraph_format.widow_control = True
            add_formatted_runs(p, raw, font_size=12, bold_default=False)
            i += 1
            continue

        if raw.startswith(("Sumber:", "*Sumber:")):
            active_list_kind = None
            active_list_num_id = None
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.first_line_indent = Cm(0)
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(8)
            p.paragraph_format.widow_control = True
            add_formatted_runs(p, raw, font_size=10, italic_default=True)
            i += 1
            continue

        if raw.startswith("|"):
            active_list_kind = None
            active_list_num_id = None
            table_lines: list[list[str]] = []
            col_aligns: list[WD_ALIGN_PARAGRAPH | None] = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                row_str = lines[i].strip()
                if re.match(r"^\|[\s:|-]+\|$", row_str):
                    if not col_aligns:
                        col_aligns = _parse_col_alignments(row_str)
                else:
                    table_lines.append(_split_markdown_table_row(row_str))
                i += 1

            if current_h1 in TOC_SECTIONS:
                if not has_body_chapters and table_lines:
                    _render_static_toc_paragraphs(doc, table_lines, current_h1)
                continue

            if table_lines:
                hdr0 = table_lines[0][0] if table_lines[0] else ""
                if current_h1 in BORDERLESS_META_SECTIONS:
                    data_rows = table_lines[1:] if len(table_lines) > 1 else table_lines
                    if hdr0.startswith("Atribut"):
                        if current_h1 == "HALAMAN PENGESAHAN":
                            _render_borderless_keyvalue_table(
                                doc, data_rows, first_col_cm=3.6, left_indent_cm=0.8
                            )
                        else:
                            _render_borderless_keyvalue_table(
                                doc, data_rows, first_col_cm=3.8, left_indent_cm=0.0
                            )
                    elif current_h1 == "HALAMAN PERNYATAAN ORISINALITAS":
                        _render_orisinalitas_signature(doc, data_rows[0])
                    elif current_h1 == "HALAMAN PENGESAHAN":
                        _render_pengesahan_signatures(doc, data_rows)
                    elif current_h1 == "KATA PENGANTAR":
                        _render_kata_pengantar_closing(doc, data_rows[0])
                    else:
                        _render_academic_table(doc, table_lines, col_aligns)
                else:
                    _render_academic_table(doc, table_lines, col_aligns)
            continue

        bib_m = BIB_ITEM_RE.match(raw) if in_bibliography else None
        if bib_m:
            active_list_kind = None
            active_list_num_id = None
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.line_spacing = 1.5
            p.paragraph_format.left_indent = Cm(1.0)
            p.paragraph_format.first_line_indent = Cm(-1.0)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.widow_control = True
            p.paragraph_format.tab_stops.clear_all()
            p.paragraph_format.tab_stops.add_tab_stop(Cm(1.0), WD_TAB_ALIGNMENT.LEFT)
            tag_run = p.add_run(f"{bib_m.group(1)}\t")
            _style_run(tag_run, 12, False, False)
            add_formatted_runs(p, bib_m.group(2), font_size=12, bold_default=False)
            i += 1
            continue

        list_m = LIST_ITEM_RE.match(raw)
        if list_m:
            alpha_lbl, dec_lbl, body_txt = list_m.groups()
            if alpha_lbl is not None:
                kind = "lowerLetter"
            elif dec_lbl is not None:
                kind = "decimal"
            else:
                kind = "bullet"

            if kind != active_list_kind or active_list_num_id is None:
                active_list_kind = kind
                active_list_num_id = _allocate_list_num_id(doc, numbering_abs[kind])

            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.line_spacing = 1.5
            p.paragraph_format.widow_control = True
            _attach_num_pr(p, active_list_num_id)
            add_formatted_runs(p, body_txt, font_size=12, bold_default=False)
            i += 1
            continue

        active_list_kind = None
        active_list_num_id = None
        is_formal_block = current_h1 in {
            "HALAMAN PERNYATAAN ORISINALITAS",
            "HALAMAN PENGESAHAN",
        }
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.0 if in_abstrak else 1.5
        p.paragraph_format.widow_control = True
        if in_abstrak:
            p.paragraph_format.first_line_indent = Cm(0)
            p.paragraph_format.space_after = Pt(6)
        elif is_formal_block:
            p.paragraph_format.first_line_indent = Cm(0)
            if raw.endswith(":"):
                p.paragraph_format.space_before = Pt(2)
                p.paragraph_format.space_after = Pt(4)
            else:
                p.paragraph_format.space_before = Pt(6)
                p.paragraph_format.space_after = Pt(8)
        else:
            p.paragraph_format.first_line_indent = Cm(1.5)

        lang_override = "en-US" if in_abstract_en else None
        if in_abstrak and (raw.startswith(("Kata Kunci:", "Keywords:"))):
            label, rest = raw.split(":", 1)
            add_formatted_runs(
                p,
                f"**{label}:**{rest}",
                font_size=12,
                bold_default=False,
                lang=lang_override,
            )
        else:
            add_formatted_runs(
                p, raw, font_size=12, bold_default=False, lang=lang_override
            )
        i += 1

    out_docx.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(out_docx))


# ---------------------------------------------------------------------------
# Local non-OneDrive Word COM staging + statistics/page-map + PDF export
# ---------------------------------------------------------------------------


def _run_word_com_on_local_stage(
    stage_docx: Path, stage_pdf: Path
) -> tuple[dict[str, int], list[dict[str, object]]]:
    ps_docx = str(stage_docx.resolve()).replace("'", "''")
    ps_pdf = str(stage_pdf.resolve()).replace("'", "''")
    ps_script = f"""
$ErrorActionPreference = 'Stop'
$word = $null
$doc = $null
try {{
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $word.DisplayAlerts = 0
    $doc = $word.Documents.Open('{ps_docx}')
    $doc.Fields.Update() | Out-Null
    foreach ($toc in $doc.TablesOfContents) {{ $toc.Update() | Out-Null }}
    foreach ($tof in $doc.TablesOfFigures) {{ $tof.Update() | Out-Null }}
    $tocRightIndent = $word.CentimetersToPoints(1.35)
    foreach ($stName in @('toc 1', 'toc 2', 'toc 3', 'table of figures', 'TOC 1', 'TOC 2', 'TOC 3', 'Table of Figures')) {{
        try {{
            $stObj = $doc.Styles.Item($stName)
            $stObj.Font.Name = 'Times New Roman'
            $stObj.Font.Size = 12
            $stObj.Font.Color = 0
            $stObj.Font.Bold = 0
            $stObj.ParagraphFormat.RightIndent = $tocRightIndent
            $stObj.ParagraphFormat.SpaceBefore = 0
            $stObj.ParagraphFormat.SpaceAfter = 2
            $stObj.ParagraphFormat.LineSpacingRule = 1
            if ($stName -like '*2*') {{ $stObj.ParagraphFormat.LeftIndent = $word.CentimetersToPoints(0.75) }}
            elseif ($stName -like '*3*') {{ $stObj.ParagraphFormat.LeftIndent = $word.CentimetersToPoints(1.5) }}
            else {{ $stObj.ParagraphFormat.LeftIndent = 0 }}
        }} catch {{}}
    }}
    foreach ($p in $doc.Paragraphs) {{
        $sname = $p.Style.NameLocal
        if ($sname -like 'TOC*' -or $sname -like 'Table of Figures*') {{
            $p.Range.Font.Name = 'Times New Roman'
            $p.Range.Font.Size = 12
            $p.Range.Font.Color = 0
            $p.Range.Font.Bold = 0
            $p.Range.ParagraphFormat.RightIndent = $tocRightIndent
            $p.Range.ParagraphFormat.SpaceBefore = 0
            $p.Range.ParagraphFormat.SpaceAfter = 2
            $p.Range.ParagraphFormat.LineSpacingRule = 1
        }}
    }}
    $doc.Repaginate()
    foreach ($toc in $doc.TablesOfContents) {{ $toc.UpdatePageNumbers() | Out-Null }}
    foreach ($tof in $doc.TablesOfFigures) {{ $tof.UpdatePageNumbers() | Out-Null }}
    foreach ($p in $doc.Paragraphs) {{
        $sname = $p.Style.NameLocal
        if ($sname -like 'TOC*' -or $sname -like 'Table of Figures*') {{
            $p.Range.Font.Name = 'Times New Roman'
            $p.Range.Font.Size = 12
            $p.Range.Font.Color = 0
            $p.Range.Font.Bold = 0
            $p.Range.ParagraphFormat.RightIndent = $tocRightIndent
            $p.Range.ParagraphFormat.SpaceBefore = 0
            $p.Range.ParagraphFormat.SpaceAfter = 2
            $p.Range.ParagraphFormat.LineSpacingRule = 1
        }}
    }}
    $doc.Repaginate()

    $items = New-Object System.Collections.Generic.List[object]
    foreach ($p in $doc.Paragraphs) {{
        $sname = $p.Style.NameLocal
        if ($sname -in @('Heading 1', 'Heading 2', 'Heading 3', 'Caption', 'Caption Tabel')) {{
            $pg = $p.Range.Information(1)
            $txt = ($p.Range.Text -replace "[`r`n`a]+$", '').Trim()
            if ($txt) {{
                $items.Add([PSCustomObject]@{{ style = $sname; page = [int]$pg; text = $txt }})
            }}
        }}
    }}
    $json = $items | ConvertTo-Json -Compress
    if (-not $json.StartsWith('[')) {{ $json = "[$json]" }}

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
    Write-Output "PAGE_MAP:$json"
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
        timeout=120,
    )
    if res.returncode != 0:
        raise RuntimeError(
            f"Gagal Word COM pada staging {stage_docx.name}: {res.stderr or res.stdout}"
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
    page_map: list[dict[str, object]] = []
    for line in res.stdout.splitlines():
        if line.startswith("WORD_STATS:"):
            vals = [int(v.strip()) for v in line.removeprefix("WORD_STATS:").split(",")]
            stats = dict(zip(keys, vals, strict=True))
        elif line.startswith("PAGE_MAP:"):
            raw_json = line.removeprefix("PAGE_MAP:").strip()
            if raw_json and raw_json != "[$null]":
                loaded = json.loads(raw_json)
                if isinstance(loaded, list):
                    page_map = [x for x in loaded if isinstance(x, dict)]
    return stats, page_map


@dataclass(frozen=True)
class DeliverableSpec:
    key: str
    md_rel: str
    docx_rel: str | None
    pdf_rel: str
    meta: DocumentMetadata


DELIVERABLE_SPECS: tuple[DeliverableSpec, ...] = (
    DeliverableSpec(
        key="00-bagian-awal",
        md_rel="06-naskah-ta/md/00-bagian-awal/00-bagian-awal.md",
        docx_rel="06-naskah-ta/docx/00-bagian-awal/00-bagian-awal.docx",
        pdf_rel="06-naskah-ta/pdf/00-bagian-awal/00-bagian-awal.pdf",
        meta=DocumentMetadata(
            title="Bagian Awal Tugas Akhir - Deteksi Phishing WhatsApp Otoritas Perpajakan",
            subject="Bagian Awal Naskah Tugas Akhir - PJJ Sistem Informasi UNSIA",
            author="Wan Mirza Dhani",
            last_modified_by="Wan Mirza Dhani",
            keywords="Cover, Pengesahan, Abstrak, Daftar Isi, Tugas Akhir UNSIA",
            category="Naskah Tugas Akhir",
            description="Bagian Awal Tugas Akhir Wan Mirza Dhani (240101020194).",
            company="Universitas Siber Asia",
            revision=18,
            total_time_minutes=320,
            created=datetime(2026, 10, 30, 20, 15, 0, tzinfo=WIB),
            modified=datetime(2026, 11, 28, 11, 20, 0, tzinfo=WIB),
        ),
    ),
    DeliverableSpec(
        key="01-bab-1",
        md_rel="06-naskah-ta/md/01-bab-1-pendahuluan/01-bab-1-pendahuluan.md",
        docx_rel="06-naskah-ta/docx/01-bab-1-pendahuluan/01-bab-1-pendahuluan.docx",
        pdf_rel="06-naskah-ta/pdf/01-bab-1-pendahuluan/01-bab-1-pendahuluan.pdf",
        meta=DocumentMetadata(
            title="Bab I Pendahuluan - Deteksi Phishing WhatsApp Otoritas Perpajakan",
            subject="Bab I Pendahuluan Tugas Akhir - PJJ Sistem Informasi UNSIA",
            author="Wan Mirza Dhani",
            last_modified_by="Wan Mirza Dhani",
            keywords="Pendahuluan, Rumusan Masalah, Tujuan Penelitian, Metode",
            category="Naskah Tugas Akhir",
            description="Bab I Pendahuluan Tugas Akhir Wan Mirza Dhani (240101020194).",
            company="Universitas Siber Asia",
            revision=21,
            total_time_minutes=410,
            created=datetime(2026, 10, 30, 20, 42, 0, tzinfo=WIB),
            modified=datetime(2026, 11, 28, 11, 45, 0, tzinfo=WIB),
        ),
    ),
    DeliverableSpec(
        key="02-bab-2",
        md_rel="06-naskah-ta/md/02-bab-2-landasan-metode/02-bab-2-landasan-metode.md",
        docx_rel="06-naskah-ta/docx/02-bab-2-landasan-metode/02-bab-2-landasan-metode.docx",
        pdf_rel="06-naskah-ta/pdf/02-bab-2-landasan-metode/02-bab-2-landasan-metode.pdf",
        meta=DocumentMetadata(
            title="Bab II Landasan Metode - Deteksi Phishing WhatsApp Otoritas Perpajakan",
            subject="Bab II Landasan Metode Tugas Akhir - PJJ Sistem Informasi UNSIA",
            author="Wan Mirza Dhani",
            last_modified_by="Wan Mirza Dhani",
            keywords="LinearSVC, Random Forest, TF-IDF, Platt Scaling, TKT 6",
            category="Naskah Tugas Akhir",
            description="Bab II Landasan Metode Tugas Akhir Wan Mirza Dhani (240101020194).",
            company="Universitas Siber Asia",
            revision=19,
            total_time_minutes=385,
            created=datetime(2026, 11, 4, 19, 30, 0, tzinfo=WIB),
            modified=datetime(2026, 11, 28, 12, 5, 0, tzinfo=WIB),
        ),
    ),
    DeliverableSpec(
        key="03-bab-3",
        md_rel="06-naskah-ta/md/03-bab-3-implementasi-metode/03-bab-3-implementasi-metode.md",
        docx_rel="06-naskah-ta/docx/03-bab-3-implementasi-metode/03-bab-3-implementasi-metode.docx",
        pdf_rel="06-naskah-ta/pdf/03-bab-3-implementasi-metode/03-bab-3-implementasi-metode.pdf",
        meta=DocumentMetadata(
            title="Bab III Implementasi Metode Usulan - Deteksi Phishing WhatsApp Otoritas Perpajakan",
            subject="Bab III Implementasi Metode Tugas Akhir - PJJ Sistem Informasi UNSIA",
            author="Wan Mirza Dhani",
            last_modified_by="Wan Mirza Dhani",
            keywords="FastAPI, Manifest V3, Sastrawi, Kurasi Korpus, Pipeline ML",
            category="Naskah Tugas Akhir",
            description="Bab III Implementasi Metode Tugas Akhir Wan Mirza Dhani (240101020194).",
            company="Universitas Siber Asia",
            revision=24,
            total_time_minutes=430,
            created=datetime(2026, 11, 11, 20, 10, 0, tzinfo=WIB),
            modified=datetime(2026, 11, 28, 12, 20, 0, tzinfo=WIB),
        ),
    ),
    DeliverableSpec(
        key="04-bab-4",
        md_rel="06-naskah-ta/md/04-bab-4-hasil-dan-analisa/04-bab-4-hasil-dan-analisa.md",
        docx_rel="06-naskah-ta/docx/04-bab-4-hasil-dan-analisa/04-bab-4-hasil-dan-analisa.docx",
        pdf_rel="06-naskah-ta/pdf/04-bab-4-hasil-dan-analisa/04-bab-4-hasil-dan-analisa.pdf",
        meta=DocumentMetadata(
            title="Bab IV Hasil dan Analisa - Deteksi Phishing WhatsApp Otoritas Perpajakan",
            subject="Bab IV Hasil dan Analisa Tugas Akhir - PJJ Sistem Informasi UNSIA",
            author="Wan Mirza Dhani",
            last_modified_by="Wan Mirza Dhani",
            keywords="Brier Score, Platt Scaling, Keyword Bias, SHAP, TKT 6",
            category="Naskah Tugas Akhir",
            description="Bab IV Hasil dan Analisa Tugas Akhir Wan Mirza Dhani (240101020194).",
            company="Universitas Siber Asia",
            revision=27,
            total_time_minutes=495,
            created=datetime(2026, 11, 16, 19, 50, 0, tzinfo=WIB),
            modified=datetime(2026, 11, 28, 12, 40, 0, tzinfo=WIB),
        ),
    ),
    DeliverableSpec(
        key="05-bab-5",
        md_rel="06-naskah-ta/md/05-bab-5-kesimpulan/05-bab-5-kesimpulan.md",
        docx_rel="06-naskah-ta/docx/05-bab-5-kesimpulan/05-bab-5-kesimpulan.docx",
        pdf_rel="06-naskah-ta/pdf/05-bab-5-kesimpulan/05-bab-5-kesimpulan.pdf",
        meta=DocumentMetadata(
            title="Bab V Kesimpulan - Deteksi Phishing WhatsApp Otoritas Perpajakan",
            subject="Bab V Kesimpulan Tugas Akhir - PJJ Sistem Informasi UNSIA",
            author="Wan Mirza Dhani",
            last_modified_by="Wan Mirza Dhani",
            keywords="Kesimpulan, Saran, Tugas Akhir UNSIA",
            category="Naskah Tugas Akhir",
            description="Bab V Kesimpulan Tugas Akhir Wan Mirza Dhani (240101020194).",
            company="Universitas Siber Asia",
            revision=14,
            total_time_minutes=190,
            created=datetime(2026, 11, 20, 20, 5, 0, tzinfo=WIB),
            modified=datetime(2026, 11, 28, 12, 55, 0, tzinfo=WIB),
        ),
    ),
    DeliverableSpec(
        key="06-lampiran",
        md_rel="06-naskah-ta/md/06-lampiran/06-lampiran.md",
        docx_rel="06-naskah-ta/docx/06-lampiran/06-lampiran.docx",
        pdf_rel="06-naskah-ta/pdf/06-lampiran/06-lampiran.pdf",
        meta=DocumentMetadata(
            title="Daftar Pustaka dan Lampiran - Deteksi Phishing WhatsApp Otoritas Perpajakan",
            subject="Daftar Pustaka dan Lampiran Tugas Akhir - PJJ Sistem Informasi UNSIA",
            author="Wan Mirza Dhani",
            last_modified_by="Wan Mirza Dhani",
            keywords="Daftar Pustaka, IEEE, Lampiran, Pengujian, Matriks Literatur",
            category="Naskah Tugas Akhir",
            description="Daftar Pustaka dan Lampiran Tugas Akhir Wan Mirza Dhani (240101020194).",
            company="Universitas Siber Asia",
            revision=29,
            total_time_minutes=540,
            created=datetime(2026, 11, 8, 21, 0, 0, tzinfo=WIB),
            modified=datetime(2026, 11, 28, 13, 10, 0, tzinfo=WIB),
        ),
    ),
    DeliverableSpec(
        key="07-naskah-lengkap",
        md_rel="06-naskah-ta/md/07-naskah-lengkap/naskah-lengkap-tugas-akhir-ta-unsia.md",
        docx_rel="06-naskah-ta/docx/07-naskah-lengkap/naskah-lengkap-tugas-akhir-ta-unsia.docx",
        pdf_rel="06-naskah-ta/pdf/07-naskah-lengkap/naskah-lengkap-tugas-akhir-ta-unsia.pdf",
        meta=DocumentMetadata(
            title=(
                "Komparasi Algoritma Support Vector Machine dan Random Forest dalam "
                "Deteksi Pesan Phishing WhatsApp Mengatasnamakan Otoritas Perpajakan"
            ),
            subject="Naskah Lengkap Tugas Akhir Prototype - PJJ Sistem Informasi UNSIA",
            author="Wan Mirza Dhani",
            last_modified_by="Wan Mirza Dhani",
            keywords=(
                "Phishing, WhatsApp, Otoritas Perpajakan, Direktorat Jenderal Pajak, "
                "Support Vector Machine, LinearSVC, Random Forest, TF-IDF, Klasifikasi Teks"
            ),
            category="Naskah Tugas Akhir",
            description=(
                "Naskah Lengkap Tugas Akhir Prototype Program Studi PJJ Sistem Informasi "
                "Universitas Siber Asia oleh Wan Mirza Dhani (NIM 240101020194)."
            ),
            company="Universitas Siber Asia",
            revision=47,
            total_time_minutes=1260,
            created=datetime(2026, 10, 30, 20, 15, 0, tzinfo=WIB),
            modified=datetime(2026, 11, 28, 13, 35, 0, tzinfo=WIB),
        ),
    ),
    DeliverableSpec(
        key="08-glosarium",
        md_rel="06-naskah-ta/md/08-glosarium/glosarium-tugas-akhir-unsia.md",
        docx_rel=None,
        pdf_rel="06-naskah-ta/pdf/08-glosarium/glosarium-tugas-akhir-unsia.pdf",
        meta=DocumentMetadata(
            title="Glosarium Tugas Akhir - Deteksi Phishing WhatsApp Otoritas Perpajakan",
            subject="Panduan Istilah dan Sidang Tugas Akhir UNSIA",
            author="Wan Mirza Dhani",
            last_modified_by="Wan Mirza Dhani",
            keywords="Glosarium, Sidang TA, NLP, Phishing DJP",
            category="Naskah Tugas Akhir",
            description="Glosarium Istilah Tugas Akhir Wan Mirza Dhani (240101020194).",
            company="Universitas Siber Asia",
            revision=11,
            total_time_minutes=95,
            created=datetime(2026, 11, 22, 19, 30, 0, tzinfo=WIB),
            modified=datetime(2026, 11, 28, 13, 20, 0, tzinfo=WIB),
        ),
    ),
)


def export_deliverable(
    md_path: Path,
    out_docx: Path | None,
    out_pdf: Path | None,
    meta: DocumentMetadata,
) -> tuple[dict[str, int], list[dict[str, object]]]:
    """Build .docx, run Word COM + PDF export purely in non-OneDrive TEMP staging, then copy atomically."""
    stage_root = Path(tempfile.gettempdir()) / "unsia_docx_build" / uuid4().hex
    stage_root.mkdir(parents=True, exist_ok=True)
    stem = out_docx.stem if out_docx is not None else (out_pdf.stem if out_pdf else md_path.stem)
    stage_docx = stage_root / f"{stem}.docx"
    stage_pdf = stage_root / f"{stem}.pdf"

    try:
        build_unsia_docx_only(md_path, stage_docx)
        patch_docx_metadata(stage_docx, meta)
        word_stats, page_map = _run_word_com_on_local_stage(stage_docx, stage_pdf)
        patch_docx_metadata(stage_docx, meta, stats=word_stats)

        if out_docx is not None:
            out_docx.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(stage_docx, out_docx)
            set_file_timestamps(out_docx, meta.created, meta.modified)
        if out_pdf is not None:
            out_pdf.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(stage_pdf, out_pdf)
            set_file_timestamps(out_pdf, meta.modified, meta.modified)
        return word_stats, page_map
    finally:
        shutil.rmtree(stage_root, ignore_errors=True)


def export_by_keys(keys: Iterable[str]) -> dict[str, tuple[dict[str, int], list[dict[str, object]]]]:
    spec_map = {s.key: s for s in DELIVERABLE_SPECS}
    results: dict[str, tuple[dict[str, int], list[dict[str, object]]]] = {}
    for key in keys:
        if key not in spec_map:
            raise KeyError(f"Kunci berkas tidak dikenal: {key}")
        spec = spec_map[key]
        md_path = REPO_ROOT / spec.md_rel
        out_docx = (REPO_ROOT / spec.docx_rel) if spec.docx_rel else None
        out_pdf = REPO_ROOT / spec.pdf_rel
        stats, page_map = export_deliverable(md_path, out_docx, out_pdf, spec.meta)
        results[key] = (stats, page_map)
        print(
            f"[OK] {key}: pages={stats.get('Pages')}, words={stats.get('Words')} -> {out_pdf.name}"
        )
    return results


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Ekspor naskah TA UNSIA ke Word/PDF via staging lokal anti-OneDrive."
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Bangun ulang seluruh 9 berkas deliverables Tugas Akhir.",
    )
    parser.add_argument(
        "--only",
        nargs="+",
        choices=[s.key for s in DELIVERABLE_SPECS],
        help="Bangun berkas tertentu berdasarkan kunci.",
    )
    parser.add_argument(
        "--print-page-map",
        action="store_true",
        help="Cetak daftar halaman Heading/Gambar/Tabel setelah ekspor.",
    )
    args = parser.parse_args()

    if args.only:
        targets = args.only
    elif args.all:
        targets = [s.key for s in DELIVERABLE_SPECS]
    else:
        targets = ["07-naskah-lengkap"]

    results = export_by_keys(targets)
    if args.print_page_map:
        for key, (_, pmap) in results.items():
            print(f"\n=== PAGE MAP: {key} ===")
            for item in pmap:
                print(f"  p.{item['page']:>2} | {item['style']:<13} | {item['text']}")


if __name__ == "__main__":
    main()
