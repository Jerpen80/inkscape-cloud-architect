### Requirement: Parse Lambda functions from cloudia data
The parser SHALL extract Lambda functions from `lambda-list-functions.json` and classify them as VPC-attached or non-VPC.

#### Scenario: VPC Lambda parsed
- **WHEN** a Lambda function has `VpcConfig.VpcId` and `VpcConfig.SubnetIds`
- **THEN** it SHALL be returned as a VPC Lambda with `name`, `runtime`, `vpc_id`, and `subnet_ids`

#### Scenario: Non-VPC Lambda parsed
- **WHEN** a Lambda function has no `VpcConfig.VpcId` or empty `SubnetIds`
- **THEN** it SHALL be classified as a non-VPC Lambda with `name` and `runtime`

### Requirement: Render VPC Lambdas as spanning elements
VPC-attached Lambda functions SHALL be rendered in the pre-grid zone within their VPC, spanning the AZ columns of their subnets.

#### Scenario: VPC Lambda card layout
- **WHEN** a VPC Lambda is rendered
- **THEN** it SHALL display the Lambda icon (left-aligned), function name, and runtime
- **THEN** a span line SHALL extend from its leftmost to rightmost subnet column

#### Scenario: Multiple VPC Lambdas in one VPC
- **WHEN** a VPC has multiple VPC-attached Lambdas
- **THEN** they SHALL stack vertically in the pre-grid zone with configurable spacing

### Requirement: VPC Lambda zone adjusts VPC height
The VPC top padding SHALL grow to accommodate the Lambda zone when VPC Lambdas are present.

#### Scenario: VPC with Lambdas
- **WHEN** a VPC contains N VPC-attached Lambdas
- **THEN** additional vertical space SHALL be added to the VPC's top area

#### Scenario: VPC without Lambdas
- **WHEN** a VPC has no VPC-attached Lambdas
- **THEN** the VPC layout SHALL remain unchanged

### Requirement: Render non-VPC Lambdas in Global region
Non-VPC Lambda functions SHALL be rendered in the Global pseudo-region as a simple list.

#### Scenario: Non-VPC Lambda list
- **WHEN** non-VPC Lambdas exist
- **THEN** they SHALL be rendered as icon + function name pairs, stacked vertically in the Global region

### Requirement: Lambda elements on dedicated layer
All Lambda elements SHALL be rendered on a dedicated "Lambda" layer.

#### Scenario: Layer creation
- **WHEN** Lambda functions are rendered (VPC or non-VPC)
- **THEN** all Lambda icons, names, and span lines SHALL be placed on a layer named "Lambda"

### Requirement: Lambda layout configuration
Lambda rendering parameters SHALL be configurable via `layout.lambda_function` in the config.

#### Scenario: Default Lambda config
- **WHEN** no user config override exists
- **THEN** `layout.lambda_function` SHALL contain spanning card config (icon_scale, font_size, card_height, card_gap, span_line_color) and non-VPC list config
