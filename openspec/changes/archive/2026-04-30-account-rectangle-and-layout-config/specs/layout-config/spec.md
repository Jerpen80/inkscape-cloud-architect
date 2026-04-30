## ADDED Requirements

### Requirement: Layout config structure
The default config SHALL include a `layout` section with spacing values organized by resource type.

#### Scenario: Default layout config
- **WHEN** the default config is loaded without user overrides
- **THEN** it SHALL contain the following structure:
  - `layout.account.padding.top` = 50
  - `layout.account.padding.right` = 20
  - `layout.account.padding.bottom` = 20
  - `layout.account.padding.left` = 20
  - `layout.vpc.padding.top` = 50
  - `layout.vpc.padding.right` = 15
  - `layout.vpc.padding.bottom` = 15
  - `layout.vpc.padding.left` = 15
  - `layout.vpc.gap` = 25
  - `layout.subnet.min_width` = 120
  - `layout.subnet.height` = 50
  - `layout.subnet.col_gap` = 10
  - `layout.subnet.row_gap` = 15

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
