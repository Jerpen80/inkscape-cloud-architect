# Layout engine with canonical AWS diagram style

**Bean:** `.beans/inkscape-cloud-architect-ialj--make-rectance-per-vpc-and-rectangles-per-subnet.md`

## Summary

Create a reusable layout module and update the VPC/subnet renderer to produce canonical AWS-style diagrams where subnets are placed in a grid (columns = AZs, rows = public/private) inside auto-sized VPC rectangles that stack vertically.

## Motivation

- Current renderer places everything at hardcoded fixed positions — multiple VPCs and subnets overlap
- Subnets should be inside their parent VPC rectangle
- The canonical AWS diagram style uses AZ columns and public/private rows
- A reusable layout module is needed for future resource types (EC2, ELB, RDS, etc.)

## Scope

### In scope
- Create `ica_utils/layout.py` — generic grid layout, auto-sizing containers, vertical stacking
- Update `ica_utils/resource_vpc.py` — use layout module, AZ columns, public/private rows, auto-sized VPC rects
- Update `aws-auto-diagram.py` — pass organized data to renderer

### Out of scope
- Rendering resource types beyond VPCs and subnets
- Dark mode / style variants
- User-configurable layout parameters (spacing, sizes)

## Files

| Action | File |
|--------|------|
| Create | `extensions/aws-auto-diagram/ica_utils/layout.py` |
| Update | `extensions/aws-auto-diagram/ica_utils/resource_vpc.py` |
| Update | `extensions/aws-auto-diagram/aws-auto-diagram.py` |
