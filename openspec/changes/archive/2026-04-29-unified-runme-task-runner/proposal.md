# Unified RUNME.sh Task Runner

## Summary

Replace the split Makefile + nested RUNME.sh with a single RUNME.sh at the project root. The project has three deliverables — symbols, templates, and the extension — each with clearly namespaced tasks. The `all` command enforces correct ordering (symbols must be built before the extension can be installed).

## Motivation

- Two task runners (Makefile at root, RUNME.sh inside extension dir) is confusing
- No enforcement of the dependency: symbols must exist before the extension is useful
- The extension install is Linux-only while the Makefile supports macOS
- No single entry point for new contributors

## Scope

### In scope
- Create `/RUNME.sh` at project root with all tasks from both files
- Cross-platform INKSCAPE_DIR detection (macOS + Linux) for all tasks
- Namespaced task names: `symbols_*`, `templates_*`, `extension_*`
- `all` command with enforced ordering: symbols_build → symbols_install → templates_install → extension_install
- `clean` command covering all three deliverables
- Delete `/Makefile`
- Delete `/extensions/aws-auto-diagram/RUNME.sh`
- Update `/README.md` to reference RUNME.sh instead of make

### Out of scope
- Windows support
- Changing build logic (build.sh, files_to_svg.py stay as-is)
- Extension dev watcher scope expansion

## Files

| Action | File |
|--------|------|
| Create | `/RUNME.sh` |
| Delete | `/Makefile` |
| Delete | `/extensions/aws-auto-diagram/RUNME.sh` |
| Update | `/README.md` |
