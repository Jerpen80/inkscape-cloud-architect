## ADDED Requirements

### Requirement: ica doctor checks environment health
`ica doctor` SHALL verify the rendering environment and report a clear per-item
status: inkex availability, presence of the required symbols, and (for GUI use)
presence of templates and the installed extension.

#### Scenario: Healthy environment
- **WHEN** `ica doctor` runs and inkex is importable and all required symbols are present
- **THEN** it SHALL report each check as OK and exit zero

#### Scenario: Symbols checked at the resolved location
- **WHEN** `ica doctor` checks symbols
- **THEN** it SHALL look in the same directory `ica render` uses (explicit option → config → Inkscape default) and SHALL verify each required symbol file the engine loads is present

#### Scenario: GUI-only items are warnings
- **WHEN** templates or the installed extension are absent but inkex and symbols are present
- **THEN** `ica doctor` SHALL report them as warnings and SHALL still exit zero (the headless CLI does not require them)

### Requirement: ica doctor fails on missing required dependencies
`ica doctor` SHALL exit non-zero when a required check fails (inkex not importable,
or required symbols missing), so it is usable as a precondition gate.

#### Scenario: Missing symbols
- **WHEN** the required symbols are not present at the resolved location
- **THEN** `ica doctor` SHALL report the failure and exit non-zero

#### Scenario: inkex unavailable
- **WHEN** inkex cannot be imported
- **THEN** `ica doctor` SHALL report the failure and exit non-zero

### Requirement: ica doctor gives actionable remedies
For each failing or warning check, `ica doctor` SHALL print a specific next step.

#### Scenario: Remedy for missing symbols
- **WHEN** symbols are missing
- **THEN** the output SHALL instruct the user to run `ica setup` (optionally with `--asset-zip`)

#### Scenario: Remedy for missing inkex
- **WHEN** inkex is unavailable
- **THEN** the output SHALL instruct the user how to obtain it (e.g. run inside the `nix develop` shell / install via the flake)
