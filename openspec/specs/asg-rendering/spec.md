### Requirement: Parse Auto Scaling Groups
The parser SHALL extract ASGs from `autoscaling-describe-auto-scaling-groups.json`.

#### Scenario: ASG with instances parsed
- **WHEN** `parse_region` is called and an ASG has InService instances
- **THEN** the ASG SHALL be returned with `name`, `instance_ids`, `subnet_ids`, `min_size`, `max_size`, `desired_capacity`, and `vpc_id`

#### Scenario: ASG with zero instances skipped
- **WHEN** an ASG has no InService instances
- **THEN** it SHALL NOT be included in the returned ASGs

### Requirement: Render ASG as horizontal spanning rectangle
Each ASG SHALL be rendered as a dashed rectangle that spans horizontally across the subnet columns it covers, crossing subnet boundaries and column gaps.

#### Scenario: ASG spanning two AZ columns
- **WHEN** an ASG has subnets in col 0 (us-east-2a) and col 1 (us-east-2b)
- **THEN** the dashed rectangle SHALL span from the left edge of col 0 to the right edge of col 1

#### Scenario: ASG in single column
- **WHEN** an ASG has subnets in only one column
- **THEN** the dashed rectangle SHALL be contained within that column's width

#### Scenario: ASG label
- **WHEN** an ASG spanning rect is rendered
- **THEN** it SHALL display the ASG icon, name on the first line, and capacity as `min:N desired:N max:N` on the second line at the top-left of the rect

#### Scenario: No visible fill
- **WHEN** an ASG spanning rect is rendered
- **THEN** it SHALL have no fill (transparent), only a dashed stroke

### Requirement: ASG band positioning
EC2 instances within ASGs SHALL be rendered in horizontal bands that are consistent across all columns in a row, so that the spanning ASG rectangle correctly encloses its instances in every column.

#### Scenario: Same ASG band y-position across columns
- **WHEN** an ASG has instances in column 0 and column 2
- **THEN** the instances SHALL be rendered at the same y-band in both columns

#### Scenario: Multiple ASGs stacking in same row
- **WHEN** 5 ASGs have instances in the same subnet row
- **THEN** they SHALL stack vertically without overlap, each in its own band

#### Scenario: Non-ASG instances above ASG bands
- **WHEN** a subnet has both ASG and non-ASG instances
- **THEN** non-ASG instances SHALL render first (top), followed by ASG bands below

### Requirement: Row height accounts for cross-column ASG bands
Subnet row height SHALL account for the total ASG band height across ALL columns in the row, not just the local subnet's ASGs. This ensures DB/NAT cards placed below the ASG bands don't overflow the subnet rect.

#### Scenario: ASG in one column, DB in another
- **WHEN** column 0 has 1 EC2 instance in an ASG, and column 1 has 6 RDS instances in the same row
- **THEN** the row height SHALL include the ASG band height (from column 0) plus the DB cards height (from column 1), whichever combination is tallest

#### Scenario: Multiple ASGs across columns in same row
- **WHEN** a row contains instances from 3 different ASGs across its columns
- **THEN** the row height SHALL include the cumulative band height for all 3 ASGs, even in columns that only have 1 of those ASGs

#### Scenario: Bottom margin after last ASG band
- **WHEN** a row contains ASG bands
- **THEN** the row height SHALL include an additional padding below the last ASG band so the ASG rect does not touch the subnet bottom edge

### Requirement: DB cards placed below cross-column ASG bands
Database and other resource cards SHALL be placed below the full cross-column ASG band area, not just below the local subnet's ASG instances.

#### Scenario: DB offset uses band cursor
- **WHEN** a subnet has EC2 instances in ASGs and RDS instances
- **THEN** the RDS cards SHALL start below the y-position where all ASG bands end (accounting for ASG bands from other columns in the same row)

### Requirement: Column width accounts for ASG labels
Subnet column width SHALL grow to fit ASG label content (icon + name + padding).

#### Scenario: Long ASG name
- **WHEN** an ASG name is wider than the subnet label
- **THEN** the column width SHALL expand to fit the ASG label

### Requirement: ASG elements on dedicated layer
ASG dashed containers, icons, and labels SHALL be rendered on a dedicated "Auto Scaling Groups" layer.

#### Scenario: Layer creation
- **WHEN** ASGs are rendered
- **THEN** all ASG spanning rects, icons, and labels SHALL be placed on a layer named "Auto Scaling Groups"

### Requirement: ASG layout configuration
ASG rendering parameters SHALL be configurable via `layout.asg` in the config.

#### Scenario: Default ASG config
- **WHEN** no user config override exists
- **THEN** `layout.asg` SHALL contain `icon_scale`, `stroke_color`, `stroke_width`, `stroke_dasharray`, `label_height`, `padding`, `top_margin`, and `font_size`
