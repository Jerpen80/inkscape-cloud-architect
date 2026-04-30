## ADDED Requirements

### Requirement: Parse Auto Scaling Groups
The parser SHALL extract ASGs from `autoscaling-describe-auto-scaling-groups.json`.

#### Scenario: ASG with instances parsed
- **WHEN** `parse_region` is called and an ASG has running instances
- **THEN** the ASG SHALL be returned with `name`, `instance_ids`, `subnet_ids`, `min_size`, `max_size`, `desired_capacity`, and `vpc_id`

#### Scenario: ASG with zero instances skipped
- **WHEN** an ASG has no running instances (empty Instances list)
- **THEN** it SHALL NOT be included in the returned ASGs

### Requirement: Render ASG as dashed container
Each ASG SHALL be rendered as a dashed rectangle wrapping its EC2 instances within each subnet.

#### Scenario: ASG container in a subnet
- **WHEN** an ASG has instances in a subnet
- **THEN** a dashed rectangle SHALL wrap those EC2 instance cards with padding

#### Scenario: ASG label
- **WHEN** an ASG container is rendered
- **THEN** it SHALL display the ASG name and capacity as `name (min/desired/max)` at the top of the dashed rectangle

#### Scenario: No visible fill
- **WHEN** an ASG container is rendered
- **THEN** it SHALL have no fill (transparent), only a dashed stroke

### Requirement: ASG spans multiple subnets
When an ASG has instances across multiple subnets, a separate dashed container SHALL be drawn in each subnet.

#### Scenario: ASG across two AZs
- **WHEN** an ASG has 1 instance in subnet-a and 1 instance in subnet-b
- **THEN** two separate dashed containers SHALL be drawn, one in each subnet

### Requirement: Subnet height accounts for ASG
Subnet height SHALL grow to accommodate ASG label and padding when ASG-grouped instances are present.

#### Scenario: Subnet with ASG instances
- **WHEN** a subnet contains EC2 instances that belong to an ASG
- **THEN** the subnet height SHALL include the ASG label height and container padding

### Requirement: Rendering order preserves ASG grouping
EC2 instances belonging to ASGs SHALL be rendered grouped together within their subnet.

#### Scenario: Mixed ASG and non-ASG instances
- **WHEN** a subnet has both ASG and non-ASG instances
- **THEN** non-ASG instances SHALL render first, followed by ASG-grouped instances with their dashed containers

### Requirement: ASG elements on dedicated layer
ASG dashed containers and labels SHALL be rendered on a dedicated "Auto Scaling Groups" layer.

#### Scenario: Layer creation
- **WHEN** ASGs are rendered
- **THEN** all ASG containers and labels SHALL be placed on a layer named "Auto Scaling Groups"

### Requirement: ASG layout configuration
ASG rendering parameters SHALL be configurable via `layout.asg` in the config.

#### Scenario: Default ASG config
- **WHEN** no user config override exists
- **THEN** `layout.asg` SHALL contain `stroke_color`, `stroke_width`, `stroke_dasharray`, `label_height`, `padding`, and `font_size`
