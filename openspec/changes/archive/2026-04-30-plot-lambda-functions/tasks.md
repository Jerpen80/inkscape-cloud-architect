## 1. Data Parsing

- [x] 1.1 Add Lambda parsing to `cloudia_parser.py` — parse `lambda-list-functions.json`, split into VPC Lambdas (with `vpc_id`, `subnet_ids`) and non-VPC Lambdas (with `name`, `runtime`)
- [x] 1.2 Return VPC Lambdas as 7th element from `parse_region`
- [x] 1.3 Collect non-VPC Lambdas into global services data (alongside S3 buckets)
- [x] 1.4 Update `parse_all_regions` return signature

## 2. VPC Lambda Rendering Module

- [x] 2.1 Create `resource_lambda.py` with spanning card rendering (icon + name + runtime + span line), mirroring `resource_eks.py`
- [x] 2.2 Add `zone_height()` and `render_lambda_zone()` functions
- [x] 2.3 Add Lambda config section to `default-config.yaml` under `layout.lambda_function`

## 3. Non-VPC Lambda Rendering

- [x] 3.1 Add non-VPC Lambda list rendering function to `resource_lambda.py` (icon + name, like S3 pattern)
- [x] 3.2 Integrate non-VPC Lambda rendering in Global region (in `aws-auto-diagram.py`)

## 4. Integration

- [x] 4.1 Update `render_vpc_with_subnets` to accept `vpc_lambdas`, compute Lambda zone height, render in pre-grid zone
- [x] 4.2 Create "Lambda" layer in z-order
- [x] 4.3 Update `aws-auto-diagram.py` to pass VPC Lambdas and non-VPC Lambdas through

## 5. Verify

- [x] 5.1 Run headless with us-east-2 (222222222222) — single-region OK (no non-VPC Lambdas in single-region, by design)
- [x] 5.2 Run headless multi-region (all) — 12 Lambda icons rendered including non-VPC Lambdas in Global region
