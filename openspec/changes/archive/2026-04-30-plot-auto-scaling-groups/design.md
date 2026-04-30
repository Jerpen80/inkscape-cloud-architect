## Context

EC2 instances are rendered as borderless cards inside subnets. ASGs group EC2 instances and manage their scaling. The data links ASGs to instances via `Instances[].InstanceId` and to subnets via `VPCZoneIdentifier`.

## Goals / Non-Goals

**Goals:**
- Render ASGs as dashed containers around their EC2 instances
- Show ASG name and capacity in a label
- Handle ASGs that span multiple subnets (instances in different AZs)

**Non-Goals:**
- Rendering scaling policies or alarms
- Showing ASGs with 0 running instances
- Launch configuration/template details

## Decisions

### 1. ASG as a grouping wrapper, not a card

Unlike EC2/RDS/Lambda which are resource cards, an ASG is a **container** — a dashed rectangle drawn around the EC2 cards it owns. It doesn't add new cards; it groups existing ones.

```
┌─ subnet ──────────────────────────────┐
│ 🔲 subnet label                       │
│                                       │
│  ┌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┐  │
│  ╎ ASG: my-asg (1/1/3)            ╎  │
│  ╎          🖥                     ╎  │
│  ╎    my-instance                  ╎  │
│  ╎       t3.micro                  ╎  │
│  └╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┘  │
│                                       │
└───────────────────────────────────────┘
```

### 2. Per-subnet ASG rendering

An ASG may span multiple subnets. For each subnet, we check which of the ASG's instances are in that subnet (by matching instance IDs against the EC2 instance map). The ASG dashed rect is drawn per-subnet, wrapping only the instances present in that subnet.

### 3. Instance-to-ASG mapping

Build a mapping: `instance_id → asg_name` from the ASG data. In the EC2 rendering loop, track which instances belong to which ASG. After rendering EC2 cards in a subnet, draw ASG containers around grouped instances.

### 4. Height impact

The ASG container adds:
- A label row at the top (ASG name + capacity)
- Padding around the EC2 cards (small border gap)

This means subnets with ASG-grouped instances need more height than the same instances without ASGs. The row height calculation must account for this.

### 5. ASG label format

`ASG name (min/desired/max)` — e.g., `ec2-asg-nat-equinetapp-us-east-2a (1/1/1)`

### 6. EC2 card position tracking

`resource_ec2.render_instances_in_subnet` currently doesn't return position info. It needs to return the y-extent of rendered cards so `resource_asg.py` knows where to draw the container. Alternatively, compute ASG bounds from the instance count and card height formulas.

Simpler approach: compute ASG container bounds from instance count × card_height, using the same formulas as `resource_ec2.cards_height()`. No need to track actual rendered positions — the layout is deterministic.

### 7. Rendering order within a subnet

1. EC2 cards (ungrouped instances first, then ASG-grouped instances by ASG)
2. ASG dashed containers drawn around the grouped EC2 cards on the ASG layer

Actually, to keep it simple: render all EC2 cards as before (order doesn't change), then overlay ASG dashed rects based on which instances are in each ASG. The ASG rect position is calculated from the card index within the subnet.

## Risks / Trade-offs

- [Mixed ASG/non-ASG instances] → A subnet may have both ASG and non-ASG instances. Non-ASG instances render first, ASG instances after. The ASG container wraps only its instances.
- [Multiple ASGs in one subnet] → Possible but rare. Each ASG gets its own dashed container, stacked vertically.
- [ASG label width] → Long ASG names may exceed subnet width. Truncate or let it overflow (consistent with other labels).
