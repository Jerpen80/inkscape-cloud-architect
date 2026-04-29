## MODIFIED Requirements

### Requirement: Initial config structure
The default config SHALL include a `document` section with a `margin` key, a `layout` section with spacing values, and a `theme` section with light and dark color palettes.

#### Scenario: Document margin default
- **WHEN** the default config is loaded without user overrides
- **THEN** `config["document"]["margin"]` SHALL be `20`

#### Scenario: Layout section present
- **WHEN** the default config is loaded without user overrides
- **THEN** `config["layout"]` SHALL contain `account`, `vpc`, `subnet`, `availability_zone`, `region`, `ec2`, `database`, `load_balancer`, `s3`, and `nat_gateway` subsections

#### Scenario: Theme section present
- **WHEN** the default config is loaded without user overrides
- **THEN** `config["theme"]` SHALL contain `light` and `dark` subsections each with `background`, `text_color`, `text_dimmed_opacity`, and border color keys
