## Context

ASGs are currently drawn as dashed rectangles inside individual subnets. This doesn't represent their multi-AZ nature. AZ columns already demonstrate the pattern of spanning across grid boundaries.

## Goals / Non-Goals

**Goals:**
- ASG dashed rect spans from leftmost to rightmost column it covers
- EC2 instances inside ASGs render within the spanning rect area
- Non-ASG instances render above (before) the ASG rect within each subnet

**Non-Goals:**
- Changing ASG parsing (already correct with `subnet_ids` and `instance_ids`)
- ECS services inside ASGs (future change)

## Decisions

### 1. ASG rect spans columns within a subnet row

For each ASG, determine which columns its subnets map to. The rect spans from `grid.cell_position(row, min_col).x` to `grid.cell_position(row, max_col).x + col_width(max_col)`. Vertically, it sits within the subnet row at the y offset where ASG-grouped instances start.

```
┌─ subnet col 0 ────────────┐  ┌─ subnet col 1 ────────────┐
│  🖥 JUMPHOST (non-ASG)     │  │                            │
│                            │  │                            │
│ ┌╌╌╌╌╌ ASG: powerbi_gw ╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┐ │
│ ╎ 🔄 ec2-asg-powerbi...   │  │                           ╎ │
│ ╎    min:1 desired:1 max:1 │  │                           ╎ │
│ ╎  🖥 powerbi_gateway      │  │                           ╎ │
│ ╎     m5a.4xlarge          │  │                           ╎ │
│ └╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┘ │
└────────────────────────────┘  └────────────────────────────┘
```

The ASG rect ignores the subnet boundaries and col_gap — it stretches across them.

### 2. Y positioning within subnet rows

Within each subnet cell, the layout is:
1. Subnet label (icon + name)
2. Non-ASG EC2 instances (card_top + cards)
3. ASG rect (label + ASG-grouped EC2 instances)
4. Other resources (DB, NAT)

The ASG rect y-start = subnet_y + subnet_label_height + non_asg_cards_height + asg_top_margin.

### 3. Multiple ASGs in same row

If two ASGs have instances in the same subnet row, they stack vertically. Each gets its own spanning rect.

### 4. ASG instances across different subnet rows

If an ASG has instances in different subnet rows (e.g., instance A in row 0 col 0, instance B in row 1 col 1), we draw a separate ASG rect in each row. This is a simplification — a single rect spanning rows would be very complex and cross too many boundaries.

### 5. Rendering order

EC2 `render_instances_in_subnet` still renders all instances (non-ASG first, then ASG-grouped). The ASG spanning rect is drawn on the ASG layer after all EC2 cards are placed, overlaying as a visual grouping.

## Risks / Trade-offs

- [ASG rect crosses subnet borders] → The rect visually breaks the subnet boundary. Acceptable — it accurately represents that the ASG is a VPC-level construct, not a subnet-level one.
- [col_gap area] → The ASG rect spans through the gap between columns. This is the correct visual — the ASG spans across AZs.
