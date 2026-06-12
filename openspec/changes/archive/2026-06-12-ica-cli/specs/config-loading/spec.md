## ADDED Requirements

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
