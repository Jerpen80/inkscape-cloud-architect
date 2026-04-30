# Tasks: Read VPCs and subnets from cloudia-reader-aws output

## Tasks

- [x] Update `.inx` — uncomment param section, add `data_dir` (path/folder) and `region` (optiongroup/combo with all AWS regions) params
- [x] Create `ica_utils/cloudia_parser.py` — `parse_region(data_dir, region)` reads vpc + subnet JSON, returns internal format with name resolution and public/private detection
- [x] Update `resource_vpc.py` — `render_vpc` accepts vpc dict (name, CIDR); `render_subnet` uses `is_public` flag instead of name check
- [x] Update `aws-auto-diagram.py` — wire .inx params via `add_arguments`, replace `parse_test_data` with cloudia parser call in `effect()`
- [x] Remove dead code from `aws-auto-diagram.py` — `rect`, `shape_test`, `remote_json_test`, `this_works`, `doc_symbols`, `parse_test_data`
- [x] Delete `test-data.json`
- [x] Manual test: run extension in Inkscape with CustomerA account-data dir and eu-west-1 region (parser verified against real data outside Inkscape)
