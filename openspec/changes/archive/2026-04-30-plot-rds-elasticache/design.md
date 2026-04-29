## Context

EC2 instances are already rendered inside subnets with dynamic height. RDS and ElastiCache follow the same card pattern but require subnet resolution from subnet groups.

## Goals / Non-Goals

**Goals:**
- Parse and render RDS instances with exact subnet placement
- Parse and render ElastiCache clusters with AZ-based heuristic placement
- Reuse the EC2 card rendering pattern (icon + name + detail, no border)

**Non-Goals:**
- ElastiCache exact subnet placement (blocked on cloudia collecting cache-subnet-groups — tracked in bean `v060`)
- Aurora cluster grouping (render individual instances)
- Replication group visualization

## Decisions

### 1. Unified `db_instances` list

Both RDS and ElastiCache are returned as a single `db_instances` list from the parser, each with a `db_type` field (`rds` or `elasticache`). This simplifies the rendering pipeline — one list to filter per VPC/subnet.

### 2. RDS subnet resolution: exact

RDS `DBSubnetGroup.Subnets[]` contains `SubnetIdentifier` and `SubnetAvailabilityZone.Name`. Cross-reference with the instance's `AvailabilityZone` to find the exact subnet.

### 3. ElastiCache subnet resolution: AZ heuristic

ElastiCache has `PreferredAvailabilityZone` but no subnet IDs. Resolution: find the first non-public subnet in the matching AZ within the same VPC. Since ElastiCache doesn't expose `VpcId` directly, derive it by matching the AZ against known subnets from ec2-describe-subnets. If multiple non-public subnets match, pick the first one.

### 4. ElastiCache VPC resolution

ElastiCache clusters don't have a `VpcId` field. To assign a VPC: look at all subnets we know, find non-public subnets in the cluster's `PreferredAvailabilityZone`, and use that subnet's `VpcId`. If no match, skip the cluster.

### 5. Type-specific symbols

From `AWS-Resource-database-light.svg`:
- RDS: `res-amazon-aurora-amazon-rds-instance`
- ElastiCache Redis: `res-amazon-elasticache-elasticache-for-redis`
- ElastiCache Memcached: `res-amazon-elasticache-elasticache-for-memcached`

### 6. Card detail line

- RDS: `{engine} / {db_instance_class}` (e.g., "postgres / db.t3.xlarge")
- ElastiCache: `{engine} / {cache_node_type}` (e.g., "redis / cache.t3.small")

### 7. Rendering reuses resource_ec2 card pattern

`resource_db.py` follows `resource_ec2.py` exactly: `card_height()`, `cards_height()`, `render_instance()`, `render_instances_in_subnet()`. The row height computation in `resource_vpc.py` sums EC2 + DB instance counts per subnet.

## Risks / Trade-offs

- [ElastiCache heuristic may misplace] → If a VPC has multiple non-public subnets in the same AZ, the cluster may be shown in the wrong one. Acceptable until cloudia improves. Tracked in bean `v060`.
- [ElastiCache VPC resolution] → Could fail if the AZ doesn't match any known subnet. Gracefully skip.
