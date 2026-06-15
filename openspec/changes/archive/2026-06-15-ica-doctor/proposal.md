## Why

`ica render` and the Inkscape dialog both depend on assets installed in the
Inkscape user directory (symbols, templates) — installed by `ica setup`. When that
install is missing or partial, `ica render` produces a near-empty diagram (the
symbols don't resolve) with no clear explanation, and a GUI user gets a broken
dialog. There is no way to *check* whether the environment is healthy or to tell
the user how to fix it. This change adds `ica doctor`: a health check that verifies
the install and, when something is wrong, says exactly what to run.

Bean: [inkscape-cloud-architect-wkj7](../../../.beans/inkscape-cloud-architect-wkj7--35-ica-doctor-setup-inkscape-env-health-install.md)
(epic [muex](../../../.beans/inkscape-cloud-architect-muex--we-need-a-wrapper-which-is-userfriendly.md);
narrowed to **doctor-only** — `ica setup` already shipped in the nix-package change.)

## What Changes

- Add an `ica doctor` subcommand that checks the environment and reports a clear, per-item status:
  - **inkex importable** (the render engine's hard dependency).
  - **symbols present** — the 6 SVGs the engine loads exist under the resolved symbol directory (`resolve_symbol_dir`: explicit → config → `$INKSCAPE_DIR/symbols/aws-architect/`).
  - **templates present** — `$INKSCAPE_DIR/templates/aws-architect/` exists (for GUI users).
  - **extension present** — `$INKSCAPE_DIR/extensions/aws-auto-diagram/` exists (for the GUI dialog) — reported as informational, since the headless CLI does not require it.
- For each failing check, print a specific remedy (e.g. "run `ica setup` to install symbols + templates"; "enter the `nix develop` shell" if inkex is missing).
- Exit non-zero if any **required** check fails (inkex, symbols), zero otherwise; GUI-only items (templates, extension) are warnings, not failures, for headless use.

### Non-goals
- No `ica setup` (already shipped). No auto-fix/auto-install from doctor — it *reports and instructs* (offering to run setup could be a later enhancement).
- No change to render/engine/config behavior.

## Capabilities

### Modified Capabilities
- `environment-setup`: add a health-check (`ica doctor`) alongside the existing `ica setup`, verifying the install setup produces and guiding the user to fix a broken/partial environment.

## Impact

- **New**: an `ica doctor` subcommand in `ica_cli.py`, reusing existing helpers (`_inkscape_dir`, `engine.resolve_symbol_dir`, `engine.SYMBOL_FILES`).
- **New tests**: `test_ica_doctor` (no-pytest, self-checking) exercising healthy vs missing-symbols vs missing-inkex outcomes via a temp `$INKSCAPE_DIR`, wired into `test_all`.
- **Engine (small bugfix added during apply)**: `engine.default_symbol_dir()` hardcoded `~/.config/inkscape` (ignored `$INKSCAPE_DIR`, wrong on macOS) while `ica setup` installs to the resolved Inkscape dir — they diverged on macOS / with an override. Added `engine.inkscape_dir()` (honors `$INKSCAPE_DIR` + macOS) and routed the symbol-dir default + `ica_cli._inkscape_dir()` through it, so setup/render/doctor agree. Rendered output is byte-identical (golden-verified; Linux-default resolves unchanged).
- **Unchanged**: render behavior, config, `ica setup` logic, the Inkscape extension (`.py`/`.inx`).
