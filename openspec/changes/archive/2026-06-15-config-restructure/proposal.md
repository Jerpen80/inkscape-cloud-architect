## Why

ICA's configuration has **three disagreeing sources of default values**: the YAML
`spaced` preset, the YAML `dense` preset, and hundreds of inline
`config.get(key, fallback)` calls in `resource_*.py` (e.g. `resource_region`
falls back to `region.gap=20` while the shipped `spaced` value is `40`). The
fallbacks are effectively dead (the resolver always populates the keys), but they
are drift waiting to happen. Separately, **18 of the 101 layout keys are identical
across `spaced`/`dense`** — they are misfiled *style* (stroke colors, dash
patterns, span-line styles, `availability_zone.enabled`, `label_prefix`), not
density knobs, and live in both presets only because the preset structure forced
all-or-nothing duplication.

This change collapses the three sources into one, fixes the misfiled style keys,
and is made safe by the just-shipped config schema + synthetic fixture: a
byte-exact golden render guards every step.

Bean: [inkscape-cloud-architect-z23q](../../../.beans/inkscape-cloud-architect-z23q--90-config-restructure-single-source-of-truth-debt.md)
(epic [muex](../../../.beans/inkscape-cloud-architect-muex--we-need-a-wrapper-which-is-userfriendly.md);
deferred debt, unblocked now that config-schema and the synthetic fixture exist.)

## What Changes

- **Defaults = spaced (canonical), dense = diff.** Restructure `default-config.yaml` so the canonical layout values live once; the `dense` preset becomes an overlay listing only the **83** keys that genuinely differ. `resolve_layout_mode` applies the dense overlay on top of the canonical values when `mode=dense`.
- **Promote the 18 style keys out of the presets.** Keys identical across `spaced`/`dense` (stroke colors, dash patterns, span-line styles, `availability_zone.enabled`, `label_prefix`) move to a non-preset location so they are defined once and are not density-dependent.
- **Remove the inline `config.get(key, fallback)` shadow defaults** from `resource_*.py` / `legend.py` where the resolver guarantees the key is present, so the YAML is the single source of truth. (Verified: these fallbacks do not currently fire — the resolver always populates the keys.)
- **Byte-exact golden guard.** Capture a golden SVG from the synthetic fixture (single + multi region) **before** the refactor; assert byte-identical output after every step. Rendered output MUST NOT change.

### Non-goals
- No new config keys, no behavior/UX change, no schema metadata change (the schema already describes the flattened engine-form keys; only the YAML *layout* changes, not the resolved shape the schema/engine see).
- No layout/visual change of any kind — byte-identical is the hard requirement.

## Capabilities

### Modified Capabilities
- `config-loading`: the default config's internal structure changes (canonical defaults + dense-as-diff overlay; style keys no longer preset-scoped) and the resolver applies the dense overlay. The *resolved* config shape (flattened `layout.*`) and all values are unchanged.

## Impact

- **Modified**: `extensions/aws-auto-diagram/default-config.yaml` (restructured), `ica_utils/config.py` (`resolve_layout_mode` applies dense-as-diff + style keys), and `resource_*.py` / `legend.py` (drop now-redundant inline fallbacks).
- **Unchanged behavior**: every rendered SVG is byte-identical (guarded by the fixture golden).
- **Schema**: `config_schema` should still pass coverage (the flattened key inventory is unchanged); confirm `test_config_schema` stays green.
- **Tests**: a byte-exact golden test (from the synthetic fixture) added for this change; `test_all` stays green.
- **Inkscape extension**: behavior unchanged (it reads the same resolved config).
