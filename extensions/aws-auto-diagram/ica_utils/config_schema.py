"""Describe-only config schema for ICA.

This module adds a *metadata* layer beside ``default-config.yaml``. It does NOT
carry default values and does NOT change engine behavior — defaults are always
read from the YAML. It exists so front-ends (the ``ica`` CLI/TUI) can discover,
explain, and validate the full configuration surface.

Key facts (see openspec/changes/config-schema/design.md):

* Key paths use the *engine (flattened)* form, e.g. ``layout.ec2.icon_scale``
  (NOT the raw preset form ``layout.spaced.ec2.icon_scale``).
* The schema carries only ``type``, optional ``range``/``enum``, optional
  ``unit``, and a ``help`` string per key.
* The key *inventory* is discovered from the YAML at load time, so a key can
  never be missing from the inventory; only hand-authored metadata can be
  incomplete (caught by :func:`check_coverage`).
"""

import re
from dataclasses import dataclass
from pathlib import Path

import yaml

from ica_utils.config import resolve_layout_mode


# --------------------------------------------------------------------------- #
# Type predicates
# --------------------------------------------------------------------------- #

_COLOR_RE = re.compile(r"^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")


def is_color(value):
    """A color is ``#RGB``/``#RRGGBB`` or the literal ``none``."""
    if isinstance(value, str):
        if value == "none":
            return True
        return bool(_COLOR_RE.match(value))
    return False


def coerce_number(value, as_int):
    """Return value as int/float if losslessly possible, else None.

    Bools are rejected (``True`` is not a valid numeric config value).
    """
    if isinstance(value, bool):
        return None
    if as_int:
        if isinstance(value, int):
            return value
        if isinstance(value, float) and value.is_integer():
            return int(value)
        return None
    # float field accepts int or float
    if isinstance(value, (int, float)):
        return float(value)
    return None


# --------------------------------------------------------------------------- #
# Field
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class Field:
    """Metadata for a single config key. No default value is stored here."""

    type: str  # "int" | "float" | "color" | "bool" | "str" | "enum"
    help: str
    range: tuple = None  # (lo, hi) inclusive, for int/float
    enum: tuple = None  # allowed values, for type == "enum"
    unit: str = None  # e.g. "px", "scale", "opacity", "ratio"

    def validate_value(self, value):
        """Return an error string if value is invalid for this field, else None."""
        if self.type == "color":
            if not is_color(value):
                return "expected a color (#RGB, #RRGGBB, or 'none')"
            return None
        if self.type == "bool":
            if not isinstance(value, bool):
                return "expected a boolean (true/false)"
            return None
        if self.type == "str":
            if not isinstance(value, str):
                return "expected a string"
            return None
        if self.type == "enum":
            if value not in self.enum:
                return "expected one of: " + ", ".join(str(v) for v in self.enum)
            return None
        if self.type in ("int", "float"):
            num = coerce_number(value, as_int=(self.type == "int"))
            if num is None:
                return "expected " + ("an integer" if self.type == "int" else "a number")
            if self.range is not None:
                lo, hi = self.range
                if num < lo or num > hi:
                    return "out of range [{}, {}]".format(lo, hi)
            return None
        return "unknown field type {!r}".format(self.type)


# --------------------------------------------------------------------------- #
# Metadata rules
#
# Rather than hand-type 120 near-identical Field entries (which would drift),
# metadata is declared as ordered rules matched against the engine/flat key
# path. The first matching rule wins. _build_fields() expands the rules against
# the *real* key inventory from the YAML, so coverage is exhaustive by
# construction and every key path that exists gets exactly one Field.
# --------------------------------------------------------------------------- #

# Exact path -> Field (highest priority).
_EXACT = {
    "document.margin": Field(
        "int", "Whitespace margin (px) around the whole diagram", range=(0, 500), unit="px"
    ),
    "layout.mode": Field(
        "enum", "Layout density preset", enum=("spaced", "dense")
    ),
    "layout.availability_zone.enabled": Field(
        "bool", "Whether availability-zone rectangles are drawn"
    ),
    "layout.availability_zone.label_prefix": Field(
        "str", "Text prefixed to each availability-zone label"
    ),
}

