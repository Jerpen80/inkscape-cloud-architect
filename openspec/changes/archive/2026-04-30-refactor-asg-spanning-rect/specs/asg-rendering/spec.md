## MODIFIED Requirements

### Requirement: Render ASG as dashed container
Each ASG SHALL be rendered as a dashed rectangle that spans horizontally across the subnet columns it covers, wrapping its EC2 instances.

#### Scenario: ASG spanning two AZ columns
- **WHEN** an ASG has subnets in col 0 (us-east-2a) and col 1 (us-east-2b)
- **THEN** the dashed rectangle SHALL span from the left edge of col 0 to the right edge of col 1, crossing subnet boundaries and col_gap

#### Scenario: ASG in single column
- **WHEN** an ASG has subnets in only one column
- **THEN** the dashed rectangle SHALL be contained within that column's width

#### Scenario: ASG label
- **WHEN** an ASG spanning rect is rendered
- **THEN** it SHALL display the ASG icon, name on the first line, and capacity as `min:N desired:N max:N` on the second line at the top-left of the rect

#### Scenario: No visible fill
- **WHEN** an ASG spanning rect is rendered
- **THEN** it SHALL have no fill (transparent), only a dashed stroke

### Requirement: Rendering order preserves ASG grouping
EC2 instances belonging to ASGs SHALL be rendered grouped together within their subnet, below non-ASG instances.

#### Scenario: Mixed ASG and non-ASG instances
- **WHEN** a subnet has both ASG and non-ASG instances
- **THEN** non-ASG instances SHALL render first (top), followed by ASG-grouped instances within the spanning rect (below)

### Requirement: Subnet height accounts for ASG
Subnet height SHALL account for the ASG spanning rect label height and padding when ASG-grouped instances are present.

#### Scenario: Subnet with ASG instances
- **WHEN** a subnet contains EC2 instances that belong to an ASG
- **THEN** the subnet height SHALL include the ASG label height, padding, and the height of ASG-grouped instance cards

### Requirement: Column width accounts for ASG labels
Subnet column width SHALL grow to fit ASG label content (icon + name + padding).

#### Scenario: Long ASG name
- **WHEN** an ASG name is wider than the subnet label
- **THEN** the column width SHALL expand to fit the ASG label
