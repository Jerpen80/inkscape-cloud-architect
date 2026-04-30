## Context

The multi-region parser skipped regions where all VPCs had `IsDefault: true`. This missed accounts where real workloads run in default VPCs.

## Goals / Non-Goals

**Goals:**
- Show default VPCs that contain resources
- Continue hiding empty default VPCs

**Non-Goals:**
- Making this configurable (simple behavioral fix)

## Decisions

### 1. Check for resources before skipping

When all VPCs in a region are default, check if any resources exist (instances, LBs, DB instances, EKS, Lambda, NAT gateways, ASGs). Only skip if no resources are found.

## Risks / Trade-offs

- [More regions shown] → Accounts with many default VPCs that have a single stray resource will now render. Acceptable — the resource is there for a reason.
