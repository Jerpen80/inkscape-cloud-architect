### Requirement: NAT gateway data parsing
The parser SHALL extract NAT gateways from `ec2-describe-network-interfaces.json` by filtering on `InterfaceType: "nat_gateway"`.

#### Scenario: NAT gateway found in network interfaces
- **WHEN** a network interface has `InterfaceType` of `"nat_gateway"`
- **THEN** the parser SHALL extract the NAT gateway ID from the `Description` field, along with `SubnetId` and `VpcId`

#### Scenario: No NAT gateways in region
- **WHEN** no network interfaces have `InterfaceType` of `"nat_gateway"`
- **THEN** the parser SHALL return an empty NAT gateway list for that region

### Requirement: NAT gateway card rendering
Each NAT gateway SHALL be rendered as an icon + name text card inside its subnet.

#### Scenario: NAT gateway visual style
- **WHEN** a NAT gateway is rendered
- **THEN** it SHALL display the `AWS-Resource-networking-content-delivery-light.svg:res-amazon-vpc-nat-gateway` icon scaled per `layout.nat_gateway.icon_scale` and the NAT gateway ID as name

### Requirement: NAT gateways inside subnets
NAT gateway cards SHALL be rendered inside their subnet cell, stacked after EC2 and database cards.

#### Scenario: Subnet with EC2 and NAT gateway
- **WHEN** a subnet contains EC2 instances and a NAT gateway
- **THEN** the NAT gateway card SHALL render below the EC2 cards

#### Scenario: NAT gateway contributes to subnet height
- **WHEN** a subnet contains a NAT gateway
- **THEN** the subnet cell height SHALL include the NAT gateway card height

### Requirement: NAT Gateways layer
NAT gateway cards SHALL be rendered on a dedicated "NAT Gateways" layer.

#### Scenario: Layer z-order
- **WHEN** the extension creates layers
- **THEN** the "NAT Gateways" layer SHALL be created after the database layer in z-order
