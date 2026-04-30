# Visual Style Spec

All generated diagrams must match the visual style of the hand-crafted templates in `templates/`.

## Reference

The reference template is `templates/AWS multi-AZ Web Appication.svg` which uses mm-based document units. All values below are converted to px (at 96 DPI) for our px-based output.

## Icons

- Symbols are 40x40 in their source coordinate space
- Template renders them at `scale(0.26458)` in mm = **40px** rendered size
- Icons are placed at the **top-left corner** of their container rect
- Icon padding from rect edge: ~2px

## Typography

- Font family: `'DejaVu Sans', sans-serif`
- Font size: **17px** (= 4.586mm in template = ~13pt)
- Text baseline aligns vertically with the **center of the icon**
- Text is placed right of the icon with a small gap

## Container Rectangles

- Stroke width: 0.5
- Fill: none
- VPC: stroke `#8c4fff` (purple)
- Public subnet: stroke `#7aa116` (green)
- Private subnet: stroke `#00a4a6` (blue)
- Containers auto-size to fit their label + icon + padding

## Layout Constants (in px)

| Constant | Value | Notes |
|---|---|---|
| Icon rendered size | 40px | scale(1.0) in px-based SVG |
| Icon padding from rect edge | 2px | top and left |
| Label gap from icon | 4px | horizontal gap |
| Label right padding | 10px | space after text to rect edge |
| Subnet min width | 120px | minimum cell width |
| Subnet height | 50px | increased to fit 40px icon + padding |
| Column gap | 10px | between AZ columns |
| Row gap | 15px | between subnet rows |
| VPC padding top | 50px | space for VPC label + icon |
| VPC padding sides | 15px | left and right |
| VPC padding bottom | 15px | below last row |
| VPC gap | 25px | between stacked VPCs |
