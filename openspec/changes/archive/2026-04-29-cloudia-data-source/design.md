# Design: Read VPCs and subnets from cloudia-reader-aws output

## Cloudia directory structure

```
account-data/{account-id}/
├── describe-regions.json
├── eu-west-1/
│   ├── ec2-describe-vpcs.json        ← { "Vpcs": [...] }
│   ├── ec2-describe-subnets.json     ← { "Subnets": [...] }
│   ├── ec2-describe-instances.json
│   └── ... (60+ more files)
├── eu-central-1/
│   └── ...
└── us-east-1/
    └── ...
```

## .inx params

```xml
<param name="data_dir" type="path" mode="folder"
  gui-text="Account data directory:"></param>
<param name="region" type="optiongroup" appearance="combo"
  gui-text="AWS Region:">
  <option value="eu-west-1">eu-west-1</option>
  <option value="eu-west-2">eu-west-2</option>
  <option value="eu-west-3">eu-west-3</option>
  <option value="eu-central-1">eu-central-1</option>
  <option value="eu-north-1">eu-north-1</option>
  <!-- ...all standard AWS regions -->
</param>
```

`data_dir` opens a native folder browser. `region` is a combo dropdown with all standard AWS regions. Default is `eu-west-1`.

## Data flow

```
.inx: data_dir + region
         │
         ▼
cloudia_parser.parse_region(data_dir, region)
         │
         ├── Read {data_dir}/{region}/ec2-describe-vpcs.json
         │   └── Vpcs[] → list of vpc dicts
         │
         ├── Read {data_dir}/{region}/ec2-describe-subnets.json
         │   └── Subnets[] → list of subnet dicts
         │
         └── Return (vpcs, subnets) in internal format
                    │
                    ▼
              effect() renders using existing resource_vpc module
```

## Internal format

Transformed from raw AWS API JSON:

```python
# VPC
{
    "type": "vpc",
    "name": "my-vpc (10.0.0.0/16)",   # from Tags["Name"] + CidrBlock, or VpcId fallback
    "vpc_id": "vpc-EXAMPLE...",
    "cidr": "10.0.0.0/16",
}

# Subnet
{
    "type": "subnet",
    "name": "public-a (172.31.16.0/20)",  # from Tags["Name"] + CidrBlock, or SubnetId fallback
    "subnet_id": "subnet-EXAMPLE...",
    "vpc_id": "vpc-EXAMPLE...",           # links subnet to VPC
    "cidr": "172.31.16.0/20",
    "az": "eu-west-1a",
    "is_public": true,                     # from MapPublicIpOnLaunch
}
```

## Name resolution

AWS resources may or may not have a Name tag:

```python
def get_name(resource, fallback_id, cidr):
    tags = resource.get("Tags", [])
    name_tag = next((t["Value"] for t in tags if t["Key"] == "Name"), None)
    if name_tag:
        return f"{name_tag} ({cidr})"
    return f"{fallback_id} ({cidr})"
```

## Public/private subnet detection

Replace the current name-based heuristic with the AWS API field:

```python
is_public = subnet.get("MapPublicIpOnLaunch", False)
```

This is the authoritative signal — if `MapPublicIpOnLaunch` is true, it's a public subnet.

## render_vpc changes

Current signature: `render_vpc(inkdoc)` — receives no VPC data.
New signature: `render_vpc(inkdoc, vpc)` — receives the vpc dict with name and CIDR.

## render_subnet changes

Current: checks `"private" not in name` for public/private.
New: checks `subnet["is_public"]` flag.

## Cleanup

- Remove `test-data.json`
- Remove `parse_test_data()` method from aws-auto-diagram.py
- Remove dead code methods marked "move to example" (rect, shape_test, remote_json_test, this_works, doc_symbols)

## Key decisions

- **Transform layer** — cloudia raw → internal format, keeps renderers decoupled from AWS API shape
- **Folder browser** — .inx `type="path" mode="folder"` gives native OS dialog
- **Region as combo dropdown** — static list of all standard AWS regions in .inx, default `eu-west-1`
- **Subnet grouping by VPC** — subnets have `vpc_id`, renderer can group them under the correct VPC rect
