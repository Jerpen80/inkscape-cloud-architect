# Tasks: Resource layers

## Tasks

- [x] Create `ica_utils/layers.py` with `get_or_create_layer(inkdoc, name)` utility
- [x] Update `aws_rect` to accept a `layer` parameter and append elements to it
- [x] Update `render_vpc_with_subnets` to create VPCs and Subnets layers, pass to aws_rect
- [x] Pre-create layers in z-order in `effect()` (VPCs first, Subnets second)
- [x] Test headless run — VPCs layer (6 children), Subnets layer (27 children), correct z-order
