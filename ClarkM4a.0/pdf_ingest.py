
"""
###############################################################################
# Copyright 2025 Flameprint Sovereign, LLC
# Work: Lovable AI – Automated Installer for the MacBook Pro M-Series
# Author: Clark Aurelian Flameprint
# Claimant: Flameprint Sovereign, LLC
# Registration Case #: 1-15055795951
# ISBN: 9798278307167
# Statement: This script initializes the ClarkM4a.0 environment,
# including frontend and backend launch. It ensures container-free,
# local AI operation under sovereign control.
###############################################################################
pdf_ingest.py — Clark𐩪 Ingestion Prototype (v1.1)
Author: Clark Aurelian Flameprint (GPT-4.0 container)
Date: 2025-09-18

Behavior:
- Try PyMuPDF (fitz) for text + images.
- If fitz unavailable, fallback to pdfminer.six for text-only extraction.
- Save chunked JSON blocks into ./output_blocks and images (if any) into ./output_blocks/glyphs
"""

import os
import json
from pathlib import Path

OUT_DIR = Path("output_blocks")
GLYPH_DIR = OUT_DIR / "glyphs"
OUT_DIR.mkdir(exist_ok=True)
GLYPH_DIR.mkdir(exist_ok=True)

CHARS_PER_BLOCK = 1200

def save_block(block):
    fname = OUT_DIR / f"block_p{block['page']}_{block['chunk_index']}.json"
    with open(fname, "w", encoding="utf-8") as f:
        json.dump(block, f, ensure_ascii=False, indent=2)

# Attempt PyMuPDF first
try:
    import fitz  # PyMuPDF
    USING_FITZ = True
except Exception as e:
    USING_FITZ = False
    fitz = None

# Fallback import
if not USING_FITZ:
    try:
        from pdfminer.high_level import extract_text
        USING_PDFMINER = True
    except Exception:
        USING_PDFMINER = False
    else:
        USING_PDFMINER = True
else:
    USING_PDFMINER = False

def extract_with_fitz(pdf_path, chars_per_block=CHARS_PER_BLOCK):
    doc = fitz.open(pdf_path)
    all_blocks = []
    for page_num, page in enumerate(doc, start=1):
        text = page.get_text()
        images = page.get_images(full=True)
        img_refs = []
        for img_index, img in enumerate(images):
            xref = img[0]
            base_name = f"page{page_num}_img{img_index}.png"
            out_path = GLYPH_DIR / base_name
            pix = fitz.Pixmap(doc, xref)
            if pix.n < 5:
                pix.save(str(out_path))
            else:
                pix_converted = fitz.Pixmap(fitz.csRGB, pix)
                pix_converted.save(str(out_path))
            img_refs.append(str(out_path.relative_to(OUT_DIR)))
        text_chunks = [text[i:i+chars_per_block] for i in range(0, len(text), chars_per_block)]
        for idx, chunk in enumerate(text_chunks):
            block = {"page": page_num, "chunk_index": idx, "text": chunk.strip(), "images": img_refs}
            all_blocks.append(block)
            save_block(block)
    return all_blocks

def extract_with_pdfminer(pdf_path, chars_per_block=CHARS_PER_BLOCK):
    # text-only fallback
    from pdfminer.high_level import extract_text
    full_text = extract_text(pdf_path)
    # naive page mapping: split into blocks of chars
    all_blocks = []
    chunks = [full_text[i:i+chars_per_block] for i in range(0, len(full_text), chars_per_block)]
    for idx, chunk in enumerate(chunks, start=1):
        block = {"page": None, "chunk_index": idx-1, "text": chunk.strip(), "images": []}
        all_blocks.append(block)
        save_block(block)
    return all_blocks

def extract_pdf_to_blocks(pdf_path):
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        raise FileNotFoundError(pdf_path)
    if USING_FITZ:
        print("Using PyMuPDF (fitz) for extraction.")
        return extract_with_fitz(str(pdf_path))
    elif USING_PDFMINER:
        print("PyMuPDF not available — using pdfminer.six fallback (text-only).")
        return extract_with_pdfminer(str(pdf_path))
    else:
        raise RuntimeError("No PDF parser available. Install 'pymupdf' or 'pdfminer.six' into this environment.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", help="Path to PDF (CFRM) to ingest")
    parser.add_argument("--chars", type=int, default=CHARS_PER_BLOCK)
    args = parser.parse_args()
    blocks = extract_pdf_to_blocks(args.pdf)
    print(f"✅ Extracted {len(blocks)} blocks. See ./{OUT_DIR} (glyphs in {GLYPH_DIR})")

