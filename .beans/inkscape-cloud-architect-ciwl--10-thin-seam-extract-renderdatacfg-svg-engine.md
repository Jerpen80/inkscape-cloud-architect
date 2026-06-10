---
# inkscape-cloud-architect-ciwl
title: '10 thin seam: extract render(data,cfg)->svg engine'
status: todo
type: task
created_at: 2026-06-10T13:25:59Z
updated_at: 2026-06-10T13:25:59Z
parent: inkscape-cloud-architect-muex
---

Refactor the rendering engine so it can be called WITHOUT the Inkscape runtime — `render(account_data, config) -> svg`, no `inkex.EffectExtension` lifecycle, no blank-SVG mktemp dance.

This is the architectural keystone for the `ica` wrapper: one engine that all front-ends (Inkscape .inx, ica CLI, future TUI) call.

Scope (thin seam — inkex stays as the SVG-tree library, language stays Python):
- Split `aws-auto-diagram.py` `effect()` into: (a) inkex lifecycle wrapper, (b) symbol import, (c) pure render orchestration.
- Provide an `inkdoc`-like document object the engine draws into that does NOT require an EffectExtension.
- SNAG to solve: `import_defs_from_external_file_in_document()` reads `~/.config/inkscape/symbols/aws-architect/` — an Inkscape-install assumption that breaks headless. Decide where symbols live for a non-Inkscape user.

Part of epic muex. Depends (informational) on the config-schema OpenSpec change. Blocks: 20 ica-cli-skeleton. Ships in v1.2.0 (one shared version line).
