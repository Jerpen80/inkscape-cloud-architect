## Why

RDS and ElastiCache are common database/caching resources that live inside VPC subnets. Rendering them completes the "data tier" visualization alongside the existing compute (EC2) and networking (ALB/NLB) layers.

Related task: [inkscape-cloud-architect-5gm4](.beans/inkscape-cloud-architect-5gm4--plot-rds-and-elasticache-inside-subnets.md)

## What Changes

- Parse `rds-describe-db-instances.json` and `elasticache-describe-cache-clusters.json` in `cloudia_parser.py`
- RDS: resolve exact subnet via AZ + inline DBSubnetGroup subnet IDs
- ElastiCache: resolve subnet via AZ heuristic (first non-public subnet in matching AZ) since cloudia doesn't collect cache subnet group details
- Render database resources inside subnet boxes using the EC2 card pattern (icon + name + engine/class, no border)
- Type-specific symbols from `AWS-Resource-database-light.svg`
- New "Database" layer
- Database layout config under `layout.database`

## Capabilities

### New Capabilities
- `database-rendering`: Parsing and rendering RDS instances and ElastiCache clusters inside subnet boxes

### Modified Capabilities
<!-- None -->

## Impact

- Modified: `extensions/aws-auto-diagram/ica_utils/cloudia_parser.py` (parse RDS + ElastiCache)
- Modified: `extensions/aws-auto-diagram/ica_utils/resource_vpc.py` (pass db_instances, render in subnets)
- Modified: `extensions/aws-auto-diagram/aws-auto-diagram.py` (symbol import, layer, passthrough)
- Modified: `extensions/aws-auto-diagram/default-config.yaml` (database config)
- New: `extensions/aws-auto-diagram/ica_utils/resource_db.py` (database card rendering)
