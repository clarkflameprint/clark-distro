import re
import json
import toml
from pathlib import Path

# Paths
EMOJI_MACROS_PATH = Path("config/Clark_Core_EmojiMacros.txt")
GLYPHSET_PATH = Path("config/Clark_Core_InnerGlyphset.txt")
GLYPH_MAP_JSON = Path("config/glyph_map.json")
GLYPH_REGISTRY_TOML = Path("config/glyph_registry.toml")

def parse_emoji_macros():
    macros = {}
    with open(EMOJI_MACROS_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            match = re.match(r'^([A-Z_]+)\s*=\s*"(.*?)"', line)
            if match:
                key, value = match.groups()
                macros[key] = value
    return macros

def parse_inner_glyphset():
    glyphs = {}
    with open(GLYPHSET_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split("  ")
            if len(parts) >= 2:
                glyph, desc = parts[0].strip(), parts[1].strip()
                glyphs[glyph] = desc
    return glyphs

def build_registry():
    emoji_macros = parse_emoji_macros()
    glyphset = parse_inner_glyphset()

    # Save as JSON map
    flat_map = {**emoji_macros, **glyphset}
    with open(GLYPH_MAP_JSON, 'w', encoding='utf-8') as jf:
        json.dump(flat_map, jf, ensure_ascii=False, indent=2)

    # Save as TOML registry
    toml_registry = {"emoji_macros": emoji_macros, "inner_glyphset": glyphset}
    with open(GLYPH_REGISTRY_TOML, 'w', encoding='utf-8') as tf:
        toml.dump(toml_registry, tf)

    print("Glyph registry and map generated.")

if __name__ == "__main__":
    build_registry()

