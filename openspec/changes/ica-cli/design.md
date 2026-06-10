## Context

Two building blocks are done and tested:

- `ica_utils.engine.render(data_dir, region, account_name, theme, layout_mode, symbol_dir, extension_dir) -> svg_string` — headless, no Inkscape runtime.
- `ica_utils.config_schema` — `load_schema(ext) -> {path: ResolvedKey}`, `validate_override(user_dict, ext) -> [Error]`, with `Field` metadata (type/range/enum/unit/help) per flattened dotted key.

`ica` is a thin front-end over these. The hard logic exists; this change is shape,
config-input ergonomics, and packaging-friendliness.

Hard constraint (from explore): **the Inkscape dialog must keep working.** Inkscape
runs the extension via `<command location="inx" interpreter="python">aws-auto-diagram.py`,
which puts the `.inx` directory on `sys.path` so `from ica_utils... import` resolves
because `ica_utils/` sits beside the script. Therefore `ica_utils` does not move.

## Goals / Non-Goals

**Goals:**
- `ica render` / `ica initconf` working via Typer, with completion + `--version` + verbosity.
- A layered, validated, type-coerced config-override pipeline.
- Required `-o` output (leak-safe). `ica` imports `ica_utils` in place; dialog untouched.

**Non-Goals:**
- `ica doctor`/`setup` (bean wkj7), TUI (60), `pull` (50).
- Moving/restructuring `ica_utils` (Option A: leave it in the extension dir).
- Bundling symbols / the installable nix entry point (bean 30) — though this change
  must not assume symbols live in the Inkscape user dir.

## Decisions

### D1. Framework: Typer
Type-hints generate `--help` and shell completion; minimal boilerplate; professional
feel. Adds `typer` + `click` to the flake `pythonEnv` (acceptable — this is now a
user-facing app). *Alternatives:* Click (more boilerplate), argparse (no-dep but
clunky completion). Typer wins on the "just works + polish" goal.

### D2. Config-input pipeline (the core ergonomics)
```
   default-config.yaml ──► deep-merge ◄── --config <file.yaml> ──► deep-merge ◄── --set k=v (repeatable)
                                                                          │
                                  ┌───────────────────────────────────────┘
                                  ▼
   coerce each --set string to its schema Field.type (int/float/bool/color/enum)
                                  ▼
   schema.validate_override(merged)  ──►  errors? print per-key, exit≠0, NO render
                                  ▼
   engine.render(...) with the merged config
```
- `--set layout.ec2.icon_scale=0.8` → split on first `=` → dotted path + raw string.
- The schema's `Field.type` for that path drives coercion: `"0.8"→0.8`, `"17"→17`,
  `"true"→True`, `"dark"→"dark"`. Unknown path → error before coercion.
- Merge order is `defaults ◄ file ◄ --set` (later wins); deep-merge reuses the
  existing `config._deep_merge` semantics.
*Why `--set` not a blob string:* maps 1:1 to the flat schema, trivial parse, crisp
per-key errors, no custom grammar or shell-quoting pain (helm/terraform pattern).

### D3. Engine integration — pass a merged config, don't re-plumb the engine
Today `engine.render()` builds config internally via `load_config()` + options. The
CLI needs to inject a *pre-merged, pre-validated* config. Two options:
- (a) extend `render()` to accept an optional `config=` (skip internal load when given), or
- (b) the CLI builds the merged config and calls a lower-level path.
Lean (a): smallest, keeps one entry point, Inkscape path unaffected (it passes no
`config=`). Decide exactly during apply; either way the engine's *behavior* for the
existing inputs is unchanged.

### D4. Output: required `-o`, explicit stdout via `-o -`
No implicit stdout. `-o <file>` writes; `-o -` streams to stdout for piping; omitting
`-o` is an error. Rationale: big SVGs + customer data → never dump silently into a
terminal or a redirect that could land in the repo.

### D5. `initconf` = curated starter, not a full dump
Emit a small YAML: `theme`, `layout.mode`, and a handful of common knobs (e.g. a
margin, an icon scale), values pulled from the schema's defaults, with a header
comment: "These are common options; run `ica render --help` / see the full key list
for the rest." A 120-key dump is not friendly; a curated seed + pointer is.

### D6. Code location: Option A (leave `ica_utils` in place)
`ica` adds `extensions/aws-auto-diagram/` to its import path (the nix package, bean
30, decides how — vendor a copy or point `sys.path`). Lowest risk to the dialog;
defers any restructure. The `ica` entry module can live at
`extensions/aws-auto-diagram/ica_cli.py` (sibling of the engine) or a small `ica/`
shim that imports it — resolve during apply.

## Risks / Trade-offs

- **`--set` type coercion edge cases** (e.g. a color that looks numeric, empty string)
  → *Mitigation:* coercion is driven by `Field.type`; validate after coerce so a bad
  value still produces a clear schema error.
- **Engine `config=` injection** might reveal hidden coupling (e.g. `resolve_layout_mode`
  / theme resolution happens inside `render`) → *Mitigation:* during apply, confirm the
  merged config flows through the same resolve/theme steps; golden-test a `--set` render
  vs an equivalent edited-`default-config` render.
- **Symbols location for the CLI** — `ica` must not assume the Inkscape user dir. For
  this change, rely on the engine's existing `symbol_dir` resolution (explicit → config
  → Inkscape default); the zero-setup bundled path is bean 30.
- **Typer/Click in the flake** — new deps; *Mitigation:* both are pure-Python, widely
  packaged in nixpkgs.

## Open Questions
- Entry-module placement (`ica_cli.py` beside engine vs an `ica/` package) — resolve in apply.
- Whether to extend `render(config=...)` (D3a) or add a lower-level call (D3b) — resolve in apply, prefer 3a.
- `initconf` exact key set — finalize the curated list during apply.
