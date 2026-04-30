## Why

Regions with only default VPCs were filtered out entirely. This hid real workloads running in default VPCs (e.g., EC2 instances in account 076504012268). Default VPCs should only be skipped when they contain no resources.

## What Changes

- Modified filter in `parse_all_regions`: default-only regions are now shown if they contain any resources (EC2, RDS, LBs, EKS, Lambda, NAT gateways, or ASGs)
- Empty default VPCs are still skipped

## Capabilities

### New Capabilities
<!-- None -->

### Modified Capabilities
- `config-loading`: Default VPC filtering behavior changed from "skip all default" to "skip empty default"

## Impact

- Modified: `extensions/aws-auto-diagram/ica_utils/cloudia_parser.py` (filter logic in `parse_all_regions`)
