### Requirement: Theme selection via INX parameter
The extension SHALL accept a `--theme` parameter via the INX dialog with options "Light" and "Dark".

#### Scenario: Light theme selected
- **WHEN** the user selects "Light" from the theme dropdown
- **THEN** the extension SHALL render with the light color palette

#### Scenario: Dark theme selected
- **WHEN** the user selects "Dark" from the theme dropdown
- **THEN** the extension SHALL render with the dark color palette

#### Scenario: Default theme
- **WHEN** no theme is explicitly selected
- **THEN** the extension SHALL default to "Light"

### Requirement: Theme color palettes in config
The config SHALL contain a `theme` section with `light` and `dark` sub-sections defining color palettes.

#### Scenario: Light palette defaults
- **WHEN** the light theme is selected
- **THEN** the palette SHALL provide `background: "none"`, `text_color: "#000000"`, `text_dimmed_opacity: 0.6`, and border colors for account, edge, vpc, subnets, and region

#### Scenario: Dark palette defaults
- **WHEN** the dark theme is selected
- **THEN** the palette SHALL provide `background: "#232F3E"`, `text_color: "#e0e0e0"`, `text_dimmed_opacity: 0.5`, and border colors appropriate for dark backgrounds

#### Scenario: User can override palette colors
- **WHEN** a user provides custom values in the theme config section
- **THEN** the custom values SHALL override the defaults

### Requirement: Theme resolution at startup
The extension SHALL resolve the theme parameter to a color palette dict at startup and make it available to all rendering modules.

#### Scenario: Theme palette available to renderers
- **WHEN** the extension starts rendering
- **THEN** every rendering module SHALL have access to the resolved theme palette via the config

### Requirement: Dark mode background
When dark mode is active, the extension SHALL render a solid background rect covering the full document.

#### Scenario: Dark background rendered
- **WHEN** the dark theme is selected
- **THEN** a filled rectangle with the theme background color SHALL be rendered as the bottommost element

#### Scenario: Light background
- **WHEN** the light theme is selected and background is "none"
- **THEN** no background rect SHALL be rendered

### Requirement: Text uses theme color
All text elements SHALL use an explicit `fill` color from the theme palette instead of relying on SVG default.

#### Scenario: Primary text color
- **WHEN** a text element is rendered
- **THEN** its style SHALL include `fill` set to the theme's `text_color`

#### Scenario: Dimmed text
- **WHEN** a dimmed text element is rendered (e.g., instance type, version label)
- **THEN** its style SHALL include `fill` set to the theme's `text_color` and `fill-opacity` set to the theme's `text_dimmed_opacity`

### Requirement: Structural borders use theme colors
Border colors for account, edge, VPC, subnet, and region rects SHALL come from the theme palette.

#### Scenario: VPC border color
- **WHEN** a VPC rect is rendered
- **THEN** its stroke color SHALL be the theme's `border_vpc` value

#### Scenario: Account border in dark mode
- **WHEN** the dark theme is active and the account rect is rendered
- **THEN** the stroke SHALL use the theme's `border_account` value (light color instead of black)

### Requirement: Theme helper module
A `theme.py` module SHALL provide helper functions for resolving theme colors.

#### Scenario: Get text color
- **WHEN** `get_text_color(config)` is called
- **THEN** it SHALL return the resolved theme's `text_color` value

#### Scenario: Get border color
- **WHEN** `get_border_color(config, "vpc")` is called
- **THEN** it SHALL return the resolved theme's `border_vpc` value
