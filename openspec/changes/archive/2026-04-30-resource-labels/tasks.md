# Tasks: Fix resource labels

## Tasks

- [x] Create `ica_utils/text_utils.py` — font discovery via `fc-match` with fallback, Pillow-based per-char metrics generation, JSON caching, `estimate_text_width()` and `get_font_height()` API
- [x] Update `ica_utils/layout.py` — Grid accepts `col_widths` as list or int, `cell_position` and `bounds` handle variable widths
- [x] Update `ica_utils/resource_vpc.py` — font size to 13pt, label positioned inside container, column widths computed from label measurements via text_utils
- [x] Update `aws_rect` label positioning — icon + text inside the rect with proper padding
- [x] Ensure `pillow` is in flake.nix withPackages
- [x] Test headless run — verify labels fit inside containers, no overlaps, VPC rect auto-sizes to widest column
- [x] Fix pt→px unit mismatch in text_utils — Pillow measures at px, SVG renders at pt (1pt = 1.333px)
- [x] Fix grid row overlap — one row per unique subnet instead of public/private grouping
- [x] Re-test headless run against us-east-2 (multi-VPC, multi-subnet-per-AZ) — no overlaps, labels fit
