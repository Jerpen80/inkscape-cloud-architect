## Why

The project has an informal CHANGELOG.md and two tags (v1.0.0, v1.1.0) but no release script or formal process. As features are rapidly added (multi-region, S3, DynamoDB, NAT gateways, legend, etc.), there's no automated way to cut a release, bump the version, update the changelog, and create a GitHub Release.

Adapted from [RUNME.sh release-workflow](file:///home/pim/cDevOps/RUNME.sh/openspec/changes/archive/2026-04-20-release-workflow/proposal.md).

Bean: [inkscape-cloud-architect-06i4](.beans/inkscape-cloud-architect-06i4--release-management-task.md)

## What Changes

- Reformat `CHANGELOG.md` to Keep a Changelog format with an `[Unreleased]` section and comparison links
- Add a `release` command to `RUNME.sh` (via `RUNME.d/`) that bumps the semver version, updates the changelog, tags the commit, pushes, and creates a GitHub Release
- Support both git and jj (Jujutsu) VCS workflows
- Establish semver versioning continuing from the current `v1.1.0` tag

## Capabilities

### New Capabilities
- `changelog`: CHANGELOG.md in Keep a Changelog format with Unreleased placeholder and comparison links
- `release-script`: RUNME.d release task to bump version, update changelog, create git tag, push, and create GitHub Release

### Modified Capabilities

## Impact

- Modified: `CHANGELOG.md` (reformatted to Keep a Changelog format)
- New: `RUNME.d/60-release.sh` (release command)
- No code changes to the extension itself
