# Design: Config schema (describe-only keystone)

## The problem in one picture

```
   THREE sources of "the default value" for every layout key, and they DISAGREE:

   ┌────────────────────────┬───────────────┬─────────────────────────┐
   │ Source                 │ ec2.icon_scale │ Used when...            │
   ├────────────────────────┼───────────────┼─────────────────────────┤
   │ YAML spaced preset     │     1.0        │ normal operation        │
   │ YAML dense preset      │     0.5        │ --layout_mode=dense     │
   │ hardcoded .get() default│    0.5        │ key missing from YAML   │
   └────────────────────────┴───────────────┴─────────────────────────┘

   There is no single place that answers "what keys exist, what type are they,
   what range is valid, what does this knob do?" — the front-end needs exactly that.
```

## Core decision: the schema carries metadata, NOT defaults

Because this change is **describe-only**, the engine's defaults must stay where they are
(`default-config.yaml` + inline fallbacks). If the schema *also* declared defaults, we would
re-create the multi-source problem we are trying to escape. So:

```
   ┌─────────────────────────┐         ┌──────────────────────────┐
   │  default-config.yaml     │         │  config_schema.py         │
   │  SOURCE of defaults &    │◄────────│  per key, METADATA ONLY:  │
   │  key inventory (UNCHANGED)│ loader  │   - type (int/float/color │
   │                          │ reads   │            /enum/str)     │
   │  engine reads this as-is │ defaults│   - range / enum          │
   └─────────────────────────┘  from it │   - unit (px, scale, ...) │
                                         │   - help (one line)       │
                                         │   - preset_varying (bool) │
                                         └──────────────────────────┘
              join at load time
                     ▼
        ┌──────────────────────────────┐
        │  resolved schema object:      │
        │  key → {value(s), type,       │
        │         range, unit, help,    │
        │         preset_varying}       │
        └──────────────────────────────┘
            │           │            │
            ▼           ▼            ▼
       CLI --help   TUI forms   validate(user_override)
```

The schema **discovers** the key inventory from the YAML at load time, so a key can never
be *missing* from the inventory. Only the hand-authored metadata can be incomplete — and
that is caught by the coverage self-check.

## Key-path form: engine (flat), not raw preset

The YAML stores layout values twice, under `layout.spaced.*` and `layout.dense.*`. The
engine never sees that nesting — `resolve_layout_mode()` flattens the chosen preset into
`layout.*` and deletes `mode/spaced/dense`. Therefore:

```
   YAML stores:   layout.spaced.ec2.icon_scale = 1.0
                  layout.dense.ec2.icon_scale  = 0.5
   Engine reads:  layout.ec2.icon_scale            (after resolve)

   Schema key:    'layout.ec2.icon_scale'          (engine/flat form)
```

The schema's key inventory uses the **flat** form (what the engine and a user override
actually address). The loader sources the default value by reading the chosen preset out
of the YAML.

## Preset-varying keys (measured, not guessed)

Of the 101 `layout` keys (per preset):

```
   ┌─────────────────────────────────────────────────────────────┐
   │  83 keys DIFFER between spaced and dense  → real density knobs │
   │     (sizes, gaps, paddings, font sizes, icon scales)          │
   │  18 keys are IDENTICAL in both presets    → misfiled style    │
   │     (stroke colors, dash patterns, span-line styles,          │
   │      availability_zone.enabled, label_prefix)                 │
   └─────────────────────────────────────────────────────────────┘
```

`preset_varying` is **derived** by comparing the two presets in the YAML, not hand-set.
For a `preset_varying=True` key the schema exposes both preset values so the front-end can
present an honest default (e.g. `ec2.icon_scale: 1.0 (spaced) / 0.5 (dense)`). The 18
identical keys collapse to a single value. This *describes* the preset structure without
*restructuring* it (restructure is a deferred follow-up), and leaves a clean breadcrumb:
the schema already knows which keys are true density knobs.

## Field metadata form

A plain Python descriptor (not Pydantic — Pydantic shines when it *becomes* the source of
defaults, which describe-only forbids). Type-checkable, no extra runtime dep, integrates
directly with Typer/Textual later.

```python
# config_schema.py  (illustrative)
FIELDS = {
    'document.margin':       Field(int,   range=(0, 200), unit='px',
                                    help='Whitespace margin around the whole diagram'),
    'layout.ec2.icon_scale': Field(float, range=(0.1, 3.0), unit='scale',
                                    help='Scale factor applied to the EC2 symbol'),
    'layout.ec2.font_size':  Field(int,   range=(6, 72), unit='px',
                                    help='EC2 instance label font size'),
    'theme.light.border_vpc':Field(color, help='VPC rectangle border color (light theme)'),
    # ... ~120 entries ...
}
```

`Field` is a small dataclass: `type`, optional `range`, optional `enum`, optional `unit`,
required `help`. `preset_varying` is computed by the loader, not stored on the Field.

Color/enum are validated by helper predicates (e.g. `color` = `#RRGGBB`/`#RGB`/`none`;
`enum` for `layout.mode` ∈ {spaced, dense}, `theme` ∈ {light, dark}, `region` includes
`all`).

## Validation contract

`validate_override(user_dict) -> list[Error]`:
- **unknown key**: path not in schema → error naming the path.
- **type mismatch**: value not coercible to the field type → error with expected type.
- **out of range / bad enum**: numeric outside `range`, or value not in `enum` → error
  with the allowed bounds/values.
- partial overrides are fine (deep-merge semantics unchanged); only the *provided* keys
  are validated.

Validation is pure (no I/O, no inkex), so the CLI/TUI and tests all call it directly.

## Coverage self-check

`check_coverage() -> (missing_in_schema, extra_in_schema)`:
- walks `default-config.yaml` (resolving each preset to the flat form) → set of real keys.
- compares against schema keys.
- any real key without a Field, or any Field without a real key, is reported.

Run in tests (and optionally `ica config doctor` later). Not invoked during rendering.

## Why this is the keystone, and why nothing else changes

This delivers two of the four front-end pains directly — **discoverability** (full key
inventory with help/units) and **validation** (clear pre-render errors) — and is the
foundation the other two (safe I/O, the account-data puller) build on. Crucially it does
so as a pure *additive metadata layer*: `aws-auto-diagram.py`, `config.py`, and every
`resource_*.py` are untouched, so SVG output is byte-identical. The deferred restructure
(single source of truth, defaults=spaced/dense-as-diff, promote the 18 style keys, drop
inline fallbacks) becomes safe to do *later* precisely because this schema will then exist
to validate it against golden output.
