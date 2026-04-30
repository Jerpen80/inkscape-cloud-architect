## MODIFIED Requirements

### Requirement: Layout config structure
The default config SHALL include a `layout` section with spacing values organized by resource type.

#### Scenario: Default layout config
- **WHEN** the default config is loaded without user overrides
- **THEN** it SHALL contain the following S3-related structure:
  - `layout.s3.icon_scale` = 0.5
  - `layout.s3.font_size` = 13
  - `layout.s3.card_gap` = 6
  - `layout.s3.card_padding` = 4
