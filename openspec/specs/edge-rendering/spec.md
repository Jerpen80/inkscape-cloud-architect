### Requirement: Edge zone placement
The Edge zone SHALL render inside the Account rect, above the regions row, as a bordered rect containing public Route 53 zones and CloudFront distributions.

#### Scenario: Account with Edge resources
- **WHEN** an account has public Route 53 zones or CloudFront distributions
- **THEN** an Edge zone rect SHALL be rendered inside the Account rect, above the horizontal Row of regions

#### Scenario: Account without Edge resources
- **WHEN** an account has no public Route 53 zones and no CloudFront distributions
- **THEN** no Edge zone SHALL be rendered and the layout SHALL remain unchanged

#### Scenario: No Account rect
- **WHEN** no account name is specified (no Account rect)
- **THEN** the Edge zone SHALL still render above the regions row without an Account wrapper

### Requirement: Edge zone internal layout
The Edge zone SHALL display Route 53 public zones on the left and CloudFront distributions on the right in side-by-side vertical stacks.

#### Scenario: Both R53 and CloudFront present
- **WHEN** the Edge zone contains both public Route 53 zones and CloudFront distributions
- **THEN** Route 53 zones SHALL be stacked vertically on the left and CloudFront distributions SHALL be stacked vertically on the right

#### Scenario: Only R53 zones present
- **WHEN** the Edge zone contains public Route 53 zones but no CloudFront distributions
- **THEN** only Route 53 zones SHALL be rendered in the Edge zone

#### Scenario: Only CloudFront present
- **WHEN** the Edge zone contains CloudFront distributions but no public Route 53 zones
- **THEN** only CloudFront distributions SHALL be rendered in the Edge zone

### Requirement: Edge zone adjusts Account layout
The Account rect and regions row SHALL shift down to accommodate the Edge zone.

#### Scenario: Edge zone present
- **WHEN** the Edge zone is rendered
- **THEN** the regions Row SHALL start below the Edge zone with configurable spacing

### Requirement: Edge zone on dedicated layer
Edge zone elements SHALL be rendered on a dedicated "Edge" layer.

#### Scenario: Layer creation
- **WHEN** the Edge zone is rendered
- **THEN** the Edge rect, all R53 zone cards, and all CloudFront cards SHALL be placed on a layer named "Edge"

### Requirement: Edge layout configuration
Edge zone rendering parameters SHALL be configurable via `layout.edge` in the config.

#### Scenario: Default Edge config
- **WHEN** no user config override exists
- **THEN** `layout.edge` SHALL contain padding, gap between R53 and CF columns, and spacing below the Edge zone
