## Context

The account rect rendering is gated behind `if account_name:` in multiple places in `aws-auto-diagram.py`: layer creation, stack/row origin offset, and the final `render_account_rect` call. The account ID (AWS account number) is always present as the last directory component of `data_dir`.

## Goals / Non-Goals

**Goals:**
- Always render the account rectangle with the account ID
- Optionally prepend a friendly name if provided

**Non-Goals:**
- Changing the account rectangle's visual style or padding
- Looking up account aliases from AWS data

## Decisions

### 1. Account ID from data_dir basename

```python
account_id = Path(data_dir).name  # "222222222222"
```

This is reliable — the cloudia data directory structure is `account-data/{account-id}/`.

### 2. Label construction

```python
if account_name:
    account_label = f"{account_name} ({account_id})"
else:
    account_label = account_id
```

### 3. Remove all conditionals

Every `if account_name:` guard becomes unconditional. The Accounts layer is always created, the Stack/Row origin is always offset by account padding, and `render_account_rect` is always called.

## Risks / Trade-offs

- [Slightly larger diagrams] → Every diagram now has account padding. Acceptable — the account boundary provides valuable context.
