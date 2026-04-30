# Typography Spec

## Font

All text elements in generated SVG diagrams must use:

```
font-family: 'DejaVu Sans', sans-serif
```

Font family names with spaces must be quoted in the SVG style attribute. This ensures consistent rendering across SVG viewers (Inkscape, librsvg/GNOME Loupe, browsers). DejaVu Sans is the primary font; `sans-serif` is the fallback.

The font metrics system (`text_utils.py`) uses `fc-match sans-serif` to discover the system font for Pillow-based width estimation. A 10% render margin (`RENDER_MARGIN = 1.10`) is applied to account for differences between Pillow and SVG renderer metrics.

## Font Size

All resource labels use **17px** as the base font size. The `px` unit is used in SVG (not `pt`) to avoid DPI-dependent interpretation differences between renderers.

## Label Positioning

Labels are placed inside their container rectangles:
- Icon: top-left inside rect with 2px padding
- Text: right of icon with 4px gap, baseline vertically centered on icon
- Container auto-sizes to fit the label width (icon + gap + text + right padding)
