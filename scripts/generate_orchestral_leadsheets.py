#!/usr/bin/env python3
"""
Generate Transposed Orchestral Lead Sheets for all 695 SDA Hymns:
1. B♭ Instruments (Trumpet, Clarinet, Tenor Sax) - Transposed +2 semitones
2. E♭ Instruments (Alto Sax, Baritone Sax) - Transposed +9 semitones
3. F Instruments (French Horn) - Transposed +7 semitones
4. Bass Clef (Cello, Trombone, Euphonium, Bassoon, Tuba, Bass) - Concert Pitch
5. Alto Clef (Viola) - Concert Pitch
"""

import glob
import json
import re
import os
import sys
from pathlib import Path

ROOT = Path("/home/antigravity/SDA-Hymnal")
sys.path.append(str(ROOT / "scripts"))
import build_hymnal

ORCH_DIR = ROOT / "Orchestral-Lead-Sheets"
PARTS = {
    "Bb-Instruments": {
        "name": "B♭ Instruments (Trumpet, Clarinet, Tenor Sax)",
        "semitones": 2,
        "use_sharps": True
    },
    "Eb-Instruments": {
        "name": "E♭ Instruments (Alto Sax, Baritone Sax)",
        "semitones": 9,
        "use_sharps": True
    },
    "F-Instruments": {
        "name": "F Instruments (French Horn)",
        "semitones": 7,
        "use_sharps": False
    },
    "Bass-Clef": {
        "name": "Bass Clef (Cello, Trombone, Bass)",
        "semitones": 0,
        "use_sharps": False
    },
    "Alto-Clef": {
        "name": "Alto Clef (Viola)",
        "semitones": 0,
        "use_sharps": False
    }
}

for folder in PARTS:
    (ORCH_DIR / folder).mkdir(parents=True, exist_ok=True)

CHROMATIC_FLAT = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
CHROMATIC_SHARP = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
PITCH_TO_SEMITONE = {
    "C": 0, "B#": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3, "E": 4, "Fb": 4,
    "F": 5, "E#": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8, "Ab": 8, "A": 9, "A#": 10,
    "Bb": 10, "B": 11, "Cb": 11
}

def transpose_chord(chord_str: str, semitones: int, use_sharps: bool = True) -> str:
    if semitones == 0:
        return chord_str
    m = re.match(r"^([A-G][b#]?)(.*)$", chord_str)
    if not m:
        return chord_str
    root, suffix = m.group(1), m.group(2)
    if root not in PITCH_TO_SEMITONE:
        return chord_str
    new_semi = (PITCH_TO_SEMITONE[root] + semitones) % 12
    scale = CHROMATIC_SHARP if use_sharps else CHROMATIC_FLAT
    return f"{scale[new_semi]}{suffix}"

def transpose_line(line: str, semitones: int, use_sharps: bool = True) -> str:
    if semitones == 0:
        return line
    return re.sub(r"\[([A-G][b#]?[^\]]*)\]", lambda m: f"[{transpose_chord(m.group(1), semitones, use_sharps)}]", line)

db_files = sorted(glob.glob(str(ROOT / "Database/[0-9][0-9][0-9]*.json")))
print(f"Generating Orchestral Lead Sheets for {len(db_files)} hymns across 5 instrument parts...")

count = 0
for f in db_files:
    h = json.load(open(f, encoding="utf-8"))
    num = h["number"]
    title = h["title"]
    safe_t = re.sub(r"[/\\:*?\"<>|]", "", title).strip()
    
    for part_key, part_cfg in PARTS.items():
        semi = part_cfg["semitones"]
        sharps = part_cfg["use_sharps"]
        part_name = part_cfg["name"]
        
        # Build transposed hymn copy
        th = dict(h)
        orig_key = h.get("key", "C")
        new_key = transpose_chord(orig_key, semi, sharps) if semi != 0 else orig_key
        th["key"] = new_key
        th["subcategory"] = f"Part: {part_name} (Concert Key: {orig_key})" if semi != 0 else f"Part: {part_name}"
        
        t_sections = []
        for sec in h.get("sections", []):
            t_sec = dict(sec)
            t_sec["lines"] = [transpose_line(l, semi, sharps) for l in sec["lines"]]
            t_sections.append(t_sec)
        th["sections"] = t_sections
        
        out_pdf = ORCH_DIR / part_key / f"{num:03d} - {safe_t}.pdf"
        build_hymnal.generate_pdf_chart(th, out_pdf)
    
    count += 1

print(f"Successfully generated orchestral lead sheets for {count} hymns (5 parts each = {count * 5} charts) in Orchestral-Lead-Sheets/!")
