#!/usr/bin/env python3
"""
Populate missing Lyricist, Composer, Tune Name, and Meter across all 695 hymns in Database/*.json.

Sources:
1. Tune Name: Extracted directly from MIDI track_name metadata (e.g. '#001 Lobe Den Herren ... S A T B').
2. Meter: Computed from the stanza syllable patterns (and standard hymnal shorthand: C.M., S.M., L.M., 8.7.8.7.D., etc.).
3. Lyricist & Composer: Extracted via high-DPI Tesseract OCR on the left and right credit boxes of the first page of each hymn in Sheet-Music/reference_scores/SDA_Hymnal_1985.pdf.
"""

from difflib import SequenceMatcher
import glob
import json
import os
import re
import subprocess
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
import fitz
import mido

ROOT_DIR = Path("/home/antigravity/SDA-Hymnal")
DB_DIR = ROOT_DIR / "Database"
MIDI_DIR = ROOT_DIR / "MIDI"
PDF_PATH = ROOT_DIR / "Sheet-Music" / "reference_scores" / "SDA_Hymnal_1985.pdf"
if not PDF_PATH.exists():
    PDF_PATH = ROOT_DIR / "Sheet-Music" / "SDA_Hymnal_1985.pdf"

CHORD_RE = re.compile(r"\[[^\]]*\]")


def count_word_syllables(word: str) -> int:
    w = re.sub(r"[^a-z]", "", word.lower())
    if not w:
        return 0
    groups = re.findall(r"[aeiouy]+", w)
    n = len(groups)
    if w.endswith("e") and not w.endswith(("le", "ee", "ie", "ye")) and n > 1:
        n -= 1
    if re.search(r"(eth|est)$", w) is None and w.endswith("ed") and n > 1 and not w.endswith(("ted", "ded")):
        n -= 1
    return max(1, n)


def compute_meter(h: dict) -> str:
    sections = h.get("sections", [])
    verses = [s for s in sections if s.get("type") == "verse"]
    if not verses:
        return "Irregular"
    lines = verses[0].get("lines", [])
    if not lines:
        return "Irregular"
    counts = []
    for ln in lines:
        clean_ln = CHORD_RE.sub("", ln)
        words = [w for w in clean_ln.split() if re.sub(r"[^a-zA-Z]", "", w)]
        c = sum(count_word_syllables(w) for w in words)
        if c > 0:
            counts.append(c)
    if not counts:
        return "Irregular"

    has_refrain = any(s.get("type") in ("chorus", "refrain") for s in sections)
    pat = ".".join(str(c) for c in counts)
    shorthands = {
        "8.6.8.6": "C.M.",
        "8.6.8.6.8.6.8.6": "C.M.D.",
        "6.6.8.6": "S.M.",
        "6.6.8.6.6.6.8.6": "S.M.D.",
        "8.8.8.8": "L.M.",
        "8.8.8.8.8.8.8.8": "L.M.D.",
        "7.7.7.7": "7s",
        "7.7.7.7.7.7.7.7": "7s D.",
        "8.7.8.7": "8.7.8.7.",
        "8.7.8.7.8.7.8.7": "8.7.8.7.D.",
        "7.6.7.6": "7.6.7.6.",
        "7.6.7.6.7.6.7.6": "7.6.7.6.D.",
        "6.5.6.5": "6.5.6.5.",
        "6.5.6.5.6.5.6.5": "6.5.6.5.D.",
        "10.10.10.10": "10s",
        "11.10.11.10": "11.10.11.10.",
    }
    base = shorthands.get(pat, pat)
    if has_refrain and not base.endswith("with Refrain"):
        return f"{base} with Refrain" if base in ("C.M.", "S.M.", "L.M.") else base
    return base


def extract_tune_from_midi(num: int) -> str:
    mid_p = MIDI_DIR / f"{num:03d}.mid"
    if not mid_p.exists():
        return ""
    try:
        m = mido.MidiFile(str(mid_p))
        for tr in m.tracks:
            for msg in tr:
                if msg.type == "track_name":
                    t = msg.name.strip()
                    if "#" in t or re.match(r"^\d+", t):
                        t_clean = re.sub(r"^\s*#?\s*\d+[a-zA-Z]?\s*", "", t)
                        t_clean = re.split(r"\.\.\.|\(Unison|Unison Setting", t_clean)[0].strip()
                        t_clean = re.sub(r"\s*\((?:a\.?k\.?a\.?|also known as).*?\)", "", t_clean, flags=re.I).strip()
                        if t_clean and not re.match(r"^[SATB\s]+$", t_clean):
                            return t_clean.upper()
    except Exception:
        pass
    return ""


