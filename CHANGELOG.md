# CHANGELOG.md

## v2.0.0 AWS Auto Diagram

- refactoring project dir
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

## v1.1.0 Dark Mode - 3 april 2025

- Add dark mode templates.

## v1.0.0 Initial Release

- Create templates and symbols
- Create make script
