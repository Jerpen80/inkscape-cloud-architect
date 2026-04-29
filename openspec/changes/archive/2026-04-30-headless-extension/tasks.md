# Tasks: Fix flake Python environment and add headless extension runner

## Tasks

- [x] Fix `flake.nix`: add lxml, tinycss2 to withPackages; extract pythonEnv; prepend to PATH in shellHook
- [x] Verify `nix develop --command python3 -c "import inkex"` works
- [x] Create `RUNME.d/35-extension-run.sh` with `extension_run` task (takes data_dir and region args, runs extension headless)
- [x] Test headless run against CustomerA account-data
