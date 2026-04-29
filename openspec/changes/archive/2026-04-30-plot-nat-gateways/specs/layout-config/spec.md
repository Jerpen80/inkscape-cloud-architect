## MODIFIED Requirements

### Requirement: Layout config structure
The default config SHALL include a `layout` section with spacing values organized by resource type.

#### Scenario: Default layout config
- **WHEN** the default config is loaded without user overrides
- **THEN** it SHALL contain the following NAT gateway-related structure:
  - `layout.nat_gateway.icon_scale` = 0.5
  - `layout.nat_gateway.font_size` = 13
  - `layout.nat_gateway.card_gap` = 8
  - `layout.nat_gateway.card_top` = 10
