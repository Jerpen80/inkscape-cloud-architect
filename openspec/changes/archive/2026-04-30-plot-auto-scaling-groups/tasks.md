## 1. Data Parsing

- [x] 1.1 Add ASG parsing to `cloudia_parser.py` — parse `autoscaling-describe-auto-scaling-groups.json`, skip ASGs with 0 instances, return with `name`, `instance_ids`, `subnet_ids`, `min_size`, `max_size`, `desired_capacity`, `vpc_id`
- [x] 1.2 Update `parse_region` and `parse_all_regions` return signatures to include ASGs

## 2. EC2 Rendering: Instance Ordering

- [x] 2.1 Update EC2 rendering in `resource_vpc.py` to sort instances: non-ASG instances first, then grouped by ASG
- [x] 2.2 Build `instance_id → asg` mapping from ASG data, pass to EC2 rendering

## 3. ASG Rendering Module

- [x] 3.1 Create `resource_asg.py` with function to render a dashed container around a group of EC2 cards (position computed from card index + count)
- [x] 3.2 Add ASG label rendering (name + min/desired/max) at top of container
- [x] 3.3 Add `container_height()` function to compute extra height needed per ASG (label + padding)
- [x] 3.4 Add ASG config section to `default-config.yaml` under `layout.asg`

## 4. Integration

- [x] 4.1 Update subnet row height calculation to account for ASG label + padding per ASG-grouped instance block
- [x] 4.2 Render ASG containers after EC2 cards in the subnet rendering loop
- [x] 4.3 Create "Auto Scaling Groups" layer in z-order
- [x] 4.4 Update `aws-auto-diagram.py` to pass ASGs through

## 5. Verify

- [x] 5.1 Run headless with us-east-2 (222222222222) and verify ASG dashed containers around EC2 instances
