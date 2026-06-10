---
# inkscape-cloud-architect-3k05
title: 40 safe IO defaults + synthetic fixtures
status: todo
type: task
created_at: 2026-06-10T13:27:06Z
updated_at: 2026-06-10T13:27:06Z
parent: inkscape-cloud-architect-muex
blocked_by:
    - inkscape-cloud-architect-fy5b
---

Make ica leak-safe by default — directly motivated by the 2026-06-09 incident where customer account-data and rendered SVGs were committed to the public repo.

Scope:
- Safe output discipline: don't default output to repo CWD where it gets committed; sensible default output dir, clear path echoing, refuse to write into the git work tree without a flag.
- Synthetic fixtures: ship a sanitized example account-data set so `ica render` works out-of-the-box with NO real customer data (also enables golden-output tests).
- Guardrails: warn/refuse when reading account-data that looks like real customer dumps into a tracked path; reinforce the .gitignore guard added during the incident.

Part of epic muex. Depends on: 30 nix-package-ica. Blocks: 60 ica-tui. Ships in v1.3.0. See incident memory project_customer_data_leak_2026-06-09.
