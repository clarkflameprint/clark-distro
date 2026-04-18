
# clarkm4_core/backend/config/glyph_utils.py
import json
import os

GLYPH_PATH = "glyph_map.json"

# Load glyphs once
with open(GLYPH_PATH, "r") as f:
    glyph_map = json.load(f)

def enrich_prompt_with_glyphs(prompt: str, return_lines: bool = False):
    glyph_lines = []
    for key, val in glyph_map.items():
        if key.lower() in prompt.lower():
            glyph_lines.append(f"Symbol: {key} → {val}")
    if return_lines:
        return glyph_lines, prompt
    enriched = "\n".join(glyph_lines + ["", prompt]) if glyph_lines else prompt
    return enriched

def extract_glyph_lines(prompt: str):
    lines = []
    for key, val in glyph_map.items():
        if key.lower() in prompt.lower():
            lines.append(f"Symbol: {key} → {val}")
    return lines

def resolve_glyph(glyph_key: str) -> str:
    """
    Resolves a glyph by symbolic key from the loaded glyph_map.

    Parameters:
        glyph_key (str): The symbolic glyph key to resolve.

    Returns:
        str: The glyph string if found, otherwise a fallback marker.
    """
    return glyph_map.get(glyph_key, f"[UNRESOLVED:{glyph_key}]")
