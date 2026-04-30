## Context

Subnets within each AZ are placed in grid rows in arbitrary order. Matching subnets across AZs (e.g., `private_az1` and `private_az2`) end up in different rows, breaking horizontal alignment.

## Goals / Non-Goals

**Goals:**
- Subnets with the same role across AZs land in the same grid row
- Deterministic, stable sorting

**Non-Goals:**
- User-configurable sort order
- Grouping subnets by role visually (e.g., adding role labels)

## Decisions

### 1. Role extraction by stripping AZ suffix from subnet name

Extract a "role" key from each subnet name by removing the AZ-specific suffix. Observed patterns across accounts:

| Name | Role | Pattern stripped |
|---|---|---|
| `public_az1` | `public` | `_az[0-9]+` |
| `private_az2` | `private` | `_az[0-9]+` |
| `local.customer.backend.1a` | `local.customer.backend` | `\.[0-9][a-z]$` |
| `yellow-db-us-west-2a` | `yellow-db` | `-{region}{az-letter}` |

Algorithm:
1. Try stripping the full AZ name from the end (e.g., remove `-us-west-2a` or `_us-east-2b`)
2. Try stripping common AZ suffix patterns: `_az[0-9]+`, `[._-][0-9][a-z]$`
3. If no pattern matches, use the full name
4. For unnamed subnets (no Name tag), use CIDR block as sort key

### 2. Sort subnets within each AZ group by role key

After grouping subnets by AZ, sort each group by role key. Since all AZs are sorted by the same key, matching roles align across columns.

### 3. Implementation location

A `_subnet_role_key(subnet)` function in `resource_vpc.py` that takes a subnet dict and returns a sort key. Applied to each AZ group before grid placement.

## Risks / Trade-offs

- [Non-matching subnet counts] → If AZ-a has 3 subnets and AZ-b has 2, some rows will have empty cells in one column. This already happens; alignment just makes it more intentional.
- [Name-based heuristic] → The role extraction is best-effort. Unusual naming conventions could produce wrong alignment. Acceptable — CIDR fallback ensures stability.
