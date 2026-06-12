# config-loading Specification

## Purpose

Defines how the extension loads its configuration: shipping a `default-config.yaml`,
merging an optional user override, resolving layout presets, and (via the config
schema) describing, validating, and discovering the full configuration surface.
## Requirements
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

### Requirement: Config schema descriptor exists
The config module SHALL provide a machine-readable schema describing every configuration
key. The schema SHALL carry, per key, metadata only — type, optional range or enum, optional
unit, and a human-readable help string — and SHALL NOT carry default values.

#### Scenario: Schema describes a key
- **WHEN** the schema is consulted for `layout.ec2.icon_scale`
- **THEN** it SHALL report a numeric type, a valid range, a unit, and a one-line help string
- **AND** it SHALL NOT itself define the key's default value

#### Scenario: Schema key paths use engine (flattened) form
- **WHEN** the schema lists layout keys
- **THEN** keys SHALL be addressed in the engine-resolved form (e.g. `layout.ec2.icon_scale`)
- **AND** SHALL NOT use the raw preset form (e.g. `layout.spaced.ec2.icon_scale`)

### Requirement: Schema loader sources defaults from default-config.yaml
The schema loader SHALL produce, for each key, a resolved view combining the schema metadata
with the default value read from the unchanged `default-config.yaml`. The loader SHALL NOT
modify `default-config.yaml` or engine behavior.

#### Scenario: Default value comes from YAML
- **WHEN** the resolved schema is built for `document.margin`
- **THEN** the default value SHALL equal `config["document"]["margin"]` from `default-config.yaml`

#### Scenario: Key inventory discovered from YAML
- **WHEN** the schema loader runs
- **THEN** the key inventory SHALL be derived from the keys present in `default-config.yaml`
  (resolved to the flattened layout form), so that key existence cannot drift from the schema

### Requirement: Preset-varying keys are identified and expose both preset values
The loader SHALL mark each `layout` key according to whether its value differs between the
`spaced` and `dense` presets. The `preset_varying` flag SHALL be derived by comparing the
presets, not hand-authored.

#### Scenario: A density knob is preset-varying
- **WHEN** the resolved schema is built for `layout.ec2.icon_scale`
- **THEN** it SHALL be marked `preset_varying = true`
- **AND** it SHALL expose both the spaced default and the dense default

#### Scenario: A misfiled style key is not preset-varying
- **WHEN** the resolved schema is built for `layout.eks.span_line_color`
- **THEN** it SHALL be marked `preset_varying = false`
- **AND** it SHALL expose a single default value

### Requirement: Override validation
The config module SHALL provide a pure validation function that checks a user override dict
against the schema and returns clear, per-key error messages. Validation SHALL perform no I/O
and SHALL NOT depend on inkex.

#### Scenario: Unknown key
- **WHEN** an override contains a key path not present in the schema
- **THEN** validation SHALL return an error naming the unknown key path

#### Scenario: Out-of-range value
- **WHEN** an override sets a numeric key outside its schema range
- **THEN** validation SHALL return an error naming the key and the allowed bounds

#### Scenario: Wrong type
- **WHEN** an override sets a key to a value not coercible to the key's schema type
- **THEN** validation SHALL return an error naming the key and the expected type

#### Scenario: Invalid enum value
- **WHEN** an override sets an enum key (e.g. `layout.mode`) to a value not in its allowed set
- **THEN** validation SHALL return an error naming the key and the allowed values

#### Scenario: Valid partial override
- **WHEN** an override sets only a subset of valid keys with valid values
- **THEN** validation SHALL return no errors

### Requirement: Schema coverage self-check
The config module SHALL provide a coverage check comparing the schema's keys against the keys
present in `default-config.yaml`. The check SHALL be available to tests and SHALL NOT run
during rendering.

#### Scenario: Every config key is described
- **WHEN** the coverage check runs against `default-config.yaml`
- **THEN** every key in the default config (in flattened layout form) SHALL have a schema entry
- **AND** every schema entry SHALL correspond to a key present in the default config

### Requirement: Schema layer does not alter rendering
Adding the schema SHALL NOT change engine behavior or rendered output.

#### Scenario: SVG output unchanged
- **WHEN** the extension renders a diagram before and after this change with identical inputs
- **THEN** the produced SVG SHALL be byte-identical

### Requirement: Load an explicit override file
The config system SHALL support loading a config override from an arbitrary file
path (not only the fixed mutable location), deep-merged over the defaults.

#### Scenario: Explicit override file path
- **WHEN** an override is loaded from an explicit file path
- **THEN** its values SHALL be deep-merged over `default-config.yaml`, with the override winning

#### Scenario: Missing override file
- **WHEN** an explicit override file path does not exist
- **THEN** loading SHALL fail with a clear error rather than silently ignoring it

### Requirement: Apply inline dotted-key overrides
The config system SHALL support applying inline overrides expressed as
`<dotted.key>=<value>` pairs, where the key is an engine-form path
(e.g. `layout.ec2.icon_scale`).

#### Scenario: Single inline override
- **WHEN** an inline override `layout.ec2.icon_scale=0.8` is applied
- **THEN** the merged config SHALL set `layout.ec2.icon_scale` accordingly

#### Scenario: Inline overrides win over file and defaults
- **WHEN** the same key is set by defaults, an override file, and an inline override
- **THEN** the inline override value SHALL take precedence

### Requirement: Coerce inline string values to schema types
Inline override values arrive as strings and SHALL be coerced to the key's schema
type before merging and validation.

#### Scenario: Coercion by schema type
- **WHEN** an inline override targets a key whose schema type is numeric, boolean, or enum
- **THEN** the string value SHALL be coerced to that type (e.g. `"0.8"`→float, `"17"`→int, `"true"`→bool)

#### Scenario: Unknown key cannot be coerced
- **WHEN** an inline override names a key absent from the schema
- **THEN** it SHALL be reported as an unknown-key error rather than guessed

### Requirement: Validate the merged config before use
The config system SHALL validate a fully merged config against the schema and report
all violations, so callers can fail before acting on an invalid config.

#### Scenario: Valid merged config
- **WHEN** the merged config contains only known keys with valid, in-range, correctly typed values
- **THEN** validation SHALL report no errors

#### Scenario: Invalid merged config
- **WHEN** the merged config contains an unknown key, a wrong-typed value, an out-of-range value, or an invalid enum
- **THEN** validation SHALL return a clear per-key error for each violation

