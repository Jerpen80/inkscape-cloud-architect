# Tasks: Layout engine with canonical AWS diagram style

## Tasks

- [x] Create `ica_utils/layout.py` with `Grid` class (cell positioning, bounds calculation, padding)
- [x] Add `Stack` class to `layout.py` (vertical stacking with gap tracking)
- [x] Update `resource_vpc.py` — organize subnets by AZ (columns) and public/private (rows), use Grid for positioning, auto-size VPC rect
- [x] Update `aws-auto-diagram.py` — pass stack origin to renderer, let it manage layout across VPCs
- [x] Test headless run against CustomerA data — verify subnets are inside VPC rect, no overlaps
- [x] Test with multi-VPC data — verify VPCs stack vertically without overlap (us-east-2: 2 VPCs, 9 subnets)
