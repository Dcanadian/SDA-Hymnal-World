# SDA-Hymnal-World
The ultimate resource hub of the modern English Seventh-day Adventist Hymnal (1985) for musicians.

---

## Key Features

- **All 695 Hymns with Complete Metadata**: Every hymn (`001`–`695`) includes full Lyricist, Composer, Tune Name, Meter, Key Signature, Time Signature, and Tempo across all formats.
- **Harmonic-Matched SATB Chording**: Every chord symbol is derived directly from the 4-part vertical SATB note stack (Bass, Tenor, Alto, Soprano) so chord charts, lead sheets, and MusicXML playback are 100% harmonically synchronized.
- **Exact Syllable-Under-Chord Alignment**: In both Chords-Over-Lyrics plain text and 1-page printable vector PDF charts, every chorded syllable starts directly underneath its chord symbol.
- **PDF Chords with Classic Hymnal Typography**: Monochrome 1-page printable charts featuring the traditional 3-row hymnal header, Key/Time/Tempo subheader, and bold-italic (`Times-BoldItalic`) non-indented `Refrain` headers with italic refrain lyrics.
- **Projection-Ready FreeShow (`.show`) Slides**: Includes an automatic **Title Slide** (Hymn #, Title, Lyricist/Composer, Tune, Meter, Key, Time) followed by clean lyric-only slides split into natural 2–3 line musical/poetic phrases.
- **Editable 2-Staff SATB + 6-Part MusicXML for MuseScore**: Authentic 2-staff SATB choral scores (Soprano & Alto on Treble, Tenor & Bass on Bass) plus toggleable instrument parts (`C`, `B♭`, `E♭`, `F`, `Bass Clef`, `Alto Clef`) with proper rhythmic ties and final double barlines (`light-heavy`).
- **True Melody-Only Sheet Music Lead Sheets**: High-contrast monochrome 5-line musical staves with melody, chord symbols above the staff, rhythmic ties, and final double barlines across 6 dedicated instrument transpositions/clefs, scaled to fit cleanly on 1 single page without orphan phrases.
- **7 Compiled Master PDF Books (`Books/`)**: Ready-to-use complete hymnal binders for PDF Chords and all 6 Instrument Lead Sheet parts, complete with a multi-page 2-column Table of Contents, clickable internal page links, and full PDF outline bookmarks for instant navigation on iPad/tablets.

---

## Folder Structure

| Folder / File | Extension | File Count | Description |
| :--- | :--- | :--- | :--- |
| [`Books/`](file:///home/antigravity/SDA-Hymnal/Books) | `.pdf` | 7 | Compiled Master PDF Books (PDF Chords + 6 Instrument Lead Sheet books) with Table of Contents & clickable PDF bookmarks |
| [`Sheet-Music/SDA_Hymnal_1985.pdf`](file:///home/antigravity/SDA-Hymnal/Sheet-Music/SDA_Hymnal_1985.pdf) | `.pdf` | 1 | Complete original 1985 Seventh-day Adventist Hymnal score PDF |
| [`Database/`](file:///home/antigravity/SDA-Hymnal/Database) | `.json` | 695 | Canonical source-of-truth JSON metadata & stanzas per hymn |
| [`Chords/ChordPro/`](file:///home/antigravity/SDA-Hymnal/Chords/ChordPro) | `.cho` | 696 | Standard ChordPro files (`{start_of_verse}`, `{title}`, `{meta: tune}`, `{meta: meter}`) + Master index file |
| [`Chords/PlainText/`](file:///home/antigravity/SDA-Hymnal/Chords/PlainText) | `.txt` | 695 | Space-aligned Chords-Over-Lyrics text for any text editor |
| [`Chords/PDF-Chords/`](file:///home/antigravity/SDA-Hymnal/Chords/PDF-Chords) | `.pdf` | 695 | High-resolution 1-page printable vector chord charts (classic hymnal header) |
| [`Slides/FreeShow/`](file:///home/antigravity/SDA-Hymnal/Slides/FreeShow) | `.show` | 695 | Native FreeShow presentation files with Title Slide, 2–3 line phrase slides & liturgical layouts |
| [`Sheet-Music/MusicXML/`](file:///home/antigravity/SDA-Hymnal/Sheet-Music/MusicXML) | `.musicxml` | 695 | Editable 2-staff SATB + 6-part instrument scores for MuseScore, Finale, Sibelius, Dorico |
| [`Sheet-Music/Lead-Sheets/C-Concert-Treble/`](file:///home/antigravity/SDA-Hymnal/Sheet-Music/Lead-Sheets/C-Concert-Treble) | `.pdf` | 695 | Melody + chord symbols only (no lyrics), black & white in Concert Pitch (Flute, Violin, Oboe, Guitar, Piano) |
| [`Sheet-Music/Lead-Sheets/Bb-Instruments/`](file:///home/antigravity/SDA-Hymnal/Sheet-Music/Lead-Sheets/Bb-Instruments) | `.pdf` | 695 | Melody + chord symbols only (no lyrics), black & white transposed +2 semitones (Trumpet, Clarinet, Tenor Sax) |
| [`Sheet-Music/Lead-Sheets/Eb-Instruments/`](file:///home/antigravity/SDA-Hymnal/Sheet-Music/Lead-Sheets/Eb-Instruments) | `.pdf` | 695 | Melody + chord symbols only (no lyrics), black & white transposed +9 semitones (Alto Sax, Baritone Sax) |
| [`Sheet-Music/Lead-Sheets/F-Instruments/`](file:///home/antigravity/SDA-Hymnal/Sheet-Music/Lead-Sheets/F-Instruments) | `.pdf` | 695 | Melody + chord symbols only (no lyrics), black & white transposed +7 semitones (French Horn) |
| [`Sheet-Music/Lead-Sheets/Bass-Clef/`](file:///home/antigravity/SDA-Hymnal/Sheet-Music/Lead-Sheets/Bass-Clef) | `.pdf` | 695 | Melody + chord symbols only (no lyrics), black & white in Bass Clef (Cello, Trombone, Euphonium, Bassoon, Tuba) |
| [`Sheet-Music/Lead-Sheets/Alto-Clef/`](file:///home/antigravity/SDA-Hymnal/Sheet-Music/Lead-Sheets/Alto-Clef) | `.pdf` | 695 | Melody + chord symbols only (no lyrics), black & white in Alto Clef (Viola) |

---

## Rebuilding & Generation Commands

```bash
# 1. Populate complete metadata (Lyricist, Composer, Tune, Meter) in Database/*.json
~/.venv/bin/python scripts/populate_metadata.py

# 2. Compile into ChordPro, PlainText, and PDF-Chords
python3 scripts/build_hymnal.py

# 3. Generate native FreeShow (.show) presentation files (Title Slide + 2-3 lines/slide phrasing)
python3 scripts/generate_slides.py

# 4. Generate authentic 2-staff SATB + 6-part MusicXML for MuseScore
~/.venv/bin/python scripts/generate_satb_musicxml.py

# 5. Generate melody-only sheet music lead sheets across 6 instrument parts (4,170 PDFs)
~/.venv/bin/python scripts/generate_melody_sheet_music.py

# 6. Compile the 7 Master PDF Books in Books/ with Table of Contents & PDF Bookmarks
~/.venv/bin/python scripts/build_master_books.py
```
