# Tasks: Config schema (describe-only keystone)

## 1. Schema descriptor
- [x] 1.1 Add `ica_utils/config_schema.py` with a small `Field` dataclass (`type`, optional `range`, optional `enum`, optional `unit`, required `help`)
- [x] 1.2 Add type/predicate helpers: numeric range check, `color` (`#RRGGBB`/`#RGB`/`none`), `enum`
- [x] 1.3 Declare `FIELDS` for all `document.*` keys (1), all `theme.{light,dark}.*` keys (18), and all flattened `layout.*` keys (101) — metadata only, NO default values, engine/flat key form
  - Implemented as ordered metadata *rules* (`_EXACT` + `_LEAF_RULES`) expanded against the real YAML inventory, so coverage is exhaustive by construction and DRY (avoids 120 hand-typed entries that would drift). Coverage verified: 121/121 keys, 0 missing, 0 orphaned.

## 2. Schema loader (joins metadata with YAML)
- [x] 2.1 Implement key-inventory discovery: walk `default-config.yaml`, resolve `spaced`/`dense` to flattened `layout.*`, produce the real key set (`inventory()`)
- [x] 2.2 Implement default-value sourcing: read each key's default from the YAML (spaced preset is canonical for layout keys); schema never stores defaults (`load_schema()`)
- [x] 2.3 Derive `preset_varying` per layout key by comparing spaced vs dense; expose both preset values when they differ, single value otherwise (verified: 83 varying / 18 not)
- [x] 2.4 Produce a resolved view `key -> ResolvedKey{value, field(type/range/enum/unit/help), preset_varying, spaced_value, dense_value}`

## 3. Validation
- [x] 3.1 Implement `validate_override(user_dict, extension_dir) -> list[Error]` — pure, no inkex
- [x] 3.2 Cover: unknown key, type mismatch, out-of-range, invalid enum; allow valid partial overrides

## 4. Coverage self-check
- [x] 4.1 Implement `check_coverage()` returning (missing_in_schema, extra_in_schema) against `default-config.yaml`

## 5. Tests
- [x] 5.1 Coverage test: schema keys == default-config.yaml keys (flattened); fails on any drift
- [x] 5.2 Validation tests: one per error case + a valid partial-override case
- [x] 5.3 `preset_varying` tests: a known density knob is True (exposes both values); a known style key is False (single value)
- [x] 5.4 Default-sourcing test: a sampled key's schema default equals the YAML value
  - Tests live in `extensions/aws-auto-diagram/tests/test_config_schema.py` (no-pytest, self-checking script — pytest is not in the devshell) and are wired into `RUNME.d/50-tests.sh` as `test_config_schema` (+ added to `test_all`).

## 6. Behavior-unchanged guard
- [x] 6.1 Confirm no edits to `aws-auto-diagram.py`, `config.py`, or any `resource_*.py` (git diff empty; no engine file imports `config_schema`)
- [x] 6.2 Golden-output check: rendered the same data with the schema module hidden vs present → byte-identical SVG (655321 bytes both). Rendered to /tmp only (real customer data is the only local fixture; never written to the repo).
- [x] 6.3 Run headless test (per project workflow: always run headless test after extension changes) — `extension_run` succeeded in `nix develop`.
