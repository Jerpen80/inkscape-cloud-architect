"""Tests for `ica doctor` outcomes.

No pytest. Run directly:

    PYTHONPATH=extensions/aws-auto-diagram \
        python3 extensions/aws-auto-diagram/tests/test_ica_doctor.py

Drives the doctor checks via the Typer CliRunner with a temp $INKSCAPE_DIR and a
`symbols.dir` config override, so it needs no real Inkscape install. Asserts:
healthy → exit 0; missing symbols → exit non-zero with the setup remedy;
templates-only-missing → exit 0 (warning).
"""

import os
import sys
import tempfile
from pathlib import Path

EXT = str(Path(__file__).resolve().parent.parent)
sys.path.insert(0, EXT)

from typer.testing import CliRunner  # noqa: E402

import ica_cli  # noqa: E402
from ica_utils import engine  # noqa: E402

_failures = []
_runner = CliRunner()


def check(cond, msg):
    if cond:
        print("  PASS:", msg)
    else:
        print("  FAIL:", msg)
        _failures.append(msg)


def _populate_symbols(sym_dir):
    sym_dir.mkdir(parents=True, exist_ok=True)
    for f in engine.SYMBOL_FILES:
        (sym_dir / f).write_text("<svg/>")


def _run_doctor(symbols_dir):
    """Run `ica doctor` with a symbols.dir override and a temp INKSCAPE_DIR.

    Returns (exit_code, output). Uses monkeypatched load_config to inject the
    override without writing a user config file.
    """
    orig_load = ica_cli.ica_config.load_config

    def fake_load(ext_dir):
        cfg = orig_load(ext_dir)
        cfg.setdefault("symbols", {})["dir"] = str(symbols_dir)
        return cfg

    ica_cli.ica_config.load_config = fake_load
    try:
        result = _runner.invoke(ica_cli.app, ["doctor"])
    finally:
        ica_cli.ica_config.load_config = orig_load
    return result.exit_code, result.output


def test_healthy():
    print("[doctor] healthy environment")
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        _populate_symbols(tmp / "symbols")
        os.environ["INKSCAPE_DIR"] = str(tmp)
        try:
            code, out = _run_doctor(tmp / "symbols")
        finally:
            os.environ.pop("INKSCAPE_DIR", None)
    check(code == 0, "healthy (symbols present) → exit 0")
    check("symbols present" in out, "reports symbols present")


def test_missing_symbols():
    print("[doctor] missing symbols")
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        os.environ["INKSCAPE_DIR"] = str(tmp)
        try:
            code, out = _run_doctor(tmp / "symbols")  # not populated
        finally:
            os.environ.pop("INKSCAPE_DIR", None)
    check(code != 0, "missing symbols → exit non-zero")
    check("symbols missing" in out, "reports symbols missing")
    check("ica setup" in out, "remedy points at `ica setup`")


def test_templates_only_missing():
    print("[doctor] symbols present, templates absent → warning, exit 0")
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        _populate_symbols(tmp / "symbols")
        # no templates/ dir created
        os.environ["INKSCAPE_DIR"] = str(tmp)
        try:
            code, out = _run_doctor(tmp / "symbols")
        finally:
            os.environ.pop("INKSCAPE_DIR", None)
    check(code == 0, "templates-only missing → still exit 0 (GUI-only warning)")
    check("templates not installed" in out, "templates reported as a warning")


def main():
    test_healthy()
    test_missing_symbols()
    test_templates_only_missing()
    print()
    if _failures:
        print("RESULT: {} doctor failure(s)".format(len(_failures)))
        return 1
    print("RESULT: all ica_doctor tests passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
