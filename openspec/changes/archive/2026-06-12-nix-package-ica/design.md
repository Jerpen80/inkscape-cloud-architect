## Context

`ica` (Typer app at `extensions/aws-auto-diagram/ica_cli.py`) drives the headless
`engine.render()` + `config_schema`. It works in the devShell but is not
installable. The flake currently exposes only `devShells`.

Two hard facts from explore shape this change:

1. **AWS icon assets are not redistributable.** The symbol build (`build.sh`)
   consumes an AWS icon ZIP downloaded from `aws.amazon.com/architecture/icons/`
   (stable mirror: `d1.awsstatic.com/.../Icon-package_*.zip`). We cannot ship the
   built symbols — the user must obtain them from AWS. → symbols are installed by
   `ica setup`, not bundled.
2. **Hard Inkscape dependency is acceptable.** The app installs into and renders
   against `$INKSCAPE_DIR` (`~/.config/inkscape`). There is no "non-Inkscape user"
   to design around — this removes the earlier "where do symbols live" dilemma.

Constraint carried from the ica-cli change: `ica_utils` must stay beside
`aws-auto-diagram.py` so the Inkscape `.inx` dialog (which puts that dir on
`sys.path`) keeps working. So the package builds the dir **in place**.

## Goals / Non-Goals

**Goals:**
- `nix run .#ica` / `nix profile install` produce an `ica` on PATH.
- `ica setup` takes a fresh machine (with Inkscape) to a working `ica render`.
- Inkscape dialog + extension untouched; `ica_utils` not moved.

**Non-Goals:**
- `ica doctor` / broken-install UX (bean wkj7). Bundling AWS symbols. `ica pull`,
  safe-io. Release/versioning (separate change).

## Decisions

### D1. `buildPythonApplication`, in place
Package `extensions/aws-auto-diagram/` as-is via `buildPythonApplication` with a
`pyproject.toml` that declares the package (`ica_cli` + the `ica_utils` package +
`default-config.yaml` as package data) and a console script `ica = ica_cli:app`.
`propagatedBuildInputs = [inkex lxml tinycss2 pyyaml typer]`.
*Why:* proper entry point + closed dependency closure, without moving code.
*Alternative rejected:* a `makeWrapper` shell shim (cruder, no real metadata).
*Risk:* `inkex` as a standalone `python3Packages.inkex` must resolve in a build
closure — verify during apply (spike).

### D2. Setup-time tools wrapped onto PATH
`ica setup` shells out to the symbol build, which needs `git`, `rsync`, `unzip`,
`python3`, and a fetcher (`curl`/nix `fetchurl` is build-time only, so runtime uses
`curl`). Wrap these onto the `ica` binary's PATH via `makeWrapper`
(`--prefix PATH`). The render path needs none of them.

### D3. ZIP resolution chain (in `ica setup`)
First available wins:
1. `--asset-zip <path>` — a local ZIP the user downloaded from AWS.
2. download the AWS icon package from the `d1.awsstatic.com` URL. The URL is
   dated+hashed and rotates, so it is **config-overridable**
   (`symbols.asset_zip_url`) — update it without a code release.
3. fallback: the `Asset-Package_*.zip` committed in the repo (last resort, offline).
*Why:* resilient to URL rot, offline-capable, and the user always obtains the
icons "from AWS" (we never redistribute the built output).

### D4. awslabs group icons (the non-ZIP half)
`build.sh` also clones `awslabs/aws-icons-for-plantuml` at a pinned MIT rev for the
Group icons. Decide during apply: vendor it as a flake input (pure, no runtime
clone) vs. runtime `git clone`. Lean toward a flake input — pure and offline — but
runtime clone is acceptable for v1.2.0 since setup is already online for the ZIP.

### D5. Setup writes to the Inkscape user dir
`ica setup` resolves `$INKSCAPE_DIR` (reuse RUNME's macOS/Linux logic) and installs:
- `symbols/aws-architect/` ← built symbols
- `templates/aws-architect/` ← shipped templates (from the package)
The extension dir is the GUI dialog's concern (RUNME `extension_install`); `ica
setup` MAY install it too, but the CLI render path does not require it.
*Why:* one shared location for CLI and GUI; matches the hard-Inkscape decision.

### D6. cloudia stays out of the package closure
`cloudia-reader-aws` is only in the devShell. Rendering never imports it (only the
future `ica pull` bean will). The package closure is therefore clean: Python env +
code + setup tools. (This also sidesteps the cloudia Python-version PATH clash
entirely for the package.)

## Risks / Trade-offs

- **`python3Packages.inkex` in a build closure** may be awkward (inkex historically
  ships with Inkscape) → *Mitigation:* spike first; if it doesn't package cleanly,
  fall back to a wrapper (D1 alternative) that reuses the devShell-proven env.
- **AWS URL rot** → *Mitigation:* D3 config-override + `--asset-zip` + repo fallback;
  clear error pointing at `aws.amazon.com/architecture/icons` if all fail.
- **AWS-copyright ZIP in a public repo** → kept only as a fallback, not our
  redistribution channel; documented. (Pre-existing; not introduced here.)
- **`nix run` UX for setup** — `nix run .#ica -- setup --asset-zip <path>` passes
  args through; verify the apps wiring forwards argv correctly.

## Migration Plan
1. Spike: confirm `python3Packages.inkex` builds in a `buildPythonApplication` closure.
2. Add `pyproject.toml` (in place) + `packages.ica`/`apps.ica`/`packages.default`.
3. Wrap setup tools onto PATH (D2).
4. Implement `ica setup` (ZIP chain D3, awslabs D4, install D5).
5. Verify: `nix run .#ica -- --help`, `-- initconf`, `-- setup --asset-zip <repo zip>`,
   then `-- render <data> all -o /tmp/out.svg`; ideally on a machine without a
   pre-populated `~/.config/inkscape`.

Rollback: remove the `packages`/`apps` outputs and the `setup` command; the devShell
+ render path are unaffected.

## Open Questions
- awslabs: flake input vs runtime clone (D4) — decide in apply.
- Does `ica setup` also install the GUI extension, or only symbols+templates? Lean symbols+templates; extension install can stay a documented RUNME/GUI step.
- Exact `pyproject` shape for an in-place package whose modules sit under `extensions/aws-auto-diagram/`.
