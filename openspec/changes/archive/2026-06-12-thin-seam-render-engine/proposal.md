## Why

The diagram-rendering logic only exists as methods on an `inkex.EffectExtension`
(`aws-auto-diagram.py`), so it can only run inside Inkscape's extension lifecycle.
Every front-end that isn't Inkscape — the planned `ica` CLI/TUI, CI, tests — must
fake that lifecycle (the blank-SVG `mktemp` dance in `RUNME.d/35-extension-run.sh`).
This change extracts a thin seam — `render(account_data, config) -> svg` — so one
engine can be called natively by any front-end, with inkex used purely as an
SVG-tree library and no Inkscape runtime required.

Bean: [inkscape-cloud-architect-ciwl](../../../.beans/inkscape-cloud-architect-ciwl--10-thin-seam-extract-renderdatacfg-svg-engine.md)
(epic [muex](../../../.beans/inkscape-cloud-architect-muex--we-need-a-wrapper-which-is-userfriendly.md);
the architectural keystone for the `ica` wrapper, ships in v1.2.0.)

## What Changes

- Introduce a headless **render engine** entry point — `render(data_dir, region, config, options) -> svg_string` — that builds an inkex SVG document, runs the existing orchestration, and returns serialized SVG, without instantiating `inkex.EffectExtension`.
- Introduce a small **document object** (an "inkdoc") the resource modules draw into. Investigation shows they require a tiny surface: `inkdoc.svg` (an inkex `SvgDocumentElement`, with `.append/.findall/.descendants/.defs`) and `inkdoc.make_symbol_instance(symbol_id, parent)`. The new object provides exactly this and is satisfiable both by the live `EffectExtension` (Inkscape path, unchanged) and by the headless engine.
- Refactor `aws-auto-diagram.py`: keep the `EffectExtension` as a thin wrapper whose `effect()` delegates to the shared engine. Move the orchestration (`effect()` body, `_render_*`, `resize_to_fit`, `make_symbol_instance`) into an importable engine module so both paths share one implementation.
- Resolve the **symbol-path SNAG**: `import_defs_from_external_file_in_document()` reads `~/.config/inkscape/symbols/aws-architect/`, an Inkscape-install assumption that breaks headless. Make symbol-source location configurable (config key + sensible default + override), so a non-Inkscape `ica` install can locate symbols. Inkscape behavior unchanged when the Inkscape path exists.
- Rewire `RUNME.d/35-extension-run.sh` to call the engine directly (drop the blank-SVG `mktemp` dance), proving the seam.

Non-goals: no `ica` CLI/TUI (later beans), no change to *what* is rendered. Rendered SVG for existing inputs MUST remain byte-identical.

## Capabilities

### New Capabilities
- `render-engine`: A headless rendering entry point and document abstraction that produce diagram SVG from account-data + config without requiring the Inkscape runtime, plus configurable symbol-source resolution.

### Modified Capabilities
<!-- None. Rendering requirements (account/region/resource rendering, document-resize, theme, layout) are unchanged; only the invocation path is refactored. Output is byte-identical, so no existing render spec's requirements change. -->

## Impact

- **Refactored**: `extensions/aws-auto-diagram/aws-auto-diagram.py` — `EffectExtension` becomes a thin wrapper delegating to the engine.
- **New**: an engine module under `ica_utils/` (e.g. `ica_utils/engine.py`) holding the shared orchestration + the inkdoc document object.
- **Modified**: `ica_utils/layers.py`, `resource_*.py` — only if needed to depend on the documented inkdoc surface rather than the concrete extension (expected: no signature changes; they already take an `inkdoc` parameter).
- **Modified**: symbol-source resolution (config + a small loader), affecting `import_defs`.
- **Modified**: `RUNME.d/35-extension-run.sh` — calls the engine directly.
- **Risk to verify early**: `make_symbol_instance` calls `use_element.bounding_box()`, which historically needed a render backend; confirm it works headless (it is the one piece that could require an Inkscape process).
- **Engine behavior**: unchanged — golden byte-identical SVG is a requirement.
