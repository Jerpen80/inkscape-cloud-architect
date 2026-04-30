## 1. Config & Layout Primitives

- [x] 1.1 Add `layout.region` section to `default-config.yaml` with padding and gap defaults
- [x] 1.2 Add `Row` class to `layout.py` (horizontal counterpart to `Stack`: tracks cursor_x, max_height, gap)

## 2. Parser Changes

- [x] 2.1 Add `is_default` field to VPC parsing in `cloudia_parser.py` (from AWS `IsDefault`)
- [x] 2.2 Add `parse_all_regions()` function that scans subdirectories, calls `parse_region` per region, filters out regions with only default VPCs

## 3. Region Rendering

- [x] 3.1 Create `resource_region.py` with function to render a region rectangle (blue `#00a4a6` stroke, `region.svg` icon)
- [x] 3.2 Add "All regions (with resources)" as first option (`value="all"`) in INX region dropdown
- [x] 3.3 Add `region == "all"` handling to `add_arguments` / `effect()` in `aws-auto-diagram.py`

## 4. Multi-Region Orchestration

- [x] 4.1 Update `effect()` to create "Regions" layer in z-order (between Accounts and VPCs)
- [x] 4.2 Implement multi-region rendering loop: Row of regions, Stack of VPCs within each region, region rects around each
- [x] 4.3 Ensure single-region mode is unchanged (no region rect, no Row)

## 5. Verification

- [x] 5.1 Run headless test with single region — confirm output unchanged
- [x] 5.2 Run headless test with `--region=all` — confirm multi-region output renders correctly
