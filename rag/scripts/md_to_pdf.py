#!/usr/bin/env python3
"""Convert RAG markdown documents to PDF files."""

from __future__ import annotations

import re
from pathlib import Path

from fpdf import FPDF


ROOT = Path(__file__).resolve().parents[1] / "documents"
PDF_ROOT = Path(__file__).resolve().parents[1] / "documents-pdf"


class DocPDF(FPDF):
    def __init__(self, title: str):
        super().__init__(format="A4")
        self.doc_title = title
        self.set_auto_page_break(auto=True, margin=18)
        self.set_margins(16, 16, 16)

    def header(self) -> None:
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(90, 90, 90)
        self.cell(0, 6, self.doc_title[:90], align="L")
        self.ln(8)
        self.set_draw_color(180, 180, 180)
        self.line(16, self.get_y(), self.w - 16, self.get_y())
        self.ln(4)
        self.set_text_color(0, 0, 0)

    def footer(self) -> None:
        self.set_y(-14)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(110, 110, 110)
        self.cell(0, 8, f"Page {self.page_no()}/{{nb}}", align="C")
        self.set_text_color(0, 0, 0)


def sanitize(text: str) -> str:
    replacements = {
        "\u2014": "-",
        "\u2013": "-",
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2022": "-",
        "\u00a0": " ",
        "\u2192": "->",
        "\u2264": "<=",
        "\u2265": ">=",
        "\u00b0": " deg",
        "\u2011": "-",
        "\u2026": "...",
    }
    for src, dst in replacements.items():
        text = text.replace(src, dst)
    # Keep latin-1 compatible content for core Helvetica fonts.
    return text.encode("latin-1", "replace").decode("latin-1")


