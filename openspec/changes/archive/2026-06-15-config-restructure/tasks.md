## 1. Golden guard (do first)

- [x] 1.1 Captured exact golden SVGs under `tests/fixtures/golden/` for all 4 cases: single/multi region × spaced/dense (666383 / 666799 / 668883 / 669139 bytes)
- [x] 1.2 Added `tests/test_config_golden.py` (byte-exact render vs committed goldens) and wired `test_config_golden` into `RUNME.d/50-tests.sh` + `test_all`
- [x] 1.3 Confirmed the golden test passes on the PRE-restructure code (baseline established)

## 2. Restructure default-config.yaml + resolver

- [x] 2.1 Restructured `default-config.yaml`: `spaced` is the canonical full set; `dense` trimmed to only the 83 differing keys (the 18 style keys now live only in spaced → defined once). Equivalence proven mathematically before editing.
- [x] 2.2 Updated `resolve_layout_mode`: for `dense`, deep-merge the dense diff onto the canonical `spaced` base; for `spaced`, use canonical directly. Output flattened `layout.*` identical to before.
- [x] 2.3 Golden byte-identical for both modes after the YAML + resolver change (D1 invariant holds)
- [x] 2.4 `test_config_schema` still green (key inventory + 83/18 preset_varying split unchanged — schema reads via resolve_layout_mode, whose output is unchanged)

## 3. Remove inline shadow defaults

- [x] 3.1 Classified `.get(key, fallback)` reads: LEAF config defaults (numeric / DEFAULT_* / color-string) vs STRUCTURAL guards (`{}`/`[]`/`None`) vs RESOURCE-DATA reads (per-resource dicts)
- [x] 3.2 Removed **161** leaf config shadow-defaults across all 17 resource modules + legend (`.get(k, default)` → `[k]`), keeping structural guards and the 66 resource-data reads. Done per-module (4 done directly + 3 parallel agent batches), golden-tested after each batch.
- [x] 3.3 Golden stayed byte-identical throughout; no removal broke output (= proof each removed key was genuinely resolver-guaranteed). Remaining 66 `.get(k, default)` are all resource-data fields (name/subnet_id/instance_id/engine/…), correctly kept.

## 4. Verify

- [x] 4.1 `./RUNME.sh test_all` green (config_schema, ica_cli, render_fixture, config_golden)
- [x] 4.2 Fixture renders byte-identical to goldens for spaced AND dense, single AND multi-region
- [x] 4.3 Inkscape extension path renders unchanged (extension_run = 650380 bytes = baseline)
- [x] 4.4 No real account-data / rendered SVGs committed; goldens contain only synthetic-fixture (fake) identifiers; engine.py / aws-auto-diagram.py / .inx untouched
