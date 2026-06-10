# render-engine Specification

## Purpose
TBD - created by archiving change thin-seam-render-engine. Update Purpose after archive.
## Requirements
### Requirement: Headless render entry point
The system SHALL provide a render function that produces diagram SVG from
account-data and config without instantiating an `inkex.EffectExtension` or
requiring a running Inkscape process.

#### Scenario: Render without Inkscape runtime
- **WHEN** the render function is called with a data directory, a region, and a loaded config
- **THEN** it SHALL return the diagram as a serialized SVG string
- **AND** it SHALL NOT instantiate `inkex.EffectExtension`
- **AND** it SHALL NOT spawn an Inkscape process

#### Scenario: Render function is importable
- **WHEN** another module imports the render entry point
- **THEN** the import SHALL succeed without side effects on the Inkscape extension

### Requirement: Shared orchestration across front-ends
The rendering orchestration SHALL be implemented once and used by both the
Inkscape extension path and the headless render path.

#### Scenario: Extension delegates to the shared engine
- **WHEN** the Inkscape extension's `effect()` runs
- **THEN** it SHALL invoke the same shared orchestration the headless path uses
- **AND** the extension class SHALL remain a thin wrapper containing no duplicated render logic

### Requirement: Document abstraction for renderers
The system SHALL provide a document object (the "inkdoc") that the resource
rendering modules draw into. The object SHALL expose an inkex SVG document as
`svg` and a `make_symbol_instance(symbol_id, parent)` method, and SHALL be
satisfiable both by the live Inkscape extension and by the headless engine.

#### Scenario: Renderers operate on the document object
- **WHEN** a resource rendering module is called with an inkdoc
- **THEN** it SHALL be able to access `inkdoc.svg` (append, findall, descendants, defs)
- **AND** it SHALL be able to call `inkdoc.make_symbol_instance(symbol_id, parent)`

#### Scenario: Both paths satisfy the same surface
- **WHEN** rendering runs via the Inkscape extension or via the headless engine
- **THEN** both SHALL provide an inkdoc satisfying the same documented surface
- **AND** the orchestration SHALL be agnostic to which path constructed it

### Requirement: Configurable symbol source location
The symbol-source directory SHALL be resolvable from an explicit option or config
value, falling back to the Inkscape installation location, so that a non-Inkscape
install can locate symbols.

#### Scenario: Explicit symbol directory honored
- **WHEN** the render is invoked with an explicit symbol directory
- **THEN** symbol defs SHALL be imported from that directory

#### Scenario: Default preserves Inkscape behavior
- **WHEN** no explicit symbol directory and no config override are provided
- **THEN** symbols SHALL be resolved from the Inkscape symbols location (`<inkscape_dir>/symbols/aws-architect/`)
- **AND** the Inkscape extension's symbol loading SHALL be unchanged

### Requirement: Output is the caller's responsibility
The render entry point SHALL return SVG content and SHALL NOT itself decide an
output file path.

#### Scenario: Engine returns content, caller writes
- **WHEN** the render function completes
- **THEN** it SHALL return the SVG as a string
- **AND** writing the SVG to a file (and choosing the path) SHALL be performed by the caller

### Requirement: Rendered output is unchanged by the refactor
Extracting the engine SHALL NOT change the rendered SVG for existing inputs.

#### Scenario: Byte-identical output
- **WHEN** the same data directory, region, and config are rendered before and after this change
- **THEN** the produced SVG SHALL be byte-identical

