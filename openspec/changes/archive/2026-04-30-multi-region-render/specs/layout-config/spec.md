## MODIFIED Requirements

### Requirement: Layout config structure
The default config SHALL include a `layout` section with spacing values organized by resource type.

#### Scenario: Default layout config
- **WHEN** the default config is loaded without user overrides
- **THEN** it SHALL contain the following structure:
  - `layout.account.padding.top` = 50
  - `layout.account.padding.right` = 20
  - `layout.account.padding.bottom` = 20
  - `layout.account.padding.left` = 20
  - `layout.vpc.padding.top` = 60
  - `layout.vpc.padding.right` = 15
  - `layout.vpc.padding.bottom` = 15
  - `layout.vpc.padding.left` = 15
  - `layout.vpc.gap` = 25
  - `layout.subnet.min_width` = 120
  - `layout.subnet.height` = 50
  - `layout.subnet.col_gap` = 10
  - `layout.subnet.row_gap` = 15
  - `layout.region.padding.top` = 50
  - `layout.region.padding.right` = 15
  - `layout.region.padding.bottom` = 15
  - `layout.region.padding.left` = 15
  - `layout.region.gap` = 20