# (leaf-name regex, Field-without-help) -> help is supplied per rule.
# Matched against the LAST path segment unless the pattern contains a dot.
_LEAF_RULES = [
    (r"icon_scale$", Field("float", "Scale factor applied to the symbol", range=(0.05, 5.0), unit="scale")),
    (r"font_size$", Field("int", "Label font size (px)", range=(4, 96), unit="px")),
    (r"text_dimmed_opacity$", Field("float", "Opacity of dimmed/secondary text", range=(0.0, 1.0), unit="opacity")),
    (r"_opacity$", Field("float", "Opacity value", range=(0.0, 1.0), unit="opacity")),
    # colors
    (r"background$", Field("color", "Background fill color")),
    (r"text_color$", Field("color", "Text color")),
    (r"^border_", Field("color", "Border/stroke color")),
    (r"_color$", Field("color", "Stroke/line color")),
    # stroke geometry
    (r"stroke_width$", Field("float", "Stroke width (px)", range=(0.0, 20.0), unit="px")),
    (r"span_line_width$", Field("float", "Spanning-line width (px)", range=(0.0, 20.0), unit="px")),
    (r"dasharray$", Field("str", "SVG stroke dash pattern, e.g. '4,4'")),
    # sizes / spacing
    (r"min_width$", Field("int", "Minimum width (px)", range=(0, 2000), unit="px")),
    (r"swatch_width$", Field("int", "Legend swatch width (px)", range=(0, 500), unit="px")),
    (r"swatch_height$", Field("int", "Legend swatch height (px)", range=(0, 500), unit="px")),
    (r"card_height$", Field("int", "Card height (px)", range=(0, 1000), unit="px")),
    (r"label_height$", Field("int", "Label band height (px)", range=(0, 1000), unit="px")),
    (r"height$", Field("int", "Height (px)", range=(0, 2000), unit="px")),
    (r"top_margin$", Field("int", "Top margin (px)", range=(0, 1000), unit="px")),
    (r"top_spacing$", Field("int", "Top spacing (px)", range=(0, 1000), unit="px")),
    (r"bottom_spacing$", Field("int", "Bottom spacing (px)", range=(0, 1000), unit="px")),
    (r"card_top$", Field("int", "Top inset of cards (px)", range=(0, 1000), unit="px")),
    (r"card_padding$", Field("int", "Padding inside cards (px)", range=(0, 1000), unit="px")),
    (r"card_gap$", Field("int", "Gap between cards (px)", range=(0, 1000), unit="px")),
    (r"col_gap$", Field("int", "Gap between columns (px)", range=(0, 1000), unit="px")),
    (r"row_gap$", Field("int", "Gap between rows (px)", range=(0, 1000), unit="px")),
    (r"item_gap$", Field("int", "Gap between items (px)", range=(0, 1000), unit="px")),
    (r"section_gap$", Field("int", "Gap between sections (px)", range=(0, 1000), unit="px")),
    (r"column_gap$", Field("int", "Gap between columns (px)", range=(0, 1000), unit="px")),
    (r"gap$", Field("int", "Gap (px)", range=(0, 1000), unit="px")),
    # padding leaves (top/right/bottom/left/sides)
    (r"padding\.(top|right|bottom|left|sides)$", Field("int", "Padding (px)", range=(0, 1000), unit="px")),
    (r"^padding$", Field("int", "Padding (px)", range=(0, 1000), unit="px")),
]


def _field_for(path):
    """Resolve the Field for a flat key path, or None if no rule matches.

    A rule whose pattern contains a literal dot (``\\.``) is matched against the
    full path; all other rules are matched against the last path segment only.
    First matching rule wins.
    """
    if path in _EXACT:
        return _EXACT[path]
    leaf = path.split(".")[-1]
    for pattern, field in _LEAF_RULES:
        target = path if r"\." in pattern else leaf
        if re.search(pattern, target):
            return field
    return None


