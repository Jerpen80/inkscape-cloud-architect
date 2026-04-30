## Context

The extension renders VPCs as bordered rectangles with resources inside (subnets, EC2, LBs, EKS, etc.) and spanning elements in pre-grid zones. Internet gateways are different — they sit at the VPC boundary, conceptually connecting the VPC to the internet. Cloudia collects `ec2-describe-internet-gateways.json` with IGW ID, attached VPC, and tags.

Test account 111111111111 has 2 IGWs: one attached to the main VPC (`vpc-EXAMPLE0000000001`, named "VPC-customer"), one to the default VPC (skipped).

## Goals / Non-Goals

**Goals:**
- Show which VPCs have internet gateways
- Place IGW visually at the VPC boundary (top-right corner)
- Simple icon+name rendering

**Non-Goals:**
- Connection lines from IGW to subnets/route tables
- Distinguishing IGW vs egress-only IGW
- VPN gateways (separate resource type)

## Decisions

### 1. Placement: top-right corner of VPC rect

The IGW icon renders at the top-right corner of the VPC rectangle, straddling the border. This is the standard AWS diagram convention — the IGW sits "on" the VPC boundary, not inside or outside it.

```
┌─ VPC ──────────────────────────────── 🌐 ─┐
│                                       IGW  │
│  ┌─────────┐  ┌─────────┐                 │
│  │ subnet  │  │ subnet  │                 │
│  └─────────┘  └─────────┘                 │
└────────────────────────────────────────────┘
```

The icon is placed at `(vpc_x + vpc_width - icon_size - padding, vpc_y + padding)` with the name below or to the left.

**Alternative considered**: Pre-grid zone spanning element (like LBs/EKS). Rejected because IGW is not a spanning element — it's a single attachment point at the VPC level.

### 2. Simple card: icon + name

Each IGW renders as: icon (internet gateway symbol) + Name tag value (or IGW ID as fallback). No additional metadata needed — IGWs are simple resources.

### 3. Parser returns IGWs per-region

`parse_region()` gains an `internet_gateways` list. Each IGW entry contains `igw_id`, `name`, `vpc_id`. Only IGWs with `State: "available"` attachments are included.

### 4. Icon from existing symbol file

`AWS-Resource-networking-content-delivery-light.svg:res-amazon-vpc-internet-gateway` — already imported (the networking file is in `SYMBOL_FILES`).

### 5. Layer z-order

Internet Gateways layer sits above VPCs (since the icon overlaps the VPC border).

## Risks / Trade-offs

- [One IGW per VPC] → AWS allows at most one IGW per VPC, so the rendering is always a single icon. No stacking needed.
- [Icon overlap] → The icon straddling the VPC border may overlap with the VPC label if the VPC name is very long. Acceptable — the icon is at the right edge, the label is at the left.
