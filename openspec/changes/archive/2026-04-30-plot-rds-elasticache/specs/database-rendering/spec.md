## ADDED Requirements

### Requirement: Parse RDS instances
The parser SHALL extract RDS instances from `rds-describe-db-instances.json`.

#### Scenario: RDS instance parsed with exact subnet
- **WHEN** `parse_region` is called and an RDS instance exists with `AvailabilityZone` and `DBSubnetGroup.Subnets`
- **THEN** the instance SHALL be returned with `name`, `engine`, `instance_class`, `subnet_id` (resolved from AZ + subnet group), and `vpc_id`

#### Scenario: RDS subnet resolution
- **WHEN** an RDS instance is in `us-east-2a` and its subnet group contains subnets in `us-east-2a` and `us-east-2b`
- **THEN** the `subnet_id` SHALL be the subnet whose AZ matches `us-east-2a`

### Requirement: Parse ElastiCache clusters
The parser SHALL extract ElastiCache clusters from `elasticache-describe-cache-clusters.json`.

#### Scenario: ElastiCache parsed with heuristic subnet
- **WHEN** an ElastiCache cluster has `PreferredAvailabilityZone`
- **THEN** it SHALL be placed in the first non-public subnet matching that AZ

#### Scenario: ElastiCache VPC resolution
- **WHEN** an ElastiCache cluster's AZ matches a known subnet
- **THEN** its `vpc_id` SHALL be derived from that subnet's VPC

#### Scenario: Unresolvable ElastiCache cluster
- **WHEN** an ElastiCache cluster's AZ doesn't match any known non-public subnet
- **THEN** the cluster SHALL be skipped

### Requirement: Render database resources inside subnets
RDS and ElastiCache resources SHALL be rendered inside their subnet boxes as borderless cards with icon, name, and engine/class.

#### Scenario: Database card layout
- **WHEN** a database resource is rendered
- **THEN** it SHALL display the type-specific icon (centered), name (centered), and engine/class detail (centered)
- **THEN** there SHALL be no visible border around the card

#### Scenario: Multiple database resources in one subnet
- **WHEN** a subnet contains multiple database resources
- **THEN** they SHALL be stacked vertically with configurable spacing

### Requirement: Dynamic subnet height includes database resources
Subnet height SHALL account for both EC2 instances and database resources.

#### Scenario: Subnet with EC2 and database resources
- **WHEN** a subnet contains 2 EC2 instances and 1 RDS instance
- **THEN** the subnet height SHALL accommodate all 3 resource cards

### Requirement: Type-specific symbols
The correct icon SHALL be used based on database resource type.

#### Scenario: RDS symbol
- **WHEN** a database resource has `db_type` "rds"
- **THEN** the RDS instance icon SHALL be used

#### Scenario: ElastiCache Redis symbol
- **WHEN** a database resource has `db_type` "elasticache" and engine "redis"
- **THEN** the ElastiCache for Redis icon SHALL be used

#### Scenario: ElastiCache Memcached symbol
- **WHEN** a database resource has `db_type` "elasticache" and engine "memcached"
- **THEN** the ElastiCache for Memcached icon SHALL be used

### Requirement: Database resources on dedicated layer
Database resource elements SHALL be rendered on a dedicated "Database" layer.

#### Scenario: Layer creation
- **WHEN** database resources are rendered
- **THEN** all database icons, names, and details SHALL be placed on a layer named "Database"

### Requirement: Database layout configuration
Database rendering parameters SHALL be configurable via `layout.database` in the config.

#### Scenario: Default database config
- **WHEN** no user config override exists
- **THEN** `layout.database` SHALL contain `icon_scale`, `font_size`, `card_gap`, and `card_top` with sensible defaults
