---
# inkscape-cloud-architect-ejab
title: '50 ica pull: cloudia account-data orchestration'
status: todo
type: task
created_at: 2026-06-10T13:27:06Z
updated_at: 2026-06-10T13:27:06Z
parent: inkscape-cloud-architect-muex
blocked_by:
    - inkscape-cloud-architect-fy5b
---

Add `ica pull` — orchestrate cloudia (cloudia-reader-aws) to dump AWS account-data, closing the end-to-end pipeline so co-workers go from AWS creds to diagram in one tool.

Scope:
- `ica pull --profile <p> --region <r>` runs cloudia, writes account-data/<account_id>/ in the layout cloudia_parser expects.
- Depends on cloudia-reader-aws (the flake input from bean 0g22/rn3b) + AWS credentials.
- This is the pipeline stage where REAL CUSTOMER DATA ENTERS — the origin of the 2026-06-09 leak. Must land AFTER safe-io defaults (bean 40) conceptually, or at minimum write to safe, gitignored locations by default.

Heaviest stage (AWS surface, creds, cloudia coupling). Part of epic muex. Depends on: 30 nix-package-ica. Blocks: 60 ica-tui. Ships in v1.4.0.
