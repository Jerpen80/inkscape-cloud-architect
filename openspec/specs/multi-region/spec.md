### Requirement: All regions option in INX
The extension SHALL offer an "All regions (with resources)" option as the first choice in the region dropdown.

#### Scenario: All regions selected
- **WHEN** the user selects "All regions (with resources)"
- **THEN** the extension SHALL scan all region subdirectories in the account data folder

#### Scenario: Specific region selected
- **WHEN** the user selects a specific region (e.g., "eu-west-1")
- **THEN** the extension SHALL render only that region, with no region rectangle, behaving as before

### Requirement: Filter empty regions
When rendering all regions, the extension SHALL skip regions that contain only default VPCs.

#### Scenario: Region with only default VPC
- **WHEN** a region's VPC data contains only VPCs where `IsDefault` is true
- **THEN** that region SHALL be skipped and not rendered

#### Scenario: Region with non-default VPC
- **WHEN** a region has at least one VPC where `IsDefault` is false
- **THEN** that region SHALL be included in the multi-region render

### Requirement: Horizontal region layout
When rendering multiple regions, regions SHALL be arranged horizontally (left to right).

#### Scenario: Multiple regions rendered
- **WHEN** 3 non-empty regions are found
- **THEN** they SHALL be placed side by side with a configurable gap between them

#### Scenario: Region ordering
- **WHEN** multiple regions are rendered
- **THEN** they SHALL be sorted alphabetically by region name

### Requirement: VPCs stack vertically within each region
Within a region, VPCs SHALL continue to stack vertically as they do in single-region mode.

#### Scenario: Region with multiple VPCs
- **WHEN** a region contains 2 VPCs
- **THEN** the VPCs SHALL be stacked top-to-bottom inside the region boundary

### Requirement: VPC is_default field
The parser SHALL include an `is_default` field in the VPC data dict, read from the AWS `IsDefault` JSON field.

#### Scenario: Default VPC parsed
- **WHEN** a VPC has `"IsDefault": true` in the AWS JSON
- **THEN** the parsed VPC dict SHALL have `"is_default": True`

### Requirement: parse_all_regions includes Global
The `parse_all_regions()` function SHALL synthesize a "Global" entry from global service data (S3 buckets) and prepend it to the results.

#### Scenario: Global region prepended
- **WHEN** `parse_all_regions()` is called and S3 bucket data exists
- **THEN** the first entry in the results SHALL be `("Global", {"s3_buckets": [...]})`

#### Scenario: No global data
- **WHEN** `parse_all_regions()` is called and no global service data exists
- **THEN** no Global entry SHALL be added to the results

### Requirement: S3 data discovery
The parser SHALL scan region subdirectories for `s3-list-buckets.json` and use the first one found.

#### Scenario: S3 file found
- **WHEN** `s3-list-buckets.json` exists in any region subdirectory
- **THEN** the parser SHALL read and parse bucket data from it

#### Scenario: S3 file not found
- **WHEN** no `s3-list-buckets.json` exists in any region subdirectory
- **THEN** the parser SHALL return an empty bucket list
