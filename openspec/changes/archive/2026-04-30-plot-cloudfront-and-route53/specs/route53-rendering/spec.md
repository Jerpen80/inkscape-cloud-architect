## ADDED Requirements

### Requirement: Parse Route 53 hosted zones from cloudia data
The parser SHALL extract Route 53 hosted zones from `route53-list-hosted-zones.json` and separate them into public and private zones.

#### Scenario: Public zones are parsed
- **WHEN** `parse_global_services` is called and `route53-list-hosted-zones.json` exists
- **THEN** each zone with `PrivateZone: false` SHALL be returned in the `route53_public_zones` list with `zone_id`, `name` (without trailing dot), `record_count`, and `is_private: false`

#### Scenario: Private zones are parsed
- **WHEN** `route53-list-hosted-zones.json` contains zones with `PrivateZone: true`
- **THEN** each private zone SHALL be returned in a separate `route53_private_zones` list with `zone_id`, `name` (without trailing dot), `record_count`, and `is_private: true`

#### Scenario: File not found
- **WHEN** `route53-list-hosted-zones.json` does not exist in any region directory
- **THEN** empty lists SHALL be returned without error

### Requirement: Render public Route 53 zones in Edge zone
Each public Route 53 hosted zone SHALL be rendered in the Edge zone as an icon+name card.

#### Scenario: Public zone card content
- **WHEN** a public Route 53 zone is rendered
- **THEN** it SHALL display the hosted zone icon, zone name (without trailing dot), and record count in parentheses

#### Scenario: All public zones shown
- **WHEN** an account has N public hosted zones
- **THEN** all N zones SHALL be rendered in the Edge zone

### Requirement: Render private Route 53 zones inside VPCs
Private Route 53 zones SHALL be rendered inside the VPC they are associated with.

#### Scenario: VPC association via list-hosted-zones-by-vpc data
- **WHEN** `route53-list-hosted-zones-by-vpc` data exists and maps a private zone to a VPC
- **THEN** the private zone SHALL be rendered inside that VPC as a spanning element in the pre-grid zone

#### Scenario: Single non-default VPC fallback
- **WHEN** no VPC association data exists and the region has exactly one non-default VPC
- **THEN** private zones SHALL be rendered inside that VPC

#### Scenario: Account-level fallback
- **WHEN** no VPC association data exists and the region has multiple non-default VPCs
- **THEN** private zones SHALL be rendered at the account level, below the Edge zone and above the regions row

### Requirement: Route 53 symbol
The extension SHALL use the Route 53 hosted zone icon from `AWS-Resource-networking-content-delivery-light.svg`.

#### Scenario: Symbol availability
- **WHEN** the extension runs
- **THEN** the symbol `AWS-Resource-networking-content-delivery-light.svg:res-amazon-route-53-hosted-zone` SHALL be available for rendering

### Requirement: Private zones on dedicated layer
Private Route 53 zone elements SHALL be rendered on a dedicated "Route 53 Private" layer.

#### Scenario: Layer creation
- **WHEN** private Route 53 zones are rendered inside VPCs
- **THEN** all private zone icons and names SHALL be placed on a layer named "Route 53 Private"

### Requirement: Route 53 layout configuration
Route 53 rendering parameters SHALL be configurable via `layout.route53` in the config.

#### Scenario: Default Route 53 config
- **WHEN** no user config override exists
- **THEN** `layout.route53` SHALL contain `icon_scale`, `font_size`, and `card_gap` with sensible defaults
