# Design: Resource layers

## Inkscape layer format

Inkscape layers are SVG `<g>` elements with special attributes:

```xml
<g inkscape:groupmode="layer" inkscape:label="VPCs">
  <!-- VPC rects, icons, labels -->
</g>
<g inkscape:groupmode="layer" inkscape:label="Subnets">
  <!-- Subnet rects, icons, labels -->
</g>
```

Z-order: elements are painted in document order. First `<g>` is bottom, last is top.

## Layer utility (layers.py)

Shared utility — any resource renderer can request a named layer:

```python
def get_or_create_layer(inkdoc, name):
    """Get or create a named Inkscape layer. Returns the Group element."""
```

- Searches existing layers by `inkscape:label`
- If not found, creates a new `Group` with `inkscape:groupmode="layer"` and `inkscape:label`
- Appends to `inkdoc.svg`
- Returns the group for appending children

## Layer creation order

In `effect()` or at the start of rendering, create layers in z-order:

```python
# Bottom to top
get_or_create_layer(inkdoc, "VPCs")
get_or_create_layer(inkdoc, "Subnets")
```

This ensures VPC rects are always behind subnet rects regardless of rendering order.

## Changes to aws_rect

Currently `aws_rect` appends rect, icon, and text to `inkdoc.svg`. Updated to accept a `layer` parameter and append to that instead:

```python
def aws_rect(inkdoc, xy, wh, color, name, symid, layer):
    layer.append(rect)
    layer.append(icon_el)  # via make_symbol_instance
    layer.append(text_elem)
```

## Template reference

```
Template "AWS multi-AZ Web Appication.svg":
  Layer "root"                → background, region frame
  Layer "Availability Zones"  → AZ rects
  Layer "VPC"                 → VPC + subnet rects
  Layer "top"                 → icons, labels, arrows

Our approach (simpler, per resource class):
  Layer "VPCs"                → VPC rects + icons + labels
  Layer "Subnets"             → Subnet rects + icons + labels
```
