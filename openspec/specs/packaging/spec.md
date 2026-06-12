# packaging Specification

## Purpose
TBD - created by archiving change nix-package-ica. Update Purpose after archive.
## Requirements
### Requirement: ica is an installable flake output
The flake SHALL expose `ica` as a package and app so it can be run via `nix run`
and installed via `nix profile install`.

#### Scenario: Run via nix
- **WHEN** `nix run .#ica -- --help` is executed
- **THEN** the `ica` CLI SHALL run and print its help

#### Scenario: Installed entry point
- **WHEN** `ica` is installed via `nix profile install`
- **THEN** an `ica` executable SHALL be available on PATH and runnable from any directory

### Requirement: Packaging does not move shared code
Packaging SHALL build the extension directory in place; `ica_utils` SHALL remain
beside the Inkscape extension script so the `.inx` dialog keeps working.

#### Scenario: Inkscape dialog unaffected
- **WHEN** the package is built
- **THEN** the Inkscape extension entry script and `ica_utils` SHALL remain co-located
- **AND** the Inkscape dialog path SHALL continue to function unchanged

### Requirement: Self-contained runtime closure
The package SHALL include the Python runtime dependencies needed to render
(inkex, lxml, tinycss2, pyyaml, typer) and SHALL NOT require the development shell.

#### Scenario: Render dependencies resolve
- **WHEN** `ica render` runs from the installed package
- **THEN** all Python imports SHALL resolve from the package closure without the dev shell

#### Scenario: cloudia excluded
- **WHEN** the package closure is built
- **THEN** it SHALL NOT include cloudia (rendering does not depend on it)

### Requirement: Inkscape dependency is declared
The package SHALL document that `ica` requires an Inkscape installation, since it
installs into and renders against the Inkscape user directory.

#### Scenario: Dependency documented
- **WHEN** a user inspects the package or its help/metadata
- **THEN** the Inkscape requirement SHALL be stated

