## Why

All colors are hardcoded throughout the rendering modules — text is implicitly black, borders use hardcoded hex values. There is no way to generate a diagram for a dark background. AWS architecture diagrams are commonly presented on dark slides and dashboards, making dark mode a practical need.

Bean: [inkscape-cloud-architect-u76x](.beans/inkscape-cloud-architect-u76x--darkmode.md)

## What Changes

- Add a `--theme` dropdown parameter to the INX dialog (Light / Dark)
- Add a `theme` section to config with light and dark color palettes (text color, dimmed opacity, background, structural border colors)
- At runtime, resolve the selected theme into a color palette and pass it through all rendering modules
- Update every rendering module to read text color and structural colors from the resolved theme instead of hardcoded values
- Add an optional background rect for dark mode
- No symbol changes needed — AWS icons use colored fills on white/transparent backgrounds that work on both light and dark

## Capabilities

### New Capabilities
- `theme`: Theme selection (light/dark) via INX parameter and config-driven color palettes

### Modified Capabilities
- `visual-style`: All rendering modules read colors from theme palette instead of hardcoded values
- `config-loading`: Config gains `theme` section with light/dark palettes
- `account-rendering`: Account rect border color comes from theme
- `ec2-rendering`: Text color comes from theme
- `load-balancer-rendering`: Text color comes from theme
- `eks-rendering`: Text color comes from theme

## Impact

- **INX**: `aws-auto-diagram.inx` gains `--theme` combo parameter
- **Config**: `default-config.yaml` gains `theme` section with light/dark palettes
- **Main**: `aws-auto-diagram.py` resolves theme and passes palette to renderers
- **All renderers**: `resource_vpc.py`, `resource_ec2.py`, `resource_lb.py`, `resource_eks.py`, `resource_db.py`, `resource_s3.py`, `resource_lambda.py`, `resource_nat.py`, `resource_route53.py`, `resource_cloudfront.py`, `resource_edge.py`, `resource_az.py`, `resource_account.py`, `resource_region.py`, `resource_asg.py` — all updated to use theme colors for text and structural elements
- **Headless runner**: `RUNME.d/35-extension-run.sh` gains optional `--theme` argument
