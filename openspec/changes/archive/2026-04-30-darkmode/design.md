## Context

Colors are scattered across 15+ rendering modules as hardcoded constants (`COLOR_PURPLE`, `COLOR_GREEN`, etc.) or implicit defaults (text defaults to black via SVG inheritance). Text elements never set an explicit `fill` color — they rely on the SVG default of black. This makes it impossible to generate diagrams for dark backgrounds without changing code.

AWS icon symbols use colored fills on white/transparent backgrounds. Testing confirmed they render well on both light and dark backgrounds — no dark-variant symbol files are needed.

## Goals / Non-Goals

**Goals:**
- User can select Light or Dark theme from the Inkscape extension dialog
- Dark mode produces a diagram with light text, appropriate border colors, and an optional dark background
- All colors are config-driven so users can customize beyond the two presets
- Headless runner supports theme selection

**Non-Goals:**
- Custom color themes beyond light/dark presets (config supports it, but we only ship two)
- Dark-variant icon symbols (existing icons work on both backgrounds)
- Gradient or complex background fills (solid color only)

## Decisions

### 1. Theme resolution: INX parameter → config fallback

The `--theme` INX parameter (`light` or `dark`) selects which color palette to use. The config provides the palettes:

```yaml
theme:
  light:
    background: "none"
    text_color: "#000000"
    text_dimmed_opacity: 0.6
    border_account: "#000000"
    border_edge: "#7B61FF"
    border_vpc: "#8c4fff"
    border_subnet_public: "#7aa116"
    border_subnet_private: "#00a4a6"
    border_region: "#00a4a6"
  dark:
    background: "#232F3E"
    text_color: "#e0e0e0"
    text_dimmed_opacity: 0.5
    border_account: "#e0e0e0"
    border_edge: "#9B81FF"
    border_vpc: "#8c4fff"
    border_subnet_public: "#7aa116"
    border_subnet_private: "#00a4a6"
    border_region: "#00a4a6"
```

Dark background uses `#232F3E` — the official AWS dark navy. Most border colors stay the same since they're bright enough on dark. Only account and edge borders lighten.

**Alternative considered**: A single `mode: dark` toggle with hardcoded palettes. Rejected because config-driven colors allow user customization.

### 2. Palette passed as resolved dict

At startup, `effect()` resolves the theme name to a palette dict and stores it on `self.theme`. Rendering modules receive it via `config` (which already flows everywhere) — the theme is added as `config["_theme"]` so it doesn't pollute the serializable config.

Each renderer calls a helper like `get_text_color(config)` or `get_border_color(config, "vpc")` to get the resolved color.

### 3. Theme helper module

A new `ica_utils/theme.py` module provides:
- `resolve_theme(theme_name, config)` → returns palette dict
- `get_text_color(config)` → returns text fill color
- `get_text_dimmed_opacity(config)` → returns dimmed opacity
- `get_border_color(config, element)` → returns border color for a named element
- `get_background(config)` → returns background color or "none"

This centralizes theme logic. Renderers import from `theme` instead of each defining their own color constants.

### 4. Text style: explicit fill color

Currently text elements don't set `fill`, relying on SVG default (black). For dark mode, every text element MUST set `fill` explicitly to the theme text color. The style dict gains `'fill': theme_text_color`.

Dimmed text uses `'fill': theme_text_color` + `'fill-opacity': theme_dimmed_opacity`.

### 5. Background: full-canvas rect on bottom layer

When `background != "none"`, a filled rectangle is added as the bottommost element covering the full document. This is rendered after `resize_to_fit()` so it matches the final document dimensions.

### 6. Structural border colors stay mostly the same

VPC purple, subnet green/teal, region teal — these are bright AWS-standard colors that work on both backgrounds. Only account border (black → light gray) and edge border (slightly brighter purple) change in dark mode.

Span line colors (LB orange, EKS orange) are already config-driven and bright enough — no change needed.

## Risks / Trade-offs

- [Cross-cutting change] → Every rendering module needs updating. But the change per module is mechanical: add `fill` to text styles, replace hardcoded `COLOR_*` with `get_border_color()`. Low risk of logic bugs.
- [SVG default text color] → If a module misses the explicit `fill`, text will still be black and invisible on dark. Testing with dark mode catches this immediately.
- [Config bloat] → Theme section adds ~20 lines to config. Acceptable — it's a self-contained section.
