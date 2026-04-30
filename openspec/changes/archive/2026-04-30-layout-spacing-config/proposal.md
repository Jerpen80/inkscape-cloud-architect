## Why

VPC padding and subnet spacing values are hardcoded as module-level constants in `resource_vpc.py`. Users cannot customize the diagram layout without editing Python code. Now that the configuration system exists (`configuration-yaml` change), these values should be moved into `default-config.yaml` so users can override them.

Related task: [inkscape-cloud-architect-wdva](.beans/inkscape-cloud-architect-wdva--padding-inside-vpcs-and-margins-between-subnet-in.md)

## What Changes

- Add VPC padding and gap settings to `default-config.yaml` under `vpc.*`
- Add subnet spacing settings to `default-config.yaml` under `subnet.*`
- Replace hardcoded constants in `resource_vpc.py` with config lookups via `inkdoc.config`
- Replace `resource_vpc.VPC_GAP` usage in `aws-auto-diagram.py` with config lookup

## Capabilities

### New Capabilities
- `layout-spacing`: Configurable VPC padding, VPC gap, and subnet spacing values read from the YAML config system

### Modified Capabilities
- `config-loading`: The default config gains new `vpc` and `subnet` sections

## Impact

- Modified: `extensions/aws-auto-diagram/default-config.yaml` (new sections)
- Modified: `extensions/aws-auto-diagram/ica_utils/resource_vpc.py` (read from config instead of constants)
- Modified: `extensions/aws-auto-diagram/aws-auto-diagram.py` (read `vpc.gap` from config)
