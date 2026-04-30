## 1. Rewrite ASG Rendering

- [x] 1.1 Rewrite `render_asg_containers` in `resource_asg.py` to draw spanning rects across columns using grid positions and `subnet_to_col` mapping
- [x] 1.2 Compute ASG rect x-span from min_col to max_col using `grid.cell_position` and `grid.col_width`
- [x] 1.3 Compute ASG rect y-position within subnet row: below non-ASG instances, with top_margin

## 2. Update VPC Integration

- [x] 2.1 Update `resource_vpc.py` to pass `grid`, `subnet_to_col`, and `placement` to ASG renderer
- [x] 2.2 Adjust EC2 rendering offset: ASG-grouped instances render at the correct y within the ASG rect area (after label + padding)

## 3. Verify

- [x] 3.1 Run headless with us-east-2 (222222222222) — verified: powerbi ASG rect w=590 spans both columns
- [x] 3.2 Run headless with 111111111111 — verified: long EKS node group ASG names render OK
