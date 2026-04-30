## 1. Config Expansion

- [x] 1.1 Expand `default-config.yaml` with `layout.account`, `layout.vpc`, and `layout.subnet` sections containing all spacing defaults
- [x] 1.2 Update `resource_vpc.py` to accept a `config` dict and read spacing values from `layout.vpc.*` and `layout.subnet.*` instead of hardcoded constants
- [x] 1.3 Update `aws-auto-diagram.py` to pass config to `render_vpc_with_subnets`

## 2. Account Rendering

- [x] 2.1 Add optional `account_name` parameter to `aws-auto-diagram.inx`
- [x] 2.2 Add `account_name` to `add_arguments` in `aws-auto-diagram.py`
- [x] 2.3 Create `resource_account.py` with a function to render the account rectangle (black stroke, `cloud.svg` icon)
- [x] 2.4 Update `effect()` to create layers in order: Accounts → VPCs → Subnets
- [x] 2.5 Update `effect()` to offset Stack origin by account padding when `account_name` is set
- [x] 2.6 Update `effect()` to render account rect around all VPCs after they are drawn (bounding-box approach)

## 3. Verification

- [x] 3.1 Run headless extension test to verify output renders correctly
