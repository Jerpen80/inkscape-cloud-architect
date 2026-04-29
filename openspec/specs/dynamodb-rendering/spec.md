### Requirement: DynamoDB table data parsing
The parser SHALL read `dynamodb-list-tables.json` and extract table names.

#### Scenario: Tables found
- **WHEN** `dynamodb-list-tables.json` exists and contains table names
- **THEN** the parser SHALL return a list of DynamoDB table dicts with `type: "dynamodb"` and `name`

#### Scenario: No tables
- **WHEN** `dynamodb-list-tables.json` is empty or missing
- **THEN** the parser SHALL return an empty DynamoDB table list

### Requirement: DynamoDB table card rendering
Each DynamoDB table SHALL be rendered as an icon + name text card.

#### Scenario: Table card visual style
- **WHEN** a DynamoDB table is rendered
- **THEN** it SHALL display the `AWS-Resource-database-light.svg:res-amazon-dynamodb-table` icon scaled per `layout.dynamodb.icon_scale` and the table name in `layout.dynamodb.font_size`

### Requirement: DynamoDB tables are regional non-VPC resources
DynamoDB tables SHALL be rendered inside the region rect, below VPCs.

#### Scenario: Multi-region mode
- **WHEN** rendering all regions and a region has DynamoDB tables
- **THEN** the tables SHALL render inside that region's rect, below the VPC stack

#### Scenario: Single-region mode
- **WHEN** rendering a single region that has DynamoDB tables
- **THEN** the tables SHALL render below the VPCs

#### Scenario: Region with no DynamoDB tables
- **WHEN** a region has no DynamoDB tables
- **THEN** no DynamoDB content SHALL be rendered for that region

### Requirement: DynamoDB layer
DynamoDB table cards SHALL be rendered on a dedicated "DynamoDB" layer.

#### Scenario: Layer z-order
- **WHEN** the extension creates layers
- **THEN** the "DynamoDB" layer SHALL be created after "S3" in z-order
