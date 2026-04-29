## ADDED Requirements

### Requirement: Parse EC2 instances from cloudia data
The parser SHALL extract EC2 instances from `ec2-describe-instances.json` and return them alongside VPCs and subnets.

#### Scenario: Running instances are parsed
- **WHEN** `parse_region` is called and `ec2-describe-instances.json` contains running instances
- **THEN** each running instance SHALL be returned with `subnet_id`, `vpc_id`, `name`, `instance_type`, and `state`

#### Scenario: Non-running instances are excluded
- **WHEN** an instance has a state other than "running"
- **THEN** it SHALL NOT be included in the returned instances

#### Scenario: Instance name from tags
- **WHEN** an instance has a Name tag
- **THEN** the `name` field SHALL use the Name tag value
- **WHEN** an instance has no Name tag
- **THEN** the `name` field SHALL use the instance ID

### Requirement: Render EC2 instances inside subnets
Each running EC2 instance SHALL be rendered inside its subnet box as a borderless card with icon, name, and instance type stacked vertically and centered.

#### Scenario: Instance card layout
- **WHEN** an EC2 instance is rendered
- **THEN** it SHALL display the EC2 icon (centered), instance name (centered below icon), and instance type (centered below name)
- **THEN** there SHALL be no visible rectangle or border around the instance card

#### Scenario: Multiple instances in one subnet
- **WHEN** a subnet contains multiple running instances
- **THEN** the instances SHALL be stacked vertically within the subnet with configurable spacing between them

### Requirement: Dynamic subnet height
Subnet height SHALL grow to accommodate the instances it contains.

#### Scenario: Subnet with instances
- **WHEN** a subnet contains N instances
- **THEN** its height SHALL be at least: subnet label area + (N * instance card height) + spacing

#### Scenario: Subnet with no instances
- **WHEN** a subnet contains no instances
- **THEN** its height SHALL remain at the configured minimum `subnet.height`

#### Scenario: Row height is max across columns
- **WHEN** subnets in the same grid row have different instance counts
- **THEN** the row height SHALL be the maximum height needed across all cells in that row

### Requirement: EC2 instances on dedicated layer
EC2 instance elements SHALL be rendered on a dedicated "EC2" layer.

#### Scenario: Layer creation
- **WHEN** EC2 instances are rendered
- **THEN** all instance icons, names, and types SHALL be placed on a layer named "EC2"

### Requirement: EC2 symbol import
The extension SHALL import EC2 symbols from `AWS-Resource-compute-light.svg`.

#### Scenario: Symbol availability
- **WHEN** the extension runs
- **THEN** the symbol `AWS-Resource-compute-light.svg:res-amazon-ec2-instance` SHALL be available for rendering

### Requirement: EC2 layout configuration
EC2 rendering parameters SHALL be configurable via `layout.ec2` in the config.

#### Scenario: Default EC2 config
- **WHEN** no user config override exists
- **THEN** `layout.ec2` SHALL contain `icon_scale`, `font_size`, `card_gap`, and `card_top` with sensible defaults
