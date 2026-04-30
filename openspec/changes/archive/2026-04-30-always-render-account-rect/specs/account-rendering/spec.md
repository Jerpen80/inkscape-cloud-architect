## MODIFIED Requirements

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

### Requirement: VPC offset always applied
VPCs SHALL always be positioned inside the account padding area.

#### Scenario: Stack origin offset
- **WHEN** the extension renders (regardless of account_name)
- **THEN** the VPC stack origin SHALL be offset by account padding values
