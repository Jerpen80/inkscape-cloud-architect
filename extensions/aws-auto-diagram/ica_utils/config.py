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
    """Resolve layout mode and merge selected preset into config["layout"].

    Args:
        config: Full config dict (modified in place)
        mode_override: Optional mode from INX parameter (overrides config default)
    """
    layout = config.get("layout", {})
    mode = mode_override or layout.get("mode", "spaced")

    preset = layout.get(mode, layout.get("spaced", {}))

    # Merge preset values into layout top-level
    for key, value in preset.items():
        layout[key] = value

    # Clean up mode/preset keys
    for key in ("mode", "spaced", "dense"):
        layout.pop(key, None)

    config["layout"] = layout
