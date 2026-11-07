#!/usr/bin/env python3
"""
Multi-Format Compiler for the Seventh-day Adventist Hymnal (1985).
Compiles canonical JSON files from Database/ into:
  1. ChordPro/      (.cho standard ChordPro + 000 - SDA Hymnal Master.cho)
  2. JustChords/    (.cho JustChords native syntax + 000 - SDA Hymnal JustChords Master.cho)
  3. PlainText/     (.txt Chords-Over-Lyrics space-aligned above syllables, no word hyphens)
  4. OnSong/        (.onsong OnSong format)
  5. OpenLyrics/    (.xml OpenLyrics 0.9 XML with <chord> tags)
  6. PDF-Chords/    (.pdf Clean Modern Worship Chart 1-page vector PDF)
"""

import html
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple

ROOT_DIR = Path("/home/antigravity/SDA-Hymnal")
DB_DIR = ROOT_DIR / "Database"

CHORD_RE = re.compile(r"\[([^\]]+)\]")


def parse_inline_line(line: str) -> List[Tuple[str, str]]:
    """
    Parse an inline ChordPro line like:
      "[F]Praise to [Dm]the [C]Lord, the [F/A]Al[F/C]might[Dm7]y,"
    into a list of (chord, text_segment) pairs.
    """
    segments: List[Tuple[str, str]] = []
    pos = 0
    current_chord = ""
    for m in CHORD_RE.finditer(line):
        start, end = m.span()
        if start > pos or current_chord:
            text_part = line[pos:start]
            segments.append((current_chord, text_part))
        current_chord = m.group(1)
        pos = end
    tail = line[pos:]
    if current_chord or tail:
        segments.append((current_chord, tail))
    return segments


def inline_to_chords_over_lyrics(line: str) -> Tuple[str, str]:
    """
    Convert an inline ChordPro line into a (chord_line, lyric_line) pair
    for PlainText (.txt) Chords-Over-Lyrics output.
    Never inserts hyphens or spaces inside words: if chords inside a word are
    wider than the syllables beneath them, the word remains 100% contiguous and
    any extra width is absorbed by padding at the next space/word boundary.
    """
    segments = parse_inline_line(line)
    chord_chars: List[str] = []
    lyric_chars: List[str] = []

    for chord, text in segments:
        cur_c_len = len("".join(chord_chars))
        cur_l_len = len("".join(lyric_chars))
        at_word_boundary = (cur_l_len == 0) or ("".join(lyric_chars).endswith(" "))

        if at_word_boundary:
            if cur_c_len > cur_l_len:
                lyric_chars.append(" " * (cur_c_len - cur_l_len))
            elif cur_l_len > cur_c_len:
                chord_chars.append(" " * (cur_l_len - cur_c_len))
        else:
            # Mid-word: never split the word with spaces!
            if cur_l_len > cur_c_len:
                chord_chars.append(" " * (cur_l_len - cur_c_len))

        if chord:
            c_str = "".join(chord_chars)
            if c_str and not c_str.endswith(" "):
                chord_chars.append(" ")
                if at_word_boundary:
                    lyric_chars.append(" ")
            chord_chars.append(chord)

        # If text contains a space and chord_chars is currently ahead of lyric_chars,
        # pad at the first space inside `text` so the following word syncs cleanly.
        if " " in text:
            first_sp = text.index(" ")
            word_tail = text[:first_sp + 1]
            rest = text[first_sp + 1:]
            lyric_chars.append(word_tail)
            cur_c_len2 = len("".join(chord_chars))
            cur_l_len2 = len("".join(lyric_chars))
            if cur_c_len2 > cur_l_len2:
                lyric_chars.append(" " * (cur_c_len2 - cur_l_len2))
            lyric_chars.append(rest)
        else:
            lyric_chars.append(text)

    chord_line = "".join(chord_chars).rstrip()
    lyric_line = "".join(lyric_chars).rstrip()
    return chord_line, lyric_line


