# Visual Style Spec

All generated diagrams must match the visual style of the hand-crafted templates in `templates/`.

## Reference

The reference template is `templates/AWS multi-AZ Web Appication.svg` which uses mm-based document units. All values below are converted to px (at 96 DPI) for our px-based output.

Layout constants are defined in `default-config.yaml` and can be overridden per-user in `~/.config/inkscape/extensions/aws-auto-diagram/config.yaml`.

## Icons

- Symbols are 40x40 in their source coordinate space
- Rendered at `scale(1.0)` = **40px** in our px-based SVG
- Icons are placed at the **top-left corner** of their container rect
- Icon padding from rect edge: 2px

## Typography

- Font family: `'DejaVu Sans', sans-serif`
- Font size: **17px** (= 4.586mm in template = ~13pt)
- Text baseline aligns vertically with the **center of the icon**
- Text is placed right of the icon with a small gap

## Container Rectangles

- Stroke width: 0.5
- Fill: none
- All border colors come from the resolved theme palette (see `theme` spec)
- VPC: default stroke `#8c4fff` (purple), solid
- Public subnet: default stroke `#7aa116` (green), solid
- Private subnet: default stroke `#00a4a6` (blue), solid
- Account: default stroke `#000000` (black, light) / `#e0e0e0` (dark), solid
- Availability Zone: stroke `#00a4a6` (blue), dashed `8,8`
- Containers auto-size to fit their label + icon + padding

## Availability Zones

- Dashed vertical columns inside each VPC, one per AZ
- Extend above and below the subnet rows (template style)
- Rendered on a dedicated "Availability Zones" layer between VPCs and Subnets
- Optional via `availability_zone.enabled` config
- When enabled, col_gap and VPC padding_top are increased to accommodate AZ rects

## Layers (z-order, bottom to top)

1. **Accounts** (optional) — account boundary rect
2. **VPCs** — VPC rects + icons + labels
3. **Availability Zones** (optional) — dashed AZ column rects + labels
4. **Subnets** — subnet rects + icons + labels

## Layout Constants (in px, from default-config.yaml)

| Constant | Config path | Value | Notes |
|---|---|---|---|
| Document margin | `document.margin` | 20 | around all content |
| Icon rendered size | — | 40px | scale(1.0) |
| Icon padding | — | 2px | top and left |
| Label gap from icon | — | 4px | horizontal |
| Label right padding | — | 10px | after text to rect edge |
| Account padding top | `layout.account.padding.top` | 50 | |
| Account padding sides | `layout.account.padding.right/left` | 20 | |
| Account padding bottom | `layout.account.padding.bottom` | 20 | |
| VPC padding top | `layout.vpc.padding.top` | 60 | space for VPC label + icon |
| VPC padding sides | `layout.vpc.padding.right/left` | 15 | |
| VPC padding bottom | `layout.vpc.padding.bottom` | 15 | |
| VPC gap | `layout.vpc.gap` | 25 | between stacked VPCs |
| Subnet min width | `layout.subnet.min_width` | 120 | minimum cell width |
| Subnet height | `layout.subnet.height` | 50 | fits 40px icon + padding |
| Column gap | `layout.subnet.col_gap` | 10 | base gap between AZ columns |
| Row gap | `layout.subnet.row_gap` | 15 | between subnet rows |
| AZ padding top | `layout.availability_zone.padding.top` | 50 | above first subnet |
| AZ padding bottom | `layout.availability_zone.padding.bottom` | 40 | below last subnet |
| AZ padding sides | `layout.availability_zone.padding.sides` | 8 | around column |
| AZ dash pattern | `layout.availability_zone.stroke_dasharray` | 8,8 | template uses ~7.6,7.6 |
