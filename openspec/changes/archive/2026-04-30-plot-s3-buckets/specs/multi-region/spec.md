## MODIFIED Requirements

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
