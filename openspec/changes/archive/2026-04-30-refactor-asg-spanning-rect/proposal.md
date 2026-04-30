## Why

ASGs currently render as per-subnet dashed containers, which loses their multi-AZ nature. An ASG like `ec2-asg-powerbi_gateway-prod` spans `private_az1` and `private_az2`, but the current rendering only shows a box in the subnet where instances happen to be. The ASG should visually span across subnet columns, similar to how AZ columns span rows.

## What Changes

- Refactor `resource_asg.py` to render ASGs as horizontal spanning rectangles that cross subnet column boundaries
- ASG rect wraps its EC2 instances across all subnets it spans, from leftmost to rightmost column
- Non-ASG instances render first in the subnet, ASG-grouped instances render within the spanning rect below
- ASG label (icon + name, capacity on second line) at the top-left of the spanning rect

## Capabilities

### Modified Capabilities
- `asg-rendering`: ASGs change from per-subnet containers to horizontal spanning rectangles across columns

## Impact

- Modified: `extensions/aws-auto-diagram/ica_utils/resource_asg.py` (rewrite spanning rect logic)
- Modified: `extensions/aws-auto-diagram/ica_utils/resource_vpc.py` (adjust EC2 rendering offsets and ASG rendering call)
