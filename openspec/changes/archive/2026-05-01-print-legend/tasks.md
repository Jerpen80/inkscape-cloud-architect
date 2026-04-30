## 1. Config & Registry

- [x] 1.1 Add `layout.legend` section to `default-config.yaml`
- [x] 1.2 Create `ica_utils/legend.py` with `register_legend()` registry and `render_legend()` function

## 2. Register All Resource Modules

- [x] 2.1 Add `register_legend()` calls to container modules: resource_account, resource_edge, resource_region, resource_vpc (VPC + both subnet types), resource_az
- [x] 2.2 Add `register_legend()` calls to resource modules: resource_ec2, resource_db (RDS + ElastiCache), resource_nat, resource_lb, resource_eks, resource_lambda, resource_s3, resource_dynamodb, resource_cloudfront, resource_route53, resource_asg

## 3. Integration

- [x] 3.1 Add "Legend" layer to `_create_layers()` at top of z-order
- [x] 3.2 Call `render_legend()` in `effect()` after content rendering, before `resize_to_fit()`

## 4. Verification

- [x] 4.1 Run headless test with account 111111111111 eu-west-1 — legend renders with 16 entries (VPC, subnets, Account, Edge, EC2, LB, RDS, ElastiCache, EKS, NAT, ASG, R53, CF)
- [x] 4.2 Run headless test with account 222222222222 eu-west-1 — legend only shows 7 entries (VPC, subnets, Account, Edge, R53, CF — no compute resources)
