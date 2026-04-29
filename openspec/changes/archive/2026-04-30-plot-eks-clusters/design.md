## Context

The extension renders VPC-scoped resources (subnets, EC2, load balancers, databases) and global resources (S3 buckets). Load balancers are rendered as spanning elements in a pre-grid zone within VPCs — icon + name + type label with a dashed span line across the AZ columns they attach to. EKS clusters follow the same pattern: they belong to a VPC and span multiple subnets across AZs.

Cloudia collects `eks-list-clusters.json` (cluster names) and `eks-describe-cluster/<name>` (cluster details including VPC, subnets, version, status). Test account 111111111111 has 3 EKS clusters in eu-west-1, all in the same VPC, spanning 2-3 AZs each.

## Goals / Non-Goals

**Goals:**
- Render ACTIVE EKS clusters as VPC-level spanning elements
- Reuse the load balancer pre-grid zone pattern
- Show cluster name, Kubernetes version, and AZ span
- Filter out non-ACTIVE clusters

**Non-Goals:**
- Node group or pod-level detail (cloudia doesn't collect this)
- Fargate profile rendering (separate ECS concern)
- Differentiating EKS Anywhere / Distro / Outposts variants (all use `arch-amazon-eks-cloud` icon for now)

## Decisions

### 1. EKS zone placement: below LBs, above subnets

EKS clusters render in the same pre-grid zone concept as load balancers, but below them. The VPC's `pad_top` grows to accommodate both zones.

```
┌─ VPC ─────────────────────────────────────────┐
│  VPC label                                     │
│                                                │
│  🔀 alb-name     ────────────────             │ ← LB zone
│                                                │
│  ☸ eks-cluster   ──────────────               │ ← EKS zone
│                                                │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐       │ ← subnet grid
│  └─────────┘  └─────────┘  └─────────┘       │
└────────────────────────────────────────────────┘
```

**Alternative considered**: Rendering EKS clusters inside subnets (like EC2 instances). Rejected because a cluster spans multiple subnets — it's architecturally a VPC-level construct, not a subnet-level one.

### 2. Reuse LB rendering pattern exactly

`resource_eks.py` follows the same structure as `resource_lb.py`:
- `zone_height(cluster_count, config)` → total height for the EKS zone
- `render_eks(inkdoc, cluster, y, grid, subnet_to_col, layer, config)` → render one cluster card
- `render_eks_zone(inkdoc, clusters, zone_y, grid, subnet_to_col, layer, config)` → render all clusters

Card layout: icon left-aligned, name right of icon, version below name (dimmed), dashed span line at card bottom.

### 3. Icon: `arch-amazon-eks-cloud` from `AWS-Service-containers.svg`

This is the standard EKS icon for cloud-hosted clusters. The symbol file needs to be added to `SYMBOL_FILES`. Full symbol ID: `AWS-Service-containers.svg:arch-amazon-eks-cloud`.

**Alternative considered**: Using `res-amazon-elastic-kubernetes-service-eks-on-outposts` from the resource-level containers file. Rejected because the `arch-` prefixed service-level icons are used for cluster-level representations (like how we use service icons for LBs), and the resource icon is specifically for Outposts.

### 4. Parser: separate return value from parse_region

`parse_region` currently returns `(vpcs, subnets, instances, load_balancers)`. Adding EKS clusters extends this to `(vpcs, subnets, instances, load_balancers, eks_clusters)`.

Each cluster dict:
```python
{
    "type": "eks",
    "name": "ota-eks-prod",
    "version": "1.33",
    "vpc_id": "vpc-EXAMPLE0000000001",
    "subnet_ids": ["subnet-EXAMPLE0000000001", ...],
    "status": "ACTIVE",
}
```

### 5. Span line color: EKS orange (#FF9900)

AWS uses orange for EKS branding. The span line uses a distinct color from LBs (which use `#ED7100`) to visually distinguish the two zone types. Configurable via `layout.eks.span_line_color`.

### 6. Layer z-order

Accounts → Regions → VPCs → AZs → Subnets → EC2 → Database → Load Balancers → EKS → S3

EKS sits above Load Balancers since it renders in the same pre-grid zone area but below LBs visually.

## Risks / Trade-offs

- [Many clusters in one VPC] → VPC rect grows tall. Acceptable — real accounts rarely have more than 3-5 EKS clusters per VPC. Configurable via `card_height` and `card_gap`.
- [Cluster subnets not in diagram] → A cluster's `resourcesVpcConfig.subnetIds` may reference subnets that don't appear in the subnet grid (e.g., subnets with no EC2 instances). The span line will only cover columns for subnets that are in the grid. If none match, the cluster renders without a span line (icon + name only).
- [Breaking change to parse_region return] → Adding a 5th element to the tuple requires updating all callers. There are only 2 call sites (`_render_single_region` and `parse_all_regions`), so impact is contained.
