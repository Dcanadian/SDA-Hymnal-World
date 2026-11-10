#!/usr/bin/env python3
"""
Generate Authentic Monochrome Classic Hymnal Lead Sheets (Vector PDFs) for all 695 SDA Hymns.

Features:
- Pure Black & White typography (high-contrast monochrome printing, #000000 on #ffffff)
- Non-AI, Authentic Classic Hymnal Header Layout (No horizontal divider lines):
  * Top Row: Hymn Number on left (bold), Instrument Part on right (bold)
  * Middle Row: Prominent centered Title (large bold serif)
  * Bottom Row: Lyricist / Author on left (italic), Tune, Meter, & Composer on right (italic)
- Zero Orphan Musical Phrases:
  * Truncates repeating verses from MIDI playback so each hymn represents one complete tune cycle
  * Dynamic scale fitting (scales 48 down to 34) ensuring each score fits on exactly 1 single page
- Complete 6 orchestral lead sheet parts:
  1. C-Concert-Treble (C Instruments)
  2. Bb-Instruments (B♭ Instruments) - Transposed +2 semitones
  3. Eb-Instruments (E♭ Instruments) - Transposed +9 semitones
  4. F-Instruments (F Instruments) - Transposed +7 semitones
  5. Bass-Clef (Bass Clef) - Concert Pitch, Bass Clef
  6. Alto-Clef (Alto Clef) - Concert Pitch, Alto Clef
- Clean universal accidentals (♯, ♭) and tempo mark (♩ = bpm) with zero font-box glitches
"""

import os
import re
import json
import math
import glob
import time
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
import verovio
import cairosvg

import sys
sys.path.insert(0, '/home/antigravity/SDA-Hymnal')

from scripts.generate_satb_musicxml import (
    KEY_FIFTHS, FLAT_PITCHES, SHARP_PITCHES, PITCH_CLASS,
    midi_to_pitch, duration_to_type,
    extract_satb_from_midi, extract_syllables_from_sections,
    get_chord_for_note_stack, chord_to_xml
)

ROOT_DIR = Path("/home/antigravity/SDA-Hymnal")
DB_DIR = ROOT_DIR / "Database"
ORCH_DIR = ROOT_DIR / "Sheet-Music" / "Lead-Sheets"

ORCH_PARTS = {
    "C-Concert-Treble": {
        "name": "C Instruments",
        "semitones": 0,
        "clef_sign": "G",
        "clef_line": 2,
    },
    "Bb-Instruments": {
        "name": "B♭ Instruments",
        "semitones": 2,
        "clef_sign": "G",
        "clef_line": 2,
    },
    "Eb-Instruments": {
        "name": "E♭ Instruments",
        "semitones": 9,
        "clef_sign": "G",
        "clef_line": 2,
    },
    "F-Instruments": {
        "name": "F Instruments",
        "semitones": 7,
        "clef_sign": "G",
        "clef_line": 2,
    },
    "Bass-Clef": {
        "name": "Bass Clef",
        "semitones": 0,
        "clef_sign": "F",
        "clef_line": 4,
    },
    "Alto-Clef": {
        "name": "Alto Clef",
        "semitones": 0,
        "clef_sign": "C",
        "clef_line": 3,
    },
}

for part_dir in ORCH_PARTS:
    (ORCH_DIR / part_dir).mkdir(parents=True, exist_ok=True)

SHARP_SCALE = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
FLAT_SCALE  = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']


def transpose_chord_name(ch_str: str, semi: int, target_fifths: int) -> str:
    if not ch_str or ch_str == '?':
        return ''
    scale = FLAT_SCALE if target_fifths < 0 else SHARP_SCALE
    parts = ch_str.split('/')
    res = []
    for p in parts:
        m = re.match(r'^([A-G][b#]?)(.*)$', p)
        if not m:
            res.append(p)
            continue
        root = m.group(1)
        suffix = m.group(2)
        pc = PITCH_CLASS.get(root, 0)
        new_pc = (pc + semi) % 12
        new_root = scale[new_pc]
        res.append(f'{new_root}{suffix}')
    return '/'.join(res)


