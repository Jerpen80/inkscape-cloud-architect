"""Tests for ica_utils.config_schema.

No pytest dependency (not available in the devshell). Run directly:

    PYTHONPATH=extensions/aws-auto-diagram \
        python3 extensions/aws-auto-diagram/tests/test_config_schema.py

Exits non-zero on any failure. Wired into RUNME.d/50-tests.sh as
`test_config_schema`.
"""

import copy
import sys
from pathlib import Path

import yaml

# extension dir is the parent of tests/
EXT = str(Path(__file__).resolve().parent.parent)
sys.path.insert(0, EXT)

from ica_utils import config_schema as cs  # noqa: E402
from ica_utils.config import resolve_layout_mode  # noqa: E402


_failures = []


def check(cond, msg):
    if cond:
        print("  PASS:", msg)
    else:
        print("  FAIL:", msg)
        _failures.append(msg)


# --- 5.1 coverage: schema keys == default-config.yaml keys (flattened) ------- #
def test_coverage():
    print("[5.1] coverage")
    missing, extra = cs.check_coverage(EXT)
    check(missing == [], "no real key is missing a Field (missing={})".format(missing))
    check(extra == [], "no Field rule is orphaned (extra={})".format(extra))
    # every resolved key actually resolves a Field
    schema = cs.load_schema(EXT)
    no_field = [p for p, rk in schema.items() if rk.field is None]
    check(no_field == [], "every resolved key has a Field (without={})".format(no_field))


# --- 5.2 validation: one per error case + a valid partial -------------------- #
def test_validation():
    print("[5.2] validation")
    e = cs.validate_override({"layout": {"ec2": {"nope": 1}}}, EXT)
    check(len(e) == 1 and "unknown" in e[0].message, "unknown key -> unknown error")

    e = cs.validate_override({"layout": {"ec2": {"icon_scale": 99}}}, EXT)
    check(len(e) == 1 and "range" in e[0].message, "out-of-range -> range error")

    e = cs.validate_override({"layout": {"ec2": {"font_size": "big"}}}, EXT)
    check(len(e) == 1 and "integer" in e[0].message, "wrong type -> type error")

    e = cs.validate_override({"layout": {"mode": "sparse"}}, EXT)
    check(len(e) == 1 and "one of" in e[0].message, "bad enum -> enum error")

    e = cs.validate_override({"theme": {"light": {"border_vpc": "purple"}}}, EXT)
    check(len(e) == 1 and "color" in e[0].message, "bad color -> color error")

    e = cs.validate_override(
        {"layout": {"ec2": {"icon_scale": 0.8}}, "document": {"margin": 40}}, EXT
    )
    check(e == [], "valid partial override -> no errors")


# --- 5.3 preset_varying: density knob True, style key False ------------------ #
def test_preset_varying():
    print("[5.3] preset_varying")
    schema = cs.load_schema(EXT)

    knob = schema["layout.ec2.icon_scale"]
    check(knob.preset_varying is True, "density knob ec2.icon_scale is preset_varying")
    check(
        knob.spaced_value == 1.0 and knob.dense_value == 0.5,
        "ec2.icon_scale exposes both preset values (spaced=1.0, dense=0.5)",
    )

    style = schema["layout.eks.span_line_color"]
    check(style.preset_varying is False, "style key eks.span_line_color is NOT preset_varying")
    check(
        style.spaced_value is None and style.dense_value is None,
        "non-varying key exposes a single value (no spaced/dense split)",
    )

    layout = [k for k in schema if k.startswith("layout.") and k != "layout.mode"]
    varying = [k for k in layout if schema[k].preset_varying]
    check(len(varying) == 83, "exactly 83 layout keys vary by preset (got {})".format(len(varying)))


# --- 5.4 default sourcing: schema default == YAML value ---------------------- #
def test_default_sourcing():
    print("[5.4] default sourcing")
    schema = cs.load_schema(EXT)
    raw = yaml.safe_load(open(Path(EXT) / "default-config.yaml"))

    check(
        schema["document.margin"].value == raw["document"]["margin"],
        "document.margin default sourced from YAML",
    )
    check(
        schema["theme.light.border_vpc"].value == raw["theme"]["light"]["border_vpc"],
        "theme.light.border_vpc default sourced from YAML",
    )
    c = copy.deepcopy(raw)
    resolve_layout_mode(c, "spaced")
    check(
        schema["layout.ec2.icon_scale"].value == c["layout"]["ec2"]["icon_scale"],
        "layout.ec2.icon_scale default sourced from YAML spaced preset",
    )


def main():
    test_coverage()
    test_validation()
    test_preset_varying()
    test_default_sourcing()
    print()
    if _failures:
        print("RESULT: {} failure(s)".format(len(_failures)))
        return 1
    print("RESULT: all config_schema tests passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
