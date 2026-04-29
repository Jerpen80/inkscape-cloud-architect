## MODIFIED Requirements

### Requirement: No Global region when no global data
The Global region SHALL NOT be rendered when there is no global service data.

#### Scenario: No S3 buckets
- **WHEN** no `s3-list-buckets.json` data is found and no non-VPC Lambda functions exist
- **THEN** no Global region SHALL appear in the diagram

#### Scenario: CloudFront and Route 53 do not trigger Global region
- **WHEN** CloudFront distributions and public Route 53 zones exist but no S3 buckets or non-VPC Lambdas exist
- **THEN** no Global region SHALL appear (CloudFront and Route 53 render in the Edge zone, not the Global region)
