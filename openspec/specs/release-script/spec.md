# release-script Specification

## Purpose
TBD - created by archiving change release-management. Update Purpose after archive.
## Requirements
### Requirement: Release command in RUNME.sh
The project SHALL have a `release` command available via `./RUNME.sh release <major|minor|patch>`.

#### Scenario: Release invocation
- **WHEN** `./RUNME.sh release minor` is run
- **THEN** it SHALL bump the minor version, update CHANGELOG.md, commit, tag, push, and create a GitHub Release

### Requirement: Semver version bumping
The release command SHALL read the current version from the latest git tag and bump according to semver.

#### Scenario: Minor bump
- **WHEN** current tag is `v1.1.0` and bump type is `minor`
- **THEN** the new version SHALL be `v1.2.0`

### Requirement: Changelog update on release
The release command SHALL replace `[Unreleased]` with the new version heading and add a fresh `[Unreleased]` section.

#### Scenario: Changelog transformed
- **WHEN** a release is cut
- **THEN** `## [Unreleased]` SHALL become `## [X.Y.Z] - YYYY-MM-DD` and a new empty `## [Unreleased]` SHALL be added above it

### Requirement: Unreleased validation
The release command SHALL refuse to release if the `[Unreleased]` section has no entries.

#### Scenario: Empty unreleased
- **WHEN** `[Unreleased]` has no content
- **THEN** the release command SHALL exit with an error

### Requirement: Git and jj support
The release command SHALL work with both git and jj (Jujutsu) VCS.

#### Scenario: Git workflow
- **WHEN** running in a git repository
- **THEN** the release command SHALL use `git add`, `git commit`, `git tag`, `git push`

#### Scenario: jj workflow
- **WHEN** running in a jj repository
- **THEN** the release command SHALL use `jj commit`, `jj git export`, `git tag`, `jj git push`

### Requirement: GitHub Release creation
The release command SHALL create a GitHub Release via `gh release create` with the version's changelog section as the body.

#### Scenario: GitHub Release
- **WHEN** a release is completed
- **THEN** a GitHub Release SHALL be created with the tag and changelog content

