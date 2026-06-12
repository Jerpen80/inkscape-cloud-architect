# environment-setup Specification

## Purpose
TBD - created by archiving change nix-package-ica. Update Purpose after archive.
## Requirements
### Requirement: ica setup installs symbols and templates
`ica setup` SHALL build the AWS symbols and install symbols and templates into the
user's Inkscape directory so that `ica render` can subsequently produce a diagram.

#### Scenario: Setup enables rendering
- **WHEN** `ica setup` completes successfully on a machine with Inkscape
- **THEN** symbols SHALL be installed under `$INKSCAPE_DIR/symbols/aws-architect/`
- **AND** templates SHALL be installed under `$INKSCAPE_DIR/templates/aws-architect/`
- **AND** a subsequent `ica render` SHALL succeed

### Requirement: AWS icon ZIP resolution order
`ica setup` SHALL obtain the AWS icon asset ZIP using the first available source
of: an explicit local path, a configurable download URL, then a repository
fallback. The built symbols SHALL NOT be shipped in the package.

#### Scenario: Explicit local ZIP
- **WHEN** `ica setup --asset-zip <path>` is given a valid local ZIP
- **THEN** that ZIP SHALL be used to build the symbols

#### Scenario: Download from the configured URL
- **WHEN** no `--asset-zip` is given and a download URL is available
- **THEN** `ica setup` SHALL download the AWS icon package from that URL
- **AND** the URL SHALL be overridable via configuration

#### Scenario: Repository fallback
- **WHEN** no `--asset-zip` is given and the download is unavailable
- **THEN** `ica setup` SHALL fall back to the AWS icon ZIP committed in the repository

#### Scenario: All sources unavailable
- **WHEN** no ZIP can be obtained from any source
- **THEN** `ica setup` SHALL fail with a clear message pointing to the AWS icons download page

### Requirement: Symbols are never redistributed by the package
The package SHALL ship the symbol build tooling and templates but SHALL NOT ship
AWS-derived symbol output; the user obtains the AWS icons at setup time.

#### Scenario: No prebuilt symbols in the package
- **WHEN** the package contents are inspected
- **THEN** they SHALL include the symbol build scripts and templates
- **AND** they SHALL NOT include built AWS symbol SVGs

### Requirement: Setup targets the Inkscape user directory
`ica setup` SHALL resolve the Inkscape user directory per platform and install into
it, so symbols/templates are shared with the Inkscape GUI.

#### Scenario: Platform-correct location
- **WHEN** `ica setup` runs
- **THEN** it SHALL resolve `$INKSCAPE_DIR` correctly for the platform (e.g. `~/.config/inkscape` on Linux)
- **AND** install symbols and templates beneath it

