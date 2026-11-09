#!/usr/bin/env python3
"""
Compress and optimize the 724-page SDA Hymnal (1985) score PDF so it is < 90 MB
(safely under GitHub's 100 MB hard limit) while preserving high-contrast, razor-sharp
legibility for all 724 pages of sheet music.
Saves directly to /home/antigravity/SDA-Hymnal/SDA_Hymnal_1985.pdf for git inclusion.
"""

import os
import io
import time
from pathlib import Path
from PIL import Image
import pymupdf

SRC_PDF = Path("/home/antigravity/SDA-Hymnal/reference_scores/SDA_Hymnal_1985.pdf")
DEST_PDF = Path("/home/antigravity/SDA-Hymnal/SDA_Hymnal_1985.pdf")

print(f"Reading source PDF: {SRC_PDF} ({SRC_PDF.stat().st_size / (1024*1024):.1f} MB)...")
start_time = time.time()

doc = pymupdf.open(str(SRC_PDF))
new_doc = pymupdf.open()
total_pages = len(doc)
print(f"Optimizing {total_pages} pages to grayscale 1020px JPEG quality 60...")

for i in range(total_pages):
    page = doc[i]
    il = page.get_images()
    if il:
        xref = il[0][0]
        base_img = doc.extract_image(xref)
        img_bytes = base_img["image"]
        pil_img = Image.open(io.BytesIO(img_bytes)).convert("L")
        
        w, h = pil_img.size
        new_w = 1020
        new_h = int(h * (1020 / w))
        pil_img = pil_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        
        out_buf = io.BytesIO()
        pil_img.save(out_buf, format="JPEG", quality=60, optimize=True)
        
        new_page = new_doc.new_page(width=page.rect.width, height=page.rect.height)
        new_page.insert_image(page.rect, stream=out_buf.getvalue())
    else:
        # Vector / text page
        new_doc.insert_pdf(doc, from_page=i, to_page=i)
        
    if (i + 1) % 100 == 0 or (i + 1) == total_pages:
        print(f"  Processed {i + 1}/{total_pages} pages...")

print("Saving optimized PDF...")
new_doc.save(str(DEST_PDF), deflate=True, garbage=4, clean=True)
elapsed = time.time() - start_time
dest_mb = DEST_PDF.stat().st_size / (1024 * 1024)
print(f"Successfully created {DEST_PDF} ({dest_mb:.1f} MB) in {elapsed:.1f}s!")
