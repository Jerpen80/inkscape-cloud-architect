## Why

DynamoDB is a commonly used AWS service but absent from generated diagrams. Unlike RDS and ElastiCache (which live inside VPCs), DynamoDB is a regional managed service that exists outside VPCs. Showing DynamoDB tables gives visibility into the serverless data layer of the account.

Bean: [inkscape-cloud-architect-ddb1](.beans/inkscape-cloud-architect-ddb1--plot-dynamodb-tables.md)

## What Changes

- Parse DynamoDB table names from `dynamodb-list-tables.json`
- Render tables as icon+name cards (same pattern as S3 buckets)
- Place tables inside the region rect, below VPCs — DynamoDB is regional, not global
- In single-region mode: render below VPCs directly
- In multi-region mode: render inside each region's section, below that region's VPC stack
- Add dedicated "DynamoDB" layer (separate from "Database" which is RDS/ElastiCache)
- Add `layout.dynamodb` config section

Note: DynamoDB Global Tables (cross-region replication) are out of scope — no `describe-global-table` data available. Tracked separately in inkscape-cloud-architect-ddbg.

## Capabilities

### New Capabilities
- `dynamodb-rendering`: Rendering DynamoDB tables as icon+name cards with configurable styling, placed as regional non-VPC resources

### Modified Capabilities
- `config-loading`: Default config gains `layout.dynamodb` section
- `layout-config`: New `layout.dynamodb` values added

## Impact

- **Parser**: `cloudia_parser.py` gains DynamoDB table parsing in `parse_region()`
- **Rendering**: New `resource_dynamodb.py` module
- **Layers**: New "DynamoDB" layer in z-order
- **Config**: `default-config.yaml` gains `layout.dynamodb` section
- **Main**: `aws-auto-diagram.py` renders DynamoDB tables in both single and multi-region modes

## Verification

```bash
nix develop --command ./RUNME.sh extension_run account-data/222222222222 us-east-2
nix develop --command ./RUNME.sh extension_run account-data/222222222222 all 'CustomerA'
```
