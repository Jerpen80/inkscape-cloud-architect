# Design: Plot availability zones

## Config

```yaml
# default-config.yaml
document:
  margin: 20

availability_zones:
  enabled: true
  label_prefix: ""           # empty = raw AZ name, e.g. "us-east-2a"
  padding_top: 25            # space for AZ label above subnets
  padding_bottom: 5
  padding_sides: 5
  stroke_color: "#00a4a6"
  stroke_width: 0.5
  stroke_dasharray: "2,2"
```

User can override any value in `~/.config/inkscape/extensions/aws-auto-diagram/config.yaml`.

## Layer z-order

```
"VPCs"                 ← VPC rects (bottom)
"Availability Zones"   ← dashed AZ columns (middle) ← NEW
"Subnets"              ← subnet rects (top)
```

Pre-created in `effect()` in this order.

## AZ rect positioning

Each AZ column gets a dashed rect that wraps its subnet cells within a VPC:

```
VPC grid origin (vpc_x, vpc_y)
│
├── VPC padding_top (50px) ← VPC label lives here
│
├── AZ rect starts here (vpc_y + VPC_PADDING_TOP - az_padding_top)
│   ├── AZ label
│   ├── az_padding_top
│   ├── Subnet row 0
│   ├── row_gap
│   ├── Subnet row 1
│   ├── ...
│   └── az_padding_bottom
│
└── VPC padding_bottom
```

AZ rect dimensions per column:
- **x**: `grid.cell_position(0, col).x - az_padding_sides`
- **y**: `vpc_y + VPC_PADDING_TOP - az_padding_top`
- **width**: `grid.col_width(col) + az_padding_sides * 2`
- **height**: `(num_rows * SUBNET_HEIGHT + (num_rows-1) * ROW_GAP) + az_padding_top + az_padding_bottom`

## Grid adjustment

The col_gap must accommodate AZ side padding on both sides of adjacent columns:

```
current: col_gap = 10
with AZ: col_gap = az_padding_sides + gap_between_az_rects + az_padding_sides
```

The effective visual gap between AZ rects should stay ~10px. So:
`COL_GAP = az_padding_sides * 2 + 10`

This is computed from config values, not hardcoded.

## VPC padding_top adjustment

With AZ labels above the subnet rows, VPC_PADDING_TOP needs to accommodate both the VPC label and the AZ label height. Since AZ labels sit inside the VPC content area, VPC_PADDING_TOP should increase by `az_padding_top`.

## resource_az.py

```python
def render_az_columns(inkdoc, vpc_x, vpc_y, grid, azs, num_rows, config):
    """Render dashed AZ column rects and labels on the AZ layer."""
```

Takes the grid, AZ names, row count, and config. Draws to the "Availability Zones" layer.

## When disabled

If `availability_zones.enabled` is false:
- No AZ layer created
- No AZ rects rendered
- col_gap stays at base value (no AZ padding added)
- VPC_PADDING_TOP stays at base value
