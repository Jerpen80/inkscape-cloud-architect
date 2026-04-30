## 1. Config

- [x] 1.1 Add `layout.dynamodb` section to `default-config.yaml` with icon_scale, font_size, card_gap, card_padding

## 2. Parser

- [x] 2.1 Add DynamoDB table parsing to `parse_region()` — read `dynamodb-list-tables.json`, return table list
- [x] 2.2 Thread `dynamodb_tables` through `parse_all_regions()` region tuples

## 3. DynamoDB Rendering

- [x] 3.1 Create `resource_dynamodb.py` with `render_tables()` function (icon+name cards, returns width/height)

## 4. Integration

- [x] 4.1 Add "DynamoDB" layer to `_create_layers()` after "S3"
- [x] 4.2 Update `_render_multi_region()` to render DynamoDB tables below VPCs inside each region rect
- [x] 4.3 Update `_render_single_region()` to render DynamoDB tables below VPCs

## 5. Verification

- [x] 5.1 Run headless test with account 222222222222 us-east-2 — confirm 2 DynamoDB tables render
- [x] 5.2 Run headless test with account 222222222222 eu-west-1 — confirm no DynamoDB (no crash)
