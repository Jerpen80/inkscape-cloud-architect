# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- **release tooling** — `./RUNME.sh release <major|minor|patch>`
  - Keep a Changelog format with `[Unreleased]`; the command bumps the version,
    rewrites the changelog, commits, tags, pushes, and creates a GitHub Release.
    Works with both git and jj.
  - See [proposal](openspec/changes/archive/2026-06-12-release-management/proposal.md).
- **synthetic test fixture** — customer-data-free render regression suite
  - A hand-authored, provably-fake account (`tests/fixtures/synthetic-account/`)
    exercising every renderer, plus a structural test (`test_render_fixture`,
    in `test_all`) that asserts the rendered SVG's shape. No real account-data.
  - See [proposal](openspec/changes/archive/2026-06-12-synthetic-fixtures/proposal.md).
- **ica doctor** — check the render environment is healthy + how to fix it
  - Verifies inkex, symbols, templates, and the installed extension; prints a
    per-item status with actionable remedies (e.g. `ica setup`) and exits
    non-zero when a required dependency (inkex, symbols) is missing.
  - See [proposal](openspec/changes/archive/2026-06-15-ica-doctor/proposal.md).

### Changed

- **config single-source-of-truth** — collapse 3 default sources into one
  - `default-config.yaml` now stores `spaced` as canonical and `dense` as a diff
    of only the keys that differ; 161 redundant inline `.get(k, default)` shadow
    defaults removed from the renderers. Output is byte-identical (guarded by a
    new byte-exact golden test, `test_config_golden`).
  - See [proposal](openspec/changes/archive/2026-06-15-config-restructure/proposal.md).

### Fixed

- **symbol directory resolution** honors `$INKSCAPE_DIR` and macOS
  - `engine.default_symbol_dir()` previously hardcoded `~/.config/inkscape`, so on
    macOS (or with `$INKSCAPE_DIR` set) `ica setup` installed symbols where the
    renderer could not find them. Now both resolve via one `engine.inkscape_dir()`.

## [2.0.0] - 2026-06-12

### Added

- **headless render engine** — call rendering without the Inkscape runtime
  - Extracted orchestration into `ica_utils/engine.py` (`RenderDoc` + `render()`);
    the Inkscape extension is now a thin wrapper that delegates to it.
  - `RUNME.sh extension_run` calls the engine by import (no subprocess / blank-SVG).
  - Output verified byte-identical for single- and multi-region renders.
  - See [proposal](openspec/changes/archive/2026-06-12-thin-seam-render-engine/proposal.md).
- **config schema** — describe & validate all ~120 config keys (metadata only)
  - `ica_utils/config_schema.py`; defaults sourced from `default-config.yaml`.
  - See [proposal](openspec/changes/archive/2026-06-10-config-schema/proposal.md).
- **ica CLI** — render diagrams + manage config from the command line
  - `ica render` (with `--config` file and repeatable `--set key=value`,
    type-coerced and validated against the schema before rendering) and
    `ica initconf` (curated starter config). Typer-based, `--version`/`--help`.
  - See [proposal](openspec/changes/archive/2026-06-12-ica-cli/proposal.md).
- **nix package + setup** — install ica via nix; ica setup builds symbols
  - `nix run .#ica` / `nix profile install`; `ica setup` obtains the AWS icon
    ZIP (`--asset-zip` / download / repo fallback) and installs symbols +
    templates into the Inkscape dir. AWS symbols are never redistributed.
  - See [proposal](openspec/changes/archive/2026-06-12-nix-package-ica/proposal.md).

### Changed

- refactoring project dir

## [1.1.0] - 2025-04-03

### Added

- Dark mode templates.

## [1.0.0] - Initial Release

### Added

- Templates and symbols.
- Make script.

[Unreleased]: https://github.com/mipmip/inkscape-cloud-architect/compare/v2.0.0...HEAD
[2.0.0]: https://github.com/mipmip/inkscape-cloud-architect/compare/v1.1.0...v2.0.0
[1.1.0]: https://github.com/mipmip/inkscape-cloud-architect/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/mipmip/inkscape-cloud-architect/releases/tag/v1.0.0
