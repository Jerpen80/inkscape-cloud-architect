## MODIFIED Requirements

### Requirement: Initial config structure
The default config SHALL include a `layout.legend` section for legend styling.

#### Scenario: Legend config defaults
- **WHEN** the default config is loaded without user overrides
- **THEN** `config["layout"]["legend"]` SHALL contain `enabled`, `padding`, `item_gap`, `row_gap`, `icon_scale`, `font_size`, and `top_spacing` values
