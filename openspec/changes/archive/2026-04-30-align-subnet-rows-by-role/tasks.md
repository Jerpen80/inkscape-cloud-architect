## 1. Role Key Extraction

- [x] 1.1 Create `_subnet_role_key(subnet)` function in `resource_vpc.py` that strips AZ suffixes from subnet name to produce a role key
- [x] 1.2 Handle patterns: `_az[0-9]+`, `.[0-9][a-z]$`, `-{full-az-name}$`, full AZ name anywhere in suffix
- [x] 1.3 Fall back to CIDR block for unnamed subnets

## 2. Apply Sorting

- [x] 2.1 Sort each AZ group by role key before grid placement in `render_vpc_with_subnets`

## 3. Verify

- [x] 3.1 Run headless with us-east-2 (222222222222) — verified: datastore/private/public all align across columns
- [x] 3.2 Run headless with eu-west-1 (111111111111) — verified: dotted-name subnets render OK
- [x] 3.3 Run headless with us-west-2 (955922232824) — verified: region-suffix subnets render OK
