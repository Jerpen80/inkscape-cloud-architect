## ADDED Requirements

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
