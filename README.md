# Seventh-day Adventist Hymnal (1985) — Multi-Format Worship & Musician Suite

A comprehensive, score-faithful digital edition of the **Seventh-day Adventist Hymnal (1985, Hymns 001–695)** compiled into all major chord, lyric, and projection formats.

---

## Key Features

- **All 695 Hymns**: The entire 1985 Seventh-day Adventist Hymnal is converted across all major worship file formats.
- **Clean Triad & 7th Chords (Zero Clutter)**: Formatted with clean root-name triads and dominant 7ths (`F`, `Dm`, `C`, `Am`, `Bb`, `Gm`, `A`, `C7`) without distracting slash-bass inversions or jazz clutter—matching the clean display of the [JustChords iOS app](https://apps.apple.com/).
- **Exact Syllable-Under-Chord Alignment**: In both Chords-Over-Lyrics plain text and 1-page printable vector PDF charts, every chorded syllable starts directly underneath its chord letter (e.g., `Al` under `Dm`, `might` under `Am`, `y,` under `Bb`). Melismatic cadences (`cre a     tion!`) place transitional chords over sustained vowel space and landing chords directly over word endings.
- **Unhyphenated Contiguous Lyrics**: Chords are placed inline at the exact syllable boundary without mid-word hyphens (`[Dm]Al[Am]might[Bb]y,`, `[Dm]cre[Bb]a[C7][F]tion!`).
- **Chords on Every Verse & Refrain**: Every stanza (`Verse 1`, `Verse 2`, `Verse 3`…) and `Refrain` includes chords so musicians never have to scroll back to Verse 1.
- **Projection Ready**: Includes native ProPresenter files for worship projection.

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

---

## Rebuilding All Formats

To regenerate the entire collection:

```bash
# 1. Generate canonical JSON database for all 695 hymns
python3 scripts/generate_all_695.py

# 2. Compile into ChordPro, JustChords, PlainText, OnSong, OpenLyrics, and PDF-Chords
python3 scripts/build_hymnal.py
```