def clean_credit_str(s: str) -> str:
    s = re.sub(r"[|_=~—–«»<>•*#\"“”‘’`]+", " ", s)
    s = re.sub(r"\s+", " ", s).strip(" .,-:;'/\\")
    # Remove wrapped lowercase title words prepended to right-hand composer credit
    s = re.sub(r"^(?:on|a|an|as|ex|in|to|of)\s+", "", s)
    s = re.sub(r"\s+a$", "", s)
    # Fix common OCR substitutions on italicized initials
    s = re.sub(r"\bFE[:;,.]?\s+", "F. ", s)
    s = re.sub(r"\bF\s+E\.\s+Belden\b", "F. E. Belden", s)
    s = re.sub(r"\bJS\.\s*", "J. S. ", s)
    s = re.sub(r"\bTrish\b", "Irish", s)
    s = re.sub(r"\bobert Lowry\b", "Robert Lowry", s)
    s = re.sub(r"P\.\s*7\s*P\.?\s*Bliss", "P. P. Bliss", s)
    s = re.sub(r"seoree.*Ele.*", "George J. Elvey", s)
    s = re.sub(r"George\s+ne\s+Whelpton", "George Whelpton", s)
    s = re.sub(r"Albert\s+F-\s+Bayly", "Albert F. Bayly", s)
    if len(s) < 3 or sum(c.isalpha() for c in s) < 3:
        return ""
    if re.match(r"^(First|Second|Unison|Harmony|Setting|Arrangement|Refrain|Verse|Chorus|Optional|Slower)\b", s, re.I):
        return ""
    return s


def ocr_page_header(page_idx: int):
    doc = fitz.open(str(PDF_PATH))
    page = doc[page_idx]
    r = page.rect
    clip = fitz.Rect(0, 0, r.width, r.height * 0.081)
    tmp_img = f"/tmp/ocr_p_{page_idx}_{os.getpid()}.png"
    page.get_pixmap(dpi=250, clip=clip).save(tmp_img)
    try:
        tsv = subprocess.check_output(
            ["tesseract", tmp_img, "stdout", "--psm", "6", "tsv"],
            stderr=subprocess.DEVNULL
        ).decode("utf-8", errors="ignore")
    except Exception:
        if os.path.exists(tmp_img):
            os.remove(tmp_img)
        return page_idx, "", "", ""
    if os.path.exists(tmp_img):
        os.remove(tmp_img)

    words = []
    for line in tsv.splitlines()[1:]:
        parts = line.split("\t")
        if len(parts) >= 12 and parts[11].strip() and int(parts[6]) > 0:
            left, top, w, h_px, conf, text = (
                int(parts[6]), int(parts[7]), int(parts[8]),
                int(parts[9]), float(parts[10]), parts[11].strip()
            )
            words.append((top, left, w, h_px, text))

    top_words = sorted([w for w in words if w[0] < 105], key=lambda x: x[1])
    cred_words = sorted([w for w in words if 105 <= w[0] <= 190], key=lambda x: x[1])

    title_line = " ".join(w[4] for w in top_words)
    left_cred = " ".join(w[4] for w in cred_words if w[1] < 960)
    right_cred = " ".join(w[4] for w in cred_words if w[1] >= 960)

    return page_idx, title_line, clean_credit_str(left_cred), clean_credit_str(right_cred)


def norm_text(s: str) -> str:
    return re.sub(r"[^a-z0-9 ]", "", s.lower()).strip()


MANUAL_OVERRIDES = {
    158: ("African-American Spiritual", "African-American Spiritual"),
    319: ("African-American Spiritual", "African-American Spiritual"),
    436: ("Hugh R. Haweis", "Arthur S. Sullivan"),
    627: ("African-American Spiritual", "African-American Spiritual"),
    663: ("Traditional", "Traditional"),
    664: ("Traditional", "John Stainer"),
    684: ("Psalm 143:1", "George Whelpton"),
}


