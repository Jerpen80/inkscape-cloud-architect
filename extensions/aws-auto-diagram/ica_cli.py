"""`ica` — the Inkscape Cloud Architect command-line front-end.

A thin Typer app over the existing engine + config schema:

* ``ica render`` — render a diagram, with layered, validated, type-coerced
  config overrides (``--config`` file and repeatable ``--set k=v``).
* ``ica initconf`` — scaffold a curated starter config.
* ``ica setup`` — obtain the AWS icon ZIP, build symbols, and install symbols +
  templates into the Inkscape user directory.

The heavy lifting lives in ``ica_utils`` (imported in place; the Inkscape
extension is untouched).
"""

import os
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

import typer
import yaml

from ica_utils import config as ica_config
from ica_utils import config_schema as schema
from ica_utils import engine

EXTENSION_DIR = str(Path(__file__).resolve().parent)

# Default AWS icon package URL (dated+hashed; AWS rotates it — overridable via
# config `symbols.asset_zip_url`, or bypass with `ica setup --asset-zip`).
_DEFAULT_ASSET_ZIP_URL = (
    "https://d1.awsstatic.com/onedam/marketing-channels/website/aws/en_US/"
    "architecture/approved/architecture-icons/"
    "Icon-package_04302026.4705b90f5aa45b019271a2699e9ce9b97b941ee1.zip"
)
_AWS_ICONS_PAGE = "https://aws.amazon.com/architecture/icons/"

app = typer.Typer(
    help="Inkscape Cloud Architect — render AWS architecture diagrams from account-data.",
    add_completion=True,
    no_args_is_help=True,
)


def _version_callback(value: bool):
    if value:
        typer.echo("ica 0.1.0")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        False, "--version", callback=_version_callback, is_eager=True,
        help="Show version and exit.",
    ),
    verbose: int = typer.Option(
        0, "-v", "--verbose", count=True, help="Increase verbosity (repeatable)."
    ),
):
    """ica — AWS diagrams from cloudia account-data."""
    # verbosity is accepted for forward-compat; engine logging hook is future work
    return None


def _build_override(config_file, set_pairs):
    """Build the validated, coerced, flat-form override dict from --config + --set.

    Returns the override dict (applied by the engine AFTER preset resolution, so
    it wins over the preset). On any error, prints per-key messages and raises
    typer.Exit(1). Each layer is fully validated by coerce_override (unknown key
    / type / range / enum) before merging; merge order is file ◄ --set.
    """
    override = {}

    # Layer: explicit override file
    if config_file:
        p = Path(config_file)
        if not p.is_file():
            typer.echo(f"error: config file not found: {config_file}", err=True)
            raise typer.Exit(1)
        with open(p) as f:
            file_override = yaml.safe_load(f) or {}
        file_coerced, file_errors = schema.coerce_override(file_override, EXTENSION_DIR)
        _fail_on(file_errors, "config file")
        override = ica_config._deep_merge(override, file_coerced)

    # Layer: inline --set pairs (win over the file)
    if set_pairs:
        try:
            set_override = schema.parse_set_pairs(list(set_pairs))
        except ValueError as e:
            typer.echo(f"error: {e}", err=True)
            raise typer.Exit(1)
        set_coerced, set_errors = schema.coerce_override(set_override, EXTENSION_DIR)
        _fail_on(set_errors, "--set")
        override = ica_config._deep_merge(override, set_coerced)

    return override


def _fail_on(errors, where):
    if errors:
        typer.echo(f"error: invalid {where}:", err=True)
        for e in errors:
            typer.echo(f"  {e}", err=True)
        raise typer.Exit(1)


@app.command()
def render(
    data_dir: str = typer.Argument(..., help="Path to the account-data directory."),
    region: str = typer.Argument(..., help="AWS region, or 'all' for multi-region."),
    output: str = typer.Option(
        ..., "-o", "--output", help="Output SVG path. Use '-' for stdout."
    ),
    theme: str = typer.Option("light", "--theme", help="Theme (light/dark)."),
    layout_mode: str = typer.Option("spaced", "--layout-mode", help="Layout density (spaced/dense)."),
    account_name: str = typer.Option("", "--account-name", help="Account label."),
    config_file: str = typer.Option(None, "--config", help="Override config YAML file."),
    set_pairs: list[str] = typer.Option(
        [], "--set", help="Inline override key=value (repeatable), e.g. layout.ec2.icon_scale=0.8.",
    ),
):
    """Render a diagram to SVG."""
    override = _build_override(config_file, set_pairs)

    svg = engine.render(
        data_dir=data_dir,
        region=region,
        account_name=account_name,
        theme=theme,
        layout_mode=layout_mode,
        extension_dir=EXTENSION_DIR,
        override=override or None,
    )

    if output == "-":
        sys.stdout.write(svg)
    else:
        with open(output, "w") as f:
            f.write(svg)
        typer.echo(f"wrote {output}", err=True)


