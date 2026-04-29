## Context

The extension currently renders resources inside a hierarchy: Account → Region → VPC → Subnet. Global services (S3, Lambda) render in a "Global" pseudo-region. CloudFront and Route 53 are architecturally different — they represent the entry point for traffic, sitting above all regional infrastructure. The extension has no concept of an "Edge" zone yet.

Cloudia collects `cloudfront-list-distributions.json` and `route53-list-hosted-zones.json` in us-east-1 (global API endpoints). Test account 111111111111 has 19 CloudFront distributions and 20 Route 53 hosted zones (1 private, 19 public).

## Goals / Non-Goals

**Goals:**
- Render an Edge zone inside the Account rect, above the regions row
- Show all public Route 53 zones and all CloudFront distributions
- Place private Route 53 zones inside their VPC (with account-level fallback)
- Show all distributions and zones — no filtering

**Non-Goals:**
- Connection lines from CloudFront to origins (separate bean: conn1)
- Route 53 record-level detail (just zone name + record count)
- CloudFront cache behavior or origin detail (just name/aliases + comment)
- Per-region CloudFront edge location rendering

## Decisions

### 1. Edge zone placement: inside Account rect, above regions row

The Edge zone is a new rendering area inside the Account rect, between the account label and the horizontal Row of regions. It uses a bordered rect similar to a region rect.

```
┌─ Account ────────────────────────────────────────┐
│                                                    │
│  ┌─ Edge ──────────────────────────────────────┐  │
│  │  R53 zones  +  CloudFront distributions     │  │
│  └─────────────────────────────────────────────┘  │
│                                                    │
│  ┌─ Global ──┐  ┌─ eu-west-1 ───────────────┐   │
│  │ S3 / λ    │  │ VPCs...                    │   │
│  └───────────┘  └────────────────────────────┘   │
└────────────────────────────────────────────────────┘
```

**Alternative considered**: Edge zone above the Account rect. Rejected because these are account-owned resources, not external.

**Alternative considered**: Adding to the Global pseudo-region. Rejected because Edge has different semantics — it's the traffic entry point, not a catch-all for non-regional services.

### 2. Edge zone internal layout: R53 left, CloudFront right

Inside the Edge zone, Route 53 public zones render as a vertical stack on the left, CloudFront distributions as a vertical stack on the right. This mirrors how they relate: DNS resolves first, then routes to CloudFront.

```
┌─ Edge ──────────────────────────────────────────────────┐
│                                                          │
│  🌐 example.com (55)      📡 example.com [TF]       │
│  🌐 example.dev (52)      📡 test.example.dev [TF]  │
│  🌐 example.tv (12)       📡 acc.example.dev [TF]   │
│  ...                        ...                         │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

**Alternative considered**: Single vertical stack interleaving R53 and CF. Rejected because they're distinct services and the side-by-side layout communicates the DNS→CDN flow.

### 3. Data parsing: extend parse_global_services()

`parse_global_services()` already scans region dirs for `s3-list-buckets.json`. It gains scanning for `cloudfront-list-distributions.json` and `route53-list-hosted-zones.json`. The global_data dict gains `cloudfront_distributions` and `route53_public_zones` keys.

Private Route 53 zones are separated during parsing: zones with `PrivateZone: true` go into a separate `route53_private_zones` list returned per-region from `parse_region()`.

### 4. Private zone VPC placement logic

1. If `route53-list-hosted-zones-by-vpc` data exists for the account → use VPC association to place zones in specific VPCs
2. Else if only one non-default VPC exists in the region → assume private zones belong to it
3. Else → render at account level (below the Edge zone, above the regions row)

For the VPC placement, private zones render as a simple icon+name element in the VPC pre-grid zone (below EKS, above subnets). This reuses the same zone pattern as LBs and EKS.

### 5. Route 53 card content

Each public zone card: hosted zone icon + zone name (without trailing dot) + record count in parentheses.

Example: `🌐 example.com (55 records)`

### 6. CloudFront card content

Each distribution card: CloudFront icon + primary alias (or comment if no aliases) + distribution ID as subtitle.

Example: `📡 example.com [TF]` with `EXAMPLECFDISTID` dimmed below.

### 7. Icons

| Resource | Symbol | File |
|----------|--------|------|
| Public R53 zone | `res-amazon-route-53-hosted-zone` | AWS-Resource-networking-content-delivery-light.svg (already imported) |
| Private R53 zone | `res-amazon-route-53-hosted-zone` | Same file, same icon (differentiated by placement) |
| CloudFront dist | `res-amazon-cloudfront-download-distribution` | AWS-Resource-networking-content-delivery-light.svg (already imported) |

No new symbol files needed — both icons are in the already-imported `AWS-Resource-networking-content-delivery-light.svg`.

### 8. Layer z-order

Edge → Accounts → Regions → VPCs → AZs → Subnets → EC2 → Database → Load Balancers → EKS → Lambda → Route 53 Private → S3

Edge is the topmost layer. Route 53 Private sits with other VPC-internal spanning elements.

### 9. Edge zone rendering flow

In `_render_multi_region` and `_render_single_region`:
1. Parse global services (gains R53 + CF data)
2. Compute Edge zone content dimensions
3. Render Edge rect at account top (below account label)
4. Offset the regions Row down by Edge zone height
5. Render regions as before

When no account name is provided (no Account rect), the Edge zone still renders above the regions but without the Account wrapper.

## Risks / Trade-offs

- [19 distributions + 20 zones] → The Edge zone could be very tall. Side-by-side layout helps. Configurable card_gap can compress. Acceptable for v1.
- [Private zone VPC heuristic] → The single-VPC fallback could be wrong in multi-VPC accounts. Acceptable — the VPC association data would fix this when available.
- [No connection lines] → Without lines from CF to origins, the relationship between Edge and VPC resources is implicit. The conn1 bean will address this later.
