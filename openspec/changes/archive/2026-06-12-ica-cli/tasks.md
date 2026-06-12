## 1. Dependencies & entry point

- [x] 1.1 Add `typer` (and its `click` dep) to the flake `pythonEnv`; confirm import works (typer 0.15.2, click 8.1.8)
- [x] 1.2 Create the `ica` entry module (`extensions/aws-auto-diagram/ica_cli.py`, Typer app, imports `ica_utils` in place); `--version`, `--help`, `-v/--verbose`
- [x] 1.3 Confirm the Inkscape extension + `.inx` are untouched — git diff vs HEAD on aws-auto-diagram.py / .inx is empty; dialog path renders byte-identical

## 2. Config-input pipeline (config-loading capability)

- [x] 2.1 Override-file loading from an arbitrary path (`ica_cli._build_override` → `yaml.safe_load` → coerce → `_deep_merge`)
- [x] 2.2 `--set <dotted.key>=<value>` parsing (`config_schema.parse_set_pairs`, split on first `=`, nested dict)
- [x] 2.3 Type coercion driven by `Field.type` (`config_schema.coerce_override` / `_coerce_string`: int/float/bool; color/str/enum pass-through); unknown key → error
- [x] 2.4 Merge order defaults ◄ --config ◄ --set; each layer fully validated (unknown/type/range/enum) by `coerce_override` before merge; errors aggregated per key
  - Design correction: overrides are NOT pre-merged into config (the merged config is raw preset form, which the flat schema can't validate). Instead the coerced flat override is passed to the engine and applied AFTER `resolve_layout_mode` (see 3.3 note).

## 3. `ica render`

- [x] 3.1 `render` subcommand: args `data_dir`,`region`; options `--theme --layout-mode --account-name --config --set`; required `-o`
- [x] 3.2 Build validated override; on error print per-key messages, exit≠0, NO render (verified: unknown/type/range/enum cases write no file)
- [x] 3.3 Call the engine with the override (extended `render(config=, override=)`); Inkscape path passes neither and is unaffected
  - BUG FOUND & FIXED: pre-merging a `layout.*` override before `resolve_layout_mode` was clobbered by the preset. Fix: engine applies `override` AFTER resolve (RenderDoc.layout_override). Verified a `layout.account.padding.top` override changes output.
- [x] 3.4 Write to `-o <file>`; `-o -` → stdout; omitting `-o` errors (Typer required option)

## 4. `ica initconf`

- [x] 4.1 `initconf` subcommand: emits a curated starter YAML (layout.mode, document.margin, ec2.icon_scale, subnet.min_width, vpc.gap) with schema-sourced defaults + header comment. (Bare `theme` is a render option, not a config key, so it's not in the file; the header points at the full set.)
- [x] 4.2 Round-trip verified: `ica initconf -o f.yaml` then `ica render --config f.yaml` renders without error (650380 bytes = baseline, since starter = defaults)

## 5. Verification

- [x] 5.1 Golden check: plain `ica render` == engine baseline byte-for-byte (650380). Rendered to /tmp, never the repo.
- [x] 5.2 Override-effect verified: `--set document.margin=99` changes canvas (364→522 width, = 2×margin delta); `--set layout.account.padding.top=500` changes output (proves post-resolve fix). (`ec2.icon_scale` had no effect only because no test account has EC2 — not a bug.)
- [x] 5.3 Validation: unknown key / wrong type / out-of-range / bad enum each fail fast (exit≠0) with a clear per-key message and NO output file
- [x] 5.4 `./RUNME.sh test_all` passes; headless render works; Inkscape extension path byte-identical to baseline
- [x] 5.5 Added `test_ica_cli` (no-pytest self-checking script) to `RUNME.d/50-tests.sh` and `test_all`
