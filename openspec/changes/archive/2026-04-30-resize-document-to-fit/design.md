## Context

The SVG document starts with a fixed 800x600 canvas. The extension renders VPCs and subnets dynamically, but the document dimensions never adapt. This is the first feature that depends on the `configuration-yaml` change for its margin setting.

## Goals / Non-Goals

**Goals:**
- Automatically resize the document to tightly fit all rendered content
- Apply a configurable margin around the content

**Non-Goals:**
- Minimum document size enforcement
- Per-side margin configuration (uniform margin is sufficient)

## Decisions

### 1. Use Inkex `get_bbox()` after rendering
Rather than manually tracking bounds through the layout system, query the bounding box of all rendered SVG elements after rendering is complete. This is simpler, more robust, and automatically handles any future element types.

**Alternative considered**: Threading width/height returns through `render_vpc_with_subnets` and `Stack`. Rejected — more invasive, couples resize logic to layout code, and breaks if new element types are added.

### 2. Resize at end of `effect()`
The resize step runs as the last operation in `effect()`, after all VPCs and subnets are rendered. This guarantees all elements exist when `get_bbox()` is called.

### 3. Set both `width`/`height` and `viewBox`
Both attributes must be updated together to ensure correct rendering in browsers and Inkscape. The viewBox origin stays at `0 0`.

## Risks / Trade-offs

- [Bounding box accuracy] → Inkex's `get_bbox()` may not account for stroke widths or text overflow precisely. Acceptable — the margin provides a buffer.
- [Empty document] → If no data is loaded and nothing is rendered, `get_bbox()` may return None. Handle gracefully by skipping resize.
