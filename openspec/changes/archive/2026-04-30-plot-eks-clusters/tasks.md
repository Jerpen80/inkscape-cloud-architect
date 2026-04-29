## 1. Parser

- [x] 1.1 Add EKS cluster parsing to `cloudia_parser.py`: read `eks-list-clusters.json` and `eks-describe-cluster/<name>` files, extract name, version, vpc_id, subnet_ids, status. Filter to ACTIVE only. Skip missing describe files.
- [x] 1.2 Update `parse_region` return to include eks_clusters as 6th element (db_instances was already 5th)
- [x] 1.3 Update `parse_all_regions` to pass eks_clusters through region tuples

## 2. Rendering

- [x] 2.1 Create `resource_eks.py` with `zone_height()`, `render_eks()`, and `render_eks_zone()` following the `resource_lb.py` pattern
- [x] 2.2 Add `AWS-Service-containers.svg` to `SYMBOL_FILES` in `aws-auto-diagram.py`
- [x] 2.3 Add "EKS" layer to `_create_layers` z-order (after "Load Balancers")

## 3. VPC Integration

- [x] 3.1 Update `resource_vpc.py` to import `resource_eks` and accept `eks_clusters` parameter
- [x] 3.2 Add EKS zone height to `pad_top` calculation (after LB zone height)
- [x] 3.3 Render EKS zone between LB zone and subnet grid using `render_eks_zone()`

## 4. Main Extension

- [x] 4.1 Update `_render_single_region` to unpack and pass eks_clusters
- [x] 4.2 Update `_render_multi_region` to unpack and pass eks_clusters
- [x] 4.3 Update `_render_vpcs` to accept and forward eks_clusters

## 5. Configuration

- [x] 5.1 Add `layout.eks` section to `default-config.yaml` with icon_scale, font_size, card_height, card_gap, span_line_color (#FF9900), span_line_width, span_line_dasharray

## 6. Testing

- [x] 6.1 Run headless test with account 111111111111 eu-west-1 to verify EKS clusters render correctly
