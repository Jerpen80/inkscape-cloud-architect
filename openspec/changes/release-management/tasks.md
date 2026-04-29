## 1. Changelog

- [ ] 1.1 Reformat `CHANGELOG.md` to Keep a Changelog format with `[Unreleased]` section, preserving existing entries as retroactive history
- [ ] 1.2 Add comparison links at the bottom

## 2. Release Script

- [ ] 2.1 Create `RUNME.d/60-release.sh` with `release` command — parse and validate argument (major/minor/patch)
- [ ] 2.2 Detect VCS (jj vs git)
- [ ] 2.3 Read current version from latest git tag and bump according to semver
- [ ] 2.4 Validate `[Unreleased]` section has entries
- [ ] 2.5 Replace `[Unreleased]` with new version heading, add fresh `[Unreleased]`
- [ ] 2.6 Update comparison links
- [ ] 2.7 Commit and tag (git and jj paths)
- [ ] 2.8 Push commit and tags to remote (git and jj paths)
- [ ] 2.9 Create GitHub Release via `gh release create` with changelog section as body
- [ ] 2.10 Print summary
