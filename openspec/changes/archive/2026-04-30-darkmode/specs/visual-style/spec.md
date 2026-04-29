## MODIFIED Requirements

### Requirement: Container Rectangles use theme colors
Container rectangle stroke colors SHALL come from the resolved theme palette instead of hardcoded constants.

#### Scenario: VPC border from theme
- **WHEN** a VPC rect is rendered
- **THEN** its stroke color SHALL be `theme.border_vpc` (default: `#8c4fff`)

#### Scenario: Account border from theme
- **WHEN** an account rect is rendered
- **THEN** its stroke color SHALL be `theme.border_account` (default: `#000000` for light, `#e0e0e0` for dark)

#### Scenario: Public subnet border from theme
- **WHEN** a public subnet rect is rendered
- **THEN** its stroke color SHALL be `theme.border_subnet_public` (default: `#7aa116`)

#### Scenario: Private subnet border from theme
- **WHEN** a private subnet rect is rendered
- **THEN** its stroke color SHALL be `theme.border_subnet_private` (default: `#00a4a6`)
