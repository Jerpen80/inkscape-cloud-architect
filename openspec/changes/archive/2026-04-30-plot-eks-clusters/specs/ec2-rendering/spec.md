## MODIFIED Requirements

### Requirement: Dynamic subnet height
Subnet height SHALL grow to accommodate the instances it contains.

#### Scenario: Subnet with instances
- **WHEN** a subnet contains N instances
- **THEN** its height SHALL be at least: subnet label area + (N * instance card height) + spacing

#### Scenario: Subnet with no instances
- **WHEN** a subnet contains no instances
- **THEN** its height SHALL remain at the configured minimum `subnet.height`

#### Scenario: Row height is max across columns
- **WHEN** subnets in the same grid row have different instance counts
- **THEN** the row height SHALL be the maximum height needed across all cells in that row

#### Scenario: VPC top padding includes EKS zone
- **WHEN** a VPC contains EKS clusters
- **THEN** the VPC top padding SHALL include the EKS zone height in addition to the load balancer zone height
