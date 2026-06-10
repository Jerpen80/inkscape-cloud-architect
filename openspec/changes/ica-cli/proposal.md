## Why

ICA's full capability now exists as importable Python — a headless `render()`
engine (no Inkscape runtime) and a config schema describing all ~120 keys — but
there is no user-facing command. Co-workers cannot install one tool and produce
a diagram. This change adds `ica`, a professional CLI that drives the existing
engine and schema, installable via the flake so that after install `ica` just
works.

Bean: [inkscape-cloud-architect-brhe](../../../.beans/inkscape-cloud-architect-brhe--20-ica-cli-skeleton-render-config-subcommands.md)
(epic [muex](../../../.beans/inkscape-cloud-architect-muex--we-need-a-wrapper-which-is-userfriendly.md);
depends on the completed thin-seam engine and config-schema; ships in v1.2.0.)

## What Changes

- Add the `ica` command (Typer-based) with shell completion, `--version`, `--help`, and verbosity.
- `ica render <data_dir> <region>` — calls `engine.render()` natively (no subprocess). Flags: `--theme`, `--layout-mode`, `--account-name`, and:
  - `-o <file>` is **required** (no implicit stdout). `-o -` opts into stdout explicitly. This prevents accidentally dumping customer-data SVG into a terminal or a redirect into the repo.
  - `--config <file.yaml>` — feed a persistent override file (for testing and alternative styles).
  - `--set <dotted.key>=<value>` — repeatable inline overrides (e.g. `--set layout.ec2.icon_scale=0.8 --set theme=dark`).
  - Config merge order: `default-config.yaml` ◄ `--config` ◄ `--set` (later wins).
  - `--set` values arrive as strings and are coerced to their schema type (int/float/bool/color/enum) using the schema's `Field` metadata.
  - The merged config is validated against the schema **before** rendering; an unknown key, wrong type, out-of-range value, or invalid enum fails fast with a clear per-key message and a non-zero exit — no diagram is produced.
- `ica initconf [-o <path>]` — scaffold a curated starter config (theme, layout_mode, and a few common knobs) with sane defaults sourced from the schema, plus a comment pointing at the full key set. Output is consumed by `ica render --config`.
- Package `ica`'s dependencies (Typer, Click) into the flake `pythonEnv`. (Bundling symbols + wiring the installable entry point is bean 30; this change is the CLI behavior.)

### Non-goals (deferred)
- No `ica doctor` / `ica setup` (Inkscape env health + install) — split into [bean wkj7](../../../.beans/inkscape-cloud-architect-wkj7--35-ica-doctor-setup-inkscape-env-health-install.md).
- No TUI (bean 60). No `ica pull` (bean 50).
- No code relocation: `ica` imports `ica_utils` in place from `extensions/aws-auto-diagram/`. The Inkscape dialog path is unchanged.
- No per-option config CLI flags (the original bean idea); `--set`/`--config`/`initconf` replace that.

## Capabilities

### New Capabilities
- `ica-cli`: The `ica` command — `render` (with layered, validated, type-coerced config overrides) and `initconf`, plus global CLI behavior (version, help, verbosity, completion, required-output safety).

### Modified Capabilities
- `config-loading`: add a layered-override + validation contract the CLI relies on — load an arbitrary override file and/or inline dotted-key overrides, deep-merge over defaults, coerce inline string values to schema types, and validate the merged result before use.

## Impact

- **New**: an `ica` entry-point module (e.g. `extensions/aws-auto-diagram/ica_cli.py` or an `ica/` package) wiring Typer → `engine.render()` + `config_schema`.
- **New deps**: `typer`, `click` added to the flake `pythonEnv`.
- **Reused as-is**: `engine.render()`, `config_schema.{load_schema,validate_override}`, `config.load_config`. The engine and schema are not modified; the layered-merge/coerce logic is new CLI-side code built on the schema.
- **Unchanged**: the Inkscape extension (`aws-auto-diagram.py`, `.inx`) and all `resource_*` — the dialog keeps working; `ica_utils` stays beside the `.py`.
- **Leak-safety**: required `-o`; never default output into the repo tree.
