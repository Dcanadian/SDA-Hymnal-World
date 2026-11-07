#!/usr/bin/env python3
"""
Deterministic 4-Part SATB Note-Stack-to-Chord Analyzer for the SDA Hymnal (1985).
Takes vertical note stacks (Bass, Tenor, Alto, Soprano) transcribed from the score
and verifies/computes exact chord symbols, including:
  - Upper-voice chord transitions over a stationary/pedal bass (e.g., Em7/D, Bb/C -> C)
  - Slash chords / first & second inversions (e.g., C/E, F/A, D/F#, Bm/D, Gm7/Bb)
  - Suspended chords & resolutions (e.g., Asus4 -> A, Dsus4 -> D, Bsus4 -> B, E7sus4 -> E7)
  - Seventh, sixth, major-7th, and diminished/half-diminished stacks
"""

from typing import List, Tuple

PITCH_CLASS = {
    "C": 0, "C#": 1, "Db": 1,
    "D": 2, "D#": 3, "Eb": 3,
    "E": 4, "Fb": 4, "E#": 5,
    "F": 5, "F#": 6, "Gb": 6,
    "G": 7, "G#": 8, "Ab": 8,
    "A": 9, "A#": 10, "Bb": 10,
    "B": 11, "Cb": 11, "B#": 0,
}

NOTE_OCTAVE_RE = r"^([A-G][b#]?)(\d+)$"


def note_to_pc(note: str) -> Tuple[str, int]:
    """Extract (pitch_name_without_octave, pitch_class_int) from e.g. 'F#3'."""
    name = "".join(ch for ch in note if not ch.isdigit())
    return name, PITCH_CLASS[name]


def identify_stack(notes: Tuple[str, ...], key_flats: bool = False) -> str:
    """
    Deterministically identify a chord symbol from a bottom-to-top vertical note stack
    (Bass, ..., Soprano).
    """
    bass_name, bass_pc = note_to_pc(notes[0])
    pcs = sorted({note_to_pc(n)[1] for n in notes})
    pc_set = set(pcs)

    # Candidate root names in enharmonic preference order for the key
    pc_to_name = (
        {0: "C", 1: "Db", 2: "D", 3: "Eb", 4: "E", 5: "F", 6: "F#", 7: "G", 8: "Ab", 9: "A", 10: "Bb", 11: "B"}
        if key_flats else
        {0: "C", 1: "C#", 2: "D", 3: "D#", 4: "E", 5: "F", 6: "F#", 7: "G", 8: "G#", 9: "A", 10: "A#", 11: "B"}
    )
    # Ensure bass name uses actual spelled note from score
    pc_to_name[bass_pc] = bass_name
    for n in notes[1:]:
        nm, pc = note_to_pc(n)
        pc_to_name[pc] = nm

    # Templates: (intervals_set, quality_suffix, base_score)
    templates = [
        ({0, 4, 7}, "", 100),
        ({0, 3, 7}, "m", 98),
        ({0, 4, 7, 10}, "7", 96),
        ({0, 3, 7, 10}, "m7", 95),
        ({0, 4, 7, 11}, "maj7", 94),
        ({0, 5, 7}, "sus4", 90),
        ({0, 2, 7}, "sus2", 88),
        ({0, 5, 7, 10}, "7sus4", 89),
        ({0, 3, 6}, "dim", 86),
        ({0, 3, 6, 10}, "m7b5", 87),
        ({0, 3, 6, 9}, "dim7", 87),
        ({0, 4, 7, 9}, "6", 84),
        ({0, 3, 7, 9}, "m6", 83),
        ({0, 4, 10}, "7", 80),       # Seventh chord with omitted 5th
        ({0, 3, 10}, "m7", 75),      # Minor 7th with omitted 5th
        ({0, 4}, "", 70),            # Dyad (root + 3rd, omitted 5th)
        ({0, 3}, "m", 68),           # Minor dyad (root + b3, omitted 5th)
        ({0, 7}, "5", 60),           # Open fifth
    ]

    best_chord = "?"
    best_score = -999

    for root_pc in pcs:
        rel_pcs = {(pc - root_pc) % 12 for pc in pc_set}
        root_name = pc_to_name[root_pc]
        for tmpl_set, suffix, base_score in templates:
            if rel_pcs == tmpl_set:
                score = base_score + (12 if root_pc == bass_pc else 0)
                if score > best_score:
                    best_score = score
                    if root_pc == bass_pc:
                        best_chord = f"{root_name}{suffix}"
                    else:
                        best_chord = f"{root_name}{suffix}/{bass_name}"

    return best_chord


