# Design: Unified RUNME.sh Task Runner

## RUNME.sh Framework

Uses the existing RUNME.sh pattern (Pim Snel's framework) already in use in the extension. Single file, function-based command dispatch.

## Cross-Platform Detection

```bash
if [[ "$(uname)" == "Darwin" ]]; then
  INKSCAPE_DIR="$HOME/Library/Application Support/org.inkscape.Inkscape/config/inkscape"
else
  INKSCAPE_DIR="$HOME/.config/inkscape"
fi
```

Shared by all tasks. Replaces the Makefile's `ifeq` and fixes the extension's hardcoded Linux path.

## Task Namespace

Three deliverables, each with a prefix:

```
symbols_build          Build SVG symbols from AWS asset zip
symbols_install        rsync target/ → INKSCAPE_DIR/symbols/aws-architect/
symbols_clean          rm INKSCAPE_DIR/symbols/aws-architect/
symbols_clean_cache    rm awslabs-repo cache (explicit only, not in clean)

templates_install      rsync templates/ → INKSCAPE_DIR/templates/aws-architect/
templates_clean        rm INKSCAPE_DIR/templates/aws-architect/

extension_install      cp extension → INKSCAPE_DIR/extensions/aws-auto-diagram/
extension_clean        rm INKSCAPE_DIR/extensions/aws-auto-diagram/
extension_dev          entr watcher, scoped to extension dir only
```

## Combo Commands

```
all     Sequential: symbols_build → symbols_install → templates_install → extension_install
clean   Parallel-safe: symbols_clean + templates_clean + extension_clean
```

`symbols_clean_cache` is deliberately excluded from `clean` because rebuilding from the zip is slow.

## Testing

Tests live inside RUNME.sh as regular namespaced tasks — no separate test file.

### INKSCAPE_DIR override

`INKSCAPE_DIR` is set via `${INKSCAPE_DIR:-<detected>}`, allowing tests to override it with a tmpdir. This is the key enabler for all install/clean tests.

### Test tasks

```
test_usage          Assert all 11 commands appear in usage output
test_inkscape_dir   Assert path resolves correctly for current OS
test_install        Override INKSCAPE_DIR to tmpdir, run templates_install
                    and extension_install, assert expected dirs/files exist.
                    Optionally test symbols_install if target/ exists (skip otherwise).
                    Cleans up tmpdir after.
test                Runs all test_* tasks sequentially
```

### What is NOT tested

- `symbols_build` — requires the 11MB zip and network access (git clone). Too heavy for a unit test.
- `extension_dev` — interactive `entr` process, not meaningfully testable.
- Individual `clean` and `rm` operations — if the path is correct (validated by `test_inkscape_dir` and `test_install`), `rm` works.

## Key Decisions

- **rsync for symbols and templates** (carried over from Makefile) — handles incremental updates well
- **cp -av for extension** (carried over from existing RUNME.sh) — simple directory copy
- **ASSETS_ZIP variable at top** — same pinned zip filename as current Makefile
- **extension_dev stays scoped to extension dir** — uses `find` + `entr` pattern from existing RUNME.sh
