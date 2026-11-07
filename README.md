# Seventh-day Adventist Hymnal (1985) — Multi-Format Worship & Musician Suite

A score-faithful digital edition of the **Seventh-day Adventist Hymnal (1985)** rebuilt directly from the 4-part SATB hymnal sheet music.

## Key Features

- **Score-Faithful Practical Worship Harmony**: Functional harmonic rhythm derived directly from the 4-part SATB hymnal score—including musical slash chords (`F/A`, `F/C`, `C7/G`, `D/F#`, `E7/G#`), secondary dominants, and cadential `V7`/`sus4` chords that match the actual piano/organ score.
- **Chords on Every Stanza & Refrain**: Every verse (`Verse 1`, `Verse 2`, `Verse 3`, …) and `Refrain` has full inline chord placement so musicians never have to scroll back to Verse 1.
- **Clean Unhyphenated Lyrics**: Chords are anchored at exact syllable positions without inserting mid-word hyphens (`Al[F/C]might[Dm7]y`).
- **Single Canonical Database (`Database/`)**: Every hymn is stored in a structured JSON schema and compiled into all target formats via [`scripts/build_hymnal.py`](file:///home/antigravity/SDA-Hymnal/scripts/build_hymnal.py).

## Folder Structure

| Folder | Extension | Description |
| :--- | :--- | :--- |
| `Database/` | `.json` | Canonical source-of-truth JSON per hymn (`001`–`695`) |
| `ChordPro/` | `.cho` | Standard ChordPro files (`{start_of_verse}` / `{start_of_chorus}`) + `000 - SDA Hymnal Master.cho` |
| `JustChords/` | `.cho` | Native JustChords format (`Verse 1:` / `Refrain:` labels, metadata tags) + `000 - SDA Hymnal JustChords Master.cho` |
| `PlainText/` | `.txt` | Traditional Chords-Over-Lyrics space-aligned plain text |
| `OnSong/` | `.onsong` | OnSong iPad/Mac worship format |
| `OpenLyrics/` | `.xml` | OpenLyrics 0.9 standard XML with inline `<chord name="..."/>` tags |
| `PDF-Chords/` | `.pdf` | Clean Modern Worship Chart 1-page printable vector PDFs |

## Rebuilding All Formats

```bash
python3 scripts/seed_pilot_001_020.py
python3 scripts/build_hymnal.py
```
