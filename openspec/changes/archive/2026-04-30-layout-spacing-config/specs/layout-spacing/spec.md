## ADDED Requirements

### Requirement: VPC padding is configurable
The VPC rectangle padding SHALL be read from config at `vpc.padding.top`, `vpc.padding.sides`, and `vpc.padding.bottom`.

#### Scenario: Default VPC padding
- **WHEN** no user config override exists
- **THEN** VPC padding SHALL be top: 50, sides: 15, bottom: 15

#### Scenario: Custom VPC padding
- **WHEN** user config sets `vpc.padding.top: 80`
- **THEN** the VPC rectangle SHALL use 80px top padding while sides and bottom remain at defaults

### Requirement: VPC gap is configurable
The vertical gap between stacked VPCs SHALL be read from config at `vpc.gap`.

#### Scenario: Default VPC gap
- **WHEN** no user config override exists
- **THEN** the gap between VPCs SHALL be 25px

### Requirement: Subnet column gap is configurable
The horizontal gap between subnet columns (AZs) SHALL be read from config at `subnet.col_gap`.

#### Scenario: Default subnet column gap
- **WHEN** no user config override exists
- **THEN** the gap between subnet columns SHALL be 10px

### Requirement: Subnet row gap is configurable
The vertical gap between subnet rows SHALL be read from config at `subnet.row_gap`.

#### Scenario: Default subnet row gap
- **WHEN** no user config override exists
- **THEN** the gap between subnet rows SHALL be 15px

### Requirement: Subnet minimum width is configurable
The minimum width of a subnet cell SHALL be read from config at `subnet.min_width`.

#### Scenario: Default subnet minimum width
- **WHEN** no user config override exists
- **THEN** the minimum subnet cell width SHALL be 120px

### Requirement: Subnet height is configurable
The height of a subnet cell SHALL be read from config at `subnet.height`.

#### Scenario: Default subnet height
- **WHEN** no user config override exists
- **THEN** the subnet cell height SHALL be 50px