# --------------------------------------------------------------------------- #
# YAML inventory helpers
# --------------------------------------------------------------------------- #


def _flatten(d, prefix=""):
    out = {}
    for k, v in d.items():
        nk = "{}.{}".format(prefix, k) if prefix else k
        if isinstance(v, dict):
            out.update(_flatten(v, nk))
        else:
            out[nk] = v
    return out


def _load_yaml(extension_dir):
    path = Path(extension_dir) / "default-config.yaml"
    with open(path, "r") as f:
        return yaml.safe_load(f)


def _resolved_layout(raw_config, mode):
    """Return the flattened layout.* dict for a given preset, non-destructively."""
    import copy

    c = copy.deepcopy(raw_config)
    resolve_layout_mode(c, mode)
    return _flatten({"layout": c["layout"]})


def inventory(extension_dir):
    """Return the set of real, engine-form key paths from default-config.yaml.

    ``layout.*`` keys are returned in flattened (post-resolve) form. The
    ``layout.mode`` selector is included since it is a real, user-settable key.
    """
    raw = _load_yaml(extension_dir)
    keys = set()
    keys.update(_flatten({"document": raw["document"]}).keys())
    keys.update(_flatten({"theme": raw["theme"]}).keys())
    keys.update(_resolved_layout(raw, "spaced").keys())
    keys.add("layout.mode")
    return keys


# --------------------------------------------------------------------------- #
# Resolved schema (metadata joined with YAML-sourced defaults)
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class ResolvedKey:
    path: str
    field: Field
    value: object  # default value, sourced from YAML (spaced for layout keys)
    preset_varying: bool = False
    spaced_value: object = None  # set when preset_varying
    dense_value: object = None  # set when preset_varying


def load_schema(extension_dir):
    """Join the metadata rules with values read from default-config.yaml.

    Returns ``dict[path -> ResolvedKey]``. Defaults come from the YAML; the
    schema never stores them. For layout keys, ``preset_varying`` is derived by
    comparing the spaced and dense presets.
    """
    raw = _load_yaml(extension_dir)
    doc = _flatten({"document": raw["document"]})
    theme = _flatten({"theme": raw["theme"]})
    spaced = _resolved_layout(raw, "spaced")
    dense = _resolved_layout(raw, "dense")

    resolved = {}

    for path, value in doc.items():
        resolved[path] = ResolvedKey(path, _field_for(path), value)
    for path, value in theme.items():
        resolved[path] = ResolvedKey(path, _field_for(path), value)

    # layout.mode selector
    resolved["layout.mode"] = ResolvedKey(
        "layout.mode", _field_for("layout.mode"), raw["layout"].get("mode", "spaced")
    )

    for path, sval in spaced.items():
        dval = dense.get(path)
        varying = (path in dense) and (sval != dval)
        resolved[path] = ResolvedKey(
            path=path,
            field=_field_for(path),
            value=sval,  # spaced is canonical default
            preset_varying=varying,
            spaced_value=sval if varying else None,
            dense_value=dval if varying else None,
        )

    return resolved


# --------------------------------------------------------------------------- #
# Validation
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class Error:
    path: str
    message: str

    def __str__(self):
        return "{}: {}".format(self.path, self.message)


def validate_override(user_dict, extension_dir):
    """Validate a user override dict against the schema.

    Pure: performs no I/O beyond reading the schema metadata + YAML inventory
    (needed to know which keys exist). Does not depend on inkex. Returns a list
    of :class:`Error`; empty list means valid. Only keys *present* in the
    override are checked (partial overrides are allowed).
    """
    schema = load_schema(extension_dir)
    errors = []
    flat = _flatten(user_dict) if user_dict else {}
    for path, value in flat.items():
        rk = schema.get(path)
        if rk is None:
            errors.append(Error(path, "unknown config key"))
            continue
        if rk.field is None:
            # key exists but has no metadata rule — coverage gap, not a user
            # error; skip validation for it
            continue
        msg = rk.field.validate_value(value)
        if msg is not None:
            errors.append(Error(path, msg))
    return errors


