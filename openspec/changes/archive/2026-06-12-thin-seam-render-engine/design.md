## Context

Rendering lives entirely on `aws_auto_diagram(inkex.EffectExtension)` in
`aws-auto-diagram.py`. `effect()` loads config, imports symbol defs, parses
account-data via `cloudia_parser`, orchestrates `resource_*` renderers, and calls
`resize_to_fit()`. The resource modules already take a parameter named `inkdoc`
(not `self`), so the seam is half-anticipated.

Investigation (this change's exploration) established two load-bearing facts:

1. **The renderers need a tiny surface from `inkdoc`:** `inkdoc.svg` (an inkex
   `SvgDocumentElement` — `.append/.findall/.descendants/.defs`) and
   `inkdoc.make_symbol_instance(symbol_id, parent)` (16 call sites). `layers.py`
   only touches `inkdoc.svg`.
2. **inkex works headless:** `inkex.load_svg(...).getroot()` yields a usable
   `SvgDocumentElement` and `.tostring()` serializes it — no `EffectExtension`,
   no Inkscape process (verified in the devshell).

Constraint from the bean and proposal: **byte-identical output**. This is a pure
invocation-path refactor; `cloudia_parser`, every `resource_*`, `theme`, `layout`,
`legend`, and `default-config.yaml` semantics stay as-is.

## Goals / Non-Goals

**Goals:**
- A headless `render(data_dir, region, config, options) -> svg_string` callable with no Inkscape runtime.
- A document object (`inkdoc`) satisfying the documented surface, shared by the Inkscape `EffectExtension` path and the headless path — one orchestration implementation, two thin entry points.
- Configurable symbol-source location so a non-Inkscape install can find symbols.
- Byte-identical SVG for existing inputs; `35-extension-run.sh` calls the engine directly.

**Non-Goals:**
- The `ica` CLI/TUI (later beans).
- Changing what is rendered, layout math, or config semantics.
- Removing inkex (it stays as the SVG-tree library; the seam is "thin").
- Replacing `cloudia_parser` or the symbol *build* pipeline.

## Decisions

### D1. Extract orchestration into an importable engine module
Move the body of `effect()`, `_render_single_region`, `_render_multi_region`,
`_render_vpcs`, `_assign_private_zones`, `resize_to_fit`, and
`make_symbol_instance` into `ica_utils/engine.py` as functions/a class that
operate on an `inkdoc` object. `aws-auto-diagram.py`'s `EffectExtension.effect()`
becomes a thin adapter: it *is* an inkdoc (or wraps `self` into one) and calls the
shared orchestration.

*Why:* one implementation, no duplication, Inkscape path preserved.
*Alternative rejected:* duplicate the logic for headless — guarantees drift, the
exact anti-pattern the seam exists to prevent.

### D2. The `inkdoc` object — minimal duck-typed surface
Define a small class (e.g. `RenderDoc`) holding an inkex `SvgDocumentElement` as
`.svg` and implementing `make_symbol_instance(symbol_id, parent)` (the existing
extension method, moved verbatim). The headless engine constructs `RenderDoc` from
a blank inkex SVG; the `EffectExtension` either subclasses/adapts to the same
surface or hands `self` (which already satisfies it) to the orchestration.

*Why:* the measured surface is tiny (`.svg` + `make_symbol_instance` + layer
helper, which only needs `.svg`). A full abstraction layer would be over-engineering.
*Alternative rejected:* a heavy document-backend interface — unjustified for two
call sites' worth of surface.

### D3. Headless SVG construction
The engine builds its document via `inkex.load_svg(<blank svg>).getroot()` (proven
headless), mirroring what `35-extension-run.sh` feeds today — but in-process, no
`mktemp`, no subprocess.

*Why:* reuses the verified-working inkex path; keeps the canvas identical to today's
extension input so output cannot drift.

### D4. Configurable symbol source (the SNAG)
Replace the hard-coded `~/.config/inkscape/symbols/aws-architect/` with a resolved
symbol directory:
1. explicit `options.symbol_dir` (CLI/engine arg), else
2. a config value (e.g. `document.symbol_dir` or a new `symbols.dir`), else
3. default to the Inkscape location `<inkscape_dir>/symbols/aws-architect/` (current
   behavior) — so Inkscape installs are unchanged.

A non-Inkscape `ica` install can point at the repo's built
`symbols/aws-inkscape-symbols/target/` or a packaged copy (nix-package bean decides
the packaged path; this change just makes the location injectable).

*Why:* smallest change that unbreaks headless without disturbing Inkscape users.
*Alternative rejected:* bundling symbols into the SVG/engine now — that's packaging
(bean 30), out of scope here; this change only makes the path configurable.

### D5. Output contract
`render(...)` returns the serialized SVG string. Writing to a file (and *where*) is
the caller's concern — keeps the engine pure and leaves safe-output-path policy to
the safe-io bean (40). `35-extension-run.sh` writes the returned string to its
`--output` path.

## Risks / Trade-offs

- **`make_symbol_instance` calls `use_element.bounding_box()`** → historically needs
  a render backend. *Mitigation:* verify headless `bounding_box()` FIRST (spike). If
  it requires Inkscape, fall back to computing symbol bbox from the loaded symbol
  defs (we import them, so the geometry is available) — note this as the one part
  that may need real work, not just moving code.
- **Byte-identical drift** from reordering or re-serialization → *Mitigation:* golden
  test (same pattern as config-schema 6.2): render a fixture before/after, assert
  identical bytes; block the change on any diff.
- **Symbol-dir default for nix** is deferred to bean 30 → *Mitigation:* this change
  ships the injection point + the unchanged Inkscape default, so nothing regresses;
  packaging fills in its path later.
- **EffectExtension adaptation subtlety** (does `self` cleanly satisfy the inkdoc
  surface, or do we need an adapter?) → *Mitigation:* D2 allows either; pick whichever
  keeps the Inkscape path byte-identical.

## Migration Plan

1. Spike: confirm headless `bounding_box()` (decides whether D2 is move-only or needs bbox fallback).
2. Add `engine.py` with `RenderDoc` + orchestration moved from the extension.
3. Repoint `EffectExtension.effect()` to delegate; confirm Inkscape path unchanged.
4. Add configurable symbol-source resolution (D4).
5. Rewire `35-extension-run.sh` to the engine; golden byte-identical check; headless test.

Rollback: revert the engine extraction; the extension's original `effect()` is restored from git. No data migration, no persisted state.

## Open Questions (resolved during apply)

- ~~Exact config key name for the symbol dir~~ → **Decided: `config["symbols"]["dir"]`** (resolution: explicit `symbol_dir` arg → `symbols.dir` config → Inkscape default `~/.config/inkscape/symbols/aws-architect`). No `symbols` block exists in `default-config.yaml`, so the default path is always hit today → Inkscape behavior unchanged.
- ~~Where does `render()` live~~ → **Decided: `ica_utils/engine.py`** (one import root; the `ica` package, bean 20, can re-export).
- **Resolved during apply — `bounding_box()` spike succeeded:** loaded 36 real symbols headless, `Use.bounding_box()` returned a real bbox with no Inkscape process. The refactor was move-only; no bbox fallback was needed.
- **Note discovered during apply:** `inkex.load_svg()` rejects a *str* carrying an XML encoding declaration. The headless blank canvas omits the `<?xml?>` declaration but keeps the original file's whitespace, yielding byte-identical output (verified for single-region AND multi-region against the pre-refactor code).
