## Why

The extension has hardcoded values (layout constants, margins, sizing) scattered across modules. As more features are added (resize-to-fit, resource rendering, multi-region), these values need to be configurable without modifying code. A configuration system provides sensible defaults while allowing users to customize behavior.

Related task: [inkscape-cloud-architect-03vi](.beans/inkscape-cloud-architect-03vi--create-configuration-yaml-file.md)

## What Changes

- Add a `default-config.yaml` file shipped with the extension containing all default configuration values
- Add a config loader module that reads the default config and optionally merges user overrides from `~/.config/inkscape/extensions/aws-auto-diagram/config.yaml`
- Load merged config at extension startup and make it available to all modules

## Capabilities

### New Capabilities
- `config-loading`: Loading, merging, and accessing YAML configuration with a default config file and user override support

### Modified Capabilities
<!-- None - this is a new foundation that other features will build on -->

## Impact

- New file: `extensions/aws-auto-diagram/default-config.yaml`
- New module: `extensions/aws-auto-diagram/ica_utils/config.py`
- Modified: `extensions/aws-auto-diagram/aws-auto-diagram.py` (load config at startup)
- New dependency: PyYAML (likely already available via Inkscape's Python environment)
