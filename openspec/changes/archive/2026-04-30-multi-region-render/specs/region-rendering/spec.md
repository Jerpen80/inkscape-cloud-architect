## ADDED Requirements

### Requirement: Region rectangle rendering
Each rendered region SHALL have a boundary rectangle with label and icon.

#### Scenario: Region rect visual style
- **WHEN** a region is rendered
- **THEN** it SHALL use blue (`#00a4a6`) stroke, 0.5 stroke-width, no fill, and the `AWS-Group-light.svg:region.svg` icon with the region name as label

#### Scenario: Region rect sizing
- **WHEN** a region contains VPCs
- **THEN** the region rectangle SHALL enclose all VPCs with padding defined in `layout.region.padding`

### Requirement: Regions layer z-order
Region rectangles SHALL be rendered on a dedicated "Regions" layer between "Accounts" and "VPCs".

#### Scenario: Layer ordering with all layers
- **WHEN** the extension creates layers for a multi-region render with account name
- **THEN** layers SHALL be created in order: Accounts, Regions, VPCs, Availability Zones, Subnets, EC2 (bottom to top)

#### Scenario: Layer ordering without account
- **WHEN** the extension creates layers for a multi-region render without account name
- **THEN** layers SHALL be created in order: Regions, VPCs, Availability Zones, Subnets, EC2 (bottom to top)
