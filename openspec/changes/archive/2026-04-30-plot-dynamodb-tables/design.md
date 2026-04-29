## Context

The extension already renders regional non-VPC resources — the Global region handles S3 buckets and Lambda functions. DynamoDB is different: it's **regional**, not global. Tables exist per-region and should render inside their respective region rects.

The `dynamodb-list-tables.json` file contains only table names — no VPC, subnet, or detailed metadata.

## Goals / Non-Goals

**Goals:**
- Render DynamoDB tables as icon+name cards inside region rects, below VPCs
- Support both single-region and multi-region modes

**Non-Goals:**
- DynamoDB Global Tables (cross-region replication)
- Table details (capacity, indexes, etc.)

## Decisions

### 1. Regional non-VPC resource pattern

This is the first **regional** non-VPC resource. It introduces a new rendering pattern: after VPCs are rendered in a region's Stack, DynamoDB tables render below them, still inside the region rect.

In multi-region mode, the flow becomes:
```
For each region:
  1. Render VPCs into Stack
  2. Render DynamoDB tables below Stack → get (ddb_w, ddb_h)
  3. Region height = VPC content height + gap + DynamoDB height
  4. Region width = max(VPC width, DynamoDB width)
```

In single-region mode:
```
  1. Render VPCs into Stack
  2. Render DynamoDB tables below Stack
  3. Account rect wraps everything (if present)
```

### 2. Card pattern matching S3

`resource_dynamodb.py` uses the same horizontal icon+name card layout as `resource_s3.py`: icon left, name right. This is appropriate for simple name-only resources.

Symbol: `AWS-Resource-database-light.svg:res-amazon-dynamodb-table` (already imported).

### 3. Parser returns DynamoDB tables as separate list

`parse_region()` gains a `dynamodb_tables` list. In `parse_all_regions()`, it's threaded through the region tuple. The tuple grows to include dynamodb_tables.

### 4. DynamoDB layer

New "DynamoDB" layer, separate from "Database" (RDS/ElastiCache inside VPCs). Placed after "S3" in z-order.

## Risks / Trade-offs

- [Growing tuple] → The `parse_region()` return tuple keeps growing. Acceptable for now, but a future refactor to a dict/dataclass may be warranted.
- [Gap between VPCs and DynamoDB] → Need a visual gap between the VPC stack and DynamoDB cards. Use the VPC gap value for consistency.
