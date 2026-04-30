# Tasks: Plot availability zones

## Tasks

- [x] Add `availability_zones` section to `default-config.yaml`
- [x] Create `ica_utils/resource_az.py` — `render_az_columns` draws dashed rects and labels to AZ layer
- [x] Update `aws-auto-diagram.py` — pre-create "Availability Zones" layer between VPCs and Subnets, pass config to renderer
- [x] Update `resource_vpc.py` — compute col_gap and VPC_PADDING_TOP from config when AZs enabled, call `render_az_columns`
- [x] Test headless run — dashed AZ rects inside VPCs, correct layer order (VPCs → AZs → Subnets), labels present
- [x] Test with `availability_zones.enabled: false` — no AZ layer or rects confirmed
