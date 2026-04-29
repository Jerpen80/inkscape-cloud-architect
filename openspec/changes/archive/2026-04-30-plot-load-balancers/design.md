## Context

EC2 instances are rendered inside individual subnets. Load balancers are fundamentally different — they span multiple subnets across AZs. The current VPC rendering flow is: VPC rect → AZ columns → subnet grid with EC2 inside. LBs need a new zone between the VPC label and the AZ/subnet area.

## Goals / Non-Goals

**Goals:**
- Parse and render ALBs and NLBs as spanning elements within their VPC
- Visually show which AZ columns a load balancer spans
- Lay groundwork for future connection lines to targets

**Non-Goals:**
- Classic ELBs (elbv1)
- Gateway Load Balancers
- Connection lines to targets (future phase)
- Target group rendering

## Decisions

### 1. Pre-grid LB zone

Load balancers are rendered in a zone between the VPC label and the AZ/subnet grid. This zone is added to the VPC's top padding when LBs are present.

```
┌─ VPC label ─────────────────────────────────────┐
│                                                  │
│  ⚖️ external-alb-customera-prd (ALB)               │
│  ──────────────────────────────────              │
│                                                  │
│    ┌─ AZ col 0 ─────┐  ┌─ AZ col 1 ──────┐     │
│    │ ┌─ subnet ────┐ │  │ ┌─ subnet ────┐ │     │
```

The LB card shows: icon (left) + name + type label. A subtle horizontal line spans from the leftmost to rightmost column the LB is attached to, indicating its reach.

### 2. Column span calculation

Each LB has `subnet_ids` from its `AvailabilityZones`. These are mapped to grid columns via the AZ-to-column mapping already built in `render_vpc_with_subnets`. The span goes from `min(col)` to `max(col)`.

The x-coordinates are derived from `grid.cell_position(0, min_col)` (left edge) to `grid.cell_position(0, max_col) + grid.col_width(max_col)` (right edge).

### 3. Multiple LBs stack vertically

If a VPC has multiple load balancers, they stack vertically in the LB zone, each with a small gap between them.

### 4. Parser returns load balancers as 4th element

`parse_region` returns `(vpcs, subnets, instances, load_balancers)`. Each LB dict contains: `name`, `lb_type` (application/network), `scheme` (internet-facing/internal), `vpc_id`, `subnet_ids` (list).

### 5. Type-specific symbols

- ALB: `AWS-Resource-networking-content-delivery-light.svg:res-elastic-load-balancing-application-load-balancer`
- NLB: `AWS-Resource-networking-content-delivery-light.svg:res-elastic-load-balancing-network-load-balancer`

### 6. New module `resource_lb.py`

Rendering logic in a new module following the pattern of `resource_ec2.py`. Called from `resource_vpc.py` before the subnet grid is drawn.

## Risks / Trade-offs

- [LB zone adds VPC height] → VPCs with many LBs will be taller. The zone height is dynamic based on LB count.
- [Column mapping depends on subnet placement] → If an LB references a subnet not in the current VPC's grid (edge case), it's skipped gracefully.
- [Spanning line aesthetics] → The horizontal span line needs to look good without cluttering. Using a subtle dashed or thin line.
