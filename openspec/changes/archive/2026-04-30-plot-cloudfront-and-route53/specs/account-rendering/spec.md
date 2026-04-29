## MODIFIED Requirements

### Requirement: VPC offset when account is present
When an account rectangle is rendered, VPCs SHALL be positioned inside the account padding area, below the Edge zone if present.

#### Scenario: Stack origin offset
- **WHEN** `account_name` is set with `layout.account.padding.left` of 20 and `layout.account.padding.top` of 50
- **THEN** the VPC stack origin SHALL be offset by (20, 50) from the account rectangle origin

#### Scenario: Stack origin offset with Edge zone
- **WHEN** `account_name` is set and an Edge zone is rendered
- **THEN** the regions Row origin SHALL be offset down by the Edge zone height plus spacing, in addition to the account padding
