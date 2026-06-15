## Context

`ica setup` (shipped) installs symbols → `$INKSCAPE_DIR/symbols/aws-architect/` and
templates → `$INKSCAPE_DIR/templates/aws-architect/`. The engine loads 6 specific
symbol SVGs (`engine.SYMBOL_FILES`) from `resolve_symbol_dir` (explicit → config →
Inkscape default). Without them, `render` produces a near-empty SVG and gives no
diagnosis. `ica doctor` closes that gap. All the pieces it needs already exist:
`_inkscape_dir()`, `engine.resolve_symbol_dir()`, `engine.SYMBOL_FILES`.

## Goals / Non-Goals

**Goals:** a clear per-item health check with actionable remedies; correct exit code
(fail on missing required deps); reuse existing helpers; customer-data-free tests.

**Non-Goals:** auto-fixing/installing from doctor (report + instruct only); any
render/engine/setup change.

## Decisions

### D1. Check set + severity
| Check | How | Severity |
|-------|-----|----------|
| inkex importable | `import inkex` | **required** (render can't work) |
| symbols present | each of `engine.SYMBOL_FILES` exists under `resolve_symbol_dir(config)` | **required** |
| templates present | `$INKSCAPE_DIR/templates/aws-architect/` non-empty | warning (GUI-only) |
| extension present | `$INKSCAPE_DIR/extensions/aws-auto-diagram/` exists | info (GUI dialog) |

Exit non-zero iff a **required** check fails. Templates/extension are GUI niceties
the headless CLI doesn't need, so they don't fail the exit code.

### D2. Actionable remedies
Each failing check prints a specific next step:
- inkex missing → "run inside the `nix develop` shell, or install via the flake".
- symbols missing → "run `ica setup` (optionally `--asset-zip <path>`)".
- templates/extension missing → "run `ica setup`" (warning only).
The symbol remedy points at `ica setup`, closing the loop with the shipped command.

### D3. Reuse, don't reinvent
Resolve the symbol dir via `engine.resolve_symbol_dir(config, None)` so doctor checks
the SAME location render uses (explicit/config/default). Resolve the Inkscape dir via
the existing `_inkscape_dir()`. The 6 required files come from `engine.SYMBOL_FILES`
(single source — if render's required set changes, doctor follows automatically).

### D4. Output format
Human-readable lines, one per check, with a leading status glyph (e.g. `ok` /
`MISSING` / `warn`), then a final summary line. Verbosity flag already exists on the
app. No machine/JSON output for now (could add `--json` later if scripted).

## Risks / Trade-offs

- **resolve_symbol_dir depends on config** (a `symbols.dir` override) → doctor must
  load config the same way render does, so it checks the real location. Mitigation:
  load config via the same path `render` uses.
- **Templates "non-empty" heuristic** → a partial template install could pass; accept
  for v1 (templates are a GUI nicety, warning-only).
- **inkex check in a packaged ica** → the nix package bundles inkex, so it should
  always pass there; the check mainly helps dev/`nix develop` and odd installs.

## Migration Plan
1. Add `doctor` subcommand reusing `_inkscape_dir` / `resolve_symbol_dir` / `SYMBOL_FILES`.
2. Add `test_ica_doctor` (temp `$INKSCAPE_DIR`: healthy, missing-symbols, missing-templates) → `test_all`.
3. Verify `test_all` green; manual `ica doctor` against a populated and an empty `$INKSCAPE_DIR`.

Rollback: remove the `doctor` subcommand + its test. No other surface affected.

## Open Questions
- Add `--json` output now or defer? Lean defer (no scripted consumer yet).
- Should doctor offer to run setup interactively? Lean no for v1 (report + instruct); revisit if users ask.
