# Fix resource labels: sizing, positioning, and container auto-fit

**Bean:** `.beans/inkscape-cloud-architect-aupd--resource-labels-may-not-overlap.md`

## Summary

Standardize label font size to 13pt, position labels inside their container rectangles, auto-size containers to fit labels using a Pillow-based font metrics system with caching. Extend the Grid layout to support variable column widths driven by label measurements.

## Motivation

- Labels currently use 18pt which is too large for 160px subnet cells
- Labels overflow their containers and overlap each other
- Container sizes are fixed and don't adapt to label content
- Long names like `subnet-EXAMPLE0000000002 (172.31.16.0/20)` need wider containers

## Scope

### In scope
- Create `ica_utils/text_utils.py` — font metrics generation via Pillow, caching, text width estimation
- Update `ica_utils/layout.py` — Grid supports variable column widths
- Update `ica_utils/resource_vpc.py` — font size 13pt, labels inside containers, column widths driven by label measurements
- Add `pillow` to flake.nix devShell (already available but ensure explicit)

### Out of scope
- Text wrapping or truncation
- User-configurable font size or font family
- Dark mode text colors

## Files

| Action | File |
|--------|------|
| Create | `extensions/aws-auto-diagram/ica_utils/text_utils.py` |
| Update | `extensions/aws-auto-diagram/ica_utils/layout.py` |
| Update | `extensions/aws-auto-diagram/ica_utils/resource_vpc.py` |
| Update | `/flake.nix` (if pillow not already explicit) |
