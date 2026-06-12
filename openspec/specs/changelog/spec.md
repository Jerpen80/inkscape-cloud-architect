# changelog Specification

## Purpose
TBD - created by archiving change release-management. Update Purpose after archive.
## Requirements
### Requirement: Keep a Changelog format
CHANGELOG.md SHALL follow Keep a Changelog format with an `[Unreleased]` section at the top.

#### Scenario: Unreleased section exists
- **WHEN** CHANGELOG.md is read
- **THEN** it SHALL contain a `## [Unreleased]` heading above all versioned entries

#### Scenario: Comparison links
- **WHEN** CHANGELOG.md is read
- **THEN** it SHALL contain comparison links at the bottom for each version and the Unreleased section

