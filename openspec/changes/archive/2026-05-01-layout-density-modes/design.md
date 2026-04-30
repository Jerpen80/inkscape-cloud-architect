## Context

The extension's layout values were originally tuned for compact output. Comparing with the hand-crafted reference template reveals spacing is 3-10x smaller. Template measurements (converted from mm to px at 96 DPI):

| Spacing | Template (px) | Current (px) |
|---------|--------------|-------------|
| Account padding top | 273 | 50 |
| Account padding left/right | 133 | 20 |
| Account padding bottom | 66 | 20 |
| VPC padding left | 42 | 15 |
| Subnet col_gap (via AZ gap) | 233 | 26 |
| Subnet min_width | 244 | 120 |
| Subnet height | 276 | 50 |

All renderers already read from `config["layout"]` — no renderer code needs changing. Only the config structure and startup resolution need work.

## Goals / Non-Goals

**Goals:**
- Two layout presets: "spaced" (template-scale) and "dense" (current values)
- Default to "spaced" for presentation-quality output
- User selects via INX dropdown, just like theme
- Zero renderer changes

**Non-Goals:**
- Continuous density slider or per-value scaling
- Responsive/auto-scaling based on content volume
- Custom named presets beyond spaced/dense

## Decisions

### 1. Config structure: mode + two complete presets

```yaml
layout:
  mode: spaced
  spaced:
    account:
      padding: { top: 270, right: 130, bottom: 65, left: 130 }
    vpc:
      padding: { top: 100, right: 40, bottom: 40, left: 40 }
      gap: 50
    subnet:
      min_width: 240
      height: 120
      col_gap: 30
      row_gap: 30
    ec2:
      icon_scale: 0.5
      font_size: 13
      card_gap: 15
      card_top: 15
    # ... all other sections
  dense:
    account:
      padding: { top: 50, right: 20, bottom: 20, left: 20 }
    # ... current values
```

Each preset is a complete, self-contained set of layout values. This avoids inheritance complexity — you can read either preset independently and know exactly what you get.

**Alternative considered**: Multiplier-based approach (dense = 1.0x, spaced = 2.5x). Rejected because different spacings need different ratios — account padding needs 5x but subnet height needs 2.5x. Explicit values are more predictable.

### 2. Resolution: merge selected preset into config["layout"]

At startup, after loading config:
1. Read `config["layout"]["mode"]` (default: "spaced")
2. Override with `--layout_mode` INX parameter if provided
3. Copy `config["layout"][mode]` values into `config["layout"]` top-level
4. Remove `spaced`, `dense`, and `mode` keys from `config["layout"]`

After resolution, `config["layout"]` looks exactly like today — renderers see no difference.

### 3. Spaced preset values (rounded from template measurements)

Spaced values are derived from template measurements, rounded for clean numbers. Not exact pixel-for-pixel match — the template has fixed content while our diagrams scale with data.

Key increases from dense:

| Value | Dense | Spaced | Notes |
|-------|-------|--------|-------|
| account.padding.top | 50 | 270 | Room for account label |
| account.padding.left/right | 20 | 130 | Breathing room |
| account.padding.bottom | 20 | 65 | |
| vpc.padding.top | 60 | 100 | More room above subnets |
| vpc.padding.right/left | 15 | 40 | |
| vpc.padding.bottom | 15 | 40 | |
| vpc.gap | 25 | 50 | Between stacked VPCs |
| subnet.min_width | 120 | 240 | Wider columns |
| subnet.height | 50 | 120 | Taller subnet boxes |
| subnet.col_gap | 10 | 30 | Between AZ columns |
| subnet.row_gap | 15 | 30 | Between subnet rows |
| ec2.card_gap | 8 | 15 | Between instance cards |
| ec2.card_top | 10 | 15 | Top margin in subnet |
| region.padding.top | 100 | 150 | |
| region.padding.right/left/bottom | 30 | 60 | |
| region.gap | 20 | 40 | Between regions |
| availability_zone.padding.top | 50 | 70 | |
| availability_zone.padding.bottom | 40 | 50 | |
| availability_zone.padding.sides | 8 | 15 | |
| edge.bottom_spacing | 20 | 40 | |

In dense mode, resource icons use `icon_scale: 0.5` (20px) and `font_size: 13`. In spaced mode, icons use `icon_scale: 1.0` (full 40px) and `font_size: 17` (matching the container label size) for all resource cards (EC2, RDS, LBs, EKS, Lambda, NAT, S3, DynamoDB, CloudFront, Route 53). This makes resources visually prominent at presentation scale rather than looking tiny inside oversized containers.

### 4. INX parameter mirrors theme pattern

```xml
<param name="layout_mode" type="optiongroup" appearance="combo"
  gui-text="Layout:">
  <option value="spaced">Spaced</option>
  <option value="dense">Dense</option>
</param>
```

### 5. User config overrides apply after mode resolution

User overrides in `~/.config/inkscape/extensions/aws-auto-diagram/config.yaml` are deep-merged last, over the resolved mode values. So a user can pick "spaced" and then override just `layout.subnet.min_width: 180` to narrow subnets.

## Risks / Trade-offs

- [Large diagrams in spaced mode] → Accounts with many VPCs/subnets will produce very large SVGs. Acceptable — that's the point. Dense mode is the escape valve.
- [Config file size doubles] → Two complete presets roughly double the layout config. Acceptable — it's readable and explicit.
- [Template values are approximate] → The template has fixed 2-column content; our diagrams vary. The spaced values are starting points, not pixel-perfect matches.
