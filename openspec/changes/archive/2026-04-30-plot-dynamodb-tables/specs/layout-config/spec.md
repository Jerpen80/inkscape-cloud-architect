## MODIFIED Requirements

### Requirement: Layout config structure
The default config SHALL include DynamoDB layout values.

#### Scenario: Default layout config
- **WHEN** the default config is loaded without user overrides
- **THEN** it SHALL contain the following DynamoDB-related structure:
  - `layout.dynamodb.icon_scale` = 0.5
  - `layout.dynamodb.font_size` = 13
  - `layout.dynamodb.card_gap` = 6
  - `layout.dynamodb.card_padding` = 4
