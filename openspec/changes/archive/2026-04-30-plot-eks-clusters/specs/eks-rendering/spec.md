## ADDED Requirements

### Requirement: Parse EKS clusters from cloudia data
The parser SHALL extract EKS clusters from `eks-list-clusters.json` and `eks-describe-cluster/<name>` files and return them alongside VPCs, subnets, instances, and load balancers.

#### Scenario: Active clusters are parsed
- **WHEN** `parse_region` is called and `eks-list-clusters.json` contains cluster names with corresponding `eks-describe-cluster/<name>` files
- **THEN** each cluster with status `ACTIVE` SHALL be returned with `name`, `version`, `vpc_id`, `subnet_ids`, and `status`

#### Scenario: Non-active clusters are excluded
- **WHEN** a cluster has a status other than `ACTIVE`
- **THEN** it SHALL NOT be included in the returned clusters

#### Scenario: Missing describe file
- **WHEN** `eks-list-clusters.json` lists a cluster name but no corresponding `eks-describe-cluster/<name>` file exists
- **THEN** that cluster SHALL be skipped without error

### Requirement: Render EKS clusters as VPC spanning elements
Each ACTIVE EKS cluster SHALL be rendered in a pre-grid zone within its VPC, visually spanning the AZ columns its subnets belong to.

#### Scenario: EKS cluster spanning two AZ columns
- **WHEN** a cluster is attached to subnets in eu-west-1a (col 0) and eu-west-1b (col 1)
- **THEN** it SHALL be rendered with a horizontal span line from the left edge of col 0 to the right edge of col 1

#### Scenario: EKS card content
- **WHEN** an EKS cluster is rendered
- **THEN** it SHALL display the EKS icon (left-aligned), cluster name (right of icon), and Kubernetes version (below name, dimmed)

#### Scenario: No visible rectangle
- **WHEN** an EKS cluster is rendered
- **THEN** there SHALL be no visible rectangle or border around the cluster card

#### Scenario: Cluster subnets not in diagram
- **WHEN** a cluster references subnets that are not present in the subnet grid
- **THEN** the span line SHALL only cover columns for subnets that are in the grid
- **AND** if no referenced subnets are in the grid, the cluster SHALL render with icon and name but no span line

### Requirement: EKS zone placement below load balancers
The EKS zone SHALL render below the load balancer zone and above the subnet grid within the VPC.

#### Scenario: VPC with both LBs and EKS clusters
- **WHEN** a VPC contains load balancers and EKS clusters
- **THEN** the LB zone SHALL render first (higher), followed by the EKS zone, followed by the subnet grid

#### Scenario: VPC with only EKS clusters
- **WHEN** a VPC contains EKS clusters but no load balancers
- **THEN** the EKS zone SHALL render in the pre-grid area above the subnet grid

### Requirement: Multiple EKS clusters stack vertically
When a VPC contains multiple EKS clusters, they SHALL stack vertically in the EKS zone.

#### Scenario: Three clusters in one VPC
- **WHEN** a VPC has three EKS clusters
- **THEN** they SHALL be rendered stacked vertically with configurable spacing between them

### Requirement: EKS zone adjusts VPC height
The VPC top padding SHALL grow to accommodate the EKS zone when clusters are present.

#### Scenario: VPC with EKS clusters
- **WHEN** a VPC contains N EKS clusters
- **THEN** additional vertical space SHALL be added to the VPC's top area to fit the EKS zone

#### Scenario: VPC without EKS clusters
- **WHEN** a VPC has no EKS clusters
- **THEN** the VPC layout SHALL remain unchanged

### Requirement: EKS symbol import
The extension SHALL import the EKS Cloud icon from `AWS-Service-containers.svg`.

#### Scenario: Symbol availability
- **WHEN** the extension runs
- **THEN** the symbol `AWS-Service-containers.svg:arch-amazon-eks-cloud` SHALL be available for rendering

### Requirement: EKS clusters on dedicated layer
EKS cluster elements SHALL be rendered on a dedicated "EKS" layer.

#### Scenario: Layer creation
- **WHEN** EKS clusters are rendered
- **THEN** all cluster icons, names, versions, and span lines SHALL be placed on a layer named "EKS"

### Requirement: EKS layout configuration
EKS rendering parameters SHALL be configurable via `layout.eks` in the config.

#### Scenario: Default EKS config
- **WHEN** no user config override exists
- **THEN** `layout.eks` SHALL contain `icon_scale`, `font_size`, `card_height`, `card_gap`, `span_line_color`, `span_line_width`, and `span_line_dasharray` with sensible defaults
