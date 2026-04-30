## ADDED Requirements

### Requirement: Optional account name argument
The extension SHALL accept an optional `account_name` text parameter via the INX interface.

#### Scenario: Account name provided
- **WHEN** the user sets `account_name` to "My AWS Account"
- **THEN** the extension SHALL render an account boundary rectangle with that label

#### Scenario: Account name empty
- **WHEN** the user leaves `account_name` empty
- **THEN** the extension SHALL NOT render an account boundary rectangle

### Requirement: Account rectangle rendering
When an account name is provided, the extension SHALL render a rectangle around all resources in the region.

#### Scenario: Account rect wraps all VPCs
- **WHEN** `account_name` is set and VPCs are rendered
- **THEN** the account rectangle SHALL enclose all VPC rectangles with padding defined in `layout.account.padding`

#### Scenario: Account rect visual style
- **WHEN** the account rectangle is rendered
- **THEN** it SHALL use black (`#000000`) stroke, 0.5 stroke-width, no fill, and the `AWS-Group-light.svg:cloud.svg` icon with the account name as label

### Requirement: Account layer z-order
The account rectangle SHALL be rendered on a dedicated "Accounts" layer that sits below the "VPCs" layer.

#### Scenario: Layer ordering
- **WHEN** the extension creates layers
- **THEN** layers SHALL be created in order: Accounts, VPCs, Subnets (bottom to top)

### Requirement: VPC offset when account is present
When an account rectangle is rendered, VPCs SHALL be positioned inside the account padding area.

#### Scenario: Stack origin offset
- **WHEN** `account_name` is set with `layout.account.padding.left` of 20 and `layout.account.padding.top` of 50
- **THEN** the VPC stack origin SHALL be offset by (20, 50) from the account rectangle origin
