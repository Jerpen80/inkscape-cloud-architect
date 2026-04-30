## Why

EKS is a core compute service missing from generated diagrams. This account (111111111111) has 3 EKS clusters in a single VPC, each spanning 2-3 availability zones. The existing load balancer spanning pattern provides a proven template for rendering EKS clusters as VPC-level spanning elements.

Bean: [inkscape-cloud-architect-eks1](.beans/inkscape-cloud-architect-eks1--plot-eks-clusters.md)

## What Changes

- Parse EKS cluster data from `eks-list-clusters.json` and `eks-describe-cluster/<name>` files
- Render EKS clusters as spanning elements in the VPC pre-grid zone (below load balancers, above subnets)
- Each cluster shows: EKS icon, cluster name, Kubernetes version, and a span line across the AZ columns its subnets belong to
- Only render clusters with status `ACTIVE`
- Add `AWS-Service-containers.svg` to imported symbol files for the EKS Cloud icon
- Add "EKS" layer to the z-order
- Add `layout.eks` config section for card styling

## Capabilities

### New Capabilities
- `eks-rendering`: Rendering EKS clusters as spanning elements inside VPCs with icon, name, version, and AZ span lines

### Modified Capabilities
- `ec2-rendering`: Subnet height calculation must account for EKS zone height in the VPC pre-grid area (same integration point as load balancers)

## Impact

- **Parser**: `cloudia_parser.py` gains EKS cluster parsing, returns clusters alongside existing data
- **Rendering**: New `resource_eks.py` module for cluster cards and span lines
- **Symbols**: `AWS-Service-containers.svg` added to `SYMBOL_FILES`
- **Layers**: New "EKS" layer after "Load Balancers" in z-order
- **Config**: `default-config.yaml` gains `layout.eks` section
- **VPC layout**: `resource_vpc.py` integrates EKS zone height into pad_top, renders EKS zone between LB zone and subnets
- **Main**: `aws-auto-diagram.py` passes EKS clusters through the rendering pipeline
