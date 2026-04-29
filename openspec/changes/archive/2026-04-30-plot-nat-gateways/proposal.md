## Why

NAT gateways are a key networking component in AWS architectures — they enable private subnets to reach the internet. The diagram currently shows VPCs, subnets, EC2, databases, and load balancers, but omits NAT gateways. Adding them completes the network picture and shows which public subnets provide outbound connectivity.

Bean: [inkscape-cloud-architect-nat1](.beans/inkscape-cloud-architect-nat1--plot-nat-gateways.md)

## What Changes

- Parse NAT gateways from `ec2-describe-network-interfaces.json` by filtering on `InterfaceType: "nat_gateway"`
- Extract NAT gateway ID from the `Description` field, plus `SubnetId` and `VpcId` from the interface
- Render NAT gateways as icon+name cards inside their public subnets (same pattern as EC2/database cards)
- NAT gateways contribute to subnet height calculation
- Add dedicated "NAT Gateways" layer for visibility toggling
- Add `layout.nat_gateway` config section for card styling

## Capabilities

### New Capabilities
- `nat-gateway-rendering`: Rendering NAT gateways as icon+name cards inside their subnets with configurable styling

### Modified Capabilities
- `config-loading`: Default config gains `layout.nat_gateway` section
- `layout-config`: New `layout.nat_gateway` values added to config structure

## Impact

- **Parser**: `cloudia_parser.py` gains NAT gateway extraction from network interfaces in `parse_region()`
- **Rendering**: New `resource_nat.py` module; `resource_vpc.py` updated to accept and render NAT gateways inside subnets
- **Layers**: New "NAT Gateways" layer in z-order
- **Config**: `default-config.yaml` gains `layout.nat_gateway` section
- **Main**: `aws-auto-diagram.py` passes NAT gateway data through the rendering pipeline

## Verification

```bash
# Test with account that has NAT gateways
nix develop --command ./RUNME.sh extension_run account-data/111111111111 eu-west-1
nix develop --command ./RUNME.sh extension_run account-data/955922232824 us-west-2
```
