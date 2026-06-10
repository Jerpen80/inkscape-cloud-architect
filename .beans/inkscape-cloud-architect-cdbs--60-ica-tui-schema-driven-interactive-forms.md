---
# inkscape-cloud-architect-cdbs
title: '60 ica TUI: schema-driven interactive forms'
status: todo
type: task
created_at: 2026-06-10T13:27:32Z
updated_at: 2026-06-10T13:27:32Z
parent: inkscape-cloud-architect-muex
blocked_by:
    - inkscape-cloud-architect-3k05
    - inkscape-cloud-architect-ejab
---

Add an interactive TUI layer on top of the ica CLI — forms/menus generated from the config schema so users can discover and tune the ~120 options visually, then render.

Scope:
- Textual-based TUI (`ica tui` or auto-launch when no subcommand given).
- Forms generated FROM the config-schema (bean 11) — every field's type/range/help/preset-varying default drives a widget. No hand-maintained form ↔ schema drift.
- Preview/render from within the TUI; pick account-data, region, theme, layout mode.

Part of epic muex. Depends on: 40 safe-io, 50 cloudia-puller (full pipeline available to drive interactively). Ships in v1.5.0.
