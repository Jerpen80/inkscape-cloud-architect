"""Byte-exact golden test guarding the config-restructure refactor.

Renders the synthetic fixture for every (region, mode) combination and asserts the
output is byte-identical to the committed golden SVGs (captured before the
restructure). This is stricter than the structural `test_render_fixture` and is the
safety net for the config-restructure change: the restructure MUST NOT change
rendered output.

No pytest. Run directly:

    PYTHONPATH=extensions/aws-auto-diagram \
        python3 extensions/aws-auto-diagram/tests/test_config_golden.py

Goldens are rendered from the synthetic fixture only (no real account-data). If an
intentional layout change is made later, regenerate them (see the header of
tests/fixtures/golden/).
"""

import sys
from pathlib import Path

EXT = str(Path(__file__).resolve().parent.parent)
sys.path.insert(0, EXT)

from ica_utils import engine  # noqa: E402

FIXTURE = str(Path(EXT) / "tests" / "fixtures" / "synthetic-account")
GOLDEN = Path(EXT) / "tests" / "fixtures" / "golden"

_CASES = [
    ("eu-west-1", "spaced", "single-spaced"),
    ("eu-west-1", "dense", "single-dense"),
    ("all", "spaced", "multi-spaced"),
    ("all", "dense", "multi-dense"),
]

_failures = []


def check(cond, msg):
    if cond:
        print("  PASS:", msg)
    else:
        print("  FAIL:", msg)
        _failures.append(msg)


def main():
    print("[golden] byte-exact render vs committed goldens")
    for region, mode, name in _CASES:
        svg = engine.render(FIXTURE, region, account_name="Demo",
                            layout_mode=mode, extension_dir=EXT)
        gold_path = GOLDEN / (name + ".svg")
        if not gold_path.is_file():
            check(False, "golden missing: {}".format(name))
            continue
        gold = gold_path.read_text()
        check(svg == gold, "byte-identical: {} ({} bytes)".format(name, len(svg)))
    print()
    if _failures:
        print("RESULT: {} golden failure(s)".format(len(_failures)))
        return 1
    print("RESULT: all config-golden tests passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
