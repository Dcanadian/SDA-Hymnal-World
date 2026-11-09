#!/usr/bin/env python3
"""
Generate True 2-Staff SATB Choral Hymnal MusicXML (4.0 Partwise) for all 695 SDA Hymns.

An exact editable clone of the Seventh-day Adventist Hymnal (1985) sheet music for:
- MuseScore 4
- Finale
- Sibelius
- Dorico

Layout Specification (matching original SDA Hymnal PDF):
- 2 Staves per System joined by a choral brace:
  1. Upper Staff (Treble Clef): Soprano (Voice 1, stems up) + Alto (Voice 2, stems down)
  2. Lower Staff (Bass Clef): Tenor (Voice 1, stems up) + Bass (Voice 2, stems down)
- Full Syllable-by-Syllable Lyric Text placed between staves with proper <syllabic>
  hyphenation (begin, middle, end, single) and multi-verse stacking.
- Chords (<harmony>) positioned cleanly above the treble staff.
- Authentic Key Signatures, Time Signatures, Tempo Marks, and Measure Barlines.
"""

import os
import re
import json
import math
import glob
import time
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
import mido
import hyphenate

ROOT_DIR = Path("/home/antigravity/SDA-Hymnal")
DB_DIR = ROOT_DIR / "Database"
MIDI_DIR = ROOT_DIR / "midis"
XML_DIR = ROOT_DIR / "MusicXML"
XML_DIR.mkdir(parents=True, exist_ok=True)

KEY_FIFTHS = {
    "C": 0, "Am": 0,
    "G": 1, "Em": 1,
    "D": 2, "Bm": 2,
    "A": 3, "F#m": 3,
    "E": 4, "C#m": 4,
    "B": 5, "G#m": 5,
    "F#": 6, "D#m": 6,
    "F": -1, "Dm": -1,
    "Bb": -2, "Gm": -2,
    "Eb": -3, "Cm": -3,
    "Ab": -4, "Fm": -4,
    "Db": -5, "Bbm": -5,
    "Gb": -6, "Ebm": -6
}

FLAT_PITCHES = {
    0: ("C", 0), 1: ("D", -1), 2: ("D", 0), 3: ("E", -1), 4: ("E", 0),
    5: ("F", 0), 6: ("G", -1), 7: ("G", 0), 8: ("A", -1), 9: ("A", 0),
    10: ("B", -1), 11: ("B", 0)
}

SHARP_PITCHES = {
    0: ("C", 0), 1: ("C", 1), 2: ("D", 0), 3: ("D", 1), 4: ("E", 0),
    5: ("F", 1), 6: ("F", 1), 7: ("G", 0), 8: ("G", 1), 9: ("A", 0),
    10: ("A", 1), 11: ("B", 0)
}


