## Why

Generated diagrams are too dense compared to the hand-crafted AWS templates. Measuring the reference template (`AWS multi-AZ Web Appication.svg`) shows spacing 3-10x larger than our current defaults. The bean says "space is not our problem" — diagrams should breathe. But dense mode is still useful for compact overviews of large accounts.

Bean: [inkscape-cloud-architect-xie4](.beans/inkscape-cloud-architect-xie4--more-padding-to-align-more-with-the-template.md)

## What Changes

- Add a `--layout_mode` INX dropdown parameter (Spaced / Dense), defaulting to Spaced
- Restructure config: `layout.spaced.*` and `layout.dense.*` contain complete sets of layout values
- At startup, resolve the selected mode and merge its values into `config["layout"]` so all renderers work unchanged
- "Spaced" values derived from the reference template measurements, with full-size icons (`icon_scale: 1.0`) and standard text (`font_size: 17`) for all resource cards
- "Dense" values are the current defaults (half-size icons at `0.5`, smaller text at `13`)
- No renderer code changes — they already read from `config["layout"]`

## Capabilities

### New Capabilities
- `layout-density`: Layout mode selection (spaced/dense) via INX parameter with config-driven presets

### Modified Capabilities
- `config-loading`: Config restructured with `layout.spaced` and `layout.dense` sub-sections; mode resolution at startup
- `layout-config`: All layout spacing values now come from the resolved density mode

## Impact

- **INX**: `aws-auto-diagram.inx` gains `--layout_mode` combo parameter
- **Config**: `default-config.yaml` restructured with `layout.mode`, `layout.spaced.*`, `layout.dense.*`
- **Main**: `aws-auto-diagram.py` resolves layout mode at startup, merges selected preset into `config["layout"]`
- **Config loader**: `config.py` needs to handle the mode resolution during deep merge
- **Renderers**: No changes — they already read from `config["layout"]`
- **Headless runner**: `RUNME.d/35-extension-run.sh` gains optional `--layout_mode` argument
