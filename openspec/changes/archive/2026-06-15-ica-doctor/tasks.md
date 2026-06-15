## 1. ica doctor subcommand

- [x] 1.1 Added a `doctor` subcommand to `ica_cli.py` — per-item status lines + final summary
- [x] 1.2 Checks **inkex importable** (required)
- [x] 1.3 Checks **symbols present** (required) — resolves via `engine.resolve_symbol_dir(config, None)` (same as render), verifies each of `engine.SYMBOL_FILES`
- [x] 1.4 Checks **templates present** (warning) — `<inkscape_dir>/templates/aws-architect/` non-empty
- [x] 1.5 Checks **extension present** (info) — `<inkscape_dir>/extensions/aws-auto-diagram/`
- [x] 1.6 Prints an actionable remedy per failing/warning check (symbols → `ica setup`; inkex → nix develop / flake)
- [x] 1.7 Exits non-zero iff a required check (inkex or symbols) fails; zero otherwise

## 1b. Engine symbol-dir bugfix (discovered during apply)

- [x] 1b.1 FIXED a pre-existing inconsistency: `engine.default_symbol_dir()` hardcoded `~/.config/inkscape` (ignored `$INKSCAPE_DIR`, wrong on macOS) while `ica setup` installs to `_inkscape_dir()` (honors both). Added `engine.inkscape_dir()` (honors `$INKSCAPE_DIR` + macOS) and routed `default_symbol_dir()` + `ica_cli._inkscape_dir()` through it. Now setup/render/doctor agree.
- [x] 1b.2 Golden byte-identical after the engine change (Linux-default resolves to the same `~/.config/inkscape`); extension `.py`/`.inx` untouched.

## 2. Tests

- [x] 2.1 Added `tests/test_ica_doctor.py` (no-pytest; Typer `CliRunner` + temp `$INKSCAPE_DIR` + `symbols.dir` override): healthy → exit 0; missing symbols → exit non-zero + `ica setup` remedy; templates-only missing → exit 0 (warning)
- [x] 2.2 Added `test_ica_doctor` to `RUNME.d/50-tests.sh` and `test_all`

## 3. Verify

- [x] 3.1 `./RUNME.sh test_all` green (incl. config_golden + ica_doctor)
- [x] 3.2 Manual: `ica doctor` against a populated `$INKSCAPE_DIR` → all OK, exit 0; against an empty temp dir → symbols MISSING, exit non-zero, `ica setup` remedy shown
- [x] 3.3 render/engine behavior + Inkscape extension unchanged (engine touched only for the symbol-dir bugfix; golden byte-identical; `.py`/`.inx` zero diff)
