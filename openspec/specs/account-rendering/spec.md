### Requirement: Optional account name argument
The extension SHALL accept an optional `account_name` text parameter via the INX interface.

#### Scenario: Account name provided
- **WHEN** the user sets `account_name` to "My AWS Account"
- **THEN** the account label SHALL be `"My AWS Account (222222222222)"` where the number is derived from the data directory

#### Scenario: Account name empty
- **WHEN** the user leaves `account_name` empty
- **THEN** the account label SHALL be just the account ID (e.g., `"222222222222"`)

### Requirement: Account rectangle always renders
The extension SHALL always render the account rectangle, regardless of whether `account_name` is provided.

#### Scenario: Account rect with name
- **WHEN** `account_name` is "Production" and data_dir is `account-data/222222222222`
- **THEN** the account rectangle SHALL render with label `"Production (222222222222)"`

#### Scenario: Account rect without name
- **WHEN** `account_name` is empty and data_dir is `account-data/222222222222`
- **THEN** the account rectangle SHALL render with label `"222222222222"`

### Requirement: Account ID from data directory
The account ID SHALL be derived from `basename(data_dir)`.

#### Scenario: Account ID extraction
- **WHEN** `data_dir` is `account-data/222222222222`
- **THEN** the account ID SHALL be `"222222222222"`

### Requirement: Account rectangle rendering
The extension SHALL render a rectangle around all resources.

#### Scenario: Account rect wraps all content
- **WHEN** resources are rendered
- **THEN** the account rectangle SHALL enclose all content with padding defined in `layout.account.padding`

#### Scenario: Account rect visual style
- **WHEN** the account rectangle is rendered
- **THEN** it SHALL use themed border color, 0.5 stroke-width, no fill, and the `AWS-Group-light.svg:cloud.svg` icon with the account label

### Requirement: Account layer z-order
The account rectangle SHALL be rendered on a dedicated "Accounts" layer that sits below the "VPCs" layer.

#### Scenario: Layer ordering
- **WHEN** the extension creates layers
- **THEN** the "Accounts" layer SHALL always be created in z-order

### Requirement: VPC offset always applied
VPCs SHALL always be positioned inside the account padding area, below the Edge zone if present.

#### Scenario: Stack origin offset
- **WHEN** the extension renders
- **THEN** the VPC stack origin SHALL be offset by account padding values

#### Scenario: Stack origin offset with Edge zone
- **WHEN** an Edge zone is rendered
- **THEN** the regions Row origin SHALL be offset down by the Edge zone height plus spacing, in addition to the account padding
