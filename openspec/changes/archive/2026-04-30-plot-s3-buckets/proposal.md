## Why

S3 is a core AWS service but is currently absent from generated diagrams. Unlike EC2 and load balancers, S3 buckets live outside VPCs — they're global/account-level resources. Showing them gives a more complete picture of the account's infrastructure.

Bean: [inkscape-cloud-architect-s301](.beans/inkscape-cloud-architect-s301--plot-s3-buckets.md)

## What Changes

- Parse S3 bucket data from `s3-list-buckets.json`
- Introduce a "Global" pseudo-region for non-VPC services, rendered alongside real regions in the horizontal Row
- Render S3 buckets as icon+name cards stacked vertically inside the Global region
- Add `AWS-Resource-storage-light.svg` to imported symbol files for the bucket icon
- Add "S3" layer to the z-order
- In single-region mode, render the Global region below the VPCs (as the only region-level element)
- Add S3 config section for card styling

## Capabilities

### New Capabilities
- `s3-rendering`: Rendering S3 buckets as icon+name cards with configurable styling
- `global-region`: A "Global" pseudo-region for account-level services that live outside VPCs

### Modified Capabilities
- `config-loading`: Default config gains `layout.s3` section
- `layout-config`: New `layout.s3` values added to config structure
- `multi-region`: `parse_all_regions()` now synthesizes a Global region entry from global service data

## Impact

- **Parser**: `cloudia_parser.py` gains S3 parsing and Global region synthesis in `parse_all_regions()`
- **Rendering**: New `resource_s3.py` module for bucket cards
- **Symbols**: `AWS-Resource-storage-light.svg` added to `SYMBOL_FILES`
- **Layers**: New "S3" layer after "Load Balancers" in z-order
- **Config**: `default-config.yaml` gains `layout.s3` section
- **Main**: `aws-auto-diagram.py` updated for Global region handling in both single and multi-region modes
