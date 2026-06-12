## 1. Changelog

- [x] 1.1 Reformat `CHANGELOG.md` to Keep a Changelog format with `[Unreleased]` section, preserving existing entries as retroactive history (the untagged "v2.0.0 AWS Auto Diagram" content was moved into `[Unreleased]` and released as v2.0.0)
- [x] 1.2 Add comparison links at the bottom

## 2. Release Script

- [x] 2.1 Create `RUNME.d/60-release.sh` with `release` command — parse and validate argument (major/minor/patch)
- [x] 2.2 Detect VCS (jj vs git)
- [x] 2.3 Read current version from latest git tag and bump according to semver (verified: v1.1.0 + major → v2.0.0)
- [x] 2.4 Validate `[Unreleased]` section has entries (exits if empty)
- [x] 2.5 Replace `[Unreleased]` with new version heading, add fresh `[Unreleased]`
- [x] 2.6 Update comparison links
- [x] 2.7 Commit and tag (git and jj paths) — jj path also advances the `main` bookmark onto the release commit before tagging
- [x] 2.8 Push commit and tags to remote (git and jj paths)
- [x] 2.9 Create GitHub Release via `gh release create` with changelog section as body
- [x] 2.10 Print summary
  - Exercised live: `./RUNME.sh release major` cut **v2.0.0** — tag pushed, main advanced (85e6da3 → 19bda27a), GitHub Release created at https://github.com/mipmip/inkscape-cloud-architect/releases/tag/v2.0.0
