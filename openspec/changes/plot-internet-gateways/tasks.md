## 1. Parser

- [ ] 1.1 Add IGW parsing to `cloudia_parser.py`: read `ec2-describe-internet-gateways.json`, extract igw_id, name (from Name tag or ID), vpc_id from available attachments
- [ ] 1.2 Update `parse_region` return to include internet_gateways
- [ ] 1.3 Update `parse_all_regions` to pass internet_gateways through region tuples

## 2. Rendering

- [ ] 2.1 Create `resource_igw.py` with `render_igw()` that renders IGW icon+name at the top-right corner of a VPC rect
- [ ] 2.2 Add "Internet Gateways" layer to `_create_layers` z-order (above VPCs)

## 3. VPC Integration

- [ ] 3.1 Update `resource_vpc.py` to accept `internet_gateways` parameter and call IGW renderer after drawing VPC rect
- [ ] 3.2 Pass VPC position and dimensions to IGW renderer for corner placement

## 4. Main Extension

- [ ] 4.1 Update `_render_single_region` to unpack and pass internet_gateways
- [ ] 4.2 Update `_render_multi_region` to unpack and pass internet_gateways
- [ ] 4.3 Update `_render_vpcs` to accept and forward internet_gateways

## 5. Configuration

- [ ] 5.1 Add `layout.internet_gateway` section to `default-config.yaml` (icon_scale, font_size)

## 6. Testing

- [ ] 6.1 Run headless test with account 111111111111 eu-west-1 to verify IGW renders on VPC-customer
