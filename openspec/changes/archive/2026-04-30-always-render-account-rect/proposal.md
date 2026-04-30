## Why

The account rectangle is currently only rendered when the user provides an account name. This means diagrams generated without a name lack the account boundary, losing visual context. The account number is always available from the data directory path and should always be shown. The user-provided name becomes an optional friendly label.

Bean: [inkscape-cloud-architect-3zhk](.beans/inkscape-cloud-architect-3zhk--always-print-account-number-in-account-label.md)

## What Changes

- Always render the account rectangle, regardless of whether `account_name` is provided
- Extract the account ID from `basename(data_dir)` (e.g., `account-data/222222222222` → `222222222222`)
- Build the account label: `"Friendly Name (222222222222)"` when name is given, else just `"222222222222"`
- Remove all `if account_name:` conditional guards for layer creation, stack offset, and rect rendering

## Capabilities

### Modified Capabilities
- `account-rendering`: Account rect always renders; label includes account ID derived from data_dir

## Impact

- **Code**: `aws-auto-diagram.py` — extract account_id, build label, remove conditionals
- **Behavior**: Diagrams always have an account boundary, even without `--account_name`
