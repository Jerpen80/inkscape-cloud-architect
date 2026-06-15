---
# inkscape-cloud-architect-z23q
title: '90 config restructure: single source of truth (debt)'
status: completed
type: task
priority: normal
openspec-link: openspec/changes/archive/2026-06-15-config-restructure
created_at: 2026-06-10T13:27:32Z
updated_at: 2026-06-15T14:20:00Z
parent: inkscape-cloud-architect-muex
blocked_by:
    - inkscape-cloud-architect-0v86
---

Deferred config debt: collapse the three drifting sources of defaults into one, and fix the misfiled style keys. Safe to do ONLY after the config-schema (bean 11) exists to golden-test against.

Findings from explore (2026-06-09/10):
- THREE sources of default values disagree: YAML spaced preset, YAML dense preset, and ~90 inline `config.get(key, fallback)` calls in resource_*.py (e.g. resource_ec2 defaults icon_scale=0.5 while shipped spaced uses 1.0).
- 18 of the 101 layout keys are IDENTICAL across spaced/dense — they are misfiled STYLE (stroke colors, dash patterns, span-line styles, availability_zone.enabled, label_prefix), not density knobs.
- 83 keys genuinely differ → the real density set.

Scope:
- Make schema defaults canonical (defaults = spaced; dense becomes a diff overlay listing only the 83 differing keys).
- Promote the 18 style keys out of presets.
- Remove the inline `.get(k, fallback)` shadow defaults from resource modules.
- Guard with golden-SVG regression tests enabled by the schema + synthetic fixtures.

Independent of the front-end critical path. Part of epic muex. Depends on: 11 config-schema. No fixed version — when convenient.
