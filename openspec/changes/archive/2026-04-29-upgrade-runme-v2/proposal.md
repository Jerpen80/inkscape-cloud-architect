# Upgrade RUNME.sh to v2.0.0 with RUNME.d structure

**Bean:** `.beans/inkscape-cloud-architect-i28w--upgrade-the-runmesh-to-the-latest-version-from-git.md`

## Summary

Upgrade the RUNME.sh boilerplate from v1 (2019-2022) to v2.0.0 (2019-2026) and split inline tasks into `RUNME.d/` subdirectory files grouped by deliverable.

## Motivation

- The v2 framework adds built-in `RUNME_DIR` and `RUNME.d/` auto-sourcing
- The current RUNME.sh is ~200 lines with all tasks inline — splitting into files improves maintainability
- The bean explicitly asks for RUNME.d subdir structure

## Scope

### In scope
- Upgrade boilerplate to v2.0.0 (copyright, `RUNME_DIR`, `RUNME.d/` sourcing)
- Replace custom `SCRIPT_DIR` with framework's `RUNME_DIR`
- Move tasks into `RUNME.d/*.sh` files grouped by deliverable
- Keep shared config (`INKSCAPE_DIR`, `ASSETS_ZIP`) in main `RUNME.sh`

### Out of scope
- Changing any task logic (install paths, build commands, test assertions)
- Adding new tasks

## Files

| Action | File |
|--------|------|
| Update | `/RUNME.sh` — v2 boilerplate + shared config only |
| Create | `/RUNME.d/10-symbols.sh` |
| Create | `/RUNME.d/20-templates.sh` |
| Create | `/RUNME.d/30-extension.sh` |
| Create | `/RUNME.d/40-combo.sh` |
| Create | `/RUNME.d/50-tests.sh` |
