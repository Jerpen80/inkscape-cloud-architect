# Plot availability zones

**Bean:** `.beans/inkscape-cloud-architect-2gbi--plot-availability-zones.md`

## Summary

Render availability zone columns as dashed rectangles with labels inside each VPC, on a dedicated "Availability Zones" layer. AZ rendering is optional via config. All AZ-specific padding and styling is config-driven.

## Motivation

- The canonical AWS style guide shows AZs as dashed vertical columns inside VPCs
- Templates use this pattern (dashed blue rects with "Availability Zone N" labels)
- AZs provide essential spatial context — subnets grouped by AZ column
- Must be optional since not all diagrams need AZ visualization

## Scope

### In scope
- Add AZ config section to `default-config.yaml` (enabled, label, padding, stroke style)
- Create `ica_utils/resource_az.py` — renders AZ rects and labels
- Add "Availability Zones" layer between VPCs and Subnets
- AZ rects span full content height of their VPC, wrap the subnet column with padding
- Adjust Grid col_gap to accommodate AZ side padding
- Update `render_vpc_with_subnets` to call AZ renderer

### Out of scope
- AZ toggle in .inx dialog (config-only for now)
- AZ rendering outside of VPC context

## Files

| Action | File |
|--------|------|
| Update | `extensions/aws-auto-diagram/default-config.yaml` |
| Create | `extensions/aws-auto-diagram/ica_utils/resource_az.py` |
| Update | `extensions/aws-auto-diagram/ica_utils/resource_vpc.py` |
| Update | `extensions/aws-auto-diagram/aws-auto-diagram.py` |
