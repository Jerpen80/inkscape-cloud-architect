# Place resource types in separate Inkscape layers

**Bean:** `.beans/inkscape-cloud-architect-vjs9--place-vpcs-in-a-lower-layer-then-subnets.md`

## Summary

Each resource class gets its own Inkscape layer. VPCs render in a lower layer than subnets, matching the template convention and enabling per-resource-type editing in Inkscape (lock, hide, select).

## Motivation

- Currently all elements append to the root SVG — no layer separation
- Templates use layers: root, Availability Zones, VPC, top
- Users need to lock/hide resource types when editing diagrams
- Z-ordering matters: VPC rects must be behind subnet rects

## Scope

### In scope
- Create shared layer utility (`get_or_create_layer`) for creating/reusing named Inkscape layers
- Update `resource_vpc.py` to render VPC elements to a "VPCs" layer and subnet elements to a "Subnets" layer
- Layer creation order determines z-order: VPCs first (bottom), Subnets second (top)

### Out of scope
- AZ or Region layers (future resource types)
- Nesting layers (flat layer stack for now)

## Files

| Action | File |
|--------|------|
| Create | `extensions/aws-auto-diagram/ica_utils/layers.py` |
| Update | `extensions/aws-auto-diagram/ica_utils/resource_vpc.py` |
