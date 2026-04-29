## Context

The extension currently renders VPCs and subnets with all spacing values hardcoded as module-level constants in `resource_vpc.py`. The config system (`default-config.yaml` + user override merge) exists but only holds `document.margin`. There is no account-level visual grouping.

The symbol `cloud.svg` exists in `AWS-Group-light.svg` and can be referenced as `AWS-Group-light.svg:cloud.svg`.

## Goals / Non-Goals

**Goals:**
- Render an optional account boundary rectangle around all resources
- Make all layout spacing values configurable via the existing YAML config system
- Maintain visual consistency with existing rendering patterns

**Non-Goals:**
- Multi-account support (one account rect per diagram for now)
- Multi-region rendering (separate task)
- Reading account metadata from AWS data files

## Decisions

### 1. Account rect uses bounding-box approach

Render all VPCs first, then compute the bounding box of rendered content and draw the account rect around it with padding.

**Alternative considered**: Pre-calculate total size from grid math. Rejected because the bounding-box approach is simpler, already proven by `resize_to_fit`, and handles edge cases (e.g., labels extending beyond rects).

### 2. Account name comes from INX argument, not data

The `account_name` is an optional text parameter in the INX file. When empty, no account rect is rendered.

**Rationale**: AWS API data doesn't include account-friendly names in the ec2-describe output. The user knows what to call their account.

### 3. Config organized by resource type

```yaml
layout:
  account:
    padding: { top: 50, right: 20, bottom: 20, left: 20 }
  vpc:
    padding: { top: 50, right: 15, bottom: 15, left: 15 }
    gap: 25
  subnet:
    min_width: 120
    height: 50
    col_gap: 10
    row_gap: 15
```

**Alternative considered**: Flat namespace (`vpc_padding_top`, `subnet_col_gap`). Rejected because nested structure matches the code's module organization and the deep-merge config system handles partial overrides naturally.

### 4. Account layer below VPCs in z-order

Layer creation order: Accounts → VPCs → Subnets (bottom to top). The account rect is a background container.

### 5. Account rect style: black stroke

Uses `#000000` stroke with the same `aws_rect` rendering pattern (0.5 stroke-width, no fill, icon + label).

### 6. Stack origin offset when account is present

When `account_name` is provided, the Stack's starting position shifts by the account padding so VPCs render inside the account boundary:

```
account_x, account_y = document_origin
stack_x = account_x + account.padding.left
stack_y = account_y + account.padding.top
```

When no account name is set, the Stack starts at the document origin as before.

### 7. Config passed to rendering functions

`resource_vpc.py` functions accept a `config` dict parameter instead of reading module-level constants. The main `effect()` method reads config once and passes it through.

## Risks / Trade-offs

- **Bounding box requires rendered content** → Account rect must be drawn after VPCs. This means the account layer is created first (for z-order) but populated last. Minor ordering complexity.
- **Config key typos fail silently** → A misspelled config key falls back to the default via deep-merge. Acceptable for a user-facing config; wrong padding is better than a crash.
