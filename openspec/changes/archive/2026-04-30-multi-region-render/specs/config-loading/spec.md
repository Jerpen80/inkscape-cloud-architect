## MODIFIED Requirements

### Requirement: Initial config structure
The default config SHALL include a `document` section with a `margin` key and a `layout` section with account, vpc, subnet, availability_zone, and region spacing values.

#### Scenario: Document margin default
- **WHEN** the default config is loaded without user overrides
- **THEN** `config["document"]["margin"]` SHALL be `20`

#### Scenario: Layout section present
- **WHEN** the default config is loaded without user overrides
- **THEN** `config["layout"]` SHALL contain `account`, `vpc`, `subnet`, `availability_zone`, and `region` subsections with padding, gap, and sizing values
