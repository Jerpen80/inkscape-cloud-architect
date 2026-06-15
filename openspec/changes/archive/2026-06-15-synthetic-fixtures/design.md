## Context

`cloudia_parser` reads a fixed set of `<service>-<call>.json` files from
`<data_dir>/<region>/`, and uses only a **small, known subset** of fields from each
(e.g. VPCs need `Vpcs[].{VpcId, CidrBlock, IsDefault, Tags}`; subnets need
`Subnets[].{SubnetId, VpcId, CidrBlock, AvailabilityZone, MapPublicIpOnLaunch}`).
So a synthetic fixture can be **tiny hand-authored JSON**, not a full AWS dump.

`account-data/` is gitignored (leak guard), so the fixture lives under
`extensions/aws-auto-diagram/tests/fixtures/` (committable). No real data is touched.

## Goals / Non-Goals

**Goals:**
- One comprehensive, provably-synthetic account that exercises every renderer.
- A structural regression test (render → assert shape) wired into `test_all`.
- Customer-data-free testing; a safe substrate for the z23q restructure.

**Non-Goals:**
- Byte-exact golden SVGs (structural assertions instead — low churn).
- Output-guard / read-side data-detection / demo-mode (see proposal Non-goals).

## Decisions

### D1. Hand-author, never sanitize
Author the JSON by hand with fabricated identifiers. Sanitizing a real dump risks
missing an id/cidr/arn/tag — which is precisely how the 2026-06-09 leak happened.
The parser's field needs are small enough that hand-authoring is straightforward.

Fake-identifier discipline (must never collide with real AWS):
- account: `000000000000`
- vpc/subnet/etc: `vpc-00000000000000001`, `subnet-00000000000000001`, …
- CIDRs: RFC1918 `10.0.0.0/16`, subnets `10.0.x.0/24`
- names/domains: `demo-*`, `example.test` (RFC 6761 reserved)

### D2. One comprehensive multi-region account
```
  tests/fixtures/synthetic-account/
    eu-west-1/
      ec2-describe-vpcs.json            (1 non-default VPC)
      ec2-describe-subnets.json         (public + private, 2 AZs)
      ec2-describe-instances.json       (≥1 running EC2)
      ec2-describe-network-interfaces.json
      elbv2-describe-load-balancers.json
      rds-describe-db-instances.json
      elasticache-describe-cache-clusters.json
      eks-list-clusters.json + eks-describe-cluster/<name>
      lambda-list-functions.json
      autoscaling-describe-auto-scaling-groups.json
      dynamodb-list-tables.json
    us-east-1/                          (global / Edge zone)
      s3-list-buckets.json
      cloudfront-list-distributions.json
      route53-list-hosted-zones.json    (public + private)
```
Single-region render targets `eu-west-1`; multi-region uses `region=all`.

### D3. Structural assertions, not byte-exact
The test renders the fixture and asserts the SVG's *shape*:
- expected layers exist (Edge, Accounts, VPCs, Subnets, EC2, Load Balancers, EKS,
  Lambda, Database, Auto Scaling Groups, NAT Gateways, S3, DynamoDB, Legend…)
- expected element signatures present (≥1 EKS span-line, S3 card, DynamoDB card,
  N subnet rects, an account rect, an Edge zone)
Rationale: survives cosmetic layout tweaks (layout engine is actively changing);
still fails loudly if a renderer breaks. **The assertion list is also the coverage
proof** — if the fixture omitted a resource, its assertion would fail.

### D4. No-pytest, RUNME-wired
Test is a self-checking Python script (`tests/test_render_fixture.py`) run via
`./RUNME.sh test_render_fixture`, added to `test_all` — matching the existing
`test_config_schema` / `test_ica_cli` convention. It parses the rendered SVG
string (engine returns it) and checks for the expected layer labels / element
markers.

## Risks / Trade-offs

- **Fixture omits a renderer silently** → mitigated by D3: the per-renderer
  assertion fails if its resource isn't in the fixture (coverage = the test).
- **Fake IDs accidentally realistic** → mitigated by D1 conventions (all-zeros ids,
  RFC1918 CIDRs, `.test` domains); a quick scan asserts no 12-digit id other than
  `000000000000` appears in the fixture.
- **Structural assertions too loose** (pass even if layout subtly wrong) → accepted
  trade-off vs byte-brittleness; byte-exact goldens can be added later (e.g. to
  guard the z23q refactor) without changing the fixture.
- **Renderers may need fields not yet known** → during apply, render the fixture
  and iterate until every renderer fires; the parser source is the field spec.

## Migration Plan
1. Author the fixture JSON per D2, fake IDs per D1.
2. Render it (`engine.render`) single + multi-region; iterate until every renderer fires.
3. Write `test_render_fixture.py` with the D3 structural assertions; wire into RUNME.
4. Verify `test_all` green; confirm no real identifiers in the fixture.

## Open Questions
- Exact element markers to assert per renderer (resolve while rendering — read the actual SVG output).
- Whether to assert on layer *labels* (`inkscape:label`) vs element classes — pick whichever is stable in the output.