def main():
    db_files = sorted(glob.glob(str(DB_DIR / "[0-9][0-9][0-9]*.json")))
    hymns = [json.loads(Path(f).read_text(encoding="utf-8")) for f in db_files]

    doc = fitz.open(str(PDF_PATH))
    num_pages = len(doc)
    doc.close()

    cache_file = Path("/tmp/ocr_cache.json")
    if cache_file.exists():
        print("Loading cached OCR header results from /tmp/ocr_cache.json...")
        raw_cache = json.loads(cache_file.read_text(encoding="utf-8"))
        page_results = {int(k): tuple(v) for k, v in raw_cache.items()}
    else:
        print(f"Scanning headers across {num_pages} pages of SDA_Hymnal_1985.pdf with 4 workers...")
        page_results = {}
        with ProcessPoolExecutor(max_workers=4) as ex:
            futs = [ex.submit(ocr_page_header, p) for p in range(num_pages)]
            for fut in as_completed(futs):
                p_idx, t_line, l_cred, r_cred = fut.result()
                page_results[p_idx] = (t_line, l_cred, r_cred)
        cache_file.write_text(json.dumps(page_results, ensure_ascii=False), encoding="utf-8")

    cur_p = 0
    matched_credits = {}
    for h in hymns:
        num = h["number"]
        t_target = norm_text(h["title"])
        best_p, best_score = None, 0.0
        for p in range(max(0, cur_p - 1), min(num_pages, cur_p + 15)):
            raw_t = page_results[p][0].strip()
            t_ocr = norm_text(re.sub(r"^\S*\d+\S*\s*", "", raw_t))
            if not t_ocr:
                continue
            ratio = SequenceMatcher(None, t_target, t_ocr).ratio()
            if t_target in t_ocr or (len(t_target) > 8 and t_target[:10] in t_ocr):
                ratio = max(ratio, 0.95)
            # Penalize page-2 continuation headers ("2 Title...") so Page 1 is always preferred
            if num != 2 and re.match(r"^2\s+", raw_t):
                ratio -= 0.15
            if ratio > best_score:
                best_score, best_p = ratio, p

        if best_score >= 0.55:
            cur_p = best_p + 1
            while cur_p < num_pages:
                t_next = norm_text(re.sub(r"^\S*\d+\S*\s*", "", page_results[cur_p][0]))
                if SequenceMatcher(None, t_target, t_next).ratio() >= 0.7:
                    cur_p += 1
                else:
                    break
        else:
            best_p = min(num_pages - 1, cur_p)
            cur_p += 1

        l_cred = clean_credit_str(page_results[best_p][1])
        r_cred = clean_credit_str(page_results[best_p][2])
        if num in MANUAL_OVERRIDES:
            l_cred, r_cred = MANUAL_OVERRIDES[num]
        if not l_cred and r_cred:
            l_cred = "Traditional" if "Traditional" in r_cred or "Spiritual" in r_cred else "Anonymous"
        if not r_cred and l_cred:
            r_cred = l_cred if "Spiritual" in l_cred or "Traditional" in l_cred else "Traditional"
        matched_credits[num] = (l_cred, r_cred)

    updated_count = 0
    for f_path, h in zip(db_files, hymns):
        num = h["number"]
        l_cred, r_cred = matched_credits.get(num, ("", ""))
        if l_cred:
            h["lyricist"] = l_cred
        if r_cred:
            h["composer"] = r_cred
        t_midi = extract_tune_from_midi(num)
        if t_midi:
            h["tune"] = t_midi
        elif not h.get("tune"):
            h["tune"] = re.sub(r"[^A-Z ]", "", h["title"].upper()).strip()[:24]
        h["meter"] = compute_meter(h)

        Path(f_path).write_text(json.dumps(h, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        updated_count += 1

    has_l = sum(1 for h in hymns if h.get("lyricist"))
    has_c = sum(1 for h in hymns if h.get("composer"))
    has_t = sum(1 for h in hymns if h.get("tune"))
    has_m = sum(1 for h in hymns if h.get("meter"))
    print(f"Updated {updated_count} hymns! Coverage: lyricist={has_l}, composer={has_c}, tune={has_t}, meter={has_m}")


if __name__ == "__main__":
    main()
