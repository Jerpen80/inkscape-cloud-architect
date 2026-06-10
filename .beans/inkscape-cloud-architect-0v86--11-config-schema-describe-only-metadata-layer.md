---
# inkscape-cloud-architect-0v86
title: '11 config schema: describe-only metadata layer'
status: completed
type: task
openspec-link: openspec/changes/archive/2026-06-10-config-schema
created_at: 2026-06-10T13:25:59Z
updated_at: 2026-06-10T13:55:00Z
parent: inkscape-cloud-architect-muex
---

Add a describe-only config schema so ICA's full option surface (~120 keys) becomes discoverable and validatable — the keystone the ica CLI/TUI consume for rich `--help`, `ica config list/explain`, and override validation.

A complete OpenSpec proposal already exists for this work: `openspec/changes/config-schema` (proposal + design + config-loading spec delta + tasks, validated). This bean tracks that change.

Key decisions (see the design.md): metadata-only Python descriptor (`ica_utils/config_schema.py`), defaults read FROM the unchanged `default-config.yaml` (no fourth source of truth), engine/flat key paths, `preset_varying` derived by comparing spaced vs dense, pure validation, coverage self-check. Behavior byte-identical — no engine change.

Part of epic muex. Blocks: 20 ica-cli-skeleton, 90 config-restructure. Ships in v1.2.0.
