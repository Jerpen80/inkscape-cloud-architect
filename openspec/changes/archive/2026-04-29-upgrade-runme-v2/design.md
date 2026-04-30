# Design: Upgrade RUNME.sh to v2.0.0 with RUNME.d

## v2 Boilerplate

The v2 framework line replaces v1. Key additions:
- `RUNME_DIR` built into framework (replaces our custom `SCRIPT_DIR`)
- Auto-sources `RUNME.d/*.sh` in alphabetical order before `runme()` is called

```bash
#!/usr/bin/env bash
#(C)2019-2026 Pim Snel - https://github.com/mipmip/RUNME.sh
CMDS=(); DESC=(); NARGS=$#; ARG1=$1;make_command(){ CMDS+=($1);DESC+=("$2");};usage(){ printf "\nUsage: %s [command]\n\nCommands:\n" $0;line="              ";for ((i=0;i<=$((${#CMDS[*]}-1));i++));do printf "  %s %s ${DESC[$i]}\n" ${CMDS[$i]} "${line:${#CMDS[$i]}}";done;echo;};RUNME_DIR="$(cd "$(dirname "$0")" && pwd)";if [ -d "$RUNME_DIR/RUNME.d" ]; then for _f in "$RUNME_DIR/RUNME.d"/*.sh; do [ -f "$_f" ] && source "$_f"; done;fi;runme(){ if test $NARGS -eq 1; then eval "$ARG1"||usage;else usage;fi;}
```

## Main RUNME.sh

Contains only:
- v2 boilerplate (line 1-3)
- Shared config: `ASSETS_ZIP`, `INKSCAPE_DIR` detection
- `runme` call at bottom

No task functions inline.

## RUNME.d Structure

```
RUNME.d/
├── 10-symbols.sh       symbols_build, symbols_install, symbols_clean, symbols_clean_cache
├── 20-templates.sh     templates_install, templates_clean
├── 30-extension.sh     extension_install, extension_clean, extension_dev
├── 40-combo.sh         all, clean
└── 50-tests.sh         __echo_inkscape_dir, test_usage, test_inkscape_dir, test_install, test_all
```

Numbered prefixes ensure sourcing order. This matters because:
- `40-combo.sh` calls functions from 10/20/30
- `50-tests.sh` calls functions from 10/20/30 and uses `__echo_inkscape_dir`

## Key Decisions

- **`SCRIPT_DIR` → `RUNME_DIR`**: All task files switch to `$RUNME_DIR` which is provided by the framework
- **Shared variables stay in RUNME.sh**: `INKSCAPE_DIR` and `ASSETS_ZIP` are set before RUNME.d files are sourced, so they're available to all task files
- **No shebangs in RUNME.d files**: They're sourced, not executed directly
- **`__echo_inkscape_dir` moves to tests**: It's only used by `test_inkscape_dir`, so it belongs in `50-tests.sh`
