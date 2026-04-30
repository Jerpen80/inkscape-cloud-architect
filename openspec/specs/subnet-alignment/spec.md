### Requirement: Subnets aligned by role across AZ columns
Subnets with matching roles SHALL be placed in the same grid row across all AZ columns.

#### Scenario: Simple AZ suffix pattern
- **WHEN** a VPC has `public_az1` (us-east-2a) and `public_az2` (us-east-2b)
- **THEN** both SHALL be in the same grid row

#### Scenario: Dotted AZ suffix pattern
- **WHEN** a VPC has `local.customer.backend.1a` (eu-west-1a) and `local.customer.backend.1b` (eu-west-1b)
- **THEN** both SHALL be in the same grid row

#### Scenario: Region-based AZ suffix pattern
- **WHEN** a VPC has `yellow-db-us-west-2a` (us-west-2a) and `yellow-db-us-west-2b` (us-west-2b)
- **THEN** both SHALL be in the same grid row

#### Scenario: Unnamed subnets sorted by CIDR
- **WHEN** subnets have no Name tag
- **THEN** they SHALL be sorted by CIDR block as fallback

### Requirement: Deterministic subnet ordering within AZ
Subnets within each AZ SHALL be sorted by tier (public first, private middle, datastore/db last) then by role key.

#### Scenario: Tier ordering
- **WHEN** a VPC has public, private, and datastore subnets
- **THEN** public subnets SHALL be in the top rows, private in the middle, datastore at the bottom

#### Scenario: Consistent ordering across runs
- **WHEN** the extension renders the same data twice
- **THEN** subnets SHALL appear in the same grid positions both times
