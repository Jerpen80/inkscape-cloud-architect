---
# inkscape-cloud-architect-fy5b
title: '30 nix package ica: installable flake output'
status: todo
type: task
created_at: 2026-06-10T13:26:33Z
updated_at: 2026-06-10T13:26:33Z
parent: inkscape-cloud-architect-muex
blocked_by:
    - inkscape-cloud-architect-brhe
---

Package `ica` as a flake output so co-workers install and run it on NixOS — the distribution goal.

Scope:
- Expose `packages.ica` and `apps.ica` (or `packages.default`) in flake.nix so `nix run github:mipmip/inkscape-cloud-architect#ica` and `nix profile install` work.
- Bundle the Python engine + ica CLI + inkex + lxml/tinycss2 deps (reuse the pythonEnv pattern from the 0g22 flake fix; avoid the cloudia Python-version PATH clash).
- Ensure symbols are available to a headless install (ties into the seam SNAG — where do AWS symbols live for a non-Inkscape user?).
- Co-worker usage target: `inputs.ica.url = "github:mipmip/inkscape-cloud-architect?ref=v1.2.0";` (one shared version line).

Note: packaging is distinct from release. Version bumping / tagging / changelog / GitHub Release is the existing release-management proposal (bean 06i4), which stands as-is and cuts every release on the shared semver line.

Part of epic muex. Depends on: 20 ica CLI. Blocks: 40 safe-io, 50 cloudia-puller. Ships in v1.2.0 (first co-worker drop).
