## ADDED Requirements

### Requirement: S3 bucket card rendering
Each S3 bucket SHALL be rendered as an icon + name text card.

#### Scenario: Bucket card visual style
- **WHEN** an S3 bucket is rendered
- **THEN** it SHALL display the `AWS-Resource-storage-light.svg:res-amazon-simple-storage-service-bucket` icon scaled per `layout.s3.icon_scale` and the bucket name in `layout.s3.font_size`

### Requirement: S3 buckets stack vertically
S3 bucket cards SHALL be stacked vertically with configurable gap.

#### Scenario: Multiple buckets rendered
- **WHEN** 5 S3 buckets are rendered
- **THEN** they SHALL be stacked top-to-bottom with `layout.s3.card_gap` between each card

### Requirement: S3 layer
S3 bucket cards SHALL be rendered on a dedicated "S3" layer.

#### Scenario: S3 layer z-order
- **WHEN** the extension creates layers
- **THEN** the "S3" layer SHALL be created after "Load Balancers" in z-order

### Requirement: S3 symbol import
The extension SHALL import `AWS-Resource-storage-light.svg` symbols for S3 bucket rendering.

#### Scenario: Storage symbols available
- **WHEN** the extension initializes
- **THEN** `AWS-Resource-storage-light.svg` SHALL be included in the imported symbol files
