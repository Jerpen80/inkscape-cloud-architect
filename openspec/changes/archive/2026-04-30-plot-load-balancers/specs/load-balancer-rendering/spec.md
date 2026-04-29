## ADDED Requirements

### Requirement: Parse load balancers from cloudia data
The parser SHALL extract ALBs and NLBs from `elbv2-describe-load-balancers.json` and return them alongside VPCs, subnets, and instances.

#### Scenario: Load balancers are parsed
- **WHEN** `parse_region` is called and `elbv2-describe-load-balancers.json` contains load balancers
- **THEN** each load balancer SHALL be returned with `name`, `lb_type`, `scheme`, `vpc_id`, and `subnet_ids`

#### Scenario: Subnet IDs extracted from AvailabilityZones
- **WHEN** a load balancer has an `AvailabilityZones` array
- **THEN** each entry's `SubnetId` SHALL be collected into the `subnet_ids` list

### Requirement: Render load balancers as spanning elements
Each load balancer SHALL be rendered in a pre-grid zone within its VPC, visually spanning the AZ columns it is attached to.

#### Scenario: LB spanning two AZ columns
- **WHEN** an ALB is attached to subnets in us-east-2a (col 0) and us-east-2b (col 1)
- **THEN** it SHALL be rendered with a horizontal span line from the left edge of col 0 to the right edge of col 1

#### Scenario: LB card content
- **WHEN** a load balancer is rendered
- **THEN** it SHALL display the appropriate icon (ALB or NLB), the load balancer name, and a type/scheme label

#### Scenario: No visible rectangle
- **WHEN** a load balancer is rendered
- **THEN** there SHALL be no visible rectangle or border around the LB card

### Requirement: Multiple load balancers stack vertically
When a VPC contains multiple load balancers, they SHALL stack vertically in the pre-grid zone.

#### Scenario: Two LBs in one VPC
- **WHEN** a VPC has two load balancers
- **THEN** they SHALL be rendered stacked vertically with configurable spacing between them

### Requirement: LB zone adjusts VPC height
The VPC top padding SHALL grow to accommodate the load balancer zone when LBs are present.

#### Scenario: VPC with load balancers
- **WHEN** a VPC contains N load balancers
- **THEN** additional vertical space SHALL be added to the VPC's top area to fit the LB zone

#### Scenario: VPC without load balancers
- **WHEN** a VPC has no load balancers
- **THEN** the VPC layout SHALL remain unchanged

### Requirement: Type-specific symbols
The correct icon SHALL be used based on load balancer type.

#### Scenario: ALB symbol
- **WHEN** a load balancer has type "application"
- **THEN** the ALB icon from `AWS-Resource-networking-content-delivery-light.svg` SHALL be used

#### Scenario: NLB symbol
- **WHEN** a load balancer has type "network"
- **THEN** the NLB icon from `AWS-Resource-networking-content-delivery-light.svg` SHALL be used

### Requirement: Load balancers on dedicated layer
Load balancer elements SHALL be rendered on a dedicated "Load Balancers" layer.

#### Scenario: Layer creation
- **WHEN** load balancers are rendered
- **THEN** all LB icons, names, and span lines SHALL be placed on a layer named "Load Balancers"

### Requirement: LB layout configuration
LB rendering parameters SHALL be configurable via `layout.load_balancer` in the config.

#### Scenario: Default LB config
- **WHEN** no user config override exists
- **THEN** `layout.load_balancer` SHALL contain `icon_scale`, `font_size`, `card_height`, and `card_gap` with sensible defaults
