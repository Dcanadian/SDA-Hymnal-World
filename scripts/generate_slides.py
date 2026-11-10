#!/usr/bin/env python3
"""
Generate ProPresenter (.txt) and FreeShow (.show) slides for every hymn.

Slides follow the phrasing of the lyrics: each slide holds 2-3 lines, and breaks are
placed where the text pauses (end of a sentence or clause) rather than mid-thought.

Run:  python3 scripts/generate_slides.py
"""
import glob
import json
import re
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DB_DIR = ROOT_DIR / "Database"
FREESHOW_DIR = ROOT_DIR / "Slides" / "FreeShow"
PROPRESENTER_DIR = ROOT_DIR / "Slides" / "ProPresenter"

CHORD_RE = re.compile(r"\[[^\]]*\]")
STRONG_END = (".", "!", "?", ";", ":")
WEAK_END = (",", "—", "-")


def clean(line: str) -> str:
    return re.sub(r"\s+", " ", CHORD_RE.sub("", line)).strip()


def break_cost(line: str, nxt: str) -> float:
    """Cost of ending a slide after `line` (lower = a more natural pause)."""
    t = line.rstrip("\"'”’)")
    if t.endswith(STRONG_END):
        return 0.0
    if t.endswith(WEAK_END):
        return 1.0
    # No punctuation: continuing a sentence (next line lowercase) is worst
    return 3.0 if nxt[:1].islower() else 2.0


def split_lines(lines):
    """Split lines into groups of 2-3 following the phrasing (DP, minimal break cost)."""
    n = len(lines)
    if n <= 3:
        return [lines]
    INF = float("inf")
    best = [INF] * (n + 1)
    prev = [0] * (n + 1)
    best[0] = 0.0
    for i in range(1, n + 1):
        for size in (2, 3):
            j = i - size
            if j < 0 or best[j] == INF:
                continue
            cost = best[j]
            cost += 0.4 if size == 3 else 0.0
            # Very long text on a 3-line slide is hard to read
            if size == 3 and sum(len(x) for x in lines[j:i]) > 105:
                cost += 1.5
            if i < n:
                cost += break_cost(lines[i - 1], lines[i])
            if cost < best[i]:
                best[i], prev[i] = cost, j
    if best[n] == INF:  # n == 1 handled above; fallback
        return [lines]
    groups, i = [], n
    while i > 0:
        groups.append(lines[prev[i]:i])
        i = prev[i]
    return groups[::-1]


def section_slides(sec):
    lines = [clean(l) for l in sec.get("lines", [])]
    lines = [l for l in lines if l]
    return split_lines(lines) if lines else []


def is_chorus(sec) -> bool:
    name = sec.get("name", "").lower()
    return sec.get("type") in ("chorus", "refrain") or "chorus" in name or "refrain" in name


def write_propresenter(h, base: str):
    out = [f"Title:#{h['number']} {h['title']}", f"Author:{h.get('lyricist', '')}", "", "Tag",
           f"SDA Hymnal #{h['number']}", h["title"], ""]
    for sec in h["sections"]:
        out.append(sec["name"])
        for gi, grp in enumerate(section_slides(sec)):
            out.extend(grp)
            out.append("")
    (PROPRESENTER_DIR / f"{base}.txt").write_text("\n".join(out).rstrip() + "\n", encoding="utf-8")


def write_freeshow(h, base: str):
    num, title = h["number"], h["title"]
    slides, layout_slides = {}, []
    group_first = {}  # section index -> list of slide ids
    for idx, sec in enumerate(h["sections"]):
        chorus = is_chorus(sec)
        ids = []
        for gi, grp in enumerate(section_slides(sec)):
            sid = f"slide_{idx}_{gi}"
            lines_data = [
                {
                    "align": "text-align:center;",
                    "text": [{"value": ln, "style": "font-size:60px;font-family:sans-serif;font-weight:600;line-height:1.4;"}],
                }
                for ln in grp
            ]
            slides[sid] = {
                "group": sec["name"],
                "color": "#e11d48" if chorus else "#2563eb",
                "settings": {"color": "", "resolution": {"width": 1920, "height": 1080}},
                "children": [],
                "notes": "",
                "items": [{
                    "type": "text",
                    "lines": lines_data,
                    "style": "top:100px;left:100px;height:880px;width:1720px;",
                    "align": "align-items:center;",
                }],
            }
            ids.append(sid)
        group_first[idx] = ids

    # Sequence: each verse is followed by the refrain (if the hymn has one)
    chorus_idx = next((i for i, s in enumerate(h["sections"]) if is_chorus(s)), None)
    for idx, sec in enumerate(h["sections"]):
        if is_chorus(sec):
            continue
        layout_slides.extend({"id": sid} for sid in group_first[idx])
        if chorus_idx is not None:
            layout_slides.extend({"id": sid} for sid in group_first[chorus_idx])

    data = {
        "name": f"{num:03d} - {title}",
        "category": h.get("category", "SDA Hymnal"),
        "settings": {"activeLayout": "default_layout", "template": None},
        "timestamps": {"created": 1700000000000, "modified": 1700000000000, "used": None},
        "meta": {
            "number": f"{num:03d}", "title": title, "artist": "",
            "author": h.get("lyricist", ""), "composer": h.get("composer", ""),
            "publisher": "Review and Herald Publishing Association",
            "copyright": "Public Domain" if num < 500 else "Seventh-day Adventist Hymnal",
            "CCLI": "", "year": "", "key": h.get("key", ""),
        },
        "slides": slides,
        "layouts": {"default_layout": {"name": "Default", "notes": "", "slides": layout_slides}},
        "media": {},
    }
    (FREESHOW_DIR / f"{base}.show").write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def main():
    FREESHOW_DIR.mkdir(parents=True, exist_ok=True)
    PROPRESENTER_DIR.mkdir(parents=True, exist_ok=True)
    for old in PROPRESENTER_DIR.glob("*.txt"):
        old.unlink()
    files = sorted(glob.glob(str(DB_DIR / "[0-9][0-9][0-9]*.json")))
    for f in files:
        h = json.loads(Path(f).read_text(encoding="utf-8"))
        safe = re.sub(r'[/\\:*?"<>|]', "", h["title"]).strip()
        base = f"{h['number']:03d} - {safe}"
        write_propresenter(h, base)
        write_freeshow(h, base)
    print(f"Generated ProPresenter + FreeShow slides (2-3 lines each) for {len(files)} hymns.")


if __name__ == "__main__":
    main()
