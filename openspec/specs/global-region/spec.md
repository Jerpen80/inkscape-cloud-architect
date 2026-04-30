### Requirement: Global pseudo-region
The extension SHALL support a "Global" pseudo-region for account-level services that live outside VPCs.

#### Scenario: Global region rendered in multi-region mode
- **WHEN** the user selects "All regions" and S3 buckets exist
- **THEN** a "Global" region rect SHALL be rendered as the first (leftmost) region in the horizontal Row

#### Scenario: Global region not rendered in single-region mode
- **WHEN** the user selects a specific region
- **THEN** no Global region SHALL be rendered

#### Scenario: Global region visual style
- **WHEN** the Global region is rendered
- **THEN** it SHALL use the same region rect style (blue stroke, `region.svg` icon) with "Global" as the label

### Requirement: Global region contains S3 buckets
S3 bucket cards SHALL be rendered inside the Global region rect.

#### Scenario: Buckets inside Global region
- **WHEN** S3 buckets exist and multi-region mode is active
- **THEN** bucket cards SHALL be rendered inside the Global region rect with region padding applied

### Requirement: No Global region when no global data
The Global region SHALL NOT be rendered when there is no global service data.

#### Scenario: No S3 buckets
- **WHEN** no `s3-list-buckets.json` data is found and no non-VPC Lambda functions exist
- **THEN** no Global region SHALL appear in the diagram

#### Scenario: CloudFront and Route 53 do not trigger Global region
- **WHEN** CloudFront distributions and public Route 53 zones exist but no S3 buckets or non-VPC Lambdas exist
- **THEN** no Global region SHALL appear (CloudFront and Route 53 render in the Edge zone, not the Global region)
