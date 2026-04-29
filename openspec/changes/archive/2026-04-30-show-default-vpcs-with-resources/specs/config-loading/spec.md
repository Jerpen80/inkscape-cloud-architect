## MODIFIED Requirements

### Requirement: Initial config structure
The default config SHALL include a `document` section with a `margin` key and a `layout` section with account, vpc, and subnet spacing values.

#### Scenario: Document margin default
- **WHEN** the default config is loaded without user overrides
- **THEN** `config["document"]["margin"]` SHALL be `20`

#### Scenario: Layout section present
- **WHEN** the default config is loaded without user overrides
- **THEN** `config["layout"]` SHALL contain `account`, `vpc`, and `subnet` subsections with padding, gap, and sizing values

#### Scenario: Default VPC with resources is shown
- **WHEN** a region contains only default VPCs but those VPCs have running resources (EC2, RDS, LBs, EKS, Lambda, NAT gateways, or ASGs)
- **THEN** the region SHALL be included in the rendered output

#### Scenario: Empty default VPC is skipped
- **WHEN** a region contains only default VPCs with no running resources
- **THEN** the region SHALL be excluded from the rendered output
