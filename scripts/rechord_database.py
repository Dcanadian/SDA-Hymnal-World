#!/usr/bin/env python3
"""
Re-chord the hymn database from the actual SATB harmony in the MIDI files.

Why: the original inline chords were placed per-syllable (often mid-word) and 255
hymns had none at all. This script:
  1. Reads the first tune pass (one stanza, + refrain if the hymn has one) from MIDI.
  2. Identifies one chord per half-measure (per measure in 3/4) from the vertical
     Bass/Tenor/Alto/Soprano stack, so the chords match what the notes play.
  3. Maps each lyric line to its musical phrase and puts a chord at the start of
     the word that falls on each chord change. Chords never land mid-word.
  4. Re-uses the stanza's chord pattern for every later verse, and gives the
     refrain its own pattern from the music.

Run:  ~/.venv/bin/python scripts/rechord_database.py
"""
import glob
import json
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from scripts.generate_satb_musicxml import (  # noqa: E402
    KEY_FIFTHS, extract_satb_from_midi,
)

DB_DIR = ROOT / "Database"
CHORD_RE = re.compile(r"\[[^\]]*\]")


def count_syllables(word: str) -> int:
    w = re.sub(r"[^a-z]", "", word.lower())
    if not w:
        return 0
    groups = re.findall(r"[aeiouy]+", w)
    n = len(groups)
    if w.endswith("e") and not w.endswith(("le", "ee")) and n > 1:
        n -= 1
    if re.search(r"(eth|est)$", w) is None and w.endswith("ed") and n > 1 and not w.endswith(("ted", "ded")):
        n -= 1
    return max(1, n)


def first_pass(satb, h):
    """Trim repeated verses out of the MIDI so we keep a single tune pass."""
    sop = satb["Soprano"]
    sections = h.get("sections", [])
    n_first = sum(count_syllables(w) for l in sections[0]["lines"] for w in CHORD_RE.sub("", l).split()) if sections else 20
    if len(sections) > 1 and sections[1].get("type") == "chorus":
        n_first += sum(count_syllables(w) for l in sections[1]["lines"] for w in CHORD_RE.sub("", l).split())
    pattern = [p for _, _, p in sop[:6]]
    min_idx = max(8, int(n_first * 0.75))
    repeat_beat = None
    for i in range(min_idx, len(sop) - 6):
        if sop[i][0] >= 16.0 and [p for _, _, p in sop[i:i + 6]] == pattern:
            repeat_beat = sop[i][0]
            break
    if repeat_beat:
        satb = {k: [n for n in v if n[0] < repeat_beat - 0.5] for k, v in satb.items()}
    return satb


FLAT_NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
SHARP_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
NOTE_PC = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3, "E": 4, "F": 5, "F#": 6, "Gb": 6,
           "G": 7, "G#": 8, "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
# chord quality -> (interval set, suffix, prior penalty as a fraction of total weight)
QUALITIES = [
    ((0, 4, 7), "", 0.0),
    ((0, 3, 7), "m", 0.0),
    ((0, 4, 7, 10), "7", 0.12),
    ((0, 3, 6), "dim", 0.35),
]
MAJOR_SCALE = {0, 2, 4, 5, 7, 9, 11}
MINOR_SCALE = {0, 2, 3, 5, 7, 8, 10, 11}


def midi_key(num: int):
    """Real key from the MIDI key_signature event (the database key was wrong for many hymns)."""
    import mido
    path = ROOT / "MIDI" / f"{num:03d}.mid"
    try:
        mid = mido.MidiFile(str(path))
    except Exception:
        return None
    for tr in mid.tracks:
        for msg in tr:
            if msg.type == "key_signature":
                return msg.key
    return None


