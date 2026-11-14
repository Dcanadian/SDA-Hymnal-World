#!/usr/bin/env python3
"""
Build the 7 Compiled Master PDF Books in Books/ with a 2-column Table of Contents,
clickable TOC entries, and complete PDF Outline Bookmarks for all 695 SDA Hymns.

Books generated:
1. Books/SDA Hymnal - Complete PDF Chords Book.pdf
2. Books/SDA Hymnal - Complete C Instruments Lead Sheets.pdf
3. Books/SDA Hymnal - Complete Bb Instruments Lead Sheets.pdf
4. Books/SDA Hymnal - Complete Eb Instruments Lead Sheets.pdf
5. Books/SDA Hymnal - Complete F Instruments Lead Sheets.pdf
6. Books/SDA Hymnal - Complete Bass Clef Lead Sheets.pdf
7. Books/SDA Hymnal - Complete Alto Clef Lead Sheets.pdf
"""

import glob
import json
import math
import re
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
import fitz

ROOT_DIR = Path("/home/antigravity/SDA-Hymnal")
DB_DIR = ROOT_DIR / "Database"
BOOKS_DIR = ROOT_DIR / "Books"
BOOKS_DIR.mkdir(parents=True, exist_ok=True)

BOOK_CONFIGS = [
    ("SDA Hymnal - Complete PDF Chords Book.pdf", "Complete PDF Chords Book", ROOT_DIR / "Chords" / "PDF-Chords"),
    ("SDA Hymnal - Complete C Instruments Lead Sheets.pdf", "C Instruments Lead Sheets", ROOT_DIR / "Sheet-Music" / "Lead-Sheets" / "C-Concert-Treble"),
    ("SDA Hymnal - Complete Bb Instruments Lead Sheets.pdf", "B-Flat Instruments Lead Sheets", ROOT_DIR / "Sheet-Music" / "Lead-Sheets" / "Bb-Instruments"),
    ("SDA Hymnal - Complete Eb Instruments Lead Sheets.pdf", "E-Flat Instruments Lead Sheets", ROOT_DIR / "Sheet-Music" / "Lead-Sheets" / "Eb-Instruments"),
    ("SDA Hymnal - Complete F Instruments Lead Sheets.pdf", "F Instruments Lead Sheets", ROOT_DIR / "Sheet-Music" / "Lead-Sheets" / "F-Instruments"),
    ("SDA Hymnal - Complete Bass Clef Lead Sheets.pdf", "Bass Clef Lead Sheets", ROOT_DIR / "Sheet-Music" / "Lead-Sheets" / "Bass-Clef"),
    ("SDA Hymnal - Complete Alto Clef Lead Sheets.pdf", "Alto Clef Lead Sheets", ROOT_DIR / "Sheet-Music" / "Lead-Sheets" / "Alto-Clef"),
]


def build_single_book(cfg):
    filename, subtitle, src_dir = cfg
    pdf_files = sorted(glob.glob(str(src_dir / "[0-9][0-9][0-9]*.pdf")))
    if not pdf_files:
        return filename, False, f"No PDFs found in {src_dir}"

    entries = []
    for pf in pdf_files:
        stem = Path(pf).stem
        entries.append((stem, pf))

    items_per_col = 45
    items_per_page = items_per_col * 2  # 90 per page -> 8 TOC pages for 695 hymns
    num_toc_pages = int(math.ceil(len(entries) / items_per_page))

    # First pass: determine starting page number (1-indexed in final document) for each hymn
    cur_doc_page = num_toc_pages + 1
    hymn_pages = []
    body_doc = fitz.open()
    for stem, pf in entries:
        sub = fitz.open(pf)
        p_count = len(sub)
        hymn_pages.append((stem, cur_doc_page))
        body_doc.insert_pdf(sub)
        sub.close()
        cur_doc_page += p_count

    # Create TOC document with clickable links
    toc_doc = fitz.open()
    page_w, page_h = 612, 792  # Letter size
    link_specs = []  # (toc_page_idx, rect, target_doc_page_0_indexed)

    for p_idx in range(num_toc_pages):
        page = toc_doc.new_page(width=page_w, height=page_h)
        # Header
        page.insert_text(
            fitz.Point(44, 46),
            "THE SEVENTH-DAY ADVENTIST HYMNAL",
            fontname="tiro",
            fontsize=11,
        )
        page.insert_text(
            fitz.Point(page_w - 44 - fitz.get_text_length(f"TOC {p_idx + 1}/{num_toc_pages}", fontname="tiro", fontsize=10), 46),
            f"TOC {p_idx + 1}/{num_toc_pages}",
            fontname="tiro",
            fontsize=10,
        )
        title_str = f"{subtitle} — Table of Contents"
        tw = fitz.get_text_length(title_str, fontname="tibo", fontsize=16)
        page.insert_text(
            fitz.Point((page_w - tw) / 2, 70),
            title_str,
            fontname="tibo",
            fontsize=16,
        )

        chunk = hymn_pages[p_idx * items_per_page : (p_idx + 1) * items_per_page]
        for i, (stem, target_page_1idx) in enumerate(chunk):
            col = 0 if i < items_per_col else 1
            row = i % items_per_col
            x0 = 44 if col == 0 else 318
            x_end = 294 if col == 0 else 568
            y = 100 + row * 14.5

            disp = stem if len(stem) <= 38 else stem[:36] + "..."
            p_str = str(target_page_1idx)
            pw = fitz.get_text_length(p_str, fontname="tiro", fontsize=8.5)

            page.insert_text(fitz.Point(x0, y), disp, fontname="tiro", fontsize=8.5)
            page.insert_text(fitz.Point(x_end - pw, y), p_str, fontname="tiro", fontsize=8.5)

            rect = fitz.Rect(x0, y - 9, x_end, y + 3)
            link_specs.append((p_idx, rect, target_page_1idx - 1))

    # Merge body into toc_doc
    toc_doc.insert_pdf(body_doc)
    body_doc.close()

    # Add clickable links on TOC pages
    for toc_p_idx, rect, target_p_0idx in link_specs:
        toc_doc[toc_p_idx].insert_link({
            "kind": fitz.LINK_GOTO,
            "from": rect,
            "page": target_p_0idx,
        })

    # Add PDF outline bookmarks
    toc_outline = [[1, "Table of Contents", 1]]
    for stem, target_page_1idx in hymn_pages:
        toc_outline.append([1, stem, target_page_1idx])
    toc_doc.set_toc(toc_outline)

    out_path = BOOKS_DIR / filename
    toc_doc.save(str(out_path), garbage=4, deflate=True)
    total_pages = len(toc_doc)
    toc_doc.close()
    size_mb = out_path.stat().st_size / (1024 * 1024)
    return filename, True, f"{total_pages} pages ({size_mb:.1f} MB)"


def main():
    print(f"Building {len(BOOK_CONFIGS)} Master Hymnal PDF Books in {BOOKS_DIR}...")
    with ProcessPoolExecutor(max_workers=4) as ex:
        futs = [ex.submit(build_single_book, cfg) for cfg in BOOK_CONFIGS]
        for fut in as_completed(futs):
            fname, ok, info = fut.result()
            status = "OK" if ok else "ERROR"
            print(f"  [{status}] {fname}: {info}")


if __name__ == "__main__":
    main()
