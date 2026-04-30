## Context

The extension renders 16 resource types across containers (Account, Edge, Region, VPC, Subnets, AZs) and resources (EC2, RDS, ElastiCache, NAT, LB, EKS, Lambda, S3, DynamoDB, CloudFront, Route 53, ASG). Each has distinct icons and/or border colors. There is no visual key explaining these.

## Goals / Non-Goals

**Goals:**
- Self-registering legend entries — new resource modules automatically appear
- Dynamic filtering — only show what's actually in the diagram
- Own layer for visibility toggling in Inkscape

**Non-Goals:**
- User-customizable legend ordering or hiding (future work)
- Legend as a separate SVG/page

## Decisions

### 1. Central registry at `ica_utils/legend.py`

```python
LEGEND_REGISTRY = []

def register_legend(category, name, symbol, layer, border_key=None):
    LEGEND_REGISTRY.append({
        "category": category,   # "container" or "resource"
        "name": name,           # display name
        "symbol": symbol,       # full symbol ID
        "layer": layer,         # layer name to check for content
        "border_key": border_key,  # theme key for border color (containers only)
    })
```

Each resource module calls `register_legend()` at module level (import time). Order of registration determines legend order.

### 2. Dynamic filtering by layer content

After all content is rendered, the legend renderer iterates the registry and checks each entry's layer for children. Entries whose layers have 0 children are skipped. This ensures only relevant items appear.

Layer content check:
```python
layer = inkdoc.svg.find(f".//{{...}}g[@inkscape:label='{entry["layer"]}']")
if layer is not None and len(layer) > 0:
    # include in legend
```

### 3. Two-section layout

**Containers section**: Small colored rectangle (matching border color from theme) + icon + name. Laid out horizontally, wrapping to new rows.

**Resources section**: Icon + name. Laid out horizontally, wrapping to new rows.

```
Containers:
  [━━ purple ━━] VPC   [━━ green ━━] Public Subnet   [━━ teal ━━] Private Subnet

Resources:
  🖥️ EC2   📦 RDS   🌐 NAT Gateway   ⚖️ ALB   🪣 S3   📊 DynamoDB
```

### 4. Positioning below all content

The legend renders below all other content with a configurable `top_spacing` gap. It's positioned after all rendering but before `resize_to_fit`, so the document auto-sizes to include it.

### 5. Legend layer

New "Legend" layer created at the top of z-order (last in `_create_layers`). This makes it the topmost visible layer in Inkscape.

### 6. Registration entries

| Module | Category | Name | Symbol | Layer | Border Key |
|---|---|---|---|---|---|
| resource_account | container | Account | cloud.svg | Accounts | border_account |
| resource_edge | container | Edge | — | Edge | border_edge |
| resource_region | container | Region | region.svg | Regions | border_region |
| resource_vpc | container | VPC | virtual-private-network-vpc.svg | VPCs | border_vpc |
| resource_vpc | container | Public Subnet | public-subnet.svg | Subnets | border_subnet_public |
| resource_vpc | container | Private Subnet | private-subnet.svg | Subnets | border_subnet_private |
| resource_ec2 | resource | EC2 | res-amazon-ec2-instance | EC2 | — |
| resource_db | resource | RDS | res-amazon-aurora-rds-instance | Database | — |
| resource_db | resource | ElastiCache | res-elasticache-for-redis | Database | — |
| resource_nat | resource | NAT Gateway | res-amazon-vpc-nat-gateway | NAT Gateways | — |
| resource_lb | resource | Load Balancer | (ALB symbol) | Load Balancers | — |
| resource_eks | resource | EKS | (EKS symbol) | EKS | — |
| resource_lambda | resource | Lambda | (Lambda symbol) | Lambda | — |
| resource_s3 | resource | S3 | res-simple-storage-service-bucket | S3 | — |
| resource_dynamodb | resource | DynamoDB | res-dynamodb-table | DynamoDB | — |
| resource_cloudfront | resource | CloudFront | (CF symbol) | Edge | — |
| resource_route53 | resource | Route 53 | (R53 symbol) | Edge or Route 53 Private | — |
| resource_asg | resource | Auto Scaling | (ASG symbol) | Auto Scaling Groups | — |

Note: Some modules register multiple entries (resource_vpc registers VPC + both subnet types, resource_db registers RDS + ElastiCache). The Subnets layer entry uses a special check — it always has content when VPCs exist, so both subnet types show if the Subnets layer has children.

## Risks / Trade-offs

- [Import order matters] → Registration order determines legend order. Since Python imports are deterministic and we control the import order in `aws-auto-diagram.py`, this is reliable.
- [Dual-layer resources] → Some resources share layers (CloudFront + Route 53 public both render in Edge). The legend correctly shows both if Edge has content.
