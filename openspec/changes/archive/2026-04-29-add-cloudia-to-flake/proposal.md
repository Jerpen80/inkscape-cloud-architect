# Add cloudia-reader-aws to flake

**Bean:** `.beans/inkscape-cloud-architect-rn3b--include-cloudia-in-the-flake-so-it-can-be-used-as.md`

## Summary

Add `cloudia-reader-aws` as a flake input and make it available in the dev shell. Also modernize the flake to support multiple systems (linux + darwin) instead of hardcoded x86_64-linux.

## Motivation

- The aws-auto-diagram extension will consume output from cloudia-reader-aws (see bean q8co)
- Developers need `cloudia-reader-aws` available in their shell to generate the data the extension reads
- The flake currently only supports x86_64-linux, but the project now supports macOS too (cross-platform RUNME.sh)

## Scope

### In scope
- Add `cloudia-reader-aws` flake input
- Switch to `forAllSystems` pattern (x86_64-linux, aarch64-linux, x86_64-darwin, aarch64-darwin)
- Include `cloudia-reader-aws` in devShell packages
- Keep nixpkgs on unstable, keep python3 + inkex

### Out of scope
- Extension code changes to actually read cloudia output (that's bean q8co)
- Changing nixpkgs channel

## Files

| Action | File |
|--------|------|
| Update | `/flake.nix` |
