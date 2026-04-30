## ADDED Requirements

### Requirement: Layout mode selection via INX parameter
The extension SHALL accept a `--layout_mode` parameter via the INX dialog with options "Spaced" and "Dense".

#### Scenario: Spaced mode selected
- **WHEN** the user selects "Spaced" from the layout dropdown
- **THEN** the extension SHALL use the spaced layout preset with template-scale spacing

#### Scenario: Dense mode selected
- **WHEN** the user selects "Dense" from the layout dropdown
- **THEN** the extension SHALL use the dense layout preset with compact spacing

#### Scenario: Default layout mode
- **WHEN** no layout mode is explicitly selected
- **THEN** the extension SHALL default to "Spaced"

### Requirement: Layout mode presets in config
The config SHALL contain `layout.spaced` and `layout.dense` sub-sections with complete sets of layout values.

#### Scenario: Spaced preset values
- **WHEN** the spaced mode is resolved
- **THEN** spacing values SHALL be derived from the reference template measurements (approximately 3-5x larger than dense)

#### Scenario: Dense preset values
- **WHEN** the dense mode is resolved
- **THEN** spacing values SHALL match the previous default compact values

#### Scenario: Both presets are complete
- **WHEN** either preset is resolved
- **THEN** it SHALL contain all layout sub-sections (account, vpc, subnet, ec2, database, eks, lambda_function, load_balancer, asg, nat_gateway, s3, dynamodb, edge, route53, cloudfront, region, availability_zone, internet_gateway)

### Requirement: Layout mode resolution at startup
The extension SHALL resolve the layout mode parameter to a complete set of layout values at startup.

#### Scenario: Resolution merges into config
- **WHEN** the extension resolves the layout mode
- **THEN** the selected preset's values SHALL be merged into `config["layout"]` so renderers see no structural change

#### Scenario: User overrides apply after resolution
- **WHEN** a user provides custom layout values in their override config
- **THEN** the custom values SHALL take precedence over the resolved preset values

### Requirement: Layout mode in headless runner
The headless runner SHALL accept an optional layout mode argument.

#### Scenario: Layout mode passed to extension
- **WHEN** the headless runner is called with a layout mode argument
- **THEN** it SHALL pass the value as `--layout_mode` to the extension
