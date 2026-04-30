## MODIFIED Requirements

### Requirement: Initial config structure
The default config SHALL include a `layout` section with a `dynamodb` subsection for table card styling.

#### Scenario: Layout section present
- **WHEN** the default config is loaded without user overrides
- **THEN** `config["layout"]` SHALL contain a `dynamodb` subsection with icon_scale, font_size, card_gap, and card_padding values
