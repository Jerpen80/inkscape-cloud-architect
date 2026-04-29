## Why

CloudFront and Route 53 are the entry points for traffic into an AWS account but are currently absent from diagrams. They represent the "edge" layer — DNS resolution and CDN distribution — that sits above all regional infrastructure. Showing them completes the traffic flow picture from user to compute.

Bean: [inkscape-cloud-architect-cf01](.beans/inkscape-cloud-architect-cf01--plot-cloudfront-and-route53.md)

## What Changes

- Introduce an "Edge" rendering zone inside the Account rect, above the regions row, for CloudFront distributions and public Route 53 hosted zones
- Parse CloudFront data from `cloudfront-list-distributions.json` and Route 53 data from `route53-list-hosted-zones.json` (both found in us-east-1 as global API endpoints)
- Render public Route 53 hosted zones as icon+name cards showing zone name and record count
- Render CloudFront distributions as icon+name cards showing aliases/comment
- Render private Route 53 zones inside their associated VPC (with fallback to account level when VPC association cannot be determined)
- Add `AWS-Resource-networking-content-delivery-light.svg` is already imported; add `AWS-Service-networking-content-delivery.svg` for service-level icons
- Add "Edge" and "Route 53 Private" layers to z-order
- Add `layout.edge`, `layout.route53`, and `layout.cloudfront` config sections

## Capabilities

### New Capabilities
- `edge-rendering`: Rendering the Edge zone inside the Account rect with public Route 53 zones and CloudFront distributions
- `cloudfront-rendering`: Parsing and rendering CloudFront distributions as icon+name cards
- `route53-rendering`: Parsing and rendering Route 53 hosted zones, with public zones in Edge and private zones inside VPCs

### Modified Capabilities
- `account-rendering`: Account rect must accommodate the Edge zone above the regions row
- `global-region`: `parse_global_services()` gains CloudFront and Route 53 parsing alongside S3

## Impact

- **Parser**: `cloudia_parser.py` gains CloudFront and Route 53 parsing in `parse_global_services()`, plus private zone extraction per-region
- **Rendering**: New `resource_cloudfront.py` and `resource_route53.py` modules
- **Layout**: New Edge zone rendering in `aws-auto-diagram.py`, rendered above the regions Row inside the Account rect
- **VPC**: `resource_vpc.py` gains private Route 53 zone rendering (spanning element in pre-grid zone)
- **Symbols**: `AWS-Service-networking-content-delivery.svg` added to `SYMBOL_FILES`
- **Layers**: New "Edge" and "Route 53 Private" layers
- **Config**: `default-config.yaml` gains `layout.edge`, `layout.route53`, and `layout.cloudfront` sections