# Sample verification on Hymn 001 & Hymn 002 stacks
HYMN_001_STACKS: List[Tuple[str, str, Tuple[str, ...], str]] = [
    ("m.1 b.1", "Praise", ("F3", "A3", "C4", "F4"), "F"),
    ("m.1 b.2", "to", ("Bb2", "F3", "D4", "F4"), "Bb"),
    ("m.1 b.3", "the", ("F3", "A3", "F4", "C5"), "F"),
    ("m.2 b.1", "Lord,", ("F3", "C4", "F4", "A4"), "F"),
    ("m.2 b.2.5", "the", ("C3", "C4", "E4", "G4"), "C"),
    ("m.2 b.3", "Al-", ("F3", "A3", "C4", "F4"), "F"),
    ("m.3 b.1", "-might-", ("C3", "G3", "C4", "E4"), "C"),
    ("m.3 b.2", "-y,", ("Bb2", "F3", "Bb3", "D4"), "Bb"),
    ("m.3 b.3", "the", ("F2", "F3", "A3", "C4"), "F"),
    ("m.4 b.1", "King", ("Bb2", "F3", "Bb3", "D4"), "Bb"),
    ("m.4 b.2", "of", ("G2", "G3", "Bb3", "E4"), "Edim/G"),
    ("m.4 b.3", "cre-", ("D3", "F3", "A3", "F4"), "Dm"),
    ("m.5 b.1", "-a- (1)", ("Bb2", "F3", "D4", "G4"), "Gm7/Bb"),
    ("m.5 b.2", "-a- (2)", ("C3", "E3", "C4", "G4"), "C"),
    ("m.5 b.3", "-a- (3)", ("C3", "E3", "Bb3", "G4"), "C7"),
    ("m.6 b.1", "-tion!", ("F2", "F3", "A3", "F4"), "F"),
    ("m.13 b.1", "All", ("F3", "A3", "C4", "C5"), "F"),
    ("m.13 b.2", "ye", ("E3", "G3", "C4", "C5"), "C/E"),
    ("m.13 b.3", "who", ("F3", "A3", "C4", "C5"), "F"),
    ("m.14 b.1", "hear,", ("Bb2", "Bb3", "F4", "D5"), "Bb"),
    ("m.15 b.1", "Now", ("D3", "D4", "F4", "A4"), "Dm"),
    ("m.15 b.2", "to", ("G3", "D4", "G4", "Bb4"), "Gm"),
    ("m.15 b.3", "His", ("C3", "E4", "G4", "C5"), "C"),
    ("m.16 b.1", "tem-", ("A2", "C4", "F4", "C5"), "F/A"),
    ("m.16 b.2", "-ple", ("Bb2", "G3", "D4", "Bb4"), "Gm/Bb"),
    ("m.16 b.3", "draw", ("F3", "C4", "F4", "A4"), "F"),
    ("m.17 b.1", "near;", ("C3", "C4", "E4", "G4"), "C"),
    ("m.18 b.1", "Join", ("F3", "A3", "C4", "C4"), "F"),
    ("m.18 b.2", "ye", ("Bb2", "F3", "Bb3", "D4"), "Bb"),
    ("m.18 b.3", "in", ("C3", "G3", "C4", "E4"), "C"),
    ("m.19 b.1", "glad", ("D3", "F3", "A3", "F4"), "Dm"),
    ("m.19 b.2", "ad-", ("Bb2", "D3", "D4", "G4"), "Gm/Bb"),
    ("m.19 b.3", "-o-", ("A2", "E3", "C#4", "A4"), "A"),
    ("m.20 b.1", "-ra- (1)", ("Bb2", "F3", "D4", "G4"), "Gm7/Bb"),
    ("m.20 b.3", "-ra- (3)", ("C3", "E3", "Bb3", "G4"), "C7"),
    ("m.21 b.1", "-tion!", ("F2", "F3", "A3", "F4"), "F"),
]

