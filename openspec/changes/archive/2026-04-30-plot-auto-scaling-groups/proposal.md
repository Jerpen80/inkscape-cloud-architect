## Why

Auto Scaling Groups are a fundamental AWS construct that manage EC2 instance lifecycle. The diagram already renders EC2 instances inside subnets, but there's no visual indication of which instances belong to an ASG. Showing ASGs as dashed containers around their instances reveals scaling boundaries and operational groupings.

Related task: [inkscape-cloud-architect-asg1](.beans/inkscape-cloud-architect-asg1--plot-auto-scaling-groups.md)

## What Changes

- Parse `autoscaling-describe-auto-scaling-groups.json` in `cloudia_parser.py`
- Render ASGs as dashed rectangles wrapping their EC2 instances within each subnet
- ASG label shows name and capacity (min/max/desired)
- ASGs with 0 running instances are skipped
- Subnet height calculation accounts for ASG label and border padding
- New "Auto Scaling Groups" layer
- ASG layout config under `layout.asg`

## Capabilities

### New Capabilities
- `asg-rendering`: Parsing and rendering Auto Scaling Groups as dashed containers around EC2 instances

### Modified Capabilities
<!-- None -->

## Impact

- Modified: `extensions/aws-auto-diagram/ica_utils/cloudia_parser.py` (parse ASGs)
- Modified: `extensions/aws-auto-diagram/ica_utils/resource_vpc.py` (pass ASGs, adjust height calc)
- Modified: `extensions/aws-auto-diagram/aws-auto-diagram.py` (layer, passthrough)
- Modified: `extensions/aws-auto-diagram/default-config.yaml` (ASG config)
- New: `extensions/aws-auto-diagram/ica_utils/resource_asg.py` (ASG container rendering)
- Modified: `extensions/aws-auto-diagram/ica_utils/resource_ec2.py` (expose card positions for ASG wrapping)
