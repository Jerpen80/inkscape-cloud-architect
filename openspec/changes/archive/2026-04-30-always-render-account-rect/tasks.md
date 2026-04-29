## 1. Implementation

- [x] 1.1 Extract account_id from `Path(data_dir).name` in `effect()`
- [x] 1.2 Build account_label: `f"{account_name} ({account_id})"` if name given, else just `account_id`
- [x] 1.3 Remove `if account_name:` guard from `_create_layers()` — always create Accounts layer
- [x] 1.4 Remove `if account_name:` guards from stack/row origin offset — always apply account padding
- [x] 1.5 Remove `if account_name:` guards from `render_account_rect` calls — always render, pass account_label

## 2. Verification

- [x] 2.1 Run headless test without `--account_name` — confirm account rect renders with just the account ID
- [x] 2.2 Run headless test with `--account_name` — confirm label includes both name and ID
