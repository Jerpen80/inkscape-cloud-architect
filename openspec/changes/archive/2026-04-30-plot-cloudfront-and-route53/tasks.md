## 1. Parser

- [x] 1.1 Add Route 53 parsing to `parse_global_services()`: scan for `route53-list-hosted-zones.json`, split into public zones (name, zone_id, record_count) and private zones
- [x] 1.2 Add CloudFront parsing to `parse_global_services()`: scan for `cloudfront-list-distributions.json`, extract distribution_id, domain_name, aliases, comment, status
- [x] 1.3 Return `route53_public_zones`, `route53_private_zones`, and `cloudfront_distributions` in the global_data dict
- [x] 1.4 Pass private zones through to per-region data for VPC placement (via global_data dict, consumed in main extension)

## 2. Route 53 Rendering

- [x] 2.1 Create `resource_route53.py` with `render_public_zones()` for Edge zone (icon + zone name + record count, stacked vertically)
- [x] 2.2 Add `render_private_zone()` for VPC pre-grid zone rendering (spanning element like LBs/EKS)
- [x] 2.3 Add private zone VPC placement logic: VPC association data → single-VPC fallback → account fallback

## 3. CloudFront Rendering

- [x] 3.1 Create `resource_cloudfront.py` with `render_distributions()` for Edge zone (icon + comment/alias + distribution ID dimmed, stacked vertically)

## 4. Edge Zone

- [x] 4.1 Create `resource_edge.py` with `render_edge_zone()` that renders the Edge rect with R53 left and CF right using a Row layout
- [x] 4.2 Compute Edge zone dimensions (height = max of R53 stack and CF stack, width = sum + gap)

## 5. Main Extension Integration

- [x] 5.1 Add "Edge" and "Route 53 Private" layers to `_create_layers` z-order
- [x] 5.2 Update `_render_multi_region` to render Edge zone above regions Row, offset Row down by Edge height
- [x] 5.3 Update `_render_single_region` to render Edge zone above VPCs
- [x] 5.4 Pass private R53 zones to `_render_vpcs` and through to `resource_vpc.py`

## 6. VPC Integration

- [x] 6.1 Update `resource_vpc.py` to accept and render private R53 zones in the pre-grid zone (below EKS, above subnets)
- [x] 6.2 Add private R53 zone height to `pad_top` calculation

## 7. Configuration

- [x] 7.1 Add `layout.edge` section to `default-config.yaml` (padding, column_gap, bottom_spacing)
- [x] 7.2 Add `layout.route53` section (icon_scale, font_size, card_gap)
- [x] 7.3 Add `layout.cloudfront` section (icon_scale, font_size, card_gap)

## 8. Testing

- [x] 8.1 Run headless test with account 111111111111 eu-west-1 to verify Edge zone renders with R53 zones and CF distributions
- [x] 8.2 Verify private zone `example.local.` renders inside VPC-customer
