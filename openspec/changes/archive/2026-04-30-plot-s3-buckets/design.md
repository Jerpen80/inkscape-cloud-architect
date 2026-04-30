## Context

The extension renders VPCs, subnets, AZs, EC2 instances, and load balancers — all VPC-scoped resources. S3 is the first global/account-level service to be added. The multi-region rendering already uses a horizontal `Row` of regions. The `s3-list-buckets.json` file is found at `{account-data}/us-east-1/s3-list-buckets.json` and contains bucket `Name` and `CreationDate` fields (no region info per bucket).

## Goals / Non-Goals

**Goals:**
- Render S3 buckets in the diagram via a "Global" pseudo-region
- Reuse the existing region rendering infrastructure (Row, region rect)
- Make the Global region extensible for future global services

**Non-Goals:**
- Per-region bucket placement (data doesn't include `BucketRegion`)
- Bucket details beyond name (size, versioning, etc.)
- Other global services (IAM, Route53) — those can follow later using the same Global region

## Decisions

### 1. Global pseudo-region in the Row

S3 buckets render inside a "Global" region rect that sits as the first entry in the horizontal Row, before real regions. This reuses the existing `Row`, `resource_region.render_region_rect`, and region padding config.

**Alternative considered**: Separate section below VPCs with custom layout. Rejected because the Global region approach requires no new layout primitives and is naturally extensible.

### 2. S3 bucket rendering as icon+name cards

Each bucket is rendered as a small icon (scaled bucket symbol) + name text, stacked vertically with a gap. This mirrors the EC2 card pattern.

The card rendering function takes a list of buckets and a position, renders them vertically, and returns total height and width.

### 3. S3 data discovery

`s3-list-buckets.json` is a global API call that AWS returns from us-east-1. The parser scans all region dirs for this file and uses the first one found. This is done in a new `parse_global_services()` function.

### 4. Global region in parse_all_regions()

After scanning real regions, `parse_all_regions()` calls `parse_global_services()`. If any global data exists (S3 buckets), it prepends a `("Global", global_data)` entry to the results list so Global renders first (leftmost).

### 5. Global region in single-region mode

When a specific region is selected, the Global region is still rendered — below the VPCs using a vertical Stack. This ensures S3 buckets always appear regardless of mode.

Actually, on reflection: in single-region mode the user chose a specific region. Showing global resources there may be unexpected. Let's keep it simple: **Global region only appears in multi-region ("all") mode**. In single-region mode, no S3 buckets.

### 6. Symbol import

Add `AWS-Resource-storage-light.svg` to `SYMBOL_FILES`. Bucket symbol: `AWS-Resource-storage-light.svg:res-amazon-simple-storage-service-bucket`.

### 7. Layer z-order

Accounts → Regions → VPCs → AZs → Subnets → EC2 → Load Balancers → S3

### 8. Rendering the Global region

The Global region rect is drawn by the same `resource_region.render_region_rect()`. Inside it, instead of VPCs, `resource_s3.render_buckets()` renders the bucket cards. The multi-region loop in `_render_multi_region` needs to detect Global vs real regions and call the appropriate renderer.

Data structure from parser: the Global region entry uses a dict instead of the (vpcs, subnets, instances, lbs) tuple:

```python
("Global", {"s3_buckets": [...]})
```

The multi-region loop checks if the data is a dict (global) vs tuple (regional) and dispatches accordingly.

## Risks / Trade-offs

- [Many buckets] → An account with 50+ buckets will make the Global region very tall. Acceptable for v1 — users can configure card_gap to compress. Future work could add bucket filtering.
- [S3 file location] → Assumes `s3-list-buckets.json` is in a region subdir (typically us-east-1). If the cloudia data structure changes, the scan function needs updating.
