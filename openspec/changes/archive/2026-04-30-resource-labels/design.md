# Design: Fix resource labels

## Architecture

```
ica_utils/
├── text_utils.py      ← NEW: font metrics, text width estimation
├── layout.py          ← UPDATED: variable column widths in Grid
├── resource_vpc.py    ← UPDATED: 13pt labels, inside containers, width-driven layout
├── cloudia_parser.py  ← unchanged
└── icalog.py          ← unchanged
```

## text_utils.py

### Font discovery

Use `fc-match` (fontconfig) to find the system sans-serif font:

```bash
fc-match sans-serif --format=%{file}
```

Falls back to Pillow's built-in default font if `fc-match` is unavailable.

### Metrics generation

On first call (or cache miss), use Pillow to measure all printable ASCII characters (32-126) at the requested font size:

```python
from PIL import ImageFont

font = ImageFont.truetype(font_path, size)
for char in range(32, 127):
    bbox = font.getbbox(chr(char))
    width = bbox[2] - bbox[0]
```

Per-character summation gives ~98% accuracy vs actual rendered text (2% kerning variance is acceptable for layout).

### Caching

Cache metrics as JSON in the extension directory:

```
ica_utils/.font_metrics_cache.json
```

Keyed by `"{font_path}:{font_size}"`. Cache is invalidated if the font path or size changes.

```json
{
  "/path/to/DejaVuSans.ttf:13": {
    " ": 4, "!": 5, "\"": 6, ...
  }
}
```

### Public API

```python
def estimate_text_width(text, font_size=13):
    """Estimate text width in pixels for the given font size."""

def get_font_height(font_size=13):
    """Return the line height for the given font size."""
```

## Grid: variable column widths

### Current

```python
Grid(cell_width=160, ...)  # all columns same width
```

### New

```python
Grid(col_widths=[180, 160, 220], ...)  # per-column widths
# or
Grid(col_widths=160, ...)  # single int = uniform (backwards compatible)
```

`cell_position(row, col)` sums widths + gaps of preceding columns for x offset.
`bounds(num_rows, num_cols)` uses sum of all column widths.

## Label positioning

Labels are placed inside their container rectangle:

```
┌──────────────────────────────────────┐
│🔲 subnet-EXAMPLE (172.31.16.0/20)  │
│                                      │
│                                      │
└──────────────────────────────────────┘
 ↑  ↑
 │  └── text at (x + icon_width + gap, y + font_size + padding)
 └───── icon at (x + padding, y + padding)
```

- Icon: top-left inside the rect with small padding
- Label: right of the icon, baseline at a comfortable y offset
- Font size: 13pt for all resource labels

## Column width calculation

For each AZ column, find the widest label among all subnets in that column:

```python
for col_idx, az in enumerate(azs):
    az_subnets = [s for s in vpc_subnets if s["az"] == az]
    widest = max(estimate_text_width(s["name"], 13) for s in az_subnets)
    col_widths[col_idx] = max(SUBNET_MIN_WIDTH, widest + label_padding)
```

`SUBNET_MIN_WIDTH` ensures columns don't get too narrow even with short labels.

## Key decisions

- **Pillow for measurement** — accurate, cross-platform, already in deps
- **`fc-match` for font discovery** — portable across Linux/macOS, falls back to Pillow default
- **Per-character cache** — generated once, reused across runs, ~98% accuracy
- **Variable column widths** — Grid accepts a list, each column independently sized
- **13pt base font size** — as specified in the bean, applies to all resource labels
- **Cache in extension dir** — persists across runs, keyed by font+size
