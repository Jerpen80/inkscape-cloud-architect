## Why

Lambda functions are a core compute resource in AWS. They have dual placement: VPC-attached Lambdas run inside subnets (spanning multiple AZs), while non-VPC Lambdas are regional/global services. Both need to appear on the diagram to give a complete picture of the architecture.

Related task: [inkscape-cloud-architect-lam1](.beans/inkscape-cloud-architect-lam1--plot-lambda-functions.md)

## What Changes

- Parse `lambda-list-functions.json` in `cloudia_parser.py`, splitting into VPC and non-VPC Lambdas
- VPC Lambdas: render as spanning elements in the pre-grid zone (same pattern as LB/EKS), with icon + name + runtime and span line across subnet columns
- Non-VPC Lambdas: render in the Global pseudo-region alongside S3 buckets
- New "Lambda" layer for VPC Lambda elements
- Lambda layout config under `layout.lambda_function`

## Capabilities

### New Capabilities
- `lambda-rendering`: Parsing and rendering Lambda functions with dual VPC/non-VPC placement

### Modified Capabilities
<!-- None -->

## Impact

- Modified: `extensions/aws-auto-diagram/ica_utils/cloudia_parser.py` (parse Lambdas, split VPC/non-VPC, add non-VPC to global services)
- Modified: `extensions/aws-auto-diagram/ica_utils/resource_vpc.py` (Lambda spanning zone, passthrough)
- Modified: `extensions/aws-auto-diagram/aws-auto-diagram.py` (layer, passthrough)
- Modified: `extensions/aws-auto-diagram/default-config.yaml` (Lambda config)
- New: `extensions/aws-auto-diagram/ica_utils/resource_lambda.py` (VPC Lambda spanning rendering)
- Modified: `extensions/aws-auto-diagram/ica_utils/resource_s3.py` or new global renderer (non-VPC Lambda rendering in Global region)
