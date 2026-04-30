# Tasks: Unified RUNME.sh Task Runner

## Tasks

- [x] Create `/RUNME.sh` at project root with RUNME.sh framework boilerplate and cross-platform INKSCAPE_DIR detection
- [x] Add symbols tasks: `symbols_build`, `symbols_install`, `symbols_clean`, `symbols_clean_cache`
- [x] Add templates tasks: `templates_install`, `templates_clean`
- [x] Add extension tasks: `extension_install`, `extension_clean`, `extension_dev`
- [x] Add combo tasks: `all` (enforced ordering), `clean` (all three deliverables)
- [x] Delete `/Makefile`
- [x] Delete `/extensions/aws-auto-diagram/RUNME.sh`
- [x] Make `INKSCAPE_DIR` overridable via environment variable for testability
- [x] Add test tasks: `test_usage`, `test_inkscape_dir`, `test_install`, `test_all` (runs all)
- [x] Update `/README.md` — replace `make` references with `./RUNME.sh` commands, mention three deliverables
