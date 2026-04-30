# Design: Fix flake Python environment and add headless extension runner

## Flake fix

### Problem

```
Current PATH in devshell:
  python3 → 3.11 (cloudia-reader-aws)  ← wins, NO inkex
  python3 → 3.13 (withPackages+inkex)  ← shadowed, has inkex

inkex also imports lxml, tinycss2, numpy — only numpy is available (via cloudia).
```

### Solution

1. Add missing deps to `withPackages`: lxml, tinycss2 (numpy already available)
2. Extract the withPackages python into a `let` binding
3. Prepend it to PATH in shellHook so it wins over cloudia's Python

```nix
let
  pythonEnv = pkgs.python3.withPackages (ps: with ps; [
    inkex
    lxml
    tinycss2
  ]);
in {
  default = pkgs.mkShell {
    buildInputs = [
      pythonEnv
      cloudia-reader-aws.packages.${system}.default
    ];
    shellHook = ''
      export PATH="${pythonEnv}/bin:$PATH"
    '';
  };
}
```

### Future improvement

When cloudia-reader-aws exposes itself as a Python package (not just a standalone app), switch to:

```nix
(pkgs.python3.withPackages (ps: [
  ps.inkex
  cloudia-reader-aws.pythonPackages.${system}.cloudia-reader-aws
]))
```

One Python runtime, no PATH conflicts.

## Headless extension runner

### RUNME.d/35-extension-run.sh

A new task `extension_run` that:
1. Takes data_dir and region as arguments
2. Creates a minimal blank SVG as input
3. Runs `python3 aws-auto-diagram.py --data_dir=... --region=... input.svg`
4. Captures output SVG

### Usage

```bash
./RUNME.sh extension_run /path/to/account-data/222222222222 eu-west-1
```

Output goes to `output.svg` in the current directory (or a specified path).

### Requires nix devshell

The runner depends on inkex being available, so it must run inside `nix develop` or equivalent. The RUNME.sh task should check for inkex availability and print a clear error if missing.
