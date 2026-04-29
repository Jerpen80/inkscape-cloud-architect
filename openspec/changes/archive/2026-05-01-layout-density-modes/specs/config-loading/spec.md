## MODIFIED Requirements

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

#### Scenario: Layout resolved before rendering
- **WHEN** the extension starts
- **THEN** the selected layout mode's values SHALL be merged into `config["layout"]` top-level keys before any rendering occurs