class Harmony:
    def __init__(self, satb, h):
        self.satb = satb
        m = re.match(r"(\d+)/(\d+)", h.get("time", "4/4"))
        beats = int(m.group(1)) if m else 4
        beat_type = int(m.group(2)) if m else 4
        self.q_meas = beats * 4.0 / beat_type
        # One chord slot per beat (dotted-quarter in compound meters)
        compound = beat_type == 8 and beats % 3 == 0 and beats >= 6
        self.unit = 1.5 if compound else 4.0 / beat_type
        key = h.get("key", "C")
        self.minor = key.endswith("m") and key != "Bbm" or key == "Bbm"
        self.tonic = NOTE_PC.get(key[:-1] if self.minor else key, 0)
        self.fifths = KEY_FIFTHS.get(key, 0)
        self.names = FLAT_NAMES if self.fifths < 0 else SHARP_NAMES
        scale = MINOR_SCALE if self.minor else MAJOR_SCALE
        self.scale = {(self.tonic + i) % 12 for i in scale}
        self.sop = satb["Soprano"]
        self.end = max(s + d for s, d, _ in self.sop)
        self.n_meas = max(1, int(math.ceil(self.end / self.q_meas - 0.05)))
        self.notes = []
        weights = {"Soprano": 1.0, "Alto": 0.8, "Tenor": 0.8, "Bass": 1.4}
        for voice, lst in satb.items():
            for st, dur, p in lst:
                self.notes.append((st, st + dur, p, weights.get(voice, 1.0), voice))
        self._cache = {}
        self._last = None
        self._last_key = None

    def chord_at_unit(self, u: int) -> str:
        # Evaluate sequentially so stickiness always sees the previous slot
        for k in range(len(self._cache), u + 1):
            if k not in self._cache:
                self._eval_unit(k)
        return self._cache[u]

    def _eval_unit(self, u: int) -> str:
        t0, t1 = u * self.unit, (u + 1) * self.unit
        w = [0.0] * 12
        bass_pc, bass_p = None, 999
        for st, en, p, wt, voice in self.notes:
            ov = min(en, t1) - max(st, t0)
            if ov <= 0.05:
                continue
            w[p % 12] += ov * wt
            if voice == "Bass" and st <= t0 + 0.6 and p < bass_p:
                bass_pc, bass_p = p % 12, p
        total = sum(w)
        if total <= 0:
            ch = self._cache.get(u - 1) or self._last or self.names[self.tonic]
            self._cache[u] = ch
            return ch
        best, best_score = None, -1e9
        for root in range(12):
            for ivs, suffix, prior in QUALITIES:
                tones = {(root + i) % 12 for i in ivs}
                inside = sum(w[pc] for pc in tones)
                outside = total - inside
                score = inside - 0.9 * outside
                if bass_pc is not None and bass_pc == root:
                    score += 0.6 * total
                elif bass_pc is not None and bass_pc in tones:
                    score += 0.15 * total
                if tones <= self.scale:
                    score += 0.3 * total
                else:
                    score -= 0.35 * total
                if suffix == "7" and root == (self.tonic + 7) % 12:
                    score += 0.12 * total
                score -= prior * total
                if self._last_key == (root, suffix):
                    score += 0.3 * total  # stickiness: ignore passing harmony
                if score > best_score:
                    best, best_score = (root, suffix, tones), score
        root, suffix, tones = best
        name = self.names[root] + suffix
        if bass_pc is not None and bass_pc != root and bass_pc in tones:
            name += "/" + self.names[bass_pc]
        self._last = name
        self._last_key = (root, suffix)
        self._cache[u] = name
        return name

    def chord_at_time(self, t: float) -> str:
        return self.chord_at_unit(int((t + 0.05) // self.unit))

    def onsets(self, a: float, b: float):
        return [s for s, _, _ in self.sop if a - 0.05 <= s < b - 0.05]


def line_syllables(line: str):
    words = CHORD_RE.sub("", line).split()
    return words, [count_syllables(w) for w in words]


def build_template(hm: Harmony, lines, t0: float, t1: float):
    """Return per-line (span_start, span_end) over [t0, t1], snapped to bars."""
    weights = [max(1, sum(line_syllables(l)[1])) for l in lines]
    total = sum(weights)
    bars = max(1, int(round((t1 - t0) / hm.q_meas)))
    spans = []
    cum = 0
    prev_edge = t0
    for i, w in enumerate(weights):
        cum += w
        if i == len(weights) - 1:
            edge = t1
        else:
            bar = int(round(cum / total * bars))
            bar = max(bar, int(round((prev_edge - t0) / hm.q_meas)) + 1)
            bar = min(bar, bars - (len(weights) - 1 - i))
            edge = t0 + bar * hm.q_meas if bars >= len(weights) else t0 + cum / total * (t1 - t0)
        spans.append((prev_edge, edge))
        prev_edge = edge
    return spans


def chord_for_fraction(hm: Harmony, span, f: float) -> str:
    a, b = span
    ons = hm.onsets(a, b)
    if ons:
        t = ons[min(len(ons) - 1, int(f * len(ons)))]
    else:
        t = a + f * (b - a)
    return hm.chord_at_time(t)


def apply_template(hm, spans, lines):
    """Insert [chord] before words at chord changes. Returns new lines."""
    out = []
    prev = None
    nt = len(spans)
    for k, line in enumerate(lines):
        words, syls = line_syllables(line)
        if not words:
            out.append(line)
            continue
        kt = k if len(lines) == nt else min(nt - 1, int(round(k * (nt - 1) / max(1, len(lines) - 1))))
        total = sum(syls)
        cum = 0
        pieces = []
        line_prev = None
        for w, s in zip(words, syls):
            ch = chord_for_fraction(hm, spans[kt], cum / total)
            cum += s
            # A bass inversion of the chord already showing (D -> D/A) is not a new chord
            if line_prev is None or ch.split("/")[0] != line_prev.split("/")[0]:
                pieces.append(f"[{ch}]{w}")
                line_prev = ch
            else:
                pieces.append(w)
        out.append(" ".join(pieces))
        prev = line_prev
    return out


def rechord(h: dict) -> bool:
    satb = extract_satb_from_midi(h["number"])
    if not satb or not satb.get("Soprano"):
        return False
    satb = first_pass(satb, h)
    mk = midi_key(h["number"])
    if mk and mk in KEY_FIFTHS:
        h["key"] = mk
    hm = Harmony(satb, h)
    sections = h["sections"]
    verse_idx = next((i for i, s in enumerate(sections) if s["type"] == "verse"), 0)
    chorus_idx = next((i for i, s in enumerate(sections) if s["type"] == "chorus"), None)

    t_end = hm.n_meas * hm.q_meas
    if chorus_idx is not None and hm.n_meas >= 2:
        nv = sum(sum(line_syllables(l)[1]) for l in sections[verse_idx]["lines"])
        nc = sum(sum(line_syllables(l)[1]) for l in sections[chorus_idx]["lines"])
        mv = min(hm.n_meas - 1, max(1, int(round(hm.n_meas * nv / (nv + nc)))))
        v_span, c_span = (0.0, mv * hm.q_meas), (mv * hm.q_meas, t_end)
    else:
        v_span, c_span = (0.0, t_end), None

    v_tpl = build_template(hm, sections[verse_idx]["lines"], *v_span)
    c_tpl = build_template(hm, sections[chorus_idx]["lines"], *c_span) if c_span else None

    for sec in sections:
        if sec["type"] == "chorus" and c_tpl:
            sec["lines"] = apply_template(hm, c_tpl, sec["lines"])
        else:
            sec["lines"] = apply_template(hm, v_tpl, sec["lines"])
    return True


def main():
    ok = bad = 0
    for f in sorted(glob.glob(str(DB_DIR / "[0-9][0-9][0-9]*.json"))):
        h = json.loads(Path(f).read_text(encoding="utf-8"))
        # Strip existing chords first so the result never depends on old data
        for s in h["sections"]:
            s["lines"] = [CHORD_RE.sub("", l) for l in s["lines"]]
        if rechord(h):
            ok += 1
        else:
            bad += 1
            print("  no MIDI harmony:", h["number"])
        Path(f).write_text(json.dumps(h, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Re-chorded {ok} hymns ({bad} without MIDI).")


if __name__ == "__main__":
    main()
