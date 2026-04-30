## 1. Config

- [x] 1.1 Add `layout.nat_gateway` section to `default-config.yaml` with icon_scale, font_size, card_gap, card_top

## 2. Parser

- [x] 2.1 Add NAT gateway parsing to `parse_region()` in `cloudia_parser.py` — scan network interfaces for `InterfaceType: "nat_gateway"`, extract NAT ID from Description, SubnetId, VpcId
- [x] 2.2 Return NAT gateways as additional list from `parse_region()` and thread through `parse_all_regions()`

## 3. NAT Gateway Rendering

- [x] 3.1 Create `resource_nat.py` with `card_height()`, `cards_height()`, `render_instance()`, and `render_in_subnet()` following the EC2 card pattern

## 4. Integration

- [x] 4.1 Add "NAT Gateways" layer to `_create_layers()` in `aws-auto-diagram.py`
- [x] 4.2 Pass NAT gateways through `_render_vpcs()` and `render_vpc_with_subnets()` in `aws-auto-diagram.py` and `resource_vpc.py`
- [x] 4.3 Add NAT gateway map, height contribution, and rendering in `resource_vpc.py` (after DB cards)

## 5. Verification

- [x] 5.1 Run headless test with account 111111111111 eu-west-1 — confirm 3 NAT gateways render in subnets
- [x] 5.2 Run headless test with account 222222222222 us-east-2 — confirm no NAT gateways (no crash)
