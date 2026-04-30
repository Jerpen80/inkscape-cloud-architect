### Requirement: Layout config structure
The default config SHALL include a `layout` section with `mode`, `spaced`, and `dense` sub-sections. Each sub-section SHALL contain complete spacing values organized by resource type.

#### Scenario: Default layout mode
- **WHEN** the default config is loaded without user overrides
- **THEN** `layout.mode` SHALL be `"spaced"`

#### Scenario: Both presets contain all sections
- **WHEN** the default config is loaded
- **THEN** both `layout.spaced` and `layout.dense` SHALL contain complete sub-sections for all resource types (account, vpc, subnet, ec2, database, eks, lambda_function, load_balancer, asg, nat_gateway, s3, dynamodb, edge, route53, cloudfront, region, availability_zone, internet_gateway)

#### Scenario: Spaced preset uses full-size icons and template spacing
- **WHEN** the spaced preset is active
- **THEN** resource cards SHALL use `icon_scale: 1.0` and `font_size: 17`, and container padding SHALL be 3-5x larger than dense

#### Scenario: Dense preset matches previous defaults
- **WHEN** the dense preset is active
- **THEN** resource cards SHALL use `icon_scale: 0.5` and `font_size: 13`, matching the original compact layout

### Requirement: Rendering uses config values
All rendering modules SHALL read spacing values from the config dict instead of hardcoded constants.

#### Scenario: VPC rendering uses config
- **WHEN** a VPC is rendered
- **THEN** it SHALL use `layout.vpc.padding.*` and `layout.vpc.gap` from config for grid construction

#### Scenario: Subnet rendering uses config
- **WHEN** subnets are rendered inside a VPC grid
- **THEN** it SHALL use `layout.subnet.*` from config for cell sizing and gaps

### Requirement: User can override layout values
Users SHALL be able to override any layout spacing value via the user config override file.

#### Scenario: Override VPC padding
- **WHEN** the user config contains `layout.vpc.padding.top: 80`
- **THEN** VPCs SHALL render with 80px top padding while other values remain at defaults
