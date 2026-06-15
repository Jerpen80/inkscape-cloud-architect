## Why

Every golden / byte-identical test built this session (config-schema, thin-seam,
ica-cli, nix-package) rendered **real customer account-data** to `/tmp` and eyeballed
byte counts, because the project has no synthetic test data. That is both a leak risk
(the 2026-06-09 incident originated from real account-data + rendered SVGs in the repo)
and a test-hygiene gap: there is no committable, repeatable regression suite, and the
upcoming config restructure (bean z23q) has nothing safe to golden-test against.

This change adds a **comprehensive, provably-synthetic account-data fixture** and a
**structural regression suite** that renders it and asserts the output's shape — so the
codebase can be tested with zero customer data.

Bean: [inkscape-cloud-architect-3k05](../../../.beans/inkscape-cloud-architect-3k05--40-safe-io-defaults-synthetic-fixtures.md)
(epic [muex](../../../.beans/inkscape-cloud-architect-muex--we-need-a-wrapper-which-is-userfriendly.md);
narrowed during explore to the fixture + golden-suite — see Non-goals.)

## What Changes

- Add `extensions/aws-auto-diagram/tests/fixtures/synthetic-account/` — one hand-authored, comprehensive synthetic account exercising **every** renderer, across multiple regions:
  - a real region (e.g. `eu-west-1`) with VPC, subnets (public/private), EC2, load balancers, RDS/ElastiCache, EKS, Lambda, ASG, NAT, DynamoDB
  - global/edge data (S3, CloudFront, Route 53) so the Edge zone renders
  - all identifiers **provably fake**: account `000000000000`, `vpc-0000…`, RFC1918 CIDRs (`10.x`), names `demo-*`. No real data is ever touched (hand-authored, not sanitized).
- Add a **structural regression test**: render the fixture (single-region and `region=all`) and assert the output's shape — expected layers present, expected element types/counts (e.g. ≥1 EKS span-line, N subnet rects, S3/DynamoDB cards). Assertions are **structural, not byte-exact**, so they survive cosmetic layout tweaks (the layout engine is still evolving — `plot-internet-gateways` is open). The same assertions double as proof the fixture exercises every renderer.
- Wire the new test into `RUNME.d/50-tests.sh` (`test_render_fixture`, added to `test_all`), following the no-pytest self-checking-script convention.

### Non-goals (explicitly dropped from the original bean)
- **Output-side guard** ("refuse writing `-o` into the git work tree") — largely already shipped this session (`.gitignore` guards + required `-o`); not pursued here.
- **Read-side data detection** ("warn when account-data looks real") — fuzzy heuristic, deferred to a separate bean if ever wanted.
- **Demo mode** (shipping the fixture in the package for `ica render --demo`) — tests-only for now; a future bean.
- No byte-exact golden SVGs committed (structural assertions instead).

## Capabilities

### New Capabilities
- `test-fixtures`: A synthetic account-data fixture and a structural regression test that renders it and verifies the output shape, enabling customer-data-free testing.

### Modified Capabilities
<!-- None. The engine, parser, and renderers are unchanged; this adds test data + a test. -->

## Impact

- **New**: `tests/fixtures/synthetic-account/` (hand-authored JSON, fake IDs) under `extensions/aws-auto-diagram/`.
- **New**: `tests/test_render_fixture.py` (no-pytest structural assertions) + a `test_render_fixture` command in `RUNME.d/50-tests.sh` (added to `test_all`).
- **Unchanged**: engine, `cloudia_parser`, all `resource_*`, config — this change only adds test data and a test.
- **Unblocks**: bean z23q (config restructure) gets a safe golden/structural substrate; ends the "render real customer data to /tmp" testing pattern.
- **Leak-safety**: the fixture lives under `tests/` (committable; `account-data/` is gitignored) and contains only fabricated identifiers.
