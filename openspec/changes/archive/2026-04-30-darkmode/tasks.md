## 1. Theme Infrastructure

- [x] 1.1 Create `ica_utils/theme.py` with `resolve_theme(theme_name, config)`, `get_text_color(config)`, `get_text_dimmed_opacity(config)`, `get_border_color(config, element)`, `get_background(config)`
- [x] 1.2 Add `theme` section to `default-config.yaml` with light and dark palettes
- [x] 1.3 Add `--theme` parameter to INX file (combo: Light/Dark)
- [x] 1.4 Add `--theme` argument to `aws-auto-diagram.py` `add_arguments()`
- [x] 1.5 Resolve theme in `effect()` and inject palette into config as `config["_theme"]`

## 2. Update Rendering Modules — Text Colors

- [x] 2.1 Update `resource_vpc.py` `aws_rect()` text style: add explicit `fill` from theme
- [x] 2.2 Update `resource_ec2.py`: name and type text get explicit `fill` from theme
- [x] 2.3 Update `resource_lb.py`: name and type text get explicit `fill` from theme
- [x] 2.4 Update `resource_eks.py`: name and version text get explicit `fill` from theme
- [x] 2.5 Update `resource_db.py`: name and engine text get explicit `fill` from theme
- [x] 2.6 Update `resource_s3.py`: bucket name text gets explicit `fill` from theme
- [x] 2.7 Update `resource_lambda.py`: function name and runtime text get explicit `fill` from theme
- [x] 2.8 Update `resource_nat.py`: NAT gateway name text gets explicit `fill` from theme
- [x] 2.9 Update `resource_route53.py`: zone name text gets explicit `fill` from theme
- [x] 2.10 Update `resource_cloudfront.py`: distribution name and ID text get explicit `fill` from theme
- [x] 2.11 Update `resource_edge.py`: "Edge" label text gets explicit `fill` from theme
- [x] 2.12 Update `resource_az.py`: AZ label text gets explicit `fill` from theme
- [x] 2.13 Update `resource_region.py`: region label text gets explicit `fill` from theme (via aws_rect)
- [x] 2.14 Update `resource_account.py`: account label text gets explicit `fill` from theme (via aws_rect)
- [x] 2.15 Update `resource_asg.py`: ASG label text gets explicit `fill` from theme

## 3. Update Rendering Modules — Border Colors

- [x] 3.1 Update `resource_vpc.py`: VPC, public subnet, private subnet border colors from theme
- [x] 3.2 Update `resource_account.py`: account border color from theme
- [x] 3.3 Update `resource_edge.py`: edge zone border color from theme
- [x] 3.4 Update `resource_region.py`: region border color from theme
- [x] 3.5 Update `resource_az.py`: AZ stroke color from theme (already config-driven)

## 4. Background

- [x] 4.1 Add background rect rendering in `resize_to_fit()` when theme background is not "none"

## 5. Headless Runner

- [x] 5.1 Update `RUNME.d/35-extension-run.sh` to accept optional `--theme` argument and pass to extension

## 6. Testing

- [x] 6.1 Run headless test with light theme (default) — verify no visual regression
- [x] 6.2 Run headless test with dark theme — verify text is light, background is dark, borders are visible
