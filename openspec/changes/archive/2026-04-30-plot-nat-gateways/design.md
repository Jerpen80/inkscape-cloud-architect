## Context

The extension renders subnet-level resources (EC2, databases) as icon+name cards stacked inside subnets. Each resource type has its own map (`instance_map`, `db_map`), contributes to row height calculation, and renders in sequence within the subnet cell. NAT gateways follow this exact pattern.

Network interfaces in `ec2-describe-network-interfaces.json` with `InterfaceType: "nat_gateway"` provide the NAT gateway ID (from Description), SubnetId, and VpcId.

## Goals / Non-Goals

**Goals:**
- Render NAT gateways inside their public subnets as icon+name cards
- Follow the established resource card pattern (EC2, databases)
- Dedicated layer for visibility toggling

**Non-Goals:**
- Showing NAT gateway elastic IPs or pricing info
- Drawing route connections from private subnets to NAT gateways
- Rendering NAT instances (EC2-based NAT, legacy)

## Decisions

### 1. Derive NAT gateways from network interfaces

Parse `ec2-describe-network-interfaces.json`, filter by `InterfaceType == "nat_gateway"`. Extract:
- `nat_gateway_id`: parsed from Description field ("Interface for NAT Gateway nat-...")
- `subnet_id`: from the interface
- `vpc_id`: from the interface

No new API call needed — data is already collected by cloudia.

### 2. Same card rendering pattern as EC2/databases

`resource_nat.py` follows the `resource_ec2.py` pattern: `card_height()`, `cards_height()`, `render_instance()`, `render_in_subnet()`. Cards stack vertically after databases in the subnet.

### 3. Height contribution

NAT gateway cards contribute to subnet row height calculation in `resource_vpc.py`, chained after EC2 + DB heights:
```python
needed = subnet_label_height
needed += resource_ec2.cards_height(n_ec2, config)
needed += resource_db.cards_height(n_db, config)
needed += resource_nat.cards_height(n_nat, config)  # new
```

### 4. Rendering order within subnet

Bottom to top inside a subnet cell: EC2 → Databases → NAT Gateways. Each renders with an offset that accounts for the cards above.

### 5. NAT Gateways layer

New layer in z-order after database layer. Provides independent visibility toggling in Inkscape.

## Risks / Trade-offs

- [One NAT per subnet] → Typically there's only one NAT gateway per public subnet. The card approach handles multiple gracefully if needed.
- [Description parsing] → NAT gateway ID is parsed from the Description field. If cloudia changes the description format, parsing would break. The format is consistent from AWS ("Interface for NAT Gateway nat-xxx").
