import yaml
from pathlib import Path


def _deep_merge(base, override):
    """Recursively merge override dict into base dict. Override values win."""
    merged = base.copy()
    for key, value in override.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def load_config(extension_dir):
    """Load config from default-config.yaml, optionally merged with user override.

    Args:
        extension_dir: Path to the extension directory containing default-config.yaml

    Returns:
        Merged configuration dict
    """
    default_path = Path(extension_dir) / "default-config.yaml"
    with open(default_path, "r") as f:
        config = yaml.safe_load(f)

    user_path = Path.home() / ".config" / "inkscape" / "extensions" / "aws-auto-diagram" / "config.yaml"
    if user_path.exists():
        with open(user_path, "r") as f:
            user_config = yaml.safe_load(f)
        if user_config:
            config = _deep_merge(config, user_config)

    return config


def resolve_layout_mode(config, mode_override=None):
    """Resolve layout mode into config["layout"] top-level keys.

    The ``spaced`` preset holds the canonical layout values. ``dense`` is a *diff*
    overlay listing only the keys that differ from canonical; for ``mode=dense``
    the diff is deep-merged on top of the canonical base. Style keys that do not
    vary by density live only in ``spaced`` and therefore apply in both modes.

    Args:
        config: Full config dict (modified in place)
        mode_override: Optional mode from INX parameter (overrides config default)
    """
    layout = config.get("layout", {})
    mode = mode_override or layout.get("mode", "spaced")

    canonical = layout.get("spaced", {})
    if mode == "dense":
        resolved = _deep_merge(canonical, layout.get("dense", {}))
    else:
        resolved = canonical

    # Merge resolved values into layout top-level
    for key, value in resolved.items():
        layout[key] = value

    # Clean up mode/preset keys
    for key in ("mode", "spaced", "dense"):
        layout.pop(key, None)

    config["layout"] = layout
