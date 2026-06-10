## 1. De-risk spike (do first)

- [x] 1.1 In the devshell, build a `Use` symbol headless and call `bounding_box()`; confirm it returns a real bbox without an Inkscape process
  - VERIFIED: loaded 36 real symbols headless, `use.bounding_box()` returned `BoundingBox((0.0, 40.0),(0.0, 40.0))` with no Inkscape process. The refactor is move-only; no bbox fallback required.
- [x] 1.2 If 1.1 fails, prototype a bbox fallback from the imported symbol defs and note it in design.md Open Questions before proceeding
  - N/A — 1.1 succeeded, so no fallback is needed.

## 2. Engine module + document object

- [x] 2.1 Add `ica_utils/engine.py` with a `RenderDoc` object exposing `.svg` (inkex `SvgDocumentElement`) and `make_symbol_instance(symbol_id, parent)` (moved verbatim from the extension)
- [x] 2.2 Move orchestration into `engine.py`: `effect()` body → `RenderDoc.render()`, plus `_render_single_region`, `_render_multi_region`, `_render_vpcs`, `_assign_private_zones`, `_create_layers`, `resize_to_fit` — all operating on the doc
- [x] 2.3 Add `render(data_dir, region, ...) -> str`: build a blank inkex SVG via `inkex.load_svg(...).getroot()`, wrap in `RenderDoc`, run orchestration, return serialized SVG
- [x] 2.4 Confirm no engine module imports require the Inkscape runtime (pure import check — `from ica_utils.engine import render` succeeds, render callable)

## 3. Inkscape extension becomes a thin wrapper

- [x] 3.1 Repoint `aws_auto_diagram.effect()` to delegate: builds `RenderDoc(self.svg, config, self.options)` and calls `.render()`
- [x] 3.2 Remove the now-duplicated render logic from `aws-auto-diagram.py` — file is now ~30 lines: `add_arguments`, `effect()` delegation, `__main__`
- [x] 3.3 Verify resource modules + `layers.py` need no signature changes — git diff shows ZERO changes to resource_*.py / layers / layout / theme / legend / cloudia_parser

## 4. Configurable symbol source (the SNAG)

- [x] 4.1 Add symbol-dir resolution (`resolve_symbol_dir`): explicit option → `config["symbols"]["dir"]` → Inkscape default `~/.config/inkscape/symbols/aws-architect`
- [x] 4.2 Route `import_defs` through the resolved directory; Inkscape default path confirmed byte-identical (the golden render used it)
- [x] 4.3 Document the chosen config key name (`symbols.dir`) — recorded in design.md Open Questions

## 5. Rewire the headless runner

- [x] 5.1 Update `RUNME.d/35-extension-run.sh` to call `engine.render(...)` via a pure-Python import (heredoc) and write the returned string to `--output`; dropped the blank-SVG `mktemp` + subprocess dance

## 6. Verification (behavior unchanged)

- [x] 6.1 Golden byte-identical check: captured baseline from pre-refactor code, rendered same fixture via new engine → identical MD5 (650380 bytes). Rendered to /tmp only (real customer data is the only local fixture).
- [x] 6.2 Confirmed unchanged output on BOTH paths: reconstructed the pre-refactor extension from git HEAD and compared multi-region (`region=all`) old vs new → byte-identical (646841 bytes)
- [x] 6.3 Headless test passes: `extension_run` succeeds via the engine for single-region, multi-region, and dark/dense
- [x] 6.4 `./RUNME.sh test_all` → "All tests passed" (includes config_schema tests)
  - Note discovered: `inkex.load_svg()` rejects a *str* with an XML encoding declaration; the headless blank SVG omits `<?xml?>` but keeps the original whitespace → byte-identical output.