# Curated starter keys for `ica initconf` (common knobs, not the full ~120).
# Note: theme (light/dark) is a render option (--theme), not a config key, so it
# is not listed here; the comment header points users at the full key set.
_STARTER_KEYS = [
    "layout.mode",
    "document.margin",
    "layout.ec2.icon_scale",
    "layout.subnet.min_width",
    "layout.vpc.gap",
]


@app.command()
def initconf(
    output: str = typer.Option("-", "-o", "--output", help="Output YAML path. Use '-' for stdout."),
):
    """Scaffold a curated starter config with sane defaults."""
    sch = schema.load_schema(EXTENSION_DIR)

    lines = [
        "# ica starter config — common options with default values.",
        "# These are a curated subset; the full set of configurable keys can be",
        "# inspected with the config schema (see project docs). Edit and pass with:",
        "#   ica render <data_dir> <region> --config this-file.yaml -o out.svg",
        "",
    ]

    # Build a nested dict from the curated keys, then dump as YAML with comments.
    starter = {}
    for key in _STARTER_KEYS:
        rk = sch.get(key)
        if rk is None:
            continue
        schema._set_nested(starter, key, rk.value)

    body = yaml.safe_dump(starter, default_flow_style=False, sort_keys=False)
    content = "\n".join(lines) + body

    if output == "-":
        sys.stdout.write(content)
    else:
        with open(output, "w") as f:
            f.write(content)
        typer.echo(f"wrote {output}", err=True)


# --------------------------------------------------------------------------- #
# ica setup — install symbols + templates into the Inkscape user dir
# --------------------------------------------------------------------------- #


def _inkscape_dir():
    """Resolve the Inkscape user config dir (single source: engine.inkscape_dir)."""
    return Path(engine.inkscape_dir())


def _symbol_build_dir():
    """Locate the symbol build toolchain (build.sh + files_to_svg.py).

    The nix package sets $ICA_SYMBOL_BUILD_DIR; in a dev checkout we fall back to
    the repo's symbols/aws-inkscape-symbols/ relative to this file.
    """
    env = os.environ.get("ICA_SYMBOL_BUILD_DIR")
    if env:
        return Path(env)
    # repo dev fallback: <repo>/symbols/aws-inkscape-symbols
    repo = Path(EXTENSION_DIR).resolve().parent.parent
    return repo / "symbols" / "aws-inkscape-symbols"


def _templates_dir():
    """Locate the templates to install (nix: $ICA_TEMPLATES_DIR; dev: repo)."""
    env = os.environ.get("ICA_TEMPLATES_DIR")
    if env:
        return Path(env)
    repo = Path(EXTENSION_DIR).resolve().parent.parent
    return repo / "templates"


def _resolve_asset_zip(asset_zip, repo_fallback):
    """Return a local path to the AWS icon ZIP, or raise typer.Exit(1).

    Order: explicit --asset-zip → download (config url or default) → repo fallback.
    Returns (path, is_temp) where is_temp means the caller should clean it up.
    """
    if asset_zip:
        p = Path(asset_zip)
        if not p.is_file():
            typer.echo(f"error: --asset-zip not found: {asset_zip}", err=True)
            raise typer.Exit(1)
        return p, False

    # download
    config = ica_config.load_config(EXTENSION_DIR)
    url = config.get("symbols", {}).get("asset_zip_url") or _DEFAULT_ASSET_ZIP_URL
    try:
        typer.echo(f"downloading AWS icon package from {url}", err=True)
        fd, tmp = tempfile.mkstemp(suffix=".zip")
        os.close(fd)
        urllib.request.urlretrieve(url, tmp)
        return Path(tmp), True
    except Exception as e:  # noqa: BLE001
        typer.echo(f"warning: download failed ({e})", err=True)

    # repo fallback
    if repo_fallback and repo_fallback.is_file():
        typer.echo(f"using repository fallback ZIP: {repo_fallback}", err=True)
        return repo_fallback, False

    typer.echo(
        "error: could not obtain the AWS icon package.\n"
        f"  Download it from {_AWS_ICONS_PAGE} and pass --asset-zip <path>.",
        err=True,
    )
    raise typer.Exit(1)


