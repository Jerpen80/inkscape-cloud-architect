---
# inkscape-cloud-architect-v060
title: Reimplement ElastiCache subnet placement after cloudia collects cache-subnet-groups
status: draft
type: task
created_at: 2026-04-30T15:13:40Z
updated_at: 2026-04-30T15:13:40Z
parent: inkscape-cloud-architect-v7i1
---

Currently ElastiCache placement uses an AZ-matching heuristic (first non-public subnet in the AZ) because cloudia-reader-aws does not collect elasticache-describe-cache-subnet-groups. Once cloudia adds this data, reimplement to use exact subnet IDs from the subnet group, matching the RDS approach.
