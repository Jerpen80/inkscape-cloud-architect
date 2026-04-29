## 1. Configuration

- [x] 1.1 Restructure `default-config.yaml`: move current `layout.*` values into `layout.dense.*`, create `layout.spaced.*` with template-scale values, add `layout.mode: spaced`
- [x] 1.2 Ensure all layout sub-sections are present in both presets (account, vpc, subnet, ec2, database, eks, lambda_function, load_balancer, asg, nat_gateway, s3, dynamodb, edge, route53, cloudfront, region, availability_zone, internet_gateway)

## 2. Layout Mode Resolution

- [x] 2.1 Add layout mode resolution function: read `config["layout"]["mode"]`, copy selected preset into `config["layout"]` top-level, remove mode/spaced/dense keys
- [x] 2.2 Add `--layout_mode` parameter to INX file (combo: Spaced/Dense)
- [x] 2.3 Add `--layout_mode` argument to `aws-auto-diagram.py` `add_arguments()`
- [x] 2.4 Call layout mode resolution in `effect()` after config load, before theme resolution; INX parameter overrides config default

## 3. Headless Runner

- [x] 3.1 Update `RUNME.d/35-extension-run.sh` to accept optional `--layout_mode` argument and pass to extension

## 4. Column Width Fix

- [x] 4.1 Fix column width calculation to account for EC2 card widths (icon + name/type at configured font_size and icon_scale) and DB card widths — prevents content overflow in spaced mode

## 5. Testing

- [x] 5.1 Run headless test with spaced mode (default) — verify diagram renders with larger spacing
- [x] 5.2 Run headless test with dense mode — verify diagram renders with compact spacing (no regression)
- [x] 5.3 Compare output dimensions between spaced and dense to confirm meaningful difference (spaced: 2643x5446, dense: 1843x3084)
