## MODIFIED Requirements

### Requirement: Initial config structure
The default config SHALL include a `document` section with a `margin` key and a `layout` section with account, vpc, subnet, availability_zone, region, ec2, load_balancer, and s3 spacing values.

#### Scenario: Document margin default
- **WHEN** the default config is loaded without user overrides
- **THEN** `config["document"]["margin"]` SHALL be `20`

#### Scenario: Layout section present
- **WHEN** the default config is loaded without user overrides
- **THEN** `config["layout"]` SHALL contain `account`, `vpc`, `subnet`, `availability_zone`, `region`, `ec2`, `load_balancer`, and `s3` subsections
