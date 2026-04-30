## Why

Subnets are placed in grid rows in the order they appear in the AWS data per AZ. This means `private_az1` can end up in row 2 while `private_az2` is in row 1. This misalignment makes the diagram harder to read and prevents ASG spanning rectangles from working correctly (ASG subnets must be in the same row for a horizontal spanning rect).

## What Changes

- Sort subnets within each AZ by a deterministic "role" key before grid placement
- Extract role by stripping AZ-specific suffixes from subnet names (e.g., `public_az1` → `public`)
- Subnets with matching roles across AZs land in the same grid row
- Fallback to CIDR block sorting for unnamed subnets

## Capabilities

### New Capabilities
- `subnet-alignment`: Deterministic subnet row alignment by role across AZ columns

### Modified Capabilities
<!-- None -->

## Impact

- Modified: `extensions/aws-auto-diagram/ica_utils/resource_vpc.py` (subnet sorting within AZ groups before grid placement)
- Prerequisite for: `refactor-asg-spanning-rect`