def strip_md_inline(text: str) -> str:
    text = re.sub(r"!\[([^\]]*)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = text.replace("**", "").replace("__", "").replace("`", "")
    return sanitize(text)


def extract_title(md: str, fallback: str) -> str:
    for line in md.splitlines():
        if line.startswith("# "):
            return strip_md_inline(line[2:].strip())
    return fallback


def reset_x(pdf: DocPDF) -> None:
    pdf.set_x(pdf.l_margin)


def write_wrapped(pdf: DocPDF, text: str, size: int = 11, style: str = "") -> None:
    reset_x(pdf)
    pdf.set_font("Helvetica", style, size)
    pdf.multi_cell(0, 5.5 if size <= 11 else 7, text)
    pdf.ln(1)
    reset_x(pdf)


def write_table(pdf: DocPDF, rows: list[list[str]]) -> None:
    if not rows:
        return
    usable = pdf.w - pdf.l_margin - pdf.r_margin
    cols = max(len(r) for r in rows)
    col_w = usable / cols
    pdf.set_font("Helvetica", "", 8)
    line_h = 4.5
    for i, row in enumerate(rows):
        cells = (row + [""] * cols)[:cols]
        max_lines = 1
        for cell in cells:
            approx = max(1, int(len(cell) / max(1, int(col_w / 1.7))))
            max_lines = max(max_lines, approx, 1 + cell.count("\n"))
        row_h = min(max_lines, 8) * line_h + 1
        if pdf.get_y() + row_h > pdf.page_break_trigger:
            pdf.add_page()
            reset_x(pdf)
        y0 = pdf.get_y()
        x0 = pdf.l_margin
        for j, cell in enumerate(cells):
            x = x0 + j * col_w
            pdf.set_xy(x, y0)
            if i == 0:
                pdf.set_font("Helvetica", "B", 8)
                pdf.set_fill_color(230, 235, 240)
            else:
                pdf.set_font("Helvetica", "", 8)
                pdf.set_fill_color(248, 248, 248)
            pdf.rect(x, y0, col_w, row_h, style="DF")
            pdf.set_xy(x + 0.8, y0 + 0.6)
            pdf.multi_cell(col_w - 1.6, line_h, cell)
        pdf.set_xy(pdf.l_margin, y0 + row_h)
    pdf.ln(2)
    reset_x(pdf)


def parse_table_block(lines: list[str], start: int) -> tuple[list[list[str]], int]:
    rows: list[list[str]] = []
    i = start
    while i < len(lines) and lines[i].strip().startswith("|"):
        raw = lines[i].strip()
        if re.match(r"^\|?\s*:?-{3,}", raw.replace("|", " ").strip()) or set(raw.replace("|", "").replace(":", "").replace("-", "").replace(" ", "")) == set():
            # separator row like |---|---|
            if re.search(r"-{3,}", raw):
                i += 1
                continue
        cells = [strip_md_inline(c.strip()) for c in raw.strip("|").split("|")]
        rows.append(cells)
        i += 1
    return rows, i


def md_to_pdf(md_path: Path, pdf_path: Path) -> None:
    text = md_path.read_text(encoding="utf-8")
    title = extract_title(text, md_path.stem)
    pdf = DocPDF(title=title)
    pdf.alias_nb_pages()
    pdf.add_page()

    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            pdf.ln(2)
            i += 1
            continue

        if stripped == "---":
            pdf.ln(1)
            y = pdf.get_y()
            pdf.set_draw_color(160, 160, 160)
            pdf.line(pdf.l_margin, y, pdf.w - pdf.r_margin, y)
            pdf.ln(3)
            i += 1
            continue

        if stripped.startswith("|"):
            rows, i = parse_table_block(lines, i)
            write_table(pdf, rows)
            continue

        if stripped.startswith("# "):
            write_wrapped(pdf, strip_md_inline(stripped[2:]), size=16, style="B")
            i += 1
            continue
        if stripped.startswith("## "):
            pdf.ln(2)
            write_wrapped(pdf, strip_md_inline(stripped[3:]), size=13, style="B")
            i += 1
            continue
        if stripped.startswith("### "):
            write_wrapped(pdf, strip_md_inline(stripped[4:]), size=11, style="B")
            i += 1
            continue

        if re.match(r"^[-*]\s+", stripped):
            bullet = strip_md_inline(re.sub(r"^[-*]\s+", "", stripped))
            reset_x(pdf)
            pdf.set_font("Helvetica", "", 11)
            pdf.multi_cell(0, 5.5, f"  - {bullet}")
            reset_x(pdf)
            i += 1
            continue

        if re.match(r"^\d+\.\s+", stripped):
            item = strip_md_inline(re.sub(r"^\d+\.\s+", "", stripped))
            num = re.match(r"^(\d+)\.\s+", stripped).group(1)
            reset_x(pdf)
            pdf.set_font("Helvetica", "", 11)
            pdf.multi_cell(0, 5.5, f"  {num}. {item}")
            reset_x(pdf)
            i += 1
            continue

        # paragraph: gather continued plain lines
        para = [strip_md_inline(stripped)]
        i += 1
        while i < len(lines):
            nxt = lines[i].strip()
            if (
                not nxt
                or nxt.startswith("#")
                or nxt.startswith("|")
                or nxt == "---"
                or re.match(r"^[-*]\s+", nxt)
                or re.match(r"^\d+\.\s+", nxt)
            ):
                break
            para.append(strip_md_inline(nxt))
            i += 1
        write_wrapped(pdf, " ".join(para), size=11, style="")

    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(pdf_path))


def main() -> None:
    md_files = sorted(
        p for p in ROOT.rglob("*.md") if p.name != "README.md"
    )
    if not md_files:
        raise SystemExit(f"No markdown files found under {ROOT}")

    PDF_ROOT.mkdir(parents=True, exist_ok=True)
    created = []
    for md in md_files:
        rel = md.relative_to(ROOT)
        pdf = PDF_ROOT / rel.with_suffix(".pdf")
        md_to_pdf(md, pdf)
        created.append(pdf)
        print(f"Created {pdf.relative_to(PDF_ROOT.parent)}")

    print(f"\nDone: {len(created)} PDF files in {PDF_ROOT}")


if __name__ == "__main__":
    main()
