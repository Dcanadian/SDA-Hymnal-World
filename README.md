# SDA-Hymnal-World
The ultimate resource hub of the modern english Seventh-day Adventist hymnal for musicians.

---

## Key Features

- **All 695 Hymns**: The entire 1985 Seventh-day Adventist Hymnal converted across all worship formats.
- **Clean Triad & 7th Chording (Zero Slash Clutter)**: Every harmony is named by its clean triad or 7th root (`F`, `Dm`, `C`, `Am`, `Bb`, `Gm`, `A`, `C7`), matching the clean display of the [JustChords iOS app](https://apps.apple.com/).
- **Exact Syllable-Under-Chord Alignment**: In both Chords-Over-Lyrics plain text and 1-page printable vector PDF charts, every chorded syllable starts directly underneath its chord letter (e.g., `Al` under `Dm`, `might` under `Am`, `y,` under `Bb`). Melismatic cadences (`cre a     tion!`) place transitional chords over sustained vowel space and landing chords directly over word endings.
- **Unhyphenated Contiguous Lyrics**: Chords are placed inline at the exact syllable boundary without mid-word hyphens (`[Dm]Al[Am]might[Bb]y,`, `[Dm]cre[Bb]a[C7][F]tion!`).
- **Chords on Every Verse & Refrain**: Every stanza (`Verse 1`, `Verse 2`, `Verse 3`…) and `Refrain` includes chords so musicians never have to scroll back to Verse 1.
- **Orchestral Lead Sheets for Special Instruments & Clefs**: Dedicated, transposed 1-page printable charts for B♭, E♭, F, Bass Clef, and Alto Clef instruments.
- **Editable MusicXML for MuseScore**: Open standard `.musicxml` files with clefs, key signatures, time signatures, chord symbols, and lyrics ready for MuseScore, Finale, Sibelius, and Dorico.
- **Projection Ready**: Native FreeShow (`.show`) presentation files with responsive typography, slide groups, and liturgical order.
- **Editable 4-Part SATB MusicXML for MuseScore**: Authentic 4-part choral scores (Soprano, Alto, Tenor, Bass) cloned directly from the SDA hymnal PDF with exact pitches, proper rhythmic durations, measure barlines, key signatures, meters, chords, and lyrics ready for MuseScore, Finale, Sibelius, and Dorico.
- **True Melody-Only Sheet Music Lead Sheets**: Professional 5-line musical staves, clefs, notes, stems, barlines, chords above the staff across 6 dedicated instrument parts (C, B♭, E♭, F, Bass Clef, Alto Clef) in clean black & white with authentic classic hymnal headers.
- **Complete Hymnal PDF Included**: Full original Seventh-day Adventist Hymnal (1985) sheet music score PDF (`SDA_Hymnal_1985.pdf`) right in the repository.

---

## Folder Structure

| Folder / File | Extension | File Count | Description |
| :--- | :--- | :--- | :--- |
| [`Sheet-Music/SDA_Hymnal_1985.pdf`](file:///home/antigravity/SDA-Hymnal/Sheet-Music/SDA_Hymnal_1985.pdf) | `.pdf` | 1 | Complete original 1985 Seventh-day Adventist Hymnal score PDF |
| [`Database/`](file:///home/antigravity/SDA-Hymnal/Database) | `.json` | 696 | Canonical source-of-truth JSON metadata & stanzas per hymn |
| [`Chords/ChordPro/`](file:///home/antigravity/SDA-Hymnal/Chords/ChordPro) | `.cho` | 696 | Standard ChordPro files (`{start_of_verse}`, `{title}`) + Master index file |
| [`Chords/PlainText/`](file:///home/antigravity/SDA-Hymnal/Chords/PlainText) | `.txt` | 696 | Space-aligned Chords-Over-Lyrics text for any text editor |
| [`Chords/PDF-Chords/`](file:///home/antigravity/SDA-Hymnal/Chords/PDF-Chords) | `.pdf` | 696 | High-resolution 1-page printable vector chord charts (classic hymnal header) |
| [`Slides/FreeShow/`](file:///home/antigravity/SDA-Hymnal/Slides/FreeShow) | `.show` | 696 | Native FreeShow presentation files with metadata, slide groups & layouts |
| [`Sheet-Music/MusicXML/`](file:///home/antigravity/SDA-Hymnal/Sheet-Music/MusicXML) | `.musicxml` | 696 | Editable 4-part SATB harmony scores for MuseScore, Finale, Sibelius, Dorico |
| [`Sheet-Music/Lead-Sheets/C-Concert-Treble/`](file:///home/antigravity/SDA-Hymnal/Sheet-Music/Lead-Sheets/C-Concert-Treble) | `.pdf` | 696 | Melody + chord symbols only (no lyrics), black & white in Concert Pitch (Flute, Violin, Oboe, Guitar, Piano) |
| [`Sheet-Music/Lead-Sheets/Bb-Instruments/`](file:///home/antigravity/SDA-Hymnal/Sheet-Music/Lead-Sheets/Bb-Instruments) | `.pdf` | 696 | Melody + chord symbols only (no lyrics), black & white transposed +2 semitones (Trumpet, Clarinet, Tenor Sax) |
| [`Sheet-Music/Lead-Sheets/Eb-Instruments/`](file:///home/antigravity/SDA-Hymnal/Sheet-Music/Lead-Sheets/Eb-Instruments) | `.pdf` | 696 | Melody + chord symbols only (no lyrics), black & white transposed +9 semitones (Alto Sax, Baritone Sax) |
| [`Sheet-Music/Lead-Sheets/F-Instruments/`](file:///home/antigravity/SDA-Hymnal/Sheet-Music/Lead-Sheets/F-Instruments) | `.pdf` | 696 | Melody + chord symbols only (no lyrics), black & white transposed +7 semitones (French Horn) |
| [`Sheet-Music/Lead-Sheets/Bass-Clef/`](file:///home/antigravity/SDA-Hymnal/Sheet-Music/Lead-Sheets/Bass-Clef) | `.pdf` | 696 | Melody + chord symbols only (no lyrics), black & white in Bass Clef (Cello, Trombone, Euphonium, Bassoon, Tuba) |
| [`Sheet-Music/Lead-Sheets/Alto-Clef/`](file:///home/antigravity/SDA-Hymnal/Sheet-Music/Lead-Sheets/Alto-Clef) | `.pdf` | 696 | Melody + chord symbols only (no lyrics), black & white in Alto Clef (Viola) |

---

## Rebuilding & Generation Commands

```bash
# 1. Compile into ChordPro, PlainText, and PDF-Chords
python3 scripts/build_hymnal.py

# 2. Generate native FreeShow (.show) presentation files (2-3 lines/slide phrasing)
python3 scripts/generate_slides.py

# 3. Generate authentic 4-part SATB MusicXML for MuseScore
~/.venv/bin/python scripts/generate_satb_musicxml.py

# 4. Generate melody-only sheet music lead sheets across 6 instrument parts (4,176 PDFs)
~/.venv/bin/python scripts/generate_melody_sheet_music.py

# 5. Generate melody-only sheet music lead sheets across 6 instrument parts (4,176 PDFs)
~/.venv/bin/python scripts/generate_melody_sheet_music.py
```

