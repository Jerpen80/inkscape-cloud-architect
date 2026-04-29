## Context

The diagram renders VPCs and subnets but no compute resources. EC2 instances have a direct `SubnetId`, making placement unambiguous. The Grid currently uses uniform `cell_height` — this must become variable to accommodate different instance counts per subnet.

## Goals / Non-Goals

**Goals:**
- Parse and render running EC2 instances inside their subnet boxes
- Dynamic subnet height based on instance count
- New "EC2" layer for instance elements

**Non-Goals:**
- Rendering stopped/terminated instances
- Rendering other compute resources (RDS, ECS, etc.)
- Connection lines between resources

## Decisions

### 1. Instance card layout: icon + name + type, no border

Each instance is rendered as 3 centered lines stacked vertically inside the subnet:
```
      🖥              ← icon (AWS EC2 instance symbol)
  ec2-asg-nat-2a      ← name (from Name tag or instance ID)
     t4g.nano         ← instance type
```

No visible rectangle around the card. The icon comes from `AWS-Resource-compute-light.svg:res-amazon-ec2-instance`.

### 2. Symbol file import

The extension currently imports `AWS-Group-light.svg` for group symbols (VPC, subnet). EC2 needs `AWS-Resource-compute-light.svg`. The import mechanism in `import_defs_from_external_file_in_document` must be generalized to load multiple symbol files.

### 3. Variable row heights in Grid

Grid currently takes a single `cell_height`. Change to accept `row_heights` (list of per-row heights), similar to how `col_widths` already works. The height of each row = max instances across subnets in that row, converted to pixel height. Subnets with 0 instances keep the minimum `subnet.height` from config.

Formula per row:
```
row_height = max(
    subnet_label_height + (instance_card_height * instance_count) + padding,
    min_subnet_height
)
```

Where `instance_count` is the max across all cells in that row.

### 4. Parser returns instances alongside VPCs and subnets

`cloudia_parser.parse_region` returns a third value: list of instance dicts with `subnet_id`, `vpc_id`, `name`, `instance_type`, `state`. Only running instances are included.

### 5. New module `resource_ec2.py`

Rendering logic for EC2 instances lives in a new module, following the pattern of `resource_vpc.py`. Called from `resource_vpc.py` after drawing the subnet rectangle, passing the subnet position and dimensions.

### 6. EC2 config section

```yaml
layout:
  ec2:
    icon_scale: 0.5
    font_size: 13
    card_gap: 8       # vertical gap between instance cards
    card_top: 10      # space between subnet label and first card
```

## Risks / Trade-offs

- [Grid refactor scope] → Changing `cell_height` to variable row heights touches `cell_position` and `bounds`. The change is localized to Grid internals but must be carefully tested.
- [Symbol import generalization] → Currently hardcoded to one file. Needs to become a list. Low risk, additive change.
- [Column width interaction] → Instance names/types might be wider than the subnet label. Column width calculation should consider instance content too.
