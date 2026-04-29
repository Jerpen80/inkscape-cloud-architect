## Context

The extension currently receives a single region selection from the INX dropdown and calls `cloudia_parser.parse_region(data_dir, region)`. The result feeds into a vertical `Stack` that renders VPCs top-to-bottom. The account rectangle (optional) wraps everything via bounding-box calculation.

The cloudia account-data directory structure is:
```
account-data/{account-id}/
  describe-regions.json
  eu-west-1/
    ec2-describe-vpcs.json
    ec2-describe-subnets.json
    ec2-describe-instances.json
  us-east-1/
    ...
```

## Goals / Non-Goals

**Goals:**
- Render all non-empty regions side by side when "All regions" is selected
- Each region gets its own labeled boundary rectangle
- Filter out regions with only default VPCs
- Single-region mode remains unchanged

**Non-Goals:**
- Multi-account rendering (one account per diagram)
- Region sorting/ordering preferences (alphabetical for now)
- Rendering regions that have no custom resources

## Decisions

### 1. Horizontal layout for regions using a `Row` primitive

Regions flow left-to-right. A new `Row` class in `layout.py` mirrors `Stack` but tracks `cursor_x` and `max_height`:

```
Row(x, y, gap):
  next_position() → (cursor_x, y)
  advance(width, height) → cursor_x += width + gap; max_height = max(max_height, height)
  bounds() → (total_width, max_height)
```

Each region renders its VPCs into a vertical Stack, computes bounds, draws the region rect, then advances the Row.

**Alternative considered**: Grid layout with fixed columns. Rejected because regions have vastly different sizes — a flexible row is simpler and handles variable widths naturally.

### 2. Region selection via "all" sentinel value in INX dropdown

Add `<option value="all">All regions (with resources)</option>` as the first option. When `region == "all"`, the extension scans subdirectories. Otherwise, single-region path unchanged.

**Alternative considered**: Multi-select checkboxes. Rejected because INX doesn't support multi-select well, and "all or one" covers the primary use cases.

### 3. Filter empty regions by `IsDefault` on VPCs

AWS VPC JSON includes `"IsDefault": true/false`. A region is "empty" if all its VPCs have `IsDefault: true`. The parser adds `is_default` to the VPC dict. The multi-region scan filters before rendering.

### 4. Region rect style

- Symbol: `AWS-Group-light.svg:region.svg`
- Color: `#00a4a6` (blue, matching AWS region color convention)
- Stroke: 0.5, no fill (consistent with VPC/subnet rects)
- Own "Regions" layer between Accounts and VPCs

### 5. Layer z-order update

Bottom to top: Accounts → Regions → VPCs → Availability Zones → Subnets → EC2

### 6. Rendering flow for multi-region

```
1. Parse all regions → list of (region_name, vpcs, subnets, instances)
2. Filter: keep only regions with non-default VPCs
3. Create layers in z-order
4. Create Row for regions (inside account padding if account_name set)
5. For each region:
   a. Get region position from Row
   b. Create Stack for VPCs (inside region padding)
   c. Render VPCs into Stack
   d. Draw region rect around Stack bounds
   e. Advance Row by region width/height
6. Draw account rect around all regions (if account_name set)
7. resize_to_fit
```

### 7. Config structure

```yaml
layout:
  region:
    padding:
      top: 50
      right: 15
      bottom: 15
      left: 15
    gap: 20
```

## Risks / Trade-offs

- [Wide diagrams] → With many active regions, the diagram can get very wide horizontally. Acceptable — users can scroll or zoom. Future work could add wrapping.
- [Default VPC heuristic] → Some users may have custom resources in a default VPC. Filtering by `IsDefault` on VPCs means we'd still show regions where a default VPC has custom subnets or instances. This is correct behavior — we filter regions that have ONLY default VPCs, not individual VPCs.
- [Region ordering] → Alphabetical may not match user's mental model (e.g., primary region first). Acceptable for v1, can add sorting config later.
