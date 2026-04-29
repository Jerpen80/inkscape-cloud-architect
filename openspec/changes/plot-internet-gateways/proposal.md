## Why

Internet gateways are the connection between a VPC and the public internet. They sit at the VPC boundary and are a key architectural element — without an IGW, a VPC has no internet access. Currently absent from diagrams.

Bean: [inkscape-cloud-architect-igw1](.beans/inkscape-cloud-architect-igw1--plot-internet-gateways.md)

## What Changes

- Parse internet gateways from `ec2-describe-internet-gateways.json`
- Render IGWs at the VPC boundary as an icon+name element on the top-right corner of the VPC rect
- Each IGW shows the internet gateway icon and its Name tag (or ID as fallback)
- Add "Internet Gateways" layer to z-order
- Add `layout.internet_gateway` config section

## Capabilities

### New Capabilities
- `igw-rendering`: Parsing and rendering internet gateways at the VPC boundary

### Modified Capabilities
(none — IGW rendering is self-contained, placed on the VPC rect border without affecting VPC sizing)

## Impact

- **Parser**: `cloudia_parser.py` gains IGW parsing in `parse_region()`, returned alongside other resources
- **Rendering**: New `resource_igw.py` module
- **VPC**: `resource_vpc.py` calls IGW renderer after drawing the VPC rect
- **Layers**: New "Internet Gateways" layer
- **Config**: `default-config.yaml` gains `layout.internet_gateway` section
- **Main**: `aws-auto-diagram.py` passes IGWs through rendering pipeline