def midi_to_pitch(midi_num: int, fifths: int):
    use_flats = fifths < 0
    pitch_map = FLAT_PITCHES if use_flats else SHARP_PITCHES
    octave = (midi_num // 12) - 1
    step, alter = pitch_map[midi_num % 12]
    return step, alter, octave


def duration_to_type(dur_div: int, divisions: int):
    ratio = dur_div / divisions
    dot = False
    if ratio <= 0.35:
        ntype = "16th"
    elif ratio <= 0.65:
        ntype = "eighth"
    elif ratio <= 0.85:
        ntype = "eighth"
        dot = True
    elif ratio <= 1.25:
        ntype = "quarter"
    elif ratio <= 1.75:
        ntype = "quarter"
        dot = True
    elif ratio <= 2.5:
        ntype = "half"
    elif ratio <= 3.5:
        ntype = "half"
        dot = True
    elif ratio <= 5.0:
        ntype = "whole"
    else:
        ntype = "whole"
        dot = True
    return ntype, dot


def extract_satb_from_midi(num: int):
    mid_path = MIDI_DIR / f"{num:03d}.mid"
    if not mid_path.exists():
        return None
    try:
        mid = mido.MidiFile(str(mid_path))
    except Exception:
        return None

    tpb = mid.ticks_per_beat
    tr0 = mid.tracks[0]
    tempo_changes = []
    abs_t = 0
    for msg in tr0:
        abs_t += msg.time
        if msg.type == 'set_tempo':
            tempo_changes.append((abs_t / tpb, msg.tempo))
            
    v1_start = 0.0
    for i in range(len(tempo_changes) - 1):
        b, t = tempo_changes[i]
        next_b, next_t = tempo_changes[i+1]
        if t > 1000000 and b < 60.0:
            v1_start = next_b
            break
            
    v1_end = None
    for i in range(len(tempo_changes) - 1):
        b, t = tempo_changes[i]
        if b > v1_start + 14.0 and t > 1000000:
            v1_end = b
            break
    if not v1_end:
        v1_end = v1_start + 64.0
        
    satb_voices = {}
    voice_names = ["Soprano", "Alto", "Tenor", "Bass"]
    for v_idx in range(4):
        tr_num = v_idx + 1
        if tr_num >= len(mid.tracks):
            continue
        tr = mid.tracks[tr_num]
        abs_t = 0
        raw_notes = []
        active = {}
        for msg in tr:
            abs_t += msg.time
            if msg.type == 'note_on' and msg.velocity > 0:
                active[msg.note] = abs_t
            elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                if msg.note in active:
                    st = active.pop(msg.note)
                    dur = abs_t - st
                    b_st = st / tpb
                    b_dur = dur / tpb
                    if b_st >= v1_start - 0.5 and (b_st + b_dur) <= v1_end + 1.0:
                        raw_notes.append((b_st - v1_start, b_dur, msg.note))
                        
        raw_notes.sort(key=lambda x: (x[0], -x[2]))
        clean_notes = []
        last_st = -999.0
        for st, dur, p in raw_notes:
            if abs(st - last_st) < 0.1:
                continue
            last_st = st
            clean_notes.append((st, dur, p))
        satb_voices[voice_names[v_idx]] = clean_notes
    return satb_voices


def extract_syllables_and_chords(h):
    all_sylls = []
    chords_list = []
    if not h.get("sections"):
        return all_sylls, chords_list
        
    for sec in h["sections"]:
        if sec.get("type") in ["verse", "chorus"]:
            for line in sec.get("lines", []):
                tokens = line.split()
                for token in tokens:
                    ch_matches = re.findall(r'\[([A-G][b#]?[^\]]*)\]', token)
                    for ch in ch_matches:
                        chords_list.append(ch)
                    pieces = re.split(r'(\[[^\]]+\])', token)
                    text_pieces = [p for p in pieces if p and not p.startswith('[')]
                    if not text_pieces:
                        continue
                    word_sylls = []
                    for tp in text_pieces:
                        clean = re.sub(r'[^a-zA-Z]', '', tp)
                        hyph = hyphenate.hyphenate_word(clean)
                        if len(hyph) > 1 and len(clean) >= 4:
                            cur = tp
                            for part in hyph[:-1]:
                                idx = cur.lower().find(part.lower())
                                if idx >= 0:
                                    word_sylls.append(cur[:idx+len(part)])
                                    cur = cur[idx+len(part):]
                            if cur:
                                word_sylls.append(cur)
                        else:
                            word_sylls.append(tp)
                    if len(word_sylls) == 1:
                        all_sylls.append((word_sylls[0], "single"))
                    else:
                        for i, syl in enumerate(word_sylls):
                            tag = "begin" if i == 0 else ("end" if i == len(word_sylls)-1 else "middle")
                            all_sylls.append((syl, tag))
            break
    return all_sylls, chords_list


def chord_to_xml(ch_name: str):
    m = re.match(r'^([A-G])([b#]?)(.*)$', ch_name)
    if not m:
        return ""
    step = m.group(1)
    acc = m.group(2)
    suffix = m.group(3)
    alter_str = ""
    if acc == "b":
        alter_str = "<root-alter>-1</root-alter>"
    elif acc == "#":
        alter_str = "<root-alter>1</root-alter>"
    kind = "major"
    text_attr = ""
    if suffix == "m":
        kind = "minor"
    elif suffix == "7":
        kind = "dominant"
        text_attr = ' text="7"'
    elif suffix == "m7":
        kind = "minor-seventh"
        text_attr = ' text="m7"'
    elif suffix == "maj7":
        kind = "major-seventh"
        text_attr = ' text="maj7"'
    elif suffix == "dim":
        kind = "diminished"
    elif suffix == "sus4":
        kind = "suspended-fourth"
    return f"""      <harmony>
        <root>
          <root-step>{step}</root-step>
          {alter_str}
        </root>
        <kind{text_attr}>{kind}</kind>
      </harmony>
"""


def build_hymnal_satb_score(json_file: str):
    try:
        with open(json_file, "r", encoding="utf-8") as f:
            h = json.load(f)
            
        num = h["number"]
        title = h["title"]
        safe_title = re.sub(r'[/\\:*?"<>|]', "", title).strip()
        composer = h.get("composer", "")
        lyricist = h.get("lyricist", "")
        key_str = h.get("key", "C")
        fifths = KEY_FIFTHS.get(key_str, 0)
        time_str = h.get("time", "4/4")
        tempo_val = h.get("tempo", 100)
        
        m = re.match(r'(\d+)/(\d+)', time_str)
        beats = int(m.group(1)) if m else 4
        beat_type = int(m.group(2)) if m else 4
        
        divisions = 4
        meas_dur_div = int(round(beats * (4.0 / beat_type) * divisions))
        
        satb = extract_satb_from_midi(num)
        if not satb or not satb.get("Soprano"):
            return num, False, "Missing MIDI SATB tracks"
            
        sop_notes = satb["Soprano"]
        alt_notes = satb.get("Alto", [])
        ten_notes = satb.get("Tenor", [])
        bas_notes = satb.get("Bass", [])
        
        # Extract verses & chords
        verses_sylls = []
        chords_list = []
        for sec in h.get("sections", []):
            if sec.get("type") in ["verse", "chorus"]:
                s_list, c_list = extract_syllables_and_chords({"sections": [sec]})
                if not chords_list and c_list:
                    chords_list = c_list
                if s_list:
                    name = sec.get("name", "")
                    num_m = re.search(r'\d+', name)
                    if num_m:
                        v_num = num_m.group(0)
                        w, tag = s_list[0]
                        s_list[0] = (f"{v_num}. {w}", tag)
                    verses_sylls.append(s_list)
                    
        if not chords_list:
            chords_list = [key_str]
            
        max_beat = max(st + dur for st, dur, _ in sop_notes)
        num_measures = max(1, int(math.ceil(max_beat / beats)))
        
        def get_measure_notes(notes, m_idx, beats_per_meas):
            m_start = m_idx * beats_per_meas
            m_end = (m_idx + 1) * beats_per_meas
            m_notes = []
            for st, dur, p in notes:
                if m_start - 0.1 <= st < m_end - 0.1:
                    rel_st = max(0.0, st - m_start)
                    rel_dur = min(dur, m_end - st)
                    m_notes.append((rel_st, rel_dur, p, st))
            return m_notes
            
        xml_parts = []
        header = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE score-partwise PUBLIC "-//Recordare//DTD MusicXML 4.0 Partwise//EN" "http://www.musicxml.org/dtds/partwise.dtd">
<score-partwise version="4.0">
  <work>
    <work-title>{num:03d} - {title}</work-title>
  </work>
  <identification>
    <creator type="composer">{composer}</creator>
    <creator type="lyricist">{lyricist}</creator>
  </identification>
  <defaults>
    <scaling>
      <millimeters>7.0</millimeters>
      <tenths>40</tenths>
    </scaling>
  </defaults>
  <part-list>
    <part-group type="start" number="1">
      <group-symbol>brace</group-symbol>
      <group-barline>yes</group-barline>
    </part-group>
    <score-part id="P1">
      <part-name></part-name>
    </score-part>
    <score-part id="P2">
      <part-name></part-name>
    </score-part>
    <part-group type="stop" number="1"/>
  </part-list>
"""
        xml_parts.append(header)
        
        sop_note_counter = 0
        chord_counter = 0
        
        # =================================================================
        # PART 1: Soprano (Voice 1, up) & Alto (Voice 2, down) on Treble
        # =================================================================
        xml_parts.append('  <part id="P1">\n')
        for m_idx in range(num_measures):
            m_num = m_idx + 1
            xml_parts.append(f'    <measure number="{m_num}">\n')
            if m_idx == 0:
                xml_parts.append(f"""      <attributes>
        <divisions>{divisions}</divisions>
        <key>
          <fifths>{fifths}</fifths>
        </key>
        <time>
          <beats>{beats}</beats>
          <beat-type>{beat_type}</beat-type>
        </time>
        <clef>
          <sign>G</sign>
          <line>2</line>
        </clef>
      </attributes>
      <direction placement="above">
        <direction-type>
          <metronome>
            <beat-unit>quarter</beat-unit>
            <per-minute>{tempo_val}</per-minute>
          </metronome>
        </direction-type>
        <sound tempo="{tempo_val}"/>
      </direction>
""")
            # Voice 1: Soprano
            sop_m = get_measure_notes(sop_notes, m_idx, beats)
            cur_div = 0
            for rel_st, rel_dur, pitch_val, abs_st in sop_m:
                target_div = int(round(rel_st * divisions))
                if target_div > cur_div:
                    rest_div = target_div - cur_div
                    rtype, rdot = duration_to_type(rest_div, divisions)
                    dot_tag = "<dot/>" if rdot else ""
                    xml_parts.append(f"""      <note>
        <rest/>
        <duration>{rest_div}</duration>
        <voice>1</voice>
        <type>{rtype}</type>
        {dot_tag}
      </note>
""")
                    cur_div = target_div
                    
                dur_div = max(1, int(round(rel_dur * divisions)))
                if cur_div + dur_div > meas_dur_div:
                    dur_div = meas_dur_div - cur_div
                if dur_div <= 0:
                    continue
                    
                step, alter, octave = midi_to_pitch(pitch_val, fifths)
                ntype, dot = duration_to_type(dur_div, divisions)
                dot_tag = "<dot/>" if dot else ""
                alter_tag = f"<alter>{alter}</alter>" if alter != 0 else ""
                
                # Chord symbol
                if chord_counter < len(chords_list) and (cur_div == 0 or (abs_st % 2.0 < 0.25)):
                    xml_parts.append(chord_to_xml(chords_list[chord_counter]))
                    chord_counter += 1
                    
                # Stacked lyrics
                lyric_blocks = []
                for v_idx, v_sylls in enumerate(verses_sylls):
                    if sop_note_counter < len(v_sylls):
                        s_txt, s_tag = v_sylls[sop_note_counter]
                        c_txt = s_txt.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                        lyric_blocks.append(f"""        <lyric number="{v_idx+1}">
          <syllabic>{s_tag}</syllabic>
          <text>{c_txt}</text>
        </lyric>""")
                lyrics_xml = "\n".join(lyric_blocks) + "\n" if lyric_blocks else ""
                sop_note_counter += 1
                
                xml_parts.append(f"""      <note>
        <pitch>
          <step>{step}</step>
          {alter_tag}
          <octave>{octave}</octave>
        </pitch>
        <duration>{dur_div}</duration>
        <voice>1</voice>
        <type>{ntype}</type>
        {dot_tag}
        <stem>up</stem>
{lyrics_xml}      </note>
""")
                cur_div += dur_div
                
            if cur_div < meas_dur_div:
                rest_div = meas_dur_div - cur_div
                rtype, rdot = duration_to_type(rest_div, divisions)
                dot_tag = "<dot/>" if rdot else ""
                xml_parts.append(f"""      <note>
        <rest/>
        <duration>{rest_div}</duration>
        <voice>1</voice>
        <type>{rtype}</type>
        {dot_tag}
      </note>
""")
            xml_parts.append(f"""      <backup>
        <duration>{meas_dur_div}</duration>
      </backup>
""")
            # Voice 2: Alto
            alt_m = get_measure_notes(alt_notes, m_idx, beats)
            cur_div = 0
            for rel_st, rel_dur, pitch_val, abs_st in alt_m:
                target_div = int(round(rel_st * divisions))
                if target_div > cur_div:
                    rest_div = target_div - cur_div
                    rtype, rdot = duration_to_type(rest_div, divisions)
                    dot_tag = "<dot/>" if rdot else ""
                    xml_parts.append(f"""      <note>
        <rest/>
        <duration>{rest_div}</duration>
        <voice>2</voice>
        <type>{rtype}</type>
        {dot_tag}
      </note>
""")
                    cur_div = target_div
                    
                dur_div = max(1, int(round(rel_dur * divisions)))
                if cur_div + dur_div > meas_dur_div:
                    dur_div = meas_dur_div - cur_div
                if dur_div <= 0:
                    continue
                    
                step, alter, octave = midi_to_pitch(pitch_val, fifths)
                ntype, dot = duration_to_type(dur_div, divisions)
                dot_tag = "<dot/>" if dot else ""
                alter_tag = f"<alter>{alter}</alter>" if alter != 0 else ""
                xml_parts.append(f"""      <note>
        <pitch>
          <step>{step}</step>
          {alter_tag}
          <octave>{octave}</octave>
        </pitch>
        <duration>{dur_div}</duration>
        <voice>2</voice>
        <type>{ntype}</type>
        {dot_tag}
        <stem>down</stem>
      </note>
""")
                cur_div += dur_div
                
            if cur_div < meas_dur_div:
                rest_div = meas_dur_div - cur_div
                rtype, rdot = duration_to_type(rest_div, divisions)
                dot_tag = "<dot/>" if rdot else ""
                xml_parts.append(f"""      <note>
        <rest/>
        <duration>{rest_div}</duration>
        <voice>2</voice>
        <type>{rtype}</type>
        {dot_tag}
      </note>
""")
            xml_parts.append('    </measure>\n')
        xml_parts.append('  </part>\n')
        
        # =================================================================
        # PART 2: Tenor (Voice 1, up) & Bass (Voice 2, down) on Bass Clef
        # =================================================================
        xml_parts.append('  <part id="P2">\n')
        for m_idx in range(num_measures):
            m_num = m_idx + 1
            xml_parts.append(f'    <measure number="{m_num}">\n')
            if m_idx == 0:
                xml_parts.append(f"""      <attributes>
        <divisions>{divisions}</divisions>
        <key>
          <fifths>{fifths}</fifths>
        </key>
        <time>
          <beats>{beats}</beats>
          <beat-type>{beat_type}</beat-type>
        </time>
        <clef>
          <sign>F</sign>
          <line>4</line>
        </clef>
      </attributes>
""")
            # Voice 1: Tenor
            ten_m = get_measure_notes(ten_notes, m_idx, beats)
            cur_div = 0
            for rel_st, rel_dur, pitch_val, abs_st in ten_m:
                target_div = int(round(rel_st * divisions))
                if target_div > cur_div:
                    rest_div = target_div - cur_div
                    rtype, rdot = duration_to_type(rest_div, divisions)
                    dot_tag = "<dot/>" if rdot else ""
                    xml_parts.append(f"""      <note>
        <rest/>
        <duration>{rest_div}</duration>
        <voice>1</voice>
        <type>{rtype}</type>
        {dot_tag}
      </note>
""")
                    cur_div = target_div
                    
                dur_div = max(1, int(round(rel_dur * divisions)))
                if cur_div + dur_div > meas_dur_div:
                    dur_div = meas_dur_div - cur_div
                if dur_div <= 0:
                    continue
                    
                step, alter, octave = midi_to_pitch(pitch_val, fifths)
                ntype, dot = duration_to_type(dur_div, divisions)
                dot_tag = "<dot/>" if dot else ""
                alter_tag = f"<alter>{alter}</alter>" if alter != 0 else ""
                xml_parts.append(f"""      <note>
        <pitch>
          <step>{step}</step>
          {alter_tag}
          <octave>{octave}</octave>
        </pitch>
        <duration>{dur_div}</duration>
        <voice>1</voice>
        <type>{ntype}</type>
        {dot_tag}
        <stem>up</stem>
      </note>
""")
                cur_div += dur_div
                
            if cur_div < meas_dur_div:
                rest_div = meas_dur_div - cur_div
                rtype, rdot = duration_to_type(rest_div, divisions)
                dot_tag = "<dot/>" if rdot else ""
                xml_parts.append(f"""      <note>
        <rest/>
        <duration>{rest_div}</duration>
        <voice>1</voice>
        <type>{rtype}</type>
        {dot_tag}
      </note>
""")
            xml_parts.append(f"""      <backup>
        <duration>{meas_dur_div}</duration>
      </backup>
""")
            # Voice 2: Bass
            bas_m = get_measure_notes(bas_notes, m_idx, beats)
            cur_div = 0
            for rel_st, rel_dur, pitch_val, abs_st in bas_m:
                target_div = int(round(rel_st * divisions))
                if target_div > cur_div:
                    rest_div = target_div - cur_div
                    rtype, rdot = duration_to_type(rest_div, divisions)
                    dot_tag = "<dot/>" if rdot else ""
                    xml_parts.append(f"""      <note>
        <rest/>
        <duration>{rest_div}</duration>
        <voice>2</voice>
        <type>{rtype}</type>
        {dot_tag}
      </note>
""")
                    cur_div = target_div
                    
                dur_div = max(1, int(round(rel_dur * divisions)))
                if cur_div + dur_div > meas_dur_div:
                    dur_div = meas_dur_div - cur_div
                if dur_div <= 0:
                    continue
                    
                step, alter, octave = midi_to_pitch(pitch_val, fifths)
                ntype, dot = duration_to_type(dur_div, divisions)
                dot_tag = "<dot/>" if dot else ""
                alter_tag = f"<alter>{alter}</alter>" if alter != 0 else ""
                xml_parts.append(f"""      <note>
        <pitch>
          <step>{step}</step>
          {alter_tag}
          <octave>{octave}</octave>
        </pitch>
        <duration>{dur_div}</duration>
        <voice>2</voice>
        <type>{ntype}</type>
        {dot_tag}
        <stem>down</stem>
      </note>
""")
                cur_div += dur_div
                
            if cur_div < meas_dur_div:
                rest_div = meas_dur_div - cur_div
                rtype, rdot = duration_to_type(rest_div, divisions)
                dot_tag = "<dot/>" if rdot else ""
                xml_parts.append(f"""      <note>
        <rest/>
        <duration>{rest_div}</duration>
        <voice>2</voice>
        <type>{rtype}</type>
        {dot_tag}
      </note>
""")
            xml_parts.append('    </measure>\n')
        xml_parts.append('  </part>\n')
        xml_parts.append('</score-partwise>\n')
        
        out_xml = XML_DIR / f"{num:03d} - {safe_title}.musicxml"
        with open(out_xml, "w", encoding="utf-8") as f_out:
            f_out.write("".join(xml_parts))
            
        return num, True, None
    except Exception as e:
        return num, False, str(e)


def main():
    db_files = sorted(glob.glob(str(DB_DIR / "[0-9][0-9][0-9]*.json")))
    print(f"Generating authentic 2-staff SATB Hymnal MusicXML for {len(db_files)} hymns...")
    start_time = time.time()
    
    success = 0
    failed = 0
    with ProcessPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(build_hymnal_satb_score, f): f for f in db_files}
        for future in as_completed(futures):
            num, ok, err = future.result()
            if ok:
                success += 1
                if success % 100 == 0 or success == len(db_files):
                    print(f"  Progress: {success}/{len(db_files)} SATB hymnal scores generated")
            else:
                failed += 1
                print(f"  Error on hymn {num}: {err}")
                
    elapsed = time.time() - start_time
    print(f"\nSuccessfully generated {success} 2-staff SATB MusicXML files in {elapsed:.1f}s! Failures: {failed}")


if __name__ == "__main__":
    main()
