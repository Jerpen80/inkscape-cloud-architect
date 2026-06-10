## Why

ICA's real configuration surface is large: `default-config.yaml` holds ~120 distinct
describable keys (1 `document`, 18 `theme`, 101 `layout`), but only **5** of them are
reachable through the `.inx`/CLI front door (`theme, layout_mode, account_name,
data_dir, region`). Every other knob is only reachable by hand-authoring YAML at a path
the user must already know (`~/.config/inkscape/extensions/aws-auto-diagram/config.yaml`).

For the planned user-friendly `ica` wrapper (bean
[inkscape-cloud-architect-muex](../../../.beans/inkscape-cloud-architect-muex--we-need-a-wrapper-which-is-userfriendly.md))
to expose this surface as a CLI **and** a TUI, both front-ends need a single,
machine-readable description of what every key is: its type, valid range, unit, and a
human-readable help string. Today that information does not exist anywhere — it is
implied by `default-config.yaml` values and scattered across ~90 inline
`config.get(key, fallback)` calls in the rendering modules (a shadow schema that is
already drifting from the YAML; e.g. `resource_ec2.py` defaults `icon_scale` to `0.5`
while the shipped `spaced` preset uses `1.0`).

This change is the **keystone** for the front-end: a config **schema** that makes the
full option surface discoverable and validatable. It is deliberately **describe-only** —
it adds a metadata layer beside the existing config and does **not** change engine
behavior, `default-config.yaml`, or any rendered SVG output.

## What Changes

- Add a Python **schema descriptor** (`ica_utils/config_schema.py`) declaring, for every
  config key, **metadata only** — `type`, `range`/`enum`, `unit`, `help`, and a derived
  `preset_varying` flag. The schema does **NOT** carry default values.
- Add a **schema loader** that joins the descriptor with the **unchanged**
  `default-config.yaml`: it discovers the key inventory and reads default values *from the
  YAML*, so defaults have exactly one source of truth and key existence cannot drift.
- Key paths in the schema use the **engine (flattened) form** (`layout.ec2.icon_scale`),
  not the raw preset form (`layout.spaced.ec2.icon_scale`). For the 83 `layout` keys whose
  values differ between `spaced` and `dense`, the schema marks `preset_varying=True` and
  the loader can surface both preset values; the other 37 keys have a single value.
- Add a **validation** function: given a user override dict, validate every key against
  the schema (unknown key, wrong type, out-of-range, bad enum) and return clear,
  per-key error messages.
- Add a **coverage self-check**: every key present in `default-config.yaml` MUST have a
  schema entry, and every schema entry MUST correspond to a real key. Mismatches are
  reported (used in tests, not at render time).

### Explicitly out of scope (deferred)

- No change to `default-config.yaml`, the `spaced`/`dense` preset structure, or the
  18 misfiled style keys that are identical across presets (documented debt; a future
  restructure change).
- No removal of the inline `config.get(key, fallback)` fallbacks in rendering modules.
- No CLI/TUI implementation, no `ica` command — this change only produces the schema the
  front-end will consume.
- No changes to rendering, parsing, or any SVG output. Byte-identical output is a
  requirement, not a goal.

## Capabilities

### Modified Capabilities
- `config-loading`: gains a schema descriptor, a schema loader that joins metadata with
  YAML-sourced defaults, override validation, and a coverage self-check.

## Impact

- **New file**: `extensions/aws-auto-diagram/ica_utils/config_schema.py`
- **New tests**: schema coverage (schema ↔ YAML key parity), validation behavior.
- **Engine**: unchanged. `aws-auto-diagram.py`, `config.py` `load_config`/
  `resolve_layout_mode`, and all `resource_*.py` modules are not modified. Rendered SVGs
  are byte-identical.
- **Consumers (future)**: the `ica` CLI `--help`, TUI forms, and override validation all
  read from this one schema.

Bean: [inkscape-cloud-architect-muex](../../../.beans/inkscape-cloud-architect-muex--we-need-a-wrapper-which-is-userfriendly.md)
(this change is the first stage — the config-schema keystone — of the larger
user-friendly `ica` wrapper epic.)
