## ADDED Requirements

### Requirement: Parse internet gateways from cloudia data
The parser SHALL extract internet gateways from `ec2-describe-internet-gateways.json`.

#### Scenario: Available IGWs are parsed
- **WHEN** `parse_region` is called and `ec2-describe-internet-gateways.json` contains internet gateways with available attachments
- **THEN** each IGW SHALL be returned with `igw_id`, `name`, and `vpc_id`

#### Scenario: IGW name from tags
- **WHEN** an IGW has a Name tag
- **THEN** the `name` field SHALL use the Name tag value
- **WHEN** an IGW has no Name tag
- **THEN** the `name` field SHALL use the IGW ID

#### Scenario: Unattached IGWs are excluded
- **WHEN** an IGW has no attachments or no attachment with state "available"
- **THEN** it SHALL NOT be included in the returned list

#### Scenario: File not found
- **WHEN** `ec2-describe-internet-gateways.json` does not exist
- **THEN** an empty list SHALL be returned without error

### Requirement: Render IGW at VPC boundary
Each internet gateway SHALL be rendered at the top-right corner of its VPC rectangle.

#### Scenario: IGW placement
- **WHEN** a VPC has an attached IGW
- **THEN** the IGW icon SHALL be rendered at the top-right corner of the VPC rect, straddling the border

#### Scenario: IGW card content
- **WHEN** an IGW is rendered
- **THEN** it SHALL display the internet gateway icon and the IGW name below or to the left of the icon

#### Scenario: VPC without IGW
- **WHEN** a VPC has no attached IGW
- **THEN** no IGW element SHALL be rendered for that VPC

### Requirement: IGW symbol
The extension SHALL use the internet gateway icon from `AWS-Resource-networking-content-delivery-light.svg`.

#### Scenario: Symbol availability
- **WHEN** the extension runs
- **THEN** the symbol `AWS-Resource-networking-content-delivery-light.svg:res-amazon-vpc-internet-gateway` SHALL be available for rendering

### Requirement: IGWs on dedicated layer
IGW elements SHALL be rendered on a dedicated "Internet Gateways" layer.

#### Scenario: Layer creation
- **WHEN** IGWs are rendered
- **THEN** all IGW icons and names SHALL be placed on a layer named "Internet Gateways"

### Requirement: IGW layout configuration
IGW rendering parameters SHALL be configurable via `layout.internet_gateway` in the config.

#### Scenario: Default IGW config
- **WHEN** no user config override exists
- **THEN** `layout.internet_gateway` SHALL contain `icon_scale` and `font_size` with sensible defaults
