## Why

The diagram currently shows VPCs and subnets but no compute resources. EC2 instances are the most straightforward resource to place — they have a direct `SubnetId` — making them the ideal first resource type to render inside subnets. This also forces solving the dynamic subnet height problem that all future resource types will need.

Related task: [inkscape-cloud-architect-ydn1](.beans/inkscape-cloud-architect-ydn1--plot-ec2-instances-inside-subnets.md)

## What Changes

- Parse `ec2-describe-instances.json` in `cloudia_parser.py` to extract running EC2 instances
- Render each instance inside its subnet as a borderless card: icon (centered), name (centered), instance type (centered)
- Make subnet height dynamic based on the number of instances it contains
- Update Grid to support variable row heights
- Add EC2 instances to a new "EC2" layer
- Add EC2 layout config to `default-config.yaml`

## Capabilities

### New Capabilities
- `ec2-rendering`: Parsing and rendering EC2 instances inside subnet boxes

### Modified Capabilities
- `layout-config`: Add EC2 spacing values to the config

## Impact

- Modified: `extensions/aws-auto-diagram/ica_utils/cloudia_parser.py` (parse EC2 instances)
- Modified: `extensions/aws-auto-diagram/ica_utils/layout.py` (variable row heights in Grid)
- Modified: `extensions/aws-auto-diagram/ica_utils/resource_vpc.py` (dynamic subnet height, render instances)
- Modified: `extensions/aws-auto-diagram/aws-auto-diagram.py` (pass instances to renderer, create EC2 layer)
- Modified: `extensions/aws-auto-diagram/default-config.yaml` (EC2 layout config)
- New: `extensions/aws-auto-diagram/ica_utils/resource_ec2.py` (EC2 instance rendering)
