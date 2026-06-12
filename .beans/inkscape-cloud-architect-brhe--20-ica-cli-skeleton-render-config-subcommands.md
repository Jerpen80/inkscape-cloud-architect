---
# inkscape-cloud-architect-brhe
title: '20 ica CLI skeleton: render + config subcommands'
status: completed
type: task
priority: normal
openspec-link: openspec/changes/archive/2026-06-12-ica-cli
created_at: 2026-06-10T13:26:17Z
updated_at: 2026-06-12T12:30:00Z
parent: inkscape-cloud-architect-muex
blocked_by:
    - inkscape-cloud-architect-ciwl
    - inkscape-cloud-architect-0v86
---

Build the `ica` command itself — the user-friendly CLI front-end (short name: ica) that co-workers run on NixOS.

v1.2.0 surface:
- `ica render <data_dir> <region> [--theme --layout-mode --account-name -o out.svg]` — calls the thin-seam engine natively (no subprocess, no blank-SVG dance).
- `ica config list` — all ~120 keys with values/units (from the schema).
- `ica config explain <key>` — type, range, help, preset-varying defaults.
- `ica config validate <file.yaml>` — validate a user override against the schema.
- `--version`, `--help`, verbosity flags, shell autocomplete (per bean muex).

Decisions: Python; framework Typer (generates --help from type hints) is the leading candidate, Textual reserved for the later TUI bean. CLI reads from the config-schema (bean 11) and calls the engine (bean 10).

Part of epic muex. Depends on: 10 thin seam, 11 config schema. Blocks: 30 nix-package-ica. Ships in v1.2.0.
