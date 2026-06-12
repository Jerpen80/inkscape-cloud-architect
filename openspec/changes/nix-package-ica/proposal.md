## Why

`ica` only runs today through a dev harness (`nix develop` → `cd` into the
extension dir → `PYTHONPATH=. python3 ica_cli.py`). Co-workers cannot install one
thing and produce a diagram. This change packages `ica` as a flake output so
`nix run`/`nix profile install` work, and folds in `ica setup` — the step that
installs the AWS symbols and templates `ica render` needs — so that after install
a co-worker can go from nothing to a diagram.

Bean: [inkscape-cloud-architect-fy5b](../../../.beans/inkscape-cloud-architect-fy5b--30-nix-package-ica-installable-flake-output.md)
(epic [muex](../../../.beans/inkscape-cloud-architect-muex--we-need-a-wrapper-which-is-userfriendly.md);
the v1.2.0 first-co-worker drop. Depends on the completed ica-cli change.)

## What Changes

- Add flake `packages.ica` + `apps.ica` (and `packages.default = ica`) so `nix run .#ica` and `nix profile install` work. Build `ica` with `buildPythonApplication` over `extensions/aws-auto-diagram/` **in place** — `ica_utils` is NOT moved, so the Inkscape dialog keeps working.
- Console entry point `ica = ica_cli:app`; `propagatedBuildInputs` = inkex, lxml, tinycss2, pyyaml, typer. Runtime tools needed by setup (git, rsync, unzip, plus a fetcher) are wrapped onto PATH.
- Add `ica setup` (folded in from the doctor/setup bean): obtain the AWS icon ZIP, build the symbols, and install symbols + templates into the user's Inkscape dir (`$INKSCAPE_DIR/{symbols,templates}/aws-architect`). `ica render` works after this.
  - **ZIP resolution** (first available wins): `--asset-zip <path>` → download from the AWS `d1.awsstatic.com` icon-package URL (overridable via config so the URL can be updated without a release) → fall back to the ZIP committed in the repo.
  - The package **ships the symbol build toolchain** (`build.sh`, `files_to_svg.py`) and **templates**, but **never ships the AWS-derived symbols** — the user obtains the icons from AWS at setup time (no redistribution by us).
- Hard Inkscape dependency is assumed and documented: `ica` installs into and renders against the Inkscape user dir (the app is *Inkscape* Cloud Architect).

### Non-goals (deferred)
- `ica doctor` + broken-install detection / fix-instructions UX → stays in [bean wkj7](../../../.beans/inkscape-cloud-architect-wkj7--35-ica-doctor-setup-inkscape-env-health-install.md) (narrowed to doctor-only).
- No bundling of AWS symbols (not redistributable). No `ica pull` (bean 50). No safe-io defaults (bean 40).
- No code relocation; no change to the Inkscape extension or `.inx`.
- Release/versioning/tagging stays the separate `release-management` change.

## Capabilities

### New Capabilities
- `packaging`: `ica` as an installable flake output (`packages.ica`/`apps.ica`), runnable via `nix run`/`nix profile install`, with the Inkscape dependency declared.
- `environment-setup`: `ica setup` — obtain the AWS icon ZIP (override → URL → repo fallback), build symbols, and install symbols + templates into the Inkscape user dir.

### Modified Capabilities
<!-- None. render-engine, config-loading, ica-cli are unchanged; this change packages and feeds them. -->

## Impact

- **Modified**: `flake.nix` — add `packages`/`apps` outputs; the package closure does NOT include cloudia (only the devShell does; rendering never needs it).
- **New**: packaging metadata (e.g. `pyproject.toml`) describing the in-place package + `ica` entry point.
- **New**: an `ica setup` command (in `ica_cli.py`) and supporting symbol/template install logic; reuses `symbols/aws-inkscape-symbols/build.sh` + `files_to_svg.py`.
- **Reused as-is**: `ica render`, `engine`, `config_schema`, the symbol build scripts, the templates.
- **Unchanged**: Inkscape extension + `.inx`; `ica_utils` location.
- **Licensing note**: the committed `Asset-Package_*.zip` (AWS-copyright) stays in the repo as a setup *fallback* only; `ica setup` prefers the user's own download / the live AWS URL. We never redistribute the built symbols.
