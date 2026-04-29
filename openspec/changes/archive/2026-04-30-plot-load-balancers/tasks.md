## 1. Data Parsing

- [x] 1.1 Add LB parsing to `cloudia_parser.py` — parse `elbv2-describe-load-balancers.json`, return LBs with `name`, `lb_type`, `scheme`, `vpc_id`, `subnet_ids`
- [x] 1.2 Update `parse_region` and `parse_all_regions` return signatures to include load balancers (4th element)

## 2. Symbol Import

- [x] 2.1 Add `AWS-Resource-networking-content-delivery-light.svg` to `SYMBOL_FILES`

## 3. LB Rendering Module

- [x] 3.1 Create `resource_lb.py` with function to render a single LB card (icon + name + type label, no border)
- [x] 3.2 Add span line rendering — horizontal line from leftmost to rightmost spanned column
- [x] 3.3 Add function to compute LB zone height based on number of LBs
- [x] 3.4 Add LB config section to `default-config.yaml` under `layout.load_balancer`

## 4. Integration

- [x] 4.1 Update `render_vpc_with_subnets` to accept load balancers, compute LB zone height, and adjust VPC top padding
- [x] 4.2 Build subnet-to-column mapping and render LBs in the pre-grid zone using grid positions
- [x] 4.3 Create "Load Balancers" layer in z-order
- [x] 4.4 Update `aws-auto-diagram.py` to pass load balancers from parser to VPC renderer

## 5. Verify

- [x] 5.1 Run headless with us-east-2 data and verify ALB renders spanning two AZ columns
