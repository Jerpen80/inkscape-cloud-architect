import os
import subprocess

_font_cache = {}
_font_path = None


def _discover_font():
    """Find system sans-serif font via fc-match, fallback to None (Pillow default)."""
    global _font_path
    if _font_path is not None:
        return _font_path

    try:
        result = subprocess.run(
            ["fc-match", "sans-serif", "--format=%{file}"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0 and result.stdout.strip():
            path = result.stdout.strip()
            if os.path.isfile(path):
                _font_path = path
                return _font_path
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass

    _font_path = ""
    return _font_path


def _get_font(font_size_px):
    """Get a Pillow font object for the given size, cached."""
    if font_size_px in _font_cache:
        return _font_cache[font_size_px]

    from PIL import ImageFont

    font_path = _discover_font()
    try:
        if font_path:
            font = ImageFont.truetype(font_path, font_size_px)
        else:
            font = ImageFont.load_default(size=font_size_px)
    except (OSError, TypeError):
        font = ImageFont.load_default()

    _font_cache[font_size_px] = font
    return font


RENDER_MARGIN = 1.10


def estimate_text_width(text, font_size_px=17):
    """Measure text width in pixels using Pillow (includes kerning).

    Applies a small margin to account for differences between Pillow's
    font metrics and SVG renderer metrics (hinting, subpixel spacing)."""
    font = _get_font(font_size_px)
    bbox = font.getbbox(str(text))
    return (bbox[2] - bbox[0]) * RENDER_MARGIN


def get_font_height(font_size_px=17):
    """Return the line height in pixels for the given font size."""
    font = _get_font(font_size_px)
    bbox = font.getbbox("Ag")
    return bbox[3] - bbox[1]
