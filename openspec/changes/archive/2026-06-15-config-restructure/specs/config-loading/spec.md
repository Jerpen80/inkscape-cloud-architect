## MODIFIED Requirements

### Requirement: Initial config structure
The default config SHALL include a `document` section with a `margin` key, a `layout` section with a `mode` selector and canonical default values, a dense overlay, and preset-invariant style values, and a `theme` section with light and dark color palettes. Density values that do not differ between modes (style: colors, dash patterns, span-line styles, `availability_zone.enabled`, `label_prefix`) SHALL be defined once, not duplicated per preset.

#### Scenario: Document margin default
- **WHEN** the default config is loaded without user overrides
- **THEN** `config["document"]["margin"]` SHALL be `20`

#### Scenario: Layout section present
- **WHEN** the default config is loaded without user overrides
- **THEN** `config["layout"]` SHALL contain a `mode` selector (default "spaced"), canonical density values, and a dense overlay containing only the keys that differ from the canonical values

#### Scenario: Style keys defined once
- **WHEN** the default config is loaded without user overrides
- **THEN** keys that are identical across density modes (e.g. stroke colors, dash patterns, span-line styles, `availability_zone.enabled`, `label_prefix`) SHALL be defined in a single place, not duplicated in both density presets

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

## ADDED Requirements

### Requirement: Resolved config is unchanged by the restructure
Restructuring the default config (canonical defaults, dense-as-diff, single-source style keys) SHALL NOT change the resolved configuration the engine consumes, for either density mode.

#### Scenario: Resolved values unchanged per mode
- **WHEN** the config is resolved for `spaced` or for `dense`
- **THEN** the resolved flattened `layout.*` keys and their values SHALL be identical to those produced before the restructure

#### Scenario: Rendered output unchanged
- **WHEN** the same inputs are rendered before and after the restructure (for both density modes)
- **THEN** the produced SVG SHALL be byte-identical

### Requirement: Single source of default values
Default values SHALL have a single source — the default config — without duplicate fallback defaults embedded in rendering code for keys the resolver guarantees.

#### Scenario: No shadow default for a resolver-provided key
- **WHEN** a rendering module reads a layout key that the resolver always populates
- **THEN** it SHALL read the value without supplying an inline fallback default
