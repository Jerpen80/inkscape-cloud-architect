## 1. Author the synthetic fixture

- [x] 1.1 Created `tests/fixtures/synthetic-account/eu-west-1/`: `ec2-describe-vpcs` (1 non-default VPC), `ec2-describe-subnets` (2 public + 2 private across eu-west-1a/1b), `ec2-describe-instances` (running + a stopped one to test exclusion), `ec2-describe-network-interfaces` (NAT gateway ENI)
- [x] 1.2 Added `elbv2-describe-load-balancers`, `rds-describe-db-instances` (AZ-matched subnet group), `elasticache-describe-cache-clusters`, `autoscaling-describe-auto-scaling-groups`, `dynamodb-list-tables`, `lambda-list-functions` (vpc + non-vpc)
- [x] 1.3 Added `eks-list-clusters.json` + `eks-describe-cluster/demo-cluster` (no extension — parser reads the path literally; status ACTIVE)
- [x] 1.4 Created `us-east-1/`: `s3-list-buckets`, `cloudfront-list-distributions`, `route53-list-hosted-zones` (public + private) — Edge zone renders
- [x] 1.5 Only fabricated identifiers: account `000000000000`, `vpc-/subnet-/i-/nat-0000…`, RFC1918 `10.x` CIDRs, `demo-*` names, `.test` domains

## 2. Make the fixture render correctly

- [x] 2.1 Rendered `eu-west-1` via `engine.render`; iterated until every renderer fired (fixed ASG: its instances must be real running instances in the EC2 file, else the ASG wraps nothing)
- [x] 2.2 Rendered `region=all`; multi-region + Regions layer + global/edge confirmed
- [x] 2.3 Rendered to `/tmp` during iteration; only the JSON inputs are committed

## 3. Structural regression test

- [x] 3.1 Added `tests/test_render_fixture.py` (no-pytest): asserts all 16 expected layers + 15 per-renderer element markers (vpc, subnets, ec2, lb, rds, elasticache, eks, lambda, asg, nat, dynamodb, account, cloudfront, route53) — structural, not byte-exact
- [x] 3.2 Multi-region assertion: `Regions` layer present for `region=all`; also asserts the stopped instance is excluded
- [x] 3.3 Coverage proof demonstrated live: when the ASG had no rendered instances, its assertion failed loudly — confirming a missing/removed resource fails the test

## 4. Wire in + verify

- [x] 4.1 Added `test_render_fixture` to `RUNME.d/50-tests.sh` and `test_all`
- [x] 4.2 `./RUNME.sh test_all` → all tests passed
- [x] 4.3 Fixture scan: no real customer identifiers; all long digit-runs are zero-prefixed fake ids; only `.test` domains
- [x] 4.4 Inkscape extension + `.inx` + `ica_utils` unchanged (git diff vs HEAD empty)
