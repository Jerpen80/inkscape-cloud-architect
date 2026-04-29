## Why

Load balancers (ALB/NLB) are a core networking component in AWS architectures. Unlike EC2 instances which live in a single subnet, load balancers span multiple subnets across availability zones. Rendering them as spanning elements accurately represents their multi-AZ nature and lays the groundwork for connection lines to targets.

Related task: [inkscape-cloud-architect-505b](.beans/inkscape-cloud-architect-505b--plot-albs-and-nlbs.md)

## What Changes

- Parse `elbv2-describe-load-balancers.json` in `cloudia_parser.py` to extract ALBs and NLBs
- Render each load balancer as a spanning element in a pre-grid zone between the VPC label and the subnet area
- The LB visually spans from its leftmost to rightmost subnet column
- Add `AWS-Resource-networking-content-delivery-light.svg` to symbol imports
- Add LB elements to a new "Load Balancers" layer
- Add LB layout config under `layout.load_balancer`

## Capabilities

### New Capabilities
- `load-balancer-rendering`: Parsing and rendering ALBs/NLBs as column-spanning elements within VPCs

### Modified Capabilities
<!-- None -->

## Impact

- Modified: `extensions/aws-auto-diagram/ica_utils/cloudia_parser.py` (parse load balancers)
- Modified: `extensions/aws-auto-diagram/ica_utils/resource_vpc.py` (LB zone, adjusted padding)
- Modified: `extensions/aws-auto-diagram/aws-auto-diagram.py` (pass LBs, symbol imports, layer)
- Modified: `extensions/aws-auto-diagram/default-config.yaml` (LB config section)
- New: `extensions/aws-auto-diagram/ica_utils/resource_lb.py` (LB rendering)