HYMN_002_STACKS: List[Tuple[str, str, Tuple[str, ...], str]] = [
    ("pickup", "All", ("D3", "F#3", "A3", "D4"), "D"),
    ("m.1 q.1", "crea-", ("D3", "F#3", "D4", "D4"), "D"),
    ("m.1 q.2", "-tures", ("D3", "G3", "B3", "E4"), "Em7/D"),
    ("m.1 q.3", "of", ("D3", "A3", "D4", "F#4"), "D"),
    ("m.1 q.4", "our", ("D3", "F#3", "A3", "D4"), "D"),
    ("m.1 q.5", "God", ("B2", "D4", "D4", "F#4"), "Bm"),
    ("m.1 q.6", "and", ("E3", "B3", "D4", "G4"), "Em7"),
    ("m.2 q.1", "King (1)", ("A2", "A3", "D4", "E4", "A4"), "Asus4"),
    ("m.2 q.3", "King (2)", ("A2", "A3", "C#4", "E4", "A4"), "A"),
    ("m.2 q.5", "Lift (1)", ("F#3", "A3", "D4", "D4"), "D/F#"),
    ("m.2 q.6", "Lift (2)", ("G3", "B3", "D4", "D4"), "G"),
    ("m.3 q.1", "up", ("F#3", "A3", "D4", "D4"), "D/F#"),
    ("m.3 q.2", "your", ("E3", "G3", "B3", "E4"), "Em"),
    ("m.3 q.3", "voice", ("D3", "A3", "D4", "F#4"), "D"),
    ("m.3 q.4", "with", ("C#3", "A3", "D4", "D4"), "D/C#"),
    ("m.3 q.5", "us", ("B2", "D4", "D4", "F#4"), "Bm"),
    ("m.3 q.6", "and", ("E3", "B3", "D4", "G4"), "Em7"),
    ("m.4 q.1", "sing: (1)", ("A2", "A3", "D4", "E4", "A4"), "Asus4"),
    ("m.4 q.3", "sing: (2)", ("A2", "A3", "C#4", "E4", "A4"), "A"),
    ("m.4 q.5", "Al-", ("D3", "F#4", "A4", "D5"), "D"),
    ("m.4 q.6", "-le-", ("D3", "F#4", "A4", "C#5"), "Dmaj7"),
    ("m.5 q.1", "-lu-", ("G3", "D4", "G4", "B4"), "G"),
    ("m.5 q.3", "-ia!", ("D3", "D4", "F#4", "A4"), "D"),
    ("m.5 q.5", "Al-", ("B2", "F#3", "D4", "D5"), "Bm"),
    ("m.5 q.6", "-le-", ("F#3", "A3", "F#4", "C#5"), "F#m"),
    ("m.6 q.1", "-lu- (1)", ("E3", "B3", "F#4", "B4"), "Esus4"),
    ("m.6 q.2", "-lu- (2)", ("E3", "G#3", "E4", "B4"), "E"),
    ("m.6 q.3", "-ia!", ("A2", "A3", "C#4", "A4"), "A"),
]


if __name__ == "__main__":
    print("=== HYMN 001 NOTE-STACK VERIFICATION ===")
    for pos, syl, stack, expected in HYMN_001_STACKS:
        computed = identify_stack(stack, key_flats=True)
        print(f"  {pos:10s} | {syl:10s} | {str(stack):30s} -> computed={computed:8s} (target={expected})")

    print("\n=== HYMN 002 NOTE-STACK VERIFICATION ===")
    for pos, syl, stack, expected in HYMN_002_STACKS:
        computed = identify_stack(stack, key_flats=False)
        print(f"  {pos:10s} | {syl:10s} | {str(stack):34s} -> computed={computed:8s} (target={expected})")
