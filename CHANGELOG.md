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

## v1.1.0 Dark Mode - 3 april 2025

- Add dark mode templates.

## v1.0.0 Initial Release

- Create templates and symbols
- Create make script
