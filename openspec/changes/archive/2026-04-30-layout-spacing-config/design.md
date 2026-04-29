## Context

The configuration system (`configuration-yaml` change) is in place. Layout constants are hardcoded in `resource_vpc.py`. The `render_vpc_with_subnets` function already receives `inkdoc` which has `inkdoc.config` available.

## Goals / Non-Goals

**Goals:**
- Make VPC padding, VPC gap, and subnet spacing configurable via `default-config.yaml`
- Remove hardcoded spacing constants from `resource_vpc.py`

**Non-Goals:**
- Configuring colors, font sizes, or icon scale (separate concern, later)
- Adding validation for spacing values

## Decisions

### 1. Nested config structure
Use `vpc.padding.top/sides/bottom`, `vpc.gap`, and `subnet.min_width/height/col_gap/row_gap`. This mirrors the visual hierarchy and works well with the deep-merge override strategy — users can override a single value without repeating the structure.

### 2. Read config via `inkdoc.config` in render functions
`render_vpc_with_subnets` already receives `inkdoc` (the extension instance). Config values are read directly from `inkdoc.config` at the point of use, replacing module-level constant references. No new parameter passing needed.

### 3. VPC_GAP in aws-auto-diagram.py
The Stack creation uses `resource_vpc.VPC_GAP` — this changes to `self.config["vpc"]["gap"]`, removing the import dependency on the constant.

## Risks / Trade-offs

- [Verbosity] → `inkdoc.config["vpc"]["padding"]["top"]` is longer than `VPC_PADDING_TOP`. Acceptable — clarity of source outweighs brevity.
