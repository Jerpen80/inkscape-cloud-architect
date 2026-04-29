## 1. Data Parsing

- [x] 1.1 Add RDS parsing to `cloudia_parser.py` — resolve exact subnet via AZ + DBSubnetGroup
- [x] 1.2 Add ElastiCache parsing — resolve subnet via AZ heuristic against known subnets
- [x] 1.3 Update `parse_region` and `parse_all_regions` return signatures (5th element: `db_instances`)

## 2. Symbol Import

- [x] 2.1 Add `AWS-Resource-database-light.svg` to `SYMBOL_FILES`

## 3. Database Rendering Module

- [x] 3.1 Create `resource_db.py` with card rendering (icon + name + engine/class, type-specific symbols)
- [x] 3.2 Add database config section to `default-config.yaml` under `layout.database`

## 4. Integration

- [x] 4.1 Update `render_vpc_with_subnets` to accept `db_instances`, build subnet map, include in row height calculation
- [x] 4.2 Render database cards inside subnets after EC2 cards
- [x] 4.3 Create "Database" layer in z-order
- [x] 4.4 Update `aws-auto-diagram.py` to pass db_instances through

## 5. Verify

- [x] 5.1 Run headless with us-east-2 (account 222222222222) and verify RDS + ElastiCache render in correct subnets
