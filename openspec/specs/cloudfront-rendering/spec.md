### Requirement: Parse CloudFront distributions from cloudia data
The parser SHALL extract CloudFront distributions from `cloudfront-list-distributions.json` and return them as part of global services data.

#### Scenario: Distributions are parsed
- **WHEN** `parse_global_services` is called and `cloudfront-list-distributions.json` exists
- **THEN** each distribution SHALL be returned with `distribution_id`, `domain_name`, `aliases`, `comment`, and `status`

#### Scenario: File not found
- **WHEN** `cloudfront-list-distributions.json` does not exist in any region directory
- **THEN** an empty list SHALL be returned without error

### Requirement: Render CloudFront distributions as icon+name cards
Each CloudFront distribution SHALL be rendered as a card with icon, primary alias or comment, and distribution ID.

#### Scenario: Distribution card content
- **WHEN** a CloudFront distribution is rendered
- **THEN** it SHALL display the CloudFront icon, the distribution comment or first alias as the name, and the distribution ID (dimmed) below

#### Scenario: Distribution with aliases
- **WHEN** a distribution has aliases
- **THEN** the card name SHALL use the comment field (which typically describes the distribution purpose)

#### Scenario: Distribution without comment
- **WHEN** a distribution has no comment
- **THEN** the card name SHALL use the first alias, or the CloudFront domain name as fallback

### Requirement: CloudFront symbol
The extension SHALL use the CloudFront download distribution icon from `AWS-Resource-networking-content-delivery-light.svg`.

#### Scenario: Symbol availability
- **WHEN** the extension runs
- **THEN** the symbol `AWS-Resource-networking-content-delivery-light.svg:res-amazon-cloudfront-download-distribution` SHALL be available for rendering

### Requirement: CloudFront layout configuration
CloudFront rendering parameters SHALL be configurable via `layout.cloudfront` in the config.

#### Scenario: Default CloudFront config
- **WHEN** no user config override exists
- **THEN** `layout.cloudfront` SHALL contain `icon_scale`, `font_size`, and `card_gap` with sensible defaults
