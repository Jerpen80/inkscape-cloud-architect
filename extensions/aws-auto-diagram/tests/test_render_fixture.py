"""Structural regression test: render the synthetic fixture and assert the
output's shape (layers + element signatures), NOT exact bytes.

No pytest (not in the devshell). Run directly:

    PYTHONPATH=extensions/aws-auto-diagram \
        python3 extensions/aws-auto-diagram/tests/test_render_fixture.py

Uses only the committed synthetic fixture (no real account-data). Assertions are
structural so they survive cosmetic layout tweaks; they fail loudly if a renderer
stops emitting its element. The per-renderer assertions are also the proof that
the fixture exercises every renderer. Wired into RUNME.d/50-tests.sh.
"""

import sys
from pathlib import Path

EXT = str(Path(__file__).resolve().parent.parent)
sys.path.insert(0, EXT)

from ica_utils import engine  # noqa: E402

FIXTURE = str(Path(EXT) / "tests" / "fixtures" / "synthetic-account")

_failures = []


def check(cond, msg):
    if cond:
        print("  PASS:", msg)
    else:
        print("  FAIL:", msg)
        _failures.append(msg)


# Expected layers (the renderer pipeline's z-order labels)
_EXPECTED_LAYERS = [
    "Edge", "Accounts", "VPCs", "Availability Zones", "Subnets", "EC2",
    "Load Balancers", "EKS", "Lambda", "Database", "Auto Scaling Groups",
    "NAT Gateways", "Route 53 Private", "S3", "DynamoDB", "Legend",
]

# Per-renderer element signatures: a substring that only appears if that
# renderer fired against the fixture's resource.
_EXPECTED_MARKERS = {
    "vpc": "demo-vpc (10.0.0.0/16)",
    "subnet (public)": "demo-public-1a",
    "subnet (private)": "demo-private-1a",
    "ec2": "demo-app-server",
    "load balancer": "demo-alb",
    "rds": "demo-postgres",
    "elasticache": "demo-redis",
    "eks": "demo-cluster",
    "lambda (vpc)": "demo-vpc-worker",
    "asg": "demo-asg",
    "nat gateway": "nat-00000000000000001",
    "dynamodb": "demo-sessions",
    "account label": "Demo (synthetic-account)",
    "cloudfront (edge)": "cloudfront",
    "route53 (edge)": "example.test",
}


def _render(region):
    return engine.render(FIXTURE, region, account_name="Demo", extension_dir=EXT)


def test_single_region_structure():
    print("[single] eu-west-1 render structure")
    svg = _render("eu-west-1")
    check(len(svg) > 10000, "render produced a non-trivial SVG ({} bytes)".format(len(svg)))
    for layer in _EXPECTED_LAYERS:
        check(':label="{}"'.format(layer) in svg, "layer present: {}".format(layer))
    for name, marker in _EXPECTED_MARKERS.items():
        check(marker in svg, "renderer fired: {} ({!r})".format(name, marker))


def test_multi_region():
    print("[multi] region=all render")
    svg = _render("all")
    check(len(svg) > 10000, "multi-region render produced a non-trivial SVG")
    check(':label="Regions"' in svg, "Regions layer present (multi-region)")


def test_excluded_stopped_instance():
    print("[exclude] stopped EC2 is not rendered")
    svg = _render("eu-west-1")
    check("demo-stopped" not in svg, "stopped instance 'demo-stopped' is excluded")


def main():
    test_single_region_structure()
    test_multi_region()
    test_excluded_stopped_instance()
    print()
    if _failures:
        print("RESULT: {} failure(s)".format(len(_failures)))
        return 1
    print("RESULT: all render-fixture tests passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
