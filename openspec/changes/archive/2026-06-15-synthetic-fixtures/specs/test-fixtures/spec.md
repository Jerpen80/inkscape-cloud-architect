## ADDED Requirements

### Requirement: Synthetic account-data fixture
The project SHALL provide a committed synthetic account-data fixture containing only
fabricated identifiers, sufficient to exercise every resource renderer.

#### Scenario: Fixture is committable and synthetic
- **WHEN** the fixture is inspected
- **THEN** it SHALL live under a committable path (not the gitignored `account-data/`)
- **AND** it SHALL contain only fabricated identifiers (e.g. account `000000000000`, `vpc-0000…`, RFC1918 CIDRs, `demo-*`/`.test` names)
- **AND** it SHALL contain no real customer identifiers

#### Scenario: Fixture covers all renderers
- **WHEN** the fixture is rendered
- **THEN** it SHALL include resources that exercise every renderer: VPC, subnet (public and private), EC2, load balancer, RDS/ElastiCache, EKS, Lambda, ASG, NAT, DynamoDB, and global S3 / CloudFront / Route 53 (Edge zone)

### Requirement: Structural render regression test
The project SHALL provide a test that renders the synthetic fixture and asserts the
output's structure (layers and element signatures), not exact bytes.

#### Scenario: Single-region render structure
- **WHEN** the fixture is rendered for its real region
- **THEN** the test SHALL assert the expected layers are present and the expected element signatures appear (e.g. an account rect, subnet rects, an EKS span-line, an S3 card, a DynamoDB card, an Edge zone)

#### Scenario: Multi-region render
- **WHEN** the fixture is rendered with `region=all`
- **THEN** the test SHALL assert a multi-region render succeeds and produces region rectangles

#### Scenario: Structural, not byte-exact
- **WHEN** a cosmetic layout value changes (e.g. a gap or padding)
- **THEN** the structural test SHALL still pass, as long as the expected layers and element signatures remain present

#### Scenario: Renderer regression is caught
- **WHEN** a renderer stops emitting its element (a regression)
- **THEN** the corresponding structural assertion SHALL fail

### Requirement: Test runs customer-data-free and via the task runner
The render regression test SHALL require no real account-data and SHALL run via the
project task runner alongside the other tests.

#### Scenario: No customer data needed
- **WHEN** the render regression test runs
- **THEN** it SHALL use only the synthetic fixture and SHALL NOT read any real account-data

#### Scenario: Wired into the suite
- **WHEN** `./RUNME.sh test_all` runs
- **THEN** it SHALL include the render regression test
