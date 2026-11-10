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
- **Projection Ready**: Native FreeShow (`.show`) presentation files, ProPresenter slide files, and OpenLyrics XML for FreeShow, OpenLP, and ProPresenter.
- **Editable 4-Part SATB MusicXML for MuseScore**: Authentic 4-part choral scores (Soprano, Alto, Tenor, Bass) cloned directly from the SDA hymnal PDF with exact pitches, proper rhythmic durations, measure barlines, key signatures, meters, chords, and lyrics ready for MuseScore, Finale, Sibelius, and Dorico.
- **True Melody-Only Sheet Music Lead Sheets**: Professional 5-line musical staves, clefs, notes, stems, barlines, chords above the staff, and lyrics below the staff across 6 dedicated instrument parts.
- **Complete Hymnal PDF Included**: Full 724-page original Seventh-day Adventist Hymnal (1985) sheet music score PDF (`SDA_Hymnal_1985.pdf`) right in the repository.

---

## Folder Structure

| Folder / File | Extension | File Count | Description |
| :--- | :--- | :--- | :--- |
| [`SDA_Hymnal_1985.pdf`](file:///home/antigravity/SDA-Hymnal/SDA_Hymnal_1985.pdf) | `.pdf` | 1 | Complete 724-page original 1985 Seventh-day Adventist Hymnal score PDF |
| [`Database/`](file:///home/antigravity/SDA-Hymnal/Database) | `.json` | 695 | Canonical source-of-truth JSON metadata & stanzas per hymn |
| [`Chords/ChordPro/`](file:///home/antigravity/SDA-Hymnal/Chords/ChordPro) | `.cho` | 696 | Standard ChordPro files (`{start_of_verse}`, `{title}`) + Master index file |
| [`Chords/JustChords/`](file:///home/antigravity/SDA-Hymnal/Chords/JustChords) | `.cho` | 696 | Native JustChords format (`Verse 1:`, `Refrain:` tags) + Master index file |
| [`Chords/PlainText/`](file:///home/antigravity/SDA-Hymnal/Chords/PlainText) | `.txt` | 695 | Space-aligned Chords-Over-Lyrics text for any text editor |
| [`Chords/OnSong/`](file:///home/antigravity/SDA-Hymnal/Chords/OnSong) | `.onsong` | 695 | OnSong iPad/iOS/macOS worship presentation format |
| [`Slides/OpenLyrics/`](file:///home/antigravity/SDA-Hymnal/Slides/OpenLyrics) | `.xml` | 695 | OpenLyrics 0.9 XML with `<chord name="..."/>` tags for OpenLP & FreeShow |
| [`Slides/FreeShow/`](file:///home/antigravity/SDA-Hymnal/Slides/FreeShow) | `.show` | 696 | Native FreeShow presentation files with metadata, slide groups & layouts |
| [`Chords/PDF-Chords/`](file:///home/antigravity/SDA-Hymnal/Chords/PDF-Chords) | `.pdf` | 695 | High-resolution 1-page printable vector chord charts |
| [`Slides/ProPresenter/`](file:///home/antigravity/SDA-Hymnal/Slides/ProPresenter) | `.txt` | 695 | Slide-divided text ready for batch import into ProPresenter |
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
# 1. Generate canonical JSON database for all 695 hymns
python3 scripts/generate_all_695.py

# 2. Compile into ChordPro, JustChords, PlainText, OnSong, OpenLyrics, and PDF-Chords
python3 scripts/build_hymnal.py

# 3. Generate native FreeShow (.show) presentation files
python3 scripts/generate_freeshow.py

# 4. Generate authentic 4-part SATB MusicXML for MuseScore
~/.venv/bin/python scripts/generate_satb_musicxml.py

# 5. Generate melody-only sheet music lead sheets across 6 instrument parts (4,176 PDFs)
~/.venv/bin/python scripts/generate_melody_sheet_music.py
```

