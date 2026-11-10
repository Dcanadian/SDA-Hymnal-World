#!/usr/bin/env python3
"""
Generate editable MusicXML files (4.0 Partwise) for all 695 SDA hymns for MuseScore, Sibelius, Finale, and Dorico.
Includes key signatures, time signatures, chord harmony symbols, and lyric text.
"""

import glob
import json
import re
import os
from pathlib import Path
import music21 as m21

ROOT = Path("/home/antigravity/SDA-Hymnal")
OUT_DIR = ROOT / "Sheet-Music" / "MusicXML"
OUT_DIR.mkdir(parents=True, exist_ok=True)

db_files = sorted(glob.glob(str(ROOT / "Database/[0-9][0-9][0-9]*.json")))
print(f"Generating editable MusicXML for {len(db_files)} hymns...")

def clean_for_m21(ch: str) -> str:
    if not ch:
        return "C"
    # replace flat 'b' after note letter with '-'
    if len(ch) > 1 and ch[1] == "b":
        return ch[0] + "-" + ch[2:]
    return ch

def generate_hymn_musicxml(h):
    num = h["number"]
    title = h["title"]
    key_str = clean_for_m21(h.get("key", "C"))
    time_str = h.get("time", "4/4")
    
    score = m21.stream.Score()
    score.metadata = m21.metadata.Metadata()
    score.metadata.title = f"{num:03d} - {title}"
    if h.get("composer"):
        score.metadata.composer = h["composer"]
    if h.get("lyricist"):
        score.metadata.lyricist = h["lyricist"]
        
    part = m21.stream.Part()
    part.partName = "Lead Sheet"
    part.append(m21.clef.TrebleClef())
    
    try:
        part.append(m21.key.Key(key_str))
    except Exception:
        part.append(m21.key.Key("C"))
        
    try:
        ts = m21.meter.TimeSignature(time_str)
        part.append(ts)
    except Exception:
        ts = m21.meter.TimeSignature("4/4")
        part.append(ts)
        
    chords = []
    lyrics_words = []
    if h.get("sections"):
        for sec in h["sections"]:
            if sec.get("type") == "verse":
                for line in sec["lines"]:
                    found_chords = re.findall(r"\[([A-G][b#]?[^\]]*)\]", line)
                    chords.extend(found_chords)
                    clean_lyric = re.sub(r"\[[^\]]+\]", "", line).strip()
                    lyrics_words.extend(clean_lyric.split())
                break
                
    if not chords:
        chords = [key_str]
    if not lyrics_words:
        lyrics_words = [title]
        
    for i, ch_sym in enumerate(chords):
        try:
            cs = m21.harmony.ChordSymbol(clean_for_m21(ch_sym))
        except Exception:
            try:
                cs = m21.harmony.ChordSymbol(key_str)
            except Exception:
                cs = m21.harmony.ChordSymbol("C")
        n = m21.note.Note(quarterLength=1.0)
        n.pitch.name = key_str[0] if key_str else "C"
        n.pitch.octave = 4
        if i < len(lyrics_words):
            n.lyric = lyrics_words[i]
        part.append(cs)
        part.append(n)
        
    score.append(part)
    safe_t = re.sub(r"[/\\:*?\"<>|]", "", title).strip()
    out_fp = OUT_DIR / f"{num:03d} - {safe_t}.musicxml"
    score.write("musicxml", fp=str(out_fp))

count = 0
for f in db_files:
    try:
        h = json.load(open(f, encoding="utf-8"))
        generate_hymn_musicxml(h)
        count += 1
    except Exception as e:
        print(f"Error on {f}: {e}")

print(f"Successfully generated {count} editable MusicXML files in MusicXML/!")