# --------------------------------------------------------------------------- #
# Coverage self-check
# --------------------------------------------------------------------------- #


def check_coverage(extension_dir):
    """Compare schema metadata coverage against the YAML inventory.

    Returns ``(missing_in_schema, extra_in_schema)``:

    * ``missing_in_schema``: real keys with no matching Field rule.
    * ``extra_in_schema``: Field rules / exact entries that match no real key.

    Used by tests; never invoked during rendering.
    """
    real = inventory(extension_dir)
    missing = sorted(p for p in real if _field_for(p) is None)

    # extras: exact entries whose path is not a real key
    extra = sorted(p for p in _EXACT if p not in real)
    return missing, extra


# --------------------------------------------------------------------------- #
# CLI override building (used by `ica render`)
# --------------------------------------------------------------------------- #


def _set_nested(d, dotted_path, value):
    """Set ``d[a][b][c] = value`` for a dotted path, creating dicts as needed."""
    parts = dotted_path.split(".")
    cur = d
    for p in parts[:-1]:
        nxt = cur.get(p)
        if not isinstance(nxt, dict):
            nxt = {}
            cur[p] = nxt
        cur = nxt
    cur[parts[-1]] = value


def parse_set_pairs(pairs):
    """Turn ``["a.b=1", "c=x"]`` into a nested override dict ``{a:{b:"1"}, c:"x"}``.

    Values are left as strings here; coercion to schema types happens separately
    (``coerce_override``) so unknown keys can be reported as errors rather than
    silently coerced. Raises ``ValueError`` on a pair lacking ``=``.
    """
    out = {}
    for pair in pairs:
        if "=" not in pair:
            raise ValueError("invalid --set %r (expected key=value)" % pair)
        key, value = pair.split("=", 1)
        key = key.strip()
        if not key:
            raise ValueError("invalid --set %r (empty key)" % pair)
        _set_nested(out, key, value)
    return out


def _coerce_string(field, raw):
    """Coerce a raw string to the field's type. Returns (value, error)."""
    if field.type == "int":
        try:
            return int(raw), None
        except ValueError:
            return None, "expected an integer"
    if field.type == "float":
        try:
            return float(raw), None
        except ValueError:
            return None, "expected a number"
    if field.type == "bool":
        low = raw.strip().lower()
        if low in ("true", "1", "yes", "on"):
            return True, None
        if low in ("false", "0", "no", "off"):
            return False, None
        return None, "expected a boolean (true/false)"
    # color / str / enum pass through as strings; validate_value checks them
    return raw, None


def coerce_override(override, extension_dir):
    """Coerce string-valued override leaves to their schema types.

    Returns ``(coerced_dict, errors)``. Only leaves whose value is a string are
    coerced (file-sourced overrides already have real types). Unknown keys are
    reported as errors here, before validation. ``coerced_dict`` excludes any
    leaf that errored.
    """
    schema = load_schema(extension_dir)
    flat = _flatten(override) if override else {}
    coerced = {}
    errors = []
    for path, value in flat.items():
        rk = schema.get(path)
        if rk is None:
            errors.append(Error(path, "unknown config key"))
            continue
        cv = value
        if isinstance(value, str) and rk.field is not None:
            cv, msg = _coerce_string(rk.field, value)
            if msg is not None:
                errors.append(Error(path, msg))
                continue
        # validate the (coerced) value against the field — range/enum/type
        if rk.field is not None:
            msg = rk.field.validate_value(cv)
            if msg is not None:
                errors.append(Error(path, msg))
                continue
        _set_nested(coerced, path, cv)
    return coerced, errors
