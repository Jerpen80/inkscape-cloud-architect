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
The default config SHALL include a `document` section with a `margin` key, a `layout` section with `mode`, `spaced`, and `dense` sub-sections, and a `theme` section with light and dark color palettes.

#### Scenario: Document margin default
- **WHEN** the default config is loaded without user overrides
- **THEN** `config["document"]["margin"]` SHALL be `20`

#### Scenario: Layout section present
- **WHEN** the default config is loaded without user overrides
- **THEN** `config["layout"]` SHALL contain `mode` (default "spaced"), `spaced`, and `dense` sub-sections, each containing complete layout value sets

#### Scenario: Theme section present
- **WHEN** the default config is loaded without user overrides
- **THEN** `config["theme"]` SHALL contain `light` and `dark` subsections each with `background`, `text_color`, `text_dimmed_opacity`, and border color keys

#### Scenario: Legend config defaults
- **WHEN** the default config is loaded without user overrides
- **THEN** `config["layout"]["legend"]` SHALL contain `icon_scale`, `font_size`, `item_gap`, `row_gap`, `section_gap`, `top_spacing`, `swatch_width`, and `swatch_height` values

#### Scenario: Layout resolved before rendering
- **WHEN** the extension starts
- **THEN** the selected layout mode's values SHALL be merged into `config["layout"]` top-level keys before any rendering occurs

#### Scenario: Default VPC with resources is shown
- **WHEN** a region contains only default VPCs but those VPCs have running resources (EC2, RDS, LBs, EKS, Lambda, NAT gateways, or ASGs)
- **THEN** the region SHALL be included in the rendered output

#### Scenario: Empty default VPC is skipped
- **WHEN** a region contains only default VPCs with no running resources
- **THEN** the region SHALL be excluded from the rendered output
