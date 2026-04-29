# Read VPCs and subnets from cloudia-reader-aws output

**Bean:** `.beans/inkscape-cloud-architect-q8co--the-extension-should-be-able-to-select-a-aws-data.md`

## Summary

Replace the hardcoded test-data.json with a cloudia-reader-aws data source. The user selects an account-data directory and region via the Inkscape extension dialog. The extension reads raw AWS API JSON files (ec2-describe-vpcs.json, ec2-describe-subnets.json), transforms them to the internal format, and renders VPCs and subnets.

## Motivation

- The extension currently reads from a hardcoded test-data.json with a custom format
- cloudia-reader-aws dumps real AWS account data to a well-structured directory tree
- Real customer data (CustomerA) is already available in this format
- The extension should work with any cloudia output, not just test data

## Scope

### In scope
- Add `.inx` params: account data directory (folder browser) and region (string input)
- New parser module to read cloudia directory structure (ec2-describe-vpcs.json, ec2-describe-subnets.json)
- Transform raw AWS API JSON to internal format
- Use `MapPublicIpOnLaunch` for public/private subnet detection (replaces name-based check)
- VPC name fallback: `Tags["Name"]` → `"{VpcId} ({CidrBlock})"`
- Subnet name fallback: `Tags["Name"]` → `"{SubnetId} ({CidrBlock})"`
- Pass VPC data (name, CIDR) to render_vpc (currently receives nothing)
- Remove test-data.json and parse_test_data

### Out of scope
- Rendering additional resource types beyond VPCs and subnets
- Dynamic region dropdown (not possible in .inx)
- Multi-region rendering in a single invocation

## Files

| Action | File |
|--------|------|
| Update | `extensions/aws-auto-diagram/aws-auto-diagram.inx` — add data_dir and region params |
| Update | `extensions/aws-auto-diagram/aws-auto-diagram.py` — replace parse_test_data with cloudia parser, wire up .inx params |
| Create | `extensions/aws-auto-diagram/ica_utils/cloudia_parser.py` — read and transform cloudia directory data |
| Update | `extensions/aws-auto-diagram/ica_utils/resource_vpc.py` — accept VPC props, use public flag for subnet type |
| Delete | `extensions/aws-auto-diagram/test-data.json` |
