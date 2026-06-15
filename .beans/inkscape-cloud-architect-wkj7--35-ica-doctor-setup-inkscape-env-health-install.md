---
# inkscape-cloud-architect-wkj7
title: '35 ica doctor + setup: inkscape env health & install'
status: completed
type: task
priority: normal
openspec-link: openspec/changes/archive/2026-06-15-ica-doctor
created_at: 2026-06-12T12:04:59Z
updated_at: 2026-06-15T14:50:00Z
parent: inkscape-cloud-architect-muex
blocked_by:
    - inkscape-cloud-architect-fy5b
---

Environment management for the Inkscape GUI integration — split out of bean 20 (brhe) during explore.

The `ica` CLI itself is self-contained ("just works" with bundled symbols, no setup). But the Inkscape *dialog* path still needs assets installed into the user's Inkscape dir. This bean owns checking and fixing that.

Commands:
- `ica doctor` — check whether the install is healthy and report clearly:
  - symbols present at `$INKSCAPE_DIR/symbols/aws-architect/`
  - templates present at `$INKSCAPE_DIR/templates/aws-architect/`
  - extension present at `$INKSCAPE_DIR/extensions/aws-auto-diagram/`
  - inkex importable
  - On a broken/missing install, tell the user exactly what to install, or offer/suggest `ica setup`.
- `ica setup` (name TBD) — install symbols/templates/extension into `$INKSCAPE_DIR` for end users (the user-facing replacement for RUNME.sh `all`, which is dev-only).

Notes:
- This is "Tier 2" (environment/install management); brhe is "Tier 1" (the CLI verbs render/initconf). See brhe proposal.
- Symbols are MIT-licensed (Will Thames / awslabs), so bundling/redistribution is allowed.
- `$INKSCAPE_DIR` resolution already exists in RUNME (macOS vs Linux); reuse that logic.

Part of epic muex. Depends on: 30 nix-package-ica (the package ships the assets `setup` installs). Relates to: 20 ica CLI. Ships after v1.2.0.
