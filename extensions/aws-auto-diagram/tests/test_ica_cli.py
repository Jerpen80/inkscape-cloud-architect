"""Tests for the `ica` CLI config-override pipeline + schema coercion.

No pytest (not in the devshell). Run directly:

    PYTHONPATH=extensions/aws-auto-diagram \
        python3 extensions/aws-auto-diagram/tests/test_ica_cli.py

These test the pure override-building logic (parse/coerce/validate) without
invoking a render, so they need no account-data. Exits non-zero on failure.
Wired into RUNME.d/50-tests.sh as `test_ica_cli`.
"""

import sys
from pathlib import Path

EXT = str(Path(__file__).resolve().parent.parent)
sys.path.insert(0, EXT)

from ica_utils import config_schema as cs  # noqa: E402

_failures = []


def check(cond, msg):
    if cond:
        print("  PASS:", msg)
    else:
        print("  FAIL:", msg)
        _failures.append(msg)


def test_parse_set_pairs():
    print("[set] parse_set_pairs")
    out = cs.parse_set_pairs(["layout.ec2.icon_scale=0.8", "layout.mode=dense"])
    check(out == {"layout": {"ec2": {"icon_scale": "0.8"}, "mode": "dense"}},
          "dotted pairs become a nested dict of raw strings")
    try:
        cs.parse_set_pairs(["nope"])
        check(False, "missing '=' should raise")
    except ValueError:
        check(True, "pair without '=' raises ValueError")


def test_coerce_types():
    print("[coerce] coerce_override types")
    coerced, errs = cs.coerce_override(
        {"layout": {"ec2": {"icon_scale": "0.8", "font_size": "17"}}}, EXT)
    check(not errs, "valid numeric strings coerce without error")
    check(coerced["layout"]["ec2"]["icon_scale"] == 0.8, "float coerced from string")
    check(coerced["layout"]["ec2"]["font_size"] == 17, "int coerced from string")

    coerced, errs = cs.coerce_override({"layout": {"availability_zone": {"enabled": "false"}}}, EXT)
    check(not errs and coerced["layout"]["availability_zone"]["enabled"] is False,
          "bool 'false' coerced to False")

    coerced, errs = cs.coerce_override({"layout": {"mode": "dense"}}, EXT)
    check(not errs and coerced["layout"]["mode"] == "dense", "enum value passes through")


def test_coerce_errors():
    print("[coerce] coerce_override errors")
    _, errs = cs.coerce_override({"layout": {"ec2": {"nope": "1"}}}, EXT)
    check(len(errs) == 1 and "unknown" in errs[0].message, "unknown key -> error")

    _, errs = cs.coerce_override({"layout": {"ec2": {"font_size": "big"}}}, EXT)
    check(len(errs) == 1 and "integer" in errs[0].message, "non-int string -> type error")

    _, errs = cs.coerce_override({"layout": {"ec2": {"icon_scale": "99"}}}, EXT)
    check(len(errs) == 1 and "range" in errs[0].message, "out-of-range -> range error")

    _, errs = cs.coerce_override({"layout": {"mode": "sparse"}}, EXT)
    check(len(errs) == 1 and "one of" in errs[0].message, "bad enum -> enum error")


def test_full_set_pipeline():
    print("[pipeline] parse -> coerce a --set value")
    nested = cs.parse_set_pairs(["layout.ec2.icon_scale=0.8"])
    coerced, errs = cs.coerce_override(nested, EXT)
    check(not errs and coerced["layout"]["ec2"]["icon_scale"] == 0.8,
          "--set string flows through parse+coerce to typed float")


def main():
    test_parse_set_pairs()
    test_coerce_types()
    test_coerce_errors()
    test_full_set_pipeline()
    print()
    if _failures:
        print("RESULT: {} failure(s)".format(len(_failures)))
        return 1
    print("RESULT: all ica_cli tests passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
