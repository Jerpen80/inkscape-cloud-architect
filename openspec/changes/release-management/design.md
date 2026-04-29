## Context

The project has tags `v1.0.0` and `v1.1.0`, an informal CHANGELOG.md, and a RUNME.sh task runner. The reference release script from RUNME.sh project already handles both git and jj VCS. The GitHub remote is `mipmip/inkscape-cloud-architect`.

## Goals / Non-Goals

**Goals:**
- Keep a Changelog format with `[Unreleased]` section
- `release` command in RUNME.sh that automates the full release flow
- Works with both `git` and `jj` (Jujutsu)
- GitHub Release via `gh release create`

**Non-Goals:**
- CI/CD integration
- Automated changelog generation from commits
- NPM/PyPI publishing

## Decisions

### CHANGELOG.md format

Keep a Changelog format. Sections: Added, Changed, Deprecated, Removed, Fixed, Security. The `[Unreleased]` heading always exists at the top. Release script replaces it with `[X.Y.Z] - YYYY-MM-DD` and adds a fresh empty `[Unreleased]`.

Comparison links at the bottom:
```markdown
[Unreleased]: https://github.com/mipmip/inkscape-cloud-architect/compare/vX.Y.Z...HEAD
[X.Y.Z]: https://github.com/mipmip/inkscape-cloud-architect/compare/vPREV...vX.Y.Z
```

### Release as RUNME.d task

Place in `RUNME.d/60-release.sh` as a `release` command:
```bash
./RUNME.sh release <major|minor|patch>
```

This follows the existing task runner pattern and keeps the release script integrated.

### VCS detection (git vs jj)

Adapted from the reference script:
```bash
if jj root &>/dev/null; then
  VCS="jj"
elif git rev-parse --git-dir &>/dev/null; then
  VCS="git"
fi
```

For jj: `jj commit`, `jj git export`, `git tag`, `jj git push --change @-`, `git push --tags`
For git: `git add`, `git commit`, `git tag`, `git push`, `git push --tags`

### Starting version

Continue from `v1.1.0`. The reformatted CHANGELOG.md preserves the existing v2.0.0, v1.1.0, and v1.0.0 entries as retroactive history.

### Repo URL

```
REPO_URL="https://github.com/mipmip/inkscape-cloud-architect"
```

## Risks / Trade-offs

- [No validation of Unreleased content] → Script checks `[Unreleased]` has entries before releasing; exits with error if empty
- [Manual changelog entries] → Intentional; keeps it simple
