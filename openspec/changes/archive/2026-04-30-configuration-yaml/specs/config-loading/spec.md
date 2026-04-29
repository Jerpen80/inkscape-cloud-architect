## ADDED Requirements

### Requirement: Default config file exists
The extension SHALL ship with a `default-config.yaml` file containing all default configuration values.

#### Scenario: Default config is present
- **WHEN** the extension is installed
- **THEN** `extensions/aws-auto-diagram/default-config.yaml` SHALL exist with valid YAML content

### Requirement: Load default config
The config module SHALL load and parse `default-config.yaml` from the extension directory.

#### Scenario: Loading defaults
- **WHEN** `load_config()` is called with the extension directory path
- **THEN** it SHALL return a dict containing all default values from `default-config.yaml`

### Requirement: User override via mutable location
The config module SHALL check for a user override file at `~/.config/inkscape/extensions/aws-auto-diagram/config.yaml`.

#### Scenario: No user override exists
- **WHEN** `load_config()` is called and no override file exists at the mutable location
- **THEN** it SHALL return the default config unchanged

#### Scenario: User override exists
- **WHEN** `load_config()` is called and an override file exists at the mutable location
- **THEN** it SHALL deep-merge user values over defaults, with user values taking precedence

### Requirement: Deep merge preserves unspecified defaults
The merge strategy SHALL be recursive so that users only need to specify the values they want to change.

#### Scenario: Partial override
- **WHEN** the default config has `document.margin: 20` and `document.other: 10`
- **THEN** a user override containing only `document.margin: 40` SHALL result in `document.margin: 40` and `document.other: 10`

### Requirement: Config loaded at extension startup
The extension SHALL load config once during `effect()` and make it available to rendering modules.

#### Scenario: Config available during rendering
- **WHEN** the extension's `effect()` method runs
- **THEN** config SHALL be loaded before any rendering occurs and passed to consumer functions

### Requirement: Initial config structure
The default config SHALL include a `document` section with a `margin` key.

#### Scenario: Document margin default
- **WHEN** the default config is loaded without user overrides
- **THEN** `config["document"]["margin"]` SHALL be `20`
