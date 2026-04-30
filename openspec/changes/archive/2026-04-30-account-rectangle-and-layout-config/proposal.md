## Why

The extension renders VPCs and subnets but has no visual grouping at the AWS account level. Users need to see which account resources belong to, especially when diagrams grow. Additionally, all layout spacing values are hardcoded constants in `resource_vpc.py`, making it impossible for users to customize padding, gaps, and sizing without editing source code.

Bean: [inkscape-cloud-architect-95py](.beans/inkscape-cloud-architect-95py--render-an-account-rectangle-around-all-resources-i.md)

## What Changes

- Add an optional "account name" argument to the extension INX interface
- Render an account rectangle (black stroke, `cloud.svg` icon) around all resources in a region on a dedicated "Accounts" layer
- The Accounts layer sits below VPCs in z-order (Accounts → VPCs → Subnets)
- Move all hardcoded layout spacing constants into `default-config.yaml` under a `layout` section, organized by resource type (account, vpc, subnet)
- Users can override any spacing value via the existing config override mechanism

## Capabilities

### New Capabilities
- `account-rendering`: Rendering an AWS account boundary rectangle around all resources in a region, with optional account name label
- `layout-config`: Configurable layout spacing (padding, gaps, sizing) for all resource types via YAML config

### Modified Capabilities
- `config-loading`: The default config gains a `layout` section with account, vpc, and subnet spacing values

## Impact

- **Config**: `default-config.yaml` expands with `layout.account`, `layout.vpc`, `layout.subnet` sections
- **INX**: New optional `account_name` parameter in `aws-auto-diagram.inx`
- **Code**: `resource_vpc.py` stops using hardcoded constants, reads from config instead; new `resource_account.py` module; `aws-auto-diagram.py` gains account layer creation and rendering logic
- **Layers**: New "Accounts" layer in generated SVG output
