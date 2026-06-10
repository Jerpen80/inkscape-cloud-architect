## 1. Dependencies & entry point

- [ ] 1.1 Add `typer` (and its `click` dep) to the flake `pythonEnv`; confirm `python3 -c "import typer"` works in the devshell
- [ ] 1.2 Create the `ica` entry module (Typer app) — placement per design D6 (sibling of the engine, importing `ica_utils` in place); wire `--version`, `--help`, verbosity
- [ ] 1.3 Confirm the Inkscape extension + `.inx` are untouched (dialog still works; `ica_utils` not moved)

## 2. Config-input pipeline (config-loading capability)

- [ ] 2.1 Implement override-file loading from an arbitrary path, deep-merged over defaults (reuse `config._deep_merge`)
- [ ] 2.2 Implement `--set <dotted.key>=<value>` parsing (split on first `=`) into a nested override dict
- [ ] 2.3 Implement type coercion driven by `config_schema` `Field.type` (int/float/bool/color/enum); unknown key → error, not a guess
- [ ] 2.4 Establish merge order defaults ◄ --config ◄ --set; validate the merged config via `schema.validate_override`; aggregate per-key errors

## 3. `ica render`

- [ ] 3.1 Add `render` subcommand: args `data_dir`, `region`; options `--theme --layout-mode --account-name --config --set` and required `-o`
- [ ] 3.2 Build merged+validated config (section 2); on validation error print per-key messages and exit non-zero WITHOUT rendering
- [ ] 3.3 Call the engine with the merged config (design D3 — prefer extending `render(config=...)`); confirm Inkscape path passes no `config=` and is unaffected
- [ ] 3.4 Write SVG to `-o <file>`; support `-o -` for explicit stdout; omitting `-o` errors

## 4. `ica initconf`

- [ ] 4.1 Add `initconf` subcommand: emit a curated starter YAML (theme, layout mode, a few common knobs) with schema-sourced defaults + a header comment pointing at the full key set
- [ ] 4.2 Verify the generated file round-trips: `ica render --config <it>` loads and validates without error

## 5. Verification

- [ ] 5.1 `ica render` golden check: a plain `ica render` matches the engine baseline byte-for-byte (render to /tmp, never the repo)
- [ ] 5.2 `--set` equivalence: `ica render --set layout.ec2.icon_scale=0.8` matches a render from an equivalently edited config (confirms coercion + merge flow through resolve/theme)
- [ ] 5.3 Validation tests: unknown key / wrong type / out-of-range / bad enum each fail fast with non-zero exit and no output file
- [ ] 5.4 Run `./RUNME.sh test_all` and a headless render in `nix develop`; confirm existing tests pass and the Inkscape extension still renders unchanged
- [ ] 5.5 Add `ica` tests to `RUNME.d/50-tests.sh` (no-pytest self-checking scripts, per project convention)