@app.command()
def setup(
    asset_zip: str = typer.Option(
        None, "--asset-zip", help="Local AWS icon ZIP (else download / repo fallback)."
    ),
):
    """Build AWS symbols and install symbols + templates into the Inkscape dir."""
    build_dir = _symbol_build_dir()
    build_sh = build_dir / "build.sh"
    if not build_sh.is_file():
        typer.echo(f"error: symbol build toolchain not found at {build_dir}", err=True)
        raise typer.Exit(1)

    # find a committed repo fallback zip (Asset-Package_*.zip) in the build dir
    repo_zips = sorted(build_dir.glob("Asset-Package_*.zip"))
    repo_fallback = repo_zips[0] if repo_zips else None

    zip_path, is_temp = _resolve_asset_zip(asset_zip, repo_fallback)

    # build.sh writes target/ and build/ in its own dir; when shipped in the
    # read-only nix store that fails, so build in a writable temp copy.
    work = Path(tempfile.mkdtemp(prefix="ica-symbols-"))
    try:
        for item in build_dir.iterdir():
            dst = work / item.name
            if item.is_dir():
                shutil.copytree(item, dst)
            else:
                shutil.copy2(item, dst)

        typer.echo("building symbols (this may take a moment)…", err=True)
        result = subprocess.run(
            ["bash", "build.sh", str(Path(zip_path).resolve())],
            cwd=str(work),
        )
        if result.returncode != 0:
            typer.echo("error: symbol build failed", err=True)
            raise typer.Exit(1)

        target = work / "target"
        if not target.is_dir():
            typer.echo("error: build produced no target/ directory", err=True)
            raise typer.Exit(1)
        _install_built(target)
    finally:
        if is_temp:
            try:
                os.unlink(zip_path)
            except OSError:
                pass
        shutil.rmtree(work, ignore_errors=True)


def _install_built(target):
    """Install built symbols + shipped templates into the Inkscape user dir."""

    ink = _inkscape_dir()
    sym_dest = ink / "symbols" / "aws-architect"
    tpl_dest = ink / "templates" / "aws-architect"
    sym_dest.mkdir(parents=True, exist_ok=True)
    tpl_dest.mkdir(parents=True, exist_ok=True)

    # install symbols
    for svg in target.glob("*.svg"):
        shutil.copy2(svg, sym_dest / svg.name)
    # install templates
    tdir = _templates_dir()
    if tdir.is_dir():
        for t in tdir.iterdir():
            if t.is_file():
                shutil.copy2(t, tpl_dest / t.name)

    typer.echo(f"installed symbols → {sym_dest}", err=True)
    typer.echo(f"installed templates → {tpl_dest}", err=True)
    typer.echo("setup complete — `ica render` is ready.", err=True)


# --------------------------------------------------------------------------- #
# ica doctor — check the rendering environment is healthy
# --------------------------------------------------------------------------- #


@app.command()
def doctor():
    """Check the environment is ready to render, and how to fix it if not."""
    config = ica_config.load_config(EXTENSION_DIR)
    ink = _inkscape_dir()
    ok = True  # tracks required checks

    # 1. inkex importable (required)
    try:
        import inkex  # noqa: F401
        typer.echo("ok    inkex importable")
    except Exception:  # noqa: BLE001
        ok = False
        typer.echo("FAIL  inkex not importable")
        typer.echo("        → run inside the `nix develop` shell, or install ica via the flake")

    # 2. symbols present (required) — same location render uses
    sym_dir = Path(engine.resolve_symbol_dir(config, None))
    missing = [f for f in engine.SYMBOL_FILES if not (sym_dir / f).is_file()]
    if not missing:
        typer.echo(f"ok    symbols present ({len(engine.SYMBOL_FILES)} files in {sym_dir})")
    else:
        ok = False
        typer.echo(f"FAIL  symbols missing in {sym_dir}: {', '.join(missing)}")
        typer.echo("        → run `ica setup` (optionally `ica setup --asset-zip <path>`)")

    # 3. templates present (warning — GUI only)
    tpl_dir = ink / "templates" / "aws-architect"
    if tpl_dir.is_dir() and any(tpl_dir.iterdir()):
        typer.echo(f"ok    templates present ({tpl_dir})")
    else:
        typer.echo(f"warn  templates not installed ({tpl_dir})")
        typer.echo("        → run `ica setup` (needed only for the Inkscape GUI)")

    # 4. extension present (info — GUI dialog only)
    ext_dir = ink / "extensions" / "aws-auto-diagram"
    if ext_dir.is_dir():
        typer.echo(f"ok    Inkscape extension installed ({ext_dir})")
    else:
        typer.echo(f"info  Inkscape extension not installed ({ext_dir})")
        typer.echo("        → install it for the Inkscape dialog (not needed for `ica render`)")

    if ok:
        typer.echo("\nenvironment OK — `ica render` is ready.")
    else:
        typer.echo("\nenvironment NOT ready — fix the FAIL items above.", err=True)
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
