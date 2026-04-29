## 1. Config & Symbols

- [x] 1.1 Add `layout.s3` section to `default-config.yaml` with icon_scale, font_size, card_gap, card_padding
- [x] 1.2 Add `AWS-Resource-storage-light.svg` to `SYMBOL_FILES` in `aws-auto-diagram.py`

## 2. Parser

- [x] 2.1 Add `parse_global_services(data_dir)` function to `cloudia_parser.py` that scans region dirs for `s3-list-buckets.json` and returns `{"s3_buckets": [...]}`
- [x] 2.2 Update `parse_all_regions()` to call `parse_global_services()` and prepend a `("Global", global_data)` entry when data exists

## 3. S3 Rendering

- [x] 3.1 Create `resource_s3.py` with `render_buckets()` function that renders icon+name cards stacked vertically, returns (width, height)

## 4. Integration

- [x] 4.1 Add "S3" layer to `_create_layers()` in z-order after "Load Balancers"
- [x] 4.2 Update `_render_multi_region()` to detect Global vs real region entries and dispatch to S3 renderer for Global

## 5. Verification

- [x] 5.1 Run headless test with `--region=all` and confirm Global region with S3 buckets renders
- [x] 5.2 Run headless test with single region and confirm no Global region appears
