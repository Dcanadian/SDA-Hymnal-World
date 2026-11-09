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
- **Projection Ready**: Native ProPresenter files and OpenLyrics XML for FreeShow, OpenLP, and ProPresenter.

---

## Folder Structure

| Folder | Extension | File Count | Description |
| :--- | :--- | :--- | :--- |
| [`Database/`](file:///home/antigravity/SDA-Hymnal/Database) | `.json` | 695 | Canonical source-of-truth JSON metadata & stanzas per hymn |
| [`ChordPro/`](file:///home/antigravity/SDA-Hymnal/ChordPro) | `.cho` | 696 | Standard ChordPro files (`{start_of_verse}`, `{title}`) + Master index file |
| [`JustChords/`](file:///home/antigravity/SDA-Hymnal/JustChords) | `.cho` | 696 | Native JustChords format (`Verse 1:`, `Refrain:` tags) + Master index file |
| [`PlainText/`](file:///home/antigravity/SDA-Hymnal/PlainText) | `.txt` | 695 | Space-aligned Chords-Over-Lyrics text for any text editor |
| [`OnSong/`](file:///home/antigravity/SDA-Hymnal/OnSong) | `.onsong` | 695 | OnSong iPad/iOS/macOS worship presentation format |
| [`OpenLyrics/`](file:///home/antigravity/SDA-Hymnal/OpenLyrics) | `.xml` | 695 | OpenLyrics 0.9 XML with `<chord name="..."/>` tags for OpenLP & FreeShow |
| [`PDF-Chords/`](file:///home/antigravity/SDA-Hymnal/PDF-Chords) | `.pdf` | 695 | High-resolution 1-page printable vector chord charts |
| [`ProPresenter/`](file:///home/antigravity/SDA-Hymnal/ProPresenter) | `.txt` | 695 | Slide-divided text ready for batch import into ProPresenter / FreeShow |
| [`MusicXML/`](file:///home/antigravity/SDA-Hymnal/MusicXML) | `.musicxml` | 696 | Universal editable notation files for MuseScore, Finale, Sibelius, Dorico |
| [`Orchestral-Lead-Sheets/Bb-Instruments/`](file:///home/antigravity/SDA-Hymnal/Orchestral-Lead-Sheets/Bb-Instruments) | `.pdf` | 696 | Transposed +2 semitones (Trumpet, Clarinet, Tenor Sax) |
| [`Orchestral-Lead-Sheets/Eb-Instruments/`](file:///home/antigravity/SDA-Hymnal/Orchestral-Lead-Sheets/Eb-Instruments) | `.pdf` | 696 | Transposed +9 semitones (Alto Sax, Baritone Sax) |
| [`Orchestral-Lead-Sheets/F-Instruments/`](file:///home/antigravity/SDA-Hymnal/Orchestral-Lead-Sheets/F-Instruments) | `.pdf` | 696 | Transposed +7 semitones (French Horn) |
| [`Orchestral-Lead-Sheets/Bass-Clef/`](file:///home/antigravity/SDA-Hymnal/Orchestral-Lead-Sheets/Bass-Clef) | `.pdf` | 696 | Concert pitch (Cello, Trombone, Euphonium, Bassoon, Tuba, Bass) |
| [`Orchestral-Lead-Sheets/Alto-Clef/`](file:///home/antigravity/SDA-Hymnal/Orchestral-Lead-Sheets/Alto-Clef) | `.pdf` | 696 | Concert pitch (Viola) |

---

## Rebuilding & Generation Commands

```bash
# 1. Generate canonical JSON database for all 695 hymns
python3 scripts/generate_all_695.py

# 2. Compile into ChordPro, JustChords, PlainText, OnSong, OpenLyrics, and PDF-Chords
python3 scripts/build_hymnal.py

# 3. Generate editable MusicXML for MuseScore
~/.venv/bin/python scripts/generate_musicxml.py

# 4. Generate transposed orchestral lead sheets for all instrument parts (3,480 charts)
python3 scripts/generate_orchestral_leadsheets.py
```
