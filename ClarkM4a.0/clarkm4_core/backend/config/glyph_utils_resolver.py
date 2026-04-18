# glyph_utils_resolver.py

from .glyph_utils import glyph_map

def resolve_glyph(glyph_key):
    """
    Resolves a glyph by its symbolic key from the glyph map.

    Parameters:
        glyph_key (str): The key for the symbolic glyph to retrieve.

    Returns:
        str: The glyph string if found, otherwise a fallback marker.
    """
    return glyph_map.get(glyph_key, f"[UNRESOLVED:{glyph_key}]")

