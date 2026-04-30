---
# inkscape-cloud-architect-ecs1
title: Plot ECS clusters and tasks
status: draft
type: task
created_at: 2026-04-30T16:00:00Z
updated_at: 2026-04-30T16:00:00Z
parent: inkscape-cloud-architect-v7i1
blocked_by:
    - inkscape-cloud-architect-5gm4
---

Render ECS clusters and tasks. Most complex of the three compute services: Fargate tasks have ENIs in specific subnets (like EC2), EC2 launch type tasks run on existing EC2 instances, and clusters span VPCs. Needs design for Fargate vs EC2 distinction and cluster grouping. Cloudia provides ecs-list-clusters.json, ecs-list-tasks, and ecs-describe-tasks. Split from inkscape-cloud-architect-g07e.
