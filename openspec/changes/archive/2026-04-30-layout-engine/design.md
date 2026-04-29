# Design: Layout engine with canonical AWS diagram style

## Architecture

```
ica_utils/
├── layout.py          ← Generic: grid, auto-sizing, stacking
├── resource_vpc.py    ← AWS-specific: maps VPCs/subnets to layout + rendering
├── cloudia_parser.py  ← Data source (unchanged)
└── icalog.py          ← Debug logging (unchanged)
```

## Layout module (layout.py)

Generic layout primitives. Not AWS-specific — reusable for any future resource types.

### Grid

Lays out cells in rows x columns with consistent sizing.

```python
class Grid:
    def __init__(self, origin_x, origin_y, cell_width, cell_height,
                 col_gap, row_gap, padding):
        ...

    def cell_position(self, row, col) -> (x, y):
        """Absolute position for a cell at (row, col)."""

    def bounds(self, num_rows, num_cols) -> (width, height):
        """Total size of the grid including padding."""
```

- `origin_x/y` — top-left of the grid content area (inside padding)
- `padding` — space between grid edge and cells (for VPC label/icon)
- `col_gap/row_gap` — space between cells

### Stack

Stacks containers vertically with spacing. Tracks cursor position.

```python
class Stack:
    def __init__(self, x, y, gap):
        ...

    def next_position(self) -> (x, y):
        """Position for the next container."""

    def advance(self, height):
        """Move cursor down by height + gap."""
```

## Canonical AWS layout

```
VPC rect (auto-sized, purple border)
┌──────────────────────────────────────────────────┐
│ VPC name + icon                                   │
│                                                    │
│        AZ-a          AZ-b          AZ-c           │
│   ┌───────────┐ ┌───────────┐ ┌───────────┐      │
│   │ public-1a │ │ public-1b │ │ public-1c │      │
│   └───────────┘ └───────────┘ └───────────┘      │
│                                                    │
│   ┌───────────┐ ┌───────────┐ ┌───────────┐      │
│   │ private-1a│ │ private-1b│ │ private-1c│      │
│   └───────────┘ └───────────┘ └───────────┘      │
│                                                    │
└──────────────────────────────────────────────────┘
```

Grid mapping:
- **Columns** = sorted unique AZs from the VPC's subnets
- **Rows** = [public, private] (only rows that have subnets)
- **Cell** = subnet rectangle with name, icon, color based on public/private

VPC rectangle auto-sizes to `grid.bounds(num_rows, num_cols)`.

Multiple VPCs stack vertically via `Stack`.

## Data flow

```
effect()
  │
  ├── cloudia_parser.parse_region(data_dir, region) → vpcs, subnets
  │
  └── for each vpc:
        │
        ├── Collect vpc_subnets, determine AZs and rows
        ├── Create Grid with appropriate dimensions
        ├── Draw VPC rect at stack.next_position() with grid.bounds() size
        ├── Draw each subnet at grid.cell_position(row, col)
        └── stack.advance(vpc_height)
```

## Layout constants

Defined at top of `resource_vpc.py` (AWS-specific sizes):

```python
SUBNET_WIDTH = 160
SUBNET_HEIGHT = 50
COL_GAP = 10
ROW_GAP = 15
VPC_PADDING_TOP = 30    # Space for VPC name + icon
VPC_PADDING_SIDES = 15
VPC_PADDING_BOTTOM = 15
VPC_GAP = 25            # Vertical gap between VPCs
```

## Key decisions

- **Layout module is generic** — Grid and Stack know nothing about AWS. They compute coordinates from rows, columns, and sizes.
- **resource_vpc owns the AWS mapping** — it decides that AZs are columns, public/private are rows, and calls layout primitives.
- **Rows are dynamic** — if a VPC only has public subnets, there's only one row. No empty private row.
- **VPC rect auto-sizes** — uses `grid.bounds()` to determine width and height, no fixed aspect ratio.
- **Constants live in resource_vpc** — layout module takes these as parameters, doesn't hardcode sizes.