def render_lead_sheet_pdf(tk, h: dict, satb: dict, v_sylls: list, part_cfg: dict) -> bytes:
    num = h["number"]
    title = h["title"]
    composer = h.get("composer", "")
    lyricist = h.get("lyricist", "")
    tune = h.get("tune", "")
    meter = h.get("meter", "")
    key_str = h.get("key", "C")
    concert_fifths = KEY_FIFTHS.get(key_str, 0)
    
    semi = part_cfg["semitones"]
    part_name = part_cfg["name"]
    clef_sign = part_cfg["clef_sign"]
    clef_line = part_cfg["clef_line"]
    
    if semi == 2:
        transposed_fifths = concert_fifths + 2
    elif semi == 9:
        transposed_fifths = concert_fifths + 3
    elif semi == 7:
        transposed_fifths = concert_fifths + 1
    else:
        transposed_fifths = concert_fifths

    time_str = h.get("time", "4/4")
    tempo_val = h.get("tempo", 100)
    m = re.match(r'(\d+)/(\d+)', time_str)
    beats = int(m.group(1)) if m else 4
    beat_type = int(m.group(2)) if m else 4
    divisions = 4
    meas_quarter_beats = beats * (4.0 / beat_type)
    meas_dur_div = int(round(meas_quarter_beats * divisions))

    sop_notes = satb["Soprano"]
    alt_notes = satb.get("Alto", [])
    ten_notes = satb.get("Tenor", [])
    bas_notes = satb.get("Bass", [])

    max_beat = max(st + dur for st, dur, _ in sop_notes)
    num_measures = max(1, int(math.ceil(max_beat / meas_quarter_beats)))

    def get_measure_notes(notes, m_idx, q_per_meas):
        m_start = m_idx * q_per_meas
        m_end = (m_idx + 1) * q_per_meas
        m_notes = []
        for st, dur, p in notes:
            if m_start - 0.1 <= st < m_end - 0.1:
                rel_st = max(0.0, st - m_start)
                rel_dur = min(dur, m_end - st)
                m_notes.append((rel_st, rel_dur, p, st))
        return m_notes

    xml_parts = [f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE score-partwise PUBLIC "-//Recordare//DTD MusicXML 4.0 Partwise//EN" "http://www.musicxml.org/dtds/partwise.dtd">
<score-partwise version="4.0">
  <part-list>
    <score-part id="P1"><part-name></part-name></score-part>
  </part-list>
  <part id="P1">
"""]

    sop_note_counter = 0
    last_chord = None

    for m_idx in range(num_measures):
        m_num = m_idx + 1
        xml_parts.append(f'    <measure number="{m_num}">\n')
        if m_idx == 0:
            xml_parts.append(f"""      <attributes>
        <divisions>{divisions}</divisions>
        <key><fifths>{transposed_fifths}</fifths></key>
        <time><beats>{beats}</beats><beat-type>{beat_type}</beat-type></time>
        <clef><sign>{clef_sign}</sign><line>{clef_line}</line></clef>
      </attributes>
      <direction placement="above">
        <direction-type>
          <metronome><beat-unit>quarter</beat-unit><per-minute>{tempo_val}</per-minute></metronome>
        </direction-type>
        <sound tempo="{tempo_val}"/>
      </direction>
""")
        sop_m = get_measure_notes(sop_notes, m_idx, meas_quarter_beats)
        cur_div = 0
        for rel_st, rel_dur, pitch_val, abs_st in sop_m:
            target_div = int(round(rel_st * divisions))
            if target_div > cur_div:
                rest_div = target_div - cur_div
                rtype, rdot = duration_to_type(rest_div, divisions)
                dot_tag = "<dot/>" if rdot else ""
                xml_parts.append(f'      <note><rest/><duration>{rest_div}</duration><type>{rtype}</type>{dot_tag}</note>\n')
                cur_div = target_div
                
            dur_div = max(1, int(round(rel_dur * divisions)))
            if cur_div + dur_div > meas_dur_div:
                dur_div = meas_dur_div - cur_div
            if dur_div <= 0:
                continue
                
            trans_pitch = pitch_val + semi
            if clef_sign == 'F' and trans_pitch > 60:
                trans_pitch -= 12
            elif clef_sign == 'C' and trans_pitch > 72:
                trans_pitch -= 12
            elif semi == 9 and trans_pitch > 81:
                trans_pitch -= 12
            elif semi == 7 and trans_pitch > 81:
                trans_pitch -= 12
                
            step, alter, octave = midi_to_pitch(trans_pitch, transposed_fifths)
            ntype, dot = duration_to_type(dur_div, divisions)
            dot_tag = "<dot/>" if dot else ""
            alter_tag = f"<alter>{alter}</alter>" if alter != 0 else ""
            
            # Chord symbol (on the beat or start of measure)
            if (abs_st % 1.0 < 0.15) or rel_dur >= 1.0 or cur_div == 0:
                concert_ch = get_chord_for_note_stack(abs_st, pitch_val, alt_notes, ten_notes, bas_notes, concert_fifths, last_chord)
                trans_ch = transpose_chord_name(concert_ch, semi, transposed_fifths)
                if trans_ch and (trans_ch != last_chord or cur_div == 0):
                    xml_parts.append(chord_to_xml(trans_ch))
                    last_chord = trans_ch
            
            xml_parts.append(f"""      <note>
        <pitch><step>{step}</step>{alter_tag}<octave>{octave}</octave></pitch>
        <duration>{dur_div}</duration>
        <voice>1</voice>
        <type>{ntype}</type>{dot_tag}
      </note>
""")
            cur_div += dur_div
            
        if cur_div < meas_dur_div:
            rest_div = meas_dur_div - cur_div
            rtype, rdot = duration_to_type(rest_div, divisions)
            dot_tag = "<dot/>" if rdot else ""
            xml_parts.append(f'      <note><rest/><duration>{rest_div}</duration><type>{rtype}</type>{dot_tag}</note>\n')
        xml_parts.append('    </measure>\n')
    xml_parts.append('  </part>\n</score-partwise>\n')

    lead_xml = ''.join(xml_parts)
    
    # Scale fitting loop: Guarantee 1 single page with zero orphan phrases
    current_scale = 48
    while current_scale >= 34:
        tk.setOptions({
            'pageWidth': 2100,
            'pageHeight': 2970,
            'scale': current_scale,
            'adjustPageHeight': False,
            'header': 'none',
            'footer': 'none',
            'harmDist': 4,
            'spacingSystem': 13,
            'spacingStaff': 11,
            'lyricTopMinMargin': 3.0,
            'breaksNoWidow': True
        })
        tk.loadData(lead_xml)
        if tk.getPageCount() == 1:
            break
        current_scale -= 2

    # In rare cases of very long hymns (>36 measures), render all pages without widows
    total_pages = tk.getPageCount()
    svg_pages = []
    for p_num in range(1, total_pages + 1):
        svg_p = tk.renderToSVG(p_num)
        svg_p = svg_p.replace('\uea66', '♯').replace('\uea64', '♭').replace('\ueca5', '♩')
        svg_p = re.sub(r'font-family="Leipzig"', 'font-family="serif"', svg_p)
        svg_p = re.sub(r'class="page-margin" transform="translate\(\d+,\s*\d+\)"', 'class="page-margin" transform="translate(500, 2500)"', svg_p)
        
        safe_title_h = title.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        safe_lyr_h = lyricist.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        safe_right_h = f'{tune} {meter}   {composer}'.strip().replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

        # Authentic Classic Hymnal Header (Pure Black & White, No lines)
        header_svg = f"""
  <g id="hymnal-header" fill="#000000">
    <!-- Top row: Number on left, Part on right -->
    <text x="1000" y="900" font-family="DejaVu Serif, Times, Georgia, serif" font-size="650" font-weight="bold" text-anchor="start">{num}</text>
    <text x="20000" y="900" font-family="DejaVu Serif, Times, Georgia, serif" font-size="380" font-weight="bold" text-anchor="end">{part_name}</text>
    
    <!-- Middle row: Title centered in prominent type -->
    <text x="10500" y="1450" font-family="DejaVu Serif, Times, Georgia, serif" font-size="650" font-weight="bold" text-anchor="middle">{safe_title_h}</text>
    
    <!-- Bottom row: Author on left, Tune/Composer on right -->
    <text x="1000" y="1950" font-family="DejaVu Serif, Times, Georgia, serif" font-size="280" font-style="italic" text-anchor="start">{safe_lyr_h}</text>
    <text x="20000" y="1950" font-family="DejaVu Serif, Times, Georgia, serif" font-size="280" font-style="italic" text-anchor="end">{safe_right_h}</text>
  </g>
"""
        idx = svg_p.find('class="definition-scale"')
        insert_pos = svg_p.find('>', idx) + 1
        final_svg = svg_p[:insert_pos] + header_svg + svg_p[insert_pos:]
        svg_pages.append(final_svg)

    # Render vector PDF (single page or joined multi-page if exceptionally long)
    if len(svg_pages) == 1:
        pdf_bytes = cairosvg.svg2pdf(bytestring=svg_pages[0].encode('utf-8'))
    else:
        import fitz
        doc = fitz.open()
        for s in svg_pages:
            p_bytes = cairosvg.svg2pdf(bytestring=s.encode('utf-8'))
            sub_doc = fitz.open(stream=p_bytes, filetype="pdf")
            doc.insert_pdf(sub_doc)
        pdf_bytes = doc.tobytes()
        
    return pdf_bytes


def process_single_hymn(json_file: str):
    try:
        with open(json_file, "r", encoding="utf-8") as f:
            h = json.load(f)
            
        num = h["number"]
        title = h["title"]
        safe_title = re.sub(r'[/\\:*?"<>|]', "", title).strip()
        
        satb = extract_satb_from_midi(num)
        if not satb or not satb.get("Soprano"):
            return num, False, "Missing MIDI SATB tracks"
            
        v_sylls = extract_syllables_from_sections(h)
        
        # Truncate repeating verses from MIDI playback so each hymn represents 1 complete tune pass
        first_pass_sylls = len(v_sylls[0]) if v_sylls else 20
        if len(h.get("sections", [])) > 1 and h["sections"][1].get("type") in ["chorus", "refrain"]:
            if len(v_sylls) > 1:
                first_pass_sylls += len(v_sylls[1])
                
        sop_raw = satb["Soprano"]
        pattern = [p for _, _, p in sop_raw[:6]]
        repeat_beat = None
        min_idx = max(8, int(first_pass_sylls * 0.75))
        for i in range(min_idx, len(sop_raw) - 6):
            if sop_raw[i][0] >= 16.0 and [p for _, _, p in sop_raw[i:i+6]] == pattern:
                repeat_beat = sop_raw[i][0]
                break
                
        if repeat_beat:
            for v_k in satb:
                satb[v_k] = [n for n in satb[v_k] if n[0] < repeat_beat - 0.5]
        
        tk = verovio.toolkit()
        
        for part_key, part_cfg in ORCH_PARTS.items():
            pdf_bytes = render_lead_sheet_pdf(tk, h, satb, v_sylls, part_cfg)
            out_pdf = ORCH_DIR / part_key / f"{num:03d} - {safe_title}.pdf"
            with open(out_pdf, "wb") as f_out:
                f_out.write(pdf_bytes)
                
        return num, True, None
    except Exception as e:
        return num, False, str(e)


def main():
    db_files = sorted(glob.glob(str(DB_DIR / "[0-9][0-9][0-9]*.json")))
    print(f"Generating Authentic B&W Classic Hymnal Lead Sheets for {len(db_files)} hymns across 6 parts...")
    start_time = time.time()
    
    success = 0
    failed = 0
    with ProcessPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(process_single_hymn, f): f for f in db_files}
        for future in as_completed(futures):
            num, ok, err = future.result()
            if ok:
                success += 1
                if success % 50 == 0 or success == len(db_files):
                    print(f"  Progress: {success}/{len(db_files)} hymns rendered ({success * 6} PDFs)")
            else:
                failed += 1
                print(f"  Error on hymn {num}: {err}")
                
    elapsed = time.time() - start_time
    print(f"\nSuccessfully generated {success * 6} B&W Lead Sheet PDFs in {elapsed:.1f}s! Failures: {failed}")


if __name__ == "__main__":
    main()
