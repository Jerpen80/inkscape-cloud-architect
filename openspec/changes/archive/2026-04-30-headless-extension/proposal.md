# Fix flake Python environment and add headless extension runner

**Bean:** `.beans/inkscape-cloud-architect-0g22--find-way-to-run-extension-task-headless.md`

## Summary

Fix the flake so inkex and its dependencies are available on the correct Python, then add a RUNME.sh task to run the extension headless with data_dir and region arguments.

## Motivation

- The devshell's `python3.withPackages` includes inkex but gets shadowed by cloudia-reader-aws's Python 3.11 in PATH
- inkex also needs lxml and tinycss2 which aren't listed in `withPackages`
- Running the extension headless enables CI/CD, scripting, and fast iteration without the Inkscape GUI

## Scope

### In scope
- Fix flake.nix: add lxml, tinycss2 to withPackages; force withPackages Python first in PATH via shellHook
- Add `extension_run` RUNME.sh task that runs the extension headless via direct Python invocation
- Verify `python3 -c "import inkex"` works in devshell

### Out of scope
- Fixing cloudia-reader-aws packaging upstream (future: expose as Python package for Option B)
- Inkscape CLI action-based invocation (works but can't pass params)

## Files

| Action | File |
|--------|------|
| Update | `/flake.nix` |
| Create | `/RUNME.d/35-extension-run.sh` |
