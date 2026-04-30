# Tasks: Upgrade RUNME.sh to v2.0.0 with RUNME.d

## Tasks

- [x] Update `/RUNME.sh` boilerplate to v2.0.0, keep shared config, remove all inline tasks
- [x] Create `/RUNME.d/10-symbols.sh` with symbols tasks
- [x] Create `/RUNME.d/20-templates.sh` with templates tasks
- [x] Create `/RUNME.d/30-extension.sh` with extension tasks
- [x] Create `/RUNME.d/40-combo.sh` with all and clean tasks
- [x] Create `/RUNME.d/50-tests.sh` with test tasks and __echo_inkscape_dir helper
- [x] Replace all `$SCRIPT_DIR` references with `$RUNME_DIR`
- [x] Verify: `./RUNME.sh` shows all 15 commands
- [x] Verify: `./RUNME.sh test_all` passes all tests
