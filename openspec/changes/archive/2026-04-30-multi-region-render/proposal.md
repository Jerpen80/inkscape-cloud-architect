## Why

The extension currently renders a single region at a time. Users with resources across multiple regions must run the extension repeatedly and manually compose the results. Adding multi-region rendering lets the diagram show the full account topology in one pass.

Bean: [inkscape-cloud-architect-0xj5](.beans/inkscape-cloud-architect-0xj5--multi-region-render.md)

## What Changes

- Add "All regions (with resources)" as the first option in the INX region dropdown
- When "all regions" is selected, scan all region subdirectories in the account data folder
- Skip regions that only contain default VPCs (filter on AWS `IsDefault` field)
- Render non-empty regions side by side (horizontally) inside the account container
- Each region gets its own rectangle with label and `region.svg` icon on a dedicated "Regions" layer
- VPCs stack vertically within each region, as they do today
- When a specific region is selected, behave exactly as today (no region rect, no horizontal layout)
- Add a `Row` layout primitive (horizontal counterpart to `Stack`) in `layout.py`
- Add region padding/gap to the config system

## Capabilities

### New Capabilities
- `multi-region`: Scanning, filtering, and rendering multiple regions horizontally with region boundary rectangles
- `region-rendering`: Region rectangle rendering with icon, label, and configurable padding

### Modified Capabilities
- `config-loading`: Default config gains `layout.region` section with padding and gap values
- `layout-config`: New `layout.region` values added to config structure

## Impact

- **INX**: New "all" option in region dropdown
- **Parser**: `cloudia_parser.py` gains `is_default` on VPCs and a multi-region scan function
- **Layout**: New `Row` class in `layout.py`
- **Rendering**: New `resource_region.py` module; `aws-auto-diagram.py` gains multi-region orchestration loop
- **Config**: `default-config.yaml` gains `layout.region` section
- **Layers**: New "Regions" layer between Accounts and VPCs in z-order

## Verification

```bash
# Single region (unchanged behavior)
nix develop --command ./RUNME.sh extension_run account-data/222222222222 eu-west-1

# Multi-region
nix develop --command ./RUNME.sh extension_run account-data/222222222222 all 'My Account'
```
