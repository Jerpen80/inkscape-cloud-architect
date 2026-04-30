## Context

LBs and EKS clusters already render as spanning elements in a pre-grid zone within VPCs. S3 buckets render in the Global pseudo-region. Lambda functions need both patterns: VPC-attached Lambdas span subnets (like LB/EKS), non-VPC Lambdas go in Global (like S3).

## Goals / Non-Goals

**Goals:**
- Parse Lambda functions and classify as VPC or non-VPC
- Render VPC Lambdas as spanning cards in the pre-grid zone
- Render non-VPC Lambdas in the Global pseudo-region

**Non-Goals:**
- Lambda layer/alias details
- Invocation patterns or event source mappings
- Grouping Lambdas by shared subnet patterns

## Decisions

### 1. Dual placement via parser split

`parse_region` returns VPC Lambdas as a separate list (7th return element: `vpc_lambdas`). Non-VPC Lambdas are added to the global services dict in `parse_global_services` (or collected per-region and merged).

Actually, since `parse_global_services` scans all regions, it's simpler to: collect non-VPC Lambdas during `parse_region` but return them separately, then aggregate them in `parse_all_regions` into the global data. For single-region mode, non-VPC Lambdas can be rendered in a simple list below VPCs.

### 2. VPC Lambda spanning — follows EKS pattern exactly

`resource_lambda.py` mirrors `resource_eks.py`: `zone_height()`, `render_lambda()`, `render_lambda_zone()`. Each Lambda card shows icon + name + runtime, with a span line across its subnet columns.

### 3. Non-VPC Lambda rendering — follows S3 pattern

A simple vertical list: icon (left) + function name (right), stacked vertically. Rendered on the same "Lambda" layer. Added to the Global region data alongside S3 buckets.

### 4. Symbol

`AWS-Resource-compute-light.svg:res-aws-lambda-lambda-function` — already imported via the compute symbol file.

### 5. Config key: `layout.lambda_function`

Using `lambda_function` not `lambda` to avoid Python keyword collision in any future dict-to-object mapping. Contains the same spanning config as LB/EKS plus non-VPC list config.

## Risks / Trade-offs

- [Many VPC Lambdas] → 10+ Lambdas in one VPC makes the spanning zone tall. Acceptable for now — full cards are consistent with the rest. Can optimize later with compact rendering.
- [Non-VPC Lambda aggregation] → In multi-region mode, non-VPC Lambdas from different regions all go into Global. Could get long. Acceptable — mirrors S3 bucket behavior.
