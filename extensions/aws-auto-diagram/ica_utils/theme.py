LIGHT_DEFAULTS = {
    "background": "none",
    "text_color": "#000000",
    "text_dimmed_opacity": 0.6,
    "border_account": "#000000",
    "border_edge": "#7B61FF",
    "border_vpc": "#8c4fff",
    "border_subnet_public": "#7aa116",
    "border_subnet_private": "#00a4a6",
    "border_region": "#00a4a6",
}

DARK_DEFAULTS = {
    "background": "#232F3E",
    "text_color": "#e0e0e0",
    "text_dimmed_opacity": 0.5,
    "border_account": "#e0e0e0",
    "border_edge": "#9B81FF",
    "border_vpc": "#8c4fff",
    "border_subnet_public": "#7aa116",
    "border_subnet_private": "#00a4a6",
    "border_region": "#00a4a6",
}


def resolve_theme(theme_name, config):
    """Resolve theme name to a palette dict, merging config overrides."""
    theme_cfg = (config or {}).get("theme", {})
    if theme_name == "dark":
        defaults = DARK_DEFAULTS
        overrides = theme_cfg.get("dark", {})
    else:
        defaults = LIGHT_DEFAULTS
        overrides = theme_cfg.get("light", {})
    palette = dict(defaults)
    palette.update({k: v for k, v in overrides.items() if v is not None})
    return palette


def get_text_color(config):
    """Get text fill color from resolved theme."""
    theme = (config or {}).get("_theme", LIGHT_DEFAULTS)
    return theme.get("text_color", "#000000")


def get_text_dimmed_opacity(config):
    """Get dimmed text opacity from resolved theme."""
    theme = (config or {}).get("_theme", LIGHT_DEFAULTS)
    return theme.get("text_dimmed_opacity", 0.6)


def get_border_color(config, element):
    """Get border color for a named element from resolved theme."""
    theme = (config or {}).get("_theme", LIGHT_DEFAULTS)
    return theme.get(f"border_{element}", "#000000")


def get_background(config):
    """Get background color from resolved theme."""
    theme = (config or {}).get("_theme", LIGHT_DEFAULTS)
    return theme.get("background", "none")
