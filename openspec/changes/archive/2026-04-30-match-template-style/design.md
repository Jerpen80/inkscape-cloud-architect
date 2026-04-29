# Design: Match template visual style

## Current vs Target

```
Current (11px icons):                    Target (40px icons, matching template):
┌──────────────────────────┐             ┌───────────────────────────────────┐
│▪ subnet-0daf... (172.31) │             │ ┌────┐                            │
│                          │  35px       │ │icon│ subnet-0daf... (172.31)    │  50px
│                          │             │ └────┘                            │
└──────────────────────────┘             └───────────────────────────────────┘
  icon: 11px, text at top                  icon: 40px, text centered on icon
```

## Icon scaling

Template: `scale(0.26458)` in mm-based SVG → 40 × 0.26458mm = 10.58mm = **40px**
Our SVG is px-based, so we need `scale(1.0)` for 40px icons.

```python
# Current
ICON_SCALE = 0.275   # → 40 * 0.275 = 11px

# New
ICON_SCALE = 1.0     # → 40 * 1.0 = 40px
ICON_SIZE = 40
```

## Cell sizing

With 40px icons, cells need more height:

```python
# Current          # New
SUBNET_HEIGHT = 35  →  50    # 40px icon + 2px top + 8px bottom
VPC_PADDING_TOP = 30  →  50  # 40px icon + label needs more space
```

## Label positioning

Text baseline aligns with icon vertical center:

```python
icon_y = rect_y + ICON_PADDING          # 2px from top
text_y = icon_y + ICON_SIZE / 2 + font_ascent / 2  # centered on icon
text_x = icon_x + ICON_SIZE + LABEL_ICON_GAP
```

## Label width calculation

With larger icons, the icon takes more horizontal space:

```python
def _label_width(name):
    text_w = estimate_text_width(name, FONT_SIZE_PX)
    return ICON_PADDING + ICON_SIZE + LABEL_ICON_GAP + text_w + LABEL_PADDING_RIGHT
```