def generate_chordpro(h: Dict) -> str:
    """Generate standard ChordPro (.cho) content."""
    num_str = f"{h['number']:03d}"
    lines = [
        f"{{title: {num_str} - {h['title']}}}",
        f"{{subtitle: SDA Hymnal #{num_str} • {h['tune']}}}",
        f"{{lyricist: {h['lyricist']}}}",
        f"{{composer: {h['composer']}}}",
        f"{{key: {h['key']}}}",
        f"{{time: {h['time']}}}",
        f"{{tempo: {h['tempo']}}}",
        f"{{meta: hymn_number {h['number']}}}",
        f"{{meta: category {h['category']} - {h['subcategory']}}}",
        ""
    ]
    for sec in h["sections"]:
        sec_type = sec.get("type", "verse")
        sec_name = sec["name"]
        if sec_type == "chorus":
            lines.append(f"{{start_of_chorus: {sec_name}}}")
            lines.extend(sec["lines"])
            lines.append("{end_of_chorus}")
        else:
            lines.append(f"{{start_of_verse: {sec_name}}}")
            lines.extend(sec["lines"])
            lines.append("{end_of_verse}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def generate_justchords(h: Dict) -> str:
    """
    Generate native JustChords (.cho) content following the JustChords SongEditor spec:
    - Metadata directives in curly braces at top
    - Sections separated by an empty line
    - Section label on its own line ending with a colon (e.g., 'Verse 1:', 'Refrain:')
    - Inline [Chord]syllable notation with no mid-word hyphens
    """
    num_str = f"{h['number']:03d}"
    lines = [
        f"{{title: {num_str} - {h['title']}}}",
        f"{{artist: Seventh-day Adventist Hymnal}}",
        f"{{lyricist: {h['lyricist']}}}",
        f"{{composer: {h['composer']}}}",
        f"{{key: {h['key']}}}",
        f"{{time: {h['time']}}}",
        f"{{tempo: {h['tempo']}}}",
        f"{{tag: {h['category']}}}",
        f"{{tag: {h['subcategory']}}}",
        ""
    ]
    for sec in h["sections"]:
        lines.append(f"{sec['name']}:")
        lines.extend(sec["lines"])
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def generate_plaintext(h: Dict) -> str:
    """Generate Chords-Over-Lyrics PlainText (.txt) content."""
    num_str = f"{h['number']:03d}"
    header_title = f"{num_str} - {h['title']}"
    meta_line = (
        f"Key: {h['key']}  |  Time: {h['time']}  |  Tempo: {h['tempo']} BPM  |  "
        f"Tune: {h['tune']}"
    )
    credits_line = f"Words: {h['lyricist']}  |  Music: {h['composer']}"
    sep = "=" * max(len(header_title), len(meta_line), len(credits_line))

    lines = [
        header_title,
        credits_line,
        meta_line,
        sep,
        ""
    ]
    for sec in h["sections"]:
        lines.append(f"[{sec['name']}]")
        for inline_line in sec["lines"]:
            c_line, l_line = inline_to_chords_over_lyrics(inline_line)
            if c_line.strip():
                lines.append(c_line)
            lines.append(l_line)
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def generate_onsong(h: Dict) -> str:
    """Generate OnSong (.onsong) file content."""
    num_str = f"{h['number']:03d}"
    lines = [
        f"{num_str} - {h['title']}",
        f"{h['lyricist']} / {h['composer']}",
        f"Key: {h['key']}",
        f"Time: {h['time']}",
        f"Tempo: {h['tempo']}",
        f"Number: {h['number']}",
        f"Topic: {h['category']} - {h['subcategory']}",
        ""
    ]
    for sec in h["sections"]:
        lines.append(f"{sec['name']}:")
        lines.extend(sec["lines"])
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def generate_openlyrics(h: Dict) -> str:
    """Generate OpenLyrics 0.9 XML (.xml) with inline <chord name="..."/> elements."""
    num_str = f"{h['number']:03d}"
    verse_order = []
    verses_xml = []

    for idx, sec in enumerate(h["sections"], start=1):
        sec_type = sec.get("type", "verse")
        if sec_type == "chorus":
            v_name = "c1"
        else:
            # Extract number from "Verse N"
            m = re.search(r"(\d+)", sec["name"])
            v_name = f"v{m.group(1)}" if m else f"v{idx}"
        verse_order.append(v_name)

        xml_lines = []
        for inline_line in sec["lines"]:
            segs = parse_inline_line(inline_line)
            parts = []
            for chord, text in segs:
                if chord:
                    parts.append(f'<chord name="{html.escape(chord)}"/>')
                if text:
                    parts.append(html.escape(text))
            xml_lines.append("".join(parts))

        joined_lines = "<br/>\n      ".join(xml_lines)
        verses_xml.append(
            f'    <verse name="{v_name}">\n'
            f'      <lines>\n'
            f'      {joined_lines}\n'
            f'      </lines>\n'
            f'    </verse>'
        )

    order_str = " ".join(verse_order)
    verses_block = "\n".join(verses_xml)
    return f"""<?xml version='1.0' encoding='UTF-8'?>
<song xmlns="http://openlyrics.info/namespace/2009/song" version="0.9">
  <properties>
    <titles>
      <title>{html.escape(f"{num_str} - {h['title']}")}</title>
      <title>{html.escape(h['title'])}</title>
    </titles>
    <authors>
      <author type="words">{html.escape(h['lyricist'])}</author>
      <author type="music">{html.escape(h['composer'])}</author>
    </authors>
    <songbooks>
      <songbook name="Seventh-day Adventist Hymnal" entry="{h['number']}"/>
    </songbooks>
    <key>{html.escape(h['key'])}</key>
    <tempo type="bpm">{h['tempo']}</tempo>
    <timeSignature>{html.escape(h['time'])}</timeSignature>
    <verseOrder>{order_str}</verseOrder>
    <themes>
      <theme>{html.escape(h['category'])}</theme>
      <theme>{html.escape(h['subcategory'])}</theme>
    </themes>
  </properties>
  <lyrics>
{verses_block}
  </lyrics>
</song>
"""


# ============================================================================
# Native Vector PDF 1.4 Generator for Clean Modern Worship Charts (1-Page)
# ============================================================================

# Approximate proportional character widths (in 1/1000 em) for Helvetica / Helvetica-Bold
CHAR_WIDTHS = {
    " ": 278, "!": 278, "\"": 355, "#": 556, "$": 556, "%": 889, "&": 667, "'": 222,
    "(": 333, ")": 333, "*": 389, "+": 584, ",": 278, "-": 333, ".": 278, "/": 278,
    "0": 556, "1": 556, "2": 556, "3": 556, "4": 556, "5": 556, "6": 556, "7": 556,
    "8": 556, "9": 556, ":": 278, ";": 278, "<": 584, "=": 584, ">": 584, "?": 556,
    "@": 1015, "A": 667, "B": 667, "C": 722, "D": 722, "E": 667, "F": 611, "G": 778,
    "H": 722, "I": 278, "J": 500, "K": 667, "L": 556, "M": 833, "N": 722, "O": 778,
    "P": 667, "Q": 778, "R": 722, "S": 667, "T": 611, "U": 722, "V": 667, "W": 944,
    "X": 667, "Y": 667, "Z": 611, "[": 278, "\\": 278, "]": 278, "^": 469, "_": 556,
    "a": 556, "b": 556, "c": 500, "d": 556, "e": 556, "f": 278, "g": 556, "h": 556,
    "i": 222, "j": 222, "k": 500, "l": 222, "m": 833, "n": 556, "o": 556, "p": 556,
    "q": 556, "r": 333, "s": 500, "t": 278, "u": 556, "v": 500, "w": 722, "x": 500,
    "y": 500, "z": 500
}


def text_width_pt(text: str, font_size: float, bold: bool = False) -> float:
    scale = 1.04 if bold else 1.0
    total = sum(CHAR_WIDTHS.get(ch, 556) for ch in text)
    return (total / 1000.0) * font_size * scale


def pdf_escape(text: str) -> str:
    """Convert Unicode punctuation to WinAnsi-safe equivalents and escape PDF parens."""
    replacements = {
        "—": "-", "–": "-", "’": "'", "‘": "'", "“": '"', "”": '"', "•": "-",
        "À": "A", "Ö": "O", "Ü": "U", "à": "a", "ö": "o", "ü": "u", "é": "e"
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def generate_pdf_chart(h: Dict, out_path: Path) -> None:
    """
    Render a 1-page US Letter (612 x 792 pt) Clean Modern Worship Chart PDF.
    Automatically selects 1-column or 2-column layout and scales font size
    so all verses and refrains fit on a single page with crisp proportional
    chord-above-syllable alignment and zero mid-word hyphens.
    """
    PAGE_W, PAGE_H = 612.0, 792.0
    MARGIN_X = 38.0
    TOP_Y = PAGE_H - 36.0
    BOTTOM_Y = 34.0

    num_str = f"{h['number']:03d}"
    sections = h["sections"]
    total_lines = sum(len(s["lines"]) for s in sections)
    max_line_chars = max(
        len(CHORD_RE.sub("", ln)) for s in sections for ln in s["lines"]
    )

    # Decide 1-column vs 2-column layout to fit cleanly on 1 page
    use_two_cols = (total_lines >= 20 and len(sections) >= 3)

    if use_two_cols:
        lyric_size = 9.2 if max_line_chars > 46 else 9.6
        chord_size = 8.4 if max_line_chars > 46 else 8.8
        sec_title_size = 9.8
        line_pair_h = 21.5 if total_lines <= 28 else 19.5
        sec_gap = 9.0
    else:
        # Scale single-column density so all lines fit comfortably above the footer
        if total_lines <= 14:
            lyric_size = 11.2
            chord_size = 10.2
            sec_title_size = 11.2
            line_pair_h = 27.5
            sec_gap = 14.0
        elif total_lines <= 19:
            lyric_size = 10.5
            chord_size = 9.6
            sec_title_size = 10.6
            line_pair_h = 25.0
            sec_gap = 11.5
        else:
            lyric_size = 9.6
            chord_size = 8.8
            sec_title_size = 9.8
            line_pair_h = 21.0
            sec_gap = 8.5

    ops: List[str] = []

    # 1. Header Banner Background & Hymn Number Badge
    # Subtle slate header card
    ops.append("0.96 0.97 0.99 rg")
    ops.append(f"{MARGIN_X:.1f} {TOP_Y - 54:.1f} {PAGE_W - 2*MARGIN_X:.1f} 54 re f")

    # Dark Navy Hymn Number Box on left
    ops.append("0.11 0.21 0.36 rg")
    ops.append(f"{MARGIN_X:.1f} {TOP_Y - 54:.1f} 58 54 re f")

    # Hymn Number in white inside badge
    ops.append("1 1 1 rg")
    num_w = text_width_pt(num_str, 20.0, bold=True)
    num_x = MARGIN_X + (58.0 - num_w) / 2.0
    ops.append(f"BT /F2 20 Tf {num_x:.2f} {TOP_Y - 34:.2f} Td ({pdf_escape(num_str)}) Tj ET")
    ops.append(f"BT /F1 6.5 Tf {MARGIN_X + 10:.2f} {TOP_Y - 46:.2f} Td (SDA HYMNAL) Tj ET")

    # Song Title & Credits (fit within available width before badges)
    title_x = MARGIN_X + 68.0
    avail_header_w = (PAGE_W - MARGIN_X - 168.0) - title_x
    title_font_sz = 16.0
    while text_width_pt(h["title"], title_font_sz, bold=True) > avail_header_w and title_font_sz > 11.5:
        title_font_sz -= 0.5

    ops.append("0.08 0.13 0.22 rg")
    ops.append(f"BT /F2 {title_font_sz:.1f} Tf {title_x:.2f} {TOP_Y - 22:.2f} Td ({pdf_escape(h['title'])}) Tj ET")

    ops.append("0.32 0.38 0.46 rg")
    credits_str = f"Words: {h['lyricist']}  |  Music: {h['composer']} ({h['tune']})"
    cred_font_sz = 8.2
    while text_width_pt(credits_str, cred_font_sz, bold=False) > avail_header_w and cred_font_sz > 6.4:
        cred_font_sz -= 0.3
    ops.append(f"BT /F1 {cred_font_sz:.1f} Tf {title_x:.2f} {TOP_Y - 36:.2f} Td ({pdf_escape(credits_str)}) Tj ET")

    cat_str = f"{h['category']} - {h['subcategory']}"
    ops.append(f"BT /F3 7.8 Tf {title_x:.2f} {TOP_Y - 48:.2f} Td ({pdf_escape(cat_str)}) Tj ET")

    # Right-side Key / Time / Tempo Badges
    badge_right = PAGE_W - MARGIN_X - 8.0
    badges = [
        ("TEMPO", f"{h['tempo']} BPM", 58.0, (0.91, 0.94, 0.98), (0.15, 0.28, 0.48)),
        ("TIME", h["time"], 44.0, (0.91, 0.94, 0.98), (0.15, 0.28, 0.48)),
        ("KEY", h["key"], 46.0, (0.11, 0.29, 0.56), (1.0, 1.0, 1.0)),
    ]
    cur_bx = badge_right
    for b_label, b_val, b_w, bg_rgb, fg_rgb in badges:
        cur_bx -= b_w
        ops.append(f"{bg_rgb[0]:.2f} {bg_rgb[1]:.2f} {bg_rgb[2]:.2f} rg")
        ops.append(f"{cur_bx:.1f} {TOP_Y - 45:.1f} {b_w:.1f} 36 re f")
        ops.append(f"{fg_rgb[0]:.2f} {fg_rgb[1]:.2f} {fg_rgb[2]:.2f} rg")
        lbl_w = text_width_pt(b_label, 6.2, bold=True)
        val_w = text_width_pt(b_val, 11.0, bold=True)
        ops.append(
            f"BT /F2 6.2 Tf {cur_bx + (b_w - lbl_w)/2:.2f} {TOP_Y - 19:.2f} Td ({pdf_escape(b_label)}) Tj ET"
        )
        ops.append(
            f"BT /F2 11.0 Tf {cur_bx + (b_w - val_w)/2:.2f} {TOP_Y - 36:.2f} Td ({pdf_escape(b_val)}) Tj ET"
        )
        cur_bx -= 5.0

    # Bottom accent line under header
    ops.append("0.11 0.29 0.56 RG 1.2 w")
    ops.append(f"{MARGIN_X:.1f} {TOP_Y - 54:.1f} m {PAGE_W - MARGIN_X:.1f} {TOP_Y - 54:.1f} l S")

    # 2. Render Sections & Chords-Over-Lyrics Body
    body_top_y = TOP_Y - 72.0
    col_w = (PAGE_W - 2 * MARGIN_X - 24.0) / 2.0 if use_two_cols else (PAGE_W - 2 * MARGIN_X)

    # Split sections across columns if 2-column
    if use_two_cols:
        half = (len(sections) + 1) // 2
        col_groups = [(MARGIN_X, sections[:half]), (MARGIN_X + col_w + 24.0, sections[half:])]
    else:
        col_groups = [(MARGIN_X, sections)]

    for col_x, sec_list in col_groups:
        cur_y = body_top_y
        for sec in sec_list:
            is_chorus = sec.get("type") == "chorus"
            sec_x = col_x + (12.0 if is_chorus else 0.0)

            # Section Header Pill / Label
            sec_title_h = sec_title_size + 5.0
            if is_chorus:
                # Left vertical accent bar for Refrain/Chorus
                total_sec_h = sec_title_h + len(sec["lines"]) * line_pair_h + 4.0
                ops.append("0.97 0.98 1.00 rg")
                ops.append(f"{sec_x - 6:.1f} {cur_y - total_sec_h + 8:.1f} {col_w - 6:.1f} {total_sec_h:.1f} re f")
                ops.append("0.16 0.38 0.72 rg")
                ops.append(f"{sec_x - 6:.1f} {cur_y - total_sec_h + 8:.1f} 2.5 {total_sec_h:.1f} re f")

            ops.append("0.14 0.26 0.45 rg")
            ops.append(
                f"BT /F2 {sec_title_size:.1f} Tf {sec_x:.2f} {cur_y - sec_title_size:.2f} Td "
                f"({pdf_escape(sec['name'].upper())}) Tj ET"
            )
            cur_y -= (sec_title_size + 6.0)

            for inline_line in sec["lines"]:
                segs = parse_inline_line(inline_line)
                chord_y = cur_y - chord_size
                lyric_y = chord_y - lyric_size - 1.5

                # Position each segment proportionally so chords never collide
                # and never insert hyphens into words!
                cur_x = sec_x
                min_next_chord_x = sec_x
                lyric_pieces: List[Tuple[float, str]] = []
                chord_pieces: List[Tuple[float, str]] = []

                for chord, text in segs:
                    if chord:
                        # Ensure this chord does not overlap the previous chord
                        if cur_x < min_next_chord_x:
                            # If we are at a word boundary (previous text ended with space or empty),
                            # shift cur_x so the word also aligns under the chord;
                            # if mid-word, keep word contiguous and only nudge the chord slightly!
                            if not lyric_pieces or lyric_pieces[-1][1].endswith(" "):
                                cur_x = min_next_chord_x
                        c_x = max(cur_x, min_next_chord_x)
                        chord_pieces.append((c_x, chord))
                        c_w = text_width_pt(chord, chord_size, bold=True)
                        min_next_chord_x = c_x + c_w + 5.0

                    if text:
                        lyric_pieces.append((cur_x, text))
                        cur_x += text_width_pt(text, lyric_size, bold=False)

                # Guard against overflowing column width in 2-column mode
                line_span = max(cur_x, min_next_chord_x) - sec_x
                max_span = col_w - (18.0 if is_chorus else 6.0)
                h_scale = min(1.0, max_span / line_span) if line_span > 0 else 1.0
                eff_chord_sz = chord_size * h_scale
                eff_lyric_sz = lyric_size * h_scale

                # Draw chords in bold navy blue
                ops.append("0.11 0.32 0.68 rg")
                for c_x, c_str in chord_pieces:
                    adj_cx = sec_x + (c_x - sec_x) * h_scale
                    ops.append(
                        f"BT /F2 {eff_chord_sz:.2f} Tf {adj_cx:.2f} {chord_y:.2f} Td ({pdf_escape(c_str)}) Tj ET"
                    )

                # Draw lyric segments in crisp dark charcoal
                ops.append("0.10 0.12 0.16 rg")
                font_tag = "/F3" if is_chorus else "/F1"
                for l_x, l_str in lyric_pieces:
                    adj_lx = sec_x + (l_x - sec_x) * h_scale
                    ops.append(
                        f"BT {font_tag} {eff_lyric_sz:.2f} Tf {adj_lx:.2f} {lyric_y:.2f} Td ({pdf_escape(l_str)}) Tj ET"
                    )

                cur_y -= line_pair_h

            cur_y -= sec_gap

    # 3. Footer
    ops.append("0.75 0.78 0.82 RG 0.5 w")
    ops.append(f"{MARGIN_X:.1f} {BOTTOM_Y + 10:.1f} m {PAGE_W - MARGIN_X:.1f} {BOTTOM_Y + 10:.1f} l S")
    ops.append("0.45 0.50 0.56 rg")
    footer_left = f"Seventh-day Adventist Hymnal #{num_str}  •  {h['title']} (Key of {h['key']}, {h['time']})"
    ops.append(f"BT /F1 7.5 Tf {MARGIN_X:.2f} {BOTTOM_Y:.2f} Td ({pdf_escape(footer_left)}) Tj ET")

    stream_bytes = "\n".join(ops).encode("latin-1", errors="replace")

    # Assemble minimal valid PDF 1.4 file
    objects: List[bytes] = []
    objects.append(b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n")
    objects.append(b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n")
    page_obj = (
        f"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {PAGE_W:.0f} {PAGE_H:.0f}] "
        f"/Resources << /Font << /F1 4 0 R /F2 5 0 R /F3 6 0 R >> >> /Contents 7 0 R >>\nendobj\n"
    ).encode("ascii")
    objects.append(page_obj)
    objects.append(b"4 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>\nendobj\n")
    objects.append(b"5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>\nendobj\n")
    objects.append(b"6 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Oblique /Encoding /WinAnsiEncoding >>\nendobj\n")
    content_obj = (
        f"7 0 obj\n<< /Length {len(stream_bytes)} >>\nstream\n".encode("ascii")
        + stream_bytes
        + b"\nendstream\nendobj\n"
    )
    objects.append(content_obj)

    out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets: List[int] = []
    for obj in objects:
        offsets.append(len(out))
        out.extend(obj)
    xref_pos = len(out)
    out.extend(f"xref\n0 {len(objects) + 1}\n0000000000 65535 f \n".encode("ascii"))
    for off in offsets:
        out.extend(f"{off:010d} 00000 n \n".encode("ascii"))
    out.extend(
        f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref_pos}\n%%EOF\n".encode("ascii")
    )
    out_path.write_bytes(bytes(out))


def build_all() -> None:
    dirs = {
        "ChordPro": ROOT_DIR / "ChordPro",
        "JustChords": ROOT_DIR / "JustChords",
        "PlainText": ROOT_DIR / "PlainText",
        "OnSong": ROOT_DIR / "OnSong",
        "OpenLyrics": ROOT_DIR / "OpenLyrics",
        "PDF-Chords": ROOT_DIR / "PDF-Chords",
    }
    for d in dirs.values():
        d.mkdir(parents=True, exist_ok=True)

    json_files = sorted(DB_DIR.glob("*.json"))
    master_chordpro_blocks: List[str] = []
    master_justchords_blocks: List[str] = []

    for jf in json_files:
        h = json.loads(jf.read_text(encoding="utf-8"))
        num_str = f"{h['number']:03d}"
        safe_title = h["title"].replace("/", "-")
        base_name = f"{num_str} - {safe_title}"

        # 1. ChordPro (.cho)
        cho_text = generate_chordpro(h)
        (dirs["ChordPro"] / f"{base_name}.cho").write_text(cho_text, encoding="utf-8")
        master_chordpro_blocks.append("{new_song}\n" + cho_text)

        # 2. JustChords (.cho)
        jc_text = generate_justchords(h)
        (dirs["JustChords"] / f"{base_name}.cho").write_text(jc_text, encoding="utf-8")
        master_justchords_blocks.append("{new_song}\n" + jc_text)

        # 3. PlainText (.txt)
        txt_text = generate_plaintext(h)
        (dirs["PlainText"] / f"{base_name}.txt").write_text(txt_text, encoding="utf-8")

        # 4. OnSong (.onsong)
        onsong_text = generate_onsong(h)
        (dirs["OnSong"] / f"{base_name}.onsong").write_text(onsong_text, encoding="utf-8")

        # 5. OpenLyrics (.xml)
        xml_text = generate_openlyrics(h)
        (dirs["OpenLyrics"] / f"{base_name}.xml").write_text(xml_text, encoding="utf-8")

        # 6. Printable PDF Chord Chart (.pdf)
        generate_pdf_chart(h, dirs["PDF-Chords"] / f"{base_name}.pdf")

    # Write bulk-import master files
    (dirs["ChordPro"] / "000 - SDA Hymnal Master.cho").write_text(
        "\n".join(master_chordpro_blocks), encoding="utf-8"
    )
    (dirs["JustChords"] / "000 - SDA Hymnal JustChords Master.cho").write_text(
        "\n".join(master_justchords_blocks), encoding="utf-8"
    )
    print(f"Successfully compiled {len(json_files)} hymns across all 6 formats!")


if __name__ == "__main__":
    build_all()
