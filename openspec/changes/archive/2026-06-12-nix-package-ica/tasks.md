## 1. De-risk spike (do first)

- [x] 1.1 Confirm `pkgs.python3Packages.inkex` resolves in a `buildPythonApplication` closure
  - VERIFIED: `python3Packages.inkex` is a standalone derivation (inkex 1.4.4), not bundled with the Inkscape app. A spike `buildPythonApplication` built and ran (`--version`/`--help`/`initconf` all worked from the closure). No makeWrapper fallback needed.

## 2. Package the CLI (in place)

- [x] 2.1 Add `extensions/aws-auto-diagram/pyproject.toml` (in-place: `ica_cli` module + `ica_utils` package + `default-config.yaml`; console script `ica = ica_cli:app`). NOTE: the actual nix package uses an explicit installPhase (copies modules + writes the entry script) rather than setuptools, since the in-place layout isn't a clean setuptools tree; pyproject documents the intent.
- [x] 2.2 Add `packages.ica` (`buildPythonApplication`, propagatedBuildInputs inkex/lxml/tinycss2/pyyaml/typer) + `apps.ica` + `packages.default = ica` in flake.nix
- [x] 2.3 Wrap setup tools onto PATH (`wrapProgram --prefix PATH`: bash, git, rsync, unzip, curl, python) + set `ICA_SYMBOL_BUILD_DIR` / `ICA_TEMPLATES_DIR`
- [x] 2.4 cloudia is NOT in the package closure (only the devShell); render imports resolve from the closure (verified by running render with no devShell)
- [x] 2.5 Inkscape extension + `.inx` + `ica_utils` location unchanged; extension_run still renders byte-identical (650380)

## 3. `ica setup` — obtain the ZIP

- [x] 3.1 Added `ica setup` subcommand with `--asset-zip <path>`
- [x] 3.2 ZIP resolution chain (`_resolve_asset_zip`): `--asset-zip` → download (`symbols.asset_zip_url` config, default = d1.awsstatic.com Icon-package URL) → repo fallback (`Asset-Package_*.zip`)
- [x] 3.3 On no obtainable ZIP: clear error pointing at `aws.amazon.com/architecture/icons`

## 4. `ica setup` — build & install

- [x] 4.1 awslabs group icons: runtime `git clone` (pinned rev, as build.sh already does); git is on the wrapped PATH. (Vendoring as a flake input deferred — runtime clone is acceptable since setup is already online for the ZIP.)
- [x] 4.2 Symbol build reuses `build.sh`/`files_to_svg.py` — run in a WRITABLE temp copy of the toolchain (build.sh writes target/build in its own dir; the shipped copy is read-only in the nix store). BUG found & fixed during apply.
- [x] 4.3 `_inkscape_dir()` resolves per platform (+ `$INKSCAPE_DIR` override); installs symbols → `symbols/aws-architect/`, templates → `templates/aws-architect/`
- [x] 4.4 Built AWS symbols are produced only at setup time on the user's machine; the package ships build tooling + templates, never built symbols

## 5. Verification (the realistic first-run flow)

- [x] 5.1 `nix run .#ica -- --version/--help/initconf` work (setup/render/initconf all listed)
- [x] 5.2 `ica setup --asset-zip <repo fallback>` builds + installs 49 symbols + 4 templates
- [x] 5.3 After setup, `ica render <data> eu-west-1 -o /tmp/...` produces a full diagram (650387 bytes)
- [x] 5.4 Verified in an ISOLATED HOME (no `~/.config/inkscape`): setup creates everything render needs. Proof: render with NO setup = 1805 bytes (near-empty); with setup = 650387 bytes.
- [x] 5.5 `./RUNME.sh test_all` passes; Inkscape extension path byte-identical (650380)
