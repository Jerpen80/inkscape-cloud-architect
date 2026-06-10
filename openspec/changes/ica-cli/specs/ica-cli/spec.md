## ADDED Requirements

### Requirement: The `ica` command exists
The system SHALL provide a command-line program named `ica` offering subcommands,
`--version`, `--help`, a verbosity option, and shell completion.

#### Scenario: Version and help
- **WHEN** `ica --version` is run
- **THEN** it SHALL print the version and exit zero
- **AND WHEN** `ica --help` is run, it SHALL list the available subcommands

#### Scenario: Unknown subcommand
- **WHEN** `ica` is invoked with an unknown subcommand
- **THEN** it SHALL print an error and exit non-zero

### Requirement: Render a diagram
`ica render` SHALL produce a diagram SVG from account-data by calling the headless
render engine directly (no subprocess, no Inkscape runtime).

#### Scenario: Basic render to a file
- **WHEN** `ica render <data_dir> <region> -o out.svg` is run
- **THEN** it SHALL write the rendered SVG to `out.svg` and exit zero

#### Scenario: Theme, layout, and account options
- **WHEN** `--theme`, `--layout-mode`, or `--account-name` are provided
- **THEN** they SHALL be applied to the render exactly as the equivalent engine inputs

### Requirement: Output target is explicit
`ica render` SHALL require an output target and SHALL NOT write SVG to stdout
implicitly.

#### Scenario: Output is required
- **WHEN** `ica render <data_dir> <region>` is run without `-o`
- **THEN** it SHALL print an error and exit non-zero without rendering

#### Scenario: Explicit stdout
- **WHEN** `ica render <data_dir> <region> -o -` is run
- **THEN** it SHALL write the SVG to stdout

### Requirement: Layered config overrides on render
`ica render` SHALL accept a config override file via `--config <file>` and repeatable
inline overrides via `--set <dotted.key>=<value>`, merged over the defaults.

#### Scenario: Override file
- **WHEN** `--config style.yaml` is provided
- **THEN** its values SHALL be deep-merged over `default-config.yaml`

#### Scenario: Inline overrides
- **WHEN** one or more `--set <dotted.key>=<value>` are provided
- **THEN** each SHALL set that key in the merged config

#### Scenario: Merge precedence
- **WHEN** both `--config` and `--set` set the same key
- **THEN** the `--set` value SHALL win (order: defaults ◄ file ◄ --set)

### Requirement: Inline overrides are validated and type-coerced before rendering
`ica render` SHALL coerce each `--set` value to the key's schema type and SHALL
validate the merged config against the schema before rendering; on any error it
SHALL fail without producing a diagram.

#### Scenario: Type coercion
- **WHEN** `--set layout.ec2.icon_scale=0.8` is provided
- **THEN** the value SHALL be coerced to the float `0.8` per the schema before rendering

#### Scenario: Invalid override fails fast
- **WHEN** a `--set` or `--config` value is an unknown key, wrong type, out of range, or an invalid enum
- **THEN** `ica render` SHALL print a clear per-key error, exit non-zero, and NOT write any SVG

### Requirement: Scaffold a starter config
`ica initconf` SHALL write a curated starter config of common options with sane
defaults sourced from the schema, suitable for use with `ica render --config`.

#### Scenario: Generate a starter config
- **WHEN** `ica initconf -o my.yaml` is run
- **THEN** it SHALL write a YAML file containing a curated subset of keys (e.g. theme, layout mode, common knobs) with default values
- **AND** it SHALL include a comment pointing to the full set of configurable keys

#### Scenario: Starter config is consumable
- **WHEN** the generated file is passed to `ica render --config <file>`
- **THEN** it SHALL load and validate without error
