## Context

`default-config.yaml` stores `layout.spaced` and `layout.dense` as two full
~101-key value sets. `resolve_layout_mode(config, mode)` picks one, flattens it
into `layout.*`, and deletes `mode/spaced/dense`. Downstream, `config_schema`
calls `resolve_layout_mode(c, "spaced")` and `(c, "dense")` to derive the key
inventory + `preset_varying`; the engine reads only the flattened `layout.*`.

Three problems (verified this session):
1. spaced/dense duplicate ~101 keys; **83 differ, 18 are identical** (misfiled style).
2. ~hundreds of inline `config.get(k, fallback)` in `resource_*.py` — a third
   default source. Verified effectively **dead** (the resolver always populates
   the keys; fallbacks don't fire).
3. No single source of truth → drift risk.

## Goals / Non-Goals

**Goals:** one canonical default set; dense as a diff; style keys defined once;
inline fallbacks removed; **byte-identical** rendered output.

**Non-Goals:** new keys, behavior/UX/visual change, schema metadata change, or any
change to the *resolved* `layout.*` shape the schema/engine consume.

## Decisions

### D1. The load-bearing invariant
`config_schema` and the engine depend on `resolve_layout_mode(c, mode)` producing
the **same flattened `layout.*` keys and values** as today, for both modes. The
restructure changes how the YAML *stores* defaults and how the resolver *assembles*
them — but the resolver's OUTPUT must be identical. This invariant is what keeps
the schema, the engine, and rendered output unchanged.

### D2. Canonical + dense-diff layout
```
  layout:
    mode: spaced
    style:            # the 18 preset-invariant keys, defined once
      eks: { span_line_color: "#FF9900", span_line_width: 1.0, span_line_dasharray: "4,4" }
      asg: { stroke_color: "#ED7100", ... }
      availability_zone: { enabled: true, label_prefix: "" }
      ...
    spaced:           # canonical density values (the 83 differing keys)
      ec2: { icon_scale: 1.0, font_size: 17, ... }
      ...
    dense:            # ONLY the 83 keys, with dense values (the diff)
      ec2: { icon_scale: 0.5, font_size: 13, ... }
      ...
```
`resolve_layout_mode` assembles: start from `style` + `spaced`, then if
`mode=dense` overlay the `dense` diff. Result flattened into `layout.*` exactly as
today.

*Exact placement of the 18 style keys (a `layout.style` block vs merging into
`spaced` and dropping from `dense`) is an implementation choice — D1 is the
constraint either way.* The simplest variant that satisfies D1: keep `spaced` as
the full canonical set (including the 18), make `dense` list only the 83 diffs;
the "promote style keys" goal is then realized by dense no longer duplicating
them. Decide the cleanest form during apply; the golden test arbitrates.

### D3. Remove inline fallbacks only where the resolver guarantees the key
For each `config.get(k, fallback)` in the resource modules: if the resolved config
always contains `k` (true for layout keys post-resolve), drop the fallback. Where a
key is genuinely optional (e.g. an absent global section), keep the guard. The
golden test catches any wrong call.

### D4. Byte-exact golden guard (per the scope decision)
Before any edit: render the synthetic fixture (single `eu-west-1` + `region=all`)
and commit the exact SVG as a golden. After each refactor step, assert
byte-identical. This is stricter than the existing structural `test_render_fixture`
and is the safety net that makes "all three at once" acceptable.

## Risks / Trade-offs

- **Resolver assembly subtly changes a value/key** → golden test fails immediately;
  fix before proceeding. This is the whole point of D4.
- **A removed fallback DID matter for an edge case the fixture doesn't cover** →
  the fixture is comprehensive (every renderer), but a value-specific edge (e.g. a
  missing optional key) could slip. Mitigation: only remove fallbacks for keys the
  resolver provably populates (D3); keep optional-section guards.
- **Schema coverage breaks** → `config_schema` derives keys via `resolve_layout_mode`;
  if the resolved key set is identical (D1) coverage is unchanged. Confirm
  `test_config_schema` green after.
- **`preset_varying` derivation** reads spaced vs dense resolved values; since both
  resolve to the same values as today, the 83/18 split is preserved.

## Migration Plan
1. Capture the byte-exact golden(s) from the synthetic fixture (pre-change).
2. Restructure `default-config.yaml` (D2) + `resolve_layout_mode` (D1/D2). Assert golden.
3. Remove inline fallbacks (D3) in batches per module. Assert golden after each.
4. Run `test_all` (incl. `test_config_schema`, `test_render_fixture`) + the new golden test.

Rollback: revert the YAML + config.py + resource edits; no data/state migration.

## Open Questions
- `layout.style` block vs spaced-as-canonical-superset — pick the form that keeps resolve simplest while satisfying D1 (resolve during apply).
- Whether to keep the byte-exact golden committed long-term or only for this change (lean: keep it as a regression guard for future config work).
